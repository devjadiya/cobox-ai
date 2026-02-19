from math import ceil, sqrt

from app.services.procedural_builder import build_house
from app.services.procedural_foliage import scatter_trees
from app.services.default_properties import get_default_properties
from app.services.ai_structure import generate_scene_plan

# ⭐ NEW (SAFE IMPORT)
try:
    from app.services.tree_beautifier import generate_beautified_trees
    TREE_BEAUTIFIER_AVAILABLE = True
except Exception:
    TREE_BEAUTIFIER_AVAILABLE = False


TILE_SIZE = 500
HOUSE_GAP = 1200


# ======================================================
# GRID POSITION GENERATOR
# ======================================================

def generate_grid_positions(count, spacing):

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

    # ⭐ we store house centers for beautifier
    house_centers = []

    # ---------------- STRUCTURES ----------------
    for s in plan.get("Structures", []):

        if s["type"] != "house":
            continue

        count = s.get("count", 1)
        size = s.get("size", 2)

        spacing = (size * TILE_SIZE) + HOUSE_GAP

        positions = generate_grid_positions(count, spacing)

        for px, py in positions:

            cx = base_x + px
            cy = base_y + py

            house_assets = build_house(
                size=size,
                floors=1,
                center_x=cx,
                center_y=cy
            )

            placeables.extend(house_assets)

            # ⭐ save house position
            house_centers.append((cx, cy))

    # ---------------- FOLIAGE ----------------
        # ---------------- FOLIAGE ----------------
    from app.services.tree_beautifier import beautify_trees

    house_centers = []

    for s in plan.get("Structures", []):

        if s["type"] != "house":
            continue

        count = s.get("count", 1)
        size = s.get("size", 2)

        spacing = (size * TILE_SIZE) + HOUSE_GAP
        positions = generate_grid_positions(count, spacing)

        for px, py in positions:
            house_centers.append((base_x + px, base_y + py))


    for f in plan.get("Foliage", []):

        if f["type"] == "tree":

            trees = beautify_trees(house_centers)
            foliage.extend(trees)


    return {
        "PlaceableAssets": placeables,
        "GeometryAssets": [],
        "Text3DActors": [],
        "Foliage": foliage,
        "DefaultProperties": get_default_properties()
    }
