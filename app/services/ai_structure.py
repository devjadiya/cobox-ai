import os
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an Unreal Engine Scene Planner.

Return ONLY valid JSON.

Rules:
- Structures ALWAYS present.
- Foliage ALWAYS present.
- Use type "house" only.
- Include "count".
- Default count = 1.
- Default size = 2.
- Trees default count = 5.

Format:
{
 "Structures":[
   {"type":"house","count":2,"size":2}
 ],
 "Foliage":[
   {"type":"tree","count":5}
 ]
}
"""

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

    # -------- NORMALIZATION --------
    for s in plan.get("Structures", []):
        if s.get("type","").lower() in ["building","buildings"]:
            s["type"] = "house"
        s["count"] = int(s.get("count",1))
        s["size"] = int(s.get("size",2))

    for f in plan.get("Foliage", []):
        f["count"] = int(f.get("count",5))

    return plan
