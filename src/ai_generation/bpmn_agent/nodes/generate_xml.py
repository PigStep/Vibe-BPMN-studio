from langchain_core.messages import SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from src.ai_generation.bpmn_agent.state import AgentState


def generate_xml(
    state: AgentState, llm: BaseChatModel, configuration: dict
) -> AgentState:
    """Generates XML code from instructions"""
    system = configuration.pop("system_prompt", None)
    messages = state["messages"]
    if system:
        messages = [SystemMessage(content=system)] + messages
    llm = llm.bind(**configuration)
    result = llm.invoke(messages)
    return {"messages": [result]}
