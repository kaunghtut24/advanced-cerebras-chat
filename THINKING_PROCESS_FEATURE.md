# Thinking Process Feature

## Overview

The application now displays the **thinking process** (reasoning) from AI models that support it. Users can **show/hide** the thinking content with a clean, collapsible interface.

---

## 🎯 What is the Thinking Process?

Some advanced AI models (like **Llama 3.3 70B**) provide their **internal reasoning** or **chain of thought** before generating the final answer. This helps users:

- 🧠 **Understand how the model arrived at its answer**
- 🔍 **Verify the reasoning process**
- 📚 **Learn from the model's thought process**
- ✅ **Trust the response more**

---

## 🎨 Visual Design

### **Collapsed State (Default):**

```
┌─────────────────────────────────────────────────────┐
│ 🧠 Thinking Process                              ▼ │ ← Click to expand
└─────────────────────────────────────────────────────┘
```

**Features:**
- Purple gradient background
- Brain emoji icon (🧠) with pulse animation
- Collapsed by default (doesn't clutter the chat)
- Click anywhere on the header to expand

---

### **Expanded State:**

```
┌─────────────────────────────────────────────────────┐
│ 🧠 Thinking Process                              ▲ │ ← Click to collapse
├─────────────────────────────────────────────────────┤
│ Let me analyze this question step by step:        │
│                                                     │
│ 1. First, I need to understand what the user is   │
│    asking about...                                 │
│                                                     │
│ 2. Then, I should consider the context...         │
│                                                     │
│ 3. Based on this reasoning, the answer is...      │
└─────────────────────────────────────────────────────┘
```

**Features:**
- White content area with scrollbar
- Full reasoning text displayed
- Max height: 400px (scrollable if longer)
- Clean typography for readability

---

## 🔧 How It Works

### **1. Model Generates Thinking Content**

When using a thinking model (like Llama 3.3 70B), the model provides:
- **Thinking/Reasoning:** Internal thought process
- **Response:** Final answer to the user

### **2. Backend Extracts Thinking**

```python
# In app.py
message = chat_completion.choices[0].message
bot_response = message.content

# Check if the model provided reasoning/thinking content
thinking_content = None
if hasattr(message, 'reasoning_content') and message.reasoning_content:
    thinking_content = message.reasoning_content
    logging.info(f"✓ Thinking content available ({len(thinking_content)} chars)")
```

### **3. Frontend Displays Thinking**

```javascript
// In static/script.js
if (data.thinking) {
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
}
```

### **4. User Toggles Visibility**

```javascript
window.toggleThinking = function(header) {
    const content = container.querySelector('.thinking-content');
    const toggle = header.querySelector('.thinking-toggle');
    
    if (content.style.display === 'none') {
        content.style.display = 'block';
        toggle.textContent = '▲';
    } else {
        content.style.display = 'none';
        toggle.textContent = '▼';
    }
}
```

---

## 📊 Message Flow

### **Complete Conversation Flow:**

```
1. User sends message
   ↓
2. Loading animation appears
   ↓
3. Model processes request
   ↓
4. Model generates:
   - Thinking process (internal reasoning)
   - Final response (answer)
   ↓
5. Loading animation disappears
   ↓
6. Thinking process appears (collapsed)
   🧠 Thinking Process ▼
   ↓
7. Final response appears
   Bot: Here's the answer...
   ↓
8. User can expand thinking to see reasoning
```

---

## 🎨 CSS Styling

### **Container:**

```css
.thinking-container {
    background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
    border-left: 4px solid #667eea;
    border-radius: 8px;
    margin: 10px 0;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

### **Header (Clickable):**

```css
.thinking-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 15px;
    cursor: pointer;
    user-select: none;
    transition: background-color 0.2s ease;
}

.thinking-header:hover {
    background-color: rgba(102, 126, 234, 0.1);
}
```

### **Icon Animation:**

```css
.thinking-icon {
    font-size: 20px;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
        opacity: 1;
    }
    50% {
        transform: scale(1.1);
        opacity: 0.8;
    }
}
```

### **Content Area:**

```css
.thinking-content {
    padding: 15px;
    background-color: #ffffff;
    color: #4a5568;
    font-size: 13px;
    line-height: 1.6;
    white-space: pre-wrap;
    word-wrap: break-word;
    max-height: 400px;
    overflow-y: auto;
}
```

---

## 🔍 Example Usage

### **Example 1: Math Problem**

**User:** "What is 15% of 240?"

**Thinking Process (Collapsed):**
```
🧠 Thinking Process ▼
```

**Click to expand:**
```
🧠 Thinking Process ▲
─────────────────────────────────────
Let me solve this step by step:

1. I need to calculate 15% of 240
2. 15% can be written as 0.15
3. Multiply: 240 × 0.15
4. 240 × 0.15 = 36

Therefore, 15% of 240 is 36.
```

**Final Response:**
```
Bot: 15% of 240 is 36.
```

---

### **Example 2: Complex Question**

**User:** "Should I invest in stocks or bonds right now?"

**Thinking Process (Collapsed):**
```
🧠 Thinking Process ▼
```

**Click to expand:**
```
🧠 Thinking Process ▲
─────────────────────────────────────
This is a complex financial question. Let me think through this:

1. First, I need to consider that I don't know the user's:
   - Risk tolerance
   - Investment timeline
   - Current financial situation
   - Investment goals

2. General considerations:
   - Stocks: Higher risk, higher potential returns
   - Bonds: Lower risk, more stable returns
   - Market conditions vary over time

3. I should provide balanced information without 
   giving specific financial advice.

4. I should recommend consulting a financial advisor.
```

**Final Response:**
```
Bot: The choice between stocks and bonds depends on several 
factors including your risk tolerance, investment timeline, 
and financial goals. Generally, stocks offer higher potential 
returns but with more volatility, while bonds provide more 
stability with lower returns. I recommend consulting with a 
financial advisor who can assess your specific situation.
```

---

## 🎯 Benefits

### **For Users:**

✅ **Transparency** - See how the AI thinks  
✅ **Trust** - Verify the reasoning process  
✅ **Learning** - Understand problem-solving approaches  
✅ **Debugging** - Identify if the AI misunderstood  

### **For Developers:**

✅ **Debugging** - See what the model is thinking  
✅ **Quality Control** - Verify reasoning quality  
✅ **User Feedback** - Users can report reasoning errors  

---

## 🔧 Technical Details

### **Backend (app.py):**

**Lines 580-588:**
```python
# Extract the response content and thinking process
message = chat_completion.choices[0].message
bot_response = message.content

# Check if the model provided reasoning/thinking content
thinking_content = None
if hasattr(message, 'reasoning_content') and message.reasoning_content:
    thinking_content = message.reasoning_content
    logging.info(f"✓ Thinking content available ({len(thinking_content)} chars)")
```

**Lines 604-606:**
```python
# Include thinking content if available
if thinking_content:
    response_data["thinking"] = thinking_content
```

---

### **Frontend (static/script.js):**

**Lines 567-585:**
```javascript
// Show thinking process if available
if (data.thinking) {
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
```

**Lines 520-537:**
```javascript
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
```

---

## 📱 Responsive Design

### **Desktop:**
- Full width thinking container
- Max height: 400px with scrollbar
- Smooth hover effects

### **Mobile:**
- Adapts to screen width
- Touch-friendly header (easy to tap)
- Scrollable content area

---

## ✅ Summary

### **What Changed:**

✅ **Backend** - Extracts thinking/reasoning content from model  
✅ **Frontend** - Displays thinking in collapsible container  
✅ **CSS** - Beautiful gradient design with animations  
✅ **UX** - Click to expand/collapse thinking  

### **Features:**

✅ **Collapsible** - Starts collapsed, doesn't clutter chat  
✅ **Animated** - Pulsing brain icon  
✅ **Scrollable** - Long thinking content scrolls  
✅ **Responsive** - Works on mobile and desktop  
✅ **Accessible** - Clear visual indicators  

### **Supported Models:**

✅ **Llama 3.3 70B** - Provides thinking content  
✅ **Other thinking models** - Automatically detected  
✅ **Regular models** - Thinking section doesn't appear  

---

**The thinking process feature provides transparency and helps users understand how the AI arrives at its answers!** 🧠✨
