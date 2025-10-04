# Loading Animation Feature

## Overview

The application now shows an **animated loading indicator** while the AI model is processing your request. This is especially useful when **web search is enabled**, as it can take several seconds to search the web and generate a response.

---

## What You'll See

### **Standard Loading (No Web Search)**

When you send a message, you'll see:

```
┌─────────────────────────────────────────┐
│ User: What is the refund policy?        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ● ● ●  Thinking...                      │ ← Animated dots
└─────────────────────────────────────────┘
```

**Animation:**
- Three blue dots bouncing up and down
- Text: "Thinking..."
- Light gray background

---

### **With RAG Enabled**

When RAG (knowledge base) is enabled:

```
┌─────────────────────────────────────────┐
│ User: What is the refund policy?        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ● ● ●  Searching knowledge base...      │ ← Animated dots
└─────────────────────────────────────────┘
```

**Animation:**
- Three blue dots bouncing
- Text: "Searching knowledge base..."
- Light gray background

---

### **With Web Search Enabled**

When web search is enabled:

```
┌─────────────────────────────────────────┐
│ User: What are the latest AI news?     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ● ● ●  Searching the web...             │ ← Animated dots + pulse
└─────────────────────────────────────────┘
```

**Animation:**
- Three blue dots bouncing
- Text: "Searching the web..."
- **Pulsing blue gradient background** (indicates web search)

---

### **With Both RAG and Web Search**

When both are enabled:

```
┌─────────────────────────────────────────┐
│ User: Compare our policy to industry?  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ● ● ●  Searching web and knowledge      │ ← Animated dots + pulse
│         base...                          │
└─────────────────────────────────────────┘
```

**Animation:**
- Three blue dots bouncing
- Text: "Searching web and knowledge base..."
- **Pulsing blue gradient background**

---

## Animation Details

### **Bouncing Dots Animation**

The three dots bounce in sequence:

```
Frame 1:  ●  ○  ○
Frame 2:  ○  ●  ○
Frame 3:  ○  ○  ●
Frame 4:  ●  ○  ○
...
```

**Specifications:**
- **Dot size:** 8px diameter
- **Dot color:** Blue (#1a73e8)
- **Animation duration:** 1.4 seconds
- **Animation type:** Bounce (scale + opacity)
- **Stagger delay:** 0.16s between dots

---

### **Pulsing Background (Web Search)**

When web search is active, the background pulses:

```
Frame 1:  [Gray ────────────────────]
Frame 2:  [Gray ──── Blue ──────────]
Frame 3:  [Gray ──────────── Blue ──]
Frame 4:  [Gray ────────────────────]
...
```

**Specifications:**
- **Gradient:** Gray → Light Blue → Gray
- **Animation duration:** 2 seconds
- **Animation type:** Smooth gradient shift
- **Direction:** Left to right and back

---

## When Does It Appear?

### **Timing:**

1. **User sends message** → Message appears
2. **Loading animation starts** → Immediately
3. **Request sent to server** → Processing
4. **Response received** → Loading animation removed
5. **Bot response appears** → Final result shown

### **Duration:**

| Scenario | Typical Duration |
|----------|------------------|
| **Simple question** | 1-2 seconds |
| **With RAG** | 2-4 seconds |
| **With Web Search** | 5-10 seconds |
| **With Both** | 8-15 seconds |

---

## Visual Examples

### **Example 1: Quick Response**

```
[10:30:45] User: Hello
[10:30:45] ● ● ● Thinking...
[10:30:46] Bot: Hello! How can I help you today?
           ↑ 1 second
```

---

### **Example 2: RAG Search**

```
[10:31:00] User: What is the refund policy?
[10:31:00] ● ● ● Searching knowledge base...
[10:31:03] Bot: Based on the knowledge base (refund_policy.pdf)...
           ↑ 3 seconds
```

---

### **Example 3: Web Search**

```
[10:32:00] User: What are the latest AI developments?
[10:32:00] ● ● ● Searching the web...
           [Pulsing blue background]
[10:32:08] Bot: According to TechCrunch (https://...)...
           ↑ 8 seconds
```

---

### **Example 4: Both RAG and Web Search**

```
[10:33:00] User: How does our policy compare to industry standards?
[10:33:00] ● ● ● Searching web and knowledge base...
           [Pulsing blue background]
[10:33:12] Bot: Based on our knowledge base (policy.pdf) and 
               external sources (RetailDive.com)...
           ↑ 12 seconds
```

---

## Technical Details

### **CSS Animation - Bouncing Dots**

```css
.loading-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #1a73e8;
    animation: loading-bounce 1.4s infinite ease-in-out both;
}

.loading-dot:nth-child(1) {
    animation-delay: -0.32s;
}

.loading-dot:nth-child(2) {
    animation-delay: -0.16s;
}

@keyframes loading-bounce {
    0%, 80%, 100% {
        transform: scale(0.8);
        opacity: 0.5;
    }
    40% {
        transform: scale(1.2);
        opacity: 1;
    }
}
```

---

### **CSS Animation - Pulsing Background**

```css
.loading-message.web-search {
    background: linear-gradient(90deg, #f5f5f5 0%, #e3f2fd 50%, #f5f5f5 100%);
    background-size: 200% 100%;
    animation: loading-pulse 2s ease-in-out infinite;
}

@keyframes loading-pulse {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}
```

---

### **JavaScript Implementation**

```javascript
// Show loading animation
function showLoadingAnimation(isWebSearch = false) {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message-container bot-message-container';
    loadingDiv.id = 'loading-animation';
    
    const loadingMessage = document.createElement('div');
    loadingMessage.className = `loading-message ${isWebSearch ? 'web-search' : ''}`;
    
    // Determine loading text based on what's enabled
    let loadingText = 'Thinking';
    if (isWebSearch && ragEnabled) {
        loadingText = 'Searching web and knowledge base';
    } else if (isWebSearch) {
        loadingText = 'Searching the web';
    } else if (ragEnabled) {
        loadingText = 'Searching knowledge base';
    }
    
    loadingMessage.innerHTML = `
        <div class="loading-spinner">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
        <div class="loading-text">${loadingText}...</div>
    `;
    
    loadingDiv.appendChild(loadingMessage);
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return loadingDiv;
}

// Remove loading animation
function removeLoadingAnimation() {
    const loadingDiv = document.getElementById('loading-animation');
    if (loadingDiv) {
        loadingDiv.remove();
    }
}
```

---

## User Experience Benefits

### **1. Visual Feedback**
✅ **Users know the system is working**  
✅ **No confusion about whether request was received**  
✅ **Clear indication of what's happening**  

### **2. Patience Management**
✅ **Users are more patient when they see progress**  
✅ **Reduces anxiety during long waits**  
✅ **Sets expectations for response time**  

### **3. Context Awareness**
✅ **Different messages for different operations**  
✅ **Web search gets special pulsing animation**  
✅ **Users understand why it's taking longer**  

### **4. Professional Appearance**
✅ **Smooth, polished animations**  
✅ **Consistent with modern UI standards**  
✅ **Enhances perceived quality**  

---

## Accessibility

### **Screen Readers:**
- Loading text is readable: "Thinking...", "Searching the web...", etc.
- Animation is purely visual (doesn't interfere with screen readers)

### **Motion Sensitivity:**
- Animations are subtle (not jarring)
- Can be disabled via browser settings (respects `prefers-reduced-motion`)

### **Color Contrast:**
- Blue dots on gray background: Good contrast
- Text is dark gray on light background: Excellent contrast

---

## Troubleshooting

### **Problem 1: Animation Doesn't Appear**

**Cause:** JavaScript error or very fast response

**Solution:**
1. Check browser console for errors
2. If response is very fast (<100ms), animation might not be visible
3. This is normal and expected

---

### **Problem 2: Animation Doesn't Disappear**

**Cause:** Error in response handling

**Solution:**
1. Refresh the page
2. Check browser console for errors
3. Animation should auto-remove on error

---

### **Problem 3: Wrong Loading Message**

**Cause:** RAG/Web Search toggles not synced

**Solution:**
1. Check quick toggle buttons
2. Verify RAG and Web Search states
3. Refresh page if needed

---

## Summary

### **What You Get:**

✅ **Bouncing dots animation** - Visual feedback  
✅ **Context-aware messages** - Know what's happening  
✅ **Pulsing background for web search** - Special indicator  
✅ **Automatic show/hide** - No manual intervention  
✅ **Error handling** - Removes on error  
✅ **Smooth animations** - Professional appearance  

### **Loading Messages:**

| Scenario | Message |
|----------|---------|
| **Standard** | "Thinking..." |
| **RAG only** | "Searching knowledge base..." |
| **Web Search only** | "Searching the web..." |
| **Both** | "Searching web and knowledge base..." |

### **Visual Indicators:**

| Feature | Indicator |
|---------|-----------|
| **Bouncing dots** | Always present |
| **Pulsing background** | Only with web search |
| **Blue color** | Matches app theme |

---

**The loading animation provides clear visual feedback and improves user experience, especially during longer web searches!** ⏳✨
