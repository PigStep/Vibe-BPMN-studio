from unittest.mock import MagicMock

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.ai_generation.bpmn_agent.nodes.imagine_procces_node import generate_process

# --- TEST --


def test_generate_procces():
    """Test is node invoking llm to generate process plan"""
    client = MagicMock()
    bound_client = MagicMock()
    client.bind.return_value = bound_client
    bound_client.invoke.return_value = AIMessage(  # invoke() called on bound_client
        content=[{"text": "process text description"}]
    )

    configuration = {"system_prompt": "dummy_system", "temperature": 0.2}

    state = {"messages": [HumanMessage(content="dummy_input")]}

    result = generate_process(state, client, configuration)

    assert (
        result["messages"][-1].content[0]["text"] == "process text description"
    )  # Result of LLm invoking
    bound_client.invoke.assert_called_once_with(
        [
            SystemMessage("dummy_system"),
            HumanMessage("dummy_input"),
        ]
    )  # Sustem prompt is inserting
