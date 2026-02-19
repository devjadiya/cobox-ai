from app.services.asset_utils import make_asset
from app.services.asset_registry import AssetRegistry
import random

registry = AssetRegistry()

TILE_SIZE = 500
HALF_TILE = TILE_SIZE / 2
CEIL_Z = 400


# ======================================================
# HOUSE STYLE SYSTEM (NEW)
# ======================================================

def choose_house_style():
    """
    Select ONE consistent asset kit per house.
    """

    floor = registry.random(registry.floors())
    wall = registry.random(registry.walls())
    door = registry.random(registry.doors())
    ceiling = registry.random(registry.ceilings())

    return {
        "floor": floor,
        "wall": wall,
        "door": door,
        "ceiling": ceiling
    }


# ======================================================
# HOUSE BUILDER
# ======================================================

def build_house(size=2, floors=1, center_x=0, center_y=0):

    style = choose_house_style()

    FLOOR_PATH = style["floor"]
    WALL_PATH = style["wall"]
    DOOR_PATH = style["door"]
    CEIL_PATH = style["ceiling"]

    assets = []

    cx = center_x
    cy = center_y

    # ---------------- FLOORS + CEILINGS ----------------
    for i in range(size):
        for j in range(size):

            fx = cx + i * TILE_SIZE
            fy = cy + j * TILE_SIZE

            assets.append(
                make_asset("Floor", FLOOR_PATH, fx, fy, 0)
            )

            assets.append(
                make_asset("Ceiling", CEIL_PATH, fx, fy, CEIL_Z)
            )

    min_x = cx
    max_x = cx + (size - 1) * TILE_SIZE
    min_y = cy
    max_y = cy + (size - 1) * TILE_SIZE

    door_index = size // 2

    # ---------------- TOP & BOTTOM WALLS ----------------
    for i in range(size):

        wx = cx + i * TILE_SIZE

        # TOP
        assets.append(
            make_asset("Wall", WALL_PATH,
                       wx, max_y + HALF_TILE,
                       0, yaw=90)
        )

        # BOTTOM (door center)
        if i == door_index:
            assets.append(
                make_asset("Door", DOOR_PATH,
                           wx, min_y - HALF_TILE,
                           0, yaw=-90)
            )
        else:
            assets.append(
                make_asset("Wall", WALL_PATH,
                           wx, min_y - HALF_TILE,
                           0, yaw=-90)
            )

    # ---------------- SIDE WALLS ----------------
    for j in range(size):

        wy = cy + j * TILE_SIZE

        assets.append(
            make_asset("Wall", WALL_PATH,
                       min_x - HALF_TILE, wy,
                       0, yaw=180)
        )

        assets.append(
            make_asset("Wall", WALL_PATH,
                       max_x + HALF_TILE, wy,
                       0, yaw=0)
        )

    return assets
