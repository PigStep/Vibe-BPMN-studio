import logging

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage
from src.ai_generation.bpmn_agent.nodes._extract_system_and_configuration import (
    extract_system_and_config,
)
from src.ai_generation.bpmn_agent.state import AgentState

logger = logging.getLogger(__name__)


def generate_process(
    state: AgentState, llm: BaseChatModel, configuration: dict
) -> AgentState:
    """Generate business process as plan for given instructions"""
    system, config_copy = extract_system_and_config(configuration)

    messages = state["messages"]
    if system:
        messages = [SystemMessage(content=system)] + messages

    logger.info("Session %s. Generating BPMN business procces", state["session_id"])
    result = llm.bind(**config_copy).invoke(messages)

    return {"messages": [result]}  # type: ignore
