from typing import Any, Dict, List
from assemblers.json.base import JsonAssembler


class BpmnJsonAssembler(JsonAssembler):
    """
    Specialized assembler for BPMN.
    Acts as an Adapter: normalizes keys (Upper/Lower case, Synonyms).
    Can be used for passing to BpmnDirector.
    """

    def __init__(self):
        super().__init__(title="Unified BPMN Project")

    def get_data_for_director(self) -> Dict[str, Any]:
        """
        Returns a clean dictionary.
        Output keys are strictly: 'process', 'collaboration', 'flow', 'layout'.
        """
        defs = self.get_raw_definitions()

        clean_data = {
            "process": self._find_first(defs, ["Process", "process"]),
            "collaboration": self._find_first(defs, ["Collaboration", "collaboration"]),
            "flow": self._find_first(defs, ["Flows", "flows", "flow"]),
            "layout": self._find_first(
                defs, ["Layout", "layout", "Diagramm", "diagramm"]
            ),
        }

        # Remove empty values to avoid confusing validators
        return {k: v for k, v in clean_data.items() if v is not None}

    def _find_first(self, source: Dict, keys: List[str]) -> Dict | None:
        """Smart search: returns the value of the first found key from the list"""
        for key in keys:
            if key in source:
                return source[key]
        return None
