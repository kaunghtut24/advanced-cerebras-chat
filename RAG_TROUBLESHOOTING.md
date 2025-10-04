# RAG Troubleshooting Guide - Model Ignoring Knowledge Base

## Critical Fixes Applied

If the model is still ignoring your knowledge base content, we've applied these critical fixes:

### **Fix 1: MUCH Stronger System Prompt**

**Changed from weak suggestion to MANDATORY instruction:**

```python
# OLD (weak):
"Please use the above context when relevant."

# NEW (mandatory):
"""
CRITICAL INSTRUCTION - YOU MUST FOLLOW THIS:
When answering the user's question, you MUST use ONLY the information provided in the KNOWLEDGE BASE CONTEXT below.
Do NOT use your general knowledge unless the knowledge base doesn't contain the answer.
You MUST cite the source files when using information from the knowledge base.

If the knowledge base contains relevant information:
- Answer EXCLUSIVELY based on the knowledge base content
- Start your response with "Based on the knowledge base..."
- Cite the specific source file(s) in your answer
"""
```

### **Fix 2: Lowered Score Threshold**

**Problem:** Score threshold was too high (0.7), filtering out relevant results

**Solution:** Lowered to 0.3 for better recall

```env
# OLD:
RAG_SCORE_THRESHOLD=0.7  # Too strict, missed relevant content

# NEW:
RAG_SCORE_THRESHOLD=0.3  # Better recall, more results
```

### **Fix 3: Enhanced Logging**

Added detailed logging to see exactly what's being retrieved:

```
INFO: Qdrant search returned 5 results (threshold: 0.3)
INFO: Result scores: min=0.456, max=0.892, avg=0.673
INFO: Returning 5 results:
INFO:   1. refund_policy.pdf (score: 0.892) - Our refund policy allows...
INFO:   2. terms.pdf (score: 0.756) - Refunds are processed within...
INFO:   3. faq.pdf (score: 0.456) - Common questions about refunds...
```

---

## Step-by-Step Debugging

### **Step 1: Verify RAG is Enabled**

**Check the UI:**
```
Look for: 📚 RAG [ON] with a knowledge base selected
NOT: 📚 RAG [OFF] or "Select KB..."
```

**Check server logs:**
```
Should see:
INFO: RAG enabled: Searching knowledge base 'your_kb_name' for query: 'your question'

Should NOT see:
WARNING: ⚠ RAG enabled but no knowledge base selected
```

---

### **Step 2: Verify Knowledge Base Has Content**

**In the UI:**
1. Click Settings (⚙️)
2. Click "Manage Knowledge Bases"
3. Check your knowledge base shows documents

**Should see:**
```
my_knowledge_base
📄 3 documents
```

**Should NOT see:**
```
my_knowledge_base
📄 0 documents
```

**Check server logs:**
```
Should see when you uploaded files:
INFO: Successfully added document 'file.pdf' to knowledge base 'my_kb'
INFO: Created 15 chunks from document
```

---

### **Step 3: Check if RAG is Retrieving Content**

**Ask a question and check server logs:**

**Good logs (RAG working):**
```
INFO: RAG enabled: Searching knowledge base 'company_docs' for query: 'What is the refund policy?'
INFO: Qdrant search returned 3 results (threshold: 0.3)
INFO: Result scores: min=0.456, max=0.892, avg=0.673
INFO: ✓ RAG: Retrieved 3 relevant chunks from 'company_docs'
INFO: ✓ RAG: Context length: 1247 characters
INFO: ✓ RAG: Sources: refund_policy.pdf, terms.pdf
INFO: ✓ System prompt includes RAG context (1247 chars)
```
✅ **RAG is working - retrieving content**

**Bad logs (RAG not finding content):**
```
INFO: RAG enabled: Searching knowledge base 'company_docs' for query: 'What is the refund policy?'
INFO: Qdrant search returned 0 results (threshold: 0.3)
WARNING: ⚠ RAG: No results found in knowledge base 'company_docs' for query
```
❌ **RAG not finding relevant content - see Fix #4 below**

---

### **Step 4: Verify Model Receives RAG Context**

**Check logs for:**
```
INFO: ✓ System prompt includes RAG context (XXXX chars)
INFO: Sending to model: 3 messages (1 system + 2 history)
```

**If you see this:** RAG context IS being sent to the model

**If you DON'T see this:** RAG context is NOT being sent - check Step 3

---

### **Step 5: Test with a Simple, Direct Question**

**Instead of vague questions, ask something specific:**

❌ **Bad (vague):**
```
"Tell me about the company"
"What do you know?"
"Help me understand this"
```

✅ **Good (specific):**
```
"What is the refund policy?"
"How long does shipping take?"
"What are the payment methods?"
```

**Why:** Specific questions match better with document chunks

---

## Common Problems & Solutions

### **Problem 1: RAG Returns 0 Results**

**Symptoms:**
```
INFO: Qdrant search returned 0 results (threshold: 0.3)
WARNING: ⚠ RAG: No results found
```

**Possible Causes:**

#### **Cause A: Query doesn't match document content**

**Example:**
- KB contains: "Company policies and procedures"
- Query: "What is the weather today?"
- Result: No match (expected)

**Solution:** Ask questions related to your documents

#### **Cause B: Documents not properly chunked**

**Check logs when you uploaded:**
```
Should see:
INFO: Created 15 chunks from document

Should NOT see:
INFO: Created 0 chunks from document
```

**Solution:** Re-upload the document

#### **Cause C: Embedding model not working**

**Check logs:**
```
Should see:
INFO: Sentence transformer model loaded successfully

Should NOT see:
ERROR: Failed to load embedding model
```

**Solution:** Restart server, check dependencies

---

### **Problem 2: RAG Retrieves Content but Model Ignores It**

**Symptoms:**
```
INFO: ✓ RAG: Retrieved 3 relevant chunks
INFO: ✓ System prompt includes RAG context (1247 chars)
[But model still gives generic answer without citing sources]
```

**This should be FIXED with the new strong prompt, but if it still happens:**

#### **Solution A: Check the actual response**

Does the model say:
```
"Based on the knowledge base..." ✅ Good
"According to [filename]..." ✅ Good
"I don't have specific information..." ❌ Not using KB
```

#### **Solution B: Try starting a new session**

Old conversation history might confuse the model:
1. Click "New Chat" or refresh page
2. Enable RAG again
3. Ask the question again

#### **Solution C: Make your question more specific**

Instead of:
```
"Tell me about refunds"
```

Try:
```
"According to the refund policy document, how many days do I have to request a refund?"
```

---

### **Problem 3: Model Cites Wrong Information**

**Symptoms:**
Model cites sources but the information is wrong or from the wrong document

**Possible Causes:**

#### **Cause A: Multiple similar documents**

If you have multiple documents with similar content, the model might mix them up.

**Solution:** Use more specific queries or organize documents better

#### **Cause B: Chunks are too small**

If `CHUNK_SIZE=500` is too small, context might be fragmented.

**Solution:** Increase chunk size in `.env`:
```env
CHUNK_SIZE=1000  # Larger chunks for more context
CHUNK_OVERLAP=100  # More overlap to preserve context
```

Then re-upload documents.

---

### **Problem 4: Score Threshold Too High**

**Symptoms:**
```
INFO: Qdrant search returned 0 results (threshold: 0.7)
```

Even though you have relevant documents.

**Solution:** Lower the threshold in `.env`:

```env
# Very strict (only exact matches)
RAG_SCORE_THRESHOLD=0.7

# Balanced
RAG_SCORE_THRESHOLD=0.5

# Better recall (recommended)
RAG_SCORE_THRESHOLD=0.3

# Maximum recall (might include irrelevant results)
RAG_SCORE_THRESHOLD=0.1
```

**Restart server after changing.**

---

### **Problem 5: Knowledge Base Not Persisting**

**Symptoms:**
Knowledge base disappears after server restart

**Solution:** Check `.env`:
```env
QDRANT_IN_MEMORY=false  # Must be false!
QDRANT_PATH=./qdrant_storage  # Must be set!
```

See `PERSISTENT_STORAGE_FIX.md` for details.

---

## Testing Checklist

Use this checklist to verify RAG is working:

### **✓ Pre-Test Setup**

- [ ] Server is running
- [ ] RAG toggle shows [ON]
- [ ] Knowledge base is selected (not "Select KB...")
- [ ] Knowledge base has documents (not "0 documents")

### **✓ During Test**

- [ ] Ask a specific question related to your documents
- [ ] Check server logs in real-time

### **✓ Expected Logs**

- [ ] `INFO: RAG enabled: Searching knowledge base...`
- [ ] `INFO: Qdrant search returned X results` (X > 0)
- [ ] `INFO: ✓ RAG: Retrieved X relevant chunks`
- [ ] `INFO: ✓ RAG: Sources: file1.pdf, file2.pdf`
- [ ] `INFO: ✓ System prompt includes RAG context`

### **✓ Expected Response**

- [ ] Response starts with "Based on the knowledge base..." or similar
- [ ] Response cites specific source files
- [ ] Response contains information from your documents
- [ ] Response does NOT give generic answers

---

## Example Test Case

### **Setup:**

1. **Create knowledge base:** "company_policies"
2. **Upload document:** "refund_policy.pdf" containing:
   ```
   Our refund policy allows customers to request a full refund within 30 days
   of purchase. Refunds are processed within 5-7 business days.
   ```
3. **Enable RAG** and select "company_policies"

### **Test Query:**

```
"What is the refund policy?"
```

### **Expected Server Logs:**

```
INFO: Chat request received from 127.0.0.1
INFO: RAG enabled: Searching knowledge base 'company_policies' for query: 'What is the refund policy?'
INFO: Qdrant search returned 2 results (threshold: 0.3)
INFO: Result scores: min=0.756, max=0.892, avg=0.824
INFO: ✓ RAG: Retrieved 2 relevant chunks from 'company_policies'
INFO: ✓ RAG: Context length: 487 characters
INFO: ✓ RAG: Sources: refund_policy.pdf
INFO: Returning 2 results:
INFO:   1. refund_policy.pdf (score: 0.892) - Our refund policy allows customers to request a full refund within 30 days...
INFO:   2. refund_policy.pdf (score: 0.756) - Refunds are processed within 5-7 business days...
INFO: Sending to model: 3 messages (1 system + 2 history)
INFO: ✓ System prompt includes RAG context (487 chars)
```

### **Expected Response:**

```
Based on the knowledge base (refund_policy.pdf), customers can request a full 
refund within 30 days of purchase. According to the same document, refunds are 
processed within 5-7 business days after the request is approved.
```

✅ **Perfect!** Model used KB content and cited source.

---

## Quick Fixes Summary

| Problem | Quick Fix |
|---------|-----------|
| No results found | Lower `RAG_SCORE_THRESHOLD` to 0.3 |
| Model ignores KB | Restart server (new strong prompt) |
| KB disappears | Set `QDRANT_IN_MEMORY=false` |
| Wrong information | Increase `CHUNK_SIZE` to 1000 |
| Generic answers | Start new chat session |
| No KB selected | Select KB from dropdown |

---

## Still Not Working?

If you've tried everything and RAG still doesn't work:

1. **Check the full server logs** and share them
2. **Try this test:**
   - Create a new KB called "test"
   - Upload a simple text file with "The answer is 42"
   - Ask "What is the answer?"
   - Check if model says "Based on the knowledge base, the answer is 42"

3. **Verify dependencies:**
   ```bash
   pip list | grep -E "sentence-transformers|qdrant-client|markitdown"
   ```

4. **Check Qdrant storage:**
   ```bash
   ls -la qdrant_storage/
   ```
   Should show collection folders

---

**With these fixes, your model should now actively use and cite knowledge base content!** 📚✨
