# Cerebras Chat Interface

A modern web-based chat interface for Cerebras AI models with session management, settings configuration, and responsive design.

## Features

- 🤖 Support for multiple Cerebras AI models (Production and Preview)
- 💬 Session management with chat history
- ⚙️ Configurable settings (model, temperature, max tokens, system prompt)
- 📱 Responsive mobile-first design
- 🔄 Import/Export chat sessions
- 🚀 Rate limiting and security features
- 🌍 Environment variable configuration
- 📚 **RAG (Retrieval-Augmented Generation)** with document upload
- 🔍 Vector search with Qdrant database
- 📄 Multi-format document parsing (PDF, DOCX, images, etc.) with MarkItDown
- 🧠 Open-source embeddings with sentence-transformers
- 🗂️ Multiple knowledge bases for different topics
- 🌐 **Web Search** with Exa (primary) and Brave Search (fallback)
- 🔎 AI-powered semantic search for up-to-date information
- 📰 Automatic source citation and content integration

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd cerebras-chat-interface
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` and add your Cerebras API key:

```env
CEREBRAS_API_KEY=your_actual_api_key_here
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### 6. (Optional) Set Up RAG Features

For document upload and RAG capabilities, see [RAG_SETUP.md](RAG_SETUP.md) for detailed instructions.

**Quick start for RAG:**
```bash
# Use in-memory mode (no separate database needed)
# Already configured in .env with QDRANT_IN_MEMORY=true

# Or run Qdrant server with Docker
docker run -p 6333:6333 qdrant/qdrant
```

### 7. (Optional) Set Up Web Search

For web search capabilities, see [WEB_SEARCH_SETUP.md](WEB_SEARCH_SETUP.md) for detailed instructions.

**Quick start for web search:**
```bash
# Install Exa SDK
pip install exa-py

# Get API keys:
# - Exa: https://dashboard.exa.ai/api-keys
# - Brave: https://brave.com/search/api/

# Add to .env:
# EXA_API_KEY=your_key_here
# BRAVE_API_KEY=your_key_here
```

## Environment Variables

The application supports the following environment variables:

### Required
- `CEREBRAS_API_KEY`: Your Cerebras API key (get one from [cloud.cerebras.ai](https://cloud.cerebras.ai/))

### Optional
- `CEREBRAS_BASE_URL`: Cerebras API base URL (default: `https://api.cerebras.ai`)
- `FLASK_ENV`: Flask environment (default: `development`)
- `FLASK_DEBUG`: Enable Flask debug mode (default: `False`)
- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `5000`)
- `RATE_LIMIT_STORAGE`: Rate limiting storage (default: `memory://`)
- `RATE_LIMIT_DEFAULT`: Default rate limits (default: `200 per day, 50 per hour`)
- `RATE_LIMIT_CHAT`: Chat endpoint rate limit (default: `30 per minute`)
- `MAX_CONTENT_LENGTH`: Maximum request size in bytes (default: `16777216`)
- `MAX_HISTORY_LENGTH`: Maximum conversation history length (default: `20`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

### RAG Configuration (Optional)
- `RAG_ENABLED`: Enable RAG features (default: `true`)
- `EMBEDDING_MODEL`: Sentence-transformers model (default: `all-MiniLM-L6-v2`)
- `EMBEDDING_DIMENSION`: Embedding vector size (default: `384`)
- `QDRANT_HOST`: Qdrant server host (default: `localhost`)
- `QDRANT_PORT`: Qdrant server port (default: `6333`)
- `QDRANT_IN_MEMORY`: Use in-memory Qdrant (default: `true`)
- `RAG_TOP_K`: Number of chunks to retrieve (default: `5`)
- `RAG_SCORE_THRESHOLD`: Minimum similarity score (default: `0.7`)
- `CHUNK_SIZE`: Document chunk size (default: `500`)
- `CHUNK_OVERLAP`: Overlap between chunks (default: `50`)
- `MAX_FILE_SIZE`: Maximum upload file size in bytes (default: `52428800`)
- `ALLOWED_EXTENSIONS`: Comma-separated file extensions

## Available Models

### Production Models
- Llama 4 Scout (109B parameters)
- Llama 3.1 8B (8B parameters)
- Llama 3.3 70B (70B parameters)
- OpenAI GPT OSS (120B parameters)
- Qwen 3 32B (32B parameters)

### Preview Models
- Llama 4 Maverick (400B parameters)
- Qwen 3 235B Instruct (235B parameters)
- Qwen 3 235B Thinking (235B parameters)
- Qwen 3 480B Coder (480B parameters)

## Development

### Building for Production

```bash
npm run build
```

This copies the frontend files to the `dist` directory.

### Running Tests

```bash
# Test the API endpoint
python -c "import requests; print(requests.post('http://127.0.0.1:5000/chat', json={'message': 'Hello', 'session_id': 'test'}).json())"
```

## API Endpoints

### Chat & Sessions
- `GET /` - Main chat interface
- `POST /chat` - Send chat message (with optional RAG)
- `GET /models` - Get available models
- `GET /settings` - Get current settings
- `POST /settings` - Update settings
- `POST /settings/reset` - Reset settings to default
- `GET /sessions` - List chat sessions
- `POST /sessions` - Create new session
- `GET /sessions/<id>` - Get session history
- `DELETE /sessions/<id>` - Delete session
- `POST /clear` - Clear current session

### RAG Endpoints
- `GET /rag/status` - Check RAG service status
- `GET /knowledge-bases` - List all knowledge bases
- `POST /knowledge-bases` - Create new knowledge base
- `DELETE /knowledge-bases/<name>` - Delete knowledge base
- `POST /knowledge-bases/<name>/upload` - Upload file to knowledge base
- `POST /knowledge-bases/<name>/search` - Search in knowledge base
- `GET /files` - List uploaded files

### Web Search Endpoints
- `GET /web-search/status` - Check web search service status
- `POST /web-search` - Perform web search
- `POST /web-search/answer` - Get direct answer from Exa

## License

MIT License
