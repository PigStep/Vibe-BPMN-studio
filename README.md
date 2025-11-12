# Easy XML-to-BPMN Creator

A web application for creating, viewing, and editing BPMN diagrams (Business Process Model and Notation).

## 📋 Description

BPMN Creator offers a user‑friendly web interface for working with BPMN diagrams. The application allows users to create new diagrams, edit existing ones, import from files or text, and export results in various formats.

## ✨ Features

- 🎨 **Diagram Creation**: Intuitive editor with a palette of elements
- 📖 **Diagram Viewing**: Quick preview of BPMN diagrams with zoom capabilities
- 📁 **Data Import**: Upload diagrams from a text field or files (.bpmn, .xml)
- 💾 **Export**: Save diagrams in SVG and BPMN formats
- 🔄 **Modes**: Switch between view and edit modes
- 🖱️ **Navigation**: Zoom, fit‑to‑screen, and pan functionality
- 📱 **Responsive Design**: Adaptive interface for all devices

## 🛠️ Technologies

- **Backend**: Node.js, Express.js
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **BPMN Library**: bpmn-js v9.4.0
- **Styling**: Built‑in CSS styles

## 📦 Installation and Setup

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd bpmn-creator
   ```

2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Start the server**:

   ```bash
   npm start
   ```

4. **Open the application**:
   Navigate to `http://localhost:3000` in your browser.

## 🚀 Usage

### Core Functions

#### 1. Diagram Upload

**From Text:**

- Paste BPMN XML into the text field
- Click **Load BPMN**

**From File:**

- Switch to the **Load from File** tab
- Select a file with a .bpmn or .xml extension

#### 2. Editing

- Click **Edit Mode** to activate the element palette
- Use left‑side elements to create new components
- Click **Save Changes** to update the XML

#### 3. Viewing

- Use zoom buttons to increase/decrease view
- **Fit to Screen** automatically adjusts the zoom level
- Drag the diagram for navigation

#### 4. Export

- **SVG**: Download vector image
- **BPMN**: Save as BPMN format for further editing

### Example BPMN

The application loads with a sample diagram that includes:

- Start event
- Two tasks
- End event
- Sequential flows

## 📁 Project Structure

```
bpmn-creator/
├── public/                 # Static assets (empty folder)
├── server.js               # Express server
├── viewer.html             # Main application interface
├── package.json            # Project configuration and dependencies
├── package-lock.json       # Locked dependency versions
├── .gitattributes          # Git attributes
├── LICENSE                 # MIT license
└── README.md               # Project documentation
```

## 🔧 API Endpoints

### GET /

Main application page

### GET /api/generate-bpmn

Endpoint for generating BPMN (extendable)

- **Response**: JSON object with status information

## 📋 Scripts

- `npm start` – Launch development server
- `npm test` – Run tests (not configured)

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

## 📞 Support

If you have questions or suggestions:

- Create an Issue on the repository
- Check bpmn-js documentation: <https://bpmn.io/>

## 🙏 Acknowledgements

- [bpmn.io](https://bpmn.io/) – for the excellent BPMN library
- [Express.js](https://expressjs.com/) – for the robust web framework
- The open‑source community for inspiration

---

**Version**: 0.0.3
**Last Updated**: November 2025
