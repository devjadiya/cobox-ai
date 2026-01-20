def generate_blueprint(intent_json: dict) -> dict:
    """
    Generates high-level blueprint only.
    No engine IDs.
    No coordinates.
    """
    return {
        "genre": "endless_runner",
        "lanes": 3,
        "segments": 120,
        "obstacles": ["wall", "gap", "hammer"],
        "foliage": ["bush", "tree"],
        "difficulty_curve": "linear"
    }
