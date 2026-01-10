from unittest.mock import Mock
import pytest

from src.schemas import SUserInputData
from src.ai_generation.bpmn_agent.simple.agent import (
    invoke_agent,
    _reset_agent,
    get_compiled_agent,
)

SCRIPT_DIR = "src.ai_generation.bpmn_agent.simple.agent"

# --- FIXTURES ---


@pytest.fixture(autouse=True)
def cleanup_agent_singleton():
    """
    Reset agent while tests
    """
    # Action before test
    _reset_agent()
    yield
    # Action after test
    _reset_agent()


@pytest.fixture
def mock_agent_dependencies(mocker):
    """
    Mocks the agent's external dependencies and returns mock objects,
    allowing tests to verify their calls or modify return values.
    """
    mock_llm = mocker.patch(SCRIPT_DIR + ".get_llm_client")
    mock_process = mocker.patch(SCRIPT_DIR + ".generate_process")
    mock_bpmn = mocker.patch(SCRIPT_DIR + ".generate_bpmn")

    mock_llm.return_value = Mock()
    # Возвращаем словари, так как ноды в LangGraph обычно обновляют state словарем
    mock_process.return_value = {"previous_stage": "process_done"}
    mock_bpmn.return_value = {"bpmn_xml": "<xml/>"}

    return {"llm": mock_llm, "process": mock_process, "bpmn": mock_bpmn}


# --- TESTS ---


def test_agent_invoke(mocker):
    """
    Invoke_agent transform userdata to dictionary for agent.
    Tets does invoke agent build and call agent
    """
    mock_agent = mocker.patch(SCRIPT_DIR + "._agent")
    mock_agent.invoke.return_value = {"result": "success"}
    test_user_data = SUserInputData(user_input="Send me success")

    result = invoke_agent(test_user_data, "thread_test_id")

    mock_agent.invoke.assert_called_once_with(
        {
            "user_input": "Send me success",
            "previous_stage": "",  # under the logic. Basic config for first call
        },
        config={"configurable": {"thread_id": "thread_test_id"}},
    )
    assert result == {"result": "success"}  # Result should be the agent returns


def test_agent_full_flow(mock_agent_dependencies):
    """Test agent do not fall down during call"""
    invoke_agent(SUserInputData(user_input="Test flow"), "thread_test_id")

    assert mock_agent_dependencies["process"].called
    assert mock_agent_dependencies["bpmn"].called


def test_memory(mock_agent_dependencies):
    """Test agent remember consevation by id's"""
    # Arrange
    session_id = "session_memory_test"

    # Act
    first_input = SUserInputData(user_input="First message")
    invoke_agent(first_input, session_id)

    # Assert
    agent = get_compiled_agent()
    state = agent.get_state({"configurable": {"thread_id": session_id}})

    assert state.values is not None  # agent should know state
    assert state.values["user_input"] == "First message"
