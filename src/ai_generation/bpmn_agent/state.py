from typing import List
from typing_extensions import TypedDict, Annotated
import operator
from src.ai_generation.llm_clients import get_llm_client


def getBpmnClient():
    return get_llm_client()


class BPMNState(TypedDict):
    messages: Annotated[list[str], operator.add]
    generated_jsons: Annotated[List[dict], operator.add]
    plan: List[dict]
    execution_step: int
