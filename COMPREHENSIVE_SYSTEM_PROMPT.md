# Comprehensive System Prompt & Instructions

## Overview

The system prompt has been completely redesigned to provide **stronger, more comprehensive instructions** that ensure the model:
1. **Always uses RAG/Web Search context when provided**
2. **Provides comprehensive, well-structured responses**
3. **Cites all sources properly**
4. **Handles all question types appropriately**

---

## New System Prompt Structure

### **Base System Prompt (Always Active)**

The default system prompt now includes:

#### **1. Core Response Principles**
```
1. COMPREHENSIVENESS: Provide thorough, complete answers
2. ACCURACY: Prioritize factual correctness
3. CLARITY: Use clear language and logical structure
4. CITATIONS: Always cite sources
5. HONESTY: Acknowledge uncertainty when appropriate
```

#### **2. Response Structure Guidelines**
```
- Start with a direct answer
- Provide detailed explanation
- Use markdown formatting
- Include examples when helpful
- End with summary or next steps
```

#### **3. Formatting Guidelines**
```
- Headers (##, ###) for organization
- Bullet points (-) or numbered lists (1., 2., 3.)
- Code blocks (```) for code/commands
- Tables for comparisons
- Blockquotes (>) for important notes
```

#### **4. Response Depth Guidelines**
```
- Simple questions: Concise but complete (2-4 sentences)
- Technical questions: Detailed with examples and code
- Complex questions: Comprehensive with sections and steps
- Comparison questions: Structured with tables/lists
- How-to questions: Step-by-step instructions
```

---

## RAG (Knowledge Base) Instructions

### **When RAG is Enabled:**

The system adds **CRITICAL MANDATORY INSTRUCTIONS**:

```
🔴 CRITICAL - KNOWLEDGE BASE CONTEXT PROVIDED 🔴

ABSOLUTE REQUIREMENTS:
1. READ the entire knowledge base context carefully
2. Your PRIMARY obligation is to answer based on this knowledge base
3. You MUST cite source files: "According to [filename]..."
4. You MUST quote directly when appropriate
5. If KB answers the question: Use ONLY KB content
6. If KB partially answers: Use KB first, supplement with general knowledge
7. If KB doesn't answer: State this explicitly, then provide general knowledge

RESPONSE FORMAT:
- Start with: "Based on the knowledge base..." or "According to [filename]..."
- Cite every piece: "As stated in [filename]..."
- Quote key passages: "The document states: '...'"
- End with: "Source: [list of files used]"
```

### **Visual Presentation:**

```
================================================================================
📚 KNOWLEDGE BASE CONTEXT - READ THIS CAREFULLY:
================================================================================

[Source: refund_policy.pdf]
Our refund policy allows customers to request a full refund within 30 days...

[Source: terms_of_service.pdf]
Refunds are processed within 5-7 business days...

================================================================================
END OF KNOWLEDGE BASE CONTEXT
================================================================================
```

---

## Web Search Instructions

### **When Web Search is Enabled:**

The system adds **WEB SEARCH REQUIREMENTS**:

```
🌐 WEB SEARCH RESULTS PROVIDED 🌐

REQUIREMENTS:
1. INCORPORATE up-to-date information
2. CITE every source with URL: "According to [Source] ([URL])..."
3. PRIORITIZE recent and authoritative sources
4. CROSS-REFERENCE when multiple sources agree
5. NOTE when sources disagree
6. SYNTHESIZE information from multiple sources
7. Include publication dates when available

RESPONSE FORMAT:
- Cite with URLs: "According to TechCrunch (https://...)..."
- Note source types: "According to research from MIT..."
- Synthesize: "Multiple sources (A, B, C) confirm..."
- End with: "Sources: [list with URLs]"
```

### **Visual Presentation:**

```
================================================================================
🔍 WEB SEARCH RESULTS - READ THIS CAREFULLY:
================================================================================

=== WEB SEARCH RESULTS ===
Found 5 results from 5 different sources

[Source 1 - techcrunch.com]
Title: Latest AI Developments
URL: https://techcrunch.com/...
Relevance Score: 0.892
Content: ...

[Source 2 - theverge.com]
Title: AI Industry News
URL: https://theverge.com/...
Relevance Score: 0.856
Content: ...

================================================================================
END OF WEB SEARCH RESULTS
================================================================================
```

---

## Combined RAG + Web Search Instructions

### **When BOTH are Enabled:**

The system adds **SYNTHESIS REQUIREMENTS**:

```
⚡ BOTH KNOWLEDGE BASE AND WEB SEARCH PROVIDED ⚡

SYNTHESIS REQUIREMENTS:
1. START with knowledge base (internal, authoritative)
2. SUPPLEMENT with web search (external, current)
3. CLEARLY distinguish sources:
   - "According to our internal documentation [filename]..."
   - "According to external sources [Source] ([URL])..."
4. SYNTHESIZE for comprehensive answers
5. RESOLVE conflicts by presenting both perspectives
6. CITE ALL sources (both KB files and web URLs)

RESPONSE STRUCTURE:
1. Internal Knowledge: "Based on our knowledge base [filename]..."
2. External Context: "According to external sources [URL]..."
3. Synthesis: "Combining internal documentation with current information..."
4. Sources: "Internal: [files], External: [URLs]"
```

---

## Example Responses

### **Example 1: RAG Only**

**User Question:**
```
What is the refund policy?
```

**Knowledge Base Contains:**
```
[Source: refund_policy.pdf]
Our refund policy allows customers to request a full refund within 30 days
of purchase. Refunds are processed within 5-7 business days after approval.
```

**Expected Response:**
```
Based on the knowledge base, specifically the refund_policy.pdf document:

**Refund Eligibility:**
According to refund_policy.pdf, customers can request a full refund within 
30 days of purchase.

**Processing Time:**
The document states: "Refunds are processed within 5-7 business days after 
approval."

**Summary:**
You have a 30-day window to request a refund, and once approved, you can 
expect the refund to be processed within 5-7 business days.

**Source:** refund_policy.pdf
```

✅ **Perfect:** Uses KB content, cites source, quotes directly, comprehensive

---

### **Example 2: Web Search Only**

**User Question:**
```
What are the latest AI developments in 2025?
```

**Web Search Returns:**
```
[Source 1 - techcrunch.com]
Title: OpenAI Releases GPT-5
URL: https://techcrunch.com/2025/01/15/gpt5-release
Content: OpenAI announced GPT-5 with improved reasoning...

[Source 2 - theverge.com]
Title: Google's New AI Model
URL: https://theverge.com/2025/01/20/google-gemini-ultra
Content: Google released Gemini Ultra with multimodal capabilities...
```

**Expected Response:**
```
Based on current web search results, here are the latest AI developments in 2025:

## Major Model Releases

**1. OpenAI GPT-5**
According to TechCrunch (https://techcrunch.com/2025/01/15/gpt5-release), 
OpenAI announced GPT-5 on January 15, 2025, featuring improved reasoning 
capabilities and better performance on complex tasks.

**2. Google Gemini Ultra**
According to The Verge (https://theverge.com/2025/01/20/google-gemini-ultra), 
Google released Gemini Ultra on January 20, 2025, with advanced multimodal 
capabilities that can process text, images, and video simultaneously.

## Summary

Multiple sources (TechCrunch, The Verge) confirm that early 2025 has seen 
significant AI model releases from major tech companies, with a focus on 
improved reasoning and multimodal capabilities.

**Sources:**
- TechCrunch: https://techcrunch.com/2025/01/15/gpt5-release
- The Verge: https://theverge.com/2025/01/20/google-gemini-ultra
```

✅ **Perfect:** Cites sources with URLs, synthesizes multiple sources, comprehensive

---

### **Example 3: RAG + Web Search Combined**

**User Question:**
```
How does our refund policy compare to industry standards?
```

**Knowledge Base Contains:**
```
[Source: refund_policy.pdf]
Our refund policy allows 30-day returns with full refund.
```

**Web Search Returns:**
```
[Source 1 - retaildive.com]
Industry standard is 14-30 days for refunds
```

**Expected Response:**
```
Let me compare our internal refund policy with industry standards:

## Our Internal Policy

According to our knowledge base (refund_policy.pdf), our refund policy allows 
customers to request a full refund within 30 days of purchase.

## Industry Standards

According to Retail Dive (https://retaildive.com/...), the industry standard 
for refund windows ranges from 14 to 30 days, with most retailers offering 
30 days for standard purchases.

## Comparison

**Our Policy:** 30-day refund window
**Industry Standard:** 14-30 days (typically 30 days)

**Analysis:**
Combining our internal documentation with current industry information, our 
30-day refund policy aligns with the upper end of industry standards, matching 
what most major retailers offer. This positions us competitively in the market.

**Sources:**
- Internal: refund_policy.pdf
- External: Retail Dive (https://retaildive.com/...)
```

✅ **Perfect:** Uses both sources, clearly distinguishes them, synthesizes, comprehensive

---

## Response Quality Standards

### **All Responses Must Meet:**

✅ **Accuracy:** Verified against provided sources  
✅ **Completeness:** Addresses all parts of the question  
✅ **Clarity:** Simple language, avoids unnecessary jargon  
✅ **Structure:** Logically organized with headers/lists  
✅ **Citations:** All information attributed to sources  
✅ **Helpfulness:** Anticipates and addresses follow-up questions  
✅ **Professionalism:** Helpful, respectful tone  

---

## Special Instructions by Question Type

### **Code Questions:**
```
- Provide working code with explanations
- Include comments in code
- Show expected output
- Mention language/version requirements
- Provide alternative approaches when relevant
```

### **Troubleshooting Questions:**
```
- Offer multiple solutions, ranked by likelihood
- Provide step-by-step debugging steps
- Explain why each solution might work
- Include prevention tips
```

### **Comparison Questions:**
```
- Present balanced views
- Use tables for side-by-side comparison
- List pros and cons
- Provide recommendation based on use case
```

### **Definition Questions:**
```
- Provide clear, concise definition
- Include examples
- Explain context and usage
- Mention related concepts
```

### **Procedure/How-To Questions:**
```
- Give step-by-step instructions
- Number each step
- Explain expected outcome for each step
- Include troubleshooting tips
- Provide verification steps
```

---

## Visual Indicators in System Prompt

The new system prompt uses **visual indicators** to grab attention:

```
🔴 CRITICAL - KNOWLEDGE BASE CONTEXT PROVIDED 🔴
🌐 WEB SEARCH RESULTS PROVIDED 🌐
⚡ BOTH KNOWLEDGE BASE AND WEB SEARCH PROVIDED ⚡
📚 KNOWLEDGE BASE CONTEXT - READ THIS CAREFULLY
🔍 WEB SEARCH RESULTS - READ THIS CAREFULLY
```

These emojis and formatting make it **impossible for the model to miss** the context.

---

## Benefits of New System Prompt

### **Before:**
❌ Weak instructions ("Please use when relevant")  
❌ Easy to ignore context  
❌ Inconsistent citation format  
❌ Variable response quality  
❌ No clear structure guidelines  

### **After:**
✅ **MANDATORY instructions** ("YOU MUST...")  
✅ **Impossible to ignore** (visual indicators, clear sections)  
✅ **Consistent citations** (specific formats required)  
✅ **High-quality responses** (quality standards defined)  
✅ **Clear structure** (formatting guidelines provided)  

---

## Configuration

### **Default System Prompt Location:**

The default prompt is defined in `static/script.js`:

```javascript
const DEFAULT_SYSTEM_PROMPT = `...comprehensive instructions...`;
```

### **Users Can Customize:**

Users can edit the system prompt in Settings:
1. Click Settings (⚙️)
2. Edit "System Prompt" textarea
3. Click "Save Settings"

### **Reset to Default:**

Users can reset to the new comprehensive prompt:
1. Click "Reset to Default" button
2. Confirms reset
3. Saves automatically

---

## Testing the New System Prompt

### **Test 1: RAG Usage**

1. Upload a document with specific information
2. Enable RAG
3. Ask a question answered in the document
4. **Expected:** Response starts with "Based on the knowledge base..." and cites source

### **Test 2: Web Search Usage**

1. Enable Web Search
2. Ask about current events
3. **Expected:** Response cites sources with URLs

### **Test 3: Combined RAG + Web Search**

1. Enable both RAG and Web Search
2. Ask a question that needs both
3. **Expected:** Response clearly distinguishes internal vs external sources

### **Test 4: Comprehensive Responses**

1. Ask a complex technical question
2. **Expected:** Well-structured response with headers, code blocks, examples

---

## Summary

### **What Changed:**

✅ **Comprehensive base instructions** (response principles, formatting, depth)  
✅ **MANDATORY RAG instructions** (must use KB, must cite, must quote)  
✅ **Strong web search instructions** (must cite URLs, must synthesize)  
✅ **Synthesis requirements** (when both RAG and web search active)  
✅ **Visual indicators** (🔴🌐⚡📚🔍 to grab attention)  
✅ **Quality standards** (accuracy, completeness, clarity, citations)  
✅ **Question-type specific guidance** (code, troubleshooting, comparisons, etc.)  

### **What You Get:**

✅ **Model ALWAYS uses RAG/Web Search context**  
✅ **Comprehensive, well-structured responses**  
✅ **Proper citations with sources**  
✅ **Appropriate depth for question type**  
✅ **Professional, helpful tone**  
✅ **Consistent high quality**  

---

**The model now has crystal-clear, mandatory instructions for handling all types of questions with maximum comprehensiveness!** 🎯✨
