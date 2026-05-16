class BotResponder {
    /**
     * Generates bot response via API
     * TODO: replace with streaming/SSE for real-time progress
     *
     * @param {string} userMessage - User message
     * @param {string} sessionId - Session identifier
     * @param {Function} onError - Optional callback for error handling
     * @returns {Promise<string>} Response from server
     */
    async generateResponse(userMessage, sessionId, onError) {
        try {
            const url = `${window.AppConfig.API_URL}/generate`;

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_input: userMessage,
                    session_id: sessionId,
                }),
            });

            const data = await response.json();

            if (data.status === false) {
                throw new Error('blocked');
            }

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return data.output || JSON.stringify(data);

        } catch (error) {
            console.error('API error:', error);
            if (onError) {
                onError(error);
            }
            if (error.message === 'blocked') {
                return '';
            }
            return "Sorry, unable to connect to the server.";
        }
    }
}
