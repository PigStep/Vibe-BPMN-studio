import re
from lxml import etree
import logging

from src.ai_generation.bpmn_agent.simple.state import SimpleBPMNAgent

logger = logging.getLogger(__name__)


def _clean_xml(raw_xml: str) -> str:
    """Clean markdown headers like ```xml from output"""
    pattern = r"```xml(.*?)```"
    match = re.search(pattern, raw_xml, re.DOTALL)
    if match:
        clean_xml_str = match.group(1).strip()
    else:
        # If there are no tags, try to remove random ``` at the beginning
        clean_xml_str = raw_xml.strip()
        if clean_xml_str.startswith("```"):
            clean_xml_str = clean_xml_str.replace("```", "").strip()

    return clean_xml_str


def validate_xml(state: SimpleBPMNAgent):
    """Clean from markdown and validate XML via lmxl"""
    raw_xml = state.get("xml_content", "")
    clean_xml_str = _clean_xml(raw_xml)

    try:
        # recover=False is critically important: we do NOT want the parser to silently fix errors.
        # We want to catch the error and force the LLM to rewrite.
        parser = etree.XMLParser(recover=False)
        etree.fromstring(clean_xml_str.encode("utf-8"), parser=parser)

        # Success
        logger.info(
            "session: %s. Processed XML is valid",
            state.get("thread_id", "id_not_found"),
        )
        return {
            **state,
            "clean_xml": clean_xml_str,
            "is_valid": True,
            "validation_error": None,
        }

    except etree.XMLSyntaxError as e:
        # Form a clear error message for the LLM
        error_msg = f"XML Syntax Error: {e.msg} at line {e.lineno}, column {e.offset}"
        logger.warning(
            "session: %s. LLM xml generation error: %s",
            state.get("thread_id", "id_not_found"),
            error_msg,
        )
        # Failure
        return {
            "clean_xml": None,
            "is_valid": False,
            "validation_error": error_msg,
        }
    except Exception as e:
        logger.error(
            "session: %s. Unexpected error while processing XML: %s",
            state.get("thread_id", "id_not_found"),
            e,
        )
        return {
            "clean_xml": None,
            "is_valid": False,
            "validation_error": f"Critical Error: {str(e)}",
        }
