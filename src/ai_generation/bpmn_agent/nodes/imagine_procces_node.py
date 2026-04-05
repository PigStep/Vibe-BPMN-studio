from src.ai_generation.bpmn_agent.state import AgentState
from src.ai_generation.llm_clients import LLMClient


def generate_process(
    state: AgentState, llm: LLMClient, configuration: dict
) -> AgentState:
    """Generate business process as plan for given instructions

    Args:
        state (SimpleBPMNAgent): state of agent
        llm (LLMClient): llm client for content generation
        configuration (dict): configuration for the llm call (system_prompt, temperature, ...)

    Returns:
        SimpleBPMNAgent: modified state with generated XML in 'previous_answer' field
    """
    user_prompt = state["user_input"]
    result = llm.generate_response_text_based(user_prompt, **configuration)

    return {**state, "previous_answer": result}
