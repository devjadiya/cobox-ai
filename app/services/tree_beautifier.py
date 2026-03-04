# app/services/tree_beautifier.py

import math

TREE_LIBRARY = [
("SM_Env_Pine_01","/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Pine_01.SM_Env_Pine_01"),
("SM_Env_Pine_02","/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Pine_02.SM_Env_Pine_02"),
("SM_Env_Pine_03","/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Pine_03.SM_Env_Pine_03"),
("SM_Env_Pine_04","/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Pine_04.SM_Env_Pine_04"),
("SM_Env_Pine_05","/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Pine_05.SM_Env_Pine_05"),
]


def beautify_trees(houses, size, total_count, layout_rng, style_rng):

    grouped = {}

    if not houses:
        houses = [(0,0)]

    for _ in range(total_count):

        hx, hy = layout_rng.choice(houses)

        angle = layout_rng.uniform(0, 2 * math.pi)
        radius = layout_rng.uniform(900, 1400)

        x = hx + math.cos(angle) * radius
        y = hy + math.sin(angle) * radius

        mesh, path = style_rng.choice(TREE_LIBRARY)

        if mesh not in grouped:
            grouped[mesh] = {
                "StaticMesh": mesh,
                "StaticMeshPath": path,
                "Transforms": []
            }

        scale = style_rng.uniform(0.9, 1.6)

        grouped[mesh]["Transforms"].append({
            "Location": {"X": x, "Y": y, "Z": 0},
            "Rotation": {"Pitch": 0, "Yaw": style_rng.uniform(-180,180), "Roll": 0},
            "Scale3D": {"X": scale, "Y": scale, "Z": scale}
        })

    return list(grouped.values())