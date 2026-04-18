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
    system = configuration.pop("system_prompt", None)
    messages = state["messages"]
    if system:
        messages = [SystemMessage(content=system)] + messages
    llm = llm.bind(**configuration)
    logger.info("Session %s. Generating XML", state["session_id"])
    xml_content = llm.invoke(messages)
    # FIXME: return DEBUG - Agent was interupted. Interrupt message: [Interrupt(value={'xml_result': ''}, id='78b2a0fb7b787961739438f6d1884e94')]
    # At the second iteration. Find why
    user_feedback = interrupt({"xml_result": xml_content.text})
    return {
        "messages": [
            AIMessage(content=xml_content),
            HumanMessage(content=user_feedback),
        ]
    }
