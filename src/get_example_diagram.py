import logging
from pathlib import Path

XML_BASE_BPMN_PATH = (
    Path(__file__).parent.parent / "data" / "XMLs" / "base_bpmn_diagram.xml"
)

logger = logging.getLogger(__name__)


def get_example_diagramm():
    try:
        with open(XML_BASE_BPMN_PATH, encoding="utf-8", mode="r") as f:
            return f.read()
    except FileNotFoundError as e:
        logger.error("File {} not found: {}".format(XML_BASE_BPMN_PATH, e))
        return "<error>File not found</error>"
    except Exception as e:
        logger.error(
            "Unexpected error while reading file {}: {}".format(XML_BASE_BPMN_PATH, e)
        )
        return "<error>Unknown error</error>"
