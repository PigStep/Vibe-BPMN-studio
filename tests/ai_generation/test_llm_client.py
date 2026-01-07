import pytest
from unittest.mock import Mock, MagicMock
from src.ai_generation.llm_client import LLMClient


# --- FIXTURES ---


@pytest.fixture
def openai_client():
    client = Mock()
    return client


@pytest.fixture
def client(openai_client):
    return LLMClient(openai_client, "test-model")


# --- TESTS ---


def test_generate_text_response_basic(client, openai_client):
    """
    Check basic answer
    Check with which args the API was called.
    """
    response = MagicMock()
    response.choices[0].message.content = "Hello"
    openai_client.chat.completions.create.return_value = response

    result = client.generate_response_text_based(
        prompt="Say hi", system_prompt="Be polite"
    )

    assert result == "Hello"  # Should be a result of chat completion

    assert openai_client.chat.completions.create.call_count == 1

    _, kwargs = openai_client.chat.completions.create.call_args

    assert kwargs == {
        "model": "test-model",
        "messages": [
            {"role": "system", "content": "Be polite"},
            {"role": "user", "content": "Say hi"},
        ],
        "temperature": None,  # we do not use temperature on this call
        "response_format": None,  # none for text generation
        "extra_body": {"reasoning": {"effort": "none"}},  # none by default
    }  # openai api call by default


def test_generate_response_json_structure(client, openai_client):
    """
    Test that answer correctly sending in JSON structure based response_format.
    """
    mock_response = MagicMock()
    mock_response.choices[0].message.content = '{"key": "value"}'
    openai_client.chat.completions.create.return_value = mock_response

    fake_schema = {"type": "object", "properties": {"foo": {"type": "string"}}}

    result = client.generate_response_json_based(
        prompt="Input by this data:",
        json_schema=fake_schema,
        system_prompt="create valid json",
    )

    assert result == '{"key": "value"}'

    call_kwargs = openai_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["response_format"] == {
        "type": "json_schema",
        "json_schema": {
            "name": "response_schema",
            "schema": fake_schema,
        },
    }  # should be "{"key": "value"}" format

    assert openai_client.chat.completions.create.call_count == 1
