def normalize_plan(plan: dict) -> dict:
    if not plan:
        return {"Structures": [], "Foliage": []}

    structures = []
    foliage = []

    # ---------- STRUCTURES ----------
    for s in plan.get("Structures", []):
        raw_type = s.get("type", "").lower()

        if raw_type in ["house", "building", "buildings", "villa", "mansion"]:
            s["type"] = "house"
            s["count"] = int(s.get("count", 1))
            s["floors"] = int(s.get("floors", 1))
            s["size"] = int(s.get("size", 2))
            structures.append(s)

    # ---------- FOLIAGE ----------
    for f in plan.get("Foliage", []):
        raw_type = f.get("type", "").lower()

        if raw_type in ["tree", "trees", "pine", "oak"]:
            f["type"] = "tree"
            f["count"] = int(f.get("count", 5))
            f["radius"] = int(f.get("radius", 2000))
            foliage.append(f)

    return {
        "Structures": structures,
        "Foliage": foliage
    }
