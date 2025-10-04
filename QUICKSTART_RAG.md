# RAG Quick Start Guide

Get up and running with RAG features in 5 minutes!

## Prerequisites

- Python 3.8+
- Virtual environment activated
- Cerebras API key

## Step 1: Install RAG Dependencies (2 minutes)

```bash
# Option A: Automated installation
python install_rag.py

# Option B: Manual installation
pip install markitdown pillow sentence-transformers qdrant-client torch numpy tqdm
```

## Step 2: Configure Environment (1 minute)

Your `.env` file should already have RAG settings. Verify:

```bash
cat .env | grep RAG
```

Should show:
```env
RAG_ENABLED=true
QDRANT_IN_MEMORY=true
```

✅ **In-memory mode** is enabled by default - no separate database needed!

## Step 3: Start the Application (30 seconds)

```bash
python app.py
```

Wait for:
```
Environment variables loaded from .env file
Cerebras SDK initialized successfully.
RAG service initialized: Available
```

## Step 4: Test RAG (1 minute)

Open browser to `http://localhost:5000`

### Create a Knowledge Base

1. Click **⚙️ Settings**
2. Scroll to **RAG Settings**
3. Click **Manage Knowledge Bases**
4. Enter name: `test_kb`
5. Click **Create**

### Upload a Document

1. In the modal, select `test_kb`
2. Click **Choose Files**
3. Select a PDF, DOCX, or TXT file
4. Click **Upload Files**
5. Wait for "Uploaded successfully"

### Chat with RAG

1. Close the modal
2. Check **☑ Enable RAG**
3. Select `test_kb` from dropdown
4. Ask a question about your document
5. See sources appear below the response!

## Step 5: Verify (30 seconds)

Run the test suite:

```bash
python test_rag.py
```

Should see:
```
✅ PASS - RAG Status
✅ PASS - Create KB
✅ PASS - Upload File
✅ PASS - Search KB
✅ PASS - Chat with RAG
```

## That's It! 🎉

You now have a fully functional RAG system!

## Quick Tips

### Supported File Types
- **Documents**: PDF, DOCX, PPTX, XLSX
- **Text**: TXT, MD, HTML, CSV, JSON
- **Images**: JPG, PNG (with OCR)

### Best Practices
- **Small files first**: Test with a simple TXT file
- **One topic per KB**: Create separate KBs for different subjects
- **Check sources**: Verify RAG is retrieving relevant chunks
- **Adjust settings**: Tune top-k and threshold if needed

### Common Issues

**"RAG service not available"**
```bash
# Check dependencies
pip list | grep -E "sentence-transformers|qdrant-client|markitdown"

# Reinstall if needed
python install_rag.py
```

**"Upload failed"**
- Check file size < 50MB
- Verify file extension is allowed
- Check disk space

**"No results found"**
- Try a different query
- Lower `RAG_SCORE_THRESHOLD` in .env
- Increase `RAG_TOP_K` in .env

## Next Steps

### Production Setup

For production, use Qdrant server instead of in-memory:

```bash
# Start Qdrant with Docker
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant

# Update .env
QDRANT_IN_MEMORY=false
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

### Advanced Configuration

Edit `.env` to customize:

```env
# Use better embedding model (slower but higher quality)
EMBEDDING_MODEL=all-mpnet-base-v2
EMBEDDING_DIMENSION=768

# Retrieve more chunks
RAG_TOP_K=10

# Lower similarity threshold
RAG_SCORE_THRESHOLD=0.5

# Larger chunks for more context
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
```

### Learn More

- **Full RAG Guide**: See `RAG_SETUP.md`
- **API Documentation**: See `README.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`

## Example Workflow

### Building a Company Knowledge Base

1. **Create KB**: `company_docs`
2. **Upload files**:
   - Product documentation (PDF)
   - Employee handbook (DOCX)
   - Meeting notes (TXT)
   - Presentations (PPTX)
3. **Enable RAG** and select `company_docs`
4. **Ask questions**:
   - "What is our vacation policy?"
   - "How does the product authentication work?"
   - "What was discussed in the Q3 planning meeting?"

### Building a Research Assistant

1. **Create KB**: `research_papers`
2. **Upload**: Academic papers (PDF)
3. **Enable RAG** and select `research_papers`
4. **Ask**: "What are the main findings about X?"

### Building a Code Documentation Helper

1. **Create KB**: `code_docs`
2. **Upload**: README files, API docs (MD, HTML)
3. **Enable RAG** and select `code_docs`
4. **Ask**: "How do I use the authentication API?"

## Troubleshooting Commands

```bash
# Check RAG status
curl http://localhost:5000/rag/status

# List knowledge bases
curl http://localhost:5000/knowledge-bases

# Test environment
python test_env.py

# Full RAG test
python test_rag.py
```

## Performance Tips

### For Speed
- Use `all-MiniLM-L6-v2` (default)
- Keep `CHUNK_SIZE=500`
- Use in-memory Qdrant

### For Quality
- Use `all-mpnet-base-v2`
- Increase `CHUNK_SIZE=1000`
- Lower `RAG_SCORE_THRESHOLD=0.5`

### For Large Documents
- Use Qdrant server (not in-memory)
- Increase `MAX_FILE_SIZE`
- Process in batches

## Getting Help

1. Check logs in terminal
2. Review `RAG_SETUP.md`
3. Run `python test_rag.py`
4. Check file permissions in `uploads/` folder

## Success Checklist

- ✅ Dependencies installed
- ✅ `.env` configured
- ✅ Application starts without errors
- ✅ "RAG service initialized: Available" in logs
- ✅ Can create knowledge base
- ✅ Can upload file
- ✅ Can enable RAG in settings
- ✅ Sources appear in chat responses

---

**Ready to build amazing RAG applications!** 🚀
