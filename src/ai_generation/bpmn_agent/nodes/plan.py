import json
import logging

from ..state import getBpmnClient, BPMNState
from src.ai_generation.llm_client import LLMClient
from src.ai_generation.managers.promt import get_prompt_manager
from src.ai_generation.managers.json_schema import get_json_schema_namager

logger = logging.getLogger(__name__)


def plan(
    state: BPMNState,
    prompt_manager=None,
    schema_manager=None,
    llm: LLMClient = None,
) -> BPMNState:
    # Define default
    if llm is None:
        llm = getBpmnClient()
    if prompt_manager is None:
        prompt_manager = get_prompt_manager()
    if schema_manager is None:
        schema_manager = get_json_schema_namager()

    # get message

    intent = state.get("messages")[0]  # First input
    system_promt = prompt_manager.get_prompt("plan", "system")
    response = llm.generate_response_json_based(
        prompt=intent,
        system_promt=system_promt,
        json_schema=schema_manager.get_schema("plan"),
    )

    if response is None:
        logger.warning("Error while generating response. JSON is not valid")
        return state

    plan = json.loads(response)["plan"]
    return {**state, "messages": [response], "plan": plan}
