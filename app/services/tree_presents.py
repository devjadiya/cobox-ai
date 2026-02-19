import random


TREE_PRESETS = [
    {
        "StaticMesh": "SM_Env_Pine_01",
        "StaticMeshPath": "/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Pine_01.SM_Env_Pine_01",
        "scale": (0.9, 1.2)
    },
    {
        "StaticMesh": "SM_Env_Pine_02",
        "StaticMeshPath": "/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Pine_02.SM_Env_Pine_02",
        "scale": (0.8, 1.3)
    },
    {
        "StaticMesh": "SM_Env_Pine_03",
        "StaticMeshPath": "/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Pine_03.SM_Env_Pine_03",
        "scale": (1.0, 1.4)
    },
    {
        "StaticMesh": "SM_Env_Pine_04",
        "StaticMeshPath": "/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Pine_04.SM_Env_Pine_04",
        "scale": (0.7, 1.1)
    },
    {
        "StaticMesh": "SM_Env_Pine_05",
        "StaticMeshPath": "/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Pine_05.SM_Env_Pine_05",
        "scale": (1.1, 1.5)
    },
]


def random_tree():
    """Return random tree preset"""
    return random.choice(TREE_PRESETS)
