class BotResponder {
    /**
     * Generates bot response via API (asynchronously)
     * @param {string} userMessage - User message
     * @returns {Promise<string>} Response from server
     */
    async generateResponse(userMessage) {
        try {
            // 1. Construct URL with parameters
            // encodeURIComponent is important to avoid breaking URL with special characters
            const queryParams = new URLSearchParams({
                user_input: userMessage
            });

            const url = `/api/generate?${queryParams.toString()}`;

            // 2. Perform GET request
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            // 3. Check if response is successful
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // 4. Retrieve data
            const data = await response.json();

            return data.output || JSON.stringify(data);

        } catch (error) {
            console.error('API error:', error);
            return "Sorry, unable to connect to the server.";
        }
    }

    /**
     * Wrapper for compatibility with app.js.
     */
    async generateResponseAsync(userMessage) {
        return await this.generateResponse(userMessage);
    }
}