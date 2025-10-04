# Settings Panel Improvements

## Overview

The settings panel has been significantly improved with better layout, scrolling, and a new customizable system prompt feature optimized for RAG and Web Search integration.

## What's New

### 1. **Improved Settings Panel Layout**

#### Fixed Scrolling Issue
- **Problem**: Settings panel was too long, buttons at bottom were not visible
- **Solution**: Implemented a three-section layout with scrollable body

#### New Structure
```
┌─────────────────────────────────┐
│  Settings                       │  ← Fixed Header
├─────────────────────────────────┤
│  Model: [dropdown]              │
│  System Prompt: [textarea]      │  ← Scrollable Body
│  Temperature: [slider]          │
│  Max Tokens: [input]            │
│  RAG Settings...                │
│  Web Search Settings...         │
│  ↕ (scrollable)                 │
├─────────────────────────────────┤
│  [Reset All]  [Save Settings]   │  ← Fixed Footer
└─────────────────────────────────┘
```

#### Benefits
✅ Header stays visible  
✅ Footer buttons always accessible  
✅ Body scrolls independently  
✅ Better use of screen space  
✅ Works on all screen sizes  

### 2. **Default System Prompt**

#### Optimized for RAG and Web Search
A comprehensive default system prompt that:
- Guides the AI on how to respond
- Provides instructions for RAG usage
- Provides instructions for Web Search usage
- Handles combined RAG + Web Search scenarios
- Maintains professional tone

#### Default Prompt Content
```
You are a helpful, knowledgeable AI assistant powered by Cerebras.

When responding:
- Be clear, concise, and informative
- Use proper formatting (markdown, lists, code blocks)
- Acknowledge uncertainty honestly
- Provide step-by-step explanations

When RAG is enabled:
- Prioritize knowledge base context
- Cite specific sources
- Acknowledge when KB lacks info
- Combine general + specific knowledge

When Web Search is enabled:
- Incorporate up-to-date web information
- Cite sources with URLs
- Prioritize recent, authoritative sources
- Cross-reference multiple sources

When both are enabled:
- Synthesize internal + external sources
- Distinguish between internal docs and web info
- Provide comprehensive answers
- Cite all sources appropriately
```

### 3. **Customizable System Prompt**

#### Features
- **Editable**: Customize to your needs
- **Reset Button**: Restore default anytime
- **Larger Textarea**: 150px minimum height
- **Monospace Font**: Better readability
- **Help Text**: Guidance on usage
- **Auto-Upgrade**: Old prompts automatically upgraded

#### Usage
1. Open Settings
2. Edit "System Prompt" field
3. Click "Reset to Default" to restore
4. Click "Save Settings" to apply

### 4. **Better Button Layout**

#### Primary/Secondary Buttons
- **Primary Button**: "Save Settings" (blue, prominent)
- **Secondary Buttons**: "Reset All", "Reset to Default" (gray, subtle)

#### Footer Buttons
- Always visible at bottom
- Right-aligned for easy access
- Clear visual hierarchy

## Technical Implementation

### CSS Changes

#### Settings Container
```css
.settings-container {
    max-height: 85vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}
```

#### Three-Section Layout
```css
.settings-header {
    padding: 20px;
    border-bottom: 1px solid #ddd;
    flex-shrink: 0;
}

.settings-body {
    padding: 20px;
    overflow-y: auto;
    flex: 1;
}

.settings-footer {
    padding: 15px 20px;
    border-top: 1px solid #ddd;
    flex-shrink: 0;
}
```

#### Button Styles
```css
.primary-button {
    background-color: #1a73e8;
    color: white;
}

.secondary-button {
    background-color: #f0f0f0;
    color: #333;
}
```

### JavaScript Changes

#### Default System Prompt Constant
```javascript
const DEFAULT_SYSTEM_PROMPT = `You are a helpful...`;
```

#### Reset System Prompt Function
```javascript
function resetSystemPromptToDefault() {
    systemPromptInput.value = DEFAULT_SYSTEM_PROMPT;
    alert('System prompt reset to default');
}
```

#### Auto-Upgrade Old Prompts
```javascript
if (!systemPrompt || systemPrompt === 'You are a helpful assistant.') {
    document.getElementById('system-prompt').value = DEFAULT_SYSTEM_PROMPT;
}
```

### HTML Changes

#### Structured Layout
```html
<div class="settings-container">
    <div class="settings-header">
        <h2>Settings</h2>
    </div>
    <div class="settings-body">
        <!-- Form fields here -->
    </div>
    <div class="settings-footer">
        <button class="secondary-button">Reset All</button>
        <button class="primary-button">Save Settings</button>
    </div>
</div>
```

## User Guide

### Opening Settings
1. Click "⚙️ Settings" button in header
2. Settings panel opens as modal

### Editing System Prompt
1. Scroll to "System Prompt" field
2. Edit the text as needed
3. Use placeholders: `{context}` for RAG, `{web_results}` for web search
4. Click "Save Settings"

### Resetting System Prompt
1. Click "Reset to Default" button below system prompt
2. Prompt is restored to default
3. Click "Save Settings" to apply

### Resetting All Settings
1. Click "Reset All" button in footer
2. Confirm the action
3. All settings restored to defaults
4. System prompt also reset

### Scrolling in Settings
- Use mouse wheel or trackpad
- Drag scrollbar on right side
- Header and footer stay fixed
- Only middle section scrolls

## Responsive Design

### Desktop (>768px)
- Max width: 600px
- Max height: 85vh
- Comfortable padding
- Large buttons

### Mobile (≤768px)
- Max width: 95%
- Max height: 90vh
- Compact padding
- Smaller fonts
- Still fully functional

## System Prompt Customization

### Variables You Can Use
- `{context}` - Replaced with RAG context
- `{web_results}` - Replaced with web search results
- `{query}` - User's query
- `{kb_name}` - Knowledge base name

### Example Custom Prompts

#### Technical Documentation Assistant
```
You are a technical documentation expert. When RAG is enabled, 
prioritize code examples and API references from the knowledge base. 
Format responses with clear code blocks and step-by-step instructions.
```

#### Customer Support Agent
```
You are a friendly customer support agent. When RAG is enabled, 
use the knowledge base to provide accurate product information. 
When Web Search is enabled, find the latest product updates and news.
Always be empathetic and solution-focused.
```

#### Research Assistant
```
You are an academic research assistant. When RAG is enabled, 
cite sources from the knowledge base with proper attribution. 
When Web Search is enabled, prioritize peer-reviewed sources and 
recent publications. Provide comprehensive literature reviews.
```

## Best Practices

### System Prompt Design
1. **Be Specific**: Clear instructions yield better results
2. **Use Sections**: Separate instructions for different scenarios
3. **Include Examples**: Show desired output format
4. **Set Tone**: Define personality and style
5. **Handle Edge Cases**: What to do when no context available

### Settings Management
1. **Save Often**: Don't lose your customizations
2. **Test Changes**: Try different prompts to find what works
3. **Keep Backups**: Copy your custom prompt before resetting
4. **Use Defaults**: Start with default and modify incrementally

### RAG + Web Search Integration
1. **Prioritize Sources**: Decide which takes precedence
2. **Cite Everything**: Always attribute information
3. **Combine Wisely**: Use both when comprehensive answer needed
4. **Distinguish Sources**: Make clear what's internal vs external

## Troubleshooting

### Settings Panel Too Small
- **Issue**: Can't see all settings
- **Fix**: Panel now scrolls automatically

### Buttons Not Visible
- **Issue**: Save button off-screen
- **Fix**: Footer now fixed at bottom

### System Prompt Not Saving
- **Issue**: Changes not persisted
- **Fix**: Click "Save Settings" after editing

### Reset Not Working
- **Issue**: Reset button doesn't restore default
- **Fix**: Refresh page and try again

### Scroll Not Working
- **Issue**: Can't scroll in settings
- **Fix**: Click inside settings body area first

## Advanced Features

### Conditional Instructions
```
When RAG is enabled AND Web Search is enabled:
- Compare internal docs with external sources
- Highlight discrepancies
- Provide balanced perspective

When only RAG is enabled:
- Focus on internal knowledge
- Suggest when external info might help

When only Web Search is enabled:
- Provide current, external information
- Note when internal docs might be relevant
```

### Output Formatting
```
Format all responses as:
1. Summary (2-3 sentences)
2. Detailed explanation
3. Sources cited
4. Related topics (if applicable)

Use markdown for:
- **Bold** for key terms
- `code` for technical terms
- > quotes for citations
```

### Tone and Style
```
Tone: Professional yet friendly
Style: Concise but comprehensive
Audience: Technical users with varying expertise
Language: Clear, jargon-free when possible
```

## Summary

The improved settings panel provides:

✅ **Better Layout**: Fixed header/footer, scrollable body  
✅ **Always Accessible**: Buttons always visible  
✅ **Customizable Prompt**: Tailor AI behavior to your needs  
✅ **Easy Reset**: Restore defaults anytime  
✅ **Optimized for RAG/Web**: Default prompt handles all scenarios  
✅ **Responsive Design**: Works on all devices  
✅ **Professional UI**: Clean, modern appearance  

**Result**: A more usable, flexible, and powerful settings experience!
