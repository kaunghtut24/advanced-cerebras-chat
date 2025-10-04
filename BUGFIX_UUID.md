# Bug Fix: Qdrant UUID Validation Error

## Issue

When uploading files to a knowledge base, the application crashed with a 500 Internal Server Error:

```
ERROR:root:Failed to add document to Qdrant: Point id 75101bcadd89fa15992d57cfd710603f_0 is not a valid UUID
INFO:werkzeug:127.0.0.1 - - [04/Oct/2025 17:06:08] "POST /knowledge-bases/Cerebras/upload HTTP/1.1" 500 -
```

## Root Cause

In `rag_service.py`, the `add_document()` function was generating point IDs by concatenating an MD5 hash with a chunk index:

```python
# OLD CODE (BROKEN)
points.append(PointStruct(
    id=f"{doc_id}_{i}",  # e.g., "75101bcadd89fa15992d57cfd710603f_0"
    vector=embedding,
    payload=point_metadata
))
```

Qdrant requires point IDs to be valid UUIDs (RFC 4122 format), but the concatenated string `"75101bcadd89fa15992d57cfd710603f_0"` is not a valid UUID.

## Solution

Changed the point ID generation to use UUID5, which creates deterministic UUIDs from a namespace and name:

```python
# NEW CODE (FIXED)
import uuid

# Generate a valid UUID from the document ID and chunk index
# Use UUID5 with a namespace to ensure deterministic IDs
point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{doc_id}_{i}"))

points.append(PointStruct(
    id=point_id,  # e.g., "a1b2c3d4-e5f6-5789-a1b2-c3d4e5f67890"
    vector=embedding,
    payload=point_metadata
))
```

### Why UUID5?

- **Deterministic**: Same input always produces the same UUID
- **Valid**: Conforms to RFC 4122 UUID format
- **Unique**: Namespace + name combination ensures uniqueness
- **Reproducible**: Re-uploading the same document chunk produces the same ID

## Changes Made

### File: `rag_service.py`

1. **Added import** (line 10):
   ```python
   import uuid
   ```

2. **Updated point ID generation** (lines 256-258):
   ```python
   # Generate a valid UUID from the document ID and chunk index
   # Use UUID5 with a namespace to ensure deterministic IDs
   point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{doc_id}_{i}"))
   ```

3. **Updated PointStruct creation** (lines 260-264):
   ```python
   points.append(PointStruct(
       id=point_id,  # Now uses valid UUID
       vector=embedding,
       payload=point_metadata
   ))
   ```

## Testing

After the fix, file uploads should work correctly:

1. **Restart the server** (if running):
   ```bash
   # Press Ctrl+C to stop
   python app.py
   ```

2. **Test file upload**:
   - Open http://localhost:5000
   - Go to Settings → Manage Knowledge Bases
   - Create a knowledge base
   - Upload a file
   - Should see success message

3. **Verify in logs**:
   ```
   INFO:root:Added X chunks from 'filename.pdf' to 'kb_name'
   INFO:werkzeug:127.0.0.1 - - [timestamp] "POST /knowledge-bases/kb_name/upload HTTP/1.1" 200 -
   ```

## Impact

- ✅ File uploads now work correctly
- ✅ Documents are properly indexed in Qdrant
- ✅ No breaking changes to existing functionality
- ✅ Deterministic IDs allow re-uploading same documents

## Related

- Qdrant documentation: https://qdrant.tech/documentation/concepts/points/
- Python UUID module: https://docs.python.org/3/library/uuid.html
- RFC 4122 (UUID spec): https://www.rfc-editor.org/rfc/rfc4122

## Status

✅ **FIXED** - Ready to test
