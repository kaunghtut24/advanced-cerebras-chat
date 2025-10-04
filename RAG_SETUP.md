# RAG (Retrieval-Augmented Generation) Setup Guide

This guide explains how to set up and use the RAG features in the Cerebras Chat Interface.

## Overview

The RAG system allows you to:
- Upload documents (PDF, DOCX, images, etc.) to knowledge bases
- Automatically parse and chunk documents using MarkItDown
- Generate embeddings using open-source models (sentence-transformers)
- Store embeddings in Qdrant vector database
- Retrieve relevant context when chatting
- Maintain separate knowledge bases for different topics

## Architecture

```
User uploads file → MarkItDown parses → Text chunking → 
Sentence-Transformers embedding → Qdrant storage → 
Query → Retrieve relevant chunks → Augment prompt → Cerebras LLM
```

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `markitdown` - Document parsing (PDF, DOCX, images, etc.)
- `sentence-transformers` - Embedding generation
- `qdrant-client` - Vector database client
- `torch` - PyTorch for embeddings
- `pillow` - Image processing

### 2. Set Up Qdrant Vector Database

You have two options:

#### Option A: In-Memory Mode (Development)

Set in `.env`:
```env
QDRANT_IN_MEMORY=true
```

This runs Qdrant in memory - no separate server needed, but data is lost on restart.

#### Option B: Qdrant Server (Production)

**Using Docker:**
```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

**Or download Qdrant:**
- Visit https://qdrant.tech/documentation/quick-start/
- Download and run the Qdrant server

Set in `.env`:
```env
QDRANT_IN_MEMORY=false
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

### 3. Configure Environment Variables

Copy and edit `.env`:

```env
# RAG Configuration
RAG_ENABLED=true
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

# Qdrant Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_IN_MEMORY=false

# RAG Settings
RAG_TOP_K=5
RAG_SCORE_THRESHOLD=0.7
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# File Upload
MAX_FILE_SIZE=52428800
ALLOWED_EXTENSIONS=pdf,docx,doc,pptx,ppt,xlsx,xls,txt,md,html,jpg,jpeg,png,gif
```

## Usage

### 1. Start the Application

```bash
python app.py
```

### 2. Create a Knowledge Base

1. Click "⚙️ Settings" in the chat interface
2. Scroll to "RAG Settings"
3. Click "Manage Knowledge Bases"
4. Enter a name and click "Create"

### 3. Upload Documents

1. In the Knowledge Base modal, select your knowledge base
2. Click "Choose Files" and select documents
3. Click "Upload Files"
4. Wait for processing (parsing + embedding + storage)

### 4. Use RAG in Chat

1. In Settings, check "Enable RAG"
2. Select your knowledge base from the dropdown
3. Start chatting - relevant context will be automatically retrieved

### 5. View Sources

When RAG is enabled, the chat will show:
- Retrieved document chunks
- Source file names
- Relevance scores

## Supported File Formats

MarkItDown supports:
- **Documents**: PDF, DOCX, DOC, PPTX, PPT, XLSX, XLS
- **Text**: TXT, MD, HTML, CSV, JSON, XML
- **Images**: JPG, JPEG, PNG, GIF (with OCR)
- **Audio**: MP3, WAV (with transcription)
- **Archives**: ZIP

## Embedding Models

Default: `all-MiniLM-L6-v2` (384 dimensions, fast, good quality)

Other options:
- `all-mpnet-base-v2` (768 dim, higher quality, slower)
- `paraphrase-multilingual-MiniLM-L12-v2` (384 dim, multilingual)
- `multi-qa-MiniLM-L6-cos-v1` (384 dim, optimized for Q&A)

Change in `.env`:
```env
EMBEDDING_MODEL=all-mpnet-base-v2
EMBEDDING_DIMENSION=768
```

## API Endpoints

### RAG Status
```bash
GET /rag/status
```

### List Knowledge Bases
```bash
GET /knowledge-bases
```

### Create Knowledge Base
```bash
POST /knowledge-bases
Content-Type: application/json

{"name": "my_kb"}
```

### Upload File
```bash
POST /knowledge-bases/{kb_name}/upload
Content-Type: multipart/form-data

file: <file>
```

### Search Knowledge Base
```bash
POST /knowledge-bases/{kb_name}/search
Content-Type: application/json

{"query": "your question", "top_k": 5}
```

### Delete Knowledge Base
```bash
DELETE /knowledge-bases/{kb_name}
```

## Troubleshooting

### RAG Not Available

Check:
1. Dependencies installed: `pip list | grep -E "sentence-transformers|qdrant-client|markitdown"`
2. Qdrant running (if not in-memory mode)
3. `.env` has `RAG_ENABLED=true`

### File Upload Fails

Check:
1. File size under `MAX_FILE_SIZE` (default 50MB)
2. File extension in `ALLOWED_EXTENSIONS`
3. Sufficient disk space in `uploads/` folder

### Poor Retrieval Quality

Adjust in `.env`:
- Increase `RAG_TOP_K` (retrieve more chunks)
- Lower `RAG_SCORE_THRESHOLD` (allow lower similarity)
- Decrease `CHUNK_SIZE` (smaller, more focused chunks)
- Increase `CHUNK_OVERLAP` (more context between chunks)

### Memory Issues

- Use smaller embedding model: `all-MiniLM-L6-v2`
- Reduce `CHUNK_SIZE`
- Use Qdrant server instead of in-memory mode

## Advanced: MarkItDown MCP Server

MarkItDown can run as an MCP (Model Context Protocol) server for advanced integrations.

See: https://github.com/microsoft/markitdown

## Performance Tips

1. **Batch uploads**: Upload multiple files at once
2. **Optimize chunk size**: Balance between context and precision
3. **Use appropriate model**: Smaller models for speed, larger for quality
4. **Persistent storage**: Use Qdrant server for production
5. **Index optimization**: Qdrant automatically optimizes indexes

## Security Considerations

1. **File validation**: Only allowed extensions are processed
2. **Size limits**: Prevent DoS with `MAX_FILE_SIZE`
3. **API key**: Protect Qdrant with `QDRANT_API_KEY` in production
4. **Rate limiting**: Upload endpoint has rate limits
5. **Sanitization**: File names are sanitized before storage

## Next Steps

- Experiment with different embedding models
- Fine-tune chunk size and overlap
- Create multiple knowledge bases for different topics
- Integrate with external document sources
- Set up automated document ingestion pipelines
