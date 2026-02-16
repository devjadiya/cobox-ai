from app.services.asset_utils import make_asset

CENTER_X = 180
CENTER_Y = 600
CEIL_Z = 400

RIGHT_OFFSET = 249.91035461425781
LEFT_OFFSET = -249.91035461425781
TOP_OFFSET = 250
BOTTOM_OFFSET = -250

CEIL_X_OFFSET = -0.48216247558594

def build_house(size=2, floors=1, center_x=None, center_y=None):

    cx = center_x if center_x else CENTER_X + 500
    cy = center_y if center_y else CENTER_Y + 500

    assets = []

    floor_path = "/WorldBuilder/Core/Actors/Placeable/Library/Floor/BP_FloorAsset_Wb_02.BP_FloorAsset_Wb_02_C"
    wall_path = "/WorldBuilder/Core/Actors/Placeable/Library/Wall/BP_WallAsset_Wb_12.BP_WallAsset_Wb_12_C"
    ceil_path = "/WorldBuilder/Core/Actors/Placeable/Library/Ceiling/BP_CeilingAsset_Wb_03.BP_CeilingAsset_Wb_03_C"
    door_path = "/WorldBuilder/Core/Actors/Placeable/Library/Door/BP_DoorAsset_Wb_01.BP_DoorAsset_Wb_01_C"

    # FLOOR
    assets.append(make_asset("Floor", floor_path, cx, cy, 0))

    # WALLS
    assets.append(make_asset("Wall", wall_path, cx + RIGHT_OFFSET, cy, 0, yaw=0))
    assets.append(make_asset("Wall", wall_path, cx, cy + TOP_OFFSET, 0, yaw=90))
    assets.append(make_asset("Wall", wall_path, cx + LEFT_OFFSET, cy, 0, yaw=180))
    assets.append(make_asset("Wall", wall_path, cx, cy + BOTTOM_OFFSET, 0, yaw=-90))

    # DOOR FRONT CENTER
    assets.append(make_asset("Door", door_path, cx, cy + BOTTOM_OFFSET, 0))

    # CEILING
    assets.append(make_asset("Ceiling", ceil_path, cx + CEIL_X_OFFSET, cy, CEIL_Z))

    return assets
