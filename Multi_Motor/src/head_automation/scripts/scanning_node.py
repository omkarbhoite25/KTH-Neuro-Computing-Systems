#!/usr/bin/env python3
"""Scanning/patrol node -- sinusoidal Lissajous pattern for room coverage.

Drives head_lr and head_ud in a Lissajous figure (different frequencies)
for smooth, continuous room scanning. Eyes stay centered.
"""

import math
import time

import rospy
from std_msgs.msg import String
from head_automation.motor_interface import MotorInterface


class ScanningNode:
    def __init__(self):
        rospy.init_node('scanning_node')

        self.motor = MotorInterface()
        self.active = False

        # Load scanning parameters
        self.rate_hz = rospy.get_param('~control_rate', 50)
        self.lr_freq = rospy.get_param('~lr_frequency', 0.1)
        self.ud_freq = rospy.get_param('~ud_frequency', 0.07)
        self.lr_amp = rospy.get_param('~lr_amplitude', 400)
        self.ud_amp = rospy.get_param('~ud_amplitude', 300)
        self.lr_center = rospy.get_param('~lr_center', 2000)
        self.ud_center = rospy.get_param('~ud_center', 2450)
        self.phase = rospy.get_param('~phase_offset', math.pi / 2)

        rospy.Subscriber('/head/active_mode', String, self._mode_cb)
        rospy.on_shutdown(self._shutdown)

    def _mode_cb(self, msg):
        was_active = self.active
        self.active = (msg.data == 'scanning')
        if self.active and not was_active:
            rospy.loginfo("Scanning mode activated")
        elif not self.active and was_active:
            rospy.loginfo("Scanning mode deactivated")

    def _shutdown(self):
        self.motor.go_default()

    def run(self):
        rospy.loginfo("Scanning node ready, waiting for activation...")
        rate = rospy.Rate(self.rate_hz)
        t0 = time.time()

        while not rospy.is_shutdown():
            if not self.active or self.motor.emergency_stopped:
                rate.sleep()
                continue

            t = time.time() - t0
            two_pi = 2.0 * math.pi

            # Lissajous: different frequencies create a figure-8 like pattern
            head_lr = self.lr_center + self.lr_amp * math.sin(two_pi * self.lr_freq * t)
            head_ud = self.ud_center + self.ud_amp * math.sin(two_pi * self.ud_freq * t + self.phase)

            self.motor.set_position('head_lr', head_lr, rate_limit=True)
            self.motor.set_position('head_ud', head_ud, rate_limit=True)

            rate.sleep()


if __name__ == '__main__':
    node = ScanningNode()
    node.run()
