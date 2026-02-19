import random
import math
from app.services.tree_presents import random_tree


# ======================================================
# CONFIG
# ======================================================

HOUSE_SIZE = 1000          # approx 2x2 house footprint
SAFE_MARGIN = 350
RING_OFFSET = 500          # distance OUTSIDE house
TREES_PER_HOUSE = 7


# ======================================================
# COLLISION CHECK
# ======================================================

def inside_house(x, y, houses):

    half = (HOUSE_SIZE / 2) + SAFE_MARGIN

    for hx, hy in houses:
        if hx - half <= x <= hx + half and \
           hy - half <= y <= hy + half:
            return True

    return False


# ======================================================
# RING TREE SPAWNER
# ======================================================

def spawn_tree_ring(cx, cy, houses):

    trees = []

    for _ in range(TREES_PER_HOUSE):

        # ⭐ spawn OUTSIDE building
        angle = random.uniform(0, 2 * math.pi)

        distance = (
            HOUSE_SIZE / 2
            + SAFE_MARGIN
            + RING_OFFSET
            + random.uniform(-150, 150)
        )

        x = cx + math.cos(angle) * distance
        y = cy + math.sin(angle) * distance

        # safety validation
        if inside_house(x, y, houses):
            continue

        preset = random_tree()

        trees.append({
            "StaticMesh": preset["StaticMesh"],
            "StaticMeshPath": preset["StaticMeshPath"],
            "Instances": [{
                "Location": {"X": x, "Y": y, "Z": 0},
                "Rotation": {
                    "Pitch": 0,
                    "Yaw": random.uniform(0, 360),
                    "Roll": 0
                },
                "Scale": {
                    "X": random.uniform(*preset["scale"]),
                    "Y": random.uniform(*preset["scale"]),
                    "Z": random.uniform(*preset["scale"])
                }
            }]
        })

    return trees


# ======================================================
# MAIN ENTRY
# ======================================================

def beautify_trees(house_positions):

    foliage = []

    for hx, hy in house_positions:
        foliage.extend(
            spawn_tree_ring(hx, hy, house_positions)
        )

    return foliage
