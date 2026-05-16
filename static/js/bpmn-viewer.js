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

    // Undo / Redo
    undo() {
        this.viewer.get('commandStack').undo();
    }

    redo() {
        this.viewer.get('commandStack').redo();
    }

    initKeyboard() {
        const commandStack = this.viewer.get('commandStack');

        const isUndo = (e) => {
            const code = e.code || '';
            const key = (e.key || '').toLowerCase();
            if (code === 'KeyZ' && !e.shiftKey) return true;
            if (!code && key === 'z') return true;
            return false;
        };

        const isRedo = (e) => {
            const code = e.code || '';
            const key = (e.key || '').toLowerCase();
            if (code === 'KeyY') return true;
            if (code === 'KeyZ' && e.shiftKey) return true;
            if (!code && (key === 'y' || (key === 'z' && e.shiftKey))) return true;
            return false;
        };

        this._keydownHandler = (e) => {
            const ctrl = e.ctrlKey || e.metaKey;
            if (!ctrl) return;

            if (isUndo(e)) {
                commandStack.undo();
                e.preventDefault();
                e.stopImmediatePropagation();
                return;
            }
            if (isRedo(e)) {
                commandStack.redo();
                e.preventDefault();
                e.stopImmediatePropagation();
            }
        };

        window.addEventListener('keydown', this._keydownHandler, { capture: true });
    }

    onCommandStackChanged(callback) {
        const eventBus = this.viewer.get('eventBus');
        const commandStack = this.viewer.get('commandStack');
        const fire = () => callback({
            canUndo: commandStack.canUndo(),
            canRedo: commandStack.canRedo()
        });
        eventBus.on('commandStack.changed', fire);
        eventBus.on('elements.changed', fire);
        fire();
        this._undoStatePoll = setInterval(fire, 1000);
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
