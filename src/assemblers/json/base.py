import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class JsonAssembler:
    """
    Base class.
    Responsible only for accumulating data and saving to file.
    """

    def __init__(self, title: str = "Unified Project"):
        self._storage = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": title,
            "type": "object",
            "definitions": {},
        }

    def add_part(self, schema_name: str, content: Dict[str, Any]) -> None:
        """
        Adds a JSON fragment to definitions.
        """
        if not schema_name:
            logger.warning("Attempted to add part without schema_name")
            return

        self._storage["definitions"][schema_name] = content
        logger.debug(f"Added schema part: {schema_name}")

    def add_parts_from_list(self, parts: List[Dict[str, Any]]) -> None:
        """Bulk addition from a list of dictionaries"""
        for part in parts:
            name = part.get("schema_name")
            if name:
                self.add_part(name, part)
            else:
                logger.warning(f"Skipping part without 'schema_name': {part.keys()}")

    def get_raw_definitions(self) -> Dict[str, Any]:
        """Returns raw definitions as is."""
        return self._storage["definitions"]

    def save_to_file(self, output_file: str) -> bool:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(self._storage, f, indent=4, ensure_ascii=False)
            logger.info(f"JSON saved to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save JSON: {e}")
            return False
