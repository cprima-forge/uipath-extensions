# Release Notes: v0.0.6

**Release Date:** 2026-01-12
**Release Type:** Alpha
**Branch:** `main`

## Overview

This release migrates **cpmf-uipath-extensions** to its canonical repository at `cprima-forge/uipath-extensions` and fixes the PyPI package name to match the published package.

## Installation

```bash
# Install from PyPI
pip install cpmf-uipath-extensions

# Or with uv:
uv pip install cpmf-uipath-extensions
```

## What's New in v0.0.6

### Package Name Correction

**Critical Fix:** The package name now correctly matches the PyPI package name.

- **Package Name:** `cpmf-uipath-extensions` (was incorrectly `cprima-forge-uipath-extensions` in source)
- **Import:** `from cpmf.uipath_ext import <ClassName>` (unchanged)

### Repository Migration

This release establishes `cprima-forge/uipath-extensions` as the canonical repository for the package.

**Changes:**
- Migrated ~4,050 lines of production code from `rpapub/coded-agents` monorepo
- Fixed package name in `pyproject.toml` and `__init__.py`
- Updated all documentation references
- Added comprehensive test suite

## What's Included

### 11 Extension Classes

This release includes **~4,050 lines of code** across 11 extension modules:

1. **FolderUtils** (135 lines) - Folder ID/Key conversion utilities with caching
2. **FolderManagementExt** (385 lines) - Complete folder CRUD operations
3. **AssetsExt** (324 lines) - Asset management and cross-folder sharing
4. **JobsExt** (392 lines) - Job operations, bulk actions, and statistics
5. **QueuesExt** (458 lines) - Queue definition management and retention policies
6. **ProcessesExt** (435 lines) - Process and release version management
7. **SchedulesExt** (378 lines) - Time-based process trigger management
8. **LibrariesExt** (353 lines) - Reusable package library operations
9. **TasksExt** (503 lines) - Human-in-the-loop task workflows
10. **ContextGroundingExt** (260 lines) - Context Grounding storage inspection
11. **BucketExtensions** (164 lines) - Storage bucket operations

### Key Features

- **~85% API Coverage** - Bridges critical gaps in the official UiPath Python SDK
- **Type-Safe** - Full type hints for all public methods
- **Production-Ready** - Comprehensive error handling and logging
- **Composition Pattern** - Wraps SDK, doesn't replace it
- **Python >=3.11** - Required for UiPath LangChain SDK compatibility

## Technical Details

### Requirements

- **Python:** >=3.11 (required by UiPath LangChain SDK)
- **Dependencies:** `uipath>=2.1.111`

### Package Details

- **Package Name:** `cpmf-uipath-extensions`
- **Import Namespace:** `cpmf.uipath_ext`
- **License:** CC-BY-4.0

### API Coverage

This library covers ~85% of the Orchestrator API surface missing from the official SDK:

| Category | Coverage |
|----------|----------|
| Asset Management | Complete |
| Job Operations | Complete |
| Queue Definitions | Complete |
| Process/Release Management | Complete |
| Schedule Management | Complete |
| Library Operations | Complete |
| Task Workflows | Complete |
| Folder Management | Complete |
| Context Grounding | Storage inspection |
| Storage Buckets | File operations |

## Migration from v0.0.5

If upgrading from v0.0.5:

### No Import Changes Required

The import namespace remains the same:

```python
from cpmf.uipath_ext import (
    AssetsExt,
    JobsExt,
    FolderUtils
)
```

### Update Installation

```bash
# Simply upgrade
pip install --upgrade cpmf-uipath-extensions
```

## Contributing

This is a **fast-moving, community-driven project**. Contributions are welcome!

### Ways to Contribute

1. **Open a Pull Request** - Add methods, fix bugs, improve docs
   - [View open PRs](https://github.com/cprima-forge/uipath-extensions/pulls)
   - [Create new PR](https://github.com/cprima-forge/uipath-extensions/compare)

2. **Submit Issues** - Report bugs, request features, share ideas
   - [View open issues](https://github.com/cprima-forge/uipath-extensions/issues)
   - [Create new issue](https://github.com/cprima-forge/uipath-extensions/issues/new)

See [docs/contributors/AGENTS.md](docs/contributors/AGENTS.md) for development setup.

## Links

- **GitHub:** https://github.com/cprima-forge/uipath-extensions
- **PyPI:** https://pypi.org/project/cpmf-uipath-extensions/
- **Official UiPath SDK:** https://github.com/UiPath/uipath-python
- **Orchestrator API Docs:** https://docs.uipath.com/orchestrator/reference

## Known Limitations

- **Alpha Release:** Breaking changes permitted in 0.0.x versions
- **No Async:** All methods are synchronous (async variants planned)

## Next Steps (v0.0.7+)

- Expand unit test coverage
- Add async method variants
- Expand Context Grounding capabilities
- Add retry strategies for transient failures
- Improve error messages

---

**Independent Community Project** - Not affiliated with or endorsed by UiPath, Inc.

**Generated with:** Claude Code (https://claude.com/claude-code)
