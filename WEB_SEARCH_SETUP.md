# Web Search Setup Guide

This guide explains how to set up and use the web search features in the Cerebras Chat Interface with Exa (primary) and Brave Search (fallback).

## Overview

The web search system allows you to:
- Automatically search the web for up-to-date information
- Use Exa as the primary search engine (AI-powered semantic search)
- Fall back to Brave Search API if Exa is unavailable
- Integrate web content directly into LLM responses
- Get comprehensive, cited answers with source attribution

## Architecture

```
User query → Exa Search (primary) → Parse & extract content →
             ↓ (if fails)
         Brave Search (fallback) → Parse & extract content →
                                 ↓
                    Format context → Augment LLM prompt → Cerebras LLM
```

## Installation

### 1. Install Python Dependencies

```bash
pip install exa-py requests
```

Or use the full requirements:
```bash
pip install -r requirements.txt
```

### 2. Get API Keys

#### Exa API Key (Primary - Recommended)

1. Visit [https://dashboard.exa.ai/api-keys](https://dashboard.exa.ai/api-keys)
2. Sign up for an account
3. Create a new API key
4. Copy the API key

**Exa Features:**
- AI-powered semantic search
- High-quality, relevant results
- Full text content extraction
- Direct answer generation
- Find similar content

#### Brave Search API Key (Fallback - Optional)

1. Visit [https://brave.com/search/api/](https://brave.com/search/api/)
2. Sign up for the Brave Search API
3. Get your API key
4. Copy the API key

**Brave Features:**
- Traditional keyword search
- Fast results
- Privacy-focused
- Good fallback option

### 3. Configure Environment Variables

Edit your `.env` file:

```env
# Exa Search (Primary)
EXA_API_KEY=your_exa_api_key_here
EXA_ENABLED=true

# Brave Search (Fallback)
BRAVE_API_KEY=your_brave_api_key_here
BRAVE_ENABLED=true

# Web Search Settings
WEB_SEARCH_MAX_RESULTS=5
WEB_SEARCH_INCLUDE_TEXT=true
WEB_SEARCH_TEXT_LENGTH=1000
```

## Usage

### 1. Start the Application

```bash
python app.py
```

Look for:
```
Web search initialized: Available
```

### 2. Enable Web Search in Chat

1. Open `http://localhost:5000`
2. Click **⚙️ Settings**
3. Scroll to **Web Search Settings**
4. Check **☑ Enable Web Search**
5. Click **Save Settings**

### 3. Ask Questions

Now when you chat, the system will:
1. Search the web for relevant information
2. Extract full text content
3. Include it in the LLM context
4. Generate comprehensive answers with citations

Example questions:
- "What are the latest developments in quantum computing?"
- "What happened in the news today?"
- "Explain the recent changes to Python 3.13"

### 4. View Sources

Web search results appear below the response with:
- Source titles
- URLs (clickable)
- Publication dates (if available)
- Source provider (Exa or Brave)

## API Endpoints

### Check Web Search Status

```bash
GET /web-search/status
```

Response:
```json
{
  "available": true,
  "exa_enabled": true,
  "brave_enabled": true,
  "max_results": 5,
  "include_text": true
}
```

### Perform Web Search

```bash
POST /web-search
Content-Type: application/json

{
  "query": "latest AI developments",
  "num_results": 5
}
```

Response:
```json
{
  "query": "latest AI developments",
  "results": [
    {
      "title": "...",
      "url": "...",
      "snippet": "...",
      "text": "...",
      "score": 0.95,
      "published_date": "2025-10-01",
      "source": "exa"
    }
  ],
  "count": 5
}
```

### Get Direct Answer (Exa Only)

```bash
POST /web-search/answer
Content-Type: application/json

{
  "query": "What is the population of Tokyo?"
}
```

Response:
```json
{
  "query": "What is the population of Tokyo?",
  "answer": "Tokyo has a population of approximately 14 million..."
}
```

## Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `EXA_API_KEY` | - | Your Exa API key |
| `EXA_ENABLED` | `true` | Enable/disable Exa search |
| `BRAVE_API_KEY` | - | Your Brave Search API key |
| `BRAVE_ENABLED` | `true` | Enable/disable Brave search |
| `WEB_SEARCH_MAX_RESULTS` | `5` | Number of results to retrieve |
| `WEB_SEARCH_INCLUDE_TEXT` | `true` | Include full text content |
| `WEB_SEARCH_TEXT_LENGTH` | `1000` | Max characters per result |

### Adjusting Search Quality

**For more results:**
```env
WEB_SEARCH_MAX_RESULTS=10
```

**For longer content:**
```env
WEB_SEARCH_TEXT_LENGTH=2000
```

**For faster responses (less content):**
```env
WEB_SEARCH_TEXT_LENGTH=500
WEB_SEARCH_MAX_RESULTS=3
```

## Exa vs Brave Search

### When Exa is Better

- Semantic/conceptual queries
- Research questions
- Finding high-quality content
- Need for full text extraction
- Direct answer generation

### When Brave is Better

- Keyword-specific searches
- News and current events
- Privacy-focused searches
- Backup/fallback option

### Automatic Fallback

The system automatically tries Exa first, then falls back to Brave if:
- Exa API is unavailable
- Exa returns no results
- Exa API key is missing
- Exa encounters an error

## Advanced Features

### Find Similar Content (Exa Only)

The service includes a `find_similar()` method to find content similar to a given URL:

```python
from web_search_service import web_search_service

results = web_search_service.find_similar(
    "https://example.com/article",
    num_results=5
)
```

### Direct Answer Streaming (Exa Only)

Get streaming answers directly from Exa:

```python
answer = web_search_service.get_answer_from_exa(
    "What are the health benefits of green tea?"
)
```

## Combining with RAG

You can use both RAG and web search together:

1. **Enable RAG**: For your internal documents
2. **Enable Web Search**: For external, up-to-date information
3. **Ask questions**: The LLM will use both sources

Example:
- RAG provides: Company policies, internal docs
- Web Search provides: Latest industry news, external research
- LLM combines: Comprehensive answer using both sources

## Troubleshooting

### Web Search Not Available

Check:
1. Dependencies installed: `pip list | grep exa-py`
2. API keys in `.env` file
3. `.env` file loaded: Check startup logs
4. At least one provider enabled

### Poor Search Results

**For Exa:**
- Use natural language queries
- Be specific about what you're looking for
- Try semantic/conceptual questions

**For Brave:**
- Use keyword-based queries
- Include specific terms
- Try shorter, more direct queries

### Rate Limiting

Both services have rate limits:

**Exa:**
- Check your plan limits at dashboard.exa.ai
- Reduce `WEB_SEARCH_MAX_RESULTS` if hitting limits

**Brave:**
- Free tier: 2,000 queries/month
- Paid tiers available for more

### Slow Responses

To speed up:
1. Reduce `WEB_SEARCH_MAX_RESULTS`
2. Reduce `WEB_SEARCH_TEXT_LENGTH`
3. Disable `WEB_SEARCH_INCLUDE_TEXT` for snippets only

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Rate Limiting**: Web search endpoints have rate limits (20/min for search, 10/min for answers)
3. **Content Validation**: Results are from external sources - validate important information
4. **Privacy**: Exa and Brave may log queries per their privacy policies

## Best Practices

1. **Use Exa for research**: Better for in-depth, semantic searches
2. **Use Brave for news**: Better for current events and keywords
3. **Combine with RAG**: Use both for comprehensive answers
4. **Cite sources**: Always check the source URLs provided
5. **Verify information**: Cross-reference important facts
6. **Monitor usage**: Keep track of API usage and costs

## Example Use Cases

### Research Assistant
- Enable web search
- Ask: "What are the latest findings on climate change?"
- Get: Comprehensive answer with recent research papers

### News Summarizer
- Enable web search
- Ask: "Summarize today's tech news"
- Get: Current news with source links

### Fact Checker
- Enable web search
- Ask: "Is this claim true: [claim]"
- Get: Verified information with sources

### Learning Assistant
- Enable web search + RAG
- Ask: "Explain quantum entanglement"
- Get: Educational content from web + your notes

## Cost Considerations

### Exa Pricing
- Check current pricing at [exa.ai/pricing](https://exa.ai/pricing)
- Pay per search request
- Different tiers available

### Brave Search Pricing
- Free tier: 2,000 queries/month
- Paid tiers for higher volume
- Check [brave.com/search/api](https://brave.com/search/api/)

### Optimization Tips
- Cache frequent queries (future feature)
- Reduce max results for common queries
- Use direct answers for simple questions
- Combine multiple questions into one search

## Next Steps

1. Get your API keys
2. Configure `.env` file
3. Test with simple queries
4. Experiment with different query types
5. Combine with RAG for best results
6. Monitor usage and adjust settings

---

**Ready to search the web with AI!** 🌐🔍
