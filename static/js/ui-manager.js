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
        const contentDiv = document.createElement('div');
        contentDiv.className = 'msg-content';
        contentDiv.textContent = text;
        messageDiv.appendChild(contentDiv);
        this.chatHistory.appendChild(messageDiv);
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
    }

    // TODO: replace showTyping() with real-time progress updates from SSE/streaming
    showTyping() {
        this._removeTyping();
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing-indicator';
        typingDiv.innerHTML = '<div class="spinner"></div>';
        typingDiv.id = 'typing-indicator';
        this.chatHistory.appendChild(typingDiv);
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
    }

    addSuccess(text) {
        this._removeTyping();
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot success';

        const icon = document.createElement('i');
        icon.className = 'fa-solid fa-check-circle';
        const span = document.createElement('span');
        span.textContent = text;

        messageDiv.appendChild(icon);
        messageDiv.appendChild(span);
        this.chatHistory.appendChild(messageDiv);
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
    }

    addRetryBadge(text, onRetry) {
        this._removeTyping();
        const userMessages = this.chatHistory.querySelectorAll('.message.user');
        const lastUserMsg = userMessages[userMessages.length - 1];
        if (!lastUserMsg) return;

        lastUserMsg.classList.add('blocked');

        const retryBar = document.createElement('div');
        retryBar.className = 'retry-bar';

        const retryText = document.createElement('span');
        retryText.className = 'retry-text';
        retryText.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Предыдущий запрос ещё выполняется. Дождитесь ответа.';

        const retryBtn = document.createElement('button');
        retryBtn.className = 'retry-btn';
        retryBtn.innerHTML = '<i class="fa-solid fa-rotate"></i>';
        retryBtn.title = 'Повторить запрос';
        retryBtn.addEventListener('click', () => {
            this._removeRetryBadge(lastUserMsg);
            onRetry(text);
        });

        retryBar.appendChild(retryText);
        retryBar.appendChild(retryBtn);
        lastUserMsg.appendChild(retryBar);
    }

    _removeRetryBadge(msgElement) {
        const bar = msgElement.querySelector('.retry-bar');
        if (bar) bar.remove();
        msgElement.classList.remove('blocked');
    }

    hideTyping() {
        this._removeTyping();
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
