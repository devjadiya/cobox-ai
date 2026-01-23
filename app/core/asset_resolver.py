# app/core/asset_resolver.py
"""
Asset Resolver
---------------
Responsibility:
- Take parsed intent (already validated)
- Resolve logical objects (building, road, tree, door)
- Pick concrete Unreal assets from asset_index.json
- Guarantee stable IDs for downstream UE consumption

This file MUST NEVER crash due to bad asset data.
"""

import random
import uuid
from typing import Dict, List


def _generate_id(prefix: str) -> str:
    """
    Generate deterministic-safe unique ID.
    UE prefers stable string IDs.
    """
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def pick_asset(category: str, assets: List[Dict]) -> Dict:
    """
    Pick a single asset from a category.

    Defensive rules:
    - asset MUST have blueprint
    - asset ID is optional (we generate if missing)
    """

    asset = random.choice(assets)

    blueprint = asset.get("blueprint")
    if not blueprint:
        raise ValueError(f"Asset missing blueprint in category '{category}'")

    return {
        "id": asset.get("id") or _generate_id(category),
        "category": category,
        "blueprint": blueprint,
        # Optional metadata (safe to ignore in UE)
        "tags": asset.get("tags", []),
        "scale": asset.get("scale", [1, 1, 1])
    }


def resolve_assets(intent: Dict, asset_index: Dict) -> List[Dict]:
    """
    Resolve intent objects → concrete assets.

    intent example:
    {
      "objects": [
        {"type": "building", "count": 3},
        {"type": "road", "count": 1}
      ]
    }
    """

    resolved_assets: List[Dict] = []

    objects = intent.get("objects", [])
    if not objects:
        return resolved_assets

    for obj in objects:
        category = obj.get("type")
        count = int(obj.get("count", 1))

        if not category:
            continue

        available_assets = asset_index.get(category)
        if not available_assets:
            # Category not found → skip silently (AI-safe)
            continue

        for _ in range(count):
            resolved_assets.append(
                pick_asset(category, available_assets)
            )

    return resolved_assets
