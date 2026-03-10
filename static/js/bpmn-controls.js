/**
 * Manage save and load operations
 */
class BPMNControls {
    constructor(viewer) {
        this.viewer = viewer;
        this.apiUrl = window.AppConfig.API_URL;
    }

    async loadExampleFromServer() {
        try {
            const response = await fetch(`${this.apiUrl}/example-bpmn-xml`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data.xml;
        } catch (error) {
            console.error('Failed to load example BPMN from server:', error);
            throw error;
        }
    }

    loadFromFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = reject;
            reader.readAsText(file);
        });
    }

    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);
    }

    async downloadSVG() {
        const svg = await this.viewer.saveSVG();
        this.downloadFile(svg, 'bpmn-diagram.svg', 'image/svg+xml');
    }

    async downloadBPMN() {
        const xml = await this.viewer.saveXML();
        this.downloadFile(xml, 'bpmn-diagram.bpmn', 'application/xml');
    }
}