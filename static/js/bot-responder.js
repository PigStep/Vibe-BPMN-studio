class BotResponder {
    /**
     * Generates bot response via API (asynchronously)
     * @param {string} userMessage - User message
     * @returns {Promise<string>} Response from server
     */
    generate_session_id() {
        return localStorage.getItem('bpmn_session_id') || crypto.randomUUID();
    }
    async generateResponseAsync(userMessage) {
        try {
            const sessionId = this.generate_session_id();
            localStorage.setItem('bpmn_session_id', sessionId);

            // Perform POST request to get xml
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Session-ID': sessionId
                },
                body: JSON.stringify({
                    user_input: userMessage
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            return data.output || JSON.stringify(data);

        } catch (error) {
            console.error('API error:', error);
            return "Sorry, unable to connect to the server.";
        }
    }
}