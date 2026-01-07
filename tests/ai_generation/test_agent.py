from unittest.mock import Mock

from src.schemas import SUserInputData
from src.ai_generation.bpmn_agent.simple.agent import invoke_agent

SCRIPT_DIR = "src.ai_generation.bpmn_agent.simple.agent"

# --- TESTS ---


def test_agent_invoke(mocker):
    """
    Invoke_agent transform userdata to dictionary for agent.
    Tets does invoke agent build and call agent
    """
    mock_agent = mocker.patch(SCRIPT_DIR + "._agent")
    mock_agent.invoke.return_value = {"result": "success"}
    test_user_data = SUserInputData(user_input="Send me success")

    result = invoke_agent(test_user_data)

    mock_agent.invoke.assert_called_once_with(
        {
            "user_input": "Send me success",
            "previous_stage": "",  # under the logic. Basic config for first call
        }
    )
    assert result == {"result": "success"}  # Result should be the agent returns


def test_agent_full_flow(mocker):
    """Test agent do not fall down during call"""
    mock_llm = mocker.patch(SCRIPT_DIR + ".get_llm_client")
    mock_process_node = mocker.patch(SCRIPT_DIR + ".generate_process")
    mock_bpmn_node = mocker.patch(SCRIPT_DIR + ".generate_bpmn")

    mock_llm.return_value = Mock()
    mock_process_node.return_value = {"result": "called"}
    mock_bpmn_node.return_value = {"result": "called"}

    invoke_agent(SUserInputData(user_input="Test flow"))

    assert mock_process_node.called
    assert mock_process_node.called
