from unittest.mock import MagicMock

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import pytest

from src.ai_generation.bpmn_agent.nodes import generate_xml

GEN_XML = "src.ai_generation.bpmn_agent.nodes.generate_xml"


@pytest.fixture
def mock_llm():
    mock_llm = MagicMock()
    mock_llm.bind.return_value = mock_llm
    mock_llm.invoke.return_value = AIMessage(content="<xml />")

    return mock_llm


def test_calls_llm_and_returns_xml(mocker, mock_llm):
    mock_interrupt = mocker.patch(f"{GEN_XML}.interrupt")
    mock_interrupt.return_value = "user feedback"

    state = {
        "messages": [HumanMessage(content="make xml")],
        "session_id": "test",
    }
    config = {"system_prompt": "Generate XML", "temperature": 0.3}

    result = generate_xml(state, mock_llm, config)  # type: ignore

    invoked_messages = mock_llm.invoke.call_args[0][0]
    assert isinstance(invoked_messages[0], SystemMessage)
    assert invoked_messages[0].content == "Generate XML"
    mock_interrupt.assert_called_once_with({"xml_result": "<xml />"})

    assert result["messages"] == [HumanMessage("user feedback")]


def test_passes_xml_content_from_ai_response(mocker, mock_llm):
    mock_llm.invoke.return_value = AIMessage(content="<process />")

    mock_interrupt = mocker.patch(f"{GEN_XML}.interrupt")
    mock_interrupt.return_value = "looks good"

    state = {
        "messages": [HumanMessage(content="make xml")],
        "session_id": "test",
    }
    config = {"system_prompt": "Generate XML", "temperature": 0.3}

    result = generate_xml(state, mock_llm, config)  # type: ignore

    mock_interrupt.assert_called_once_with({"xml_result": "<process />"})

    assert result["messages"] == [HumanMessage("looks good")]


def test_skips_system_prompt_when_not_configured(mocker, mock_llm):
    mock_interrupt = mocker.patch(f"{GEN_XML}.interrupt")
    mock_interrupt.return_value = "ok"

    state = {
        "messages": [HumanMessage(content="make xml")],
        "session_id": "test",
    }
    config = {"temperature": 0.3}

    result = generate_xml(state, mock_llm, config)  # type: ignore

    invoked_messages = mock_llm.invoke.call_args[0][0]
    assert not any(isinstance(m, SystemMessage) for m in invoked_messages)

    assert result["messages"] == [HumanMessage("ok")]
