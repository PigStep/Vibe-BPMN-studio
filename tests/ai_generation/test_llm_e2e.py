"""
E2E tests for LLM client using OpenRouter.
Tests verify real API calls and compare reasoning modes by execution time.
"""

from typing import Literal

from pydantic import BaseModel
import pytest
import time
import src.ai_generation.llm_client as llm_client_module
from src.ai_generation.llm_client import get_llm_client

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


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Set test environment to use .env.test"""
    monkeypatch.setenv("ENVIROMENT", "test")
    llm_client_module._llm_client = None


@pytest.mark.parametrize("reasoning_mode", ["minimal", "high"])
def test_llm_e2e_text_with_reasoning(reasoning_mode: ReasoningMode):
    """
    E2E test: text-based response with different reasoning modes.
    Compares execution time between minimal and high reasoning effort.
    """
    llm = get_llm_client()

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


def test_llm_e2e_json():
    """
    E2E test: JSON-based response with reasoning modes.
    Verifies JSON structure is returned correctly.
    """
    llm = get_llm_client()

    schema = {
        "type": "object",
        "properties": {
            "steps": {"type": "array", "items": {"type": "string"}},
            "duration": {"type": "integer"},
        },
    }

    result = llm.generate_response_json_based(
        prompt="Create a plan with 3 steps",
        json_schema=schema,
        system_prompt=SYSTEM_PROMPT,
    )

    assert result is not None
    assert "steps" in result


def test_llm_e2e_bpmn_baseline_schema():
    """
    E2E test: Generate BPMN process using baseline schema.
    Validates LLM output against SBpmnBaselineProcess Pydantic model.
    Domain: Order Processing (Receive Order -> Process Payment -> Ship)
    """
    llm = get_llm_client()

    schema = SBpmnBaselineProcess.model_json_schema(mode="validation")

    result = llm.generate_response_json_based(
        prompt="""Create a simple order processing workflow with:
        - Start event: Order Received
        - Task: Process Payment  
        - Task: Ship Order
        - End event: Order Complete
        - Flows connecting them in sequence""",
        json_schema=schema,
        system_prompt=SYSTEM_PROMPT,
        reasoning_mode="minimal",
    )

    assert result is not None

    print(result)
    validated = SBpmnBaselineProcess.model_validate(result)
    assert validated.schema_name == "baseline_process"
    assert validated.id
    assert validated.name
    assert len(validated.nodes) >= 3
    assert len(validated.flows) >= 2
