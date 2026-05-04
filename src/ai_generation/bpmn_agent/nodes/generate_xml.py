import logging

from langgraph.types import interrupt
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from src.ai_generation.bpmn_agent.state import AgentState

logger = logging.getLogger(__name__)


def generate_xml(
    state: AgentState, llm: BaseChatModel, configuration: dict
) -> AgentState:
    """Generates XML code from instructions"""
    # Using copy because working with global object (partial)
    config_copy = configuration.copy()
    system = config_copy.pop("system_prompt", None)
    messages = state["messages"]
    if system:
        messages = [SystemMessage(content=system)] + messages
    xml_response = llm.bind(**config_copy).invoke(messages)
    xml_content = xml_response.text
    logger.info("Session %s. Generating XML", state["session_id"])
    user_feedback = interrupt({"xml_result": xml_content})
    return {
        "messages": [  # type: ignore
            AIMessage(content=xml_content),
            HumanMessage(content=user_feedback),
        ]
    }
