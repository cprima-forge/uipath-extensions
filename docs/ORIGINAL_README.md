# UiPath SDK Extensions

**Production-ready extensions for the UiPath Python SDK that bridge critical API gaps**

Version: **0.0.2** (Phase 2 - Major expansion)

## Problem Statement

The official UiPath Python SDK covers ~15% of the Orchestrator API surface, leaving critical gaps in operations, management, and automation capabilities.

### What's Missing from the SDK

**Phase 1 Gaps (v0.0.1):**
- ❌ **No file listing** - Can't see what's in Context Grounding storage buckets
- ❌ **No ingestion visibility** - Can't verify which files were indexed vs skipped
- ❌ **Inconsistent headers** - Some endpoints need `folder_key`, others need `OrganizationUnitId`
- ❌ **No bucket operations** - Can't inspect storage bucket configuration
- ❌ **No folder utilities** - Manual conversion between folder IDs and keys

**Phase 2 Gaps (v0.0.2):**
- ❌ **No asset management** - Can't list, create, or delete assets
- ❌ **No job operations** - Can't list, stop, or bulk manage jobs
- ❌ **No queue definitions** - Can't create or configure queues
- ❌ **No process/release management** - Can't list versions or manage retention
- ❌ **No schedule management** - Can't create or manage time-based triggers
- ❌ **No library operations** - Can't manage reusable package libraries
- ❌ **No task/form management** - Can't create or complete human-in-the-loop tasks
- ❌ **No folder management** - Can't create, update, or delete folders

### The Workaround (Without This Library)

```python
# Manual API calls with hardcoded endpoints, header management, and ID conversions
folder_response = sdk.api_client.request("GET", "/odata/Folders")
folder_id = None
for folder in folder_response.json()["value"]:
    if folder["Key"] == folder_key:
        folder_id = folder["Id"]
        break

bucket_response = sdk.api_client.request(
    "GET",
    "/odata/Buckets",
    headers={"X-UIPATH-OrganizationUnitId": str(folder_id)}
)
# ... 50 more lines of manual parsing and error handling
```

## Solution

**uipath-sdk-extensions** provides clean, tested, documented wrappers around missing SDK functionality.

### Installation

```bash
pip install uipath-sdk-extensions
```

**Privacy Note:** This library wraps the official UiPath Python SDK, which collects basic usage telemetry by default. To disable telemetry, set the environment variable before using the SDK:

```python
import os
os.environ["UIPATH_TELEMETRY_ENABLED"] = "false"

# Or use the helper function
from uipath_sdk_extensions import disable_telemetry
disable_telemetry()

from uipath import UiPath
sdk = UiPath()  # Telemetry now disabled
```

Alternatively, set the environment variable system-wide:
```bash
# Linux/macOS
export UIPATH_TELEMETRY_ENABLED=false

# Windows PowerShell
$env:UIPATH_TELEMETRY_ENABLED="false"

# Windows CMD
set UIPATH_TELEMETRY_ENABLED=false
```

### Usage

```python
from uipath import UiPath
from uipath_sdk_extensions import ContextGroundingExt, FolderUtils

sdk = UiPath()

# Context Grounding extensions
cg = ContextGroundingExt(sdk)

# List all files in storage bucket (including subdirectories)
files = cg.list_bucket_files(
    index_name="MyIndex",
    folder_key="5ebb73c3-b114-43b2-8615-c6a093e0eaab",
    recursive=True
)

for file in files:
    print(f"{file['FullPath']}: {file['Size']/1024:.1f} KB")

# Verify file was indexed
is_indexed = cg.verify_file_indexed(
    index_name="MyIndex",
    folder_key="5ebb73c3-b114-43b2-8615-c6a093e0eaab",
    file_path="/documents/invoice_001.pdf"
)

# Folder utilities
utils = FolderUtils(sdk)
folder_id = utils.get_folder_id_from_key("5ebb73c3-b114-43b2-8615-c6a093e0eaab")
folder_key = utils.get_folder_key_from_id(5083200)
```

## Features

### Phase 1 Extensions (v0.0.1)

**ContextGroundingExt** - Storage inspection for Context Grounding:
- `list_bucket_files()` - List all files in storage bucket with subdirectory support
- `get_ingestion_status()` - Enhanced status check with detailed metrics
- `verify_file_indexed()` - Check if specific file was ingested
- `get_bucket_file_stats()` - Get file statistics and directory breakdown

**BucketExtensions** - Direct storage bucket operations:
- `list_files()` - List files with filtering and pagination
- `get_bucket_info()` - Retrieve bucket metadata and configuration
- `list_all_buckets()` - List all storage buckets in a folder
- `organize_files_by_directory()` - Group files for analysis

**FolderUtils** - Folder ID/Key conversion and caching:
- `get_folder_id_from_key()` - Convert folder GUID to numeric ID (cached)
- `get_folder_key_from_id()` - Convert numeric ID back to GUID
- `list_all_folders()` - Get all accessible folders
- `get_folder_info()` - Get complete folder information

### Phase 2 Extensions (v0.0.2) - NEW

**AssetsExt** - Complete asset CRUD operations:
- `list_assets()` - List assets with filtering and pagination
- `create_asset()` - Create new assets (text, credentials, etc.)
- `delete_asset()` - Remove assets
- `get_assets_across_folders()` - Multi-folder asset queries
- `share_asset_to_folders()` - Cross-folder asset sharing

**JobsExt** - Enhanced job operations:
- `list_jobs()` - List jobs with filters and pagination
- `stop_job()` / `bulk_stop_jobs()` - Cancel running jobs
- `restart_job()` - Retry failed jobs
- `get_job_statistics()` - Aggregated success/failure metrics
- `list_jobs_by_state()` - Filter by job state

**QueuesExt** - Queue definition management:
- `list_queue_definitions()` - List all queue configurations
- `create_queue_definition()` - Define new queues with retry policies
- `update_queue_definition()` / `delete_queue_definition()` - Modify queues
- `set_retention_policy()` - Configure data retention
- `get_queue_statistics()` - Item counts by status

**ProcessesExt** - Process and release management:
- `list_releases()` - List all release versions
- `get_release_by_process_name()` - Get latest or specific version
- `list_process_versions()` - Version history for a process
- `set_retention_policy()` - Release data retention
- `update_release()` / `delete_release()` - Release management

**SchedulesExt** - Time-based process triggers:
- `list_process_schedules()` - List all cron-like schedules
- `create_schedule()` - Define new time-based triggers
- `update_schedule()` / `delete_schedule()` - Modify schedules
- `enable_schedule()` / `disable_schedule()` - Toggle schedules
- `get_schedules_for_release()` - Find schedules by release

**LibrariesExt** - Reusable package management:
- `list_libraries()` - List all library packages
- `get_library_by_title()` - Get library by name and version
- `list_library_versions()` - Version history for a library
- `delete_library_version()` - Remove specific versions
- `get_library_usage()` - Usage statistics

**TasksExt** - Human-in-the-loop workflows:
- `list_tasks()` - List tasks with filtering
- `create_task()` - Create form tasks for human approval
- `complete_task()` - Submit task with action (Approve/Reject)
- `save_task_data()` - Draft save without completing
- `reassign_task()` - Transfer task ownership
- `bulk_complete_tasks()` - Process multiple tasks
- `list_task_catalogs()` - Available task type definitions

**FolderManagementExt** - Full folder CRUD:
- `create_folder()` - Provision new folders/subfolders
- `delete_folder()` / `update_folder()` - Manage folders
- `get_folder_hierarchy()` - Tree structure navigation
- `move_folder()` - Reorganize folder structure
- `get_user_folder_roles()` - Permission matrix
- `search_folders()` - Find folders by name/description

## Quick Start Examples

### Asset Management
```python
from uipath import UiPath
from uipath_sdk_extensions import AssetsExt

sdk = UiPath()
assets = AssetsExt(sdk)

# Create credential asset
asset = assets.create_asset(
    name="DatabaseCreds",
    value_type="Credential",
    value={"Username": "admin", "Password": "secret"},
    folder_key="5ebb73c3-...",
    description="Production database credentials"
)

# List all credential assets
creds = assets.list_assets(
    folder_key="5ebb73c3-...",
    filter_query="ValueType eq 'Credential'"
)
```

### Job Operations
```python
from uipath_sdk_extensions import JobsExt

jobs = JobsExt(sdk)

# Get failed jobs from today
from datetime import datetime, UTC
today = datetime.now(UTC).strftime("%Y-%m-%d")
failed = jobs.list_jobs(
    folder_key="5ebb73c3-...",
    filter_query=f"State eq 'Faulted' and StartTime ge {today}T00:00:00Z"
)

# Bulk stop all running jobs for a process
running = jobs.list_jobs(
    filter_query="State eq 'Running' and ProcessName eq 'MyProcess'",
    folder_key="5ebb73c3-..."
)
job_keys = [job['Key'] for job in running]
jobs.bulk_stop_jobs(job_keys, folder_key="5ebb73c3-...")

# Get statistics
stats = jobs.get_job_statistics(
    folder_key="5ebb73c3-...",
    process_name="OrderProcessing"
)
print(f"Success rate: {stats['successful']}/{stats['total']}")
```

### Queue Management
```python
from uipath_sdk_extensions import QueuesExt

queues = QueuesExt(sdk)

# Create queue with retry policy
queue = queues.create_queue_definition(
    name="OrderProcessing",
    folder_key="5ebb73c3-...",
    description="Queue for processing orders",
    max_retries=3,
    accept_auto_retry=True,
    enforce_unique_reference=True
)

# Set 30-day retention
queues.set_retention_policy(
    queue_id=queue['Id'],
    retention_days=30,
    folder_key="5ebb73c3-..."
)

# Get queue statistics
stats = queues.get_queue_statistics(
    queue_name="OrderProcessing",
    folder_key="5ebb73c3-..."
)
print(f"Pending: {stats['new']}, Failed: {stats['failed']}")
```

### Task Workflows (Human-in-the-Loop)
```python
from uipath_sdk_extensions import TasksExt

tasks = TasksExt(sdk)

# Create approval task
task = tasks.create_task(
    title="Approve Purchase Order #1234",
    task_catalog_id=56789,
    folder_key="5ebb73c3-...",
    priority="High",
    data={"OrderNumber": "1234", "Amount": 5000, "Vendor": "Acme Corp"}
)

# List pending tasks for current user
my_tasks = tasks.list_pending_tasks_for_user(folder_key="5ebb73c3-...")

# Complete task with approval
tasks.complete_task(
    task_id=task['Id'],
    action="Approve",
    folder_key="5ebb73c3-...",
    comment="Approved - within budget"
)
```

### Schedule Management
```python
from uipath_sdk_extensions import SchedulesExt

schedules = SchedulesExt(sdk)

# Daily report at 9 AM
daily_schedule = schedules.create_schedule(
    name="DailyReport",
    release_id=67890,
    cron_expression="0 9 * * *",
    folder_key="5ebb73c3-...",
    time_zone_id="America/New_York",
    enabled=True
)

# Weekday processing at 8 AM
weekday_schedule = schedules.create_schedule(
    name="WeekdayProcessing",
    release_id=67890,
    cron_expression="0 8 * * 1-5",  # Mon-Fri
    folder_key="5ebb73c3-..."
)
```

## Design Principles

1. **Composition over Inheritance** - Wraps SDK, doesn't replace it
2. **Automatic Authentication** - Leverages `sdk.api_client` for auth and retry logic
3. **Minimal Dependencies** - Only requires the UiPath SDK
4. **Type-Safe** - Full type hints for IDE autocomplete
5. **Production-Ready** - Comprehensive error handling and logging

## API Reference

### ContextGroundingExt

```python
class ContextGroundingExt:
    """Extensions for Context Grounding operations"""

    def __init__(self, sdk: UiPath):
        """Initialize with UiPath SDK instance"""

    def list_bucket_files(
        self,
        index_name: str,
        folder_key: str,
        directory: str = "/",
        recursive: bool = True,
        file_name_glob: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all files in the Context Grounding storage bucket

        Args:
            index_name: Name of the Context Grounding index
            folder_key: Folder GUID
            directory: Root directory to list (default: "/")
            recursive: Include subdirectories (default: True)
            file_name_glob: Optional file filter (e.g., "*.pdf")

        Returns:
            List of file dictionaries with FullPath, Size, ContentType, etc.

        Raises:
            ValueError: If index or folder not found
        """

    def get_ingestion_status(
        self,
        index_name: str,
        folder_key: str
    ) -> Dict[str, Any]:
        """Get detailed ingestion status for an index"""

    def verify_file_indexed(
        self,
        index_name: str,
        folder_key: str,
        file_path: str
    ) -> bool:
        """Check if a specific file exists in the storage bucket"""

    def get_bucket_file_stats(
        self,
        index_name: str,
        folder_key: str
    ) -> Dict[str, Any]:
        """Get statistics about files in the storage bucket"""

    def get_data_source_config(
        self,
        index_name: str,
        folder_key: str
    ) -> Dict[str, Any]:
        """Get the data source configuration for an index"""
```

## Real-World Use Case

During Context Grounding testing, a common workflow involves:

1. Upload documents to storage
2. Verify they were stored in the bucket
3. Trigger ingestion
4. Confirm which files were indexed vs skipped
5. Run validation tests

**Without this library**: 150+ lines of manual API calls, header juggling, and error-prone ID conversions

**With this library**: 15 lines of clean, readable code

```python
cg = ContextGroundingExt(sdk)

# Upload files
for md_file in corpus_files:
    pdf_bytes = convert_to_pdf(md_file)
    sdk.context_grounding.add_to_index(name=index_name, content=pdf_bytes, ...)

# Verify storage
files = cg.list_bucket_files(index_name, folder_key)
print(f"Stored: {len(files)} files")

# Get statistics
stats = cg.get_bucket_file_stats(index_name, folder_key)
print(f"Total size: {stats['total_size_mb']:.1f} MB")

# Trigger ingestion
sdk.context_grounding.ingest_data(index, folder_key)

# Check status
status = cg.get_ingestion_status(index_name, folder_key)
print(f"Status: {status['last_ingestion_status']}")
```

## Technical Background

### SDK Architecture

The UiPath Python SDK provides high-level service classes (`context_grounding`, `buckets`, etc.) but doesn't cover all API endpoints. It exposes `sdk.api_client` as an escape hatch for direct HTTP requests.

This library uses `sdk.api_client` to access:

- **OData endpoints**: `/odata/Buckets({id})/UiPath.Server.Configuration.OData.GetFiles`
- **REST API endpoints**: `/api/Buckets/{id}/ListFiles`
- **Folder operations**: `/odata/Folders` for ID/Key lookups

All documented in the official Swagger spec at `https://cloud.uipath.com/{account}/{tenant}/orchestrator_/swagger/`

### Header Management

Different API families require different authentication headers:

| SDK Service       | Header Required               | Value Type |
| ----------------- | ----------------------------- | ---------- |
| Context Grounding | `x-uipath-folderkey`          | GUID       |
| Storage Buckets   | `X-UIPATH-OrganizationUnitId` | Numeric ID |
| OData Folders     | `x-uipath-folderkey`          | GUID       |

This library handles header selection automatically based on the endpoint.

## Requirements

- Python >= 3.10
- uipath >= 2.1.111

## Contributing

This library was created to solve real gaps discovered during production SDK usage. Contributions welcome for:

- Additional Context Grounding utilities
- Enhanced ingestion monitoring
- Cross-folder operations
- Async method variants

## License

CC BY 4.0 License

## Acknowledgments

- Addresses real pain points from Context Grounding production usage
- Inspired by the UiPath Python SDK team's `api_client` escape hatch pattern

## Links

- **UiPath Python SDK**: https://github.com/UiPath/uipath-python
- **Swagger Spec**: Orchestrator API reference at `{base_url}/swagger/`
