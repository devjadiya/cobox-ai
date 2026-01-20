from app.core.llm_client import get_llm_client
from app.settings import settings

INTENT_SYSTEM_PROMPT = """
You are a game intent parser.
Extract ONLY structured JSON.
No explanations.
"""

def parse_intent(user_text: str) -> dict:
    client = get_llm_client()

    if client is None:
        # Safe fallback (system still runs)
        return {
            "objects": [],
            "note": "LLM not configured"
        }

    response = client.chat.completions.create(
        model=settings.DEEPSEEK_MODEL,
        temperature=0.0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": INTENT_SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        max_tokens=1024
    )

    return response.choices[0].message.content
