from unittest.mock import Mock

from src.ai_generation.bpmn_agent.simple.get_bpmn_node import generate_bpmn

# --- TEST ---


def test_generation():
    """Test is generated xml in the state and AI API have been called"""
    client = Mock()
    client.generate_response_text_based.return_value = "<bpmn>xml</bpmn>"
    state = {"previous_answer": "Test", "user_input": "Test"}

    result = generate_bpmn(state, client, {})  # config empty due llm_mock
    assert result["previous_answer"] == "<bpmn>xml</bpmn>"
    client.generate_response_text_based.assert_called_once()
