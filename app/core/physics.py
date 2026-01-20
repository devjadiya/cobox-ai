# app/core/physics.py
from typing import Dict


def runner_physics(difficulty: int) -> Dict:
    """
    Returns physics constants based on difficulty.
    These values NEVER come from AI.
    """

    base_speed = 8.0
    speed_increment = 0.6

    gravity = -9.8
    jump_velocity = 5.8

    return {
        "forward_speed": base_speed + (difficulty * speed_increment),
        "gravity": gravity,
        "jump_velocity": jump_velocity,
        "lane_width": 1.5,
        "max_lanes": 3
    }
