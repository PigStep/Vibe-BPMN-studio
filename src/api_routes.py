import asyncio
import logging
from fastapi import APIRouter, HTTPException

from src.get_example_diagram import get_example_diagramm
from src.ai_generation.bpmn_agent.simple.agent import invoke_agent
from src.schemas import SExampleBPMN, SAgentOutput, SUserInputData

router = APIRouter(
    tags=["API"],
)

logger = logging.getLogger(__name__)


# FIXME: user input typo. Use Schema
@router.get("/generate")
async def generate_bpmn(user_input: str) -> SAgentOutput:
    """
    Generate BPMN XML code to render with bpmn-js
    """
    user_data = SUserInputData(user_input=user_input)
    xml = await asyncio.to_thread(invoke_agent, user_data)
    return {
        "output": xml.get("previous_answer", "Sorry, tech problem. Please retry later.")
    }


@router.get("/example-bpmn-xml")
async def get_example_bpmn_xml() -> SExampleBPMN:
    """
    Get the base BPMN XML structure
    """
    logger.info("Asked for base BPMN XML")
    try:
        xml = await asyncio.to_thread(get_example_diagramm)
    except Exception as e:
        logger.error("Error getting example BPMN XML: " + str(e))
        raise HTTPException(status_code=500, detail=str(e))
    return {"xml": xml}
