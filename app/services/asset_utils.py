def make_asset(
    asset_class,
    asset_path,
    x,
    y,
    z=0,
    pitch=0,
    yaw=0,
    roll=0,
    scale=1,
    scale_x=None,
    scale_y=None,
    scale_z=None
):
    # if single scale used → apply to xyz
    if scale_x is None:
        scale_x = scale
    if scale_y is None:
        scale_y = scale
    if scale_z is None:
        scale_z = scale

    return {
        "AssetClass": asset_class,
        "AssetClassPath": asset_path,
        "Transform": {
            "Location": {"X": x, "Y": y, "Z": z},
            "Rotation": {"Pitch": pitch, "Yaw": yaw, "Roll": roll},
            "Scale": {"X": scale_x, "Y": scale_y, "Z": scale_z}
        },
        "OcaData": {
            "CollisionProfile": "BlockAllDynamic",
            "Physics": False,
            "Shadow": True
        }
    }
