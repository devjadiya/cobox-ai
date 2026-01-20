# app/core/scoring.py
from typing import Dict


def calculate_multiplier(difficulty: int) -> float:
    """
    Controlled multiplier curve.
    Prevents runaway scores.
    """
    return round(1.0 + (difficulty * 0.15), 2)


def calculate_score(
    distance: int,
    coins: int,
    difficulty: int
) -> Dict:
    multiplier = calculate_multiplier(difficulty)

    base_score = (
        (distance * 10) +
        (coins * 50) +
        (difficulty * 100)
    )

    total_score = int(base_score * multiplier)

    return {
        "distance": distance,
        "coins": coins,
        "difficulty": difficulty,
        "multiplier": multiplier,
        "score": total_score
    }
