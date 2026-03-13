#!/usr/bin/env python3
"""Keyframe interpolation for smooth motor trajectories.

Yields position dicts at a given rate, linearly interpolating between keyframes.
Motors not specified in a keyframe carry forward their last position.
"""


def interpolate_keyframes(keyframes, rate_hz):
    """Generator that yields interpolated position dicts between keyframes.

    Parameters
    ----------
    keyframes : list of dict
        Each keyframe: {'positions': {motor_name: value, ...}, 'duration': seconds}
        Partial keyframes (only some motors) are supported.
    rate_hz : float
        Output rate in Hz (e.g. 50 for 20ms steps). Must be > 0.

    Yields
    ------
    dict
        {motor_name: position} at each time step
    """
    if not keyframes:
        return
    if rate_hz <= 0:
        raise ValueError("rate_hz must be positive, got %s" % rate_hz)

    current_positions = {}

    # Initialize with first keyframe positions
    first_kf = keyframes[0]
    current_positions.update(first_kf.get('positions', {}))

    for i in range(len(keyframes) - 1):
        end_kf = keyframes[i + 1]
        duration = end_kf.get('duration', 1.0)

        if duration <= 0:
            # Instant jump
            current_positions.update(end_kf.get('positions', {}))
            yield dict(current_positions)
            continue

        start_pos = dict(current_positions)
        end_pos = dict(current_positions)
        end_pos.update(end_kf.get('positions', {}))

        # All motors that appear in either start or end
        all_motors = set(start_pos.keys()) | set(end_pos.keys())

        n_steps = max(1, int(duration * rate_hz))
        for step in range(n_steps):
            # Use (step + 1) / n_steps so final step reaches t=1.0
            t = (step + 1) / float(n_steps)
            frame = {}
            for motor in all_motors:
                s = start_pos.get(motor, end_pos.get(motor, 0))
                e = end_pos.get(motor, s)
                frame[motor] = s + (e - s) * t
            yield frame

        # Update current positions to end of this segment
        current_positions.update(end_kf.get('positions', {}))

    # Yield the final keyframe positions
    yield dict(current_positions)
