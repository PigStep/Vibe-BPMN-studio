from unittest.mock import MagicMock, Mock
from unittest.mock import patch
import pytest

from src.schemas import SUserInputData
from src.ai_generation.bpmn_agent.agent import invoke_agent

SCRIPT_DIR = "src.ai_generation.bpmn_agent.agent"

# --- TESTS ---


@pytest.fixture
def mock_dependencies():
    with patch(
        SCRIPT_DIR + ".get_dependencies",
    ) as mock_func:
        mock_config = MagicMock()
        mock_non_langgraph_llm = MagicMock()
        mock_llm_with_tools = MagicMock()
        mock_func.return_value = (
            mock_config,
            mock_non_langgraph_llm,
            mock_llm_with_tools,
        )
        yield mock_func, mock_config, mock_non_langgraph_llm, mock_llm_with_tools


def test_invoking_agent(mock_dependencies):
    "Test agent invoking and dependecies injected"
    mock_func, mock_config, mock_llm, mock_llm_with_tools = mock_dependencies

    test_user_data = SUserInputData(session_id="test", user_input="test")
    mock_llm_with_tools.invoke.result_value = MagicMock()
    invoke_agent(test_user_data)

    mock_func.assert_called_once()  # Check are dependencies inserted
    mock_llm_with_tools.invoke.assert_called_once()  # Check agent was invoked


def test_agent_tool_invoking(mock_dependencies):
    """Test agent invoking get dependecies -> agent invoke -> tool ivoking -> return xml"""
    mock_func, mock_config, mock_llm, mock_llm_with_tools = mock_dependencies

    test_user_data = SUserInputData(session_id="test", user_input="test")

    with patch(SCRIPT_DIR + ".generate_draft") as mock_generate_draft:
        # response that llm return for tool call
        response = MagicMock()
        response.tool_calls = [
            {
                "args": "function_args",
                "configurable": {
                    "llm": mock_llm,
                    "config_manager": mock_config,
                    "session_id": "test",
                },
            }
        ]
        mock_generate_draft.invoke.return_value = MagicMock()
        mock_llm_with_tools.invoke.return_value = response
        invoke_agent(test_user_data)

        mock_generate_draft.invoke.assert_called_once_with(
            "function_args",
            config={
                "configurable": {
                    "llm": mock_llm,
                    "config_manager": mock_config,
                    "session_id": "test",
                }
            },
        )
