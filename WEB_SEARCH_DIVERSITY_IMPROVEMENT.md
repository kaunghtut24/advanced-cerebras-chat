# Web Search Diversity Improvement

## Problem Solved

**Issue:** Web search was returning most results from a single source/domain, leading to:
- Limited perspective (single-source bias)
- Redundant information from same website
- Missing diverse viewpoints
- Poor coverage of the topic

**Example Before:**
```
Search: "Python async programming"
Results:
1. docs.python.org - Asyncio documentation
2. docs.python.org - Coroutines guide
3. docs.python.org - Event loop reference
4. docs.python.org - Tasks and futures
5. docs.python.org - Streams API
```
❌ All from same source (official docs only)

## Solution Implemented

Added **intelligent source diversity** to ensure results come from multiple different sources:

**Example After:**
```
Search: "Python async programming"
Results:
1. docs.python.org - Asyncio documentation
2. realpython.com - Async/await tutorial
3. stackoverflow.com - Common async patterns
4. medium.com - Async best practices
5. github.com - Popular async libraries
```
✅ 5 different sources for comprehensive coverage

---

## How It Works

### **1. Request More Results Than Needed**

```python
# Request 3x more results to filter from
request_count = num_results * diversity_multiplier  # e.g., 5 * 3 = 15
```

**Why:** Exa returns results sorted by relevance. By requesting more, we can filter for diversity while keeping quality.

### **2. Domain-Based Deduplication**

```python
# Extract domain from URL
domain = urlparse(item.url).netloc.replace('www.', '')

# Limit results per domain
domain_count = sum(1 for d in seen_domains if d == domain)
if domain_count >= max_per_domain:
    skip  # Already have enough from this domain
```

**Why:** Prevents single-domain dominance while allowing high-quality sources to contribute multiple results.

### **3. Configurable Diversity Settings**

Two new environment variables control diversity:

```env
# Maximum results from same domain (default: 2)
WEB_SEARCH_MAX_PER_DOMAIN=2

# Request multiplier for diversity (default: 3)
WEB_SEARCH_DIVERSITY_MULTIPLIER=3
```

---

## Configuration Options

### **WEB_SEARCH_MAX_PER_DOMAIN**

**What it does:** Limits how many results can come from the same domain

**Values:**
- `1` - Maximum diversity (one result per domain)
- `2` - Balanced (default, allows 2 per domain)
- `3+` - Less strict (allows more from same domain)

**Examples:**

```env
# Maximum diversity - one result per source
WEB_SEARCH_MAX_PER_DOMAIN=1

# Balanced - allow 2 results from high-quality sources
WEB_SEARCH_MAX_PER_DOMAIN=2

# Relaxed - allow 3 results per domain
WEB_SEARCH_MAX_PER_DOMAIN=3
```

**When to use:**
- `1` - When you want maximum source diversity
- `2` - Default, good balance between diversity and quality
- `3+` - When authoritative sources are more important than diversity

---

### **WEB_SEARCH_DIVERSITY_MULTIPLIER**

**What it does:** Controls how many extra results to request for filtering

**Values:**
- `2` - Request 2x results (e.g., 10 to get 5)
- `3` - Request 3x results (default, e.g., 15 to get 5)
- `4+` - Request 4x+ results (maximum diversity)

**Examples:**

```env
# Moderate diversity
WEB_SEARCH_DIVERSITY_MULTIPLIER=2

# High diversity (default)
WEB_SEARCH_DIVERSITY_MULTIPLIER=3

# Maximum diversity (may hit API limits)
WEB_SEARCH_DIVERSITY_MULTIPLIER=4
```

**When to use:**
- `2` - Faster, less API usage, moderate diversity
- `3` - Default, good balance
- `4+` - Maximum diversity, more API usage

---

## Algorithm Details

### **Step-by-Step Process:**

1. **Request Extra Results**
   ```python
   request_count = min(num_results * diversity_multiplier, 20)
   # Example: 5 * 3 = 15 results requested
   ```

2. **Fetch from Exa**
   ```python
   result = exa_client.search_and_contents(
       query,
       num_results=request_count,  # 15 results
       use_autoprompt=True
   )
   ```

3. **Filter for Diversity**
   ```python
   for item in result.results:
       domain = extract_domain(item.url)
       
       # Count existing results from this domain
       domain_count = count_domain(seen_domains, domain)
       
       # Skip if too many from this domain
       if domain_count >= max_per_domain:
           continue
       
       # Add to results
       formatted_results.append(item)
       seen_domains.append(domain)
       
       # Stop when we have enough
       if len(formatted_results) >= num_results:
           break
   ```

4. **Return Diverse Results**
   ```python
   # Returns 5 results from 5 different domains (if max_per_domain=1)
   # Or 5 results from 3-5 domains (if max_per_domain=2)
   ```

---

## Logging and Monitoring

### **Enhanced Logging**

The service now logs detailed diversity statistics:

```
INFO: Searching with Exa: 'Python async programming' (requesting diverse sources)
INFO: Exa returned 5 diverse results from 5 different sources
INFO: Top sources: realpython.com(1), docs.python.org(1), stackoverflow.com(1)
```

**What you can see:**
- Total results returned
- Number of unique sources
- Top contributing domains

### **Domain Statistics**

```python
domain_stats = {
    'realpython.com': 1,
    'docs.python.org': 2,
    'stackoverflow.com': 1,
    'medium.com': 1
}
```

Logged as:
```
INFO: Top sources: docs.python.org(2), realpython.com(1), stackoverflow.com(1)
```

---

## Context Formatting Improvements

### **Before:**
```
=== WEB SEARCH RESULTS ===

[Source 1]
Title: Asyncio Documentation
URL: https://docs.python.org/3/library/asyncio.html
Content: ...
```

### **After:**
```
=== WEB SEARCH RESULTS ===
Found 5 results from 5 different sources

[Source 1 - docs.python.org]
Title: Asyncio Documentation
URL: https://docs.python.org/3/library/asyncio.html
Relevance Score: 0.892
Content: ...

[Source 2 - realpython.com]
Title: Async IO in Python
URL: https://realpython.com/async-io-python/
Relevance Score: 0.856
Content: ...

=== END WEB SEARCH RESULTS ===
Note: Results are from 5 diverse sources for comprehensive coverage.
```

**Improvements:**
✅ Shows total sources upfront  
✅ Displays domain in source header  
✅ Includes relevance score  
✅ Notes diversity at the end  

---

## Benefits

### **1. Better Information Quality**

**Before:**
- Single perspective (e.g., only official docs)
- May miss practical examples
- Limited to one writing style

**After:**
- Multiple perspectives (docs, tutorials, discussions)
- Practical examples from various sources
- Different writing styles for better understanding

### **2. Comprehensive Coverage**

**Before:**
```
Query: "React hooks best practices"
Results: All from reactjs.org
Coverage: Official docs only
```

**After:**
```
Query: "React hooks best practices"
Results:
- reactjs.org (official docs)
- kentcdodds.com (expert blog)
- stackoverflow.com (community Q&A)
- dev.to (developer tutorials)
- github.com (real-world examples)
Coverage: Docs + tutorials + community + examples
```

### **3. Reduced Bias**

**Before:**
- Single source may have bias
- Limited viewpoint
- May miss alternatives

**After:**
- Multiple sources balance each other
- Diverse viewpoints
- Includes alternatives and comparisons

---

## Use Cases

### **Use Case 1: Technical Documentation**

**Query:** "How to use Docker volumes"

**Old Results:**
1. docs.docker.com - Volumes overview
2. docs.docker.com - Volume drivers
3. docs.docker.com - Volume commands
4. docs.docker.com - Volume plugins
5. docs.docker.com - Volume API

**New Results:**
1. docs.docker.com - Official volumes guide
2. digitalocean.com - Docker volumes tutorial
3. stackoverflow.com - Common volume issues
4. medium.com - Docker volumes best practices
5. github.com - Docker compose examples

✅ **Better:** Official docs + tutorials + troubleshooting + examples

---

### **Use Case 2: News and Current Events**

**Query:** "Latest AI developments 2025"

**Old Results:**
1. techcrunch.com - AI news article 1
2. techcrunch.com - AI news article 2
3. techcrunch.com - AI news article 3
4. techcrunch.com - AI news article 4
5. techcrunch.com - AI news article 5

**New Results:**
1. techcrunch.com - AI startup funding
2. theverge.com - New AI model release
3. arxiv.org - Recent AI research
4. bloomberg.com - AI industry analysis
5. github.com - Popular AI projects

✅ **Better:** Multiple news sources + research + industry analysis

---

### **Use Case 3: Learning and Tutorials**

**Query:** "Learn machine learning basics"

**Old Results:**
1. coursera.org - ML course 1
2. coursera.org - ML course 2
3. coursera.org - ML specialization
4. coursera.org - ML certificate
5. coursera.org - ML fundamentals

**New Results:**
1. coursera.org - ML course
2. kaggle.com - ML tutorials
3. towardsdatascience.com - ML guide
4. youtube.com - ML video series
5. github.com - ML code examples

✅ **Better:** Courses + tutorials + articles + videos + code

---

## Performance Impact

### **API Usage:**

**Before:**
- Request: 5 results
- API calls: 1
- Results used: 5/5 (100%)

**After:**
- Request: 15 results (5 * 3)
- API calls: 1 (same)
- Results used: 5/15 (33%)
- Filtered out: 10 (duplicates from same domains)

**Impact:**
- ✅ Same number of API calls
- ✅ Better quality results
- ⚠️ Slightly more data transfer (15 vs 5 results)
- ⚠️ Slightly more processing (filtering)

**Note:** The diversity multiplier is capped at 20 results to avoid API limits.

---

## Configuration Examples

### **Maximum Diversity (Strict)**

```env
WEB_SEARCH_MAX_PER_DOMAIN=1
WEB_SEARCH_DIVERSITY_MULTIPLIER=4
```

**Result:** Each result from a different domain
**Use when:** You want maximum source diversity
**Trade-off:** May miss some high-quality sources

---

### **Balanced (Default)**

```env
WEB_SEARCH_MAX_PER_DOMAIN=2
WEB_SEARCH_DIVERSITY_MULTIPLIER=3
```

**Result:** Good mix of diversity and quality
**Use when:** General purpose search
**Trade-off:** Best balance

---

### **Quality-Focused (Relaxed)**

```env
WEB_SEARCH_MAX_PER_DOMAIN=3
WEB_SEARCH_DIVERSITY_MULTIPLIER=2
```

**Result:** Allows more from authoritative sources
**Use when:** You trust certain sources more
**Trade-off:** Less diversity, more from top sources

---

## Testing the Improvement

### **How to Test:**

1. **Restart the server** to load new settings
2. **Enable Web Search** in chat
3. **Ask a query** that might have single-source bias:
   - "Python documentation for asyncio"
   - "React hooks tutorial"
   - "Docker best practices"

4. **Check the results** in the response:
   - Look for the diversity note
   - Count unique domains
   - Verify multiple sources

### **Expected Results:**

**Query:** "Python asyncio tutorial"

**Response should include:**
```
Based on web search results from 5 diverse sources:

1. From docs.python.org: [Official documentation]
2. From realpython.com: [Tutorial]
3. From stackoverflow.com: [Q&A]
4. From medium.com: [Blog post]
5. From github.com: [Code examples]
```

---

## Troubleshooting

### **Still Getting Single-Source Results**

**Possible causes:**

1. **Query is too specific**
   - Example: "site:python.org asyncio"
   - Solution: Use more general queries

2. **Max per domain too high**
   - Check: `WEB_SEARCH_MAX_PER_DOMAIN`
   - Solution: Set to 1 or 2

3. **Diversity multiplier too low**
   - Check: `WEB_SEARCH_DIVERSITY_MULTIPLIER`
   - Solution: Increase to 3 or 4

4. **Topic has limited sources**
   - Some topics naturally have fewer sources
   - This is expected behavior

### **Not Enough Results**

**Possible causes:**

1. **Max per domain too strict**
   - Check: `WEB_SEARCH_MAX_PER_DOMAIN=1`
   - Solution: Increase to 2

2. **Diversity multiplier too low**
   - Not enough results to filter from
   - Solution: Increase multiplier

---

## Summary

### **What Changed:**

✅ **Request 3x more results** to filter from  
✅ **Domain-based deduplication** (max 2 per domain)  
✅ **Configurable diversity settings** (2 new env vars)  
✅ **Enhanced logging** (shows source diversity)  
✅ **Improved context formatting** (displays domains)  
✅ **Statistics tracking** (domain distribution)  

### **Benefits:**

✅ **Multiple perspectives** instead of single source  
✅ **Comprehensive coverage** of topics  
✅ **Reduced bias** from diverse sources  
✅ **Better learning** with varied content styles  
✅ **Configurable** to match your needs  

### **Configuration:**

```env
# In .env file:
WEB_SEARCH_MAX_PER_DOMAIN=2          # Max results per domain
WEB_SEARCH_DIVERSITY_MULTIPLIER=3    # Request multiplier
```

---

**Your web search now returns diverse, comprehensive results from multiple sources!** 🌐✨

