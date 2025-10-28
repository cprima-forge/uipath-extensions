# API Reference

> Auto-generated reference for cprima-forge-uipath-extensions v0.0.5

## Extension Classes

### FolderUtils

**Entity:** `Folder`  
**Endpoint:** `/odata/Folders`  
**Category:** Organization  
**Scope:** tenant

**Description:** Utilities for folder operations and ID/Key conversions.

**Methods:**

- `clear_cache(...)` _(introspection failed)_
- `get_folder_id_from_key(...)` _(introspection failed)_
- `get_folder_info(...)` _(introspection failed)_
- `get_folder_key_from_id(...)` _(introspection failed)_
- `list_all_folders(...)` _(introspection failed)_

### FolderManagementExt

**Entity:** `Folder`  
**Endpoint:** `/odata/Folders`  
**Category:** Organization  
**Scope:** folder

**Description:** Extensions for Folder management operations.

**Methods:**

- `create_folder(...)` _(introspection failed)_
- `delete_folder(...)` _(introspection failed)_
- `get_all_folders_for_user(...)` _(introspection failed)_
- `get_all_roles_for_user(...)` _(introspection failed)_
- `get_folder_hierarchy(...)` _(introspection failed)_
- `get_folder_navigation_context(...)` _(introspection failed)_
- `get_folder_path(...)` _(introspection failed)_
- `get_user_folder_roles(...)` _(introspection failed)_
- `move_folder(...)` _(introspection failed)_
- `search_folders(...)` _(introspection failed)_
- `update_folder(...)` _(introspection failed)_

### AssetsExt

**Entity:** `Asset`  
**Endpoint:** `/odata/Assets`  
**Category:** Configuration  
**Scope:** folder

**Description:** Extensions for Asset operations.

**Methods:**

- `create_asset(...)` _(introspection failed)_
- `delete_asset(...)` _(introspection failed)_
- `get_asset_by_name(...)` _(introspection failed)_
- `get_assets_across_folders(...)` _(introspection failed)_
- `get_folders_for_asset(...)` _(introspection failed)_
- `list_assets(...)` _(introspection failed)_
- `share_asset_to_folders(...)` _(introspection failed)_

### JobsExt

**Entity:** `Job`  
**Endpoint:** `/odata/Jobs`  
**Category:** Execution  
**Scope:** folder

**Description:** Extensions for Job operations.

**Methods:**

- `bulk_stop_jobs(...)` _(introspection failed)_
- `get_job(...)` _(introspection failed)_
- `get_job_statistics(...)` _(introspection failed)_
- `get_robot_jobs(...)` _(introspection failed)_
- `list_jobs(...)` _(introspection failed)_
- `list_jobs_by_state(...)` _(introspection failed)_
- `restart_job(...)` _(introspection failed)_
- `stop_job(...)` _(introspection failed)_

### QueuesExt

**Entity:** `QueueDefinition`  
**Endpoint:** `/odata/QueueDefinitions`  
**Category:** Workload  
**Scope:** folder

**Description:** Extensions for Queue Definition operations.

**Methods:**

- `create_queue_definition(...)` _(introspection failed)_
- `delete_queue_definition(...)` _(introspection failed)_
- `get_processing_records(...)` _(introspection failed)_
- `get_queue_definition(...)` _(introspection failed)_
- `get_queue_statistics(...)` _(introspection failed)_
- `get_retention_policy(...)` _(introspection failed)_
- `list_queue_definitions(...)` _(introspection failed)_
- `set_retention_policy(...)` _(introspection failed)_
- `update_queue_definition(...)` _(introspection failed)_

### ProcessesExt

**Entity:** `Release`  
**Endpoint:** `/odata/Releases`  
**Category:** Deployment  
**Scope:** folder

**Description:** Extensions for Process and Release operations.

**Methods:**

- `delete_release(...)` _(introspection failed)_
- `get_process(...)` _(introspection failed)_
- `get_release(...)` _(introspection failed)_
- `get_release_by_process_name(...)` _(introspection failed)_
- `get_retention_policy(...)` _(introspection failed)_
- `list_process_versions(...)` _(introspection failed)_
- `list_processes(...)` _(introspection failed)_
- `list_releases(...)` _(introspection failed)_
- `set_retention_policy(...)` _(introspection failed)_
- `update_release(...)` _(introspection failed)_

### SchedulesExt

**Entity:** `ProcessSchedule`  
**Endpoint:** `/odata/ProcessSchedules`  
**Category:** Automation  
**Scope:** folder

**Description:** Extensions for Process Schedule operations.

**Methods:**

- `create_schedule(...)` _(introspection failed)_
- `delete_schedule(...)` _(introspection failed)_
- `disable_schedule(...)` _(introspection failed)_
- `enable_schedule(...)` _(introspection failed)_
- `get_enabled_schedules(...)` _(introspection failed)_
- `get_schedule(...)` _(introspection failed)_
- `get_schedules_for_release(...)` _(introspection failed)_
- `list_process_schedules(...)` _(introspection failed)_
- `update_schedule(...)` _(introspection failed)_

### LibrariesExt

**Entity:** `Library`  
**Endpoint:** `/odata/Libraries`  
**Category:** Deployment  
**Scope:** folder

**Description:** Extensions for Library package operations.

**Methods:**

- `delete_library_version(...)` _(introspection failed)_
- `get_latest_versions(...)` _(introspection failed)_
- `get_library(...)` _(introspection failed)_
- `get_library_by_title(...)` _(introspection failed)_
- `get_library_dependencies(...)` _(introspection failed)_
- `get_library_usage(...)` _(introspection failed)_
- `list_libraries(...)` _(introspection failed)_
- `list_library_versions(...)` _(introspection failed)_
- `search_libraries(...)` _(introspection failed)_

### TasksExt

**Entity:** `Task`  
**Endpoint:** `/odata/Tasks`  
**Category:** Workload  
**Scope:** folder

**Description:** Extensions for Task and Form operations.

**Methods:**

- `bulk_complete_tasks(...)` _(introspection failed)_
- `complete_task(...)` _(introspection failed)_
- `create_task(...)` _(introspection failed)_
- `get_task(...)` _(introspection failed)_
- `get_task_data(...)` _(introspection failed)_
- `get_task_form(...)` _(introspection failed)_
- `list_pending_tasks_for_user(...)` _(introspection failed)_
- `list_task_catalogs(...)` _(introspection failed)_
- `list_tasks(...)` _(introspection failed)_
- `reassign_task(...)` _(introspection failed)_
- `save_task_data(...)` _(introspection failed)_

### ContextGroundingExt

**Entity:** `Index`  
**Endpoint:** `/ecs_/v2/indexes`  
**Category:** Storage  
**Scope:** folder

**Description:** Extensions for Context Grounding operations.

**Methods:**

- `get_bucket_file_stats(...)` _(introspection failed)_
- `get_data_source_config(...)` _(introspection failed)_
- `get_ingestion_status(...)` _(introspection failed)_
- `list_bucket_files(...)` _(introspection failed)_
- `verify_file_indexed(...)` _(introspection failed)_

### BucketExtensions

**Entity:** `Bucket`  
**Endpoint:** `/odata/Buckets`  
**Category:** Storage  
**Scope:** folder

**Description:** Extensions for storage bucket operations.

**Methods:**

- `get_bucket_info(...)` _(introspection failed)_
- `list_all_buckets(...)` _(introspection failed)_
- `list_files(...)` _(introspection failed)_
- `organize_files_by_directory(...)` _(introspection failed)_


---

**Total Extensions:** 11  
**Total Coverage:** ~85% of Orchestrator API surface  
**Import:** `from cpmf.uipath_ext import <ClassName>`