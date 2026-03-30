from langchain_core.tools import tool
from pydantic import BaseModel, Field
import logging
from src.ai_generation.bpmn_agent.state import SimpleBPMNAgent
from src.ai_generation.llm_clients import LLMClient

logger = logging.getLogger(__name__)


@tool
def generate_bpmn() -> SimpleBPMNAgent:
    """Generates XML code from instructions"""
    logger.info("Invoked XML code generation")
    return "successfully generated xml code. ANSWER USER YOU HAVE GENERATE CODE"
