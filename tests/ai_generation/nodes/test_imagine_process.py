from unittest.mock import Mock

from ai_generation.bpmn_agent.simple.nodes.imagine_procces import generate_process

# --- TEST --


def test_generate_procces():
    """Test is generated xml in the state and AI API have been called"""
    client = Mock()
    client.generate_response_text_based.return_value = "Process of the plan>"
    state = {"previous_answer": "Test", "user_input": "Test"}

    result = generate_process(state, client, {})  # config empty due llm_mock
    assert result["previous_answer"] == "Process of the plan>"
    client.generate_response_text_based.assert_called_once()
