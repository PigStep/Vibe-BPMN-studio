import pytest
from unittest.mock import MagicMock
from pydantic import BaseModel
from src.ai_generation.llm_clients.gemini import GeminiClient


@pytest.fixture
def gemini_client(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL_NAME", "test-model")
    mock_client = MagicMock()
    client = GeminiClient()
    client.client = mock_client
    return client


def test_generate_text_response_basic(gemini_client):
    response = MagicMock()
    response.text = "Hello"
    gemini_client.client.models.generate_content.return_value = response

    result = gemini_client.generate_response_text_based(
        prompt="Say hi", system_prompt="Be polite"
    )

    assert result == "Hello"

    assert gemini_client.client.models.generate_content.call_count == 1

    _, kwargs = gemini_client.client.models.generate_content.call_args

    assert kwargs["contents"] == "Say hi"
    assert kwargs["config"].system_instruction == "Be polite"


def test_generate_response_json_structure(gemini_client):
    mock_response = MagicMock()
    mock_response.text = '{"key": "value"}'
    gemini_client.client.models.generate_content.return_value = mock_response

    fake_schema = {"type": "object", "properties": {"foo": {"type": "string"}}}

    result = gemini_client.generate_response_json_based(
        prompt="Input by this data:",
        json_schema=fake_schema,
        system_prompt="create valid json",
    )

    assert result == '{"key": "value"}'

    _, kwargs = gemini_client.client.models.generate_content.call_args
    config = kwargs["config"]

    assert config.response_mime_type == "application/json"
    assert config.response_schema == fake_schema
    assert config.system_instruction == "create valid json"

    assert gemini_client.client.models.generate_content.call_count == 1


def test_generate_response_json_structure_from_basemodel(gemini_client):
    mock_response = MagicMock()
    mock_response.text = '{"key": "value"}'
    gemini_client.client.models.generate_content.return_value = mock_response

    class FakeModel(BaseModel):
        foo: str

    result = gemini_client.generate_response_json_based(
        prompt="Input by this data:",
        json_schema=FakeModel,
        system_prompt="create valid json",
    )

    assert result == '{"key": "value"}'

    _, kwargs = gemini_client.client.models.generate_content.call_args
    config = kwargs["config"]

    assert config.response_mime_type == "application/json"
    assert config.response_schema == FakeModel.model_json_schema()
    assert config.system_instruction == "create valid json"

    assert gemini_client.client.models.generate_content.call_count == 1
