#!/usr/bin/env python3
"""Unit tests for keyframe interpolation."""

import unittest
import sys
from unittest.mock import MagicMock

# No ROS dependency needed for interpolation
from head_automation.interpolation import interpolate_keyframes


class TestInterpolation(unittest.TestCase):

    def test_two_keyframes_linear(self):
        """Linear interpolation between two keyframes."""
        keyframes = [
            {'positions': {'head_lr': 1000}, 'duration': 0},
            {'positions': {'head_lr': 2000}, 'duration': 1.0},
        ]
        frames = list(interpolate_keyframes(keyframes, rate_hz=10))
        # Should have 10 interpolated frames + 1 final
        self.assertGreater(len(frames), 5)
        # First frame should be near start
        self.assertAlmostEqual(frames[0]['head_lr'], 1000, delta=150)
        # Last frame should be at end
        self.assertAlmostEqual(frames[-1]['head_lr'], 2000, delta=1)

    def test_partial_keyframes(self):
        """Unspecified motors should carry forward."""
        keyframes = [
            {'positions': {'head_lr': 1000, 'head_ud': 2000}, 'duration': 0},
            {'positions': {'head_lr': 2000}, 'duration': 1.0},
        ]
        frames = list(interpolate_keyframes(keyframes, rate_hz=10))
        # head_ud should be 2000 throughout (carried forward)
        for frame in frames:
            self.assertAlmostEqual(frame['head_ud'], 2000, delta=1)

    def test_single_keyframe(self):
        """Single keyframe should yield one frame."""
        keyframes = [
            {'positions': {'head_lr': 1500}, 'duration': 0},
        ]
        frames = list(interpolate_keyframes(keyframes, rate_hz=50))
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0]['head_lr'], 1500)

    def test_zero_duration_instant_jump(self):
        """Zero-duration keyframe should produce instant jump."""
        keyframes = [
            {'positions': {'head_lr': 1000}, 'duration': 0},
            {'positions': {'head_lr': 3000}, 'duration': 0},
        ]
        frames = list(interpolate_keyframes(keyframes, rate_hz=50))
        # Should be a small number of frames (instant jump + final)
        self.assertLessEqual(len(frames), 3)
        self.assertAlmostEqual(frames[-1]['head_lr'], 3000, delta=1)

    def test_empty_keyframes(self):
        """Empty keyframes should yield nothing."""
        frames = list(interpolate_keyframes([], rate_hz=50))
        self.assertEqual(len(frames), 0)

    def test_three_keyframes(self):
        """Three keyframes should produce smooth transitions."""
        keyframes = [
            {'positions': {'head_lr': 1000}, 'duration': 0},
            {'positions': {'head_lr': 2000}, 'duration': 0.5},
            {'positions': {'head_lr': 1500}, 'duration': 0.5},
        ]
        frames = list(interpolate_keyframes(keyframes, rate_hz=20))
        # Should have frames spanning both segments
        self.assertGreater(len(frames), 10)
        # Final should be at 1500
        self.assertAlmostEqual(frames[-1]['head_lr'], 1500, delta=1)


if __name__ == '__main__':
    unittest.main()
