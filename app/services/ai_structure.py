import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an Unreal Engine Scene Planner.

Return ONLY valid JSON.
NO explanations. NO markdown.

Rules:
- Structures ALWAYS present.
- Foliage ALWAYS present.
- Use type "house" only.
- Include "count".
- Include "size".
- Default count = 1.
- Default size = 2.
- Trees default count = 5.

CRITICAL SEMANTIC RULES:
- "3x3 house" = size 3, count 1.
- "3 houses" = count 3.
- NEVER infer count from size.
- "size" means NxN grid tiles only.

- If user says "big" -> size 3.
- If user says "huge" -> size 4.
- If user says "small" -> size 1.
- Never output decimals.

Format STRICT:
{
 "Structures":[
   {"type":"house","count":2,"size":2}
 ],
 "Foliage":[
   {"type":"tree","count":5}
 ]
}
"""


# ---------------- DETERMINISTIC EXTRACTION ----------------
def extract_grid_size(text: str):
    match = re.search(r'(\d+)\s*[xX]\s*(\d+)', text)
    if match:
        return int(match.group(1))

    text_lower = text.lower()
    if "huge" in text_lower:
        return 4
    if "big" in text_lower:
        return 3
    if "small" in text_lower:
        return 1

    return None


def extract_structure_count(text: str):
    match = re.search(r'(\d+)\s*(house|houses|building|buildings)', text.lower())
    if match:
        return int(match.group(1))
    return None


def extract_tree_count(text: str):
    match = re.search(r'(\d+)\s*(tree|trees)', text.lower())
    if match:
        return int(match.group(1))
    return None


# ---------------- MAIN FUNCTION ----------------
def generate_scene_plan(user_text: str):
    try:
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            response_format={"type": "json_object"}
        )

        content = resp.choices[0].message.content
        plan = json.loads(content)

    except Exception as e:
        print("AI ERROR:", e)
        plan = {
            "Structures":[{"type":"house","count":1,"size":2}],
            "Foliage":[{"type":"tree","count":3}]
        }

    # -------- DETERMINISTIC OVERRIDES --------
    size_override = extract_grid_size(user_text)
    count_override = extract_structure_count(user_text)
    tree_override = extract_tree_count(user_text)

    # -------- NORMALIZATION --------
    for s in plan.get("Structures", []):
        s["type"] = "house"

        count = int(s.get("count", 1))
        size = int(s.get("size", 2))

        if count_override:
            count = count_override
        if size_override:
            size = size_override

        # -------- INTENT FIX --------
        if count > 1 and size > 1 and count == size and not count_override:
            count = 1

        s["size"] = max(1, min(size, 6))
        s["count"] = max(1, min(count, 20))

    for f in plan.get("Foliage", []):
        count = int(f.get("count", 5))
        if tree_override:
            count = tree_override

        f["count"] = max(0, min(count, 200))

    # guarantee keys
    if "Structures" not in plan:
        plan["Structures"] = [{"type":"house","count":1,"size":2}]

    if "Foliage" not in plan:
        plan["Foliage"] = [{"type":"tree","count":5}]

    return plan
