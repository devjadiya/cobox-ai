from math import ceil, sqrt

from app.services.procedural_builder import build_house
from app.services.procedural_foliage import scatter_trees
from app.services.default_properties import get_default_properties
from app.services.ai_structure import generate_scene_plan


TILE_SIZE = 500
HOUSE_GAP = 1200  # spacing between buildings


# ======================================================
# GRID POSITION GENERATOR (NEW)
# ======================================================

def generate_grid_positions(count, spacing):

    """
    Places houses in square grid automatically.

    Examples:
    1 -> 1x1
    2 -> 2x1
    4 -> 2x2
    6 -> 3x2
    9 -> 3x3
    """

    cols = ceil(sqrt(count))
    rows = ceil(count / cols)

    positions = []

    start_x = 0
    start_y = 0

    index = 0

    for r in range(rows):
        for c in range(cols):

            if index >= count:
                break

            x = start_x + c * spacing
            y = start_y + r * spacing

            positions.append((x, y))
            index += 1

    return positions


# ======================================================
# MAIN SCENE FACTORY
# ======================================================

def create_scene_from_text(text: str):

    plan = generate_scene_plan(text)

    placeables = []
    foliage = []

    base_x = 500
    base_y = 500

    # ---------------- STRUCTURES ----------------
    for s in plan.get("Structures", []):

        if s["type"] != "house":
            continue

        count = s.get("count", 1)
        size = s.get("size", 2)

        # dynamic spacing based on house size
        spacing = (size * TILE_SIZE) + HOUSE_GAP

        # ⭐ NEW GRID LOGIC
        positions = generate_grid_positions(count, spacing)

        for px, py in positions:

            house_assets = build_house(
                size=size,
                floors=1,
                center_x=base_x + px,
                center_y=base_y + py
            )

            placeables.extend(house_assets)

    # ---------------- FOLIAGE ----------------
    for f in plan.get("Foliage", []):

        if f["type"] == "tree":

            count = f.get("count", 5)

            radius = 2500 + (len(placeables) * 0.08)

            trees = scatter_trees(count=count, radius=radius)
            foliage.extend(trees)

    return {
        "PlaceableAssets": placeables,
        "GeometryAssets": [],
        "Text3DActors": [],
        "Foliage": foliage,
        "DefaultProperties": get_default_properties()
    }
