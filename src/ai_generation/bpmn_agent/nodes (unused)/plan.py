import json
import logging
import re

from ..state import BPMNState
from src.ai_generation.llm_client import LLMClient
from ai_generation.managers.llm_config import LLMConfigManager
from src.ai_generation.managers.json_schema import JsonSchemaManager

logger = logging.getLogger(__name__)


def parse_llm_json(llm_output: str):
    # 1. Remove markdown code blocks ```json ... ``` or just ``` ... ```
    clean_text = re.sub(r"```(json)?", "", llm_output, flags=re.IGNORECASE)
    clean_text = clean_text.strip()

    # 2. If any stray backticks remain at the end
    clean_text = clean_text.replace("```", "")

    try:
        return json.loads(clean_text)
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}")
        print(f"Raw content: {clean_text}")
        return None


def plan(
    state: BPMNState,
    prompt_manager: LLMConfigManager,
    schema_manager: JsonSchemaManager,
    llm: LLMClient,
) -> BPMNState:
    # get message

    intent = state.get("messages")[0]  # First input
    system_promt = prompt_manager.get_call_config("plan", "system")
    response = llm.generate_response_json_based(
        prompt=intent,
        system_prompt=system_promt,
        json_schema=schema_manager.get_schema("plan"),
    )

    if response is None:
        logger.warning("Error while generating response. JSON is not valid")
        return state

    logger.info("Plan response generated, plan length: %s", len(response))
    plan = parse_llm_json(response)["execution_steps"]
    return {**state, "messages": [response], "plan": plan}
