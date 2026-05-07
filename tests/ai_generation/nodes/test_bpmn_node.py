from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from requests import session

from src.ai_generation.bpmn_agent.nodes.generate_xml import generate_xml

# --- TEST ---


@patch("src.ai_generation.bpmn_agent.nodes.generate_xml.interrupt")
def test_generation(mock_interrupt):
    """Test is generated xml in the state and AI API have been called"""
    client = MagicMock()
    bound_client = MagicMock()
    mock_interrupt.return_value = (
        "Simple user feedback"  # Need for passing interrupt node
    )

    client.bind.return_value = bound_client
    bound_client.invoke.return_value = AIMessage(  # invoke() called on bound_client
        content=[{"text": "LLM RETURNED <XML>"}]
    )

    configuration = {"system_prompt": "dummy_system", "temperature": 0.2}

    state = {"messages": [HumanMessage(content="dummy_input")], "session_id": "test_id"}

    generate_xml(state, client, configuration)  # type: ignore

    bound_client.invoke.assert_called_once_with(
        [
            SystemMessage("dummy_system"),
            HumanMessage("dummy_input"),
        ]
    )  # Sustem prompt is inserting
