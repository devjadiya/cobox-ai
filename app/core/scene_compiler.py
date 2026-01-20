# app/core/scene_compiler.py
from typing import Dict, List
from app.core.difficulty import calculate_difficulty
from app.core.physics import runner_physics
from app.core.heuristics import generate_obstacles


def compile_scene(intent: Dict, assets: List[Dict]) -> Dict:
    """
    Builds a FULL endless runner scene with physics + difficulty scaling.
    """

    total_segments = 400
    segments = []

    for i in range(total_segments):
        difficulty = calculate_difficulty(i)
        physics = runner_physics(difficulty)

        segment = {
            "segment_id": i,
            "difficulty": difficulty,
            "physics": physics,
            "obstacles": generate_obstacles(i, difficulty),
            "decor": [],
            "collectibles": []
        }

        if i % 6 == 0:
            segment["collectibles"].append({
                "type": "coin",
                "lane": 0,
                "count": 3 + difficulty
            })

        if i % 10 == 0:
            segment["decor"].append("torch")

        segments.append(segment)

    return {
        "game_type": "endless_runner",
        "theme": intent.get("theme", "temple"),
        "segments": segments,
        "meta": {
            "length": total_segments,
            "difficulty_curve": "linear_100"
        }
    }
