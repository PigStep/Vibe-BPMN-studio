"""
E2E tests for LLM client using OpenRouter.
Tests verify real API calls and compare reasoning modes by execution time.
"""

from typing import Literal
from unittest.mock import Mock

from pydantic import BaseModel
import pytest
import time

SYSTEM_PROMPT = """You are an expert in business process analysis.
Your task is to thoroughly analyze each request, consider all possible
variants, identify hidden dependencies, and provide the most optimal
solution. Explain your reasoning step by step."""

ReasoningMode = Literal["minimal", "high"]


# used for LLM json output validation
class SBpmnNode(BaseModel):
    id: str
    name: str
    type: Literal[
        "startEvent",
        "endEvent",
        "task",
        "userTask",
        "serviceTask",
        "exclusiveGateway",
        "parallelGateway",
        "subProcess",
    ]


class SBpmnFlow(BaseModel):
    id: str
    name: str | None = None
    sourceRef: str
    targetRef: str


class SBpmnBaselineProcess(BaseModel):
    schema_name: Literal["baseline_process"]
    id: str
    name: str
    nodes: list[SBpmnNode]
    flows: list[SBpmnFlow]


@pytest.mark.skip(reason="Using langgraph now, deprecated logic")
@pytest.mark.parametrize("reasoning_mode", ["minimal", "high"])
def test_llm_e2e_text_with_reasoning(reasoning_mode: ReasoningMode):
    """
    E2E test: text-based response with different reasoning modes.
    Compares execution time between minimal and high reasoning effort.
    """
    # FIXME: previous behaviour mocked. No longer exists
    llm = Mock()

    start = time.time()
    result = llm.generate_response_text_based(
        prompt="Describe the employee hiring process",
        system_prompt=SYSTEM_PROMPT,
        reasoning_mode=reasoning_mode,
    )
    elapsed = time.time() - start

    assert result is not None
    assert len(result) > 0

    print(
        f"\nreasoning_mode={reasoning_mode}, time={elapsed:.2f}s, length={len(result)}"
    )


@pytest.mark.skip(reason="Using langgraph now, deprecated logic")
def test_llm_e2_json_schema():
    """
    E2E test: Generate BPMN process using baseline schema.
    Validates LLM output against SBpmnBaselineProcess Pydantic model.
    Domain: Order Processing (Receive Order -> Process Payment -> Ship)
    """
    # FIXME: previous behaviour mocked. No longer exists

    llm = Mock()

    result = llm.generate_response_json_based(
        prompt="""Create a simple order processing workflow with:
        - Start event: Order Received
        - Task: Process Payment  
        - Task: Ship Order
        - End event: Order Complete
        - Flows connecting them in sequence""",
        json_schema=SBpmnBaselineProcess,
        system_prompt=SYSTEM_PROMPT,
        reasoning_mode="minimal",
    )

    assert result is not None

    print(result)
    validated = SBpmnBaselineProcess.model_validate_json(result)
    assert validated.schema_name == "baseline_process"
    assert validated.id
    assert validated.name
    assert len(validated.nodes) >= 3
    assert len(validated.flows) >= 2
