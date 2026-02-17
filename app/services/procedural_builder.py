from app.services.asset_utils import make_asset

CENTER_X = 180
CENTER_Y = 600

TILE_SIZE = 500
HALF_TILE = TILE_SIZE / 2
CEIL_Z = 400

FLOOR_PATH = "/WorldBuilder/Core/Actors/Placeable/Library/Floor/BP_FloorAsset_Wb_02.BP_FloorAsset_Wb_02_C"
WALL_PATH = "/WorldBuilder/Core/Actors/Placeable/Library/Wall/BP_WallAsset_Wb_12.BP_WallAsset_Wb_12_C"
DOOR_PATH = "/WorldBuilder/Core/Actors/Placeable/Library/Door/BP_DoorAsset_Wb_01.BP_DoorAsset_Wb_01_C"
CEIL_PATH = "/WorldBuilder/Core/Actors/Placeable/Library/Ceiling/BP_CeilingAsset_Wb_03.BP_CeilingAsset_Wb_03_C"


def build_house(size=2, floors=1, center_x=None, center_y=None):

    cx = center_x if center_x is not None else CENTER_X + 500
    cy = center_y if center_y is not None else CENTER_Y + 500

    assets = []

    # -------- FLOORS + CEILINGS --------
    for i in range(size):
        for j in range(size):
            fx = cx + i * TILE_SIZE
            fy = cy + j * TILE_SIZE

            assets.append(make_asset("Floor", FLOOR_PATH, fx, fy, 0))
            assets.append(make_asset("Ceiling", CEIL_PATH, fx, fy, CEIL_Z))

    min_x = cx
    max_x = cx + (size - 1) * TILE_SIZE
    min_y = cy
    max_y = cy + (size - 1) * TILE_SIZE

    door_index = size // 2  # center front

    # -------- TOP & BOTTOM --------
    for i in range(size):
        wx = cx + i * TILE_SIZE

        # TOP WALL
        assets.append(
            make_asset("Wall", WALL_PATH, wx, max_y + HALF_TILE, 0, yaw=90)
        )

        # BOTTOM WALL / DOOR
        if i == door_index:
            assets.append(
                make_asset("Door", DOOR_PATH, wx, min_y - HALF_TILE, 0, yaw=-90)
            )
        else:
            assets.append(
                make_asset("Wall", WALL_PATH, wx, min_y - HALF_TILE, 0, yaw=-90)
            )

    # -------- LEFT & RIGHT --------
    for j in range(size):
        wy = cy + j * TILE_SIZE

        assets.append(
            make_asset("Wall", WALL_PATH, min_x - HALF_TILE, wy, 0, yaw=180)
        )
        assets.append(
            make_asset("Wall", WALL_PATH, max_x + HALF_TILE, wy, 0, yaw=0)
        )

    return assets
