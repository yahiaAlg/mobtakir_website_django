document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.querySelector('.chat-messages');
    const messageInput = document.querySelector('#message-input');
    const sendButton = document.querySelector('#send-button');
    const newChatButton = document.querySelector('#new-chat-button');
    const sessionsList = document.querySelector('.chat-sessions');
    const fileUploadButton = document.querySelector('#file-upload-button');
    const fileInput = document.querySelector('#file-input');
    
    let currentSessionId = null;
    let isProcessing = false;

    // Initialize chat
    initializeChat();

    function initializeChat() {
        // Load existing sessions
        loadChatSessions();
        
        // Set up event listeners
        setupEventListeners();
        
        // Load last active session if any
        const lastSessionId = localStorage.getItem('lastSessionId');
        if (lastSessionId) {
            loadChatHistory(lastSessionId);
        }
    }

    function setupEventListeners() {
        // Send message on button click or Enter key
        sendButton.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // New chat button
        newChatButton.addEventListener('click', startNewChat);

        // File upload handling
        fileUploadButton.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', handleFileUpload);

        // Dynamic textarea height
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }

    async function sendMessage() {
        if (isProcessing || !messageInput.value.trim()) return;

        const message = messageInput.value.trim();
        messageInput.value = '';
        messageInput.style.height = 'auto';

        // Display user message immediately
        appendMessage('user', message);

        // Show typing indicator
        showTypingIndicator();
        
        isProcessing = true;
        
        try {
            const formData = new FormData();
            formData.append('prompt', message);
            if (currentSessionId) {
                formData.append('session_id', currentSessionId);
            }

            const response = await fetch('/chat/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });

            const data = await response.json();
            
            if (!response.ok) throw new Error(data.error || 'Failed to get response');

            // Remove typing indicator
            hideTypingIndicator();

            // Display bot response
            appendMessage('assistant', data.content);
            
            // Update session if new
            if (data.session_id && !currentSessionId) {
                currentSessionId = data.session_id;
                localStorage.setItem('lastSessionId', currentSessionId);
                await loadChatSessions(); // Refresh sessions list
            }

        } catch (error) {
            hideTypingIndicator();
            showNotification(error.message, 'error');
        } finally {
            isProcessing = false;
        }

        scrollToBottom();
    }

    async function loadChatSessions() {
        try {
            const response = await fetch('/chat/sessions/');
            const data = await response.json();
            
            sessionsList.innerHTML = ''; // Clear existing sessions
            
            data.sessions.forEach(session => {
                const sessionElement = createSessionElement(session);
                sessionsList.appendChild(sessionElement);
            });
        } catch (error) {
            showNotification('Failed to load chat sessions', 'error');
        }
    }

    async function loadChatHistory(sessionId) {
        try {
            const response = await fetch(`/chat/history/${sessionId}/`);
            const data = await response.json();
            
            // Clear current chat
            chatContainer.innerHTML = '';
            
            // Display messages
            data.messages.forEach(msg => {
                appendMessage(msg.role, msg.content);
            });
            
            currentSessionId = sessionId;
            scrollToBottom();
            
        } catch (error) {
            showNotification('Failed to load chat history', 'error');
        }
    }

    async function handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        try {
            const formData = new FormData();
            formData.append('file', file);
            if (currentSessionId) {
                formData.append('session_id', currentSessionId);
            }

            showUploadingIndicator();

            const response = await fetch('/chat/upload/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });

            const data = await response.json();
            
            if (!response.ok) throw new Error(data.error);

            hideUploadingIndicator();
            
            // Handle successful upload
            if (data.image_url) {
                appendMessage('user', `[Uploaded image: ${file.name}]`);
                // If the response includes analysis, show it
                if (data.analysis) {
                    appendMessage('assistant', data.analysis);
                }
            }

        } catch (error) {
            hideUploadingIndicator();
            showNotification(error.message, 'error');
        }

        // Clear file input
        fileInput.value = '';
    }

    function startNewChat() {
        currentSessionId = null;
        chatContainer.innerHTML = '';
        messageInput.value = '';
        localStorage.removeItem('lastSessionId');
    }

    function appendMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Handle markdown/code formatting if needed
        if (role === 'assistant') {
            contentDiv.innerHTML = marked.parse(content); // Using marked.js for markdown
            // Highlight code blocks if any
            contentDiv.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });
        } else {
            contentDiv.textContent = content;
        }
        
        messageDiv.appendChild(contentDiv);
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
    }

    function createSessionElement(session) {
        const div = document.createElement('div');
        div.className = 'chat-session';
        div.innerHTML = `
            <span>${session.title}</span>
            <span class="session-time">${formatDate(session.updated_at)}</span>
        `;
        
        div.addEventListener('click', () => loadChatHistory(session.id));
        
        return div;
    }

    function showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.innerHTML = '<span></span><span></span><span></span>';
        chatContainer.appendChild(indicator);
        scrollToBottom();
    }

    function hideTypingIndicator() {
        const indicator = document.querySelector('.typing-indicator');
        if (indicator) indicator.remove();
    }

    function showUploadingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'uploading-indicator';
        indicator.textContent = 'Uploading file...';
        chatContainer.appendChild(indicator);
        scrollToBottom();
    }

    function hideUploadingIndicator() {
        const indicator = document.querySelector('.uploading-indicator');
        if (indicator) indicator.remove();
    }

    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffMinutes = Math.floor((now - date) / 60000);
        
        if (diffMinutes < 1) return 'just now';
        if (diffMinutes < 60) return `${diffMinutes}m ago`;
        if (diffMinutes < 1440) return `${Math.floor(diffMinutes/60)}h ago`;
        return date.toLocaleDateString();
    }
});