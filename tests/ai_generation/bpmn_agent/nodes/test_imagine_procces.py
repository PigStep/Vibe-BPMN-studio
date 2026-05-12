from unittest.mock import MagicMock

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import pytest

from src.ai_generation.bpmn_agent.nodes.imagine_procces_node import generate_process


@pytest.fixture
def mock_llm():
    mock_llm = MagicMock()
    mock_llm.bind.return_value = mock_llm
    mock_llm.invoke.return_value = AIMessage(content="plan")

    return mock_llm


def test_adds_system_prompt_when_configured(mock_llm):
    state = {
        "messages": [HumanMessage(content="do something")],
        "session_id": "test",
    }
    config = {"system_prompt": "You are a helpful assistant", "temperature": 0.7}

    result = generate_process(state, mock_llm, config)  # type: ignore

    invoked_messages = mock_llm.invoke.call_args[0][0]

    # system message must be first for best answers
    assert isinstance(invoked_messages[0], SystemMessage)
    assert any(
        isinstance(m, HumanMessage) and m.content == "do something"
        for m in invoked_messages
    )
    assert result == {"messages": [AIMessage(content="plan")]}


def test_skips_system_prompt_when_not_configured(mock_llm):
    state = {
        "messages": [HumanMessage(content="do something")],
        "session_id": "test",
    }
    config = {"temperature": 0.5}

    generate_process(state, mock_llm, config)  # type: ignore

    invoked_messages = mock_llm.invoke.call_args[0][0]
    assert not any(isinstance(m, SystemMessage) for m in invoked_messages)


def test_returns_llm_response_in_messages(mock_llm):
    expected_response = AIMessage(content="result")
    mock_llm.invoke.return_value = expected_response

    state = {
        "messages": [HumanMessage(content="hello")],
        "session_id": "test",
    }
    config = {}

    result = generate_process(state, mock_llm, config)  # type: ignore

    # Do not check for [Human("hello"), AImessage("result")] in result
    # Langgraph create AgentState wrap with operator `add`

    # Function output -> {"messages": [AImessage("result")]}
    # Lanngraph after warpping -> {"messages": [Human("hello"), AImessage("result")]}

    assert result == {"messages": [expected_response]}
