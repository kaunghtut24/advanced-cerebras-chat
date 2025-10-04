# Persistent Storage Fix for Knowledge Bases

## Problem Identified

**Issue:** Knowledge bases disappear when the application restarts

**Root Cause:** Qdrant was configured to use in-memory storage (`QDRANT_IN_MEMORY=true`), which means:
- All data stored in RAM only
- Data lost when application stops
- Knowledge bases not persisted
- Uploaded documents disappear

## Solution Implemented

Changed Qdrant from **in-memory mode** to **persistent file storage** mode.

### What Changed

#### **Before:**
```env
QDRANT_IN_MEMORY=true
```
- Data stored in RAM
- Lost on restart
- Fast but temporary

#### **After:**
```env
QDRANT_IN_MEMORY=false
QDRANT_PATH=./qdrant_storage
```
- Data stored on disk
- Persists across restarts
- Permanent storage

---

## Files Modified

### 1. `.env`
```env
# Changed from:
QDRANT_IN_MEMORY=true

# To:
QDRANT_IN_MEMORY=false
QDRANT_PATH=./qdrant_storage
```

### 2. `.env.example`
```env
# Added documentation and new variable:
QDRANT_IN_MEMORY=false
QDRANT_PATH=./qdrant_storage
```

### 3. `rag_service.py`
- Added support for `QDRANT_PATH` environment variable
- Automatically creates storage directory
- Uses file-based persistent storage
- Falls back to remote server if path not set

### 4. `.gitignore`
```
# Added to prevent committing data:
qdrant_storage/
uploads/
```

---

## How It Works Now

### Storage Modes

Qdrant now supports **3 storage modes**:

#### **Mode 1: Persistent File Storage (Default - Recommended)**
```env
QDRANT_IN_MEMORY=false
QDRANT_PATH=./qdrant_storage
```
✅ **Data persists across restarts**  
✅ **No external server needed**  
✅ **Easy setup**  
✅ **Good for development and production**  

#### **Mode 2: Remote Qdrant Server**
```env
QDRANT_IN_MEMORY=false
QDRANT_PATH=localhost  # or leave empty
QDRANT_HOST=localhost
QDRANT_PORT=6333
```
✅ **Scalable for production**  
✅ **Can run in Docker**  
✅ **Shared across multiple apps**  
⚠️ **Requires running Qdrant server**  

#### **Mode 3: In-Memory (Not Recommended)**
```env
QDRANT_IN_MEMORY=true
```
✅ **Fast**  
✅ **No setup needed**  
❌ **Data lost on restart**  
❌ **Only for testing**  

---

## What Happens Now

### On First Start
1. Application creates `./qdrant_storage/` directory
2. Qdrant initializes persistent storage
3. Empty database ready for knowledge bases

### Creating Knowledge Bases
1. Create knowledge base via UI
2. Upload documents
3. Data stored in `./qdrant_storage/`
4. **Persists across restarts**

### On Restart
1. Application connects to existing storage
2. Loads all knowledge bases
3. All documents still available
4. **No data loss!**

---

## Directory Structure

```
cerebras/
├── app.py
├── rag_service.py
├── .env
├── qdrant_storage/          ← New persistent storage directory
│   ├── collection/
│   ├── meta.json
│   └── ... (Qdrant data files)
├── uploads/                 ← Uploaded files
│   ├── knowledge_base_1/
│   └── knowledge_base_2/
└── ...
```

---

## Testing the Fix

### Step 1: Stop the Server
```bash
# Press Ctrl+C in terminal
```

### Step 2: Verify Configuration
Check `.env` file:
```env
QDRANT_IN_MEMORY=false
QDRANT_PATH=./qdrant_storage
```

### Step 3: Restart the Server
```bash
python app.py
```

**Look for this message:**
```
INFO:root:Initializing Qdrant with persistent storage at: ./qdrant_storage
INFO:root:Qdrant client initialized with persistent file storage
```

### Step 4: Create a Test Knowledge Base
1. Open http://localhost:5000
2. Click **⚙️ Settings** → **Manage Knowledge Bases**
3. Create a new knowledge base (e.g., "test_kb")
4. Upload a document

### Step 5: Restart and Verify
```bash
# Stop server (Ctrl+C)
python app.py
```

1. Open http://localhost:5000
2. Click **⚙️ Settings** → **Manage Knowledge Bases**
3. **Your knowledge base should still be there!** ✅

---

## Troubleshooting

### Knowledge Bases Still Disappearing

**Check 1: Verify .env setting**
```bash
# Open .env and confirm:
QDRANT_IN_MEMORY=false
QDRANT_PATH=./qdrant_storage
```

**Check 2: Check startup logs**
```bash
python app.py
# Look for:
# "Initializing Qdrant with persistent storage at: ./qdrant_storage"
```

**Check 3: Verify directory exists**
```bash
# After creating a KB, check:
ls -la qdrant_storage/
# Should see files
```

### Permission Errors

**Issue:** Can't create `qdrant_storage/` directory

**Fix:**
```bash
# Manually create with proper permissions
mkdir qdrant_storage
chmod 755 qdrant_storage
```

### Storage Directory Not Created

**Issue:** `qdrant_storage/` doesn't exist

**Fix:**
```bash
# Create manually
mkdir qdrant_storage
# Restart server
python app.py
```

### Old In-Memory Data

**Issue:** Had data in memory mode, now it's gone

**Explanation:** In-memory data cannot be recovered. You need to:
1. Re-create knowledge bases
2. Re-upload documents
3. They will now persist!

---

## Migration Guide

### If You Had In-Memory Data

Unfortunately, in-memory data **cannot be recovered**. You need to:

1. **Stop the server**
2. **Update `.env`** (already done)
3. **Restart the server**
4. **Re-create knowledge bases**
5. **Re-upload documents**
6. **Data will now persist!**

### If You Want to Keep In-Memory Mode

If you prefer in-memory mode (for testing):

```env
# In .env:
QDRANT_IN_MEMORY=true
# Remove or comment out:
# QDRANT_PATH=./qdrant_storage
```

**Note:** You'll lose data on every restart.

---

## Storage Size Considerations

### Disk Space Usage

- **Embeddings**: ~1.5 KB per chunk (384 dimensions × 4 bytes)
- **Metadata**: ~500 bytes per chunk
- **Example**: 100 documents × 10 chunks = ~200 MB

### Monitoring Storage

```bash
# Check storage size
du -sh qdrant_storage/

# Check number of files
find qdrant_storage/ -type f | wc -l
```

### Cleaning Up

To remove all knowledge bases:
```bash
# Stop server first!
rm -rf qdrant_storage/
rm -rf uploads/
# Restart server - fresh start
```

---

## Production Recommendations

### For Development
✅ **Use persistent file storage** (current setup)
```env
QDRANT_IN_MEMORY=false
QDRANT_PATH=./qdrant_storage
```

### For Production (Small Scale)
✅ **Use persistent file storage**
```env
QDRANT_IN_MEMORY=false
QDRANT_PATH=/var/lib/cerebras/qdrant_storage
```

### For Production (Large Scale)
✅ **Use dedicated Qdrant server**
```bash
# Run Qdrant in Docker
docker run -d -p 6333:6333 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

```env
# In .env:
QDRANT_IN_MEMORY=false
QDRANT_PATH=localhost
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

---

## Backup and Recovery

### Backing Up Knowledge Bases

```bash
# Stop server
# Copy storage directory
cp -r qdrant_storage/ qdrant_storage_backup/
cp -r uploads/ uploads_backup/
```

### Restoring from Backup

```bash
# Stop server
# Restore directories
cp -r qdrant_storage_backup/ qdrant_storage/
cp -r uploads_backup/ uploads/
# Restart server
```

### Automated Backup Script

```bash
#!/bin/bash
# backup_kb.sh
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf kb_backup_$DATE.tar.gz qdrant_storage/ uploads/
echo "Backup created: kb_backup_$DATE.tar.gz"
```

---

## Summary

### What Was Fixed
✅ Changed from in-memory to persistent storage  
✅ Knowledge bases now survive restarts  
✅ Uploaded documents persist  
✅ No data loss on application restart  

### What You Need to Do
1. ✅ Configuration already updated (`.env`)
2. ✅ Code already updated (`rag_service.py`)
3. ⚠️ **Restart the server** to apply changes
4. ⚠️ **Re-create knowledge bases** (old in-memory data is lost)
5. ⚠️ **Re-upload documents**
6. ✅ **Enjoy persistent storage!**

### Benefits
✅ **Permanent storage** - Data persists across restarts  
✅ **No external dependencies** - No Docker/server needed  
✅ **Easy setup** - Works out of the box  
✅ **Production ready** - Suitable for real use  
✅ **Backup friendly** - Easy to backup/restore  

---

**Your knowledge bases will now persist across application restarts!** 🎉
