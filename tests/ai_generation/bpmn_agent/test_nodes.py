import pytest
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.types import interrupt

from src.ai_generation.bpmn_agent.nodes.imagine_procces_node import generate_process
from src.ai_generation.bpmn_agent.nodes.generate_xml import generate_xml

GEN_PROC = "src.ai_generation.bpmn_agent.nodes.imagine_procces_node"
GEN_XML = "src.ai_generation.bpmn_agent.nodes.generate_xml"

# FIXME: update tests


class TestGenerateProcess:
    def test_adds_system_prompt_when_configured(self, mocker):
        mock_llm = mocker.MagicMock()
        mock_llm.bind.return_value = mock_llm
        mock_llm.invoke.return_value = AIMessage(content="plan")

        state = {
            "messages": [HumanMessage(content="do something")],
            "session_id": "test",
        }
        config = {"system_prompt": "You are a helpful assistant", "temperature": 0.5}

        result = generate_process(state, mock_llm, config)

        invoked_messages = mock_llm.invoke.call_args[0][0]
        assert any(isinstance(m, SystemMessage) for m in invoked_messages)
        assert any(
            isinstance(m, HumanMessage) and m.content == "do something"
            for m in invoked_messages
        )
        assert result == {"messages": [AIMessage(content="plan")]}

    def test_skips_system_prompt_when_not_configured(self, mocker):
        mock_llm = mocker.MagicMock()
        mock_llm.bind.return_value = mock_llm
        mock_llm.invoke.return_value = AIMessage(content="plan")

        state = {
            "messages": [HumanMessage(content="do something")],
            "session_id": "test",
        }
        config = {"temperature": 0.5}

        generate_process(state, mock_llm, config)

        invoked_messages = mock_llm.invoke.call_args[0][0]
        assert not any(isinstance(m, SystemMessage) for m in invoked_messages)

    def test_returns_llm_response_in_messages(self, mocker):
        mock_llm = mocker.MagicMock()
        mock_llm.bind.return_value = mock_llm
        expected_response = AIMessage(content="result")
        mock_llm.invoke.return_value = expected_response

        state = {
            "messages": [HumanMessage(content="hello")],
            "session_id": "test",
        }
        config = {}

        result = generate_process(state, mock_llm, config)

        assert result == {"messages": [expected_response]}


class TestGenerateXml:
    def test_calls_llm_and_returns_human_message(self, mocker):
        mock_llm = mocker.MagicMock()
        mock_llm.bind.return_value = mock_llm
        mock_llm.invoke.return_value = mocker.MagicMock(text="<xml />")

        mocker.patch(f"{GEN_XML}.interrupt", return_value="user feedback")

        state = {
            "messages": [HumanMessage(content="make xml")],
            "session_id": "test",
        }
        config = {"system_prompt": "Generate XML", "temperature": 0.3}

        result = generate_xml(state, mock_llm, config)

        mock_llm.invoke.assert_called_once()
        invoked_messages = mock_llm.invoke.call_args[0][0]
        assert any(isinstance(m, SystemMessage) for m in invoked_messages)
        assert result == {"messages": [HumanMessage(content="user feedback")]}
