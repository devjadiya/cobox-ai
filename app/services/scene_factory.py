from app.services.procedural_builder import build_house
from app.services.procedural_foliage import scatter_trees
from app.services.default_properties import get_default_properties
from app.services.ai_structure import generate_scene_plan

TILE_SIZE = 500
HOUSE_GAP = 1000  # extra gap between houses


def create_scene_from_text(text: str):

    plan = generate_scene_plan(text)

    placeables = []
    foliage = []

    base_x = 500
    base_y = 500

    # -------- STRUCTURES --------
    for s in plan.get("Structures", []):
        if s["type"] == "house":

            count = s.get("count", 1)
            size = s.get("size", 2)

            # 🔹 dynamic spacing based on size
            spacing = (size * TILE_SIZE) + HOUSE_GAP

            for i in range(count):
                cx = base_x + (i * spacing)
                cy = base_y

                house_assets = build_house(
                    size=size,
                    floors=1,
                    center_x=cx,
                    center_y=cy
                )

                placeables.extend(house_assets)

    # -------- FOLIAGE --------
    for f in plan.get("Foliage", []):
        if f["type"] == "tree":
            count = f.get("count", 5)

            # deterministic scatter radius scales with structures
            radius = 2000 + (len(placeables) * 0.1)

            trees = scatter_trees(count=count, radius=radius)
            foliage.extend(trees)

    return {
        "PlaceableAssets": placeables,
        "GeometryAssets": [],
        "Text3DActors": [],
        "Foliage": foliage,
        "DefaultProperties": get_default_properties()
    }
