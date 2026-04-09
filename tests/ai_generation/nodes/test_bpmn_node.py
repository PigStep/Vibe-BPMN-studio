from unittest.mock import MagicMock

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from ai_generation.bpmn_agent.nodes.generate_xml import generate_xml

# --- TEST ---


def test_generation():
    """Test is generated xml in the state and AI API have been called"""
    client = MagicMock()
    bound_client = MagicMock()
    client.bind.return_value = bound_client
    bound_client.invoke.return_value = AIMessage(  # invoke() called on bound_client
        content=[{"text": "LLM RETURNED <XML>"}]
    )

    configuration = {"system_prompt": "dummy_system", "temperature": 0.2}

    state = {"messages": [HumanMessage(content="dummy_input")]}

    result = generate_xml(state, client, configuration)

    assert (
        result["messages"][-1].content[0]["text"] == "LLM RETURNED <XML>"
    )  # Result of LLm invoking
    bound_client.invoke.assert_called_once_with(
        [
            SystemMessage("dummy_system"),
            HumanMessage("dummy_input"),
        ]
    )  # Sustem prompt is inserting
