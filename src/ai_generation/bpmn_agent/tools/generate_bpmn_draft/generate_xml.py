from src.ai_generation.bpmn_agent.state import SimpleBPMNAgent
from src.ai_generation.llm_clients import LLMClient


def generate_xml(
    process_description: str, llm: LLMClient, configuration: dict
) -> SimpleBPMNAgent:
    """Genrates XML code from instructions

    Args:
        state (SimpleBPMNAgent): state of agent
        llm (LLMClient): llm client for content generation
        configuration (dict): configuration for the llm call (system_prompt, temperature, ...)

    Returns:
        SimpleBPMNAgent: modified state with generated XML in 'previous_answer' field
    """
    user_prompt = process_description
    result = llm.generate_response_text_based(user_prompt, **configuration)

    return result
