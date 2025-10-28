"""cpmf.uipath_ext - Community-built extensions for the UiPath Python SDK

This library bridges critical gaps in the official UiPath Python SDK by providing
clean, tested wrappers around missing API functionality.

Privacy Notice:
    This library wraps the official UiPath Python SDK, which collects basic usage
    telemetry by default. To disable telemetry, call disable_telemetry() before
    initializing the UiPath SDK, or set UIPATH_TELEMETRY_ENABLED=false environment
    variable.

Main Classes:
    ContextGroundingExt: Extensions for Context Grounding storage inspection
    BucketExtensions: Direct storage bucket operations
    FolderUtils: Folder ID/Key conversion and navigation utilities
    FolderManagementExt: Full folder CRUD and management operations
    AssetsExt: Asset management and cross-folder operations
    JobsExt: Enhanced job operations and bulk management
    QueuesExt: Queue definition and retention policy management
    ProcessesExt: Process and release version management
    SchedulesExt: Process schedule (cron-like) management
    LibrariesExt: Library package management
    TasksExt: Human-in-the-loop task and form management

Example:
    >>> from cpmf.uipath_ext import disable_telemetry
    >>> disable_telemetry()  # Disable UiPath SDK telemetry
    >>>
    >>> from uipath import UiPath
    >>> from cpmf.uipath_ext import ContextGroundingExt, JobsExt, AssetsExt
    >>>
    >>> sdk = UiPath()
    >>>
    >>> # Context Grounding - List files in storage
    >>> cg = ContextGroundingExt(sdk)
    >>> files = cg.list_bucket_files(
    ...     index_name="MyIndex",
    ...     folder_key="5ebb73c3-b114-43b2-8615-c6a093e0eaab"
    ... )
    >>> print(f"Found {len(files)} files in storage")
    >>>
    >>> # Jobs - List recent failed jobs
    >>> jobs = JobsExt(sdk)
    >>> failed = jobs.list_jobs_by_state("Faulted", folder_key="5ebb73c3-...", top=10)
    >>> print(f"Recent failures: {len(failed)}")
    >>>
    >>> # Assets - Create and manage assets
    >>> assets = AssetsExt(sdk)
    >>> asset = assets.create_asset(
    ...     name="APIKey",
    ...     value_type="Text",
    ...     value="secret-key",
    ...     folder_key="5ebb73c3-..."
    ... )

For detailed documentation, see: https://github.com/cprima-forge/uipath-extensions
"""

import os
from importlib.metadata import PackageNotFoundError, version
from typing import Dict, Any, List, Type

from .context_grounding import ContextGroundingExt
from .buckets import BucketExtensions
from .folder_utils import FolderUtils
from .folders import FolderManagementExt
from .assets import AssetsExt
from .jobs import JobsExt
from .queues import QueuesExt
from .processes import ProcessesExt
from .schedules import SchedulesExt
from .libraries import LibrariesExt
from .tasks import TasksExt

try:
    __version__ = version("cprima-forge-uipath-extensions")
except PackageNotFoundError:
    # Package is not installed, use development version
    __version__ = "0.0.0.dev"

__all__ = [
    "ContextGroundingExt",
    "BucketExtensions",
    "FolderUtils",
    "FolderManagementExt",
    "AssetsExt",
    "JobsExt",
    "QueuesExt",
    "ProcessesExt",
    "SchedulesExt",
    "LibrariesExt",
    "TasksExt",
    "get_all_extensions",
    "get_extension_metadata",
    "disable_telemetry",
    "is_telemetry_enabled",
]


def disable_telemetry() -> None:
    """Disable UiPath SDK telemetry collection.

    This function sets the UIPATH_TELEMETRY_ENABLED environment variable to "false",
    which disables the official UiPath Python SDK's usage telemetry collection.

    Must be called before initializing the UiPath SDK instance for it to take effect.

    Example:
        >>> from cpmf.uipath_ext import disable_telemetry
        >>> disable_telemetry()
        >>>
        >>> from uipath import UiPath
        >>> sdk = UiPath()  # Telemetry now disabled

    Note:
        This only affects the UiPath SDK's telemetry. This library (cprima-forge-uipath-extensions)
        does not collect any telemetry data.
    """
    os.environ["UIPATH_TELEMETRY_ENABLED"] = "false"


def is_telemetry_enabled() -> bool:
    """Check if UiPath SDK telemetry is currently enabled.

    Returns:
        bool: True if telemetry is enabled (default), False if disabled

    Example:
        >>> from cpmf.uipath_ext import is_telemetry_enabled
        >>> if is_telemetry_enabled():
        ...     print("Telemetry is enabled")
    """
    return os.environ.get("UIPATH_TELEMETRY_ENABLED", "true").lower() != "false"


def get_all_extensions() -> List[Type]:
    """Return all extension classes for introspection.

    Used by probe scripts and discovery tools to enumerate all available
    extension classes without hardcoding class names.

    Returns:
        List of extension class types

    Example:
        >>> from cpmf.uipath_ext import get_all_extensions
        >>> from uipath import UiPath
        >>>
        >>> sdk = UiPath()
        >>> for ext_class in get_all_extensions():
        ...     ext = ext_class(sdk)
        ...     print(f"{ext_class.__name__}: {ext.__doc__}")
    """
    return [
        FolderUtils,
        FolderManagementExt,
        AssetsExt,
        JobsExt,
        QueuesExt,
        ProcessesExt,
        SchedulesExt,
        LibrariesExt,
        TasksExt,
        ContextGroundingExt,
        BucketExtensions,
    ]


def get_extension_metadata() -> Dict[str, Dict[str, Any]]:
    """Return metadata about each extension class.

    Provides structured information about each extension including the entity
    type it manages and the primary OData endpoint it uses.

    Returns:
        Dict mapping class names to their metadata (entity type, endpoint)

    Example:
        >>> from cpmf.uipath_ext import get_extension_metadata
        >>>
        >>> metadata = get_extension_metadata()
        >>> print(metadata["AssetsExt"])
        {'entity': 'Asset', 'endpoint': '/odata/Assets', 'category': 'Configuration'}
    """
    return {
        "FolderUtils": {
            "entity": "Folder",
            "endpoint": "/odata/Folders",
            "category": "Organization",
            "scope": "tenant",
            "description": "Folder ID/Key conversion and navigation utilities"
        },
        "FolderManagementExt": {
            "entity": "Folder",
            "endpoint": "/odata/Folders",
            "category": "Organization",
            "scope": "folder",
            "description": "Full folder CRUD and management operations"
        },
        "AssetsExt": {
            "entity": "Asset",
            "endpoint": "/odata/Assets",
            "category": "Configuration",
            "scope": "folder",
            "description": "Asset management and cross-folder operations"
        },
        "JobsExt": {
            "entity": "Job",
            "endpoint": "/odata/Jobs",
            "category": "Execution",
            "scope": "folder",
            "description": "Enhanced job operations and bulk management"
        },
        "QueuesExt": {
            "entity": "QueueDefinition",
            "endpoint": "/odata/QueueDefinitions",
            "category": "Workload",
            "scope": "folder",
            "description": "Queue definition and retention policy management"
        },
        "ProcessesExt": {
            "entity": "Release",
            "endpoint": "/odata/Releases",
            "category": "Deployment",
            "scope": "folder",
            "description": "Process and release version management"
        },
        "SchedulesExt": {
            "entity": "ProcessSchedule",
            "endpoint": "/odata/ProcessSchedules",
            "category": "Automation",
            "scope": "folder",
            "description": "Process schedule (cron-like) management"
        },
        "LibrariesExt": {
            "entity": "Library",
            "endpoint": "/odata/Libraries",
            "category": "Deployment",
            "scope": "folder",
            "description": "Library package management"
        },
        "TasksExt": {
            "entity": "Task",
            "endpoint": "/odata/Tasks",
            "category": "Workload",
            "scope": "folder",
            "description": "Human-in-the-loop task and form management"
        },
        "ContextGroundingExt": {
            "entity": "Index",
            "endpoint": "/ecs_/v2/indexes",
            "category": "Storage",
            "scope": "folder",
            "description": "Context Grounding storage inspection"
        },
        "BucketExtensions": {
            "entity": "Bucket",
            "endpoint": "/odata/Buckets",
            "category": "Storage",
            "scope": "folder",
            "description": "Direct storage bucket operations"
        },
    }
