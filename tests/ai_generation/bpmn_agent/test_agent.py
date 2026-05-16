from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from langchain_core.messages import AIMessage
from langgraph.types import Command, Interrupt, interrupt

from src.schemas import SUserInputData
from src.ai_generation.bpmn_agent.agent import invoke_agent

SCRIPT = "src.ai_generation.bpmn_agent.agent"


@pytest.fixture
def mock_get_agent():
    with patch(f"{SCRIPT}.get_agent") as mock_get_agent_f:
        mock_agent = AsyncMock()
        mock_cp = MagicMock()
        mock_get_agent_f.return_value = (mock_agent, mock_cp)
        yield mock_get_agent_f, mock_agent, mock_cp


@pytest.mark.asyncio
async def test_new_session_sends_initial_state(mock_get_agent):
    _, mock_agent, mock_cp = mock_get_agent
    # Session do not exists
    mock_cp.get_tuple.return_value = None

    mock_agent.ainvoke.return_value = {
        "messages": [AIMessage([{"text": "ok"}])],
    }

    await invoke_agent(SUserInputData(session_id="s1", user_input="hello"))

    mock_agent.ainvoke.assert_awaited_once()
    args, _ = mock_agent.ainvoke.call_args
    state = args[0]
    assert isinstance(state, dict)
    assert state["session_id"] == "s1"
    assert any(getattr(m, "content", None) == "hello" for m in state["messages"])


@pytest.mark.asyncio
async def test_existing_session_sends_command_resume(mock_get_agent):
    _, mock_agent, mock_cp = mock_get_agent
    mock_cp.get_tuple.return_value = {
        "something": "existing"
    }  # checkpointer dict existing

    mock_agent.ainvoke.return_value = {
        "messages": [AIMessage([{"text": "ok"}])],
    }

    await invoke_agent(SUserInputData(session_id="s1", user_input="continue"))

    mock_agent.ainvoke.assert_called_once()
    args, _ = mock_agent.ainvoke.call_args
    assert isinstance(args[0], Command)
    assert args[0].resume == "continue"


@pytest.mark.asyncio
async def test_agent_memory_pipeline(mock_get_agent):
    _, mock_agent, mock_cp = mock_get_agent
    mock_cp.get_tuple.side_effect = [
        None,
        {"some": "state"},
    ]  # checkpointer don't exists in first run

    mock_agent.ainvoke.return_value = {
        "messages": [AIMessage([{"text": "ok"}])],
    }

    await invoke_agent(SUserInputData(session_id="s1", user_input="hello"))
    expected_config = {"configurable": {"thread_id": "s1"}}
    mock_cp.get_tuple.assert_called_once_with(expected_config)

    args, _ = mock_agent.ainvoke.call_args
    state = args[0]
    assert isinstance(state, dict)  # created initial state
    assert state["session_id"] == "s1"

    await invoke_agent(SUserInputData(session_id="s1", user_input="continue"))
    assert mock_cp.get_tuple.call_count == 2
    mock_cp.get_tuple.assert_called_with(expected_config)  # same config used

    args, _ = mock_agent.ainvoke.call_args
    assert isinstance(args[0], Command)  # resumed state
    assert args[0].resume == "continue"


@pytest.mark.asyncio
async def test_returns_xml_from_interrupt(mock_get_agent):
    _, mock_agent, _ = mock_get_agent

    mock_agent.ainvoke.return_value = {
        "__interrupt__": [
            Interrupt(value={"xml_result": "<bpmn />"}, id="x"),
        ],
    }

    result = await invoke_agent(
        SUserInputData(session_id="s1", user_input="generate xml")
    )

    assert result == "<bpmn />"


@pytest.mark.asyncio
async def test_full_pipeline_calls_both_nodes(mocker):
    mocker.patch(f"{SCRIPT}.get_langgraph_llm_client")
    mocker.patch(f"{SCRIPT}.LLMConfigManager")

    mock_process = mocker.patch(f"{SCRIPT}.generate_process")
    mock_xml = mocker.patch(f"{SCRIPT}.generate_xml")

    mock_process.return_value = {
        "messages": [AIMessage([{"text": "imagine done"}])],
    }
    mock_xml.side_effect = lambda state, **kw: interrupt({"xml_result": "<bpmn/>"})

    result = await invoke_agent(SUserInputData(session_id="s1", user_input="make bpmn"))

    assert mock_process.called
    assert mock_xml.called
    assert result == "<bpmn/>"
