from openai import OpenAI
from typing_extensions import TypedDict, Annotated
import operator
from src.ai_generation.llm_client import LLMClient
from settings import get_settings

settings = get_settings()

AI_API_KEY = settings.OPENROUTER_API_KEY
MODEL_NAME = settings.OPENROUTER_MODEL_NAME

raw_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=AI_API_KEY)

clientBpmn = LLMClient(raw_client, MODEL_NAME)


def getBpmnClient():
    return clientBpmn


class BPMNState(TypedDict):
    messages: Annotated[list[str], operator.add]
