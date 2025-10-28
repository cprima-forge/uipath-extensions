# Library Best Practices

This document outlines the design principles and best practices for `uipath-sdk-extensions`, informed by Python API wrapper library standards and SDK extension patterns.

## Core Philosophy

**uipath-sdk-extensions is a production SDK extension that:**
- Extends (not replaces) the official UiPath Python SDK
- Fills API gaps with clean, predictable wrappers
- Returns raw data structures (dicts, lists) without presentation logic
- Uses naming conventions as self-documenting metadata
- Enables introspection through Python's built-in capabilities

## Design Principles

### 1. Separation of Concerns

**Libraries Return Raw Data**
```python
# ✅ GOOD: Library returns raw dict/list
def list_assets(self, folder_key: str) -> List[Dict[str, Any]]:
    response = self.sdk.api_client.request("GET", "/odata/Assets", ...)
    return response.json().get("value", [])

# ❌ BAD: Library handles presentation
def list_assets(self, folder_key: str) -> None:
    assets = self.sdk.api_client.request("GET", "/odata/Assets", ...)
    for asset in assets:
        print(f"📦 {asset['Name']}")  # NO! Presentation logic doesn't belong here
```

**Why:** Consuming code (CLI tools, web apps, probe scripts) needs flexibility to format data differently. Libraries provide data, consumers present it.

### 2. Avoid God Objects

**Split by Entity Type**
```python
# ✅ GOOD: Separate classes per entity
class AssetsExt:      # Manages assets only
class JobsExt:        # Manages jobs only
class QueuesExt:      # Manages queues only

# ❌ BAD: One giant class
class UiPathExtensions:
    def list_assets(self): ...
    def list_jobs(self): ...
    def list_queues(self): ...
    # ... 100+ methods
```

**Why:** Single Responsibility Principle. Each class has one reason to change. Easier to test, maintain, and extend.

### 3. Naming Conventions as Metadata

Method names are self-documenting. **No decorators or complex annotations needed.**

**Standard Naming Patterns:**
```python
# Read-only operations (safe to call on production)
list_*()      # Returns List[Dict] - all entities of type
get_*()       # Returns Dict - single entity by ID/name
count_*()     # Returns int - count without fetching all data

# Write operations (modify production data)
create_*()    # Creates new entity
update_*()    # Modifies existing entity
delete_*()    # Removes entity

# Bulk operations
bulk_*()      # Operates on multiple entities at once
```

**Examples:**
```python
class AssetsExt:
    def list_assets(...)           # Read-only: get all assets
    def get_asset(...)             # Read-only: get one asset
    def create_asset(...)          # Write: create new asset
    def delete_asset(...)          # Write: remove asset
    def bulk_delete_assets(...)    # Write: remove multiple assets
```

**Discovery via Introspection:**
```python
# Find all read-only probe methods
from inspect import getmembers, ismethod

probe_methods = [
    name for name, _ in getmembers(AssetsExt(sdk), predicate=ismethod)
    if name.startswith(('list_', 'get_', 'count_')) and not name.startswith('_')
]
# → ['list_assets', 'get_asset']
```

### 4. Type Hints Are Mandatory

**All public methods must have complete type annotations:**
```python
# ✅ GOOD
def list_assets(
    self,
    folder_key: Optional[str] = None,
    filter_query: Optional[str] = None,
    top: Optional[int] = None
) -> List[Dict[str, Any]]:
    """List all assets in a folder."""
    ...

# ❌ BAD
def list_assets(self, folder_key=None, filter_query=None):
    ...
```

**Why:**
- IDE autocomplete and type checking
- Self-documenting API
- Prevents runtime errors
- Industry standard (boto3-stubs, google-cloud-*)

### 5. Composition Over Inheritance

**Extension classes wrap the SDK, don't inherit from it:**
```python
# ✅ GOOD: Composition
class AssetsExt:
    def __init__(self, sdk: UiPath):
        self.sdk = sdk  # Wrap, don't inherit

# ❌ BAD: Inheritance
class AssetsExt(UiPath):
    ...
```

**Why:** Inheritance tightly couples your code to SDK internals. Composition is flexible and testable.

### 6. Consistent Error Handling

**Let exceptions bubble up naturally:**
```python
# ✅ GOOD: Let API errors propagate
def list_assets(self, folder_key: str) -> List[Dict[str, Any]]:
    response = self.sdk.api_client.request("GET", "/odata/Assets", ...)
    return response.json().get("value", [])
    # If request fails, exception propagates to caller

# ❌ BAD: Swallow errors or return inconsistent types
def list_assets(self, folder_key: str) -> List[Dict[str, Any]]:
    try:
        response = self.sdk.api_client.request("GET", "/odata/Assets", ...)
        return response.json().get("value", [])
    except Exception:
        return []  # Silently fails! Caller can't distinguish empty folder from error
```

**Why:** Explicit is better than implicit. Callers should handle errors appropriate to their context.

## Library Structure

### Package Organization
```
src/uipath_sdk_extensions/
├── __init__.py          # Exports + introspection helpers
├── assets.py            # AssetsExt class
├── jobs.py              # JobsExt class
├── queues.py            # QueuesExt class
├── processes.py         # ProcessesExt class
├── schedules.py         # SchedulesExt class
├── libraries.py         # LibrariesExt class
├── tasks.py             # TasksExt class
├── folders.py           # FolderManagementExt class
├── folder_utils.py      # FolderUtils class
├── context_grounding.py # ContextGroundingExt class
└── buckets.py           # BucketExtensions class
```

### __init__.py Pattern
```python
"""UiPath SDK Extensions - Production-ready extensions for the UiPath Python SDK."""

from .assets import AssetsExt
from .jobs import JobsExt
# ... all exports

__version__ = "0.0.5"

__all__ = [
    "AssetsExt",
    "JobsExt",
    # ... all classes
]

# Introspection helpers
def get_all_extensions() -> List[Type]:
    """Return all extension classes for introspection.

    Used by probe scripts and discovery tools.
    """
    return [
        AssetsExt,
        JobsExt,
        QueuesExt,
        # ...
    ]

def get_extension_metadata() -> Dict[str, Dict[str, str]]:
    """Return metadata about each extension.

    Returns:
        Dict mapping class name to entity type and endpoint.
    """
    return {
        "AssetsExt": {"entity": "Asset", "endpoint": "/odata/Assets"},
        "JobsExt": {"entity": "Job", "endpoint": "/odata/Jobs"},
        # ...
    }
```

## Extension Class Template

```python
"""[Entity] management operations.

Provides [operations] that extend the official SDK's [existing capabilities].
"""

from typing import Dict, Any, List, Optional
from uipath import UiPath


class [Entity]Ext:
    """Extensions for [Entity] operations.

    The official SDK provides [what SDK has], but is missing:
    - [Gap 1]
    - [Gap 2]
    - [Gap 3]

    This extension fills those gaps using the OData endpoints.
    """

    def __init__(self, sdk: UiPath):
        """Initialize with UiPath SDK instance.

        Args:
            sdk: Authenticated UiPath SDK instance
        """
        self.sdk = sdk

    def list_[entities](
        self,
        folder_key: Optional[str] = None,
        filter_query: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        order_by: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all [entities] in a folder with optional filtering.

        Args:
            folder_key: Folder GUID (optional - uses current folder if not specified)
            filter_query: OData $filter query (e.g., "Name eq 'MyEntity'")
            top: Maximum number of results to return
            skip: Number of results to skip (for pagination)
            order_by: OData $orderby query (e.g., "CreatedTime desc")

        Returns:
            List of [entity] dictionaries with [key fields]

        Raises:
            Exception: If API request fails

        Example:
            >>> ext = [Entity]Ext(sdk)
            >>> entities = ext.list_[entities](folder_key="5ebb73c3-...")
            >>> for entity in entities:
            ...     print(f"{entity['Name']}: {entity['Status']}")
        """
        params = {}
        if filter_query:
            params["$filter"] = filter_query
        if top:
            params["$top"] = top
        if skip:
            params["$skip"] = skip
        if order_by:
            params["$orderby"] = order_by

        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        response = self.sdk.api_client.request(
            "GET",
            "/odata/[Entities]",
            params=params,
            headers=headers
        )

        return response.json().get("value", [])
```

## Testing Approach

**Don't hit live APIs in unit tests:**
```python
# ✅ GOOD: Mock HTTP responses
from unittest.mock import Mock, MagicMock

def test_list_assets():
    mock_sdk = Mock()
    mock_sdk.api_client.request.return_value.json.return_value = {
        "value": [{"Name": "TestAsset", "ValueType": "Text"}]
    }

    assets_ext = AssetsExt(mock_sdk)
    result = assets_ext.list_assets(folder_key="test-key")

    assert len(result) == 1
    assert result[0]["Name"] == "TestAsset"

# ❌ BAD: Hit live API
def test_list_assets():
    sdk = UiPath()  # Makes real network call!
    assets = AssetsExt(sdk).list_assets()
```

**Probe scripts are for live API exploration:**
- Unit tests: Mocked, fast, offline
- Probe scripts: Live API, read-only, discovery

## Introspection and Discovery

**Library provides simple introspection helpers:**

```python
# In consuming code (probe scripts)
from uipath import UiPath
from uipath_sdk_extensions import get_all_extensions
from inspect import getmembers, ismethod

sdk = UiPath()

for ext_class in get_all_extensions():
    print(f"\n{ext_class.__name__}")
    ext = ext_class(sdk)

    # Find all read-only methods
    read_methods = [
        name for name, _ in getmembers(ext, predicate=ismethod)
        if name.startswith(('list_', 'get_')) and not name.startswith('_')
    ]

    print(f"  Read-only methods: {', '.join(read_methods)}")
```

**Output:**
```
AssetsExt
  Read-only methods: list_assets, get_asset

JobsExt
  Read-only methods: list_jobs, get_job, list_jobs_by_state
...
```

## Documentation Standards

### Docstrings
- All public classes and methods must have docstrings
- Use Google-style docstring format
- Include Args, Returns, Raises, Example sections
- Link to Orchestrator API docs where applicable

### Examples in Docstrings
```python
def list_assets(self, folder_key: str) -> List[Dict[str, Any]]:
    """List all assets in a folder.

    Args:
        folder_key: Folder GUID

    Returns:
        List of asset dictionaries with Name, ValueType, Value, etc.

    Example:
        >>> assets = AssetsExt(sdk)
        >>> all_assets = assets.list_assets(folder_key="5ebb73c3-...")
        >>> for asset in all_assets:
        ...     print(f"{asset['Name']}: {asset['ValueType']}")
        APIKey: Text
        DatabasePassword: Credential
    """
```

## Version Management

**Semantic Versioning:**
- `0.0.x` - Alpha, breaking changes expected
- `0.x.0` - Beta, API stabilizing
- `1.0.0` - Stable, backwards compatibility guaranteed

**Current State (v0.0.5):**
- All is in flux
- Breaking changes permitted
- Focus on maturing the API surface

## References

**Patterns studied:**
- AWS boto3 / boto3-extensions
- Google Cloud Python SDK
- Stripe Python SDK
- Requests library

**Key resources:**
- [Designing Pythonic library APIs](https://benhoyt.com/writings/python-api-design/)
- [Python API Client Design Patterns](https://bhomnick.net/design-pattern-python-api-client/)
- [Building API Wrappers in Python](https://semaphore.io/community/tutorials/building-and-testing-an-api-wrapper-in-python)
- [boto3-extensions on PyPI](https://pypi.org/project/boto3-extensions/)

---

**Last Updated:** 2025-10-27
**Version:** 0.0.5 (Alpha)
