# app/core/scene_compiler.py

"""
SCENE COMPILER — FINAL STAGE

Input:
- Intent (parsed)
- Resolved assets (engine-safe descriptors)

Output:
- Deterministic scene JSON
- Unreal-ready actor definitions
"""

from typing import Dict, List
import uuid


# ---------------------------------------------------------
# GLOBAL DEFAULTS (LOCKED — DO NOT AUTO-MODIFY)
# ---------------------------------------------------------

DEFAULT_SCALE = {"x": 1, "y": 1, "z": 1}

DEFAULT_LIGHTING = {
    "brightness": 10.0,
    "temperature": 46.6,
    "time_of_day": 6.82,
    "sun_angle": 0.0
}

DEFAULT_FOG = {
    "density": 0.02,
    "ray_density": 0.02,
    "height": 0.2
}


# ---------------------------------------------------------
# MAIN ENTRY
# ---------------------------------------------------------

def compile_scene(intent: Dict, assets: List[Dict]) -> Dict:
    """
    Build final scene definition.
    """

    scene_id = f"scene-{uuid.uuid4().hex[:8]}"

    actors = []
    cursor_x = 0

    for asset in assets:
        actor = build_actor(asset, cursor_x)
        actors.append(actor)
        cursor_x += spacing_for(asset["category"])

    return {
        "scene_id": scene_id,
        "scene_type": intent.get("scene_type", "sandbox"),
        "lighting": DEFAULT_LIGHTING,
        "fog": DEFAULT_FOG,
        "actors": actors,
        "rules": {
            "allow_physics": intent.get("allow_physics", False),
            "allow_ai_agents": intent.get("allow_ai_agents", False),
            "allow_multiplayer": intent.get("allow_multiplayer", False)
        }
    }


# ---------------------------------------------------------
# ACTOR BUILDER
# ---------------------------------------------------------

def build_actor(asset: Dict, x_offset: float) -> Dict:
    """
    Convert asset descriptor into a spawnable actor.
    """

    return {
        "actor_id": f"actor-{uuid.uuid4().hex[:6]}",
        "asset_id": asset["id"],
        "name": asset["name"],
        "category": asset["category"],

        "transform": {
            "location": {
                "x": x_offset,
                "y": 0,
                "z": 0
            },
            "rotation": {
                "pitch": 0,
                "yaw": 0,
                "roll": 0
            },
            "scale": asset.get("default_scale", DEFAULT_SCALE)
        },

        "physics": {
            "enabled": False,
            "collidable": asset.get("collidable", True),
            "gravity": False
        },

        "visibility": {
            "visible": True,
            "hidden_in_game": False
        }
    }


# ---------------------------------------------------------
# PLACEMENT SPACING RULES
# ---------------------------------------------------------

def spacing_for(category: str) -> int:
    """
    Simple deterministic spacing rules.
    Prevents overlaps and snapping chaos.
    """

    if category == "floor":
        return 400
    if category == "wall":
        return 200
    if category == "door":
        return 150
    if category == "track":
        return 600
    if category == "decor":
        return 250

    return 300
