#!/usr/bin/env python3
"""Unit tests for MotorInterface -- position clamping, defaults, validation."""

import unittest
import sys
from unittest.mock import MagicMock, patch


# Mock rospy before importing the module under test
sys.modules['rospy'] = MagicMock()
sys.modules['std_msgs'] = MagicMock()
sys.modules['std_msgs.msg'] = MagicMock()
sys.modules['multi_motor'] = MagicMock()
sys.modules['multi_motor.msg'] = MagicMock()

import rospy
rospy.get_param = MagicMock(side_effect=lambda key, default=None: default)
rospy.Publisher = MagicMock()
rospy.Subscriber = MagicMock()
rospy.loginfo = MagicMock()
rospy.logwarn = MagicMock()

from head_automation.motor_interface import MotorInterface


MOCK_CONFIG = {
    'head_lr': {'id': 1, 'topic': '/head_lr', 'min': 1500, 'max': 2500, 'default': 2000},
    'head_ud': {'id': 2, 'topic': '/head_ud', 'min': 2000, 'max': 2900, 'default': 2450},
    'reye_lr': {'id': 3, 'topic': '/reye_lr', 'min': 1500, 'max': 2500, 'default': 2000},
    'leye_lr': {'id': 4, 'topic': '/leye_lr', 'min': 1500, 'max': 2500, 'default': 2000},
    'reye_ud': {'id': 5, 'topic': '/reye_ud', 'min': 1700, 'max': 2300, 'default': 2000},
    'leye_ud': {'id': 6, 'topic': '/leye_ud', 'min': 1700, 'max': 2300, 'default': 2000},
}


class TestMotorInterface(unittest.TestCase):

    def setUp(self):
        self.mi = MotorInterface(config=MOCK_CONFIG)

    def test_clamp_below_min(self):
        """Position below minimum should be clamped to min."""
        self.mi.set_position('head_lr', 1000, rate_limit=False)
        self.assertEqual(self.mi.get_last_position('head_lr'), 1500)

    def test_clamp_above_max(self):
        """Position above maximum should be clamped to max."""
        self.mi.set_position('head_lr', 3000, rate_limit=False)
        self.assertEqual(self.mi.get_last_position('head_lr'), 2500)

    def test_valid_position(self):
        """Position within range should be set exactly."""
        self.mi.set_position('head_lr', 2100, rate_limit=False)
        self.assertEqual(self.mi.get_last_position('head_lr'), 2100)

    def test_go_default(self):
        """go_default should reset all motors to their default positions."""
        self.mi.set_position('head_lr', 2400, rate_limit=False)
        self.mi.set_position('reye_ud', 2200, rate_limit=False)
        self.mi.go_default()
        self.assertEqual(self.mi.get_last_position('head_lr'), 2000)
        self.assertEqual(self.mi.get_last_position('reye_ud'), 2000)
        self.assertEqual(self.mi.get_last_position('head_ud'), 2450)

    def test_invalid_motor_name_set(self):
        """Setting position for unknown motor should raise ValueError."""
        with self.assertRaises(ValueError):
            self.mi.set_position('nonexistent', 2000)

    def test_invalid_motor_name_get(self):
        """Getting position for unknown motor should raise ValueError."""
        with self.assertRaises(ValueError):
            self.mi.get_last_position('nonexistent')

    def test_set_all_partial(self):
        """set_all with partial dict should only move specified motors."""
        self.mi.set_all({'head_lr': 2200, 'reye_ud': 1800}, rate_limit=False)
        self.assertEqual(self.mi.get_last_position('head_lr'), 2200)
        self.assertEqual(self.mi.get_last_position('reye_ud'), 1800)
        # Unspecified motors should retain default
        self.assertEqual(self.mi.get_last_position('head_ud'), 2450)

    def test_emergency_stop_blocks_commands(self):
        """After emergency stop, set_position should be silently ignored."""
        self.mi._emergency = True
        self.mi.set_position('head_lr', 2200, rate_limit=False)
        # Position should remain at default since command was blocked
        self.assertEqual(self.mi.get_last_position('head_lr'), 2000)

    def test_rate_limiting_head(self):
        """Head motors should be rate limited to max_step_head."""
        self.mi._max_step_head = 100
        self.mi.set_position('head_lr', 2000, rate_limit=False)  # Set baseline
        self.mi.set_position('head_lr', 2300, rate_limit=True)   # 300 tick jump
        # Should be clamped to 2000 + 100 = 2100
        self.assertEqual(self.mi.get_last_position('head_lr'), 2100)

    def test_rate_limiting_eye(self):
        """Eye motors should be rate limited to max_step_eye."""
        self.mi._max_step_eye = 60
        self.mi.set_position('reye_ud', 2000, rate_limit=False)
        self.mi.set_position('reye_ud', 2200, rate_limit=True)
        # Should be clamped to 2000 + 60 = 2060
        self.assertEqual(self.mi.get_last_position('reye_ud'), 2060)


if __name__ == '__main__':
    unittest.main()
