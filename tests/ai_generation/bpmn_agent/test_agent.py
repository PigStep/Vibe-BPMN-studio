from unittest.mock import MagicMock

import pytest
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, Interrupt, interrupt

from src.ai_generation.bpmn_agent.langgraph import reset_llm_client
from src.schemas import SUserInputData
from src.ai_generation.bpmn_agent.agent import invoke_agent

SCRIPT = "src.ai_generation.bpmn_agent.agent"


@pytest.fixture
def mock_get_agent(mocker):
    mock_get_agent_f = mocker.patch(f"{SCRIPT}.get_agent")
    mock_agent = mocker.MagicMock()
    mock_cp = mocker.MagicMock()
    mock_get_agent_f.return_value = (mock_agent, mock_cp)

    return mock_get_agent_f, mock_agent, mock_cp


def test_new_session_sends_initial_state(mock_get_agent):
    mock_get_agent_f, mock_agent, mock_cp = mock_get_agent
    mock_cp.get_tuple.return_value = None
    mock_get_agent_f.return_value = (mock_agent, mock_cp)

    mock_agent.invoke.return_value = {
        "messages": [AIMessage([{"text": "ok"}])],
    }

    invoke_agent(SUserInputData(session_id="s1", user_input="hello"))

    mock_agent.invoke.assert_called_once()
    args, _ = mock_agent.invoke.call_args
    state = args[0]
    assert isinstance(state, dict)
    assert state["session_id"] == "s1"
    assert any(getattr(m, "content", None) == "hello" for m in state["messages"])


def test_existing_session_sends_command_resume(mock_get_agent):
    _, mock_agent, mock_cp = mock_get_agent
    mock_cp.get_tuple.return_value = {
        "something": "existing"
    }  # checkpointer dict existing

    mock_agent.invoke.return_value = {
        "messages": [AIMessage([{"text": "ok"}])],
    }

    invoke_agent(SUserInputData(session_id="s1", user_input="continue"))

    mock_agent.invoke.assert_called_once()
    args, _ = mock_agent.invoke.call_args
    assert isinstance(args[0], Command)
    assert args[0].resume == "continue"


def test_agent_memory_pipeline(mock_get_agent):
    _, mock_agent, mock_cp = mock_get_agent
    mock_cp.get_tuple.side_effect = [
        None,
        {"some": "state"},
    ]  # checkpointer don't exists in first run

    mock_agent.invoke.return_value = {
        "messages": [AIMessage([{"text": "ok"}])],
    }

    invoke_agent(SUserInputData(session_id="s1", user_input="hello"))
    expected_config = {"configurable": {"thread_id": "s1"}}
    mock_cp.get_tuple.assert_called_once_with(expected_config)

    args, _ = mock_agent.invoke.call_args
    state = args[0]
    assert isinstance(state, dict)  # created initial state
    assert state["session_id"] == "s1"

    invoke_agent(SUserInputData(session_id="s1", user_input="continue"))
    assert mock_cp.get_tuple.call_count == 2
    mock_cp.get_tuple.assert_called_with(expected_config)  # same config used

    args, _ = mock_agent.invoke.call_args
    assert isinstance(args[0], Command)  # resumed state
    assert args[0].resume == "continue"


def test_returns_xml_from_interrupt(mock_get_agent):
    _, mock_agent, _ = mock_get_agent

    mock_agent.invoke.return_value = {
        "__interrupt__": [
            Interrupt(value={"xml_result": "<bpmn />"}, id="x"),
        ],
    }

    result = invoke_agent(SUserInputData(session_id="s1", user_input="generate xml"))

    assert result == "<bpmn />"


def test_full_pipeline_calls_both_nodes(mocker):
    mocker.patch(f"{SCRIPT}.get_langgraph_llm_client")
    mocker.patch(f"{SCRIPT}.LLMConfigManager")

    mock_process = mocker.patch(f"{SCRIPT}.generate_process")
    mock_xml = mocker.patch(f"{SCRIPT}.generate_xml")

    mock_process.return_value = {
        "messages": [AIMessage([{"text": "imagine done"}])],
    }
    mock_xml.side_effect = lambda state, **kw: interrupt({"xml_result": "<bpmn/>"})

    reset_llm_client()

    result = invoke_agent(SUserInputData(session_id="s1", user_input="make bpmn"))

    assert mock_process.called
    assert mock_xml.called
    assert result == "<bpmn/>"
