# Vibe BPMN Studio

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue?style=for-the-badge&logo=github)](https://github.com/PigStep/Easy-XML-to-BPMN-creator/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker)](https://hub.docker.com/repository/docker/pigstep/vibe-bpmn/general)
[![Python 3.13](https://img.shields.io/badge/Python-3.13+-green?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![BPMN-JS API](https://img.shields.io/badge/BPMN-JS-yellow?style=for-the-badge&logo=bpmn-js)](https://bpmn.io/toolkit/bpmn-js/walkthrough/)

A modern web application for creating, viewing, and editing BPMN diagrams (Business Process Model and Notation) with AI-powered assistant.

## 📋 Description

Vibe BPMN Studio offers a user‑friendly web interface for working with BPMN diagrams. The application allows users to create new diagrams, edit existing ones, import from files or text, and export results in various formats.

## ✨ Features

- 🎨 **Diagram Creation**: Intuitive editor with a palette of elements
- 🤖 **AI Assistant**: Chat-based BPMN generation and editing help
- 📖 **Diagram Viewing**: Quick preview of BPMN diagrams with zoom capabilities
- 📁 **Data Import**: Upload diagrams from files (.bpmn, .xml) or load examples
- 💾 **Export**: Save diagrams in SVG and BPMN formats
- 🔄 **Modes**: Switch between view and edit modes
- 🖱️ **Navigation**: Zoom, fit‑to‑screen, and pan functionality
- 📱 **Responsive Design**: Adaptive interface for all devices
- 🎭 **Modern UI**: Clean, professional interface with dark theme code editor

## 🛠️ Technologies

- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **BPMN Library**: bpmn-js v14.0.0
- **Styling**: Modern CSS with Custom Properties
- **Package Manager**: UV (modern Python package manager)
- **CI/CD**: GitHub Actions with Docker integration
- **Code Quality**: ruff linter, Hadolint for Docker files
- **AI**: LangGraph + OpenRouter free tier models

> **🚀 CI/CD Integration:** This project features fully automated CI/CD pipelines with GitHub Actions, including Docker image building, automated testing, code linting (ruff), and Hadolint for Docker files. All changes are automatically tested and deployed!

## 📦 Installation and Setup

### Prerequisites

- Python 3.13 or higher
- UV package manager (recommended) or pip

### Installation Steps

#### Cloning the Repository

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd vibe-bpmn-studio
   ```

2. **Install dependencies with UV**:

   ```bash
   uv sync
   ```

   Or with pip:

   ```bash
   pip install -e .
   ```

3. **Start the server**:

   With uvicorn directly:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Open the application**:
   Navigate to `http://localhost:8000` in your browser.

#### 🐳 Docker (Recommended + Fast way)

Alternatively, you can run the application using Docker:

1. **Pull the Docker image**:

   ```bash
   docker pull pigstep/vibe-bpmn:latest
   ```

2. **Run the container**:

   ```bash
   docker run -d -p 8000:8000 --name vibe-bpmn-studio pigstep/vibe-bpmn:latest
   ```

3. **Access the application**:
   Open `http://localhost:8000` in your browser.

## 🚀 Usage

### Core Functions

#### 1. Working with AI Assistant

- Navigate to **AI Ассистент** tab in the sidebar
- Type your request in natural language (e.g., "Add task 'Review Document'")
- AI will help generate and modify BPMN diagrams
- Example: "Create a process chain of Touristic company"

AI generation powered by LangGraph and Open router free tier model for intelligent BPMN creation.

#### 2. Diagram Upload

**From File:**

- Click **Открыть** button in the toolbar
- Select a .bpmn or .xml file
- Diagram will load automatically

**From XML Editor:**

- Navigate to **XML** tab in the sidebar
- Paste BPMN XML into the code editor
- Click **Применить** to load the diagram

#### 3. Editing

- Use the toolbar buttons for zoom controls
- The interface supports both view and edit modes
- Changes are reflected in real-time

#### 4. Export

- **Скачать .bpmn**: Save as BPMN format for further editing
- **Скачать .svg**: Download as vector image for presentations

### Example BPMN

The application loads with a sample diagram that includes:

- Start event
- Two tasks
- End event
- Sequential flows

## 📁 Project Structure

```bash
vibe-bpmn-studio/
├── src/                        # Python source code
│   ├── api_routes.py           # FastAPI routes
│   ├── get_example_diagram.py  # Example diagram loader
│   ├── schemas.py              # Pydantic schemas
│   ├── ai_generation/          # AI agent (LangGraph)
│   │   ├── llm_client.py       # OpenAI LLM client
│   │   ├── promts.py           # System prompts
│   │   └── bpmn_agent/         # BPMN generation agent
│   │       └── simple/         # Simple agent implementation
│   │           ├── agent.py    # Main agent logic
│   │           ├── state.py    # Agent state
│   │           └── get_bpmn_node.py
│   └── assemblers/             # XML/JSON generators
│       ├── xml/                # XML assembly
│       │   ├── base_xml.py     # Base XML builder
│       │   ├── bpmn.py         # BPMN XML assembler
│       │   └── director.py     # XML director
│       └── json/               # JSON assembly
│           ├── base.py         # Base JSON assembler
│           └── bpmn.py         # BPMN JSON assembler
├── static/                     # Frontend assets
│   ├── index.html              # Main application interface
│   ├── css/
│   │   └── style.css           # Modern styling
│   └── js/                     # JavaScript modules
│       ├── app.js              # Main application logic
│       ├── bpmn-viewer.js      # BPMN viewer management
│       ├── bpmn-controls.js    # File operations
│       ├── bot-responder.js    # AI assistant logic
│       └── ui-manager.js       # UI management
├── data/                       # Data files
│   ├── XMLs/                   # BPMN XML templates
│   └── bpmn_schemas/           # JSON schemas for BPMN
├── main.py                     # FastAPI application entry point
├── pyproject.toml              # Python project configuration
├── settings.py                 # Application settings
└── README.md                   # Project documentation
```

## 🔄 CI/CD Pipeline

This project features a comprehensive CI/CD setup with GitHub Actions:

### Automated Workflows

- **🔨 Continuous Integration**:
  - Docker image building and testing
  - Python code linting with ruff
  - Docker file validation with Hadolint
- **🚀 Continuous Deployment**:
  - Automated Docker image pushes
  - Multi-stage deployment pipeline
  - Automated testing on every push

### Available Workflows

1. `ci-docker-build.yml` - Builds and tests Docker images
2. `ruff_linter.yml` - Python code quality checks
3. `docker_hadolint.yml` - Docker file security and best practices validation
4. `cd-docker-push.yml` - Automated Docker image deployment
5. `cd-render-push.yml` - Static site deployment pipeline

### Benefits

- ✅ Automatic testing on every commit
- ✅ Code quality enforcement
- ✅ Secure Docker practices
- ✅ One-click deployment
- ✅ Consistent development environment

## 🏗️ Architecture

```bash
┌─────────────────────────────────────┐
│  Frontend (bpmn-js)                 │
│  - BPMN visualization               │
│  - Interactive editing              │
│  - UI for AI-assistant              │
└──────────────┬──────────────────────┘
               │ REST API
┌──────────────▼──────────────────────┐
│  Backend (FastAPI)                  │
│  - API routes                       │
│  - XML/JSON assemblers              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  AI Layer (LangGraph + OpenAI)      │
│  - BPMN agent with state machine    │
│  - LLM for natural language → BPMN  │
└─────────────────────────────────────┘
```

## 🔧 API Endpoints

### GET /

Main application page serving the React interface

### GET /health

Health check endpoint

- **Response**: `{"status": "OK"}`

### GET /api/example-bpmn-xml

Get the base BPMN XML structure

- **Response**: `{"xml": "<bpmn:definitions>..."}`

### GET /api/generate?user_input=

Generate BPMN XML code using AI

- **Parameters**: `user_input` (string) - Text description of the process
- **Response**: `{"output": "<bpmn:definitions>..."}`
- **Note**: Powered by LangGraph agent with Open router free tier models

## 📋 Scripts

### Development

- `python main.py` – Launch development server
- `uvicorn main:app --reload` – Launch with auto-reload
- `uvicorn main:app --reload --host 0.0.0.0 --port 8000` – Launch for external access

### Package Management

- `uv sync` – Install/update dependencies
- `uv add <package>` – Add new dependency
- `uv remove <package>` – Remove dependency

### Testing

- `pytest` – Run tests
- `python -m pytest` – Alternative test command

## 🎯 Expansion Possibilities

- Add new BPMN element types
- Integrate a database for diagram persistence
- Implement user authentication
- Enable real‑time collaborative editing
- Export to additional formats (PNG, PDF)
- Provide ready‑made process templates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is released under the MIT license. See the `LICENSE` file for details.

## 🐛 Known Issues

- Requires an internet connection to load the bpmn-js library
- Large diagrams may load slowly
- No built‑in server‑side persistence

## TO-DO's

### ✅ Completed

- [x] Implement BPMN creating from XML-code
- [x] Implement GitHub Actions CI/CD pipeline
- [x] Create modern web interface with bpmn-js
- [x] Implement file upload/download functionality
- [x] Add zoom and viewport controls
- [x] Create AI chat interface with LangGraph
- [x] Implement full AI assistant BPMN generation

### 🚧 In Progress

- [ ] Implement security measures for abusing
- [ ] Implement agent redactoring diagramm
- [ ] Implement XML code validation
- [ ] Add database persistence for diagrams
- [ ] Add extended capabilities of diagram generation

### 📋 Planned Features

- [ ] Add support for additional file formats (PNG, PDF)
- [ ] Add user authentication and diagram sharing
- [ ] Create diagram templates library

## 📞 Support

If you have questions or suggestions:

- Create an Issue on the repository
- Check bpmn-js documentation: <https://bpmn.io/>

## 🙏 Acknowledgements

- [bpmn.io](https://bpmn.io/) – for the excellent BPMN library
- [FastAPI](https://fastapi.tiangolo.com/) – for the modern Python web framework
- [UV](https://docs.astral.sh/uv/) – for the fast Python package manager
- The open‑source community for inspiration

---

**Version**: 0.6.0
**Last Updated**: January 2026
