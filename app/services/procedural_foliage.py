import random

def scatter_trees(count: int = 5, radius: int = 2000):
    foliage_assets = []

    half = count // 2

    foliage_assets.append({
        "StaticMesh": "SM_Env_Pine_01",
        "StaticMeshPath": "/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Pine_01.SM_Env_Pine_01",
        "Instances": []
    })

    foliage_assets.append({
        "StaticMesh": "SM_Env_Pine_02",
        "StaticMeshPath": "/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Pine_02.SM_Env_Pine_02",
        "Instances": []
    })

    for i in range(count):
        inst = {
            "Location": {
                "X": random.randint(-radius, radius),
                "Y": random.randint(-radius, radius),
                "Z": 0
            },
            "Rotation": {
                "Pitch": 0,
                "Yaw": random.randint(0, 360),
                "Roll": 0
            },
            "Scale": {"X":1,"Y":1,"Z":1}
        }

        if i < half:
            foliage_assets[0]["Instances"].append(inst)
        else:
            foliage_assets[1]["Instances"].append(inst)

    return foliage_assets
