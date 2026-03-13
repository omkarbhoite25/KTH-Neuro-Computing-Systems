#!/usr/bin/env python3
"""Sequence player node -- plays named keyframe sequences from YAML config.

Receives sequence name via ModeCommand.param. Supports looping and
chaining (comma-separated names). Uses interpolation.py for smooth playback.
"""

import rospy
import yaml
from std_msgs.msg import String
from head_automation.motor_interface import MotorInterface
from head_automation.interpolation import interpolate_keyframes
from head_automation.msg import ModeCommand


class SequencePlayerNode:
    def __init__(self):
        rospy.init_node('sequence_player_node')

        self.motor = MotorInterface()
        self.active = False
        self.current_sequence = None
        self.playing = False

        # Load sequences from YAML config
        config_path = rospy.get_param(
            '~sequences_file', '')
        self.sequences = {}
        self._load_sequences(config_path)

        self.rate_hz = 50  # Playback rate

        rospy.Subscriber('/head/active_mode', String, self._mode_cb)
        rospy.Subscriber('/head/mode_command', ModeCommand, self._command_cb)
        rospy.on_shutdown(self._shutdown)

    def _load_sequences(self, config_path):
        """Load sequences from param server or YAML file."""
        # Try param server first
        seq_data = rospy.get_param('~sequences', None)
        if seq_data is None and config_path:
            try:
                with open(config_path, 'r') as f:
                    data = yaml.safe_load(f)
                    seq_data = data.get('sequences', {})
            except (IOError, yaml.YAMLError) as e:
                rospy.logerr("Failed to load sequences: %s", e)
                return

        if seq_data:
            self.sequences = seq_data
            # Validate all keyframe positions are within motor limits
            config = self.motor.get_config()
            for name, seq in self.sequences.items():
                for i, kf in enumerate(seq.get('keyframes', [])):
                    for motor, pos in kf.get('positions', {}).items():
                        if motor in config:
                            mc = config[motor]
                            if pos < mc['min'] or pos > mc['max']:
                                rospy.logwarn(
                                    "Sequence '%s' keyframe %d: %s=%d out of range [%d,%d]",
                                    name, i, motor, pos, mc['min'], mc['max'])
            rospy.loginfo("Loaded %d sequences: %s",
                          len(self.sequences), list(self.sequences.keys()))

    def _mode_cb(self, msg):
        was_active = self.active
        self.active = (msg.data == 'sequence')
        if not self.active and was_active:
            self.playing = False
            rospy.loginfo("Sequence mode deactivated")

    def _command_cb(self, msg):
        if msg.mode != 'sequence':
            return
        if msg.action == 'start' and msg.param:
            self.current_sequence = msg.param
            self.playing = True
            rospy.loginfo("Starting sequence: %s", msg.param)
        elif msg.action == 'stop':
            self.playing = False
            rospy.loginfo("Stopping sequence playback")

    def _shutdown(self):
        self.motor.go_default()

    def _play_sequence(self, name):
        """Play a single sequence by name."""
        if name not in self.sequences:
            rospy.logerr("Unknown sequence: %s", name)
            return

        seq = self.sequences[name]
        keyframes = seq.get('keyframes', [])
        loop = seq.get('loop', False)

        if not keyframes:
            rospy.logwarn("Sequence '%s' has no keyframes", name)
            return

        rate = rospy.Rate(self.rate_hz)

        while not rospy.is_shutdown() and self.playing and self.active:
            for positions in interpolate_keyframes(keyframes, self.rate_hz):
                if not self.playing or not self.active:
                    return
                if self.motor.emergency_stopped:
                    return

                self.motor.set_all(positions, rate_limit=True)
                rate.sleep()

            if not loop:
                break

        self.playing = False

    def run(self):
        rospy.loginfo("Sequence player ready, waiting for activation...")
        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            if self.playing and self.active and self.current_sequence:
                # Support chaining: comma-separated sequence names
                names = [n.strip() for n in self.current_sequence.split(',')]
                for name in names:
                    if not self.playing or not self.active:
                        break
                    self._play_sequence(name)
                self.playing = False
                self.current_sequence = None
            else:
                rate.sleep()


if __name__ == '__main__':
    node = SequencePlayerNode()
    node.run()
