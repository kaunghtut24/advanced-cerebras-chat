document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const clearButton = document.getElementById('clear-button');

    // Function to add a message to the chat
    function addMessage(content, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to show loading message
    function showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('loading');
        loadingDiv.id = 'loading-message';
        loadingDiv.textContent = 'Thinking...';
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        sendButton.disabled = true;
    }

    // Function to hide loading message
    function hideLoading() {
        const loadingDiv = document.getElementById('loading-message');
        if (loadingDiv) {
            loadingDiv.remove();
        }
        sendButton.disabled = false;
    }

    // Function to get bot response
    async function getBotResponse(userMessage) {
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userMessage })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data.response;
        } catch (error) {
            console.error('Error getting bot response:', error);
            return 'Sorry, I encountered an error while processing your request.';
        }
    }

    // Function to handle sending a message
    async function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            // Add user message to chat
            addMessage(message, true);
            userInput.value = '';

            // Show loading indicator
            showLoading();

            // Get bot response
            const botResponse = await getBotResponse(message);

            // Hide loading indicator
            hideLoading();

            // Add bot message to chat
            addMessage(botResponse, false);
        }
    }

    // Function to clear the conversation
    async function clearConversation() {
        try {
            const response = await fetch('/clear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Clear the chat messages display
            chatMessages.innerHTML = '';

            // Add initial bot message
            addMessage('Hello! I am a Cerebras AI assistant. How can I help you today?', false);
        } catch (error) {
            console.error('Error clearing conversation:', error);
            addMessage('Sorry, I encountered an error while clearing the conversation.', false);
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    clearButton.addEventListener('click', clearConversation);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Add initial bot message
    addMessage('Hello! I am a Cerebras AI assistant. How can I help you today?', false);
});
