# app/services/procedural_builder.py

from app.services.asset_utils import make_asset
from app.services.asset_registry import AssetRegistry
import random

registry = AssetRegistry()

TILE = 500
HALF = TILE / 2
CEIL_Z = 400


def choose_style(rng: random.Random):

    def pick(df):
        if df is None or df.empty:
            return None
        rows = df.to_dict("records")
        return rng.choice(rows).get("AssetToPlace")

    return {
        "floor": pick(registry.floors()),
        "wall": pick(registry.walls()),
        "door": pick(registry.doors()),
        "ceiling": pick(registry.ceilings())
    }


def build_house(size=3, center_x=0, center_y=0, style_seed=0):

    rng = random.Random(style_seed)
    style = choose_style(rng)

    floor = style["floor"]
    wall = style["wall"]
    door = style["door"]
    ceil = style["ceiling"]

    assets = []

    cx, cy = center_x, center_y

    # Floors & Ceilings
    for i in range(size):
        for j in range(size):

            x = cx + i * TILE
            y = cy + j * TILE

            assets.append(make_asset("Floor", floor, x, y, 0))
            assets.append(make_asset("Ceiling", ceil, x, y, CEIL_Z))

    min_x = cx
    max_x = cx + (size - 1) * TILE
    min_y = cy
    max_y = cy + (size - 1) * TILE

    # deterministic door position
    door_idx = size // 2

# -------- FRONT + BACK --------

    for i in range(size):

        x = cx + i * TILE

        # FRONT WALL (faces player)
        if i == door_idx:
            assets.append(make_asset("Door", door, x, cy - HALF, 0, yaw=90))
        else:
            assets.append(make_asset("Wall", wall, x, cy - HALF, 0, yaw=90))

        # BACK WALL
        assets.append(make_asset("Wall", wall, x, cy + (size * TILE) - HALF, 0, yaw=-90))


# -------- LEFT + RIGHT --------

    for j in range(size):

        y = cy + j * TILE

        assets.append(make_asset("Wall", wall, cx - HALF, y, 0, yaw=180))
        assets.append(make_asset("Wall", wall, cx + (size * TILE) - HALF, y, 0, yaw=0))
    return assets