/**
 * Chatbot Frontend Logic
 * Handles UI interactions, API calls, and real-time updates
 */

class ChatbotApp {
    constructor() {
        this.sessionId = null;
        this.uploadedFile = null;
        this.isProcessing = false;

        this.initializeElements();
        this.attachEventListeners();
        this.createSession();
    }

    initializeElements() {
        this.messagesContainer = document.getElementById('messagesContainer');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.fileInput = document.getElementById('fileInput');
        this.fileUploadZone = document.getElementById('fileUploadZone');
        this.filePreview = document.getElementById('filePreview');
        this.fileName = document.getElementById('fileName');
        this.removeFileBtn = document.getElementById('removeFile');
        this.modeBadge = document.getElementById('modeBadge');
    }

    attachEventListeners() {
        // Send message
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
        });

        // File upload
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.removeFileBtn.addEventListener('click', () => this.removeFile());

        // Drag and drop
        this.fileUploadZone.addEventListener('click', () => {
            if (!this.uploadedFile) {
                this.fileInput.click();
            }
        });

        this.fileUploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.fileUploadZone.classList.add('dragover');
        });

        this.fileUploadZone.addEventListener('dragleave', () => {
            this.fileUploadZone.classList.remove('dragover');
        });

        this.fileUploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            this.fileUploadZone.classList.remove('dragover');

            if (e.dataTransfer.files.length > 0) {
                this.uploadedFile = e.dataTransfer.files[0];
                this.showFilePreview();
            }
        });
    }

    async createSession() {
        try {
            const response = await fetch('/api/chat/sessions/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            const data = await response.json();
            this.sessionId = data.id;
            console.log('Session created:', this.sessionId);
        } catch (error) {
            console.error('Error creating session:', error);
            this.showError('Failed to create chat session. Please refresh the page.');
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            const ext = file.name.split('.').pop().toLowerCase();
            if (ext !== 'pdf' && ext !== 'csv') {
                alert('Please upload only PDF or CSV files.');
                return;
            }

            this.uploadedFile = file;
            this.showFilePreview();
        }
    }

    showFilePreview() {
        this.fileName.textContent = this.uploadedFile.name;
        this.filePreview.style.display = 'flex';
        this.fileUploadZone.querySelector('.file-upload-content').style.display = 'none';
    }

    removeFile() {
        this.uploadedFile = null;
        this.fileInput.value = '';
        this.filePreview.style.display = 'none';
        this.fileUploadZone.querySelector('.file-upload-content').style.display = 'block';
    }

    async sendMessage() {
        if (this.isProcessing) return;

        const message = this.messageInput.value.trim();

        if (!message && !this.uploadedFile) {
            return;
        }

        this.isProcessing = true;
        this.sendButton.disabled = true;

        // Create FormData or JSON based on file upload
        let requestData;
        let headers = {};

        if (this.uploadedFile) {
            requestData = new FormData();
            requestData.append('session_id', this.sessionId);
            requestData.append('message', message || 'File uploaded');
            requestData.append('file', this.uploadedFile);
        } else {
            requestData = JSON.stringify({
                session_id: this.sessionId,
                message: message
            });
            headers['Content-Type'] = 'application/json';
        }

        // Clear input
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        this.removeFile();

        // Show typing indicator
        this.showTypingIndicator();

        try {
            const response = await fetch('/api/chat/message/', {
                method: 'POST',
                headers: headers,
                body: requestData
            });

            const data = await response.json();

            // Remove typing indicator
            this.removeTypingIndicator();

            // Display messages
            this.displayMessage(data.user_message);
            this.displayMessage(data.assistant_message);

            // Update mode badge
            this.updateModeBadge(data.assistant_message.mode);

        } catch (error) {
            console.error('Error sending message:', error);
            this.removeTypingIndicator();
            this.showError('Failed to send message. Please try again.');
        } finally {
            this.isProcessing = false;
            this.sendButton.disabled = false;
            this.messageInput.focus();
        }
    }

    displayMessage(messageData) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${messageData.role}`;

        // Avatar
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = messageData.role === 'user' ? '👤' : '🤖';

        // Content
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';

        // Handle CSV suggestions
        if (messageData.mode === 'csv_analysis' && messageData.metadata?.suggestions) {
            textDiv.innerHTML = this.formatMarkdown(messageData.content);
            const suggestionsDiv = this.createSuggestions(
                messageData.metadata.suggestions,
                messageData.metadata.file_path,
                messageData.metadata  // Pass full metadata for later use
            );
            contentDiv.appendChild(textDiv);
            contentDiv.appendChild(suggestionsDiv);
        } else {
            // Format content with markdown
            textDiv.innerHTML = this.formatMarkdown(messageData.content);
            contentDiv.appendChild(textDiv);
        }

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);

        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();

        // Highlight code blocks
        if (messageData.content.includes('```')) {
            setTimeout(() => {
                contentDiv.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });
            }, 100);
        }
    }

    createSuggestions(suggestions, csvPath, fullMetadata) {
        const container = document.createElement('div');
        container.className = 'csv-suggestions';

        suggestions.forEach(suggestion => {
            const card = document.createElement('div');
            card.className = 'suggestion-card';
            card.onclick = () => this.executeCsvAction(suggestion.id, csvPath, fullMetadata);

            const number = document.createElement('div');
            number.className = 'suggestion-number';
            number.textContent = suggestion.id;

            const content = document.createElement('div');
            content.className = 'suggestion-content';
            content.innerHTML = `
                <h4>${suggestion.title}</h4>
                <p>${suggestion.description}</p>
            `;

            card.appendChild(number);
            card.appendChild(content);
            container.appendChild(card);
        });

        return container;
    }

    async executeCsvAction(actionId, csvPath, analysis) {
        if (this.isProcessing) return;

        this.isProcessing = true;
        this.showTypingIndicator();

        try {
            const response = await fetch('/api/chat/action/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    action_id: actionId,
                    csv_path: csvPath,
                    analysis: analysis || {}
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            this.removeTypingIndicator();

            if (data.assistant_message) {
                this.displayMessage(data.assistant_message);
            } else if (data.error) {
                this.showError(data.error);
            }

        } catch (error) {
            console.error('Error executing CSV action:', error);
            this.removeTypingIndicator();
            this.showError('Failed to execute action. Please try again.');
        } finally {
            this.isProcessing = false;
        }
    }

    formatMarkdown(text) {
        // Use marked.js if available, otherwise basic formatting
        if (typeof marked !== 'undefined') {
            marked.setOptions({
                highlight: function (code, lang) {
                    if (lang && hljs.getLanguage(lang)) {
                        return hljs.highlight(code, { language: lang }).value;
                    }
                    return code;
                },
                breaks: true
            });
            return marked.parse(text);
        }

        // Fallback: basic formatting
        return text
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.+?)\*/g, '<em>$1</em>')
            .replace(/`(.+?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }

    showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'message assistant';
        indicator.id = 'typingIndicator';

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = '🤖';

        const content = document.createElement('div');
        content.className = 'message-content';
        content.innerHTML = `
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;

        indicator.appendChild(avatar);
        indicator.appendChild(content);

        this.messagesContainer.appendChild(indicator);
        this.scrollToBottom();
    }

    removeTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.remove();
        }
    }

    updateModeBadge(mode) {
        const modeNames = {
            'general_chat': 'General Chat',
            'code_generation': '💻 Code Generation',
            'pdf_extraction': '📄 PDF Extraction',
            'csv_analysis': '📊 CSV Analysis',
            'csv_action': '📊 CSV Processing',
            'error': '⚠️ Error'
        };

        this.modeBadge.textContent = modeNames[mode] || 'General Chat';

        if (mode !== 'general_chat') {
            this.modeBadge.classList.add('active');
            setTimeout(() => {
                this.modeBadge.classList.remove('active');
            }, 3000);
        }
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message assistant';

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = '⚠️';

        const content = document.createElement('div');
        content.className = 'message-content';
        content.innerHTML = `
            <div class="message-text" style="color: var(--secondary);">
                ${message}
            </div>
        `;

        errorDiv.appendChild(avatar);
        errorDiv.appendChild(content);

        this.messagesContainer.appendChild(errorDiv);
        this.scrollToBottom();
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new ChatbotApp();
});
