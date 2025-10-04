# RAG Settings Location Guide

## Where to Find RAG Settings

The RAG settings are located in the **Settings Panel** and are now properly styled with clear section headers.

---

## How to Access RAG Settings

### **Step 1: Open Settings**
1. Click the **⚙️ Settings** button in the top-right corner of the chat interface
2. The settings panel will open as a modal

### **Step 2: Scroll to RAG Settings**
The settings panel has three sections:
- **Header** (fixed at top) - "Settings" title
- **Body** (scrollable) - All settings fields
- **Footer** (fixed at bottom) - "Reset All" and "Save Settings" buttons

**RAG Settings are in the scrollable body section**, after:
- Model selection
- System Prompt
- Temperature
- Max Tokens

---

## Settings Panel Layout

```
┌─────────────────────────────────────────┐
│  Settings                               │  ← Fixed Header
├─────────────────────────────────────────┤
│  Model: [dropdown]                      │
│  System Prompt: [textarea]              │
│  Temperature: [slider]                  │
│  Max Tokens: [input]                    │
│                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  RAG Settings                           │  ← Section Header (Blue)
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  ☑ Enable RAG                           │
│  Knowledge Base: [dropdown]             │
│  [Manage Knowledge Bases]               │
│                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Web Search Settings                    │  ← Section Header (Blue)
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  ☑ Enable Web Search                    │
│  ↕ (scrollable)                         │
├─────────────────────────────────────────┤
│  [Reset All]        [Save Settings]     │  ← Fixed Footer
└─────────────────────────────────────────┘
```

---

## RAG Settings Section Details

### **Section Header**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RAG Settings
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
- **Blue text** (#1a73e8)
- **Blue underline** (2px solid)
- **Clear visual separation**

### **Controls**

#### 1. **Enable RAG Checkbox**
```
☑ Enable RAG
```
- Toggle RAG on/off
- Syncs with quick toggle button

#### 2. **Knowledge Base Dropdown**
```
Knowledge Base: [Select KB... ▼]
```
- Lists all available knowledge bases
- Shows "None (No RAG)" if no KB selected
- Syncs with quick toggle dropdown

#### 3. **Manage Knowledge Bases Button**
```
[Manage Knowledge Bases]
```
- Opens knowledge base management modal
- Create, delete, upload files
- Blue button with white text

---

## Visual Improvements Made

### **Before:**
- No clear section headers
- Hard to find RAG settings
- Buttons not styled consistently
- Unclear hierarchy

### **After:**
✅ **Clear section headers** with blue underlines  
✅ **Consistent button styling** (blue primary buttons)  
✅ **Better visual hierarchy**  
✅ **Easy to scan and find settings**  

---

## Styling Details

### **Section Headers (h3)**
```css
.form-group h3 {
    margin: 15px 0 10px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid #1a73e8;
    color: #1a73e8;
    font-size: 16px;
}
```

### **Buttons**
```css
.form-group button {
    margin-top: 10px;
    padding: 8px 16px;
    background-color: #1a73e8;
    color: white;
    border: none;
    border-radius: 4px;
}
```

---

## Quick Access Alternative

You can also use the **Quick Toggle Buttons** above the chat input:

```
┌──────────────────────────────────────────────────────┐
│  📚 RAG [OFF] [Select KB...▼]  🌐 Web Search [OFF]  │
├──────────────────────────────────────────────────────┤
│  Type your message here...                     [Send]│
└──────────────────────────────────────────────────────┘
```

**Quick toggles provide:**
- Instant enable/disable
- Knowledge base selection
- No need to open settings
- Always visible

---

## Complete Settings Workflow

### **Method 1: Using Settings Panel**

1. **Open Settings** (⚙️ button)
2. **Scroll down** to "RAG Settings" section
3. **Check "Enable RAG"**
4. **Select Knowledge Base** from dropdown
5. **Click "Manage Knowledge Bases"** to create/upload (if needed)
6. **Click "Save Settings"** at bottom

### **Method 2: Using Quick Toggles**

1. **Click dropdown** next to 📚 RAG
2. **Select knowledge base**
3. RAG automatically enables
4. Start chatting!

---

## Troubleshooting

### **Can't See RAG Settings**

**Issue:** Settings panel doesn't show RAG section

**Solutions:**

1. **Scroll down** in the settings panel
   - The panel is scrollable
   - RAG settings are below basic settings

2. **Check if RAG is available**
   - Look at server startup logs
   - Should see: "RAG service initialized: Available"

3. **Refresh the page**
   - Press F5 or Ctrl+R
   - Reopen settings

### **RAG Settings Grayed Out**

**Issue:** Can't interact with RAG settings

**Possible Causes:**
- RAG service not available
- Dependencies not installed
- Qdrant not initialized

**Check:**
```bash
# In terminal where server is running:
# Look for:
INFO:root:RAG service initialized: Available
```

### **No Knowledge Bases in Dropdown**

**Issue:** Dropdown shows only "None (No RAG)"

**Solution:**
1. Click **"Manage Knowledge Bases"** button
2. Create a new knowledge base
3. Upload documents
4. Close modal
5. Dropdown will now show your KB

---

## Settings Panel Sections Summary

| Section | Location | Contents |
|---------|----------|----------|
| **Header** | Top (fixed) | "Settings" title |
| **Model** | Body (top) | Model selection, info |
| **System Prompt** | Body | Prompt textarea, reset button |
| **Temperature** | Body | Slider (0-1) |
| **Max Tokens** | Body | Number input |
| **RAG Settings** | Body | Enable checkbox, KB dropdown, manage button |
| **Web Search** | Body | Enable checkbox |
| **Footer** | Bottom (fixed) | Reset All, Save Settings |

---

## Screenshots Reference

### **Settings Panel - RAG Section**
```
┌─────────────────────────────────────┐
│  Max Tokens: [1024        ]         │
│                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  RAG Settings                       │  ← Blue header
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                     │
│  ☑ Enable RAG                       │  ← Checkbox
│                                     │
│  Knowledge Base:                    │  ← Label
│  [my_documents          ▼]          │  ← Dropdown
│                                     │
│  [Manage Knowledge Bases]           │  ← Blue button
│                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Web Search Settings                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
└─────────────────────────────────────┘
```

---

## Summary

### **RAG Settings Location:**
✅ **Settings Panel** → Scroll down → **"RAG Settings"** section  
✅ **Quick Toggles** → Above chat input → **📚 RAG** button  

### **What You Can Do:**
✅ Enable/disable RAG  
✅ Select knowledge base  
✅ Manage knowledge bases (create, delete, upload)  
✅ Quick access via toggles  

### **Visual Improvements:**
✅ Clear blue section headers  
✅ Consistent button styling  
✅ Better organization  
✅ Easy to find and use  

---

**The RAG settings are there and now beautifully styled!** 🎨✨
