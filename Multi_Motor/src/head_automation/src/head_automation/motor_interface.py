#!/usr/bin/env python3
"""Shared motor publisher interface with limit enforcement and emergency stop.

All automation nodes use MotorInterface to publish position commands.
This ensures consistent clamping, rate limiting, and emergency stop handling.
"""

import threading
import rospy
from std_msgs.msg import Bool, String
from multi_motor.msg import Control


class MotorInterface:
    """Abstraction over the 6 motor position topics with safety enforcement."""

    def __init__(self, config=None):
        """Initialize publishers and load motor config from parameter server.

        Parameters
        ----------
        config : dict, optional
            Motor config dict. If None, loads from /motor_limits on param server.
        """
        if config is None:
            config = rospy.get_param('/motor_limits/motors', {})
        if not config:
            rospy.logerr("MotorInterface: motor config is EMPTY! "
                         "Check that motor_limits.yaml is loaded on the param server.")
        self._config = config
        self._publishers = {}
        self._speed_pub = rospy.Publisher('/set_speed', Control, queue_size=1)
        self._emergency = False
        self._emergency_logged = False
        self._lock = threading.Lock()
        self._last_positions = {}

        # Load safety params
        self._max_step_head = rospy.get_param('/motor_limits/max_step_head', 100)
        self._max_step_eye = rospy.get_param('/motor_limits/max_step_eye', 60)

        # Create a publisher for each motor
        for name, mc in self._config.items():
            topic = mc['topic']
            self._publishers[name] = rospy.Publisher(topic, Control, queue_size=1)
            self._last_positions[name] = mc['default']

        # Emergency stop subscriber
        rospy.Subscriber('/head/emergency_stop', Bool, self._emergency_cb)

    def _emergency_cb(self, msg):
        if msg.data and not self._emergency:
            rospy.logwarn("EMERGENCY STOP activated!")
            self._emergency = True
            self._emergency_logged = False
        elif not msg.data and self._emergency:
            rospy.loginfo("Emergency stop cleared via topic")
            self._emergency = False

    def _clamp(self, name, value):
        """Clamp position to motor limits."""
        mc = self._config[name]
        clamped = max(mc['min'], min(mc['max'], int(value)))
        if clamped != int(value):
            rospy.loginfo("Clamped %s: %d -> %d", name, int(value), clamped)
        return clamped

    def _rate_limit(self, name, target):
        """Apply rate limiting to prevent jerky movements."""
        with self._lock:
            last = self._last_positions.get(name, target)
        motor_id = self._config[name]['id']
        max_step = self._max_step_head if motor_id <= 2 else self._max_step_eye
        delta = target - last
        if abs(delta) > max_step:
            target = last + max_step * (1 if delta > 0 else -1)
        return target

    def set_position(self, motor_name, position, rate_limit=True):
        """Set a motor position with clamping and optional rate limiting.

        Parameters
        ----------
        motor_name : str
            Motor name (e.g. 'head_lr', 'reye_ud')
        position : float
            Target position in ticks
        rate_limit : bool
            Whether to apply rate limiting (default True)

        Returns
        -------
        bool
            True if command was sent, False if blocked (emergency stop)
        """
        if self._emergency:
            if not self._emergency_logged:
                rospy.logwarn_throttle(5.0, "Commands blocked: emergency stop active")
                self._emergency_logged = True
            return False
        if motor_name not in self._config:
            raise ValueError("Unknown motor: %s" % motor_name)

        pos = self._clamp(motor_name, position)
        if rate_limit:
            pos = self._rate_limit(motor_name, pos)

        msg = Control()
        msg.position = pos
        self._publishers[motor_name].publish(msg)
        with self._lock:
            self._last_positions[motor_name] = pos
        return True

    def set_speed(self, motor_id, speed):
        """Set motor speed."""
        if self._emergency:
            return False
        msg = Control()
        msg.id = motor_id
        msg.speed = speed
        self._speed_pub.publish(msg)
        return True

    def set_all(self, positions_dict, rate_limit=True):
        """Set multiple motors at once.

        Parameters
        ----------
        positions_dict : dict
            {motor_name: position} for motors to move
        rate_limit : bool
            Whether to apply rate limiting
        """
        for name, pos in positions_dict.items():
            if name in self._config:
                self.set_position(name, pos, rate_limit=rate_limit)

    def go_default(self):
        """Return all motors to their default positions (no rate limiting)."""
        for name, mc in self._config.items():
            self.set_position(name, mc['default'], rate_limit=False)
        rospy.loginfo("All motors returning to default positions")

    def get_last_position(self, motor_name):
        """Get last commanded position for a motor.

        Raises ValueError if motor_name is unknown.
        """
        if motor_name not in self._config:
            raise ValueError("Unknown motor: %s" % motor_name)
        with self._lock:
            return self._last_positions[motor_name]

    def get_config(self):
        """Get the motor configuration dict."""
        return self._config

    @property
    def emergency_stopped(self):
        return self._emergency

    def clear_emergency(self):
        self._emergency = False
        self._emergency_logged = False
        rospy.loginfo("Emergency stop cleared")
