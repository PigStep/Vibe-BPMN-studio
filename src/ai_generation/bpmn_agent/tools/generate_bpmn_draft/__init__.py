from pydantic import BaseModel, Field
from langchain_core.tools import tool
from src.ai_generation.llm_clients import LLMClient
from src.ai_generation.managers.llm_config import LLMConfigManager
from src.ai_generation.bpmn_agent.tools.generate_bpmn_draft.generate_xml import (
    generate_xml,
)
from src.ai_generation.bpmn_agent.tools.generate_bpmn_draft.imagine_process import (
    imagine_process,
)


class SGenerateDraftArgs(BaseModel):
    user_prompt: str = Field("User request for diagramm")


@tool(args_schema=SGenerateDraftArgs)
def generate_draft(user_prompt: str, llm: LLMClient, config_manager: LLMConfigManager):
    """Generates bpmn draft based on user intent"""
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
