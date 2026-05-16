from langchain_core.language_models.chat_models import BaseChatModel

from src.ai_generation.bpmn_agent.langgraph import (
    get_langgraph_llm_client,
)

SCRIPT = "src.ai_generation.bpmn_agent.langgraph"


def test_returns_valid_client(mocker):
    mockert_prvd = mocker.patch(f"{SCRIPT}._match_provider")
    mockert_prvd.return_value = ("gemini", "gemini-3.1-flash-lite-preview", "dummy_key")

    agent1 = get_langgraph_llm_client()
    agent2 = get_langgraph_llm_client()

    assert isinstance(agent1, BaseChatModel)
    assert isinstance(agent2, BaseChatModel)
    assert agent1 is not agent2  # different objects as run parallel
