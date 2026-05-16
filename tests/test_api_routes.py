from unittest.mock import ANY, AsyncMock, patch

import pytest

from src.schemas import SAgentOutput, SUserInputData
from src.api_routes import generate_bpmn

SCRIPT = "src.api_routes"


@pytest.fixture
def mock_task_registry():
    with patch(f"{SCRIPT}.TaskRegistry") as mock:
        yield mock


@pytest.fixture
def mock_invocation():
    with patch(f"{SCRIPT}.invoke_agent", new_callable=AsyncMock) as mock:
        mock.return_value = "xml"
        yield mock


@pytest.mark.asyncio
async def test_bpmn_generation_happy(mock_task_registry, mock_invocation):
    user_request_test_data = SUserInputData(
        session_id="test_id", user_input="test_input"
    )

    mock_task_registry.should_start_new_task.return_value = True
    mock_task_registry.register_task.return_value = "have registered some data"

    result = await generate_bpmn(user_request_test_data)
    assert result == SAgentOutput(status=True, output="xml")

    mock_invocation.assert_awaited_once_with(user_request_test_data)
    mock_task_registry.should_start_new_task.assert_called_once_with(
        user_request_test_data.session_id
    )
    mock_task_registry.register_task.assert_called_once_with(
        user_request_test_data.session_id, ANY
    )


@pytest.mark.asyncio
async def test_bpmn_generation_second_procces_run(mock_task_registry):
    user_request_test_data = SUserInputData(
        session_id="test_id", user_input="test_input"
    )
    mock_task_registry.should_start_new_task.return_value = False

    result = await generate_bpmn(user_request_test_data)
    assert result == SAgentOutput(status=False, output="")
