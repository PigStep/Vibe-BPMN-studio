import asyncio
import logging
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Header

from src.get_example_diagram import get_example_diagramm
from src.ai_generation.bpmn_agent.simple.agent import invoke_agent
from .schemas import SExampleBPMN, SAgentOutput, SUserInputData

router = APIRouter(
    tags=["API"],
)

logger = logging.getLogger(__name__)


@router.post("/generate")
async def generate_bpmn(
    user_input: SUserInputData, x_session_id: str = Header(default=None)
) -> SAgentOutput:
    """
    Generate BPMN XML code to render with bpmn-js.
    Uses X-Session-ID header to maintain conversation context.
    """
    if not x_session_id:
        # create fallback session_id
        x_session_id = str(uuid4())
        logger.warning("No session ID provided. Generated temporary: %s", x_session_id)

    logger.info(f"Processing request for session: {x_session_id}")
    try:
        xml = await asyncio.to_thread(invoke_agent, user_input, x_session_id)

        return {"output": xml.get("previous_answer")}
    except Exception as e:
        logger.error("Error in generation: %s with session_id %s", e, x_session_id)
        return {"output": "Sorry, tech problem. Please retry later."}


@router.post("/example-bpmn-xml")
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
