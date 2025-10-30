document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const newChatButton = document.getElementById('new-chat-button');
    const sessionList = document.getElementById('session-list');
    const importButton = document.getElementById('import-button');
    const exportButton = document.getElementById('export-button');
    const chatTitle = document.getElementById('chat-title');
    const ragStatusButton = document.getElementById('rag-status-button');
    const webSearchStatusButton = document.getElementById('web-search-status-button');
    const settingsButton = document.getElementById('settings-button');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const settingsModal = document.getElementById('settings-modal');
    const closeButton = document.querySelector('.close-button');
    const modelSelect = document.getElementById('model-select');
    const temperatureSlider = document.getElementById('temperature-slider');
    const temperatureValue = document.getElementById('temperature-value');
    const maxTokensSlider = document.getElementById('max-tokens-slider');
    const maxTokensValue = document.getElementById('max-tokens-value');
    const systemPrompt = document.getElementById('system-prompt');
    const saveSettingsButton = document.getElementById('save-settings-button');
    const resetSettingsButton = document.getElementById('reset-settings-button');

    // State
    let currentSessionId = null;
    let sessions = {};
    let useRag = false;
    let useWebSearch = false;

    // Initialize Markdown-it and hljs
    const md = window.markdownit({
        highlight: function (str, lang) {
            if (lang && hljs.getLanguage(lang)) {
                try {
                    return hljs.highlight(str, { language: lang }).value;
                } catch (__) {}
            }
            return ''; // use external default escaping
        }
    });

    // Event Listeners
    sidebarToggle.addEventListener('click', () => {
        sidebar.style.marginLeft = sidebar.style.marginLeft === '0px' ? '-260px' : '0px';
    });

    newChatButton.addEventListener('click', createNewSession);
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    settingsButton.addEventListener('click', () => settingsModal.style.display = 'flex');
    closeButton.addEventListener('click', () => settingsModal.style.display = 'none');
    window.addEventListener('click', (e) => {
        if (e.target === settingsModal) {
            settingsModal.style.display = 'none';
        }
    });

    saveSettingsButton.addEventListener('click', saveSettings);
    resetSettingsButton.addEventListener('click', resetSettings);

    ragStatusButton.addEventListener('click', () => {
        useRag = !useRag;
        ragStatusButton.classList.toggle('active', useRag);
    });

    webSearchStatusButton.addEventListener('click', () => {
        useWebSearch = !useWebSearch;
        webSearchStatusButton.classList.toggle('active', useWebSearch);
    });

    temperatureSlider.addEventListener('input', () => temperatureValue.textContent = temperatureSlider.value);
    maxTokensSlider.addEventListener('input', () => maxTokensValue.textContent = maxTokensSlider.value);

    // Functions
    async function createNewSession() {
        try {
            const response = await fetch('/sessions', { method: 'POST' });
            const data = await response.json();
            currentSessionId = data.session_id;
            chatMessages.innerHTML = '';
            chatTitle.textContent = 'New Chat';
            loadSessions();
        } catch (error) {
            console.error('Error creating new session:', error);
        }
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage(message, true);
        userInput.value = '';
        showThinking();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    session_id: currentSessionId,
                    use_rag: useRag,
                    use_web_search: useWebSearch
                })
            });
            const data = await response.json();
            hideThinking();
            addMessage(data.response, false);
        } catch (error) {
            console.error('Error sending message:', error);
            hideThinking();
            addMessage('An error occurred. Please try again.', false);
        }
    }

    function addMessage(content, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', isUser ? 'user-message' : 'bot-message');
        messageDiv.innerHTML = md.render(content);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showThinking() {
        const thinkingDiv = document.createElement('div');
        thinkingDiv.classList.add('message', 'bot-message');
        thinkingDiv.id = 'thinking-indicator';
        thinkingDiv.innerHTML = '<i class="fas fa-spinner fa-pulse"></i> Thinking...';
        chatMessages.appendChild(thinkingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function hideThinking() {
        const thinkingIndicator = document.getElementById('thinking-indicator');
        if (thinkingIndicator) {
            thinkingIndicator.remove();
        }
    }

    async function loadSessions() {
        try {
            const response = await fetch('/sessions');
            sessions = await response.json();
            sessionList.innerHTML = '';
            sessions.forEach(session => {
                const sessionItem = document.createElement('div');
                sessionItem.classList.add('session-item');
                sessionItem.textContent = session.title;
                sessionItem.dataset.sessionId = session.id;
                if (session.id === currentSessionId) {
                    sessionItem.classList.add('active');
                }
                sessionItem.addEventListener('click', () => {
                    currentSessionId = session.id;
                    loadSession(session.id);
                    document.querySelectorAll('.session-item').forEach(item => item.classList.remove('active'));
                    sessionItem.classList.add('active');
                });
                sessionList.appendChild(sessionItem);
            });
        } catch (error) {
            console.error('Error loading sessions:', error);
        }
    }

    async function loadSession(sessionId) {
        try {
            const response = await fetch(`/sessions/${sessionId}`);
            const history = await response.json();
            chatMessages.innerHTML = '';
            history.forEach(message => {
                addMessage(message.content, message.role === 'user');
            });
            chatTitle.textContent = sessions.find(s => s.id === sessionId).title;
        } catch (error) {
            console.error('Error loading session:', error);
        }
    }

    async function loadModels() {
        try {
            const response = await fetch('/models');
            const models = await response.json();
            modelSelect.innerHTML = '';

            const productionHeader = document.createElement('optgroup');
            productionHeader.label = 'Production Models';
            models.production.forEach(model => {
                const option = document.createElement('option');
                option.value = model.id;
                option.textContent = `${model.name} (${model.parameters})`;
                productionHeader.appendChild(option);
            });
            modelSelect.appendChild(productionHeader);

            const previewHeader = document.createElement('optgroup');
            previewHeader.label = 'Preview Models';
            models.preview.forEach(model => {
                const option = document.createElement('option');
                option.value = model.id;
                option.textContent = `${model.name} (${model.parameters})`;
                previewHeader.appendChild(option);
            });
            modelSelect.appendChild(previewHeader);
        } catch (error) {
            console.error('Error loading models:', error);
        }
    }

    async function loadSettings() {
        try {
            const response = await fetch('/settings');
            const settings = await response.json();
            modelSelect.value = settings.model;
            temperatureSlider.value = settings.temperature;
            temperatureValue.textContent = settings.temperature;
            maxTokensSlider.value = settings.max_tokens;
            maxTokensValue.textContent = settings.max_tokens;
            systemPrompt.value = settings.system_prompt;
        } catch (error) {
            console.error('Error loading settings:', error);
        }
    }

    async function saveSettings() {
        const settings = {
            model: modelSelect.value,
            temperature: parseFloat(temperatureSlider.value),
            max_tokens: parseInt(maxTokensSlider.value),
            system_prompt: systemPrompt.value,
        };
        try {
            await fetch('/settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(settings)
            });
            settingsModal.style.display = 'none';
        } catch (error) {
            console.error('Error saving settings:', error);
        }
    }

    async function resetSettings() {
        try {
            await fetch('/settings/reset', { method: 'POST' });
            loadSettings();
        } catch (error) {
            console.error('Error resetting settings:', error);
        }
    }

    // Initial Load
    async function init() {
        await loadModels();
        await loadSettings();
        await loadSessions();
        if (!currentSessionId && sessions.length > 0) {
            currentSessionId = sessions[0].id;
            loadSession(currentSessionId);
        } else if (!currentSessionId) {
            createNewSession();
        }
    }

    init();
});
