# app/llm/deepseek_client.py
import os
import httpx
from typing import Dict, Any
from app.llm.base import BaseLLMClient


DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"


class DeepSeekClient(BaseLLMClient):
    """
    DeepSeek implementation of BaseLLMClient.
    Used temporarily until ChatGPT-4o-mini is enabled.
    """

    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise RuntimeError("DEEPSEEK_API_KEY not set")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def parse_intent(self, text: str) -> Dict[str, Any]:
        payload = {
            "model": "deepseek-chat",
            "temperature": 0.0,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Extract game-building intent.\n"
                        "Return JSON ONLY.\n"
                        "Keys: theme, game_type, objects, difficulty."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                DEEPSEEK_API_URL,
                headers=self.headers,
                json=payload
            )

        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]
