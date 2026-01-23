# app/llm/deepseek_client.py
import os
import httpx
from typing import Dict, Any


DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"


class DeepSeekClient:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.enabled = bool(self.api_key)

    async def parse_intent(self, text: str) -> Dict[str, Any]:
        if not self.enabled:
            raise RuntimeError("DeepSeek disabled")

        payload = {
            "model": "deepseek-chat",
            "temperature": 0.0,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Extract scene intent.\n"
                        "Return JSON ONLY.\n"
                        "Schema: {scene_type, objects:[{type,count}]}"
                    )
                },
                {"role": "user", "content": text}
            ]
        }

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                DEEPSEEK_API_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )

        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    # ---- SYNC FALLBACK ----
    def parse_intent_sync(self, text: str) -> Dict[str, Any]:
        return {
            "scene_type": "custom",
            "objects": [],
            "notes": "ai_failed"
        }
