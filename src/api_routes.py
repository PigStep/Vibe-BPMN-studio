import asyncio
import logging
from unittest import result
from fastapi import APIRouter, HTTPException

from src.get_example_diagram import get_example_diagramm
from src.ai_generation.bpmn_agent.agent import invoke_agent
from src.schemas import SExampleBPMN, SAgentOutput, SUserInputData
from src.task_registry import TaskRegistry

router = APIRouter(
    tags=["API"],
)

logger = logging.getLogger(__name__)


@router.post("/generate")
async def generate_bpmn(user_data: SUserInputData) -> SAgentOutput:
    """
    Generate BPMN XML code to render with bpmn-js
    """
    logger.info("Recived diagram request. SessionID: %s", user_data.session_id)
    task = asyncio.create_task((invoke_agent(user_data)))
    TaskRegistry.register(user_data.session_id, task)
    xml = await task
    return {"output": xml}


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
