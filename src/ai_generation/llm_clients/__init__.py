from typing import Literal
from settings import settings
from src.ai_generation.llm_clients.llm_base import LLMClient
from src.ai_generation.llm_clients.gemini import GeminiClient
from src.ai_generation.llm_clients.openrouter import OpenRouterClient

_llm: LLMClient | None = None


def get_llm_client(provider: Literal["gemini", "openrouter"] = None) -> LLMClient:
    if provider is None:
        provider = settings.PROVIDER_NAME
    global _llm
    if _llm is None:
        match provider:
            case "gemini":
                _llm = GeminiClient()
            case "openrouter":
                _llm = OpenRouterClient()
            case _:
                raise ValueError(f"Unknown provider: {provider}")
    return _llm


def reset_llm_client():
    global _llm
    _llm = None
