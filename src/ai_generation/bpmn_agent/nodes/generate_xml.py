import logging

from langgraph.types import interrupt
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from src.ai_generation.bpmn_agent.nodes._extract_system_and_configuration import (
    extract_system_and_config,
)
from src.ai_generation.bpmn_agent.state import AgentState

logger = logging.getLogger(__name__)


def generate_xml(
    state: AgentState, llm: BaseChatModel, configuration: dict
) -> AgentState:
    """Generates XML code from instructions"""
    system, config_copy = extract_system_and_config(configuration)

    messages = state["messages"]
    if system:
        messages = [SystemMessage(content=system)] + messages
    logger.debug(
        "Session %s. XML generation messages: %s", state["session_id"], messages
    )
    xml_response = llm.bind(**config_copy).invoke(messages)
    logger.debug(
        "Session %s. LLM response: %s, text: '%s'",
        state["session_id"],
        xml_response,
        xml_response.text,
    )
    xml_content = xml_response.text
    logger.info("Session %s. Generating XML", state["session_id"])
    user_feedback = interrupt({"xml_result": xml_content})
    return {
        "messages": [  # type: ignore
            HumanMessage(content=user_feedback),
        ]
    }
