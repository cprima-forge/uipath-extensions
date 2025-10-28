# RFC: Extension Package Pattern for UiPath Python SDK

**Status:** Proposed – Phase 2 Complete (11 Extensions)
**Author:** Christian Prior-Mamulyan
**Date:** 2025-10-26
**Package:** [uipath-sdk-extensions v0.0.2 on MyGet](https://www.myget.org/feed/cprima-forge/package/pythonwhl/uipath-sdk-extensions)

## Installation

```bash
uv pip install uipath-sdk-extensions \
  --extra-index-url https://www.myget.org/F/cprima-forge/python/ \
  --index-strategy unsafe-best-match
```

---

## The Developer Problem

You're building Context Grounding workflows. The official SDK lets you create indexes and trigger ingestion, but then you hit a wall:

**"Which files are actually in the storage bucket?"** - No SDK method exists.

**"Did my file get indexed or skipped?"** - You can't tell.

**"What's the bucket configuration?"** - Manual API spelunking required.

You end up writing 150+ lines of undocumented OData calls, juggling two different folder identifiers (GUID vs numeric), manually managing headers, and copy-pasting folder lookup logic across every script.

**This is a solved problem in every other SDK ecosystem.** Extension packages exist to fill gaps without waiting for official updates.

---

## Why Extension Packages Matter

### The Dilemma

Official SDKs move slowly by design—stability, backwards compatibility, governance. But developers need solutions **today** for:

- Missing CRUD operations on known endpoints
- Utility functions for common patterns (ID conversions, bulk operations)
- Workflow helpers that compose multiple SDK calls
- Debug/inspection tools for troubleshooting production issues

### The Extension Package Strategy

**Composition over forking:** Wrap the SDK, don't replace it. Leverage `sdk.api_client` for authentication, retry logic, and token management. Add only what's missing.

**Benefits:**
- **Ship in hours, not months** - No dependency on SDK release cycles
- **Zero breaking changes** - Extension sits alongside SDK, doesn't override it
- **Community-driven** - Developers solve their own pain points
- **Upgrade-safe** - When SDK adds native support, migrate incrementally

---

## Environment Setup

Standard `.env` file configuration:

### Example `.env`

```bash
# UiPath Cloud credentials
UIPATH_URL=https://cloud.uipath.com/<account>/<tenant>/orchestrator_/
UIPATH_CLIENT_ID=your-client-id-here
UIPATH_CLIENT_SECRET=your-client-secret-here

# Folder context (optional - can be passed in code instead)
UIPATH_FOLDER_KEY=5ebb73c3-b114-43b2-8615-c6a093e0eaab
```

### Retrieving Credentials

1. **Navigate to UiPath Cloud Admin**

   * Go to `https://cloud.uipath.com`
   * Click **Admin → External Applications**

2. **Create External Application**

   * Name: “SDK Integration” (or preferred name)
   * Type: **Confidential Application**
   * Grant type: **Client Credentials**
   * Select scopes such as `OR.Execution`, `OR.Folders`, etc.

3. **Save Credentials**

   * Copy **Client ID** → `.env` → `UIPATH_CLIENT_ID`
   * Copy **Client Secret** → `.env` → `UIPATH_CLIENT_SECRET`
   * Copy your Orchestrator URL → `.env` → `UIPATH_URL`

4. **Get Folder Key**

   * In Orchestrator, open folder → **Copy Folder Path**
   * Extract final GUID → `.env` → `UIPATH_FOLDER_KEY`

---

## The Solution: What This Extension Provides

### Phase 1 Extensions (v0.0.1) - Core Infrastructure

**ContextGroundingExt** - Storage visibility and verification
- `list_bucket_files()` - List all files in storage with directory support
- `verify_file_indexed()` - Check if specific file exists in bucket
- `get_bucket_file_stats()` - Get file counts, sizes, directory breakdown
- `get_ingestion_status()` - Enhanced status with detailed metrics

**FolderUtils** - ID conversion and folder navigation
- `get_folder_id_from_key()` - GUID → numeric ID (cached)
- `get_folder_key_from_id()` - Numeric ID → GUID
- `list_all_folders()` - Get accessible folders for debugging

**BucketExtensions** - Direct storage operations
- `list_files()` - Filter files by pattern and directory
- `get_bucket_info()` - Bucket metadata and configuration
- `organize_files_by_directory()` - Group files for analysis

### Phase 2 Extensions (v0.0.2) - Operations & Management

**AssetsExt** - Asset CRUD and sharing
- `list_assets()`, `create_asset()`, `delete_asset()`
- `get_assets_across_folders()` - Multi-folder queries
- `share_asset_to_folders()` - Cross-folder sharing

**JobsExt** - Job operations and analytics
- `list_jobs()`, `stop_job()`, `restart_job()`
- `bulk_stop_jobs()` - Mass cancellation
- `get_job_statistics()` - Success/failure metrics

**QueuesExt** - Queue definition management
- `create_queue_definition()`, `update_queue_definition()`
- `set_retention_policy()` - Data retention
- `get_queue_statistics()` - Processing metrics

**ProcessesExt** - Release and version management
- `list_releases()`, `list_process_versions()`
- `get_release_by_process_name()` - Version lookup
- `set_retention_policy()` - Release retention

**SchedulesExt** - Time-based triggers
- `create_schedule()` - Cron-like process triggers
- `enable_schedule()`, `disable_schedule()`
- `get_schedules_for_release()`

**LibrariesExt** - Package management
- `list_libraries()`, `list_library_versions()`
- `get_library_usage()` - Usage statistics
- `delete_library_version()`

**TasksExt** - Human-in-the-loop workflows
- `create_task()`, `complete_task()`
- `bulk_complete_tasks()` - Batch processing
- `list_pending_tasks_for_user()`

**FolderManagementExt** - Full folder CRUD
- `create_folder()`, `delete_folder()`, `update_folder()`
- `get_folder_hierarchy()` - Tree navigation
- `search_folders()`, `move_folder()`

---

## Real-World Impact: Before vs After

### Without Extension (Manual Approach - 150+ LOC)

```python
# 1. Manually lookup folder_id from folder_key
folder_response = sdk.api_client.request("GET", "/odata/Folders")
folder_id = None
for folder in folder_response.json()["value"]:
    if folder["Key"] == folder_key:
        folder_id = folder["Id"]
        break

# 2. Get index and bucket name
index = sdk.context_grounding.retrieve(name=index_name, folder_key=folder_key)
bucket_name = index.data_source.bucketName

# 3. Find bucket_id from bucket name (requires folder_id in headers!)
bucket_response = sdk.api_client.request(
    "GET",
    "/odata/Buckets",
    headers={"X-UIPATH-OrganizationUnitId": str(folder_id)}  # Numeric ID!
)
bucket_id = None
for bucket in bucket_response.json()["value"]:
    if bucket["Name"] == bucket_name:
        bucket_id = bucket["Id"]
        break

# 4. FINALLY list files (need BOTH bucket_id AND folder_id)
files_response = sdk.api_client.request(
    "GET",
    f"/orchestrator_/odata/Buckets({bucket_id})/UiPath.Server.Configuration.OData.GetFiles",
    params={"directory": "/", "recursive": "true"},
    headers={"X-UIPATH-OrganizationUnitId": str(folder_id)}
)
files = files_response.json()["value"]

# + Error handling, pagination, retry logic, header juggling...
```

**Problems:**
- Hardcoded OData endpoints (breaks on URL changes)
- Manual header management (which header for which API?)
- Repeated lookups (folder_id lookup in every script)
- No caching (API calls repeat across operations)
- Brittle error handling (SDK errors vs HTTP errors)

### With Extension (15 LOC)

```python
from uipath_sdk_extensions import ContextGroundingExt

cg = ContextGroundingExt(sdk)

# One call, all complexity handled
files = cg.list_bucket_files(
    index_name="MyIndex",
    folder_key=folder_key,
    recursive=True
)

# Folder context cached automatically
stats = cg.get_bucket_file_stats(index_name="MyIndex", folder_key=folder_key)
status = cg.get_ingestion_status(index_name="MyIndex", folder_key=folder_key)
```

**Benefits:**
- Automatic folder_id caching (33% fewer API calls)
- Correct headers selected per endpoint
- SDK-level retry and auth token handling inherited
- Readable, self-documenting code

---

## Implementation Details

### How Authentication Works

The extension leverages the SDK's existing OAuth2 client credentials flow:

```
1. SDK reads UIPATH_CLIENT_ID / SECRET / URL from environment
2. Requests token: POST /identity_/connect/token
3. Stores access token (~1 hour validity)
4. Auto-refreshes on expiry or 401/403
5. Injects Bearer token on all requests via sdk.api_client
```

**Developer benefit:** Extension inherits authentication automatically. No duplicate token management.

### Folder Context: The Two-ID Problem

UiPath uses two different folder identifiers across APIs:

| Identifier   | Type    | Format                                 | Used By          |
| ------------ | ------- | -------------------------------------- | ---------------- |
| `folder_key` | GUID    | `5ebb73c3-b114-43b2-8615-c6a093e0eaab` | SDK + some OData |
| `folder_id`  | Integer | `5083200`                              | Bucket + raw API |

**The manual pain:** Every script needs conversion logic. Every direct API call needs to figure out which ID to use in which header.

**Extension solution:** `FolderUtils` handles conversion and caches results.

```python
from uipath_sdk_extensions import FolderUtils

folder_utils = FolderUtils(sdk)

# Convert once, cache internally
folder_id = folder_utils.get_folder_id_from_key(folder_key)

# Subsequent calls return cached value (no API hit)
folder_id_again = folder_utils.get_folder_id_from_key(folder_key)
```

---

## Developer Benefits in Practice

### 1. Faster Development Velocity

| Task                         | Manual Approach    | With Extension |
| ---------------------------- | ------------------ | -------------- |
| List files in storage bucket | 150 LOC, 2 hours   | 3 LOC, 2 min   |
| Verify file indexed          | 80 LOC, 1 hour     | 2 LOC, 1 min   |
| Get bucket statistics        | 120 LOC, 1.5 hours | 3 LOC, 2 min   |
| Debug folder access issues   | Manual API testing | Built-in utils |

**Real impact:** Test automation that took days to write now takes hours.

### 2. Production Reliability

- **Consistent error handling** - No ad-hoc try/except patterns
- **Automatic retries** - Inherits SDK's exponential backoff
- **Type safety** - Full type hints for IDE autocomplete
- **Battle-tested endpoints** - OData calls documented and validated

### 3. Team Knowledge Sharing

**Before:** Every developer maintains their own utils folder with slightly different implementations of folder lookup, bucket listing, etc.

**After:** Shared library with documentation. New developers onboard in minutes, not days.

### 4. Future-Proof

When SDK adds native support for these operations:
- Extension can delegate to SDK methods
- No breaking changes to your code
- Gradual migration path

---

## Security Best Practices

**Environment-based secrets:**
```bash
# .env (never commit)
UIPATH_URL=https://cloud.uipath.com/<account>/<tenant>/orchestrator_/
UIPATH_CLIENT_ID=your-client-id
UIPATH_CLIENT_SECRET=your-client-secret
UIPATH_FOLDER_KEY=your-folder-guid
```

**Developer checklist:**
- ✅ Add `.env` to `.gitignore`
- ✅ Use `.env.example` for team onboarding (with placeholders)
- ✅ Rotate client secrets regularly
- ✅ Grant minimum required scopes only
- ✅ Use separate credentials for dev/test/prod
- ✅ Never log credentials (even for debugging)

---

## Strategic Questions for Community Feedback

### 1. Would developers find SDK extension libraries valuable?

**The hypothesis:** Developer time is wasted re-implementing common patterns that should be library utilities.

**Validation questions:**
- Are you writing custom code for operations the SDK doesn't cover?
- How much time do you spend maintaining internal utility modules?
- Would you trust/use a community extension package vs. building your own?

**What we need to know:**
- Is the pain real enough that developers would adopt an external library?
- Or is "copy-paste from Stack Overflow" still the default approach?

### 2. Which platform areas have the biggest SDK gaps?

**Current evidence from Swagger spec vs SDK:**

| Orchestrator API Family | SDK Coverage                   | Gap Assessment                                                      |
| ----------------------- | ------------------------------ | ------------------------------------------------------------------- |
| **Context Grounding**   | Create, retrieve, ingest       | ❌ No file listing, no bucket inspection                             |
| **Storage Buckets**     | Upload, download single files  | ❌ No bulk operations, no file listing, no directory management      |
| **Queues**              | Full CRUD + transactions       | ✅ Mostly complete                                                   |
| **Jobs**                | Execute, retrieve, attachments | ⚠️ Missing: bulk operations, advanced filtering                      |
| **Test Automation**     | Not covered                    | ❌ Complete gap - TestSets, TestCases, Executions                    |
| **Stats/Monitoring**    | Not covered                    | ❌ Complete gap - License stats, job stats, consumption metrics      |
| **Folders**             | Not covered                    | ❌ Folder hierarchy navigation, permissions, cross-folder operations |
| **Documents (DU)**      | Basic operations               | ⚠️ Likely missing: validation queues, classification workflows       |

**Questions for developers:**
- Which areas do you most frequently drop to `sdk.api_client.request()` for?
- Where do you maintain the most internal wrapper code?
- Which workflows are most painful without high-level helpers?

### 3. What's the call to action for the community?

**Potential directions:**

**Option A: Curated Extensions Library** (current approach)
- Maintainers curate specific extensions based on demand
- Quality-controlled, documented, tested
- Slower to add new features
- **Trade-off:** Limited scope vs. high quality

**Option B: Community Cookbook Pattern**
- GitHub repo with community-contributed recipes
- Lower barrier to contribution (just working code examples)
- No package installation required (copy-paste patterns)
- **Trade-off:** Wider coverage vs. quality varies

**Option C: Plugin Architecture**
- SDK team provides extension points
- Community builds installable plugins
- Marketplace for discovery
- **Trade-off:** Most scalable vs. most complex infrastructure

**Option D: Official SDK Enhancement Proposals**
- Community submits enhancement requests with proof-of-concept
- Popular patterns get adopted into official SDK
- Extension libraries serve as proving ground
- **Trade-off:** Best long-term outcome vs. slowest iteration

**Which model serves developers best?**

---

## Phase 2 Status Update

**What's Been Delivered (v0.0.2):**

- ✅ **11 Extension Classes** - Complete coverage of operations, management, and workflows
- ✅ **~85+ Methods** - CRUD operations, bulk management, analytics, cross-folder operations
- ✅ **~25% API Coverage** - Up from ~3% in Phase 1 (covering ~85 of 339 endpoints)
- ✅ **Production-Ready** - Full type hints, comprehensive docstrings, error handling
- ✅ **Published on MyGet** - Available for installation and testing

**Coverage Achieved:**

| Category | Phase 1 (v0.0.1) | Phase 2 (v0.0.2) | Coverage |
|----------|------------------|------------------|----------|
| **Storage & Context** | ✅ Complete | ✅ Complete | 100% |
| **Assets** | ❌ Missing | ✅ Complete | 100% |
| **Jobs** | ⚠️ SDK Basic | ✅ Enhanced | 90% |
| **Queues** | ⚠️ SDK Transactions | ✅ Definitions | 85% |
| **Processes/Releases** | ⚠️ SDK Execution | ✅ Management | 80% |
| **Schedules** | ❌ Missing | ✅ Complete | 100% |
| **Libraries** | ❌ Missing | ✅ Complete | 90% |
| **Tasks/Forms** | ❌ Missing | ✅ Core Ops | 75% |
| **Folders** | ⚠️ Basic Utils | ✅ Full CRUD | 90% |

**Developer Impact:**

- **Time Savings:** Tasks that took 150+ LOC now take 3-5 lines
- **Reliability:** Automatic header management, folder context caching, retry logic
- **Discoverability:** Type hints and IDE autocomplete for all operations
- **Flexibility:** Cross-folder operations, bulk management, advanced filtering

## Call for Community Input

If you're a UiPath Python SDK user, we want to hear from you:

1. **Test Phase 2 Features** - Try the new extensions (assets, jobs, queues, tasks, schedules)
2. **Share Feedback** - Which extensions are most valuable? What's missing?
3. **Suggest Phase 3 Priorities** - Based on the [gap analysis](../../../tmp/orchestrator-api-gap-analysis.md), what should come next?
   - TestAutomationExt (29 endpoints, 0% coverage, high CI/CD demand)?
   - MonitoringExt (stats, audit logs, dashboards)?
   - RobotsExt (robot fleet management)?

**Discussion channels:**
- GitHub Gist: [cprima/10c7bbc6](https://gist.github.com/cprima/10c7bbc65dd578940c7654d13d083d9e)

**The goal:** Build what developers actually need, not what we think they need.
