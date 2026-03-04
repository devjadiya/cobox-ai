import random

BUSH_PRESETS = [
{
"StaticMesh":"SM_Env_Bush_01_",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Bush_01_.SM_Env_Bush_01_"
},
{
"StaticMesh":"SM_Env_Bush_01_Alt",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Bush_01_Alt.SM_Env_Bush_01_Alt"
},
{
"StaticMesh":"SM_Env_Bush_02",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Bush_02.SM_Env_Bush_02"
},
{
"StaticMesh":"SM_Env_Bush_02_Alt",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Bush_02_Alt.SM_Env_Bush_02_Alt"
},
{
"StaticMesh":"SM_Env_Bush_Flower_01",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Bush_Flower_01.SM_Env_Bush_Flower_01"
},
{
"StaticMesh":"SM_Env_Bush_Flower_01_Alt",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Bush_Flower_01_Alt.SM_Env_Bush_Flower_01_Alt"
},
{
"StaticMesh":"SM_Env_Flowers_01",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Flowers_01.SM_Env_Flowers_01"
},
{
"StaticMesh":"SM_Env_Flowers_01_Alt",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Flowers_01_Alt.SM_Env_Flowers_01_Alt"
},
{
"StaticMesh":"SM_Env_Grass_01",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Grass_01.SM_Env_Grass_01"
},
{
"StaticMesh":"SM_Env_GroundCover_01",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_GroundCover_01.SM_Env_GroundCover_01"
},
{
"StaticMesh":"SM_Env_GroundCover_02",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_GroundCover_02.SM_Env_GroundCover_02"
},
{
"StaticMesh":"SM_Env_GroundCover_03",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_GroundCover_03.SM_Env_GroundCover_03"
}
]


def generate_foliage(
    houses,
    grass_count,
    bush_count,
    layout_rng,
    style_rng,
    scene_type="default"
):

    groups = {}

    total_instances = grass_count + bush_count

    # ---------------------------------------------------
    # SCENE BOUNDS (fix for min_x / max_x error)
    # ---------------------------------------------------

    min_x = min(h["x"] for h in houses) - 2500
    max_x = max(h["x"] for h in houses) + 2500
    min_y = min(h["y"] for h in houses) - 2500
    max_y = max(h["y"] for h in houses) + 2500

    # ---------------------------------------------------

    for _ in range(total_instances):

        house = layout_rng.choice(houses)

        hx = house["x"]
        hy = house["y"]
        r = house["r"]

        for _ in range(10):

            # cluster spawn
            cluster_x = layout_rng.uniform(min_x, max_x)
            cluster_y = layout_rng.uniform(min_y, max_y)

            x = cluster_x + layout_rng.uniform(-300, 300)
            y = cluster_y + layout_rng.uniform(-300, 300)

            # prevent spawning inside house
            if abs(x - hx) < r and abs(y - hy) < r:
                continue

            break

        preset = style_rng.choice(BUSH_PRESETS)

        mesh = preset["StaticMesh"]
        path = preset["StaticMeshPath"]

        if mesh not in groups:
            groups[mesh] = {
                "StaticMesh": mesh,
                "StaticMeshPath": path,
                "Instances": []
            }

        groups[mesh]["Instances"].append({

            "Location": {"X": x, "Y": y, "Z": 0},

            "Rotation": {
                "Pitch": 0,
                "Yaw": style_rng.uniform(-180, 180),
                "Roll": 0
            },

            "Scale": {
                "X": style_rng.uniform(0.8, 1.3),
                "Y": style_rng.uniform(0.8, 1.3),
                "Z": style_rng.uniform(0.8, 1.3)
            }

        })

    return list(groups.values())