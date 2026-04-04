from typing import Literal
from langchain_core.language_models.base import BaseLanguageModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from settings import settings
from src.ai_generation.llm_clients.llm_base import LLMClient
from src.ai_generation.llm_clients.gemini import GeminiClient
from src.ai_generation.llm_clients.openrouter import OpenRouterClient

_llm: LLMClient | None = None
_langraph_llm: BaseLanguageModel | None = None


def get_langgraph_llm_client(
    provider: Literal["gemini", "openrouter"] = None,
) -> BaseLanguageModel:
    if provider is None:
        provider = settings.PROVIDER_NAME
    global _langraph_llm
    if _langraph_llm is None:
        match provider:
            case "gemini":
                _langraph_llm = ChatGoogleGenerativeAI(
                    model=settings.GEMINI_MODEL_NAME,
                    max_retries=2,
                    api_key=settings.GEMINI_API_KEY,
                )
            case "openrouter":
                # TODO: implement support
                _langraph_llm = ChatOpenAI()
            case _:
                raise ValueError(f"Unknown provider: {provider}")
    return _langraph_llm


# TODO: deprecated. Need to be removed
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
