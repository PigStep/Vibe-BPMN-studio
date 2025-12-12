import asyncio
import logging
from fastapi import APIRouter
from src.get_example_diagram import get_example_diagramm
from .schemas import SExampleBPMN

router = APIRouter(
    tags=["API"],
)

logger = logging.getLogger(__name__)


@router.post("/generate")
async def generate_bpmn():
    """
    Generate BPMN XML code to render with bpmn-js
    """
    # TODO for future realization
    return {"message": "BPMN generation endpoint"}


@router.get("/example-bpmn-xml")
async def get_example_bpmn_xml() -> SExampleBPMN:
    """
    Get the base BPMN XML structure
    """
    logger.info("Asked for base BPMN XML")
    try:
        xml = await asyncio.to_thread(get_example_diagramm)
    except Exception as e:
        logger.error(f"Error getting example BPMN XML: {e}")
        return {"error": str(e)}
    return {"xml": xml}
