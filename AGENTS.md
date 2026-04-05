# AGENTS.md - Developer Guide for Vibe BPMN Studio

## Overview

FastAPI web app for creating/editing BPMN diagrams with AI-powered assistance. Python 3.13+, LangGraph for AI agents, lxml for XML generation.

## Build, Lint, and Test Commands

### Development

```bash
uv sync                           # Install dependencies
uvicorn main:app --reload         # Run dev server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Linting and Formatting

```bash
ruff check .                      # Run linter
ruff check . --fix                # Auto-fix linting issues
ruff format --check .            # Check formatting
ruff format .                     # Auto-format
```

### Testing

```bash
pytest -v                         # Run all tests
pytest -v -k "not e2e"           # Unit tests only
pytest -v -k "e2e"               # E2E tests only
pytest -v -k "test_name"         # Run single test by name
pytest --cov=src --cov-report=term-missing  # With coverage
```

### Environment Variables

```bash
ENVIROMENT=dev                    # dev, prod, test
OPENROUTER_API_KEY=...           # AI features (never commit)
OPENROUTER_MODEL_NAME=...
```

## Code Style Guidelines

### Python Version
- **Required**: Python 3.13+
- Use `|` instead of `Optional` for union types

### Imports
- Use absolute imports from `src`:
```python
from src.schemas import SUserInputData
from src.ai_generation.llm_clients import get_llm_client
```
- Order: standard library → third-party → local

### Type Hints
```python
def foo() -> str | None:
    x: dict | None = None

from typing import Literal
mode: Literal["none", "low", "high"] = "none"
```

### Naming Conventions
- **Functions/variables**: snake_case
- **Classes**: PascalCase
- **Constants**: SCREAMING_SNAKE_CASE
- **Private methods**: prefix with `_`

### Docstrings
Google-style docstrings for public functions. Concise one-liners for simple functions.

### Logging
Always use module-level loggers:
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Starting process")
```

### Error Handling
- Use try/except with logging for error cases
- Raise specific exceptions with meaningful messages
- For API routes, use FastAPI's `HTTPException`

### Pydantic Schemas
- Use Pydantic v2 with `BaseModel`
- Define schemas in `src/schemas.py`
- Use `S` prefix for schema names

### FastAPI Routes
- Use `APIRouter` for grouping routes
- Define tags for documentation
- Use async/await for I/O operations

## Testing Conventions

- Place tests in `tests/` mirroring `src/` structure
- Use pytest fixtures and `mocker` (pytest-mock) for mocking
- Mark e2e tests with "e2e" in the name
- Test files: `test_*.py`, functions: `test_*`

## Project Structure

```
src/
├── api_routes.py           # FastAPI endpoints
├── schemas.py              # Pydantic models
├── get_example_diagram.py # Example diagram loader
├── ai_generation/
│   ├── llm_clients/        # LLM client wrappers
│   ├── managers/           # Configuration managers
│   └── bpmn_agent/         # LangGraph agents
│       └── simple/         # Simple agent impl
└── assemblers/
    ├── xml/                # XML generation (lxml)
    └── json/               # JSON generation

tests/
└── ai_generation/
```

## LLM Client Usage

```python
from src.ai_generation.llm_clients import get_llm_client

llm = get_llm_client()
result = llm.generate_response_json_based(
    prompt="...",
    json_schema=schema,
    system_prompt="...",
)
```

## XML Generation

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

## Key Dependencies

- **fastapi**, **uvicorn** - Web framework
- **lxml** - XML generation
- **langgraph** - AI agent orchestration
- **langchain-openai**, **langchain-google-genai** - LLM integrations
