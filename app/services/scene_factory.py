from app.services.procedural_builder import build_house
from app.services.procedural_foliage import scatter_trees
from app.services.default_properties import get_default_properties
from app.services.ai_structure import generate_scene_plan

def create_scene_from_text(text: str):

    plan = generate_scene_plan(text)

    placeables = []
    foliage = []

    base_x = 500
    base_y = 500
    spacing = 1500

    # -------- STRUCTURES --------
    for s in plan.get("Structures", []):
        if s["type"] == "house":
            count = s.get("count", 1)
            size = s.get("size", 2)

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
            trees = scatter_trees(count=count, radius=2000)
            foliage.extend(trees)

    return {
        "PlaceableAssets": placeables,
        "GeometryAssets": [],
        "Text3DActors": [],
        "Foliage": foliage,
        "DefaultProperties": get_default_properties()
    }
