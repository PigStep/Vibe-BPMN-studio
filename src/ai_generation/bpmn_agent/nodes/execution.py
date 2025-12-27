import json
import logging
import asyncio

from ..state import BPMNState
from ...llm_client import LLMClient
from ...managers.promt import PromptManager
from ...managers.json_schema import (
    JsonSchemaManager,
)

logger = logging.getLogger(__name__)


def execute(
    state: BPMNState,
    llm: LLMClient,
    prompt_manager: PromptManager,
    json_schema_manager: JsonSchemaManager,
) -> BPMNState:
    # Get plan from state
    plan_dict = state["plan"]
    step_index = state["execution_step"]

    # Get step from plan
    current_step = plan_dict[step_index]["agent"]
    step_intent = plan_dict[step_index]["reason"]

    # Generate reply
    schema = json_schema_manager.get_schema(current_step)
    system_promt = prompt_manager.get_prompt(step_intent, "system")
    response = llm.generate_response_json_based(step_intent, schema, system_promt)
    return {**state, "messages": [response], "execution_step": step_index + 1}
