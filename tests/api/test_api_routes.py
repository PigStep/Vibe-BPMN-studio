"""
Tests for API routes (api_routes.py)
"""

import logging
from unittest.mock import patch, Mock, AsyncMock
import pytest
from httpx import AsyncClient, ASGITransport

from src.api_routes import router
from src.schemas import SUserInputData, SExampleBPMN, SAgentOutput


# --- FIXTURES ---


@pytest.fixture
def mock_invoke_agent():
    """Mock invoke_agent function"""
    with patch("src.api_routes.invoke_agent") as mock:
        mock.return_value = {"previous_answer": "<bpmn:definitions/>"}
        yield mock


@pytest.fixture
def mock_get_example_diagram():
    """Mock get_example_diagramm function"""
    with patch("src.api_routes.get_example_diagramm") as mock:
        mock.return_value = "<bpmn:definitions/>"
        yield mock


@pytest.fixture
def mock_uuid4():
    """Mock uuid4 for predictable session IDs"""
    mock_uuid = Mock()
    mock_uuid.__str__ = Mock(return_value="test-uuid-1234")
    with patch("src.api_routes.uuid4", return_value=mock_uuid):
        yield mock_uuid


@pytest.fixture
def app_client():
    """Create test client for the router"""
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(router)
    return app


# --- TESTS: GET /generate ---


class TestGenerateBPMN:
    """Tests for the generate BPMN endpoint"""

    @pytest.mark.asyncio
    async def test_generate_bpmn_success(self, app_client, mock_invoke_agent):
        """
        Test successful BPMN generation with session ID header
        """
        transport = ASGITransport(app=app_client)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/generate",
                json={"user_input": "Создай процесс заказа"},
                headers={
                    "X-Session-ID": "test-session-123",
                },
            )

        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        assert data["output"] == "<bpmn:definitions/>"

        mock_invoke_agent.assert_called_once()
        call_args = mock_invoke_agent.call_args
        assert call_args[0][0] == SUserInputData(user_input="Создай процесс заказа")
        assert call_args[0][1] == "test-session-123"

    @pytest.mark.asyncio
    async def test_generate_bpmn_without_session_id(
        self, app_client, mock_invoke_agent, mock_uuid4
    ):
        """
        Test BPMN generation without X-Session-ID header generates fallback ID
        """
        transport = ASGITransport(app=app_client)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/generate",
                json={"user_input": "Test input"},
            )

        assert response.status_code == 200
        mock_invoke_agent.assert_called_once()
        # Verify fallback session ID was used
        call_args = mock_invoke_agent.call_args
        assert call_args[0][1] == "test-uuid-1234"

    @pytest.mark.asyncio
    async def test_generate_bpmn_agent_exception(self, app_client, mock_invoke_agent):
        """
        Test that agent exceptions are handled gracefully
        """
        mock_invoke_agent.side_effect = Exception("AI service unavailable")

        transport = ASGITransport(app=app_client)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/generate",
                json={"user_input": "Test input"},
                headers={
                    "X-Session-ID": "test-session",
                },
            )

        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        assert "tech problem" in data["output"].lower()

    @pytest.mark.asyncio
    async def test_generate_bpmn_empty_user_input(self, app_client, mock_invoke_agent):
        """
        Test BPMN generation with empty user input
        """
        mock_invoke_agent.return_value = {"previous_answer": ""}

        transport = ASGITransport(app=app_client)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/generate",
                json={"user_input": ""},
                headers={
                    "X-Session-ID": "test-session",
                },
            )

        assert response.status_code == 200
        mock_invoke_agent.assert_called_once()


# --- TESTS: GET /example-bpmn-xml ---


class TestGetExampleBPMNXML:
    """Tests for the example BPMN XML endpoint"""

    @pytest.mark.asyncio
    async def test_get_example_bpmn_xml_success(
        self, app_client, mock_get_example_diagram
    ):
        """
        Test successful retrieval of example BPMN XML
        """
        transport = ASGITransport(app=app_client)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/example-bpmn-xml")

        assert response.status_code == 200
        data = response.json()
        assert "xml" in data
        assert data["xml"] == "<bpmn:definitions/>"
        mock_get_example_diagram.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_example_bpmn_xml_file_not_found(self, app_client):
        """
        Test handling when example file is not found
        """
        with patch("src.api_routes.get_example_diagramm") as mock:
            mock.side_effect = FileNotFoundError("File not found")

            transport = ASGITransport(app=app_client)
            async with AsyncClient(
                transport=transport, base_url="http://test"
            ) as client:
                response = await client.post("/example-bpmn-xml")

            assert response.status_code == 500
            data = response.json()
            assert "detail" in data

    @pytest.mark.asyncio
    async def test_get_example_bpmn_xml_generic_exception(self, app_client):
        """
        Test handling of generic exceptions
        """
        with patch("src.api_routes.get_example_diagramm") as mock:
            mock.side_effect = Exception("Unexpected error")

            transport = ASGITransport(app=app_client)
            async with AsyncClient(
                transport=transport, base_url="http://test"
            ) as client:
                response = await client.post("/example-bpmn-xml")

            assert response.status_code == 500
            data = response.json()
            assert "detail" in data


# --- TESTS: Schema Validation ---


class TestSchemaValidation:
    """Tests for schema validation"""

    def test_s_user_input_data_creation(self):
        """
        Test SUserInputData schema creation
        """
        data = SUserInputData(user_input="Test input")
        assert data.user_input == "Test input"

    def test_s_agent_output_defaults(self):
        """
        Test SAgentOutput schema has correct defaults
        """
        output = SAgentOutput(output="<xml/>")
        assert output.status is True
        assert output.output == "<xml/>"

    def test_s_example_bpmn_schema(self):
        """
        Test SExampleBPMN schema
        """
        example = SExampleBPMN(xml="<bpmn:definitions/>")
        assert example.status is True
        assert example.xml == "<bpmn:definitions/>"


# --- TESTS: Logging (mocked) ---


class TestLogging:
    """Tests for logging behavior"""

    @pytest.mark.asyncio
    async def test_generate_logs_session_id(
        self, app_client, mock_invoke_agent, caplog
    ):
        """
        Test that generate endpoint logs the session ID
        """
        with caplog.at_level(logging.INFO):
            transport = ASGITransport(app=app_client)
            async with AsyncClient(
                transport=transport, base_url="http://test"
            ) as client:
                await client.post(
                    "/generate",
                    json={"user_input": "Test"},
                    headers={
                        "X-Session-ID": "my-session",
                    },
                )

        assert any("my-session" in record.message for record in caplog.records)

    @pytest.mark.asyncio
    async def test_example_logs_request(
        self, app_client, mock_get_example_diagram, caplog
    ):
        """
        Test that example endpoint logs the request
        """
        with caplog.at_level(logging.INFO):
            transport = ASGITransport(app=app_client)
            async with AsyncClient(
                transport=transport, base_url="http://test"
            ) as client:
                await client.post("/example-bpmn-xml")

        assert any("base BPMN XML" in record.message for record in caplog.records)
