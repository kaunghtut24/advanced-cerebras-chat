# Quick Toggles Guide

## Overview

The Quick Toggles feature provides convenient, always-visible buttons to enable/disable RAG and Web Search directly in the chat interface, eliminating the need to open settings for every query.

## Features

### 📚 RAG Quick Toggle
- **One-click enable/disable** RAG for your queries
- **Knowledge base selector** right in the chat interface
- **Visual status indicator** (ON/OFF)
- **Auto-enable** when selecting a knowledge base
- **Synced** with settings panel

### 🌐 Web Search Quick Toggle
- **One-click enable/disable** web search
- **Visual status indicator** (ON/OFF)
- **Instant activation** for current and future queries
- **Synced** with settings panel

## User Interface

### Location
The quick toggles appear **above the chat input box** in a clean, horizontal bar with:
- Light gray background
- Rounded pill-shaped buttons
- Clear icons and labels
- Status indicators

### Visual Design

```
┌─────────────────────────────────────────────────────────┐
│  📚 RAG [OFF] [Select KB...▼]  🌐 Web Search [OFF]    │
├─────────────────────────────────────────────────────────┤
│  Type your message here...                        [Send]│
└─────────────────────────────────────────────────────────┘
```

When active:
```
┌─────────────────────────────────────────────────────────┐
│  📚 RAG [ON] [my_docs▼]  🌐 Web Search [ON]           │
├─────────────────────────────────────────────────────────┤
│  Type your message here...                        [Send]│
└─────────────────────────────────────────────────────────┘
```

### Color Coding

**Inactive State:**
- Gray background
- Gray "OFF" badge
- Subtle appearance

**Active State:**
- Light blue background
- Green "ON" badge (bold)
- Highlighted appearance
- Blue border on hover

## How to Use

### Enabling RAG

**Method 1: Select Knowledge Base First**
1. Click the dropdown next to "📚 RAG"
2. Select a knowledge base
3. RAG automatically enables
4. Status shows "ON"

**Method 2: Click Toggle Button**
1. Ensure a knowledge base is selected
2. Click the "📚 RAG" button
3. Status toggles between ON/OFF

### Enabling Web Search

1. Click the "🌐 Web Search" button
2. Status toggles between ON/OFF
3. That's it!

### Using Both Together

1. Enable RAG (select knowledge base)
2. Enable Web Search (click button)
3. Both show "ON" status
4. Your queries will use both sources!

### Quick Workflow Examples

**Research Question:**
1. Click "🌐 Web Search" → ON
2. Ask: "What are the latest AI developments?"
3. Get comprehensive answer with web sources

**Company Knowledge:**
1. Select "company_docs" from RAG dropdown
2. RAG automatically enables
3. Ask: "What is our vacation policy?"
4. Get answer from your documents

**Combined Query:**
1. Select "product_docs" from RAG dropdown
2. Click "🌐 Web Search" → ON
3. Ask: "How does our product compare to competitors?"
4. Get answer using both internal docs and web research

## Features & Benefits

### Always Visible
✅ No need to open settings  
✅ See status at a glance  
✅ Quick enable/disable  
✅ Stays visible while typing  

### Smart Behavior
✅ Auto-enable RAG when KB selected  
✅ Auto-disable RAG when KB deselected  
✅ Syncs with settings panel  
✅ Remembers your preferences  

### Visual Feedback
✅ Clear ON/OFF indicators  
✅ Color-coded status  
✅ Hover effects  
✅ Smooth animations  

### Mobile Friendly
✅ Responsive design  
✅ Touch-friendly buttons  
✅ Adapts to screen size  
✅ Compact on small screens  

## Technical Details

### Synchronization

The quick toggles are **fully synchronized** with the settings panel:

- Changing quick toggle → Updates settings panel
- Changing settings panel → Updates quick toggle
- Both always show the same state

### State Management

**RAG State:**
- `ragEnabled`: Boolean (true/false)
- `currentKnowledgeBase`: String (KB name or null)
- Both must be set for RAG to work

**Web Search State:**
- `webSearchEnabled`: Boolean (true/false)

### Auto-Show/Hide

**RAG Toggle:**
- Shows only if RAG service is available
- Hides if RAG dependencies not installed

**Web Search Toggle:**
- Shows only if web search service is available
- Hides if no API keys configured

## Styling Details

### Button States

**Default (Inactive):**
```css
Background: White
Border: Light gray
Text: Dark gray
Badge: Gray "OFF"
```

**Active:**
```css
Background: Light blue (#e8f4fd)
Border: Blue (#1a73e8)
Text: Blue (#1a73e8)
Badge: Green "ON" (#28a745)
```

**Hover:**
```css
Border: Blue
Shadow: Subtle blue glow
Background: Light gray (if inactive)
```

### Responsive Breakpoints

**Desktop (>768px):**
- Full labels visible
- Larger buttons
- More spacing

**Mobile (≤768px):**
- Compact layout
- Smaller fonts
- Reduced spacing
- Still fully functional

## Keyboard Shortcuts (Future Enhancement)

Potential shortcuts:
- `Ctrl+R`: Toggle RAG
- `Ctrl+W`: Toggle Web Search
- `Ctrl+K`: Open KB selector

## Accessibility

✅ **Tooltips**: Hover for descriptions  
✅ **Clear labels**: Easy to understand  
✅ **Color contrast**: WCAG compliant  
✅ **Keyboard accessible**: Tab navigation  
✅ **Screen reader friendly**: Proper ARIA labels  

## Troubleshooting

### RAG Toggle Not Showing

**Check:**
1. RAG dependencies installed?
2. Qdrant running (if not in-memory)?
3. Check browser console for errors
4. Refresh the page

**Fix:**
```bash
pip install markitdown sentence-transformers qdrant-client
python app.py
```

### Web Search Toggle Not Showing

**Check:**
1. API keys in `.env` file?
2. `exa-py` installed?
3. Check browser console
4. Refresh the page

**Fix:**
```bash
pip install exa-py
# Add API keys to .env
python app.py
```

### Toggle Not Working

**Check:**
1. Knowledge base selected (for RAG)?
2. Status indicator updating?
3. Browser console for errors?

**Fix:**
1. Select a knowledge base first
2. Refresh the page
3. Check server logs

### Dropdown Empty

**Check:**
1. Knowledge bases created?
2. Server running?
3. Network connection?

**Fix:**
1. Create a knowledge base in settings
2. Refresh the page

## Best Practices

### For RAG
1. **Create knowledge bases first** before using quick toggle
2. **Select appropriate KB** for your query topic
3. **Disable when not needed** to save processing time
4. **Check sources** in the response

### For Web Search
1. **Enable for current info** (news, latest developments)
2. **Disable for general chat** to save API costs
3. **Combine with RAG** for comprehensive answers
4. **Verify sources** provided in response

### General
1. **Use visual indicators** to confirm status
2. **Toggle as needed** per query
3. **Experiment** with combinations
4. **Monitor costs** (web search API usage)

## Examples

### Example 1: Quick Research
```
1. Click "🌐 Web Search" → ON
2. Type: "Latest quantum computing breakthroughs"
3. Send
4. Review web sources in response
```

### Example 2: Internal Knowledge
```
1. Select "hr_policies" from dropdown
2. RAG auto-enables → ON
3. Type: "What is the remote work policy?"
4. Send
5. Review knowledge base sources
```

### Example 3: Comprehensive Answer
```
1. Select "product_specs" from dropdown → RAG ON
2. Click "🌐 Web Search" → ON
3. Type: "How does our product compare to market leaders?"
4. Send
5. Get answer using both internal specs and web research
```

### Example 4: Quick Disable
```
1. Both toggles ON
2. Want to ask general question
3. Click both toggles → OFF
4. Type: "Tell me a joke"
5. Send (no RAG or web search used)
```

## UI Components

### HTML Structure
```html
<div class="quick-toggles">
  <div class="toggle-group">
    <button class="quick-toggle-btn">
      <span class="toggle-icon">📚</span>
      <span class="toggle-label">RAG</span>
      <span class="toggle-status">OFF</span>
    </button>
    <select class="quick-kb-select">...</select>
  </div>
  <div class="toggle-group">
    <button class="quick-toggle-btn">
      <span class="toggle-icon">🌐</span>
      <span class="toggle-label">Web Search</span>
      <span class="toggle-status">OFF</span>
    </button>
  </div>
</div>
```

### CSS Classes
- `.quick-toggles`: Container
- `.toggle-group`: Individual toggle group
- `.quick-toggle-btn`: Toggle button
- `.quick-toggle-btn.active`: Active state
- `.toggle-icon`: Emoji icon
- `.toggle-label`: Text label
- `.toggle-status`: ON/OFF badge
- `.quick-kb-select`: KB dropdown

## Future Enhancements

Potential improvements:
- [ ] Keyboard shortcuts
- [ ] Custom toggle colors
- [ ] Toggle presets (save combinations)
- [ ] Quick toggle for other features
- [ ] Drag to reorder toggles
- [ ] Collapse/expand toggle bar
- [ ] Toggle history/favorites

## Summary

The Quick Toggles feature provides:
- ✅ **Convenient access** to RAG and Web Search
- ✅ **Always visible** status indicators
- ✅ **One-click** enable/disable
- ✅ **Smart behavior** with auto-enable
- ✅ **Fully synchronized** with settings
- ✅ **Clean, modern UI** design
- ✅ **Mobile responsive** layout

**Result:** Faster, easier workflow for using RAG and Web Search in your queries!
