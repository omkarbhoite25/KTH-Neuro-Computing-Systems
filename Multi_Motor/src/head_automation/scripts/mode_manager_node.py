#!/usr/bin/env python3
"""Mode manager node -- coordinates exclusive motor access between automation modes.

Only one mode is active at a time. Publishes the active mode name on
/head/active_mode so all mode nodes can check whether they should be publishing.

Valid modes: idle, keyboard, scanning, sequence, tracking
On 'idle': all modes stop, head returns to default position.
On shutdown: auto-switches to idle.
"""

import rospy
from std_msgs.msg import String, Bool
from head_automation.msg import ModeCommand
from head_automation.motor_interface import MotorInterface

VALID_MODES = {'idle', 'keyboard', 'scanning', 'sequence', 'tracking'}


class ModeManagerNode:
    def __init__(self):
        rospy.init_node('mode_manager_node')

        self.motor = MotorInterface()
        self.current_mode = 'idle'

        self.mode_pub = rospy.Publisher(
            '/head/active_mode', String, queue_size=1, latch=True)
        self.estop_pub = rospy.Publisher(
            '/head/emergency_stop', Bool, queue_size=1)

        rospy.Subscriber('/head/mode_command', ModeCommand, self._command_cb)
        rospy.Subscriber('/head/emergency_stop', Bool, self._estop_cb)

        rospy.on_shutdown(self._shutdown)

        # Publish initial mode
        self.mode_pub.publish(String(data=self.current_mode))
        rospy.loginfo("Mode manager started. Current mode: %s", self.current_mode)

    def _command_cb(self, msg):
        """Handle mode switch commands."""
        mode = msg.mode.lower().strip()
        action = msg.action.lower().strip()

        if mode not in VALID_MODES:
            rospy.logerr("Unknown mode '%s'. Valid modes: %s",
                         mode, VALID_MODES)
            return

        if action == 'start':
            if mode == self.current_mode:
                rospy.loginfo("Already in '%s' mode", mode)
                return

            rospy.loginfo("Switching from '%s' to '%s'", self.current_mode, mode)
            self.current_mode = mode
            self.mode_pub.publish(String(data=self.current_mode))

            if mode == 'idle':
                rospy.loginfo("Idle mode: returning to default positions")
                self.motor.go_default()

        elif action == 'stop':
            if self.current_mode == mode or mode == 'idle':
                rospy.loginfo("Stopping '%s', switching to idle", self.current_mode)
                self.current_mode = 'idle'
                self.mode_pub.publish(String(data=self.current_mode))
                self.motor.go_default()

    def _estop_cb(self, msg):
        """Handle emergency stop. Send False to clear."""
        if msg.data:
            rospy.logwarn("Emergency stop received! Switching to idle.")
            self.current_mode = 'idle'
            self.mode_pub.publish(String(data='idle'))
        else:
            rospy.loginfo("Emergency stop cleared. Clearing motor interface e-stop.")
            self.motor.clear_emergency()

    def _shutdown(self):
        """On shutdown, switch to idle and return to default."""
        rospy.loginfo("Shutdown: switching to idle")
        self.current_mode = 'idle'
        self.mode_pub.publish(String(data='idle'))
        self.motor.go_default()
        rospy.sleep(0.5)  # Give time for the message to publish

    def run(self):
        rospy.spin()


if __name__ == '__main__':
    node = ModeManagerNode()
    node.run()
