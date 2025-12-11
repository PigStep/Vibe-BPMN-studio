import logging
from pathlib import Path

XML_BASE_BPMN_PATH = Path(__file__).parent / "data" / "base_bpmn_diagram.xml"

logger = logging.getLogger(__name__)


def get_base_diagramm():
    try:
        with open(XML_BASE_BPMN_PATH, encoding="utf-8", mode="r") as f:
            return f.read()
    except FileNotFoundError as e:
        logger.error(f"Файл {XML_BASE_BPMN_PATH} не найден")
        return "<error>File not found</error>"

    except Exception as e:
        logger.error(
            f"Непредвиденная ошибка при чтении файла {XML_BASE_BPMN_PATH}: {e}"
        )
        return "<error>Unknown error</error>"
