from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import Secret, SecretStr
from settings import settings

_llm: BaseChatModel | None = None
provider = settings.PROVIDER_NAME


def get_langgraph_llm_client() -> BaseChatModel:
    provider = settings.PROVIDER_NAME
    global _llm
    if _llm is None:
        match provider:
            case "gemini":
                model = settings.OPENROUTER_MODEL_NAME
                key = settings.OPENROUTER_API_KEY

                if model is None or key is None:
                    raise ValueError(
                        f"Enviroment model and api_key were not set up. Check .env"
                    )

                _llm = ChatGoogleGenerativeAI(
                    model=model,
                    max_retries=7,
                    api_key=SecretStr(key),
                )
            case "openrouter":
                model = settings.OPENROUTER_MODEL_NAME
                key = settings.OPENROUTER_API_KEY

                if model is None or key is None:
                    raise ValueError(
                        f"Enviroment model and api_key were not set up. Check .env"
                    )

                _llm = ChatOpenAI(
                    model=model,
                    max_retries=7,
                    api_key=SecretStr(key),
                )
            case _:
                raise ValueError(f"Unknown provider: {provider}")
    return _llm


def reset_llm_client():
    global _llm
    _llm = None
