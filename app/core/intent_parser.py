# app/core/intent_parser.py

import re
from typing import Dict
from app.core.intent_schema import SceneIntent, ObjectIntent
from app.llm.deepseek_client import DeepSeekClient


# ---------- RULE BASED PARSER (PRIMARY) ----------

OBJECT_KEYWORDS = {
    "building": ["building", "house", "tower"],
    "road": ["road", "street", "path"],
    "tree": ["tree", "trees"],
    "door": ["door", "doors"],
    "wall": ["wall", "walls"],
    "floor": ["floor", "floors"],
    "vehicle": ["car", "vehicle"],
}


SCENE_KEYWORDS = {
    "city": ["city", "town"],
    "track": ["race", "track"],
    "building": ["building"],
    "open_world": ["open world"],
}


def _extract_count(text: str, word: str) -> int:
    """
    Extracts numeric counts like:
    - '3 buildings' → 3
    - defaults to 1 if not found
    """
    match = re.search(rf"(\d+)\s+{word}", text)
    if match:
        return int(match.group(1))
    return 1


def parse_intent(text: str) -> Dict:
    text = text.lower()

    # ---------- scene type ----------
    scene_type = "custom"
    for s_type, keywords in SCENE_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            scene_type = s_type
            break

    objects = []

    for obj_type, keywords in OBJECT_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            count = 1
            for keyword in keywords:
                count = max(count, _extract_count(text, keyword))
            objects.append(
                ObjectIntent(type=obj_type, count=count)
            )

    # ---------- fallback to AI if NOTHING found ----------
    if not objects:
        try:
            llm = DeepSeekClient()
            ai_intent = llm.parse_intent_sync(text)
            return ai_intent
        except Exception:
            pass

    intent = SceneIntent(
        scene_type=scene_type,
        objects=objects,
        notes="rule_based",
    )

    return intent.model_dump()
