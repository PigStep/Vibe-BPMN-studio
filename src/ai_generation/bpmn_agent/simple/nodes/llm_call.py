from typing_extensions import Literal
from src.ai_generation.bpmn_agent.simple.state import SimpleBPMNAgent
from src.ai_generation.llm_client import LLMClient


def llm_call(
    state: SimpleBPMNAgent,
    llm: LLMClient,
    user_prompt_key: Literal["user_input", "...<other_keys_from_state>"],
    configuration: dict,
) -> SimpleBPMNAgent:
    """Create a llm call with specific params

    Args:
        state (SimpleBPMNAgent): state of agent
        llm (LLMClient): llm client for content generation
        user_prompt (Literal): key from state with instruction on what to do with imported data
        configuration (dict): configuration for the llm call (system_prompt, temperature, ...)

    Returns:
        SimpleBPMNAgent: modified state with generated XML in 'previous_answer' field
    """
    user_prompt_key = state[user_prompt_key]
    result = llm.generate_response_text_based(user_prompt_key, **configuration)

    return {**state, "previous_answer": result}
