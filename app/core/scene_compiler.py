# app/core/scene_compiler.py

import uuid
from typing import Dict, List


def _uid(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def compile_scene(intent: Dict, assets: List[Dict]) -> Dict:
    """
    Converts intent + resolved assets into a spatially-correct Unreal-ready scene.
    Buildings are generated as grouped structures (floor + walls + ceiling + door).
    """

    scene_id = _uid("scene")

    scene = {
        "scene_id": scene_id,
        "scene_type": intent.get("scene_type", "generic"),
        "lighting": {
            "brightness": 10,
            "temperature": 46.6,
            "time_of_day": 6.82,
            "sun_angle": 0
        },
        "fog": {
            "density": 0.02,
            "ray_density": 0.02,
            "height": 0.2
        },
        "actors": [],
        "rules": {
            "allow_physics": intent.get("allow_physics", False),
            "allow_ai_agents": intent.get("allow_ai_agents", False),
            "allow_multiplayer": intent.get("allow_multiplayer", False)
        }
    }

    # -----------------------------
    # ASSET LOOKUP BY CATEGORY
    # -----------------------------
    asset_lookup = {}
    for asset in assets:
        asset_lookup.setdefault(asset["category"], []).append(asset)

    def get_asset(category: str, index: int = 0):
        pool = asset_lookup.get(category, [])
        if not pool:
            return None
        return pool[index % len(pool)]

    # -----------------------------
    # SPATIAL CONSTANTS (UNREAL UNITS)
    # -----------------------------
    BUILDING_SPACING_X = 6000
    BUILDING_SPACING_Y = 0

    WALL_OFFSET = 600
    CEILING_Z = 400
    DOOR_OFFSET_Y = 650

    TREE_SPACING = 1200
    ROAD_SPACING = 8000

    cursor_x = 0
    cursor_y = 0

    # -----------------------------
    # BUILDINGS
    # -----------------------------
    for obj in intent.get("objects", []):
        if obj["type"] != "building":
            continue

        building_count = obj.get("count", 1)

        floors = asset_lookup.get("floor", [])
        walls = asset_lookup.get("wall", [])
        ceilings = asset_lookup.get("ceiling", [])
        doors = asset_lookup.get("door", [])

        if not floors or not walls:
            continue  # cannot form buildings

        for b in range(building_count):
            base_x = cursor_x
            base_y = cursor_y

            # FLOOR
            floor_asset = floors[b % len(floors)]
            scene["actors"].append(_actor(floor_asset, "floor", base_x, base_y, 0))

            # WALLS (4 sides)
            wall_positions = [
                (0, WALL_OFFSET),
                (0, -WALL_OFFSET),
                (WALL_OFFSET, 0),
                (-WALL_OFFSET, 0),
            ]

            for i, (dx, dy) in enumerate(wall_positions):
                wall_asset = walls[i % len(walls)]
                scene["actors"].append(
                    _actor(wall_asset, "wall", base_x + dx, base_y + dy, 0)
                )

            # CEILING
            if ceilings:
                ceiling_asset = ceilings[b % len(ceilings)]
                scene["actors"].append(
                    _actor(ceiling_asset, "ceiling", base_x, base_y, CEILING_Z)
                )

            # DOOR (front)
            if doors:
                door_asset = doors[b % len(doors)]
                scene["actors"].append(
                    _actor(door_asset, "door", base_x, base_y + DOOR_OFFSET_Y, 0)
                )

            cursor_x += BUILDING_SPACING_X

        cursor_y += BUILDING_SPACING_Y

    # -----------------------------
    # ROADS
    # -----------------------------
    for obj in intent.get("objects", []):
        if obj["type"] != "road":
            continue

        road_assets = asset_lookup.get("road") or asset_lookup.get("track", [])
        if not road_assets:
            continue

        road_asset = road_assets[0]
        scene["actors"].append(
            _actor(road_asset, "road", 0, -ROAD_SPACING, 0)
        )

    # -----------------------------
    # TREES (DECOR AS TREE)
    # -----------------------------
    for obj in intent.get("objects", []):
        if obj["type"] != "tree":
            continue

        tree_assets = asset_lookup.get("tree") or asset_lookup.get("decor", [])
        count = obj.get("count", 1)

        if not tree_assets:
            continue

        tx = 0
        for i in range(count):
            asset = tree_assets[i % len(tree_assets)]
            scene["actors"].append(
                _actor(asset, "tree", tx, ROAD_SPACING // 2, 0)
            )
            tx += TREE_SPACING

    return scene


# -------------------------------------------------
# ACTOR FACTORY
# -------------------------------------------------
def _actor(asset: Dict, category: str, x: int, y: int, z: int) -> Dict:
    return {
        "actor_id": _uid("actor"),
        "asset_id": asset["id"],
        "name": f"{category}",
        "category": category,
        "blueprint": asset["blueprint"],
        "transform": {
            "location": {"x": x, "y": y, "z": z},
            "rotation": {"pitch": 0, "yaw": 0, "roll": 0},
            "scale": {"x": 1, "y": 1, "z": 1},
        },
        "physics": {
            "enabled": False,
            "collidable": True,
            "gravity": False,
        },
        "visibility": {
            "visible": True,
            "hidden_in_game": False,
        },
    }

from app.llm.openai_client import enhance_scene

scene = enhance_scene(scene, intent.get("notes",""))
