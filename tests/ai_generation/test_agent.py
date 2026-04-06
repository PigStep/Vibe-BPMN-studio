from unittest.mock import MagicMock

from langchain_core.messages import AIMessage, HumanMessage

from src.schemas import SUserInputData
from src.ai_generation.bpmn_agent.agent import invoke_agent

SCRIPT_DIR = "src.ai_generation.bpmn_agent.agent"

# --- TESTS ---


def test_agent_invoke(mocker):
    """
    Invoke_agent transform userdata to dictionary for agent.
    Tets does invoke agent build and call agent
    """
    mock_agent = mocker.patch(SCRIPT_DIR + "._agent")
    mock_agent.invoke.return_value = {
        "messages": [
            HumanMessage("Send me success"),
            AIMessage(
                [
                    # AI message may contain multiple values
                    # Currently logic extracts only text field
                    {"text": "succes"}
                ]
            ),
        ]
    }
    test_user_data = SUserInputData(session_id="test_id", user_input="Send me success")

    result = invoke_agent(test_user_data)

    mock_agent.invoke.assert_called_once_with(
        {
            "messages": [HumanMessage("Send me success")],
        }
    )
    assert result == "succes"  # Result should be the agent returns


def test_agent_full_flow(mocker):
    """Test agent do not fall down during call"""
    mock_llm = mocker.patch(SCRIPT_DIR + ".get_langgraph_llm_client")
    mock_process_node = mocker.patch(SCRIPT_DIR + ".generate_process")
    mock_bpmn_node = mocker.patch(SCRIPT_DIR + ".generate_bpmn")

    mock_llm.invoke.return_value = MagicMock()
    # Do not really call nodes
    mock_process_node.return_value = {
        "messages": [
            HumanMessage("Send me success"),
            AIMessage([{"text": "generate_process called"}]),
        ]
    }
    mock_bpmn_node.return_value = {
        "messages": [
            HumanMessage("Send me success"),
            AIMessage([{"text": "generate_bpmn called"}]),
        ]
    }

    invoke_agent(SUserInputData(session_id="test_id", user_input="Test flow"))

    assert mock_process_node.called
    assert mock_process_node.called
