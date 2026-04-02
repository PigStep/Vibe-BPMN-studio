from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field
from langchain_core.tools import tool
import logging

from requests import session
from src.ai_generation.llm_clients import LLMClient
from src.ai_generation.managers.llm_config import LLMConfigManager
from src.ai_generation.bpmn_agent.tools.generate_bpmn_draft.generate_xml import (
    generate_xml,
)
from src.ai_generation.bpmn_agent.tools.generate_bpmn_draft.imagine_process import (
    imagine_process,
)

logger = logging.getLogger(__name__)


class SGenerateDraftArgs(BaseModel):
    user_prompt: str = Field("User request for diagramm")


@tool(args_schema=SGenerateDraftArgs)
def generate_draft(user_prompt: str, config: RunnableConfig):
    """Generates bpmn draft based on user intent"""
    configurable = config.get("configurable", {})
    llm: LLMClient = configurable["llm"]
    config_manager: LLMConfigManager = configurable["config_manager"]
    session_id: str = configurable["session_id"]

    logger.info("[%s] generating draft", session_id)
    bpmn_plan = imagine_process(
        request=user_prompt,
        llm=llm,
        configuration=config_manager.get_call_config("business_generation"),
    )
    xml = generate_xml(
        process_description=bpmn_plan,
        llm=llm,
        configuration=config_manager.get_call_config("XML_generation"),
    )
    return xml
