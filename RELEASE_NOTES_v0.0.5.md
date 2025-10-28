# Release Notes: v0.0.5

**Release Date:** 2025-10-28
**Release Type:** Alpha
**Branch:** `develop`

## 🎉 Overview

This is the first standalone release of **cprima-forge-uipath-extensions**, migrated from the `rpapub/coded-agents` monorepo. This library provides production-ready extensions that fill ~85% of the API gaps in the official UiPath Python SDK.

## 📦 Installation

```bash
# Install from MyGet feed (alpha releases)
pip install cprima-forge-uipath-extensions \
  --extra-index-url https://www.myget.org/F/cprima-forge/python/
```

## ✨ What's Included

### 11 Extension Classes

This release includes **6,096 lines of code** across 11 extension modules:

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

## 🚀 Major Changes

### Migration to Standalone Repository

**Before (Monorepo):**
```python
from uipath_sdk_extensions import AssetsExt, JobsExt
```

**After (Standalone):**
```python
from cpmf.uipath_ext import AssetsExt, JobsExt
```

**Changes:**
- ✅ Migrated from `rpapub/coded-agents` monorepo
- ✅ New namespace: `uipath_sdk_extensions` → `cpmf.uipath_ext`
- ✅ New package name: `cprima-forge-uipath-extensions`
- ✅ Trademark-safe namespace (`cpmf` prefix)
- ✅ Version bump: 0.0.4 → 0.0.5

### Documentation Restructure

**New Documentation Structure:**
```
docs/
├── users/
│   └── API_REFERENCE.md       # Complete method signatures (232 lines)
└── contributors/
    ├── AGENTS.md              # AI coding assistant guide (187 lines)
    ├── lib-best-practices.md  # Design patterns (424 lines)
    ├── PLAN.md                # Development roadmap (473 lines)
    └── ALPHA_TESTING.md       # Testing guidelines (389 lines)
```

**README Improvements:**
- ✅ Streamlined from 505 lines to 92 lines (82% reduction)
- ✅ Added MyGet installation instructions
- ✅ Added fork/submodule workflow for contributors
- ✅ Prominent call-to-action for contributions
- ✅ Removed first/second person language (neutral voice)

### Branch Strategy

**New Git Flow Model:**
```
main (releases only, protected)
  └── develop (active development)
      └── feature/* (optional feature branches)
```

- ✅ `develop` branch for all active development
- ✅ `main` branch reserved for stable releases
- ✅ Tags created directly on `develop` for alpha releases
- ✅ Previous `alpha/initial-migration` branch retired

## 📝 Detailed Changelog

### Features

#### Migration & Infrastructure
- **feat: migrate extension library from coded-agents repo** (7d1b39e)
  - Add all 11 extension modules
  - Refactor namespace: `uipath_sdk_extensions` → `cpmf.uipath_ext`
  - Update version 0.0.1 → 0.0.5
  - Migrate documentation and examples

### Documentation

#### Restructure & Organization
- **docs: restructure for v0.0.5 standalone library** (edfb16a)
  - Create `docs/users/` and `docs/contributors/` folders
  - Move contributor documentation to dedicated folder
  - Generate `API_REFERENCE.md` for LLM consumption
  - Create `AGENTS.md` guide for AI coding assistants
  - Remove outdated docs (ORIGINAL_README, RfC)
  - Update all version references (0.0.2/0.0.4 → 0.0.5)

#### README Improvements
- **docs: streamline README for v0.0.5** (89a3140)
  - Remove redundant content now in docs/ folder
  - Add MyGet installation instructions
  - Update Python requirement to >=3.11
  - Reduce from 505 lines to 92 lines

- **docs: add fork/submodule instructions and prominent CTA** (d290f08)
  - Add prominent links to open PRs and submit issues
  - Add "Option 2" installation for fork + submodule workflow
  - Add dedicated "Contributing" section with 4 ways to contribute
  - Include step-by-step fork and PR instructions

- **docs: remove first and second person language** (c89984a)
  - Maintain neutral, third-person voice throughout
  - Replace "we" with passive constructions
  - Professional tone for solo developer project

- **docs: update branch references to develop** (2849ee6)
  - Update submodule instructions (alpha/initial-migration → develop)
  - Update version references in AGENTS.md

### Refactoring

- **refactor: move generate_api_ref.py to tools folder** (ede811f)
  - Consolidate development scripts in `tools/` directory
  - Better organization for maintenance scripts

### Fixes

- **fix: update goreleaser config to version 2 format** (4121d29)
  - Add required `version: 2` field for modern GoReleaser

- **fix: update goreleaser config for v2 format** (ea35d51)
  - Remove deprecated `extra_files` field
  - Include Python wheels directly in `archives.files` array

## 📊 Statistics

**Code Changes:**
- **23 files changed**
- **6,096 insertions**
- **32 deletions**

**File Breakdown:**
- Python source: 11 extension modules (3,787 lines)
- Documentation: 4 contributor guides (1,473 lines)
- API reference: Auto-generated (232 lines)
- Tools: 1 generator script (98 lines)

## 🔧 Technical Details

### Requirements

- **Python:** >=3.11 (required by UiPath LangChain SDK)
- **Dependencies:** `uipath>=2.1.111`

### Package Details

- **Package Name:** `cprima-forge-uipath-extensions`
- **Import Namespace:** `cpmf.uipath_ext`
- **License:** CC-BY-4.0
- **Wheel Size:** 40 KB

### API Coverage

This library covers ~85% of the Orchestrator API surface missing from the official SDK:

| Category | Coverage |
|----------|----------|
| Asset Management | ✅ Complete |
| Job Operations | ✅ Complete |
| Queue Definitions | ✅ Complete |
| Process/Release Management | ✅ Complete |
| Schedule Management | ✅ Complete |
| Library Operations | ✅ Complete |
| Task Workflows | ✅ Complete |
| Folder Management | ✅ Complete |
| Context Grounding | ✅ Storage inspection |
| Storage Buckets | ✅ File operations |

## 🤝 Contributing

This is a **fast-moving, community-driven project**. Contributions are welcome!

### Ways to Contribute

1. **Open a Pull Request** - Add methods, fix bugs, improve docs
   - [View open PRs](https://github.com/cprima-forge/uipath-extensions/pulls)
   - [Create new PR](https://github.com/cprima-forge/uipath-extensions/compare)

2. **Submit Issues** - Report bugs, request features, share ideas
   - [View open issues](https://github.com/cprima-forge/uipath-extensions/issues)
   - [Create new issue](https://github.com/cprima-forge/uipath-extensions/issues/new)

3. **Fork & Use as Submodule**
   ```bash
   git submodule add -b develop \
     https://github.com/YOUR_USERNAME/uipath-extensions \
     libs/uipath-extensions
   ```

See [docs/contributors/AGENTS.md](docs/contributors/AGENTS.md) for development setup.

## 🔗 Links

- **GitHub:** https://github.com/cprima-forge/uipath-extensions
- **MyGet Feed:** https://www.myget.org/F/cprima-forge/python/
- **Official UiPath SDK:** https://github.com/UiPath/uipath-python
- **Orchestrator API Docs:** https://docs.uipath.com/orchestrator/reference

## 📋 Migration Guide

If migrating from the monorepo version:

### Update Imports

```python
# OLD (monorepo)
from uipath_sdk_extensions import (
    AssetsExt,
    JobsExt,
    FolderUtils
)

# NEW (standalone)
from cpmf.uipath_ext import (
    AssetsExt,
    JobsExt,
    FolderUtils
)
```

### Update Installation

```bash
# OLD (editable install from monorepo)
cd libs/uipath-sdk-extensions
pip install -e .

# NEW (install from MyGet)
pip install cprima-forge-uipath-extensions \
  --extra-index-url https://www.myget.org/F/cprima-forge/python/

# OR (fork as submodule)
git submodule add -b develop \
  https://github.com/YOUR_USERNAME/uipath-extensions \
  libs/uipath-extensions
cd libs/uipath-extensions
pip install -e .
```

## ⚠️ Known Limitations

- **Alpha Release:** Breaking changes permitted in 0.0.x versions
- **MyGet Only:** Not yet published to PyPI (pending account verification)
- **Windows cp1252:** All emoji/Unicode removed for console compatibility
- **No Async:** All methods are synchronous (async variants planned)

## 🎯 Next Steps (v0.0.6+)

- Add unit tests for all extension classes
- Add async method variants
- Expand Context Grounding capabilities
- Add telemetry management utilities
- Improve error messages
- Add retry strategies for transient failures
- Publish to PyPI (when account unlocked)

---

**Independent Community Project** - Not affiliated with or endorsed by UiPath, Inc.

**Generated with:** Claude Code (https://claude.com/claude-code)
