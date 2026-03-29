/**
 * UI management
 */
class UIManager {
    constructor() {
        this.chatHistory = document.getElementById('chat-history');
        this.hintElement = document.querySelector('.message.hint');
        this.typingElement = null;
    }

    addMessage(text, isUser = false) {
        this._removeTyping();
        this._hideHint();

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        messageDiv.innerHTML = `<div class="msg-content">${text}</div>`;
        this.chatHistory.appendChild(messageDiv);
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
    }

    showTyping() {
        this._removeTyping();
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing-indicator';
        typingDiv.innerHTML = '<div class="spinner"></div>';
        typingDiv.id = 'typing-indicator';
        this.chatHistory.appendChild(typingDiv);
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
    }

    _removeTyping() {
        const existing = document.getElementById('typing-indicator');
        if (existing) existing.remove();
    }

    _hideHint() {
        if (this.hintElement && !this.hintElement.classList.contains('fade-out')) {
            this.hintElement.classList.add('fade-out');
            setTimeout(() => {
                if (this.hintElement?.parentNode) {
                    this.hintElement.remove();
                    this.hintElement = null;
                }
            }, 300);
        }
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
