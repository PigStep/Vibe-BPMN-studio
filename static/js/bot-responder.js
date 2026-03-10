class BotResponder {
    /**
     * Generates bot response via API
     * @param {string} userMessage - User message
     * @returns {Promise<string>} Response from server
     */
    async generateResponse(userMessage) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000);

        try {
            const queryParams = new URLSearchParams({ user_input: userMessage });
            const url = `${window.AppConfig.API_URL}/generate?${queryParams.toString()}`;

            const response = await fetch(url, {
                method: 'GET',
                signal: controller.signal,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data.output || JSON.stringify(data);

        } catch (error) {
            console.error('API error:', error);
            return "Sorry, unable to connect to the server.";
        } finally {
            clearTimeout(timeoutId);
        }
    }
}
