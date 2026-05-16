# AGENTS.md

FastAPI web app for creating/editing BPMN diagrams with AI (LangGraph + OpenRouter/Gemini). Python 3.13+, lxml, bpmn-js.

## Commands

```bash
uv sync                              # Install deps
uvicorn main:app --reload            # Dev server
ruff check . && ruff format --check .  # CI gate (both must pass)
ruff check . --fix && ruff format .  # Auto-fix
pytest -v -k "not e2e"              # Unit tests
pytest -v -k "test_name"            # Single test
pytest --cov=src --cov-report=term-missing
```

Lint first, then format check — CI enforces both. Tests use `pytest-asyncio` + `pytest-mock`.

## Architecture

```
main.py                 # FastAPI entrypoint (mounts /api router, serves static/)
├── src/
│   ├── api_routes.py              # POST /generate, GET /example-bpmn-xml
│   ├── schemas.py                 # Pydantic v2 models (S prefix)
│   ├── task_registry.py           # Prevents concurrent AI runs per session_id
│   ├── get_example_diagram.py     # Reads data/XMLs/base_bpmn_diagram.xml
│   ├── ai_generation/
│   │   ├── bpmn_agent/
│   │   │   ├── agent.py           # LangGraph agent build + invoke
│   │   │   ├── langgraph.py       # LLM client factory (OpenRouter / Gemini)
│   │   │   ├── state.py           # AgentState: messages + session_id
│   │   │   └── nodes/
│   │   │       ├── imagine_procces_node.py  # "imagine" node
│   │   │       ├── generate_xml.py          # "generate" node (interrupts)
│   │   │       └── _extract_system_and_configuration.py
│   │   └── managers/
│   │       ├── llm_config.py      # Loads YAML+Jinja2 prompt configs
│   │       └── json_schema.py     # Loads JSON schemas from data/
│   └── assemblers/
│       ├── xml/                   # BpmnBuilder (programmatic, not used by agent)
│       └── json/
├── data/
│   ├── prompts/                   # business_generation.yaml, XML_generation.yaml
│   ├── bpmn_schemas/              # JSON schemas for LLM tool calling
│   └── XMLs/base_bpmn_diagram.xml # Default example diagram
├── static/                        # Frontend (vanilla JS + bpmn-js)
└── tests/
    ├── test_api_routes.py
    └── ai_generation/
        ├── bpmn_agent/
        │   ├── test_agent.py
        │   ├── test_langgraph.py
        │   └── nodes/
        └── managers/
```

## Key gotchas

- **ENVIROMENT** (not ENVIRONMENT) env var controls `.env` vs `.env.test` loading. `settings.py` validates this.
- **PROVIDER_NAME** must be `openrouter` or `gemini`. Each requires matching `*_API_KEY` + `*_MODEL_NAME` — validated at import time.
- **TaskRegistry** blocks a second AI generation for the same `session_id` while one is running (returns `status=false`). There is no true cancellation.
- **LangGraph agent** is a 2-node loop: `imagine` → `generate` → `imagine`. The `generate` node calls `interrupt()` to yield XML to the user; resuming sends user feedback back into the loop.
- **Prompts** are YAML files in `data/prompts/` rendered through Jinja2. Each file has `temperature` and `system_prompt`. Loaded via `LLMConfigManager.get_call_config("name")`.
- **Frontend** is vanilla JS (no framework). bpmn-js loaded from CDN at runtime.
- **Docker** uses `uv sync --no-dev`, prod only.

## LLM client

```python
from src.ai_generation.bpmn_agent.langgraph import get_langgraph_llm_client

llm: BaseChatModel = get_langgraph_llm_client()  # ChatOpenAI or ChatGoogleGenerativeAI
result = llm.bind(temperature=0.2).invoke(messages)
```

## XML builder (programmatic, not AI)

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

## CI

- `ruff_linter.yml` runs `ruff check . && ruff format --check .` on PRs to main
- `pytest.yml` runs unit tests (`-k "not e2e"`) with coverage on PRs to main
- `docker_hadolint.yml` lints Dockerfile on PRs to main
- `ci-cd-pipeline.yml` builds + pushes Docker image on push to main, then triggers Render deploy hook
