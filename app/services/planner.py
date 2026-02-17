import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------- SYSTEM PROMPT ----------------
SYSTEM_PROMPT = """
You are an Unreal Engine Scene Planner.

Return ONLY valid JSON.
NO markdown. NO explanations.

Rules:
- Structures ALWAYS present.
- Foliage ALWAYS present.
- Use type "house".
- Include "count".
- Include "size".
- Default count = 1.
- Default size = 2.
- Trees default count = 5.
- Size is NxN tiles.
- Never decimals.

FORMAT STRICT:
{
 "Structures":[{"type":"house","count":1,"size":2}],
 "Foliage":[{"type":"tree","count":5}]
}
"""

# ---------------- SAFE DEFAULT ----------------
def fallback_plan():
    return {
        "Structures": [{"type": "house", "count": 1, "size": 2}],
        "Foliage": [{"type": "tree", "count": 5}]
    }

# ---------------- EXTRACTION ----------------
def extract_grid_size(text: str):
    try:
        m = re.search(r'(\d+)\s*[xX]\s*(\d+)', text)
        if m:
            return int(m.group(1))
        t = text.lower()
        if "huge" in t: return 4
        if "big" in t: return 3
        if "small" in t: return 1
    except:
        pass
    return None

def extract_structure_count(text: str):
    try:
        m = re.search(r'(\d+)\s*(house|houses|building|buildings)', text.lower())
        if m:
            return int(m.group(1))
    except:
        pass
    return None

def extract_tree_count(text: str):
    try:
        m = re.search(r'(\d+)\s*(tree|trees)', text.lower())
        if m:
            return int(m.group(1))
    except:
        pass
    return None

# ---------------- NORMALIZE ----------------
def normalize_plan(plan: dict):
    if not isinstance(plan, dict):
        return fallback_plan()

    structures = []
    foliage = []

    for s in plan.get("Structures", []):
        try:
            size = int(float(s.get("size", 2)))
            count = int(float(s.get("count", 1)))
        except:
            size, count = 2, 1

        size = max(1, min(size, 6))
        count = max(1, min(count, 20))

        structures.append({
            "type": "house",
            "count": count,
            "size": size
        })

    for f in plan.get("Foliage", []):
        try:
            count = int(float(f.get("count", 5)))
        except:
            count = 5

        count = max(0, min(count, 500))

        foliage.append({
            "type": "tree",
            "count": count
        })

    if not structures:
        structures = [{"type": "house", "count": 1, "size": 2}]
    if not foliage:
        foliage = [{"type": "tree", "count": 5}]

    return {"Structures": structures, "Foliage": foliage}

# ---------------- MAIN ----------------
def generate_scene_plan(user_text: str):
    plan = fallback_plan()

    # ---- AI CALL ----
    try:
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text or ""}
            ],
            response_format={"type": "json_object"}
        )
        plan = json.loads(resp.choices[0].message.content)
    except Exception as e:
        print("AI ERROR:", e)

    # ---- NORMALIZE ----
    plan = normalize_plan(plan)

    # ---- DETERMINISTIC OVERRIDES ----
    size_override = extract_grid_size(user_text or "")
    count_override = extract_structure_count(user_text or "")
    tree_override = extract_tree_count(user_text or "")

    for s in plan["Structures"]:
        if size_override: s["size"] = size_override
        if count_override: s["count"] = count_override

    for f in plan["Foliage"]:
        if tree_override: f["count"] = tree_override

    return normalize_plan(plan)
