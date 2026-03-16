from src.ai_generation.llm_clients.llm_base import LLMClient
from src.ai_generation.llm_clients.gemeni import GeminiClient
from src.ai_generation.llm_clients.openrouter import OpenRouterClient
from settings import settings

_llm: LLMClient = None

provider = settings.PROVIDER_NAME


def get_llm_client() -> LLMClient:
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
