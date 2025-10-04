document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const clearButton = document.getElementById('clear-button');
    const settingsPanel = document.getElementById('settings-panel');
    const toggleSettings = document.getElementById('toggle-settings');
    const settingsForm = document.getElementById('settings-form');
    const resetSettings = document.getElementById('reset-settings');
    const resetSystemPrompt = document.getElementById('reset-system-prompt');
    const temperatureInput = document.getElementById('temperature');
    const temperatureValue = document.getElementById('temperature-value');
    const systemPromptInput = document.getElementById('system-prompt');

    // Sessions elements
    const sessionsPanel = document.getElementById('sessions-panel');
    const sessionsList = document.getElementById('sessions-list');
    const toggleSessions = document.getElementById('toggle-sessions');
    const newChatButton = document.getElementById('new-chat');
    const exportChatButton = document.getElementById('export-chat');
    const importChatButton = document.getElementById('import-chat');
    const importFileInput = document.getElementById('import-file');
    const sessionsSearchInput = document.getElementById('sessions-search-input');
    const clearSearchButton = document.getElementById('clear-search');

    let currentSessionId = null;
    let currentKnowledgeBase = null;
    let ragEnabled = false;
    let webSearchEnabled = false;

    // Default system prompt optimized for RAG and Web Search
    const DEFAULT_SYSTEM_PROMPT = `You are an advanced AI assistant powered by Cerebras, designed to provide comprehensive, accurate, and well-structured responses. Your primary goal is to be maximally helpful while maintaining accuracy and clarity.

CORE RESPONSE PRINCIPLES:
1. COMPREHENSIVENESS: Provide thorough, complete answers that fully address the user's question
2. ACCURACY: Prioritize factual correctness over speed or brevity
3. CLARITY: Use clear language, proper formatting, and logical structure
4. CITATIONS: Always cite sources when using external information
5. HONESTY: Acknowledge uncertainty or limitations when appropriate

RESPONSE STRUCTURE:
- Start with a direct answer to the main question
- Provide detailed explanation with supporting information
- Use markdown formatting: **bold** for emphasis, \`code\` for technical terms, lists for organization
- Include examples, step-by-step instructions, or code blocks when helpful
- End with a summary or next steps for complex topics

FORMATTING GUIDELINES:
- Use headers (##, ###) to organize long responses
- Use bullet points (-) or numbered lists (1., 2., 3.) for clarity
- Use code blocks (\`\`\`) for code, commands, or configuration
- Use tables when comparing multiple items
- Use blockquotes (>) for important notes or warnings

WHEN KNOWLEDGE BASE (RAG) IS PROVIDED:
CRITICAL - You MUST follow these rules:
1. PRIORITIZE knowledge base content as your PRIMARY source of truth
2. ALWAYS cite specific source files when using KB information: "According to [filename]..."
3. Quote directly from KB when appropriate: "The document states: '...'"
4. If KB contains the answer: Base your ENTIRE response on KB content
5. If KB is incomplete: Use KB for what it covers, supplement carefully with general knowledge
6. If KB doesn't contain the answer: Explicitly state "The knowledge base does not contain information about [topic]"
7. NEVER contradict information in the knowledge base
8. Start responses with: "Based on the knowledge base..." or "According to [filename]..."

WHEN WEB SEARCH RESULTS ARE PROVIDED:
CRITICAL - You MUST follow these rules:
1. INCORPORATE up-to-date information from web search results
2. ALWAYS cite sources with URLs: "According to [Source Name] ([URL])..."
3. PRIORITIZE recent and authoritative sources
4. CROSS-REFERENCE multiple sources when they agree
5. NOTE discrepancies when sources disagree
6. Synthesize information from diverse sources for comprehensive coverage
7. Include publication dates when available
8. Distinguish between news, research, documentation, and opinion sources

WHEN BOTH RAG AND WEB SEARCH ARE PROVIDED:
1. START with knowledge base information (internal, authoritative)
2. SUPPLEMENT with web search results (external, current)
3. CLEARLY distinguish: "According to our internal documentation [KB]..." vs "According to external sources [Web]..."
4. SYNTHESIZE both sources for comprehensive answers
5. RESOLVE conflicts by noting both perspectives
6. CITE ALL sources appropriately

RESPONSE DEPTH GUIDELINES:
- Simple questions: Concise but complete answers (2-4 sentences)
- Technical questions: Detailed explanations with examples and code
- Complex questions: Comprehensive responses with sections, examples, and step-by-step guidance
- Comparison questions: Structured comparisons with tables or lists
- How-to questions: Step-by-step instructions with explanations

QUALITY STANDARDS:
✓ Accuracy: Verify information against provided sources
✓ Completeness: Address all parts of the question
✓ Clarity: Use simple language, avoid jargon unless necessary
✓ Structure: Organize information logically
✓ Citations: Always attribute information to sources
✓ Helpfulness: Anticipate follow-up questions and address them
✓ Professionalism: Maintain a helpful, respectful tone

SPECIAL INSTRUCTIONS:
- For code questions: Provide working code with explanations
- For troubleshooting: Offer multiple solutions, ranked by likelihood
- For comparisons: Present balanced views with pros/cons
- For definitions: Provide clear explanations with examples
- For procedures: Give step-by-step instructions with expected outcomes

Remember: Your goal is to provide the MOST HELPFUL, ACCURATE, and COMPREHENSIVE response possible. Use all available context (knowledge base, web search) to give users complete, well-sourced answers.`;


    // Session management functions
    async function createNewSession() {
        try {
            const response = await fetch('/sessions', { method: 'POST' });
            const data = await response.json();
            currentSessionId = data.session_id;
            chatMessages.innerHTML = '';
            await loadSessions();
        } catch (error) {
            console.error('Error creating new session:', error);
        }
    }

    async function loadSessions() {
        try {
            const response = await fetch('/sessions');
            const sessions = await response.json();

            sessionsList.innerHTML = '';
            sessions.forEach(session => {
                const sessionDiv = document.createElement('div');
                sessionDiv.className = `session-item ${session.id === currentSessionId ? 'active' : ''}`;
                sessionDiv.dataset.sessionId = session.id;
                sessionDiv.dataset.sessionTitle = session.title.toLowerCase();
                sessionDiv.dataset.messageCount = session.message_count;

                sessionDiv.innerHTML = `
                    <div class="session-content">
                        <div class="session-title">${escapeHtml(session.title)}</div>
                        <div class="session-info">${session.message_count} messages</div>
                    </div>
                    <div class="session-actions">
                        <button class="session-action-btn edit" onclick="editSession('${session.id}', event)" title="Edit title">✏️</button>
                        <button class="session-action-btn export" onclick="exportSession('${session.id}', event)" title="Export chat">💾</button>
                        <button class="session-action-btn delete" onclick="deleteSession('${session.id}', event)" title="Delete chat">🗑️</button>
                    </div>
                `;

                // Add click handler to the content area only
                const contentArea = sessionDiv.querySelector('.session-content');
                contentArea.addEventListener('click', () => loadSession(session.id));

                sessionsList.appendChild(sessionDiv);
            });

            // Apply current search filter if any
            filterSessions();
        } catch (error) {
            console.error('Error loading sessions:', error);
        }
    }

    // Filter sessions based on search query
    function filterSessions() {
        const searchQuery = sessionsSearchInput.value.toLowerCase().trim();
        const sessionItems = sessionsList.querySelectorAll('.session-item');
        let visibleCount = 0;

        sessionItems.forEach(item => {
            const title = item.dataset.sessionTitle || '';
            const matches = title.includes(searchQuery);

            if (matches) {
                item.classList.remove('hidden');
                visibleCount++;
            } else {
                item.classList.add('hidden');
            }
        });

        // Show/hide "no results" message
        let noResultsDiv = sessionsList.querySelector('.no-results');
        if (visibleCount === 0 && searchQuery) {
            if (!noResultsDiv) {
                noResultsDiv = document.createElement('div');
                noResultsDiv.className = 'no-results';
                noResultsDiv.textContent = `No sessions found for "${sessionsSearchInput.value}"`;
                sessionsList.appendChild(noResultsDiv);
            } else {
                noResultsDiv.textContent = `No sessions found for "${sessionsSearchInput.value}"`;
            }
        } else if (noResultsDiv) {
            noResultsDiv.remove();
        }

        // Show/hide clear button
        if (searchQuery) {
            clearSearchButton.classList.add('visible');
        } else {
            clearSearchButton.classList.remove('visible');
        }
    }

    // Helper function to escape HTML
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    async function loadSession(sessionId) {
        try {
            const response = await fetch(`/sessions/${sessionId}`);
            const history = await response.json();
            currentSessionId = sessionId;

            chatMessages.innerHTML = '';
            history.forEach(msg => {
                if (msg.role !== 'system') {
                    appendMessage(msg.content, msg.role === 'user');
                }
            });

            await loadSessions();
        } catch (error) {
            console.error('Error loading session:', error);
        }
    }

    // Edit session title
    window.editSession = async function(sessionId, event) {
        event.stopPropagation(); // Prevent loading the session

        const sessionDiv = document.querySelector(`[data-session-id="${sessionId}"]`);
        if (!sessionDiv) return;

        const titleDiv = sessionDiv.querySelector('.session-title');
        const currentTitle = titleDiv.textContent;

        // Create input field
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'session-edit-input';
        input.value = currentTitle;

        // Create save and cancel buttons
        const actionsDiv = document.createElement('div');
        actionsDiv.className = 'session-edit-actions';

        const saveBtn = document.createElement('button');
        saveBtn.className = 'session-action-btn edit';
        saveBtn.innerHTML = '✓';
        saveBtn.title = 'Save';
        saveBtn.onclick = async (e) => {
            e.stopPropagation();
            const newTitle = input.value.trim();
            if (!newTitle) {
                alert('Title cannot be empty');
                return;
            }

            try {
                const response = await fetch(`/sessions/${sessionId}/rename`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title: newTitle })
                });

                if (!response.ok) {
                    throw new Error('Failed to rename session');
                }

                await loadSessions();
            } catch (error) {
                console.error('Error renaming session:', error);
                alert('Failed to rename session. Please try again.');
            }
        };

        const cancelBtn = document.createElement('button');
        cancelBtn.className = 'session-action-btn';
        cancelBtn.innerHTML = '✗';
        cancelBtn.title = 'Cancel';
        cancelBtn.onclick = async (e) => {
            e.stopPropagation();
            await loadSessions();
        };

        actionsDiv.appendChild(saveBtn);
        actionsDiv.appendChild(cancelBtn);

        // Replace title with input
        sessionDiv.classList.add('editing');
        const contentDiv = sessionDiv.querySelector('.session-content');
        contentDiv.insertBefore(input, titleDiv);
        contentDiv.appendChild(actionsDiv);

        // Hide original actions
        const originalActions = sessionDiv.querySelector('.session-actions');
        if (originalActions) {
            originalActions.style.display = 'none';
        }

        // Focus input and select text
        input.focus();
        input.select();

        // Handle Enter key
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                saveBtn.click();
            } else if (e.key === 'Escape') {
                cancelBtn.click();
            }
        });
    };

    // Delete session
    window.deleteSession = async function(sessionId, event) {
        event.stopPropagation(); // Prevent loading the session

        const sessionDiv = document.querySelector(`[data-session-id="${sessionId}"]`);
        const title = sessionDiv ? sessionDiv.querySelector('.session-title').textContent : 'this chat';

        const confirmed = confirm(
            `Delete chat session?\n\n` +
            `Title: ${title}\n\n` +
            `This action cannot be undone. All messages in this chat will be permanently deleted.\n\n` +
            `Click OK to delete, or Cancel to keep the chat.`
        );

        if (!confirmed) return;

        try {
            const response = await fetch(`/sessions/${sessionId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Failed to delete session');
            }

            // If we deleted the current session, create a new one
            if (sessionId === currentSessionId) {
                await createNewSession();
            } else {
                await loadSessions();
            }

            alert('✓ Chat session deleted successfully');
        } catch (error) {
            console.error('Error deleting session:', error);
            alert('Failed to delete session. Please try again.');
        }
    };

    // Export session
    window.exportSession = async function(sessionId, event) {
        event.stopPropagation(); // Prevent loading the session

        try {
            const response = await fetch(`/sessions/${sessionId}/export`);
            const data = await response.json();

            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `chat_${sessionId}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            alert('✓ Chat session exported successfully');
        } catch (error) {
            console.error('Error exporting session:', error);
            alert('Failed to export session. Please try again.');
        }
    };

    async function exportChat() {
        if (!currentSessionId) return;
        
        try {
            const response = await fetch(`/sessions/${currentSessionId}/export`);
            const data = await response.json();
            
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = `chat_export_${currentSessionId}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Error exporting chat:', error);
        }
    }

    async function importChat(file) {
        try {
            const content = await file.text();
            const data = JSON.parse(content);
            
            const response = await fetch('/sessions/import', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            currentSessionId = result.session_id;
            
            await loadSession(currentSessionId);
            await loadSessions();
        } catch (error) {
            console.error('Error importing chat:', error);
        }
    }

    // Auto-resize textarea
    function autoResizeTextarea() {
        userInput.style.height = 'auto';
        userInput.style.height = Math.min(userInput.scrollHeight, 150) + 'px';
    }

    // Initialize
    createNewSession();
    autoResizeTextarea();

    function formatTimestamp() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function showCopyFeedback() {
        const feedback = document.createElement('div');
        feedback.className = 'copy-feedback';
        feedback.textContent = 'Copied to clipboard!';
        document.body.appendChild(feedback);
        
        // Remove the feedback element after animation
        setTimeout(() => {
            document.body.removeChild(feedback);
        }, 1500);
    }

    async function copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            showCopyFeedback();
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
    }

    function formatBotMessage(content) {
        // Basic markdown-like formatting
        return content
            .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>') // Code blocks
            .replace(/`([^`]+)`/g, '<code>$1</code>') // Inline code
            .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>') // Bold
            .replace(/\*([^*]+)\*/g, '<em>$1</em>') // Italic
            .replace(/\n/g, '<br>'); // Line breaks
    }

    function appendMessage(content, isUser) {
        const container = document.createElement('div');
        container.className = isUser ? 'message-container user-message-container' : 'message-container bot-message-container';

        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'message user-message' : 'message bot-message';

        // Add message header
        const header = document.createElement('div');
        header.className = 'message-header';
        
        const avatar = document.createElement('img');
        avatar.className = 'message-avatar';
        avatar.src = isUser ? 'https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp' : 'https://www.gravatar.com/avatar/00000000000000000000000000000000?d=identicon';
        avatar.alt = isUser ? 'User' : 'Bot';
        header.appendChild(avatar);

        const name = document.createElement('span');
        name.textContent = isUser ? 'You' : 'Cerebras AI';
        header.appendChild(name);

        const timestamp = document.createElement('span');
        timestamp.className = 'message-timestamp';
        timestamp.textContent = formatTimestamp();
        header.appendChild(timestamp);

        messageDiv.appendChild(header);

        // Add message content
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        if (isUser) {
            contentDiv.textContent = content;
        } else {
            contentDiv.innerHTML = formatBotMessage(content);
        }
        messageDiv.appendChild(contentDiv);

        container.appendChild(messageDiv);

        // Add copy button
        const actions = document.createElement('div');
        actions.className = 'message-actions';
        
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 4v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7.242a2 2 0 0 0-.602-1.43L16.083 2.57A2 2 0 0 0 14.685 2H10a2 2 0 0 0-2 2z"/><path d="M16 18v2a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h2"/></svg> Copy';
        copyButton.addEventListener('click', () => copyToClipboard(content));
        actions.appendChild(copyButton);

        container.appendChild(actions);
        
        chatMessages.appendChild(container);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Show loading animation
    function showLoadingAnimation(isWebSearch = false) {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message-container bot-message-container';
        loadingDiv.id = 'loading-animation';

        const loadingMessage = document.createElement('div');
        loadingMessage.className = `loading-message ${isWebSearch ? 'web-search' : ''}`;

        // Determine loading text based on what's enabled
        let loadingText = 'Thinking';
        if (isWebSearch && ragEnabled) {
            loadingText = 'Searching web and knowledge base';
        } else if (isWebSearch) {
            loadingText = 'Searching the web';
        } else if (ragEnabled) {
            loadingText = 'Searching knowledge base';
        }

        loadingMessage.innerHTML = `
            <div class="loading-spinner">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
            <div class="loading-text">${loadingText}...</div>
        `;

        loadingDiv.appendChild(loadingMessage);
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        return loadingDiv;
    }

    // Remove loading animation
    function removeLoadingAnimation() {
        const loadingDiv = document.getElementById('loading-animation');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    }

    // Toggle thinking process visibility
    window.toggleThinking = function(header) {
        const container = header.parentElement;
        const content = container.querySelector('.thinking-content');
        const toggle = header.querySelector('.thinking-toggle');

        if (content.style.display === 'none') {
            content.style.display = 'block';
            toggle.textContent = '▲';
            header.classList.add('expanded');
        } else {
            content.style.display = 'none';
            toggle.textContent = '▼';
            header.classList.remove('expanded');
        }
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message || !currentSessionId) return;

        // Clear input
        userInput.value = '';
        autoResizeTextarea();

        // Show user message
        appendMessage(message, true);

        // Show loading animation
        const loadingDiv = showLoadingAnimation(webSearchEnabled);

        try {
            // Disable input and button while waiting for response
            userInput.disabled = true;
            sendButton.disabled = true;

            // Send request to backend with RAG and web search parameters
            const requestBody = {
                message,
                session_id: currentSessionId,
                use_rag: ragEnabled,
                kb_name: currentKnowledgeBase,
                use_web_search: webSearchEnabled
            };

            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Debug: Log the response data
            console.log('Response data:', data);
            console.log('Thinking content:', data.thinking);

            // Remove loading animation
            removeLoadingAnimation();

            // Show thinking process if available
            if (data.thinking) {
                console.log('Displaying thinking process:', data.thinking);
                const thinkingDiv = document.createElement('div');
                thinkingDiv.className = 'message-container bot-message-container';
                thinkingDiv.innerHTML = `
                    <div class="thinking-container">
                        <div class="thinking-header" onclick="toggleThinking(this)">
                            <span class="thinking-icon">🧠</span>
                            <span class="thinking-title">Thinking Process</span>
                            <span class="thinking-toggle">▼</span>
                        </div>
                        <div class="thinking-content" style="display: none;">
                            ${escapeHtml(data.thinking).replace(/\n/g, '<br>')}
                        </div>
                    </div>
                `;
                chatMessages.appendChild(thinkingDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            // Show bot response
            appendMessage(data.response, false);

            // Show RAG sources if available
            if (data.rag_sources && data.rag_sources.length > 0) {
                const sourcesDiv = document.createElement('div');
                sourcesDiv.className = 'rag-sources';
                sourcesDiv.innerHTML = `
                    <div class="sources-header">📚 Knowledge Base Sources (${data.rag_sources.length}):</div>
                    ${data.rag_sources.map((source, idx) => `
                        <div class="source-item">
                            <strong>${idx + 1}. ${source.file_name}</strong> (Score: ${source.score.toFixed(2)})
                        </div>
                    `).join('')}
                `;
                chatMessages.appendChild(sourcesDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            // Show web search results if available
            if (data.web_search_results && data.web_search_results.length > 0) {
                const webSourcesDiv = document.createElement('div');
                webSourcesDiv.className = 'web-search-sources';
                webSourcesDiv.innerHTML = `
                    <div class="sources-header">🌐 Web Sources (${data.web_search_results.length}):</div>
                    ${data.web_search_results.map((source, idx) => `
                        <div class="source-item">
                            <strong>${idx + 1}. ${source.title}</strong><br>
                            <a href="${source.url}" target="_blank">${source.url}</a>
                            ${source.published_date ? `<br><small>Published: ${source.published_date}</small>` : ''}
                        </div>
                    `).join('')}
                `;
                chatMessages.appendChild(webSourcesDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            // Update sessions list to show new message count
            await loadSessions();
        } catch (error) {
            console.error('Error:', error);

            // Remove loading animation on error
            removeLoadingAnimation();

            appendMessage('Sorry, there was an error processing your request.', false);
        } finally {
            // Re-enable input and button
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        }
    }

    async function clearChat() {
        if (!currentSessionId) return;
        
        try {
            const response = await fetch('/clear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ session_id: currentSessionId }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Clear chat messages from UI
            chatMessages.innerHTML = '';
            
            // Update sessions list
            await loadSessions();
        } catch (error) {
            console.error('Error clearing chat:', error);
        }
    }

    // Load available models
    async function loadModels() {
        try {
            const response = await fetch('/models');
            const models = await response.json();
            
            const productionGroup = document.getElementById('production-models');
            const previewGroup = document.getElementById('preview-models');
            
            // Clear existing options
            productionGroup.innerHTML = '';
            previewGroup.innerHTML = '';
            
            // Add production models
            models.production.forEach(model => {
                const option = document.createElement('option');
                option.value = model.id;
                option.textContent = model.name;
                option.dataset.parameters = model.parameters;
                option.dataset.speed = model.speed;
                option.dataset.type = 'production';
                productionGroup.appendChild(option);
            });
            
            // Add preview models
            models.preview.forEach(model => {
                const option = document.createElement('option');
                option.value = model.id;
                option.textContent = model.name;
                option.dataset.parameters = model.parameters;
                option.dataset.speed = model.speed;
                option.dataset.type = 'preview';
                previewGroup.appendChild(option);
            });
        } catch (error) {
            console.error('Error loading models:', error);
        }
    }

    // Update model info display
    function updateModelInfo(modelSelect) {
        const selectedOption = modelSelect.selectedOptions[0];
        const modelInfo = document.getElementById('model-info');
        
        if (selectedOption) {
            const type = selectedOption.dataset.type === 'production' ? 'Production' : 'Preview';
            modelInfo.innerHTML = `
                <p><span class="label">Type:</span> ${type}</p>
                <p><span class="label">Parameters:</span> ${selectedOption.dataset.parameters}</p>
                <p><span class="label">Speed:</span> ${selectedOption.dataset.speed} tokens/s</p>
                ${type === 'preview' ? '<p class="warning">⚠️ Preview model - Not recommended for production use</p>' : ''}
            `;
        } else {
            modelInfo.innerHTML = '';
        }
    }

    // Load settings when page loads
    async function loadSettings() {
        try {
            const response = await fetch('/settings');
            const settings = await response.json();

            await loadModels(); // Load models first

            document.getElementById('model').value = settings.model;

            // Always show the current system prompt from settings
            // If it's empty or the old default, use the new comprehensive default
            const systemPrompt = settings.system_prompt;
            if (!systemPrompt ||
                systemPrompt.trim() === '' ||
                systemPrompt === 'You are a helpful assistant.' ||
                systemPrompt === 'You are a helpful AI assistant.') {
                // Old or empty prompt - upgrade to new comprehensive default
                document.getElementById('system-prompt').value = DEFAULT_SYSTEM_PROMPT;
                // Auto-save the new default
                setTimeout(() => {
                    console.log('Auto-upgrading to new comprehensive system prompt');
                }, 100);
            } else {
                // Show whatever is currently saved (could be default or custom)
                document.getElementById('system-prompt').value = systemPrompt;
            }

            document.getElementById('temperature').value = settings.temperature;
            document.getElementById('max-tokens').value = settings.max_tokens;
            temperatureValue.textContent = settings.temperature;

            // Update model info for the current model
            updateModelInfo(document.getElementById('model'));
        } catch (error) {
            console.error('Error loading settings:', error);
        }
    }

    // Save settings
    async function saveSettings(event) {
        event.preventDefault();
        
        const settings = {
            model: document.getElementById('model').value,
            system_prompt: document.getElementById('system-prompt').value,
            temperature: parseFloat(document.getElementById('temperature').value),
            max_tokens: parseInt(document.getElementById('max-tokens').value)
        };

        try {
            const response = await fetch('/settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(settings)
            });

            if (!response.ok) {
                throw new Error('Failed to save settings');
            }

            settingsPanel.classList.remove('active');
        } catch (error) {
            console.error('Error saving settings:', error);
            alert('Failed to save settings. Please try again.');
        }
    }

    // Reset system prompt to default
    function resetSystemPromptToDefault() {
        if (systemPromptInput) {
            // Show confirmation dialog
            const confirmed = confirm(
                'Reset system prompt to default?\n\n' +
                'This will replace your current system prompt with the comprehensive default prompt.\n\n' +
                'Your current custom prompt will be lost unless you save it elsewhere first.\n\n' +
                'Click OK to reset, or Cancel to keep your current prompt.'
            );

            if (confirmed) {
                systemPromptInput.value = DEFAULT_SYSTEM_PROMPT;
                alert('✓ System prompt reset to comprehensive default!\n\nDon\'t forget to click "Save Settings" to save this change.');

                // Scroll to top of textarea to show the beginning
                systemPromptInput.scrollTop = 0;
            }
        }
    }

    // Reset settings
    async function resetSettingsToDefault() {
        if (!confirm('Reset all settings to default? This will also reset the system prompt.')) {
            return;
        }

        try {
            const response = await fetch('/settings/reset', {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error('Failed to reset settings');
            }

            const settings = await response.json();
            document.getElementById('model').value = settings.model;
            document.getElementById('system-prompt').value = DEFAULT_SYSTEM_PROMPT;
            document.getElementById('temperature').value = settings.temperature;
            document.getElementById('max-tokens').value = settings.max_tokens;
            temperatureValue.textContent = settings.temperature;

            alert('Settings reset to default');
        } catch (error) {
            console.error('Error resetting settings:', error);
            alert('Failed to reset settings. Please try again.');
        }
    }

    // Update temperature value display
    temperatureInput.addEventListener('input', (e) => {
        temperatureValue.textContent = e.target.value;
    });

    // Toggle settings panel
    toggleSettings.addEventListener('click', () => {
        settingsPanel.classList.toggle('active');
    });

    // Event listeners
    settingsForm.addEventListener('submit', saveSettings);
    resetSettings.addEventListener('click', resetSettingsToDefault);
    if (resetSystemPrompt) {
        resetSystemPrompt.addEventListener('click', resetSystemPromptToDefault);
    }
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    userInput.addEventListener('input', autoResizeTextarea);
    clearButton.addEventListener('click', clearChat);
    
    // Session management listeners
    toggleSessions.addEventListener('click', () => {
        sessionsPanel.classList.toggle('active');
    });
    
    newChatButton.addEventListener('click', createNewSession);
    
    exportChatButton.addEventListener('click', exportChat);
    
    importChatButton.addEventListener('click', () => {
        importFileInput.click();
    });
    
    importFileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            importChat(e.target.files[0]);
            e.target.value = ''; // Reset file input
        }
    });
    
    // Close panels when clicking outside
    document.addEventListener('click', (e) => {
        if (!sessionsPanel.contains(e.target) && e.target !== toggleSessions) {
            sessionsPanel.classList.remove('active');
        }
    });
    document.getElementById('model').addEventListener('change', (e) => {
        updateModelInfo(e.target);
    });

    // ============================================================================
    // RAG Functions
    // ============================================================================

    async function checkRAGStatus() {
        try {
            const response = await fetch('/rag/status');
            const status = await response.json();
            return status.available;
        } catch (error) {
            console.error('Error checking RAG status:', error);
            return false;
        }
    }

    async function loadKnowledgeBases() {
        try {
            const response = await fetch('/knowledge-bases');
            const kbs = await response.json();

            const kbSelect = document.getElementById('kb-select');
            if (kbSelect) {
                kbSelect.innerHTML = '<option value="">None (No RAG)</option>';
                kbs.forEach(kb => {
                    const option = document.createElement('option');
                    option.value = kb.name;
                    option.textContent = `${kb.name} (${kb.vectors_count} chunks)`;
                    kbSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading knowledge bases:', error);
        }
    }

    async function createKnowledgeBase(name) {
        try {
            const response = await fetch('/knowledge-bases', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name })
            });

            if (response.ok) {
                await loadKnowledgeBases();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Error creating knowledge base:', error);
            return false;
        }
    }

    async function uploadFileToKB(file, kbName) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`/knowledge-bases/${kbName}/upload`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                console.log('File uploaded:', data);
                await loadKnowledgeBases();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Error uploading file:', error);
            return false;
        }
    }

    // Knowledge Base Management Modal
    const kbModal = document.getElementById('kb-modal');
    const manageKBButton = document.getElementById('manage-kb-button');
    const closeKBModal = document.getElementById('close-kb-modal');
    const createKBButton = document.getElementById('create-kb-button');
    const uploadFilesButton = document.getElementById('upload-files-button');
    const newKBNameInput = document.getElementById('new-kb-name');
    const fileUploadInput = document.getElementById('file-upload');
    const uploadKBSelect = document.getElementById('upload-kb-select');
    const uploadStatus = document.getElementById('upload-status');
    const kbList = document.getElementById('kb-list');

    if (manageKBButton) {
        manageKBButton.addEventListener('click', () => {
            kbModal.style.display = 'block';
            loadKnowledgeBasesForModal();
        });
    }

    if (closeKBModal) {
        closeKBModal.addEventListener('click', () => {
            kbModal.style.display = 'none';
        });
    }

    window.addEventListener('click', (e) => {
        if (e.target === kbModal) {
            kbModal.style.display = 'none';
        }
    });

    if (createKBButton) {
        createKBButton.addEventListener('click', async () => {
            const name = newKBNameInput.value.trim();
            if (!name) {
                alert('Please enter a knowledge base name');
                return;
            }

            const success = await createKnowledgeBase(name);
            if (success) {
                newKBNameInput.value = '';
                await loadKnowledgeBasesForModal();
                alert(`Knowledge base "${name}" created successfully`);
            } else {
                alert('Failed to create knowledge base');
            }
        });
    }

    if (uploadFilesButton) {
        uploadFilesButton.addEventListener('click', async () => {
            const kbName = uploadKBSelect.value;
            const files = fileUploadInput.files;

            if (!kbName) {
                alert('Please select a knowledge base');
                return;
            }

            if (files.length === 0) {
                alert('Please select files to upload');
                return;
            }

            uploadStatus.innerHTML = 'Uploading...';
            let successCount = 0;

            for (let i = 0; i < files.length; i++) {
                const success = await uploadFileToKB(files[i], kbName);
                if (success) successCount++;
            }

            uploadStatus.innerHTML = `Uploaded ${successCount} of ${files.length} files`;
            fileUploadInput.value = '';

            setTimeout(() => {
                uploadStatus.innerHTML = '';
            }, 3000);
        });
    }

    async function loadKnowledgeBasesForModal() {
        try {
            const response = await fetch('/knowledge-bases');
            const kbs = await response.json();

            // Also update quick select
            loadQuickKnowledgeBases();

            // Update upload KB select
            uploadKBSelect.innerHTML = '<option value="">Select knowledge base...</option>';
            kbs.forEach(kb => {
                const option = document.createElement('option');
                option.value = kb.name;
                option.textContent = kb.name;
                uploadKBSelect.appendChild(option);
            });

            // Update KB list
            kbList.innerHTML = '';
            if (kbs.length === 0) {
                kbList.innerHTML = '<p>No knowledge bases yet. Create one above.</p>';
            } else {
                kbs.forEach(kb => {
                    const kbDiv = document.createElement('div');
                    kbDiv.className = 'kb-item';
                    kbDiv.innerHTML = `
                        <strong>${kb.name}</strong> - ${kb.vectors_count} chunks
                        <button class="delete-kb-btn" data-kb="${kb.name}">Delete</button>
                    `;
                    kbList.appendChild(kbDiv);
                });

                // Add delete listeners
                document.querySelectorAll('.delete-kb-btn').forEach(btn => {
                    btn.addEventListener('click', async (e) => {
                        const kbName = e.target.dataset.kb;
                        if (confirm(`Are you sure you want to delete "${kbName}"?`)) {
                            const response = await fetch(`/knowledge-bases/${kbName}`, {
                                method: 'DELETE'
                            });
                            if (response.ok) {
                                await loadKnowledgeBasesForModal();
                                await loadKnowledgeBases();
                            }
                        }
                    });
                });
            }
        } catch (error) {
            console.error('Error loading knowledge bases for modal:', error);
        }
    }

    // ============================================================================
    // Quick Toggle Buttons
    // ============================================================================

    const quickRagToggle = document.getElementById('quick-rag-toggle');
    const quickWebSearchToggle = document.getElementById('quick-web-search-toggle');
    const quickKbSelect = document.getElementById('quick-kb-select');
    const ragStatusIndicator = document.getElementById('rag-status-indicator');
    const webSearchStatusIndicator = document.getElementById('web-search-status-indicator');
    const ragToggleGroup = document.getElementById('rag-toggle-group');
    const webSearchToggleGroup = document.getElementById('web-search-toggle-group');

    // Update status indicators
    function updateRAGStatus() {
        if (quickRagToggle) {
            if (ragEnabled && currentKnowledgeBase) {
                quickRagToggle.classList.add('active');
                ragStatusIndicator.textContent = 'ON';
                quickKbSelect.disabled = false;
            } else {
                quickRagToggle.classList.remove('active');
                ragStatusIndicator.textContent = 'OFF';
                if (!currentKnowledgeBase) {
                    quickKbSelect.disabled = false;
                }
            }
        }
    }

    function updateWebSearchStatus() {
        if (quickWebSearchToggle) {
            if (webSearchEnabled) {
                quickWebSearchToggle.classList.add('active');
                webSearchStatusIndicator.textContent = 'ON';
            } else {
                quickWebSearchToggle.classList.remove('active');
                webSearchStatusIndicator.textContent = 'OFF';
            }
        }
    }

    // Quick RAG toggle handler
    if (quickRagToggle) {
        quickRagToggle.addEventListener('click', () => {
            if (!currentKnowledgeBase) {
                alert('Please select a knowledge base first');
                return;
            }
            ragEnabled = !ragEnabled;
            updateRAGStatus();

            // Sync with settings panel
            const settingsRagToggle = document.getElementById('rag-toggle');
            if (settingsRagToggle) {
                settingsRagToggle.checked = ragEnabled;
            }
        });
    }

    // Quick KB select handler
    if (quickKbSelect) {
        quickKbSelect.addEventListener('change', (e) => {
            currentKnowledgeBase = e.target.value || null;

            // Auto-enable RAG when KB is selected
            if (currentKnowledgeBase && !ragEnabled) {
                ragEnabled = true;
            } else if (!currentKnowledgeBase) {
                ragEnabled = false;
            }

            updateRAGStatus();

            // Sync with settings panel
            const settingsKbSelect = document.getElementById('kb-select');
            if (settingsKbSelect) {
                settingsKbSelect.value = currentKnowledgeBase || '';
            }
            const settingsRagToggle = document.getElementById('rag-toggle');
            if (settingsRagToggle) {
                settingsRagToggle.checked = ragEnabled;
            }
        });
    }

    // Quick web search toggle handler
    if (quickWebSearchToggle) {
        quickWebSearchToggle.addEventListener('click', () => {
            webSearchEnabled = !webSearchEnabled;
            updateWebSearchStatus();

            // Sync with settings panel
            const settingsWebSearchToggle = document.getElementById('web-search-toggle');
            if (settingsWebSearchToggle) {
                settingsWebSearchToggle.checked = webSearchEnabled;
            }
        });
    }

    // Load knowledge bases into quick select
    async function loadQuickKnowledgeBases() {
        try {
            const response = await fetch('/knowledge-bases');
            const kbs = await response.json();

            if (quickKbSelect) {
                quickKbSelect.innerHTML = '<option value="">Select KB...</option>';
                kbs.forEach(kb => {
                    const option = document.createElement('option');
                    option.value = kb.name;
                    option.textContent = `${kb.name} (${kb.vectors_count})`;
                    quickKbSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading knowledge bases for quick select:', error);
        }
    }

    // Initialize RAG UI if available
    checkRAGStatus().then(available => {
        if (available) {
            console.log('RAG features available');
            loadKnowledgeBases();
            loadQuickKnowledgeBases();

            // Show quick toggle
            if (ragToggleGroup) {
                ragToggleGroup.style.display = 'flex';
            }

            // Add RAG toggle listener (settings panel)
            const ragToggle = document.getElementById('rag-toggle');
            if (ragToggle) {
                ragToggle.addEventListener('change', (e) => {
                    ragEnabled = e.target.checked;
                    updateRAGStatus();
                });
            }

            // Add KB selection listener (settings panel)
            const kbSelect = document.getElementById('kb-select');
            if (kbSelect) {
                kbSelect.addEventListener('change', (e) => {
                    currentKnowledgeBase = e.target.value || null;
                    updateRAGStatus();

                    // Sync with quick select
                    if (quickKbSelect) {
                        quickKbSelect.value = currentKnowledgeBase || '';
                    }
                });
            }
        } else {
            console.log('RAG features not available');
        }
    });

    // Initialize Web Search UI
    async function checkWebSearchStatus() {
        try {
            const response = await fetch('/web-search/status');
            const status = await response.json();
            return status.available;
        } catch (error) {
            console.error('Error checking web search status:', error);
            return false;
        }
    }

    checkWebSearchStatus().then(available => {
        if (available) {
            console.log('Web search features available');

            // Show quick toggle
            if (webSearchToggleGroup) {
                webSearchToggleGroup.style.display = 'flex';
            }

            // Add web search toggle listener (settings panel)
            const webSearchToggle = document.getElementById('web-search-toggle');
            if (webSearchToggle) {
                webSearchToggle.addEventListener('change', (e) => {
                    webSearchEnabled = e.target.checked;
                    updateWebSearchStatus();
                });
            }
        } else {
            console.log('Web search features not available');
            // Hide web search toggle if not available
            const webSearchToggle = document.getElementById('web-search-toggle');
            if (webSearchToggle && webSearchToggle.parentElement) {
                webSearchToggle.parentElement.style.display = 'none';
            }
        }
    });

    // Sessions search functionality
    sessionsSearchInput.addEventListener('input', () => {
        filterSessions();
    });

    // Clear search button
    clearSearchButton.addEventListener('click', () => {
        sessionsSearchInput.value = '';
        filterSessions();
        sessionsSearchInput.focus();
    });

    // Allow Enter key to focus first result
    sessionsSearchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const firstVisible = sessionsList.querySelector('.session-item:not(.hidden)');
            if (firstVisible) {
                const contentArea = firstVisible.querySelector('.session-content');
                if (contentArea) {
                    contentArea.click();
                }
            }
        }
    });

    // Load settings when page loads
    loadSettings();
});