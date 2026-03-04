import hashlib
import random
from math import sqrt, ceil

from app.services.procedural_builder import build_house
from app.services.default_properties import get_default_properties
from app.services.ai_structure import generate_scene_plan

from app.services.tree_beautifier import beautify_trees
from app.services.foliage_layer import generate_foliage
from app.services.stone_layer import generate_stones
from app.services.geometry_layer import generate_geometry


# ---------------------------------------------------
# WORLD CONSTANTS
# ---------------------------------------------------

TILE = 500
HOUSE_GAP = 3200

BASE_X = 2000
BASE_Y = 2000


# ---------------------------------------------------
# INTENT PARSER
# ---------------------------------------------------

def detect_scene_modifiers(text: str):

    t = text.lower()

    density = 1.0
    scene_type = "default"

    spawn_geometry = False
    spawn_nature = True
    spawn_houses = True

    # density
    if "low" in t:
        density = 0.5
    if "medium" in t:
        density = 1.0
    if "high" in t or "dense" in t:
        density = 2.0

    # scene types
    if "village" in t:
        scene_type = "village"
        density *= 1.4

    if "city" in t:
        scene_type = "city"
        density *= 0.4

    # explicit filters
    if "only house" in t or "only houses" in t:
        spawn_nature = False

    if "only tree" in t or "only trees" in t:
        spawn_houses = False

    if "geometry" in t:
        spawn_geometry = True

    return density, scene_type, spawn_geometry, spawn_nature, spawn_houses


# ---------------------------------------------------
# GRID POSITION GENERATOR
# ---------------------------------------------------

def generate_positions(count, spacing):

    cols = ceil(sqrt(count))
    rows = ceil(count / cols)

    positions = []
    index = 0

    for r in range(rows):
        for c in range(cols):

            if index >= count:
                break

            x = BASE_X + c * spacing
            y = BASE_Y + r * spacing

            positions.append((x, y))
            index += 1

    return positions


# ---------------------------------------------------
# MAIN SCENE FACTORY
# ---------------------------------------------------

def create_scene_from_text(text: str):

    text = text or ""

    plan = generate_scene_plan(text)
    structures = plan.get("Structures", [])
    foliage_plan = plan.get("Foliage", [])

    # ------------------------------------------------
    # SEEDS
    # ------------------------------------------------

    layout_seed = int(hashlib.md5(text.encode()).hexdigest(), 16) % 10_000_000
    layout_rng = random.Random(layout_seed)
    style_rng = random.SystemRandom()

    # ------------------------------------------------
    # INTENT
    # ------------------------------------------------

    density_multiplier, scene_type, spawn_geometry, spawn_nature, spawn_houses = detect_scene_modifiers(text)

    # ------------------------------------------------
    # STRUCTURE SETTINGS
    # ------------------------------------------------

    house_count = 0
    size = 3

    if structures:
        house_count = structures[0].get("count", 1)
        size = max(3, structures[0].get("size", 3))

    # ------------------------------------------------
    # COUNTS
    # ------------------------------------------------

    house_area = size * size
    total_area = max(1, house_area * max(1, house_count))

    grass_count = int(10 * total_area * density_multiplier)
    bush_count = int(6 * total_area * density_multiplier)
    stone_count = int(4 * total_area * density_multiplier)
    tree_count = int(5 * house_count)  # ------------------------------------------------
    # OUTPUT ARRAYS
    # ------------------------------------------------

    placeables = []
    foliage = []
    geometry_assets = []

    houses = []
    house_centers = []

    # ------------------------------------------------
    # HOUSE GENERATION
    # ------------------------------------------------

    if spawn_houses and house_count > 0:

        spacing = (size * TILE) + 1200
        positions = [(BASE_X + i * spacing, BASE_Y) for i in range(house_count)]
        for (px, py) in positions:

            cx = px
            cy = py

            center_x = cx + ((size - 1) * TILE) / 2
            center_y = cy + ((size - 1) * TILE) / 2

            houses.append({
                "x": center_x,
                "y": center_y,
                "r": (size * TILE) / 2
            })

            house_centers.append((center_x, center_y))

            house_assets = build_house(
                size=size,
                center_x=cx,
                center_y=cy,
                style_seed=style_rng.randint(0, 999999999)
            )

            placeables.extend(house_assets)

    # ------------------------------------------------
    # TREE GENERATION
    # ------------------------------------------------

    if spawn_nature and foliage_plan:

        for f in foliage_plan:

            if f["type"] == "tree":

                # tree-only scenes
                if not house_centers:

                    house_centers = [(BASE_X, BASE_Y)]

                trees = beautify_trees(
                    houses=house_centers,
                    size=size,
                    total_count=tree_count,
                    layout_rng=layout_rng,
                    style_rng=style_rng
                )

                foliage.extend(trees)

    # ------------------------------------------------
    # FOLIAGE LAYER
    # ------------------------------------------------

    if spawn_nature and houses:

        grass_layer = generate_foliage(
            houses=houses,
            grass_count=grass_count,
            bush_count=bush_count,
            layout_rng=layout_rng,
            style_rng=style_rng,
            scene_type=scene_type
        )

        foliage.extend(grass_layer)

        stones = generate_stones(
            houses=houses,
            stone_count=stone_count,
            layout_rng=layout_rng,
            style_rng=style_rng,
            scene_type=scene_type
        )

        foliage.extend(stones)

    # ------------------------------------------------
    # GEOMETRY
    # ------------------------------------------------

    if spawn_geometry or scene_type == "city":

        geometry_assets = generate_geometry(
            style_rng=style_rng
        )

    # ------------------------------------------------
    # FINAL JSON
    # ------------------------------------------------

    return {

        "PlaceableAssets": placeables,

        "GeometryAssets": geometry_assets,

        "Text3DActors": [],

        "Foliage": foliage,

        "DefaultProperties": get_default_properties()
    }