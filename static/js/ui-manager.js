/**
 * UI management
 */
class UIManager {
    constructor() {
        this.chatHistory = document.getElementById('chat-history');
    }

    addMessage(text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        messageDiv.innerHTML = `<div class="msg-content">${text}</div>`;
        this.chatHistory.appendChild(messageDiv);
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
    }

    initTabs() {
        const tabButtons = document.querySelectorAll('.tab-btn');

        tabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const targetId = e.target.getAttribute('data-target');

                tabButtons.forEach(btn => btn.classList.remove('active'));
                e.target.classList.add('active');

                document.querySelectorAll('.sidebar-content').forEach(content => {
                    content.classList.remove('active');
                });
                document.getElementById(targetId).classList.add('active');
            });
        });
    }
}
