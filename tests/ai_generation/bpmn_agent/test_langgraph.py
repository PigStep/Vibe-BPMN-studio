import pytest
from src.ai_generation.bpmn_agent.langgraph import (
    reset_llm_client,
    get_langgraph_llm_client,
)

SCRIPT = "src.ai_generation.bpmn_agent.langgraph"


def test_returns_same_instance(mocker):
    mockert_prvd = mocker.patch(f"{SCRIPT}._match_provider")
    mockert_prvd.return_value = ("gemini", "gemini-3.1-flash-lite-preview", "dummy_key")

    reset_llm_client()

    agent1 = get_langgraph_llm_client()
    agent2 = get_langgraph_llm_client()

    assert agent1 is agent2
