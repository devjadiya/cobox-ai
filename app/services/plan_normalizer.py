def normalize_plan(plan: dict) -> dict:
    if not plan:
        return {"Structures": [], "Foliage": []}

    structures = []
    foliage = []

    # ---------- STRUCTURES ----------
    for s in plan.get("Structures", []):
        raw_type = s.get("type", "").lower()

        if raw_type in ["house", "building", "buildings", "villa", "mansion"]:
            s_type = "house"
            count = int(s.get("count", 1))
            floors = int(s.get("floors", 1))
            size = int(s.get("size", 2))

            # -------- INTENT DISAMBIGUATION --------
            # If both >1 and equal, assume "3x3 house" not "3 houses"
            if count > 1 and size > 1 and count == size:
                count = 1

            # clamps
            count = max(1, min(count, 20))
            size = max(1, min(size, 6))
            floors = max(1, min(floors, 10))

            structures.append({
                "type": s_type,
                "count": count,
                "floors": floors,
                "size": size
            })

    # ---------- FOLIAGE ----------
    for f in plan.get("Foliage", []):
        raw_type = f.get("type", "").lower()

        if raw_type in ["tree", "trees", "pine", "oak"]:
            f_type = "tree"
            count = int(f.get("count", 5))
            radius = int(f.get("radius", 2000))

            count = max(0, min(count, 200))
            radius = max(500, min(radius, 10000))

            foliage.append({
                "type": f_type,
                "count": count,
                "radius": radius
            })

    return {
        "Structures": structures,
        "Foliage": foliage
    }
