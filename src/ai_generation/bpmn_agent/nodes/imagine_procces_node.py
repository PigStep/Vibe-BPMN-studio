from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage
from src.ai_generation.bpmn_agent.state import AgentState


def generate_process(
    state: AgentState, llm: BaseChatModel, configuration: dict
) -> AgentState:
    """Generate business process as plan for given instructions"""
    system = configuration.pop("system_prompt", None)
    messages = state["messages"]
    if system:
        messages = [SystemMessage(content=system)] + messages

    llm = llm.bind(**configuration)
    result = llm.invoke(messages)
    return {"messages": [result]}
