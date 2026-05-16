/**
 * Main application file - initialization and event handling
 */
(function () {
    let bpmnViewer;
    let bpmnControls;
    let uiManager;
    let botResponder;
    let notificationManager;
    let sessionId;

    function getOrCreateSessionId() {
        const storageKey = 'vibe-bpmn-session-id';
        let id = localStorage.getItem(storageKey);
        if (!id) {
            id = crypto.randomUUID();
            localStorage.setItem(storageKey, id);
        }
        return id;
    }

    // Initialization on page load
    window.addEventListener('DOMContentLoaded', async () => {
        try {
            sessionId = getOrCreateSessionId();
            console.log('Session ID:', sessionId);

            I18N.translatePage();

            // Initialize components
            notificationManager = new NotificationManager();
            bpmnViewer = new BPMNViewer();
            uiManager = new UIManager();
            bpmnControls = new BPMNControls(bpmnViewer);
            botResponder = new BotResponder();

            notificationManager.info(I18N.t('notification_hint'));

            bpmnViewer.initialize();

            bpmnViewer.onXMLChange(xml => {
                document.getElementById('xml-editor').value = xml;
            });

            // Load example on start
            const defaultXML = await bpmnControls.loadExampleFromServer();
            document.getElementById('xml-editor').value = defaultXML;
            await bpmnViewer.loadXML(defaultXML);

            setupEventListeners();
            uiManager.initTabs();

            // Language switcher
            document.getElementById('lang-switch').addEventListener('click', function () {
                I18N.switchLang();
            });
        } catch (error) {
            console.error('Initialization error:', error);
        }
    });

    async function updateDiagram(xml) {
        try {
            // Update the text editor
            document.getElementById('xml-editor').value = xml;

            // Update the visual editor
            await bpmnViewer.loadXML(xml);

            console.log('Diagram updated from AI response');
        } catch (error) {
            console.error('Error updating diagram:', error);
        }
    }

    // Setup all event handlers
    function setupEventListeners() {
        // Load from file
        document.getElementById('file-input').addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;

            try {
                const xml = await bpmnControls.loadFromFile(file);
                await updateDiagram(xml);
            } catch (error) {
                console.error('File read error:', error);
            }
        });

        // Undo / Redo
        document.getElementById('undo').addEventListener('click', () => {
            bpmnViewer.undo();
        });
        document.getElementById('redo').addEventListener('click', () => {
            bpmnViewer.redo();
        });
        bpmnViewer.onCommandStackChanged(({ canUndo, canRedo }) => {
            document.getElementById('undo').disabled = !canUndo;
            document.getElementById('redo').disabled = !canRedo;
        });
        bpmnViewer.initKeyboard();

        // Zoom controls
        document.getElementById('zoom-in').addEventListener('click', () => {
            bpmnViewer.zoomIn();
        });

        document.getElementById('zoom-out').addEventListener('click', () => {
            bpmnViewer.zoomOut();
        });

        document.getElementById('fit-viewport').addEventListener('click', () => {
            bpmnViewer.fitViewport();
        });

        // Download controls
        document.getElementById('download-svg').addEventListener('click', async () => {
            try {
                await bpmnControls.downloadSVG();
            } catch (error) {
                console.error('SVG save error:', error);
            }
        });

        document.getElementById('download-bpmn').addEventListener('click', async () => {
            try {
                await bpmnControls.downloadBPMN();
            } catch (error) {
                console.error('BPMN save error:', error);
            }
        });

        // Apply XML from editor
        document.getElementById('apply-xml').addEventListener('click', async () => {
            try {
                const xml = document.getElementById('xml-editor').value.trim();
                if (!xml) return;

                await bpmnViewer.loadXML(xml);
            } catch (error) {
                console.error('XML apply error:', error);
            }
        });

        // Chat functionality
        const chatInput = document.getElementById('chat-input');
        const sendChatBtn = document.getElementById('send-chat');

        sendChatBtn.addEventListener('click', async () => {
            const text = chatInput.value.trim();
            if (!text) return;

            // Guard: don't interrupt an active request
            if (document.getElementById('typing-indicator')) {
                notificationManager.warning(I18N.t('request_in_progress'));
                return;
            }

            uiManager.addMessage(text, true);
            chatInput.value = '';
            uiManager.showTyping();

            try {
                const botResponse = await botResponder.generateResponse(text, sessionId, (error) => {
                    if (error.message === 'blocked') {
                        uiManager.hideTyping();
                        notificationManager.warning(I18N.t('request_in_progress'));
                        return;
                    }
                    notificationManager.error(I18N.t('error_ai_unavailable'));
                });

                if (!botResponse) {
                    uiManager.hideTyping();
                    return;
                }

                const xmlMatch = botResponse.match(/<\?xml[\s\S]*?<\/bpmn:definitions>|<bpmn:definitions[\s\S]*?<\/bpmn:definitions>/);

                if (xmlMatch) {
                    const xmlContent = xmlMatch[0];
                    const cleanXml = xmlContent.replace(/^```xml\s*/, '').replace(/```$/, '');
                    await updateDiagram(cleanXml);
                    uiManager.addSuccess(I18N.t('success'));
                } else if (botResponse.includes('Sorry') || botResponse.includes('tech problem')) {
                    uiManager.addMessage(I18N.t('error_unavailable'));
                }
            } catch (error) {
                console.error('Error generating bot response:', error);
                uiManager.addMessage(I18N.t('error_generic'));
            }
        });

        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendChatBtn.click();
            }
        });
    }
})();
