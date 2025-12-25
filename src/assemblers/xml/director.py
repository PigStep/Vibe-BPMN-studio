from typing import Dict, Any
from .bpmn import BpmnBuilder


class BpmnDirector:
    def __init__(self, builder: BpmnBuilder | None):
        if builder is None:
            self.builder = BpmnBuilder()
        self.builder = builder

    def construct_from_json(self, data: Dict[str, Any]):
        """
        Parses JSON data and creates a BPMN diagram in XNL
        """
        self._create_definitions()
        self._handle_collaboration(data)
        proc_id = self._handle_process(data)
        self._handle_layout(data, proc_id)

    def _create_definitions(self):
        self.builder.create_definitions(def_id="Definitions_1")

    def _handle_collaboration(self, data: Dict[str, Any]):
        if collab_data := data.get("collaboration"):
            collab_node = self.builder.add_collaboration(collab_data["id"])
            for p in collab_data.get("participants", []):
                self.builder.add_participant(
                    collab_node, p["id"], p.get("name"), p["processRef"]
                )

    def _handle_process(self, data: Dict[str, Any]) -> str:
        if proc_data := data.get("process"):
            self.builder.start_process(proc_data["id"], proc_data.get("name"))
            for node in proc_data.get("nodes", []):
                self.builder.add_node(
                    node_type=node["type"],
                    node_id=node["id"],
                    name=node.get("name"),
                )
            flows = data.get("flow", {}).get("flows", [])
            for flow in flows:
                self.builder.add_flow(
                    flow_id=flow["id"],
                    source=flow["sourceRef"],
                    target=flow["targetRef"],
                    name=flow.get("name"),
                )
            return proc_data["id"]
        raise ValueError("Process data missing")

    def _handle_layout(self, data: Dict[str, Any], proc_id: str):
        if layout_data := data.get("layout"):
            self.builder.init_diagram(proc_id)
            for pos in layout_data.get("positions", []):
                b = pos["bounds"]
                self.builder.add_shape(
                    element_id=pos["elementId"],
                    x=b["x"],
                    y=b["y"],
                    w=b["width"],
                    h=b["height"],
                )

    def to_string(self) -> str:
        return self.builder.to_string()
