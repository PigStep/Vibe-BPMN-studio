/**
 * Management of BPMN viewer/modeler
 */
class BPMNViewer {
    constructor() {
        this.viewer = null;
    }

    initialize() {
        if (typeof BpmnJS === 'undefined') {
            throw new Error('bpmn-js library is not loaded');
        }

        this.viewer = new BpmnJS({
            container: '#bpmn-container',
            keyboard: { bindTo: window }
        });

        return this.viewer;
    }

    get #canvas() {
        return this.viewer.get('canvas');
    }

    async loadXML(xml) {
        if (!xml || xml.trim() === '') {
            throw new Error('Empty XML provided for loading');
        }

        await this.viewer.importXML(xml);
        this.fitViewport();
    }

    async saveXML() {
        const result = await this.viewer.saveXML({ format: true });
        return result.xml;
    }

    async saveSVG() {
        const result = await this.viewer.saveSVG();
        return result.svg;
    }

    onXMLChange(callback) {
        this.viewer.on('commandStack.changed', async () => {
            const xml = await this.saveXML();
            callback(xml);
        });
    }

    // Zoom control
    zoomIn() {
        this.#canvas.zoom(this.#canvas.zoom() * 1.2);
    }

    zoomOut() {
        this.#canvas.zoom(this.#canvas.zoom() * 0.8);
    }

    fitViewport() {
        this.#canvas.zoom('fit-viewport');
    }
}
