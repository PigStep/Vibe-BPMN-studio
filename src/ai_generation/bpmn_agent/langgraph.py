from typing import Literal

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import SecretStr
from settings import settings

provider = settings.PROVIDER_NAME


def _match_provider() -> tuple[Literal["gemini", "openrouter"], str, str]:
    provider = settings.PROVIDER_NAME

    if provider == "gemini":
        model = settings.GEMINI_MODEL_NAME
        api_key = settings.GEMINI_API_KEY
    elif provider == "openrouter":
        model = settings.OPENROUTER_MODEL_NAME
        api_key = settings.OPENROUTER_API_KEY
    else:
        raise ValueError(f"Unknown provider: {provider}")

    if model is None or api_key is None:
        raise ValueError(
            f"Missing model or API key for provider '{provider}'. "
            "Check your environment variables."
        )

    return provider, model, api_key


def get_langgraph_llm_client() -> BaseChatModel:
    provider, model, api_key = _match_provider()

    if provider == "gemini":
        llm = ChatGoogleGenerativeAI(
            model=model,
            max_retries=7,
            api_key=SecretStr(api_key),
        )
    elif provider == "openrouter":
        llm = ChatOpenAI(
            model=model,
            max_retries=7,
            api_key=SecretStr(api_key),
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")
    return llm
