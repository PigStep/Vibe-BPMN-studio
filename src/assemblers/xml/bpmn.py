from typing import Optional
from lxml import etree
import logging
from .base_xml import BaseXmlBuilder


logger = logging.getLogger(__name__)


class BpmnBuilder(BaseXmlBuilder):
    """
    BPMN XML Builder

    XML Structure:
    <definitions>
        <collaboration> [Optional]
            <participant />
        </collaboration>
        <process id="...">
            <startEvent /> -> <userTask /> -> <sequenceFlow />
        </process>
        <BPMNDiagram>
            <BPMNPlane>
                <BPMNShape> <Bounds /> </BPMNShape>
            </BPMNPlane>
        </BPMNDiagram>
    </definitions>

    """

    _BPMN_NAMESPACES = {
        "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
        "dc": "http://www.omg.org/spec/DD/20100524/DC",
        "di": "http://www.omg.org/spec/DD/20100524/DI",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }

    def __init__(self):
        super().__init__(self._BPMN_NAMESPACES)
        # Builder state (cursors)
        self._current_process: Optional[etree.Element] = None
        self._current_plane: Optional[etree.Element] = None

    def create_definitions(self, def_id: str) -> "BpmnBuilder":
        self.create_root(
            "definitions",
            "bpmn",
            id=def_id,
            targetNamespace="http://bpmn.io/schema/bpmn",
            exporter="UnifiedBPMNAssembler",
        )
        return self

    def add_collaboration(self, collab_id: str) -> etree.Element:
        """Create collaboration container"""
        return self.create_element(self.root, "collaboration", "bpmn", id=collab_id)

    def add_participant(
        self, parent_collab: etree.Element, p_id: str, name: str, process_ref: str
    ):
        self.create_element(
            parent_collab,
            "participant",
            "bpmn",
            id=p_id,
            name=name,
            processRef=process_ref,
        )

    def start_process(self, proc_id: str, name: str) -> "BpmnBuilder":
        """Create a process and set it as the current active context"""
        self._current_process = self.create_element(
            self.root, "process", "bpmn", id=proc_id, name=name, isExecutable="false"
        )
        return self

    def add_node(self, node_type: str, node_id: str, name: str) -> "BpmnBuilder":
        """Add a node to the current active process"""
        if self._current_process is None:
            raise ValueError("Start a process before adding nodes")

        self.create_element(
            self._current_process, node_type, "bpmn", id=node_id, name=name
        )
        return self

    def add_flow(
        self, flow_id: str, source: str, target: str, name: str = ""
    ) -> "BpmnBuilder":
        if self._current_process is None:
            raise ValueError("Start a process before adding flows")

        self.create_element(
            self._current_process,
            "sequenceFlow",
            "bpmn",
            id=flow_id,
            name=name,
            sourceRef=source,
            targetRef=target,
        )
        return self

    def init_diagram(self, process_ref: str) -> "BpmnBuilder":
        diagram = self.create_element(
            self.root, "BPMNDiagram", "bpmndi", id="BPMNDiagram_1"
        )
        self._current_plane = self.create_element(
            diagram, "BPMNPlane", "bpmndi", id="BPMNPlane_1", bpmnElement=process_ref
        )
        return self

    def add_shape(
        self, element_id: str, x: float, y: float, w: float, h: float
    ) -> "BpmnBuilder":
        if self._current_plane is None:
            raise ValueError("Init diagram before adding shapes")

        shape = self.create_element(
            self._current_plane,
            "BPMNShape",
            "bpmndi",
            id=f"{element_id}_di",
            bpmnElement=element_id,
        )
        self.create_element(shape, "Bounds", "dc", x=x, y=y, width=w, height=h)
        return self
