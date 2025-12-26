import json
import logging
from ..state import getBpmnClient, BPMNState
from src.ai_generation.llm_client import LLMClient
from src.ai_generation.promt_manager import get_prompt_manager

logger = logging.getLogger(__name__)


def plan(
    state: BPMNState,
    prompt_manager=None,
    llm: LLMClient = None,
) -> BPMNState:
    if llm is None:
        llm = getBpmnClient()
    if prompt_manager is None:
        prompt_manager = get_prompt_manager()

    intent = state.get("messages")[0]  # First input

    with open(r"data\bpmn_schemas\layout.json", "r", encoding="utf-8") as file:
        json_schema = json.load(file)  # FIXME decompose

    system_promt = prompt_manager.get_prompt("plan", "system")
    response = llm.generate_response_json_based(
        prompt=intent, system_promt=system_promt, json_schema=json_schema
    )

    if response is None:
        logger.warning("Error while generating response. JSON is not valid")
        return state

    return {**state, "messages": [response]}
