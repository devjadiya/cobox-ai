from typing import Optional
from openai import OpenAI
from app.settings import settings

_client: Optional[OpenAI] = None

def get_llm_client() -> Optional[OpenAI]:
    global _client

    if _client is not None:
        return _client

    if settings.LLM_PROVIDER == "deepseek":
        if not settings.DEEPSEEK_API_KEY:
            return None

        _client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL
        )
        return _client

    if settings.LLM_PROVIDER == "openai":
        if not settings.OPENAI_API_KEY:
            return None

        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
        return _client

    return None
