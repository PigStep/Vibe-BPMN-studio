from langgraph.types import interrupt

from src.ai_generation.bpmn_agent.simple.state import SimpleBPMNAgent


def wait_for_editing(state: SimpleBPMNAgent) -> SimpleBPMNAgent:
    """Call interrupt function to save agent state and wait for new input

    Args:
        state (SimpleBPMNAgent): state of agent
        llm (LLMClient): llm client for content generation

    Returns:
        SimpleBPMNAgent: modified state with interrupt values in `__interrupt__`field
    """

    user_edit_promt = interrupt(
        {
            "content": "Share your feedback. Ask me anything to edit!",
        }
    )

    # Update the state with the edited version
    return {**state, "user_edit_promt": user_edit_promt}
