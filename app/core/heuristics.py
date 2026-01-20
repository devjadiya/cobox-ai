# app/core/heuristics.py
import random


def generate_obstacles(segment_id: int, difficulty: int):
    """
    Returns SAFE obstacle configuration.
    Never blocks all lanes.
    """

    obstacles = []

    lane_pool = [-1, 0, 1]
    max_obstacles = min(2, 1 + difficulty // 3)

    blocked_lanes = random.sample(lane_pool, k=max_obstacles)

    for lane in blocked_lanes:
        obstacles.append({
            "type": random.choice(["barrier", "hammer", "gap"]),
            "lane": lane,
            "height": random.choice(["low", "mid", "high"])
        })

    return obstacles
