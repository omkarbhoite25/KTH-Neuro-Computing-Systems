#!/usr/bin/env python3
"""Event camera tracking node -- tracks motion using eDVS event stream.

Algorithm:
1. Subscribe to /edvs/events (EventArray)
2. Maintain 128x128 numpy decay-weighted accumulator
3. At control_rate Hz: compute weighted centroid
4. Error = centroid offset from image center
5. Two-tier control:
   - Large error (> fine_threshold): drive head servos
   - Small error: drive eye servos for fine tracking
6. Both eyes move together (vergence)

Optionally uses a C extension (libaccumulator.so) for the hot-path
accumulator update and centroid computation.
"""

import time
import ctypes
import os

import numpy as np
import rospy
from std_msgs.msg import String
from head_automation.motor_interface import MotorInterface

# Try to load optional C accelerator for the accumulator update
_c_accel = None
_accel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           '..', 'lib', 'libaccumulator.so')
if os.path.exists(_accel_path):
    try:
        _c_accel = ctypes.CDLL(_accel_path)
        _c_accel.accumulator_update.argtypes = [
            ctypes.c_void_p,   # accumulator data pointer
            ctypes.c_int,      # width
            ctypes.c_int,      # height
            ctypes.c_void_p,   # event x array
            ctypes.c_void_p,   # event y array
            ctypes.c_int,      # num events
            ctypes.c_double,   # decay factor
        ]
        _c_accel.accumulator_update.restype = None

        _c_accel.accumulator_centroid.argtypes = [
            ctypes.c_void_p,   # accumulator data pointer
            ctypes.c_int,      # width
            ctypes.c_int,      # height
            ctypes.POINTER(ctypes.c_double),  # cx out
            ctypes.POINTER(ctypes.c_double),  # cy out
        ]
        _c_accel.accumulator_centroid.restype = ctypes.c_double
    except (OSError, AttributeError) as e:
        rospy.logwarn("Failed to load C accumulator accelerator: %s", e)
        _c_accel = None


class EventTrackingNode:
    def __init__(self):
        rospy.init_node('event_tracking_node')

        self.motor = MotorInterface()
        self.active = False

        # Load tracking parameters
        self.rate_hz = rospy.get_param('~control_rate', 30)
        self.decay_tau = rospy.get_param('~decay_tau', 0.3)
        if self.decay_tau <= 0:
            rospy.logwarn("decay_tau must be > 0, got %.4f. Using 0.3", self.decay_tau)
            self.decay_tau = 0.3
        self.kp_head = rospy.get_param('~kp_head', 3.0)
        self.kp_eye = rospy.get_param('~kp_eye', 1.5)
        self.fine_threshold = rospy.get_param('~fine_threshold', 20)
        self.max_step_head = rospy.get_param('~max_step_head', 80)
        self.max_step_eye = rospy.get_param('~max_step_eye', 40)
        self.img_w = rospy.get_param('~image_width', 128)
        self.img_h = rospy.get_param('~image_height', 128)

        # Decay-weighted accumulator (128x128)
        self.accumulator = np.zeros((self.img_h, self.img_w), dtype=np.float64)
        self.last_update = time.time()
        self.center_x = self.img_w / 2.0
        self.center_y = self.img_h / 2.0

        # Pre-compute coordinate grids for centroid calculation
        self._y_coords, self._x_coords = np.mgrid[0:self.img_h, 0:self.img_w]
        self._x_coords = self._x_coords.astype(np.float64)
        self._y_coords = self._y_coords.astype(np.float64)

        rospy.Subscriber('/head/active_mode', String, self._mode_cb)
        rospy.on_shutdown(self._shutdown)

        # Subscribe to event camera -- dvs_msgs is REQUIRED for tracking
        try:
            from dvs_msgs.msg import EventArray
            rospy.Subscriber('/edvs/events', EventArray, self._events_cb,
                             queue_size=1)
            rospy.loginfo("Subscribed to /edvs/events (dvs_msgs/EventArray)")
        except ImportError:
            rospy.logfatal(
                "dvs_msgs package not found! Event tracking requires dvs_msgs. "
                "Install with: sudo apt-get install ros-noetic-dvs-msgs "
                "or from source: https://github.com/uzh-rpg/rpg_dvs_ros")
            rospy.signal_shutdown("Missing required dependency: dvs_msgs")

    def _mode_cb(self, msg):
        was_active = self.active
        self.active = (msg.data == 'tracking')
        if self.active and not was_active:
            self.accumulator.fill(0)
            rospy.loginfo("Tracking mode activated")
        elif not self.active and was_active:
            rospy.loginfo("Tracking mode deactivated")

    def _events_cb(self, msg):
        """Handle dvs_msgs/EventArray messages."""
        if not self.active:
            return

        now = time.time()
        dt = now - self.last_update
        self.last_update = now

        # Clamp decay factor to [0, 1]
        decay = min(1.0, max(0.0, np.exp(-dt / self.decay_tau)))

        if _c_accel is not None:
            # Use C accelerator path
            ev_x = np.array([e.x for e in msg.events], dtype=np.int32)
            ev_y = np.array([e.y for e in msg.events], dtype=np.int32)
            _c_accel.accumulator_update(
                self.accumulator.ctypes.data,
                self.img_w, self.img_h,
                ev_x.ctypes.data, ev_y.ctypes.data,
                len(msg.events), decay)
        else:
            # Pure numpy/python path
            self.accumulator *= decay
            for event in msg.events:
                x = int(event.x)
                y = int(event.y)
                if 0 <= x < self.img_w and 0 <= y < self.img_h:
                    self.accumulator[y, x] += 1.0

    def _compute_centroid(self):
        """Compute weighted centroid of the accumulator."""
        if _c_accel is not None:
            cx = ctypes.c_double(0.0)
            cy = ctypes.c_double(0.0)
            total = _c_accel.accumulator_centroid(
                self.accumulator.ctypes.data,
                self.img_w, self.img_h,
                ctypes.byref(cx), ctypes.byref(cy))
            return cx.value, cy.value

        total = self.accumulator.sum()
        if total < 1e-6:
            return self.center_x, self.center_y

        cx = np.sum(self._x_coords * self.accumulator) / total
        cy = np.sum(self._y_coords * self.accumulator) / total
        return cx, cy

    def _shutdown(self):
        self.motor.go_default()

    def run(self):
        rospy.loginfo("Event tracking node ready, waiting for activation...")
        if _c_accel is not None:
            rospy.loginfo("Using C accelerator for accumulator operations")
        else:
            rospy.loginfo("Using pure numpy for accumulator (C accelerator not available)")

        rate = rospy.Rate(self.rate_hz)

        while not rospy.is_shutdown():
            if not self.active or self.motor.emergency_stopped:
                rate.sleep()
                continue

            cx, cy = self._compute_centroid()

            # Error: offset from image center (in pixels)
            err_x = cx - self.center_x  # positive = right
            err_y = cy - self.center_y  # positive = down

            err_magnitude = np.sqrt(err_x**2 + err_y**2)

            if err_magnitude > self.fine_threshold:
                # Large error: drive HEAD servos (coarse tracking)
                dx = np.clip(self.kp_head * err_x, -self.max_step_head, self.max_step_head)
                dy = np.clip(self.kp_head * err_y, -self.max_step_head, self.max_step_head)

                head_lr = self.motor.get_last_position('head_lr') + dx
                head_ud = self.motor.get_last_position('head_ud') + dy
                self.motor.set_position('head_lr', head_lr)
                self.motor.set_position('head_ud', head_ud)
            else:
                # Small error: drive EYE servos (fine tracking, vergence)
                dx = np.clip(self.kp_eye * err_x, -self.max_step_eye, self.max_step_eye)
                dy = np.clip(self.kp_eye * err_y, -self.max_step_eye, self.max_step_eye)

                # Both eyes move together (vergence)
                for eye_lr in ('reye_lr', 'leye_lr'):
                    pos = self.motor.get_last_position(eye_lr) + dx
                    self.motor.set_position(eye_lr, pos)
                for eye_ud in ('reye_ud', 'leye_ud'):
                    pos = self.motor.get_last_position(eye_ud) + dy
                    self.motor.set_position(eye_ud, pos)

            rate.sleep()


if __name__ == '__main__':
    node = EventTrackingNode()
    node.run()
