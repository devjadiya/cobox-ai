# app/llm/openai_client.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def parse_intent(text: str):
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": """
You are a game scene planner.
Return ONLY JSON.
Schema:
{
 "scene_type": "city|track|open_world|building|custom",
 "objects":[{"type":"building|road|tree|door","count":number}]
}
"""
            },
            {"role": "user", "content": text}
        ]
    )

    return eval(response.choices[0].message.content)


def enhance_scene(scene_json: dict, user_text: str):
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": """
You enhance game scenes.
Add extra decor, trees, lights, props.
Do NOT remove actors.
Return FULL JSON.
"""
            },
            {
                "role": "user",
                "content": f"User prompt: {user_text}\nScene JSON:\n{scene_json}"
            }
        ]
    )

    return eval(response.choices[0].message.content)
