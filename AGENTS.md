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

## Frontend design patterns (vanilla JS + native CSS)

### Visual Baseline (High-Agency Skill)
- **DESIGN_VARIANCE**: 8 | **MOTION_INTENSITY**: 6 | **VISUAL_DENSITY**: 4
- **Font**: `Geist` (Google Fonts CDN) — Inter is BANNED. Body inherits via `font-family`.
- **Palette**: Neutral Zinc/Slate base (`#f8fafc` body, `#ffffff` panels). Single accent: Slate Blue `#475569` (low saturation, no "AI purple/blue").
- **Shadows**: Diffusion shadows (`0 20px 40px -15px rgba(0,0,0,0.05)`) instead of flat box-shadows.
- **Transitions**: `cubic-bezier(0.16, 1, 0.3, 1)` on all interactive elements.
- **Tactile feedback**: `:active { transform: scale(0.97) }` on all `.btn` elements.
- **Viewport**: Always use `100dvh` (never `100vh`) to prevent iOS Safari layout jumps.

### Micro-interactions (CSS-only, no Framer Motion)
- **Status dot**: Infinite pulse via `@keyframes pulse` on `.canvas-status::before`.
- **Typing indicator**: 3 bouncing dots (`typingBounce` keyframes) instead of a spinner.
- **Fade-in**: `.sidebar-content.active` uses `fadeIn 0.25s` with spring-like cubic-bezier.

### i18n (RU/EN switcher)
- **File**: `static/js/i18n.js` — global `window.I18N` object with `t()`, `switchLang()`, `translatePage()`.
- **Markup**: Use `data-i18n="key"` for text, `data-i18n-placeholder="key"` for placeholders, `data-i18n-title="key"` for titles.
- **Dynamic strings**: In JS, use `I18N.t('key')` (I18N is guaranteed to exist before component scripts run).
- **Storage**: Language choice persisted in `localStorage` key `vibe-bpmn-lang`.

### Responsive
- **Breakpoint**: `max-width: 767px` collapses the grid to single-column (canvas top, sidebar bottom at `max-height: 45dvh`).
- **Toolbar**: Button text labels hidden via `.btn-text` span with `display: none` on mobile; icons remain visible.

### CSS conventions
- **Grid over flex-math**: Use CSS Grid for layout (`.layout-container { grid-template-columns: 1fr var(--sidebar-width) }`). Never use `calc()` with flex percentages.
- **Variables**: All colors, spacing, shadows, and timing are in `:root` CSS custom properties.
- **No h-screen**: Banned. Use `min-h-[100dvh]` or `height: 100dvh`.

### Anti-patterns to avoid
- No emojis in code or UI (use Font Awesome icons).
- No Inter font, no "AI purple/blue" accents, no neon glows, no pure black (`#000000`).
- No 3-column card layouts (use asymmetric grids or split-screen).
- No generic names/filler copy ("Jane Doe", "Elevate", "Seamless", "Next-Gen").
- No custom mouse cursors, no `h-screen`, no `unsplash.com` URLs.

## CI

- `ruff_linter.yml` runs `ruff check . && ruff format --check .` on PRs to main
- `pytest.yml` runs unit tests (`-k "not e2e"`) with coverage on PRs to main
- `docker_hadolint.yml` lints Dockerfile on PRs to main
- `ci-cd-pipeline.yml` builds + pushes Docker image on push to main, then triggers Render deploy hook
