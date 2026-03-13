#!/usr/bin/env python3
"""Unit tests for sequence YAML loading and validation."""

import os
import unittest
import yaml


# Motor limits for validation
MOTOR_LIMITS = {
    'head_lr': {'min': 1500, 'max': 2500},
    'head_ud': {'min': 2000, 'max': 2900},
    'reye_lr': {'min': 1500, 'max': 2500},
    'leye_lr': {'min': 1500, 'max': 2500},
    'reye_ud': {'min': 1700, 'max': 2300},
    'leye_ud': {'min': 1700, 'max': 2300},
}


class TestSequences(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load sequences.yaml once for all tests."""
        config_path = os.path.join(
            os.path.dirname(__file__), '..', 'config', 'sequences.yaml')
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
        cls.sequences = data.get('sequences', {})

    def test_yaml_loads_successfully(self):
        """sequences.yaml should parse without errors."""
        self.assertIsInstance(self.sequences, dict)
        self.assertGreater(len(self.sequences), 0)

    def test_all_positions_within_limits(self):
        """Every position in every keyframe must be within motor limits."""
        for name, seq in self.sequences.items():
            for i, kf in enumerate(seq.get('keyframes', [])):
                for motor, pos in kf.get('positions', {}).items():
                    if motor in MOTOR_LIMITS:
                        limits = MOTOR_LIMITS[motor]
                        self.assertGreaterEqual(
                            pos, limits['min'],
                            msg="Seq '%s' kf %d: %s=%d < min %d" %
                                (name, i, motor, pos, limits['min']))
                        self.assertLessEqual(
                            pos, limits['max'],
                            msg="Seq '%s' kf %d: %s=%d > max %d" %
                                (name, i, motor, pos, limits['max']))

    def test_required_sequences_exist(self):
        """Core sequences should be defined."""
        for name in ['look_around', 'nod_yes', 'shake_no', 'scan_room']:
            self.assertIn(name, self.sequences,
                          msg="Missing required sequence: %s" % name)

    def test_keyframes_have_required_fields(self):
        """Each keyframe must have 'positions' and 'duration'."""
        for name, seq in self.sequences.items():
            keyframes = seq.get('keyframes', [])
            self.assertGreater(len(keyframes), 0,
                               msg="Sequence '%s' has no keyframes" % name)
            for i, kf in enumerate(keyframes):
                self.assertIn('positions', kf,
                              msg="Seq '%s' kf %d missing 'positions'" % (name, i))
                self.assertIn('duration', kf,
                              msg="Seq '%s' kf %d missing 'duration'" % (name, i))

    def test_looping_sequences(self):
        """scan_room should be marked as looping."""
        self.assertTrue(self.sequences['scan_room'].get('loop', False))

    def test_non_looping_sequences(self):
        """nod_yes and shake_no should not loop."""
        self.assertFalse(self.sequences['nod_yes'].get('loop', False))
        self.assertFalse(self.sequences['shake_no'].get('loop', False))

    def test_sequence_chaining_format(self):
        """Comma-separated sequence names should all be valid."""
        all_names = set(self.sequences.keys())
        # Simulate chaining: "nod_yes,shake_no"
        chain = "nod_yes,shake_no"
        for name in chain.split(','):
            self.assertIn(name.strip(), all_names)


if __name__ == '__main__':
    unittest.main()
