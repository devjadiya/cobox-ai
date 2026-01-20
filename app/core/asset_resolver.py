# app/core/asset_resolver.py
from typing import Dict, List


def resolve_assets(intent: Dict, asset_index: Dict) -> List[Dict]:
    """
    Maps intent objects → concrete engine assets.
    """
    resolved = []

    for obj in intent.get("objects", []):
        obj_type = obj.get("type")
        candidates = asset_index.get(obj_type, [])

        if candidates:
            resolved.append(candidates[0])  # deterministic for now

    return resolved
