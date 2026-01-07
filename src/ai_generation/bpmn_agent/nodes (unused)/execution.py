import logging

from ..state import BPMNState
from ...llm_client import LLMClient
from ...managers.llm_config import LLMConfigManager
from ...managers.json_schema import (
    JsonSchemaManager,
)

logger = logging.getLogger(__name__)


def execute(
    state: BPMNState,
    llm: LLMClient,
    prompt_manager: LLMConfigManager,
    schema_manager: JsonSchemaManager,
) -> BPMNState:
    # Get plan from state
    plan_dict = state["plan"]
    step_index = state["execution_step"]

    # Get step from plan
    current_step = plan_dict[step_index]["step_key"]
    system_promt = plan_dict[step_index]["system_instruction"]
    step_intent = plan_dict[step_index]["task_context"]
    logger.info("Running %s step '%s'", current_step, step_intent)

    # Generate reply
    schema = schema_manager.get_schema(current_step)
    response = llm.generate_response_json_based(step_intent, schema, system_promt)
    return {**state, "messages": [response], "execution_step": step_index + 1}
