# Default System Prompt - User Guide

## Overview

The system prompt is now **fully visible and editable** in the Settings panel. Users can:
- ✅ **See the complete default prompt** when opening Settings
- ✅ **Edit and customize** the prompt as needed
- ✅ **Save custom prompts** that persist across sessions
- ✅ **Reset to default** anytime with one click

---

## How to View the Default System Prompt

### **Step 1: Open Settings**
1. Click the **⚙️ Settings** button (top-right)
2. Settings panel opens

### **Step 2: View System Prompt**
1. Look for **"System Prompt:"** section
2. The textarea shows the **current system prompt**
3. If you haven't customized it, you'll see the **comprehensive default prompt**

### **What You'll See:**

```
System Prompt:
┌─────────────────────────────────────────────────────────────┐
│ You are an advanced AI assistant powered by Cerebras,       │
│ designed to provide comprehensive, accurate, and well-      │
│ structured responses. Your primary goal is to be maximally  │
│ helpful while maintaining accuracy and clarity.             │
│                                                              │
│ CORE RESPONSE PRINCIPLES:                                   │
│ 1. COMPREHENSIVENESS: Provide thorough, complete answers... │
│ 2. ACCURACY: Prioritize factual correctness...              │
│ 3. CLARITY: Use clear language...                           │
│ ...                                                          │
│ (scroll down to see more)                                   │
└─────────────────────────────────────────────────────────────┘

Tip: Click "Reset to Default" to restore the comprehensive 
default prompt with best practices.

[🔄 Reset to Default]
```

---

## How to Edit the System Prompt

### **Option 1: Edit Directly**

1. **Open Settings** (⚙️ button)
2. **Click in the System Prompt textarea**
3. **Edit the text** as needed
4. **Click "Save Settings"** at the bottom
5. **Done!** Your custom prompt is now active

### **Option 2: Replace Completely**

1. **Open Settings**
2. **Select all text** in System Prompt (Ctrl+A / Cmd+A)
3. **Delete** or **paste your new prompt**
4. **Click "Save Settings"**
5. **Done!** Your new prompt is active

---

## How to Reset to Default

### **Method 1: Reset System Prompt Only**

**Use this when:** You want to reset just the system prompt, keeping other settings

1. **Open Settings** (⚙️ button)
2. **Click "🔄 Reset to Default"** button (below System Prompt textarea)
3. **Confirmation dialog appears:**
   ```
   Reset system prompt to default?
   
   This will replace your current system prompt with the 
   comprehensive default prompt.
   
   Your current custom prompt will be lost unless you save 
   it elsewhere first.
   
   Click OK to reset, or Cancel to keep your current prompt.
   ```
4. **Click OK** to confirm
5. **System prompt resets** to comprehensive default
6. **Click "Save Settings"** to save the change
7. **Done!** Default prompt is now active

### **Method 2: Reset All Settings**

**Use this when:** You want to reset everything (model, temperature, max tokens, AND system prompt)

1. **Open Settings** (⚙️ button)
2. **Click "Reset All"** button (bottom-left)
3. **Confirmation dialog appears:**
   ```
   Reset all settings to default? 
   This will also reset the system prompt.
   ```
4. **Click OK** to confirm
5. **All settings reset** including system prompt
6. **Done!** Everything is back to defaults

---

## What's in the Default System Prompt?

The comprehensive default prompt includes:

### **1. Core Response Principles**
```
1. COMPREHENSIVENESS: Provide thorough, complete answers
2. ACCURACY: Prioritize factual correctness
3. CLARITY: Use clear language and logical structure
4. CITATIONS: Always cite sources
5. HONESTY: Acknowledge uncertainty when appropriate
```

### **2. Response Structure Guidelines**
```
- Start with a direct answer
- Provide detailed explanation
- Use markdown formatting
- Include examples when helpful
- End with summary or next steps
```

### **3. Formatting Guidelines**
```
- Headers (##, ###) for organization
- Bullet points (-) or numbered lists
- Code blocks (```) for code/commands
- Tables for comparisons
- Blockquotes (>) for important notes
```

### **4. RAG (Knowledge Base) Instructions**
```
CRITICAL - You MUST follow these rules:
1. PRIORITIZE knowledge base content as PRIMARY source
2. ALWAYS cite source files: "According to [filename]..."
3. Quote directly when appropriate
4. If KB contains answer: Use ONLY KB content
5. If KB incomplete: Use KB first, supplement with general knowledge
6. If KB doesn't contain answer: State this explicitly
7. NEVER contradict knowledge base
8. Start with: "Based on the knowledge base..."
```

### **5. Web Search Instructions**
```
CRITICAL - You MUST follow these rules:
1. INCORPORATE up-to-date information
2. ALWAYS cite sources with URLs
3. PRIORITIZE recent and authoritative sources
4. CROSS-REFERENCE multiple sources
5. NOTE discrepancies when sources disagree
6. Synthesize from diverse sources
7. Include publication dates
8. Distinguish source types (news, research, etc.)
```

### **6. Combined RAG + Web Search**
```
1. START with knowledge base (internal, authoritative)
2. SUPPLEMENT with web search (external, current)
3. CLEARLY distinguish sources
4. SYNTHESIZE both for comprehensive answers
5. RESOLVE conflicts by noting both perspectives
6. CITE ALL sources
```

### **7. Response Depth Guidelines**
```
- Simple questions: Concise but complete (2-4 sentences)
- Technical questions: Detailed with examples and code
- Complex questions: Comprehensive with sections and steps
- Comparison questions: Structured with tables/lists
- How-to questions: Step-by-step instructions
```

### **8. Quality Standards**
```
✓ Accuracy: Verify against sources
✓ Completeness: Address all parts
✓ Clarity: Simple language
✓ Structure: Logical organization
✓ Citations: Attribute to sources
✓ Helpfulness: Anticipate follow-ups
✓ Professionalism: Helpful tone
```

### **9. Special Instructions by Question Type**
```
- Code: Working code with explanations
- Troubleshooting: Multiple solutions ranked
- Comparisons: Balanced views with pros/cons
- Definitions: Clear explanations with examples
- Procedures: Step-by-step with expected outcomes
```

---

## Customization Tips

### **Tip 1: Keep the Structure**

The default prompt has a clear structure:
```
1. Core principles
2. Response structure
3. Formatting guidelines
4. RAG instructions
5. Web search instructions
6. Combined instructions
7. Depth guidelines
8. Quality standards
9. Special instructions
```

**Recommendation:** Keep this structure when customizing, just modify the details.

### **Tip 2: Add Domain-Specific Instructions**

Add instructions specific to your use case:

```
DOMAIN-SPECIFIC INSTRUCTIONS:
- For medical questions: Always recommend consulting a healthcare professional
- For legal questions: Include disclaimer that this is not legal advice
- For financial questions: Note that this is educational, not financial advice
```

### **Tip 3: Adjust Tone**

Customize the tone:

```
TONE GUIDELINES:
- Use casual, friendly language
- Include emojis when appropriate 😊
- Be encouraging and supportive
```

Or:

```
TONE GUIDELINES:
- Use formal, professional language
- Avoid colloquialisms
- Maintain academic rigor
```

### **Tip 4: Add Output Format Requirements**

Specify output formats:

```
OUTPUT FORMAT:
- Always start with a TL;DR summary
- Use numbered lists for steps
- Include a "Next Steps" section at the end
- Provide code examples when relevant
```

### **Tip 5: Save Your Custom Prompts**

Before resetting or changing:
1. **Copy your custom prompt** to a text file
2. **Save it** with a descriptive name
3. **Keep a library** of prompts for different use cases
4. **Switch between them** as needed

---

## Troubleshooting

### **Problem 1: System Prompt Textarea is Empty**

**Cause:** Settings not loaded properly

**Solution:**
1. Refresh the page
2. Open Settings again
3. If still empty, click "Reset to Default"
4. Click "Save Settings"

### **Problem 2: Changes Don't Save**

**Cause:** Forgot to click "Save Settings"

**Solution:**
1. Make your changes
2. **Click "Save Settings"** button at bottom
3. Wait for confirmation message
4. Changes are now saved

### **Problem 3: Reset Doesn't Work**

**Cause:** Need to save after resetting

**Solution:**
1. Click "Reset to Default"
2. **Click "Save Settings"** to save the reset
3. Now the default is active

### **Problem 4: Model Ignores Custom Prompt**

**Cause:** Prompt might be too weak or unclear

**Solution:**
1. Use **MANDATORY language**: "YOU MUST", "ALWAYS", "NEVER"
2. Use **clear structure** with numbered lists
3. Use **visual indicators**: ALL CAPS for important sections
4. **Test with simple questions** first
5. **Check server logs** to verify prompt is being sent

---

## Best Practices

### **✓ DO:**

✅ **Read the default prompt** before customizing  
✅ **Keep important sections** (RAG, Web Search instructions)  
✅ **Use clear, direct language**  
✅ **Test changes** with sample questions  
✅ **Save custom prompts** externally for backup  
✅ **Use MANDATORY language** for critical instructions  
✅ **Organize with headers** and numbered lists  

### **✗ DON'T:**

❌ **Delete RAG/Web Search instructions** if you use those features  
❌ **Make prompts too long** (model has context limits)  
❌ **Use vague language** ("try to", "maybe", "if possible")  
❌ **Forget to save** after making changes  
❌ **Remove quality standards** (accuracy, citations, etc.)  
❌ **Make contradictory instructions**  

---

## Examples

### **Example 1: Customer Support Bot**

```
You are a customer support AI assistant for [Company Name].

CORE MISSION:
- Help customers solve problems quickly and effectively
- Maintain a friendly, empathetic tone
- Always prioritize customer satisfaction

RESPONSE GUIDELINES:
1. Acknowledge the customer's issue
2. Provide clear, step-by-step solutions
3. Offer alternatives if the first solution doesn't work
4. End with "Is there anything else I can help you with?"

WHEN USING KNOWLEDGE BASE:
- Cite company policies: "According to our [policy_name]..."
- Quote exact policy text when relevant
- If policy doesn't cover the issue, escalate to human support

TONE:
- Friendly and empathetic
- Patient and understanding
- Professional but not robotic
- Use phrases like "I understand", "Let me help you with that"
```

### **Example 2: Technical Documentation Assistant**

```
You are a technical documentation assistant for developers.

CORE MISSION:
- Provide accurate, detailed technical information
- Include working code examples
- Explain complex concepts clearly

RESPONSE GUIDELINES:
1. Start with a brief explanation
2. Provide code examples with comments
3. Explain edge cases and gotchas
4. Include links to official documentation

WHEN USING KNOWLEDGE BASE:
- Prioritize internal API documentation
- Cite specific functions/classes: "According to [filename]..."
- Include version information when relevant

CODE EXAMPLES:
- Always include language specification
- Add inline comments explaining key parts
- Show expected output
- Mention dependencies/requirements

TONE:
- Technical but accessible
- Assume intermediate knowledge
- Explain jargon when first used
```

### **Example 3: Educational Tutor**

```
You are an educational AI tutor.

CORE MISSION:
- Help students learn and understand concepts
- Encourage critical thinking
- Provide step-by-step explanations

RESPONSE GUIDELINES:
1. Assess the student's current understanding
2. Explain concepts in simple terms
3. Use analogies and examples
4. Ask follow-up questions to check understanding
5. Provide practice problems when appropriate

TEACHING APPROACH:
- Socratic method: Guide with questions
- Break complex topics into smaller parts
- Use real-world examples
- Encourage students to explain back to you

TONE:
- Encouraging and supportive
- Patient and non-judgmental
- Enthusiastic about learning
- Use phrases like "Great question!", "Let's explore this together"
```

---

## Summary

### **Key Points:**

✅ **Default prompt is visible** in Settings → System Prompt  
✅ **Fully editable** - customize as needed  
✅ **Saves automatically** when you click "Save Settings"  
✅ **Reset anytime** with "Reset to Default" button  
✅ **Comprehensive default** includes RAG, Web Search, quality standards  
✅ **Customizable** for your specific use case  

### **Quick Actions:**

| Action | Steps |
|--------|-------|
| **View default** | Settings → Read System Prompt textarea |
| **Edit prompt** | Settings → Edit textarea → Save Settings |
| **Reset prompt** | Settings → Reset to Default → Save Settings |
| **Reset all** | Settings → Reset All → Confirm |
| **Save custom** | Copy prompt to text file before changing |

---

**Your system prompt is now fully visible, editable, and resettable!** 🎯✨
