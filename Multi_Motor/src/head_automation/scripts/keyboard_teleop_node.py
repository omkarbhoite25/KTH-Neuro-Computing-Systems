#!/usr/bin/env python3
"""Keyboard teleop node for the robotic head.

Key mappings:
  w/s: head pitch (up/down)
  a/d: head yaw (left/right)
  Arrow keys: both eyes together (up/down/left/right)
  q/e: independent left/right eye horizontal
  +/-: adjust step size
  Space: return to default position
  Esc: emergency stop and exit
"""

import sys
import select
import termios
import tty

import rospy
from std_msgs.msg import String, Bool
from head_automation.motor_interface import MotorInterface

HELP_TEXT = """
Keyboard Teleop for Robotic Head
---------------------------------
  w/s : head pitch up/down
  a/d : head yaw left/right

  Arrow keys : both eyes together
  q/e : left/right eye horizontal offset

  +/- : adjust step size
  Space : return to default
  Esc : emergency stop & exit
---------------------------------
"""


class KeyboardTeleop:
    def __init__(self):
        rospy.init_node('keyboard_teleop_node')

        self.motor = MotorInterface()
        self.active_mode_sub = rospy.Subscriber(
            '/head/active_mode', String, self._mode_cb)
        self.active = False
        self.mode_name = 'keyboard'

        # Load params
        self.step = rospy.get_param('~step_size', 20)
        self.step_inc = rospy.get_param('~step_increment', 5)
        self.min_step = rospy.get_param('~min_step', 5)
        self.max_step = rospy.get_param('~max_step', 100)

        # Terminal settings for raw input
        self.old_settings = termios.tcgetattr(sys.stdin)

    def _mode_cb(self, msg):
        self.active = (msg.data == self.mode_name)

    def get_key(self, timeout=0.1):
        """Non-blocking key read using select.

        Handles bare Escape vs escape sequences (arrow keys) by using
        a short timeout on the follow-up read.
        """
        try:
            rlist, _, _ = select.select([sys.stdin], [], [], timeout)
            if not rlist:
                return None
            key = sys.stdin.read(1)
            # Handle escape sequences (arrow keys send \x1b[A etc.)
            if key == '\x1b':
                # Short timeout to distinguish bare Escape from escape sequence
                rlist2, _, _ = select.select([sys.stdin], [], [], 0.05)
                if rlist2:
                    extra = sys.stdin.read(2)
                    return '\x1b' + extra
                # Bare Escape key
                return '\x1b'
            return key
        except (IOError, OSError):
            return None

    def run(self):
        print(HELP_TEXT)
        print("Step size: %d ticks" % self.step)
        print("Waiting for 'keyboard' mode activation...")

        try:
            tty.setraw(sys.stdin.fileno())
            rate = rospy.Rate(20)

            while not rospy.is_shutdown():
                key = self.get_key(0.05)
                if key is None:
                    rate.sleep()
                    continue

                if self.motor.emergency_stopped:
                    if key == '\x1b':
                        break
                    continue

                # Always handle emergency stop
                if key == '\x1b' and len(key) == 1:
                    rospy.logwarn("Emergency stop triggered by Esc key")
                    estop_pub = rospy.Publisher(
                        '/head/emergency_stop', Bool, queue_size=1)
                    rospy.sleep(0.1)
                    estop_pub.publish(Bool(data=True))
                    break

                if not self.active:
                    rate.sleep()
                    continue

                config = self.motor.get_config()
                moved = False

                # Head yaw (left-right)
                if key == 'a':
                    pos = self.motor.get_last_position('head_lr') - self.step
                    self.motor.set_position('head_lr', pos, rate_limit=False)
                    moved = True
                elif key == 'd':
                    pos = self.motor.get_last_position('head_lr') + self.step
                    self.motor.set_position('head_lr', pos, rate_limit=False)
                    moved = True

                # Head pitch (up-down)
                elif key == 'w':
                    pos = self.motor.get_last_position('head_ud') - self.step
                    self.motor.set_position('head_ud', pos, rate_limit=False)
                    moved = True
                elif key == 's':
                    pos = self.motor.get_last_position('head_ud') + self.step
                    self.motor.set_position('head_ud', pos, rate_limit=False)
                    moved = True

                # Both eyes up (arrow up)
                elif key == '\x1b[A':
                    for eye in ('reye_ud', 'leye_ud'):
                        pos = self.motor.get_last_position(eye) - self.step
                        self.motor.set_position(eye, pos, rate_limit=False)
                    moved = True

                # Both eyes down (arrow down)
                elif key == '\x1b[B':
                    for eye in ('reye_ud', 'leye_ud'):
                        pos = self.motor.get_last_position(eye) + self.step
                        self.motor.set_position(eye, pos, rate_limit=False)
                    moved = True

                # Both eyes left (arrow left)
                elif key == '\x1b[D':
                    for eye in ('reye_lr', 'leye_lr'):
                        pos = self.motor.get_last_position(eye) - self.step
                        self.motor.set_position(eye, pos, rate_limit=False)
                    moved = True

                # Both eyes right (arrow right)
                elif key == '\x1b[C':
                    for eye in ('reye_lr', 'leye_lr'):
                        pos = self.motor.get_last_position(eye) + self.step
                        self.motor.set_position(eye, pos, rate_limit=False)
                    moved = True

                # Left eye only
                elif key == 'q':
                    pos = self.motor.get_last_position('leye_lr') - self.step
                    self.motor.set_position('leye_lr', pos, rate_limit=False)
                    moved = True
                elif key == 'e':
                    pos = self.motor.get_last_position('leye_lr') + self.step
                    self.motor.set_position('leye_lr', pos, rate_limit=False)
                    moved = True

                # Adjust step size
                elif key == '+' or key == '=':
                    self.step = min(self.max_step, self.step + self.step_inc)
                elif key == '-':
                    self.step = max(self.min_step, self.step - self.step_inc)

                # Return to default
                elif key == ' ':
                    self.motor.go_default()
                    moved = True

                rate.sleep()

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
            print("\nKeyboard teleop stopped.")

    def shutdown(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)


if __name__ == '__main__':
    node = KeyboardTeleop()
    rospy.on_shutdown(node.shutdown)
    node.run()
