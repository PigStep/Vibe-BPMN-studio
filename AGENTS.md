# AGENTS.md - Developer Guide for Vibe BPMN Studio

## Overview
This is a FastAPI-based web application for creating and editing BPMN diagrams with AI-powered assistance. The backend uses Python 3.13+, LangGraph for AI agents, and lxml for XML generation.

## Build, Lint, and Test Commands

### Development
```bash
# Install dependencies
uv sync

# Run development server
uvicorn main:app --reload

# Run with custom host/port
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Linting and Formatting
```bash
# Run ruff linter
ruff check .

# Check code formatting
ruff format --check .

# Fix linting issues
ruff check . --fix

# Fix formatting
ruff format .
```

### Testing
```bash
# Run all tests
pytest -v

# Run unit tests only (excludes e2e)
pytest -v -k "not e2e"

# Run e2e tests only
pytest -v -k "e2e"

# Run a specific test
pytest -v -k "test_agent_invoke"

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run tests matching pattern
pytest -v -k "test_llm"
```

### Environment Variables
```bash
# Set environment (dev, prod, test)
ENVIROMENT=dev

# Required for AI features
OPENROUTER_API_KEY=your_api_key
OPENROUTER_MODEL_NAME=anthropic/claude-3-haiku
```

## Code Style Guidelines

### Python Version
- **Required**: Python 3.13+
- Use modern Python syntax (type unions with `|` instead of `Optional`)

### Imports
- Use absolute imports from `src`:
  ```python
  from src.schemas import SUserInputData
  from src.ai_generation.llm_client import get_llm_client
  ```
- Third-party imports first, then local imports
- Standard library imports (logging, typing, etc.) before third-party

### Type Hints
- Use Python 3.13+ union syntax:
  ```python
  # Good
  def foo() -> str | None:
      x: dict | None = None
  
  # Avoid
  def foo() -> Optional[str]:
      x: Optional[dict] = None
  ```
- Use `Literal` for enum-like string constants:
  ```python
  from typing import Literal
  reasoning_mode: Literal["none", "minimal", "low", "medium", "high"] = "none"
  ```

### Naming Conventions
- **Functions/variables**: snake_case
- **Classes**: PascalCase
- **Constants**: SCREAMING_SNAKE_CASE
- **Private methods**: prefix with underscore

### Docstrings
Use Google-style docstrings for all public functions and methods:

```python
def generate_response(
    prompt: str,
    system_prompt: str,
    temperature: float = 0.7,
) -> str | None:
    """
    Generate a response from the LLM using the provided prompt.

    Parameters
    ----------
    prompt : str
        The user prompt to send to the model.
    system_prompt : str
        The system prompt to send as the initial message.
    temperature : float, optional
        Sampling temperature. Default is 0.7.

    Returns
    -------
    str | None
        Content of the first message, or None if no content.
    """
```

### Logging
Always use module-level loggers:

```python
import logging

logger = logging.getLogger(__name__)

# Then use appropriate levels
logger.info("Starting process")
logger.warning("Something unexpected")
logger.error(f"Failed: {e}")
```

### Error Handling
- Use try/except with logging for error cases
- Raise specific exceptions with meaningful messages
- For API routes, use FastAPI's `HTTPException`:

```python
from fastapi import HTTPException

try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Validation failed: {e}")
    raise HTTPException(status_code=400, detail=str(e))
```

### Pydantic Schemas
- Use Pydantic v2 with `BaseModel`
- Define response schemas in `src/schemas.py`
- Use descriptive names with `S` prefix for schemas:

```python
from pydantic import BaseModel

class SUserInputData(BaseModel):
    user_input: str

class SAgentOutput(BaseModel):
    status: bool = True
    output: str
```

### FastAPI Routes
- Use `APIRouter` for grouping routes
- Define tags for documentation
- Use async/await for I/O operations

```python
from fastapi import APIRouter

router = APIRouter(tags=["API"])

@router.get("/generate")
async def generate_bpmn(user_input: str) -> SAgentOutput:
    ...
```

### Testing Conventions
- Place tests in `tests/` directory mirroring `src/` structure
- Use pytest fixtures for test setup
- Use `mocker` (pytest-mock) for mocking
- Mark e2e tests with "e2e" in the name:

```python
def test_agent_invoke(mocker):
    """Test description"""
    mock_agent = mocker.patch("path.to.module")
    mock_agent.invoke.return_value = {"result": "success"}
    
    # assertions
    assert result == expected
```

- Test files should be named `test_*.py`
- Test functions should be named `test_*`

### Project Structure
```
src/
├── api_routes.py          # FastAPI endpoints
├── schemas.py             # Pydantic models
├── get_example_diagram.py # Example diagram loader
├── ai_generation/
│   ├── llm_client.py      # OpenAI LLM wrapper
│   ├── managers/          # Configuration managers
│   └── bpmn_agent/       # LangGraph agents
│       ├── agent.py       # Agent definitions
│       ├── state.py       # Agent state
│       └── simple/         # Simple agent impl
└── assemblers/
    ├── xml/               # XML generation
    └── json/              # JSON generation

tests/
└── ai_generation/
    ├── test_agent.py
    ├── test_llm_client.py
    └── nodes/
```

### LLM Client Usage
When calling the LLM client, use the singleton pattern:

```python
from src.ai_generation.llm_client import get_llm_client

llm = get_llm_client()
result = llm.generate_response_json_based(
    prompt="...",
    json_schema=schema,
    system_prompt="...",
)
```

### XML Generation
Use the builder pattern with lxml:

```python
from src.assemblers.xml.bpmn import BpmnBuilder

xml = (
    BpmnBuilder()
    .create_definitions("def_1")
    .start_process("process_1", "My Process")
    .add_node("startEvent", "start_1", "Start")
    .add_node("userTask", "task_1", "Do Something")
    .init_diagram("process_1")
    .build()
)
```
