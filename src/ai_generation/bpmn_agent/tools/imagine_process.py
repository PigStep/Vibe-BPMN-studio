from langchain_core.tools import tool
from pydantic import BaseModel, Field
import logging
from src.ai_generation.bpmn_agent.state import SimpleBPMNAgent
from src.ai_generation.llm_clients import LLMClient

logger = logging.getLogger(__name__)


@tool
def generate_process() -> SimpleBPMNAgent:
    """Generate procces draft with xml code. Use this when user do not have XML code or want to get draft"""
    logger.info("Invoked draft process generation")
    return "successfully generated draft process. ANSWER USER YOU HAVE GENERATE CODE"
