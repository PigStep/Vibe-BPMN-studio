from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from settings import settings

_llm: BaseChatModel | None = None
provider = settings.PROVIDER_NAME


def get_langgraph_llm_client() -> BaseChatModel:
    provider = settings.PROVIDER_NAME
    global _llm
    if _llm is None:
        match provider:
            case "gemini":
                _llm = ChatGoogleGenerativeAI(
                    model=settings.GEMINI_MODEL_NAME,
                    max_retries=2,
                    api_key=settings.GEMINI_API_KEY,
                )
            case "openrouter":
                # TODO: implement support
                _llm = ChatOpenAI()
            case _:
                raise ValueError(f"Unknown provider: {provider}")
    return _llm


def reset_llm_client():
    global _llm
    _llm = None
