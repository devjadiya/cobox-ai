# app/core/hud.py
from typing import Dict
from app.core.scoring import calculate_score
from app.core.physics import runner_physics


def build_hud_state(
    segment_index: int,
    coins_collected: int
) -> Dict:
    difficulty = min(10, segment_index // 100)
    physics = runner_physics(difficulty)
    score_data = calculate_score(
        distance=segment_index,
        coins=coins_collected,
        difficulty=difficulty
    )

    return {
        "distance": segment_index,
        "coins": coins_collected,
        "speed": physics["forward_speed"],
        "difficulty": difficulty,
        "multiplier": score_data["multiplier"],
        "score": score_data["score"],
        "status": "running"
    }
