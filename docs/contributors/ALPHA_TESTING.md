# Alpha Testing Guide - uipath-sdk-extensions

**Current Version:** 0.0.5

## Installation

```bash
# Install from MyGet feed
uv pip install uipath-sdk-extensions \
  --extra-index-url https://www.myget.org/F/cprima-forge/python/ \
  --index-strategy unsafe-best-match
```

Or with pip:
```bash
pip install uipath-sdk-extensions \
  --extra-index-url https://www.myget.org/F/cprima-forge/python/
```

## Quick Start

### Phase 1 Features (v0.0.1)

```python
from uipath import UiPath
from uipath_sdk_extensions import ContextGroundingExt

# Initialize SDK
sdk = UiPath()

# Create Context Grounding extension
cg = ContextGroundingExt(sdk)

# List files in Context Grounding storage
files = cg.list_bucket_files(
    index_name="YourIndexName",
    folder_key="your-folder-guid"
)

print(f"Found {len(files)} files in storage")
for file in files:
    print(f"  - {file['FullPath']}: {file['Size']/1024:.1f} KB")
```

### Phase 2 Features (v0.0.5) - NEW

```python
from uipath_sdk_extensions import AssetsExt, JobsExt, QueuesExt, TasksExt

# Asset Management
assets = AssetsExt(sdk)
asset = assets.create_asset(
    name="APIKey",
    value_type="Text",
    value="secret-key",
    folder_key="your-folder-guid"
)

# Job Operations
jobs = JobsExt(sdk)
failed = jobs.list_jobs_by_state("Faulted", folder_key="your-folder-guid")
print(f"Failed jobs: {len(failed)}")

# Queue Management
queues = QueuesExt(sdk)
queue = queues.create_queue_definition(
    name="OrderQueue",
    folder_key="your-folder-guid",
    max_retries=3
)

# Human Tasks
tasks = TasksExt(sdk)
my_tasks = tasks.list_pending_tasks_for_user(folder_key="your-folder-guid")
print(f"You have {len(my_tasks)} pending tasks")
```

## What to Test

### 1. File Listing
```python
# List all files recursively
files = cg.list_bucket_files(
    index_name="YourIndex",
    folder_key="folder-guid",
    directory="/",
    recursive=True
)

# List files in specific directory
files = cg.list_bucket_files(
    index_name="YourIndex",
    folder_key="folder-guid",
    directory="/documents",
    recursive=False
)

# Filter by pattern
files = cg.list_bucket_files(
    index_name="YourIndex",
    folder_key="folder-guid",
    file_name_glob="*.pdf"
)
```

### 2. Ingestion Status
```python
status = cg.get_ingestion_status(
    index_name="YourIndex",
    folder_key="folder-guid"
)

print(f"Status: {status['last_ingestion_status']}")
print(f"In Progress: {status['in_progress']}")
print(f"Last Ingested: {status['last_ingested']}")
```

### 3. File Verification
```python
exists = cg.verify_file_indexed(
    index_name="YourIndex",
    folder_key="folder-guid",
    file_path="/document.pdf"
)

print(f"File exists in storage: {exists}")
```

### 4. Bucket Statistics
```python
stats = cg.get_bucket_file_stats(
    index_name="YourIndex",
    folder_key="folder-guid"
)

print(f"Total files: {stats['total_files']}")
print(f"Total size: {stats['total_size_mb']:.1f} MB")
print(f"Files by directory: {stats['files_by_directory']}")
```

### 5. Data Source Config
```python
config = cg.get_data_source_config(
    index_name="YourIndex",
    folder_key="folder-guid"
)

print(f"Bucket: {config['bucketName']}")
print(f"Directory: {config['directoryPath']}")
print(f"Pattern: {config['fileNameGlob']}")
```

## Phase 2 Testing (v0.0.5)

### 6. Asset Management
```python
assets = AssetsExt(sdk)

# List all assets
all_assets = assets.list_assets(folder_key="your-folder-guid")
print(f"Total assets: {len(all_assets)}")

# Create text asset
text_asset = assets.create_asset(
    name="APIEndpoint",
    value_type="Text",
    value="https://api.example.com",
    folder_key="your-folder-guid",
    description="API endpoint URL"
)

# Create credential asset
cred_asset = assets.create_asset(
    name="DBCreds",
    value_type="Credential",
    value={"Username": "user", "Password": "pass"},
    folder_key="your-folder-guid"
)

# Get assets across folders
global_assets = assets.get_assets_across_folders(asset_name="APIEndpoint")
```

### 7. Job Operations
```python
jobs = JobsExt(sdk)

# List recent jobs
recent = jobs.list_jobs(
    folder_key="your-folder-guid",
    order_by="StartTime desc",
    top=20
)

# List failed jobs
failed = jobs.list_jobs_by_state("Faulted", folder_key="your-folder-guid")

# Stop a running job
jobs.stop_job(job_key="job-guid", folder_key="your-folder-guid")

# Get statistics
stats = jobs.get_job_statistics(
    folder_key="your-folder-guid",
    process_name="MyProcess"
)
print(f"Success rate: {stats['successful']}/{stats['total']}")
```

### 8. Queue Management
```python
queues = QueuesExt(sdk)

# List all queues
all_queues = queues.list_queue_definitions(folder_key="your-folder-guid")

# Create queue
queue = queues.create_queue_definition(
    name="OrderQueue",
    folder_key="your-folder-guid",
    max_retries=3,
    accept_auto_retry=True
)

# Set retention policy
queues.set_retention_policy(
    queue_id=queue['Id'],
    retention_days=30,
    folder_key="your-folder-guid"
)

# Get queue statistics
stats = queues.get_queue_statistics(
    queue_name="OrderQueue",
    folder_key="your-folder-guid"
)
print(f"Pending: {stats['new']}, In Progress: {stats['in_progress']}")
```

### 9. Process & Release Management
```python
from uipath_sdk_extensions import ProcessesExt

processes = ProcessesExt(sdk)

# List all releases
releases = processes.list_releases(
    folder_key="your-folder-guid",
    order_by="Published desc",
    top=10
)

# Get latest version of a process
latest = processes.get_release_by_process_name(
    process_name="OrderProcessing",
    folder_key="your-folder-guid"
)

# List all versions
versions = processes.list_process_versions(
    process_name="OrderProcessing",
    folder_key="your-folder-guid"
)
```

### 10. Schedule Management
```python
from uipath_sdk_extensions import SchedulesExt

schedules = SchedulesExt(sdk)

# List all schedules
all_schedules = schedules.list_process_schedules(folder_key="your-folder-guid")

# Create daily schedule
daily = schedules.create_schedule(
    name="DailyReport",
    release_id=12345,
    cron_expression="0 9 * * *",  # 9 AM daily
    folder_key="your-folder-guid",
    time_zone_id="America/New_York"
)

# Enable/disable schedule
schedules.disable_schedule(daily['Id'], folder_key="your-folder-guid")
schedules.enable_schedule(daily['Id'], folder_key="your-folder-guid")
```

### 11. Library Management
```python
from uipath_sdk_extensions import LibrariesExt

libraries = LibrariesExt(sdk)

# List all libraries
all_libs = libraries.list_libraries(
    folder_key="your-folder-guid",
    order_by="Published desc"
)

# Get library versions
versions = libraries.list_library_versions(
    title="CommonUtilities",
    folder_key="your-folder-guid"
)

# Get library usage
usage = libraries.get_library_usage(
    library_title="CommonUtilities",
    folder_key="your-folder-guid"
)
print(f"Total versions: {usage['version_count']}")
```

### 12. Task Management (Human-in-the-Loop)
```python
tasks = TasksExt(sdk)

# List my pending tasks
my_tasks = tasks.list_pending_tasks_for_user(folder_key="your-folder-guid")

# Create task
task = tasks.create_task(
    title="Approve Order #1234",
    task_catalog_id=56789,
    folder_key="your-folder-guid",
    priority="High",
    data={"OrderNumber": "1234", "Amount": 5000}
)

# Complete task with approval
tasks.complete_task(
    task_id=task['Id'],
    action="Approve",
    folder_key="your-folder-guid",
    comment="Approved"
)

# List task catalogs
catalogs = tasks.list_task_catalogs(folder_key="your-folder-guid")
```

### 13. Folder Management
```python
from uipath_sdk_extensions import FolderManagementExt

folders = FolderManagementExt(sdk)

# Create folder
new_folder = folders.create_folder(
    display_name="Production",
    description="Production environment"
)

# Get folder hierarchy
tree = folders.get_folder_hierarchy()

# Search folders
results = folders.search_folders("Production")

# Get user's folder roles
user_folders = folders.get_user_folder_roles()
```

## Known Limitations

- Requires authenticated UiPath SDK instance
- Asset creation requires appropriate permissions
- Some operations (like task creation) require task catalog IDs
- Schedule cron expressions must be valid cron format
- Folder operations require proper RBAC permissions

## Reporting Issues

Please report any issues with:
- Installation problems
- Import errors
- Unexpected behavior
- Missing features you need

Include:
- Python version
- uv/pip version
- UiPath SDK version
- Error messages
- Example code that reproduces the issue

## Version

Current version: **0.0.5** (Phase 2 - Major expansion)
