# Authentication and Folder Context Reuse

This guide shows how to authenticate with UiPath Cloud, manage folder context, and efficiently reuse authentication and context information across multiple API calls.

## Environment Setup

### Create .env file

Save this as `.env` in your project root:

```bash
# UiPath Cloud credentials
UIPATH_URL=https://cloud.uipath.com/<account>/<tenant>/orchestrator_/
UIPATH_CLIENT_ID=your-client-id-here
UIPATH_CLIENT_SECRET=your-client-secret-here

# Folder context (optional - can be passed in code instead)
UIPATH_FOLDER_KEY=5ebb73c3-b114-43b2-8615-c6a093e0eaab
```

### Getting Your Credentials

1. **Navigate to UiPath Cloud Admin**
   - Go to `https://cloud.uipath.com`
   - Click on **Admin** → **External Applications**

2. **Create External Application**
   - Click **Add Application**
   - Name: "SDK Integration" (or your preferred name)
   - Application Type: **Confidential Application**
   - Grant type: **Client Credentials**
   - Scopes: Select required scopes (OR.Execution, OR.Folders, etc.)

3. **Save Credentials**
   - Copy the **Client ID** → Save to `.env` as `UIPATH_CLIENT_ID`
   - Copy the **Client Secret** → Save to `.env` as `UIPATH_CLIENT_SECRET`
   - Get your Orchestrator URL from browser → Save to `.env` as `UIPATH_URL`

4. **Get Folder Key**
   - Navigate to your folder in Orchestrator
   - Click folder name → **Copy Folder Path**
   - Extract the GUID (last part) → Save to `.env` as `UIPATH_FOLDER_KEY`

## Complete Example: Authentication + Folder Context

```python
import os
from pathlib import Path
from dotenv import load_dotenv
from uipath import UiPath
from uipath_sdk_extensions import ContextGroundingExt, FolderUtils

# === STEP 1: Load environment and authenticate ===
# Load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Initialize SDK - automatically authenticates using env vars
# The SDK reads UIPATH_URL, UIPATH_CLIENT_ID, UIPATH_CLIENT_SECRET
sdk = UiPath()

print("✅ Authenticated with UiPath Cloud")
print(f"   URL: {os.getenv('UIPATH_URL')}")
print(f"   Client ID: {os.getenv('UIPATH_CLIENT_ID')[:8]}...")

# === STEP 2: Get folder context ONCE ===
folder_key = os.getenv("UIPATH_FOLDER_KEY")
folder_utils = FolderUtils(sdk)

# Convert folder_key to folder_id (needed for bucket operations)
# This is cached internally, so subsequent calls are fast
folder_id = folder_utils.get_folder_id_from_key(folder_key)

print(f"\n📁 Folder Context:")
print(f"   Folder Key (GUID): {folder_key}")
print(f"   Folder ID (numeric): {folder_id}")

# === STEP 3: Use SDK endpoint (high-level) ===
# SDK methods use folder_key and handle auth automatically
index_name = "MyIndex"
index = sdk.context_grounding.retrieve(
    name=index_name,
    folder_key=folder_key  # SDK uses folder_key (GUID)
)

print(f"\n🔍 Retrieved index via SDK:")
print(f"   Name: {index.name}")
print(f"   Bucket: {index.data_source.bucketName}")

# === STEP 4: Reuse folder context for direct API call ===
# Direct API calls need folder_id in headers
# sdk.api_client automatically adds authentication headers
bucket_response = sdk.api_client.request(
    "GET",
    "/odata/Buckets",
    headers={"X-UIPATH-OrganizationUnitId": str(folder_id)}  # Reuse folder_id!
)

# Find bucket by name
bucket_id = None
bucket_name = index.data_source.bucketName
for bucket in bucket_response.json()["value"]:
    if bucket["Name"] == bucket_name:
        bucket_id = bucket["Id"]
        break

print(f"\n🪣 Found bucket via direct API:")
print(f"   Bucket Name: {bucket_name}")
print(f"   Bucket ID: {bucket_id}")

# === STEP 5: Reuse both folder_id and bucket_id ===
# Now we have both IDs cached, no more lookups needed!
files_response = sdk.api_client.request(
    "GET",
    f"/orchestrator_/odata/Buckets({bucket_id})/UiPath.Server.Configuration.OData.GetFiles",
    params={"directory": "/", "recursive": "true"},
    headers={"X-UIPATH-OrganizationUnitId": str(folder_id)}  # Reuse again!
)

files = files_response.json()["value"]
print(f"\n📄 Listed files via direct API:")
print(f"   Total files: {len(files)}")
for file in files[:3]:  # Show first 3
    print(f"   - {file['FullPath']}: {file['Size']/1024:.1f} KB")

# === STEP 6: More operations reusing same context ===
# Trigger ingestion using SDK (uses folder_key)
sdk.context_grounding.ingest_data(
    index=index,
    folder_key=folder_key  # Reuse folder_key for SDK
)
print(f"\n🔄 Triggered ingestion (reusing folder_key)")

# Check status using another direct API call (uses folder_id)
status_response = sdk.api_client.request(
    "GET",
    f"/odata/ContextGroundingIndexes?$filter=name eq '{index_name}'",
    headers={"x-uipath-folderkey": folder_key}  # Some APIs use folder_key!
)
print(f"📊 Checked status (reusing folder_key)")
```

## The Easy Way: Let the Library Handle It

```python
from dotenv import load_dotenv
from uipath import UiPath
from uipath_sdk_extensions import ContextGroundingExt

# Load credentials and authenticate
load_dotenv()
sdk = UiPath()

# Create extension - handles all folder context automatically
cg = ContextGroundingExt(sdk)
folder_key = os.getenv("UIPATH_FOLDER_KEY")
index_name = "MyIndex"

# Library internally:
# 1. Converts folder_key → folder_id
# 2. Gets bucket_id from index
# 3. Adds correct headers automatically
# 4. Caches folder_id for reuse
files = cg.list_bucket_files(
    index_name=index_name,
    folder_key=folder_key
)
print(f"📄 Files via library: {len(files)} total")

# Reuse same folder_key - library uses cached folder_id
stats = cg.get_bucket_file_stats(
    index_name=index_name,
    folder_key=folder_key  # No re-lookup! Uses cache
)
print(f"📊 Stats: {stats['total_size_mb']:.1f} MB")

# Get ingestion status
status = cg.get_ingestion_status(
    index_name=index_name,
    folder_key=folder_key  # Still using cache
)
print(f"🔄 Status: {status['last_ingestion_status']}")
```

## How Authentication Works

### OAuth2 Client Credentials Flow

```
1. SDK initialization
   ↓
2. SDK reads UIPATH_CLIENT_ID and UIPATH_CLIENT_SECRET from env
   ↓
3. SDK requests access token from UiPath Cloud
   POST https://cloud.uipath.com/identity_/connect/token
   Body: grant_type=client_credentials&client_id=...&client_secret=...
   ↓
4. UiPath Cloud returns access token (valid ~1 hour)
   ↓
5. SDK stores token and uses for all requests
   ↓
6. SDK automatically refreshes token when expired
```

### What `sdk.api_client` Adds Automatically

Every call to `sdk.api_client.request()` automatically includes:

- ✅ `Authorization: Bearer <access_token>` header
- ✅ Token refresh logic on 401/403 responses
- ✅ Retry logic with exponential backoff
- ✅ Request/response logging (if configured)

**You only need to provide:**
- Folder context headers (`X-UIPATH-OrganizationUnitId` or `x-uipath-folderkey`)
- Request-specific parameters

## Folder Context: Key vs ID

UiPath uses two different folder identifiers:

| Identifier | Type | Format | Used By |
|------------|------|--------|---------|
| Folder Key | GUID | `5ebb73c3-b114-43b2-8615-c6a093e0eaab` | SDK methods, some OData endpoints |
| Folder ID | Integer | `5083200` | Bucket APIs, headers |

### When to Use Which

```python
# SDK methods → Use folder_key (GUID)
index = sdk.context_grounding.retrieve(
    name="MyIndex",
    folder_key="5ebb73c3-..."  # ✅ GUID
)

# Direct bucket API calls → Use folder_id (numeric) in headers
response = sdk.api_client.request(
    "GET",
    "/odata/Buckets",
    headers={"X-UIPATH-OrganizationUnitId": str(folder_id)}  # ✅ Numeric
)

# Some OData endpoints → Use folder_key in headers
response = sdk.api_client.request(
    "GET",
    "/odata/Folders",
    headers={"x-uipath-folderkey": folder_key}  # ✅ GUID
)
```

### Converting Between Them

**Manual approach:**
```python
from uipath_sdk_extensions import FolderUtils

folder_utils = FolderUtils(sdk)

# GUID → Numeric
folder_id = folder_utils.get_folder_id_from_key("5ebb73c3-...")

# Numeric → GUID
folder_key = folder_utils.get_folder_key_from_id(5083200)
```

**Automatic with library:**
```python
# Library handles conversion internally
cg = ContextGroundingExt(sdk)
files = cg.list_bucket_files(
    index_name="MyIndex",
    folder_key="5ebb73c3-..."  # Library converts to folder_id as needed
)
```

## Benefits of Context Reuse

### Without Context Reuse (Inefficient)

```python
# Every operation does expensive lookups
def list_files():
    folder_id = lookup_folder_id(folder_key)  # API call #1
    bucket_id = lookup_bucket_id(folder_id)   # API call #2
    return get_files(bucket_id, folder_id)    # API call #3

def get_stats():
    folder_id = lookup_folder_id(folder_key)  # API call #4 (duplicate!)
    bucket_id = lookup_bucket_id(folder_id)   # API call #5 (duplicate!)
    return get_stats(bucket_id, folder_id)    # API call #6

# Total: 6 API calls for 2 operations
```

### With Context Reuse (Efficient)

```python
# Lookup once, reuse everywhere
folder_id = lookup_folder_id(folder_key)    # API call #1
bucket_id = lookup_bucket_id(folder_id)     # API call #2

def list_files():
    return get_files(bucket_id, folder_id)  # API call #3 (reuses context)

def get_stats():
    return get_stats(bucket_id, folder_id)  # API call #4 (reuses context)

# Total: 4 API calls for 2 operations (33% fewer calls)
```

### With Library Caching (Most Efficient)

```python
# Library caches folder_id internally
cg = ContextGroundingExt(sdk)

files = cg.list_bucket_files(index, folder_key)  # Lookup + cache
stats = cg.get_bucket_file_stats(index, folder_key)  # Uses cache!
status = cg.get_ingestion_status(index, folder_key)  # Uses cache!

# FolderUtils also has caching
folder_utils = FolderUtils(sdk)
folder_id = folder_utils.get_folder_id_from_key(folder_key)  # Lookup + cache
folder_id_again = folder_utils.get_folder_id_from_key(folder_key)  # Cache hit!
```

## Troubleshooting

### "401 Unauthorized" Error

**Problem:** Invalid or expired credentials

**Solutions:**
1. Verify `.env` file has correct credentials
2. Check external application is active in UiPath Cloud
3. Verify scopes include required permissions
4. Try regenerating client secret

```python
# Debug: Check what SDK is using
import os
print(f"URL: {os.getenv('UIPATH_URL')}")
print(f"Client ID: {os.getenv('UIPATH_CLIENT_ID')}")
print(f"Client Secret present: {bool(os.getenv('UIPATH_CLIENT_SECRET'))}")
```

### "Folder not found" Error

**Problem:** Invalid folder_key or insufficient permissions

**Solutions:**
1. Verify folder_key GUID is correct
2. Check external application has access to the folder
3. Confirm folder exists and you have permissions

```python
# Debug: List all accessible folders
from uipath_sdk_extensions import FolderUtils

folder_utils = FolderUtils(sdk)
folders = folder_utils.list_all_folders()

for folder in folders:
    print(f"{folder['DisplayName']}: {folder['Key']}")
```

### "Bucket not found" Error

**Problem:** Index doesn't have a storage bucket or wrong index name

**Solutions:**
1. Verify index name is correct
2. Check index has a data source configured
3. Confirm bucket name matches

```python
# Debug: Check index configuration
index = sdk.context_grounding.retrieve(
    name="MyIndex",
    folder_key=folder_key
)

print(f"Index: {index.name}")
print(f"Bucket: {index.data_source.bucketName}")
print(f"Directory: {index.data_source.directoryPath}")
print(f"Glob: {index.data_source.fileNameGlob}")
```

## Security Best Practices

### ✅ Do's

- **Use `.env` files** for credentials (never hardcode)
- **Add `.env` to `.gitignore`** (never commit secrets)
- **Use separate credentials** for dev/test/prod
- **Rotate client secrets** regularly
- **Grant minimum required scopes** only
- **Use environment variables** in CI/CD

### ❌ Don'ts

- **Never commit credentials** to version control
- **Never share client secrets** in plain text
- **Never log credentials** (even for debugging)
- **Never use production credentials** in development
- **Never hardcode folder keys** (use environment variables)

### Example .gitignore

```
# Environment files with credentials
.env
.env.*
!.env.example
```

### Example .env.example

```bash
# Copy this to .env and fill in your values
UIPATH_URL=https://cloud.uipath.com/<account>/<tenant>/orchestrator_/
UIPATH_CLIENT_ID=your-client-id
UIPATH_CLIENT_SECRET=your-client-secret
UIPATH_FOLDER_KEY=your-folder-guid
```

## Next Steps

- **Read the [API Reference](../README.md#api-reference)** for complete method documentation
- **See [Examples](./examples/)** for more use cases
- **Check [Troubleshooting](./troubleshooting.md)** for common issues
