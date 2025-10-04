# Chat History Management - Edit & Delete Feature

## Overview

You can now **edit and delete chat histories** directly from the sessions panel. Each chat session has compact action buttons that appear when you hover over it.

---

## Features

### **1. Edit Chat Title** ✏️
Rename any chat session with a custom title.

### **2. Export Chat** 💾
Download chat history as a JSON file.

### **3. Delete Chat** 🗑️
Permanently delete a chat session.

---

## How to Use

### **View Action Buttons**

1. **Open Sessions Panel**
   - Click the **☰** menu icon (top-left)
   - Sessions panel slides in from the left

2. **Hover Over a Chat Session**
   - Move your mouse over any chat in the list
   - **Three small buttons appear** at the bottom:
     ```
     ┌─────────────────────────────────────┐
     │ How to use RAG feature?             │
     │ 5 messages                          │
     │ [✏️] [💾] [🗑️]                      │
     └─────────────────────────────────────┘
     ```

3. **Button Functions**
   - **✏️** = Edit title
   - **💾** = Export chat
   - **🗑️** = Delete chat

---

## Edit Chat Title

### **Steps:**

1. **Hover over the chat** you want to rename
2. **Click the ✏️ button**
3. **Input field appears** with current title
   ```
   ┌─────────────────────────────────────┐
   │ [How to use RAG feature?          ] │
   │ 5 messages                          │
   │ [✓] [✗]                             │
   └─────────────────────────────────────┘
   ```
4. **Type new title** in the input field
5. **Click ✓** to save or **✗** to cancel
6. **Done!** Title is updated

### **Keyboard Shortcuts:**
- **Enter** = Save
- **Escape** = Cancel

### **Example:**

**Before:**
```
What is the refund policy?
3 messages
```

**After editing:**
```
Company Refund Policy Info
3 messages
```

---

## Export Chat

### **Steps:**

1. **Hover over the chat** you want to export
2. **Click the 💾 button**
3. **File downloads automatically** as `chat_YYYYMMDD_HHMMSS.json`
4. **Success message** appears: "✓ Chat session exported successfully"

### **What's Exported:**

The JSON file contains:
```json
{
  "session_id": "20250104_143022",
  "history": [
    {
      "role": "user",
      "content": "What is the refund policy?"
    },
    {
      "role": "assistant",
      "content": "Based on the knowledge base..."
    }
  ],
  "settings": {
    "model": "llama-4-scout-17b-16e-instruct",
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

### **Use Cases:**

✅ **Backup important conversations**  
✅ **Share chats with team members**  
✅ **Archive project discussions**  
✅ **Import into other tools**  
✅ **Keep records for compliance**  

---

## Delete Chat

### **Steps:**

1. **Hover over the chat** you want to delete
2. **Click the 🗑️ button**
3. **Confirmation dialog appears:**
   ```
   Delete chat session?
   
   Title: How to use RAG feature?
   
   This action cannot be undone. All messages in this chat 
   will be permanently deleted.
   
   Click OK to delete, or Cancel to keep the chat.
   ```
4. **Click OK** to confirm deletion
5. **Chat is deleted** and removed from the list
6. **Success message** appears: "✓ Chat session deleted successfully"

### **Important Notes:**

⚠️ **Deletion is permanent** - Cannot be undone  
⚠️ **All messages are lost** - Export first if you need a backup  
⚠️ **If deleting current chat** - A new chat session is created automatically  

---

## Visual Guide

### **Normal State (Not Hovering):**
```
┌─────────────────────────────────────┐
│ How to use RAG feature?             │
│ 5 messages                          │
│                                     │
└─────────────────────────────────────┘
```

### **Hover State (Buttons Visible):**
```
┌─────────────────────────────────────┐
│ How to use RAG feature?             │
│ 5 messages                          │
│ [✏️] [💾] [🗑️]                      │ ← Buttons appear
└─────────────────────────────────────┘
```

### **Edit Mode:**
```
┌─────────────────────────────────────┐
│ [RAG Feature Tutorial             ] │ ← Input field
│ 5 messages                          │
│ [✓] [✗]                             │ ← Save/Cancel
└─────────────────────────────────────┘
```

---

## Button Design

### **Size & Style:**

- **Very compact** - Only icons, no text
- **Small padding** - 2px vertical, 6px horizontal
- **10px font size** - Easy to see but not overwhelming
- **Tooltips** - Hover to see full description
- **Color-coded:**
  - ✏️ Edit = Blue
  - 💾 Export = Green
  - 🗑️ Delete = Red

### **Responsive:**

- **Hover effect** - Slight scale up (1.05x)
- **Smooth transitions** - 0.2s animation
- **Only visible on hover** - Keeps UI clean

---

## Technical Details

### **Backend Endpoints:**

#### **1. Rename Session**
```
POST /sessions/<session_id>/rename
Body: { "title": "New Title" }
Response: { "status": "success", "title": "New Title" }
```

#### **2. Delete Session**
```
DELETE /sessions/<session_id>
Response: { "status": "success" }
```

#### **3. Export Session**
```
GET /sessions/<session_id>/export
Response: { "session_id": "...", "history": [...], "settings": {...} }
```

### **Metadata Storage:**

Custom titles are stored in separate metadata files:
```
chat_history_20250104_143022.json  ← Chat messages
chat_metadata_20250104_143022.json ← Custom title
```

**Metadata file format:**
```json
{
  "title": "Custom Chat Title"
}
```

### **Title Priority:**

1. **Custom title** (from metadata file) - if exists
2. **First user message** (first 50 chars) - if no custom title
3. **"New Chat"** - if no messages yet

---

## Use Cases

### **Use Case 1: Organize Project Chats**

**Before:**
```
How do I implement authentication?
What's the best database for this?
Can you help me with the API?
```

**After editing:**
```
Authentication Implementation
Database Selection Discussion
API Development Help
```

✅ **Much easier to find specific conversations!**

---

### **Use Case 2: Archive Important Discussions**

1. **Have important chat** about system architecture
2. **Edit title** to "System Architecture - Final Design"
3. **Export chat** to save as backup
4. **Keep in sessions** for future reference

✅ **Important decisions are documented and backed up!**

---

### **Use Case 3: Clean Up Old Chats**

1. **Review old chat sessions**
2. **Export important ones** for archival
3. **Delete test chats** and experiments
4. **Keep sessions panel clean**

✅ **Only relevant chats remain!**

---

## Tips & Best Practices

### **✓ DO:**

✅ **Edit titles for important chats** - Makes them easy to find  
✅ **Export before deleting** - Keep backups of valuable conversations  
✅ **Use descriptive titles** - "Q1 2025 Planning" not "Chat about stuff"  
✅ **Delete test chats regularly** - Keep sessions panel organized  
✅ **Export project discussions** - Share with team members  

### **✗ DON'T:**

❌ **Delete without exporting** - You can't recover deleted chats  
❌ **Use very long titles** - Keep them under 50 characters  
❌ **Leave titles as first message** - Edit for better organization  
❌ **Delete current active chat** - Finish conversation first  

---

## Keyboard Shortcuts

### **When Editing Title:**

| Key | Action |
|-----|--------|
| **Enter** | Save new title |
| **Escape** | Cancel editing |

### **General:**

| Action | Shortcut |
|--------|----------|
| Open sessions | Click ☰ menu |
| New chat | Click "New Chat" button |
| Export chat | Click 💾 on session |
| Delete chat | Click 🗑️ on session |

---

## Troubleshooting

### **Problem 1: Buttons Don't Appear**

**Cause:** Not hovering over the session

**Solution:**
1. Move mouse **directly over** the chat session
2. Buttons should appear at the bottom
3. If still not visible, refresh the page

---

### **Problem 2: Can't Save New Title**

**Cause:** Title is empty

**Solution:**
1. Type a **non-empty title**
2. Title must have at least 1 character
3. Click ✓ to save

---

### **Problem 3: Delete Doesn't Work**

**Cause:** Clicked Cancel in confirmation dialog

**Solution:**
1. Click 🗑️ button again
2. Click **OK** in the confirmation dialog
3. Chat will be deleted

---

### **Problem 4: Export Downloads Empty File**

**Cause:** Session has no messages

**Solution:**
1. This is expected for empty chats
2. The file will contain empty history: `"history": []`
3. Send at least one message before exporting

---

## Security & Privacy

### **Data Storage:**

- **Local files only** - All chats stored on your server
- **No cloud sync** - Data stays on your machine
- **JSON format** - Easy to read and backup
- **Metadata separate** - Custom titles in separate files

### **Deletion:**

- **Permanent** - Files are deleted from disk
- **No recovery** - Cannot undo deletion
- **Immediate** - Takes effect right away

### **Export:**

- **Complete data** - Includes all messages and settings
- **Portable format** - Standard JSON
- **No encryption** - Export files are plain text
- **Your responsibility** - Secure exported files appropriately

---

## Summary

### **What You Can Do:**

✅ **Edit chat titles** - Rename any chat session  
✅ **Export chats** - Download as JSON files  
✅ **Delete chats** - Remove unwanted sessions  
✅ **Organize sessions** - Keep panel clean and organized  
✅ **Backup important chats** - Export before deleting  

### **Key Features:**

✅ **Compact buttons** - Small, icon-only design  
✅ **Hover to reveal** - Keeps UI clean  
✅ **Color-coded** - Easy to identify actions  
✅ **Tooltips** - Hover for descriptions  
✅ **Confirmations** - Prevents accidental deletions  
✅ **Keyboard shortcuts** - Enter/Escape in edit mode  

### **Quick Reference:**

| Button | Action | Color |
|--------|--------|-------|
| ✏️ | Edit title | Blue |
| 💾 | Export chat | Green |
| 🗑️ | Delete chat | Red |

---

**Your chat history is now fully manageable with edit, export, and delete features!** 🎉✨
