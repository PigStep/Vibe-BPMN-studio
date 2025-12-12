# Vibe BPMN Studio

A modern web application for creating, viewing, and editing BPMN diagrams (Business Process Model and Notation) with AI-powered assistant.

## 📋 Description

BPMN Creator offers a user‑friendly web interface for working with BPMN diagrams. The application allows users to create new diagrams, edit existing ones, import from files or text, and export results in various formats.

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

## 📦 Installation and Setup

### Prerequisites

- Python 3.13 or higher
- UV package manager (recommended) or pip

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd bpmn-creator
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

## 🚀 Usage

### Core Functions

#### 1. Working with AI Assistant

- Navigate to **AI Ассистент** tab in the sidebar
- Type your request in natural language (e.g., "Add task 'Review Document'")
- AI will help generate and modify BPMN diagrams
- Example: "Create a process with start event, approval task, and end event"

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

```
bpmn-creator/
├── src/                    # Python source code
│   ├── api_routes.py       # FastAPI routes
│   ├── get_example_diagram.py  # Example diagram loader
│   └── schemas.py          # Pydantic schemas
├── static/                 # Frontend assets
│   ├── index.html          # Main application interface
│   ├── css/
│   │   └── style.css       # Modern styling
│   └── js/                 # JavaScript modules
│       ├── app.js          # Main application logic
│       ├── bpmn-viewer.js  # BPMN viewer management
│       ├── bpmn-controls.js # File operations
│       ├── bot-responder.js # AI assistant logic
│       └── ui-manager.js   # UI management
├── data/                   # Data files
│   └── XMLs/
│       └── base_bpmn_diagram.xml  # Default BPMN template
├── main.py                 # FastAPI application entry point
├── pyproject.toml          # Python project configuration
├── uv.lock                 # UV package manager lock file
├── .python-version         # Python version specification
├── .gitattributes          # Git attributes
├── LICENSE                 # MIT license
└── README.md               # Project documentation
```

## 🏗️ Arhitecture

┌─────────────────────────────────────┐
│  Frontend (bpmn-js)                 │
│  - BPMN vizualization               │
│  - Interactive editing              │
│  - UI for AI-assistant              │
└──────────────┬──────────────────────┘
               │ REST API
┌──────────────▼──────────────────────┐
│  Backend (FastAPI)                  │
│  - Storing BPMN XML in DB           │
│  - AI XML code generation           │
│  - Validation and transforming      │
└─────────────────────────────────────┘

## 🔧 API Endpoints

### GET /

Main application page serving the React interface

### GET /health

Health check endpoint

- **Response**: `{"status": "OK"}`

### GET /api/example-bpmn-xml

Get the base BPMN XML structure

- **Response**: `{"xml": "<bpmn:definitions>..."}`

### POST /api/generate

Generate BPMN XML code (extendable)

- **Response**: JSON object with generation status
- **Note**: Currently returns placeholder, ready for AI integration

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

- `pytest` – Run tests (to be implemented)
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
- Visualization of complex BPMN diagrams can be cumbersome due to limited zoom and panning controls

## TO-DO's

- [x] Implement BPMN creating from XML-code
- [ ] Implement AI assistant diagramm creation
- [ ] Implement AI assistant diagramm editing
- [ ] Implement XML code validation
- [ ] Implement database persistence
- [ ] Add support for additional file formats (PNG, PDF)
- [ ] Implement real‑time collaborative editing

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

**Version**: 0.1.0
**Last Updated**: December 2025
