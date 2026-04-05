from src.ai_generation.bpmn_agent.state import AgentState
from src.ai_generation.llm_clients import LLMClient


def generate_bpmn(state: AgentState, llm: LLMClient, configuration: dict) -> AgentState:
    """Genrates XML code from instructions

    Args:
        state (SimpleBPMNAgent): state of agent
        llm (LLMClient): llm client for content generation
        configuration (dict): configuration for the llm call (system_prompt, temperature, ...)

    Returns:
        SimpleBPMNAgent: modified state with generated XML in 'previous_answer' field
    """
    user_prompt = state["previous_answer"]
    result = llm.generate_response_text_based(user_prompt, **configuration)

    return {**state, "previous_answer": result}
