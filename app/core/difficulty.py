# app/core/difficulty.py
def calculate_difficulty(segment_index: int) -> int:
    """
    Difficulty increases every 100 segments.
    Caps at 10.
    """
    return min(10, segment_index // 100)
