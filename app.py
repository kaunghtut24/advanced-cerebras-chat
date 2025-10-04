import os
import json
import signal
import sys
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Environment variables loaded from .env file")
except ImportError:
    print("python-dotenv not installed. Install with: pip install python-dotenv")
except Exception as e:
    print(f"Could not load .env file: {e}")

# Import RAG services
try:
    from rag_service import rag_service
    from file_handler import file_handler
    RAG_AVAILABLE = True
    print(f"RAG service initialized: {'Available' if rag_service.is_available() else 'Not available'}")
except ImportError as e:
    RAG_AVAILABLE = False
    print(f"RAG services not available: {e}")

# Import Web Search service
try:
    from web_search_service import web_search_service
    WEB_SEARCH_AVAILABLE = True
    print(f"Web search initialized: {'Available' if web_search_service.is_available() else 'Not available'}")
except ImportError as e:
    WEB_SEARCH_AVAILABLE = False
    print(f"Web search not available: {e}")

# Configure logging
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# ============================================================================
# Directory Configuration
# ============================================================================

# Chat history storage directory
CHAT_HISTORY_DIR = 'chat_sessions'

# Create chat history directory if it doesn't exist
if not os.path.exists(CHAT_HISTORY_DIR):
    os.makedirs(CHAT_HISTORY_DIR)
    logging.info(f"Created chat history directory: {CHAT_HISTORY_DIR}")

# Configuration from environment variables
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

# Configure CORS with more specific settings
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure rate limiting
default_limits_str = os.environ.get('RATE_LIMIT_DEFAULT', '200 per day, 50 per hour')
default_limits = [limit.strip() for limit in default_limits_str.split(',')]
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=default_limits,
    storage_uri=os.environ.get('RATE_LIMIT_STORAGE', 'memory://')
)

# Available models configuration
CEREBRAS_MODELS = {
    "production": [
        {
            "name": "Llama 4 Scout",
            "id": "llama-4-scout-17b-16e-instruct",
            "parameters": "109 billion",
            "speed": "~2600"
        },
        {
            "name": "Llama 3.1 8B",
            "id": "llama3.1-8b",
            "parameters": "8 billion",
            "speed": "~2200"
        },
        {
            "name": "Llama 3.3 70B",
            "id": "llama-3.3-70b",
            "parameters": "70 billion",
            "speed": "~2100"
        },
        {
            "name": "OpenAI GPT OSS",
            "id": "gpt-oss-120b",
            "parameters": "120 billion",
            "speed": "~3000"
        },
        {
            "name": "Qwen 3 32B",
            "id": "qwen-3-32b",
            "parameters": "32 billion",
            "speed": "~2600"
        }
    ],
    "preview": [
        {
            "name": "Llama 4 Maverick",
            "id": "llama-4-maverick-17b-128e-instruct",
            "parameters": "400 billion",
            "speed": "~2400"
        },
        {
            "name": "Qwen 3 235B Instruct",
            "id": "qwen-3-235b-a22b-instruct-2507",
            "parameters": "235 billion",
            "speed": "~1400"
        },
        {
            "name": "Qwen 3 235B Thinking",
            "id": "qwen-3-235b-a22b-thinking-2507",
            "parameters": "235 billion",
            "speed": "~1700"
        },
        {
            "name": "Qwen 3 480B Coder",
            "id": "qwen-3-coder-480b",
            "parameters": "480 billion",
            "speed": "~2000"
        }
    ]
}

# Default comprehensive system prompt
DEFAULT_SYSTEM_PROMPT = """You are an advanced AI assistant powered by Cerebras, designed to provide comprehensive, accurate, and well-structured responses. Your primary goal is to be maximally helpful while maintaining accuracy and clarity.

CORE RESPONSE PRINCIPLES:
1. COMPREHENSIVENESS: Provide thorough, complete answers that fully address the user's question
2. ACCURACY: Prioritize factual correctness over speed or brevity
3. CLARITY: Use clear language, proper formatting, and logical structure
4. CITATIONS: Always cite sources when using external information
5. HONESTY: Acknowledge uncertainty or limitations when appropriate

RESPONSE STRUCTURE:
- Start with a direct answer to the main question
- Provide detailed explanation with supporting information
- Use markdown formatting: **bold** for emphasis, `code` for technical terms, lists for organization
- Include examples, step-by-step instructions, or code blocks when helpful
- End with a summary or next steps for complex topics

FORMATTING GUIDELINES:
- Use headers (##, ###) to organize long responses
- Use bullet points (-) or numbered lists (1., 2., 3.) for clarity
- Use code blocks (```) for code, commands, or configuration
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

Remember: Your goal is to provide the MOST HELPFUL, ACCURATE, and COMPREHENSIVE response possible. Use all available context (knowledge base, web search) to give users complete, well-sourced answers."""

# Default settings
DEFAULT_SETTINGS = {
    "model": "llama-4-scout-17b-16e-instruct",
    "system_prompt": DEFAULT_SYSTEM_PROMPT,
    "temperature": 0.7,
    "max_tokens": 1000
}

# Settings file path
SETTINGS_FILE = os.path.join(CHAT_HISTORY_DIR, 'settings.json')

# Load or create settings
def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except:
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)

# Initialize settings
current_settings = load_settings()

# Try to initialize the Cerebras client, but handle the case where it's not available or API key is missing
cerebras_available = False
client = None
try:
    from cerebras.cloud.sdk import Cerebras
    api_key = os.environ.get("CEREBRAS_API_KEY")
    if api_key:
        client = Cerebras(api_key=api_key)
        cerebras_available = True
        print("Cerebras SDK initialized successfully.")
    else:
        print("CEREBRAS_API_KEY environment variable not set. Running in mock mode.")
except ImportError:
    print("Cerebras SDK not available. Running in mock mode.")

# Chat history storage functions
def load_chat_history(session_id):
    try:
        history_file = os.path.join(CHAT_HISTORY_DIR, f'chat_history_{session_id}.json')
        with open(history_file, 'r') as f:
            return json.load(f)
    except:
        return []

def save_chat_history(session_id, history):
    history_file = os.path.join(CHAT_HISTORY_DIR, f'chat_history_{session_id}.json')
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)

def list_chat_sessions():
    import glob
    sessions = []
    pattern = os.path.join(CHAT_HISTORY_DIR, 'chat_history_*.json')
    for file in glob.glob(pattern):
        session_id = os.path.basename(file).replace('chat_history_', '').replace('.json', '')
        try:
            # Load chat history
            with open(file, 'r') as f:
                history = json.load(f)

            # Check for custom title in metadata file
            metadata_file = os.path.join(CHAT_HISTORY_DIR, f'chat_metadata_{session_id}.json')
            custom_title = None
            if os.path.exists(metadata_file):
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                        custom_title = metadata.get('title')
                except:
                    pass

            # Use custom title if available, otherwise use first message
            if custom_title:
                title = custom_title
            else:
                first_msg = next((msg for msg in history if msg['role'] == 'user'), None)
                title = first_msg['content'][:50] + '...' if first_msg else 'New Chat'

            sessions.append({
                'id': session_id,
                'timestamp': session_id.split('_')[0],
                'title': title,
                'message_count': len(history)
            })
        except:
            continue
    return sorted(sessions, key=lambda x: x['timestamp'], reverse=True)

# In-memory storage for active conversations
active_conversations = {}

# Limit conversation history to prevent overly long contexts
MAX_HISTORY_LENGTH = int(os.environ.get('MAX_HISTORY_LENGTH', 20))  # Configurable from environment

@app.route('/models', methods=['GET'])
def get_models():
    return jsonify(CEREBRAS_MODELS)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings', methods=['GET'])
def get_settings():
    return jsonify(current_settings)

@app.route('/settings', methods=['POST'])
def update_settings():
    global current_settings
    new_settings = request.json
    
    # Validate required fields
    required_fields = ["model", "system_prompt", "temperature", "max_tokens"]
    for field in required_fields:
        if field not in new_settings:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Update settings
    current_settings.update(new_settings)
    save_settings(current_settings)
    return jsonify(current_settings)

@app.route('/settings/reset', methods=['POST'])
def reset_settings():
    global current_settings
    current_settings = DEFAULT_SETTINGS.copy()
    save_settings(current_settings)
    return jsonify(current_settings)

@app.route('/chat', methods=['POST'])
@limiter.limit(os.environ.get('RATE_LIMIT_CHAT', '30 per minute'))  # Configurable chat rate limit
def chat():
    global client, cerebras_available
    logging.info(f"Chat request received from {request.remote_addr}")
    
    if not request.json or 'message' not in request.json or 'session_id' not in request.json:
        return jsonify({"error": "Invalid request format"}), 400
    
    session_id = request.json['session_id']
    if session_id not in active_conversations:
        active_conversations[session_id] = load_chat_history(session_id)
    
    user_message = request.json['message']
    conversation_history = active_conversations[session_id]
    kb_name = request.json.get('kb_name', None)  # Optional knowledge base for RAG
    use_rag = request.json.get('use_rag', False)  # Enable/disable RAG
    use_web_search = request.json.get('use_web_search', False)  # Enable/disable web search
    web_search_query = request.json.get('web_search_query', user_message)  # Custom search query or use message

    # Add user message to conversation history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # RAG: Retrieve relevant context if enabled
    rag_context = ""
    rag_sources = []
    if use_rag and kb_name and RAG_AVAILABLE and rag_service.is_available():
        logging.info(f"RAG enabled: Searching knowledge base '{kb_name}' for query: '{user_message}'")
        try:
            search_results = rag_service.search(kb_name, user_message)
            if search_results:
                rag_sources = search_results
                context_parts = [f"[Source: {r['file_name']}]\n{r['text']}" for r in search_results]
                rag_context = "\n\n".join(context_parts)
                logging.info(f"✓ RAG: Retrieved {len(search_results)} relevant chunks from '{kb_name}'")
                logging.info(f"✓ RAG: Context length: {len(rag_context)} characters")
                logging.info(f"✓ RAG: Sources: {', '.join(set(r['file_name'] for r in search_results))}")
            else:
                logging.warning(f"⚠ RAG: No results found in knowledge base '{kb_name}' for query")
        except Exception as e:
            logging.error(f"✗ RAG retrieval failed: {e}")
    elif use_rag:
        if not kb_name:
            logging.warning("⚠ RAG enabled but no knowledge base selected")
        elif not RAG_AVAILABLE:
            logging.warning("⚠ RAG enabled but RAG service not available")
        elif not rag_service.is_available():
            logging.warning("⚠ RAG enabled but RAG service not initialized")

    # Web Search: Retrieve web content if enabled
    web_search_context = ""
    web_search_results = []
    if use_web_search and WEB_SEARCH_AVAILABLE and web_search_service.is_available():
        try:
            search_results = web_search_service.search(web_search_query)
            if search_results:
                web_search_results = search_results
                web_search_context = web_search_service.format_search_context(search_results)
                logging.info(f"Retrieved {len(search_results)} web search results")
        except Exception as e:
            logging.error(f"Web search failed: {e}")

    # Limit conversation history length and remove any old system messages
    # System messages should not be in conversation history - we add them fresh each time
    conversation_history = [msg for msg in conversation_history if msg['role'] != 'system']

    if len(conversation_history) > MAX_HISTORY_LENGTH:
        # Keep only the most recent messages
        conversation_history = conversation_history[-MAX_HISTORY_LENGTH:]

    if cerebras_available and client:
        try:
            # Prepare system prompt - start with base prompt
            system_prompt = current_settings["system_prompt"]

            # Add current date/time information for context
            from datetime import datetime
            current_date = datetime.now().strftime("%B %d, %Y")
            current_time = datetime.now().strftime("%I:%M %p")
            current_datetime_full = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p %Z")

            # Prepend date information to system prompt
            system_prompt = f"""CURRENT DATE AND TIME INFORMATION:
Today's date: {current_date}
Current time: {current_time}
Full date/time: {current_datetime_full}

IMPORTANT: When searching the web or providing information about current events, news, or time-sensitive topics, use this date as reference. This helps you provide the most up-to-date and relevant information.

{system_prompt}
"""

            # CRITICAL: Add RAG context if available
            if rag_context:
                # Override with RAG-specific instructions
                system_prompt += f"""

{'='*80}
🔴 CRITICAL - KNOWLEDGE BASE CONTEXT PROVIDED 🔴
{'='*80}

You have been provided with KNOWLEDGE BASE CONTEXT below. This is MANDATORY reading.

ABSOLUTE REQUIREMENTS:
1. READ the entire knowledge base context below carefully
2. Your PRIMARY obligation is to answer based on this knowledge base
3. You MUST cite source files: "According to [filename]..." or "Based on [filename]..."
4. You MUST quote directly when appropriate: "The document states: '...'"
5. If the KB answers the question: Use ONLY KB content (do not add external knowledge)
6. If the KB partially answers: Use KB first, then supplement with general knowledge (clearly labeled)
7. If the KB doesn't answer: State "The knowledge base does not contain information about this topic" then provide general knowledge

RESPONSE FORMAT WHEN USING KB:
- Start with: "Based on the knowledge base..." or "According to [filename]..."
- Cite every piece of information: "As stated in [filename]..."
- Quote key passages: "The document states: '...'"
- End with: "Source: [list of files used]"

{'='*80}
📚 KNOWLEDGE BASE CONTEXT - READ THIS CAREFULLY:
{'='*80}

{rag_context}

{'='*80}
END OF KNOWLEDGE BASE CONTEXT
{'='*80}

REMINDER: The above knowledge base context is your PRIMARY source. Use it first and foremost.
"""

            # Add web search context if available
            if web_search_context:
                system_prompt += f"""

{'='*80}
🌐 WEB SEARCH RESULTS PROVIDED 🌐
{'='*80}

You have been provided with CURRENT WEB SEARCH RESULTS below.

REQUIREMENTS FOR WEB SEARCH:
1. INCORPORATE up-to-date information from these results
2. CITE every source with URL: "According to [Source] ([URL])..."
3. PRIORITIZE recent and authoritative sources
4. CROSS-REFERENCE when multiple sources agree
5. NOTE when sources disagree or provide different perspectives
6. SYNTHESIZE information from multiple sources for comprehensive answers
7. Include publication dates when available

RESPONSE FORMAT WHEN USING WEB SEARCH:
- Cite with URLs: "According to TechCrunch (https://...)..."
- Note source types: "According to research from MIT..." vs "According to news from BBC..."
- Synthesize: "Multiple sources (Source1, Source2, Source3) confirm that..."
- End with: "Sources: [list with URLs]"

{'='*80}
🔍 WEB SEARCH RESULTS - READ THIS CAREFULLY:
{'='*80}

{web_search_context}

{'='*80}
END OF WEB SEARCH RESULTS
{'='*80}

REMINDER: Use these web search results to provide current, comprehensive information.
"""

            # If both RAG and Web Search are provided
            if rag_context and web_search_context:
                system_prompt += f"""

{'='*80}
⚡ BOTH KNOWLEDGE BASE AND WEB SEARCH PROVIDED ⚡
{'='*80}

You have BOTH internal knowledge base AND external web search results.

SYNTHESIS REQUIREMENTS:
1. START with knowledge base (internal, authoritative for your organization)
2. SUPPLEMENT with web search (external, current, broader context)
3. CLEARLY distinguish sources:
   - "According to our internal documentation [filename]..."
   - "According to external sources [Source Name] ([URL])..."
4. SYNTHESIZE for comprehensive answers
5. RESOLVE conflicts by presenting both perspectives
6. CITE ALL sources (both KB files and web URLs)

RESPONSE STRUCTURE:
1. Internal Knowledge: "Based on our knowledge base [filename]..."
2. External Context: "According to external sources [URL]..."
3. Synthesis: "Combining internal documentation with current information..."
4. Sources: "Internal: [files], External: [URLs]"

{'='*80}
"""

            # Prepare messages with system prompt (no system messages in conversation_history)
            messages = [{"role": "system", "content": system_prompt}] + conversation_history

            # Log what we're sending to the model
            logging.info(f"Sending to model: {len(messages)} messages (1 system + {len(conversation_history)} history)")
            if rag_context:
                logging.info(f"✓ System prompt includes RAG context ({len(rag_context)} chars)")
            if web_search_context:
                logging.info(f"✓ System prompt includes web search context ({len(web_search_context)} chars)")

            # Call the Cerebras API with the conversation history and settings
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=current_settings["model"],
                temperature=current_settings["temperature"],
                max_tokens=current_settings["max_tokens"]
            )
            
            # Extract the response content
            bot_response = chat_completion.choices[0].message.content
            
            # Add bot response to conversation history
            conversation_history.append({
                "role": "assistant",
                "content": bot_response
            })
            
            # Save updated conversation history
            active_conversations[session_id] = conversation_history
            save_chat_history(session_id, conversation_history)

            # Return the response as JSON
            response_data = {
                "response": bot_response,
                "history": conversation_history
            }

            # Include RAG sources if available
            if rag_sources:
                response_data["rag_sources"] = rag_sources
                response_data["rag_enabled"] = True

            # Include web search results if available
            if web_search_results:
                response_data["web_search_results"] = web_search_results
                response_data["web_search_enabled"] = True

            return jsonify(response_data)
        except Exception as e:
            # Handle any errors that occur during the API call
            error_message = f"Error: {str(e)}"
            return jsonify({"response": error_message}), 500
    else:
        # Mock response when Cerebras is not available
        mock_responses = [
            "I'm running in mock mode because the Cerebras API key is not set. In a real implementation, I would connect to the Cerebras model to generate a response.",
            "This is a mock response. To use the actual Cerebras models, please set the CEREBRAS_API_KEY environment variable.",
            "Mock mode: I would normally use the Cerebras API to answer your question, but I'm providing a mock response instead."
        ]
        
        # Add a mock response to conversation history
        mock_response = mock_responses[len(conversation_history) % len(mock_responses)]
        conversation_history.append({
            "role": "assistant",
            "content": mock_response
        })
        
        # Save updated conversation history
        active_conversations[session_id] = conversation_history
        save_chat_history(session_id, conversation_history)
        
        # Return the mock response as JSON
        return jsonify({
            "response": mock_response,
            "history": conversation_history
        })

@app.route('/sessions', methods=['GET'])
def get_sessions():
    return jsonify(list_chat_sessions())

@app.route('/sessions', methods=['POST'])
def create_session():
    from datetime import datetime
    session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    active_conversations[session_id] = []
    return jsonify({"session_id": session_id})

@app.route('/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    if session_id not in active_conversations:
        active_conversations[session_id] = load_chat_history(session_id)
    return jsonify(active_conversations[session_id])

@app.route('/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    if session_id in active_conversations:
        del active_conversations[session_id]
    try:
        # Delete chat history file
        history_file = os.path.join(CHAT_HISTORY_DIR, f'chat_history_{session_id}.json')
        if os.path.exists(history_file):
            os.remove(history_file)

        # Delete metadata file if exists
        metadata_file = os.path.join(CHAT_HISTORY_DIR, f'chat_metadata_{session_id}.json')
        if os.path.exists(metadata_file):
            os.remove(metadata_file)
    except Exception as e:
        logging.error(f"Error deleting session files: {e}")
    return jsonify({"status": "success"})

@app.route('/sessions/<session_id>/rename', methods=['POST'])
def rename_session(session_id):
    """Rename a chat session by updating its title in the metadata"""
    data = request.json
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400

    new_title = data['title'].strip()
    if not new_title:
        return jsonify({"error": "Title cannot be empty"}), 400

    # Load the session history
    if session_id in active_conversations:
        history = active_conversations[session_id]
    else:
        history = load_chat_history(session_id)

    # Save with updated metadata (the title will be used when listing sessions)
    # We'll store the custom title in a separate metadata file
    try:
        metadata_file = os.path.join(CHAT_HISTORY_DIR, f'chat_metadata_{session_id}.json')
        with open(metadata_file, 'w') as f:
            json.dump({"title": new_title}, f, indent=2)
        return jsonify({"status": "success", "title": new_title})
    except Exception as e:
        logging.error(f"Error renaming session: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/sessions/<session_id>/export', methods=['GET'])
def export_session(session_id):
    if session_id in active_conversations:
        history = active_conversations[session_id]
    else:
        history = load_chat_history(session_id)
    
    return jsonify({
        "session_id": session_id,
        "history": history,
        "settings": current_settings
    })

@app.route('/sessions/import', methods=['POST'])
def import_session():
    data = request.json
    if not data or 'history' not in data:
        return jsonify({"error": "Invalid import data"}), 400
    
    from datetime import datetime
    session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    active_conversations[session_id] = data['history']
    save_chat_history(session_id, data['history'])
    
    if 'settings' in data:
        update_settings(data['settings'])
    
    return jsonify({"session_id": session_id})

@app.route('/clear', methods=['POST'])
def clear():
    session_id = request.json.get('session_id')
    if session_id:
        active_conversations[session_id] = []
        save_chat_history(session_id, [])
    return jsonify({"response": "Conversation history cleared"})

# ============================================================================
# Web Search Endpoints
# ============================================================================

@app.route('/web-search/status', methods=['GET'])
def web_search_status():
    """Get web search service status"""
    if not WEB_SEARCH_AVAILABLE:
        return jsonify({
            "available": False,
            "message": "Web search services not installed"
        })

    return jsonify({
        "available": web_search_service.is_available(),
        "exa_enabled": web_search_service.exa_client is not None,
        "brave_enabled": bool(web_search_service.brave_api_key and web_search_service.brave_enabled),
        "max_results": web_search_service.max_results,
        "include_text": web_search_service.include_text
    })

@app.route('/web-search', methods=['POST'])
@limiter.limit("20 per minute")
def web_search():
    """Perform web search"""
    if not WEB_SEARCH_AVAILABLE or not web_search_service.is_available():
        return jsonify({"error": "Web search not available"}), 503

    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Missing query parameter"}), 400

    query = data['query']
    num_results = data.get('num_results', None)

    try:
        results = web_search_service.search(query, num_results)
        return jsonify({
            "query": query,
            "results": results,
            "count": len(results)
        })
    except Exception as e:
        logging.error(f"Web search error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/web-search/answer', methods=['POST'])
@limiter.limit("10 per minute")
def web_search_answer():
    """Get direct answer from Exa"""
    if not WEB_SEARCH_AVAILABLE or not web_search_service.is_available():
        return jsonify({"error": "Web search not available"}), 503

    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Missing query parameter"}), 400

    query = data['query']

    try:
        answer = web_search_service.get_answer_from_exa(query)
        if answer:
            return jsonify({
                "query": query,
                "answer": answer
            })
        else:
            return jsonify({"error": "Could not get answer from Exa"}), 503
    except Exception as e:
        logging.error(f"Web search answer error: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================================
# RAG Endpoints
# ============================================================================

@app.route('/rag/status', methods=['GET'])
def rag_status():
    """Get RAG service status"""
    if not RAG_AVAILABLE:
        return jsonify({
            "available": False,
            "message": "RAG services not installed"
        })

    return jsonify({
        "available": rag_service.is_available(),
        "embedding_model": rag_service.embedding_model_name if rag_service.is_available() else None,
        "in_memory": rag_service.in_memory if rag_service.is_available() else None,
        "settings": {
            "top_k": rag_service.top_k,
            "score_threshold": rag_service.score_threshold,
            "chunk_size": rag_service.chunk_size,
            "chunk_overlap": rag_service.chunk_overlap
        } if rag_service.is_available() else {}
    })

@app.route('/knowledge-bases', methods=['GET'])
def list_knowledge_bases():
    """List all knowledge bases"""
    if not RAG_AVAILABLE or not rag_service.is_available():
        return jsonify([])

    kbs = rag_service.list_knowledge_bases()
    return jsonify(kbs)

@app.route('/knowledge-bases', methods=['POST'])
def create_knowledge_base():
    """Create a new knowledge base"""
    if not RAG_AVAILABLE or not rag_service.is_available():
        return jsonify({"error": "RAG service not available"}), 503

    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Knowledge base name required"}), 400

    kb_name = data['name']
    success = rag_service.create_knowledge_base(kb_name)

    if success:
        return jsonify({"message": f"Knowledge base '{kb_name}' created", "name": kb_name})
    else:
        return jsonify({"error": "Failed to create knowledge base"}), 500

@app.route('/knowledge-bases/<kb_name>', methods=['DELETE'])
def delete_knowledge_base(kb_name):
    """Delete a knowledge base"""
    if not RAG_AVAILABLE or not rag_service.is_available():
        return jsonify({"error": "RAG service not available"}), 503

    success = rag_service.delete_knowledge_base(kb_name)

    if success:
        return jsonify({"message": f"Knowledge base '{kb_name}' deleted"})
    else:
        return jsonify({"error": "Failed to delete knowledge base"}), 500

@app.route('/knowledge-bases/<kb_name>/upload', methods=['POST'])
@limiter.limit("10 per minute")
def upload_file(kb_name):
    """Upload and process a file to a knowledge base"""
    if not RAG_AVAILABLE or not rag_service.is_available():
        return jsonify({"error": "RAG service not available"}), 503

    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save file
    file_path = file_handler.save_file(file, kb_name)
    if not file_path:
        return jsonify({"error": "Failed to save file"}), 500

    # Add to knowledge base
    metadata = {
        'uploaded_by': request.form.get('uploaded_by', 'unknown'),
        'description': request.form.get('description', '')
    }

    success = rag_service.add_document(kb_name, file_path, metadata)

    if success:
        return jsonify({
            "message": "File uploaded and processed successfully",
            "file_name": file.filename,
            "kb_name": kb_name
        })
    else:
        # Clean up file if processing failed
        file_handler.delete_file(file_path)
        return jsonify({"error": "Failed to process file"}), 500

@app.route('/knowledge-bases/<kb_name>/search', methods=['POST'])
def search_knowledge_base(kb_name):
    """Search in a knowledge base"""
    if not RAG_AVAILABLE or not rag_service.is_available():
        return jsonify({"error": "RAG service not available"}), 503

    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Query required"}), 400

    query = data['query']
    top_k = data.get('top_k', None)

    results = rag_service.search(kb_name, query, top_k)

    return jsonify({
        "query": query,
        "results": results,
        "count": len(results)
    })

@app.route('/files', methods=['GET'])
def list_files():
    """List uploaded files"""
    kb_name = request.args.get('kb_name', None)
    files = file_handler.list_files(kb_name)
    return jsonify(files)

def get_ip_addresses():
    """Get all IP addresses of the machine, including Tailscale"""
    import socket
    addresses = []
    try:
        # Get all network interfaces
        interfaces = socket.getaddrinfo(socket.gethostname(), None)
        
        # Filter and format addresses
        for interface in interfaces:
            addr = interface[4][0]
            # Only include IPv4 addresses and exclude localhost
            if '.' in addr and addr != '127.0.0.1':
                addresses.append(addr)
        
        # Remove duplicates and sort
        addresses = sorted(list(set(addresses)))
    except Exception as e:
        print(f"Error getting IP addresses: {e}")
        addresses = ['0.0.0.0']
    
    return addresses

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n🛑 Shutting down Cerebras Chat Interface...")
    print("✅ Server stopped successfully")
    sys.exit(0)

if __name__ == '__main__':
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Get configuration from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    # Get all available IP addresses
    ip_addresses = get_ip_addresses()

    print("\nCerebras Chat Interface is now available at:")
    print("----------------------------------------")
    for ip in ip_addresses:
        print(f"http://{ip}:{port}")
    print("----------------------------------------")
    print("Press Ctrl+C to stop the server\n")

    # Run the Flask application
    try:
        app.run(debug=debug, host=host, port=port, threaded=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Cerebras Chat Interface...")
        print("✅ Server stopped successfully")
