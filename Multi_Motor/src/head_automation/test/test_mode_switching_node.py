#!/usr/bin/env python3
"""Integration test: verify mode switching via mode_manager_node."""

import unittest
import rospy
import rostest
from std_msgs.msg import String
from head_automation.msg import ModeCommand


class TestModeSwitching(unittest.TestCase):

    def setUp(self):
        self.active_mode = None
        self.mode_pub = rospy.Publisher(
            '/head/mode_command', ModeCommand, queue_size=1)
        rospy.Subscriber('/head/active_mode', String, self._mode_cb)
        rospy.sleep(1.0)  # Wait for connections

    def _mode_cb(self, msg):
        self.active_mode = msg.data

    def test_initial_mode_is_idle(self):
        """Mode manager should start in idle mode."""
        rospy.sleep(0.5)
        self.assertEqual(self.active_mode, 'idle')

    def test_switch_to_scanning(self):
        """Switching to scanning mode should update active_mode."""
        cmd = ModeCommand()
        cmd.mode = 'scanning'
        cmd.action = 'start'
        self.mode_pub.publish(cmd)
        rospy.sleep(0.5)
        self.assertEqual(self.active_mode, 'scanning')

    def test_switch_to_idle(self):
        """Switching to idle should deactivate all modes."""
        cmd = ModeCommand()
        cmd.mode = 'scanning'
        cmd.action = 'start'
        self.mode_pub.publish(cmd)
        rospy.sleep(0.3)

        cmd.mode = 'idle'
        cmd.action = 'start'
        self.mode_pub.publish(cmd)
        rospy.sleep(0.5)
        self.assertEqual(self.active_mode, 'idle')

    def test_invalid_mode_rejected(self):
        """Invalid mode name should not change the active mode."""
        # Start from idle
        rospy.sleep(0.3)
        current = self.active_mode

        cmd = ModeCommand()
        cmd.mode = 'nonexistent_mode'
        cmd.action = 'start'
        self.mode_pub.publish(cmd)
        rospy.sleep(0.5)

        self.assertEqual(self.active_mode, current)


if __name__ == '__main__':
    rospy.init_node('test_mode_switching')
    rostest.rosrun('head_automation', 'test_mode_switching', TestModeSwitching)
