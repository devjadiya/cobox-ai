import random

def scatter_trees(count=5, radius=2000):

    # -------- SAFE CAST --------
    try:
        count = int(float(count))
    except:
        count = 5

    try:
        radius = int(float(radius))
    except:
        radius = 2000

    # -------- CLAMPS --------
    count = max(0, min(count, 500))
    radius = max(100, min(radius, 20000))

    trees = []

    for _ in range(count):
        try:
            tree = {
                "StaticMesh": "SM_Env_Pine_01",
                "StaticMeshPath": "/Game/Biomes/PNB_Alpine_Mountain/Models/Environment/SM_Env_Pine_01.SM_Env_Pine_01",
                "Instances": [
                    {
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
                        "Scale": {
                            "X": 1,
                            "Y": 1,
                            "Z": 1
                        }
                    }
                ]
            }

            trees.append(tree)

        except Exception as e:
            print("TREE ERROR:", e)

    # Guarantee at least empty list
    return trees if trees else []
