import random

STONE_PRESETS = [

{
"StaticMesh":"SM_Env_Rock_Pebbles_01",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Rock_Pebbles_01.SM_Env_Rock_Pebbles_01"
},

{
"StaticMesh":"SM_Env_Rock_Pebbles_02",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Rock_Pebbles_02.SM_Env_Rock_Pebbles_02"
},

{
"StaticMesh":"SM_Env_Rock_Pebbles_03",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Rock_Pebbles_03.SM_Env_Rock_Pebbles_03"
},

{
"StaticMesh":"SM_Env_Rock_Pebbles_04",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Rock_Pebbles_04.SM_Env_Rock_Pebbles_04"
},

{
"StaticMesh":"SM_Env_Rock_Pebbles_05",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Rock_Pebbles_05.SM_Env_Rock_Pebbles_05"
},

{
"StaticMesh":"SM_Env_Rock_River_01",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Rock_River_01.SM_Env_Rock_River_01"
},

{
"StaticMesh":"SM_Env_Rock_River_02",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Rock_River_02.SM_Env_Rock_River_02"
},

{
"StaticMesh":"SM_Env_Rock_River_03",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Rock_River_03.SM_Env_Rock_River_03"
},

{
"StaticMesh":"SM_Env_Rock_River_04",
"StaticMeshPath":"/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Rock_River_04.SM_Env_Rock_River_04"
}

]


def random_stone():
    return random.choice(STONE_PRESETS)


def generate_stones(
    houses,
    stone_count,
    layout_rng,
    style_rng,
    scene_type="default"
):

    groups = {}

    # ---------------------------------------------------
    # SCENE BOUNDS (fix for min_x / max_x error)
    # ---------------------------------------------------

    min_x = min(h["x"] for h in houses) - 2500
    max_x = max(h["x"] for h in houses) + 2500
    min_y = min(h["y"] for h in houses) - 2500
    max_y = max(h["y"] for h in houses) + 2500

    # ---------------------------------------------------

    for _ in range(stone_count):

        house = layout_rng.choice(houses)

        hx = house["x"]
        hy = house["y"]
        r = house["r"]

        # create a cluster center
        cluster_x = layout_rng.uniform(min_x, max_x)
        cluster_y = layout_rng.uniform(min_y, max_y)

        cluster_size = layout_rng.randint(3, 6)

        for _ in range(cluster_size):

            x = cluster_x + layout_rng.uniform(-120, 120)
            y = cluster_y + layout_rng.uniform(-120, 120)

            # avoid spawning stones inside houses
            if abs(x - hx) < r and abs(y - hy) < r:
                continue

            preset = style_rng.choice(STONE_PRESETS)

            mesh = preset["StaticMesh"]
            path = preset["StaticMeshPath"]

            if mesh not in groups:
                groups[mesh] = {
                    "StaticMesh": mesh,
                    "StaticMeshPath": path,
                    "Instances": []
                }

            groups[mesh]["Instances"].append({

                "Location": {
                    "X": x,
                    "Y": y,
                    "Z": 0
                },

                "Rotation": {
                    "Pitch": 0,
                    "Yaw": style_rng.uniform(-180, 180),
                    "Roll": 0
                },

                "Scale": {
                    "X": style_rng.uniform(0.7, 1.4),
                    "Y": style_rng.uniform(0.7, 1.4),
                    "Z": style_rng.uniform(0.7, 1.4)
                }

            })

    return list(groups.values())