# v0.0.5 - First Standalone Release

**Production-ready extensions for the UiPath Python SDK**

This is the first standalone alpha release of **cprima-forge-uipath-extensions**, migrated from the `rpapub/coded-agents` monorepo. Provides 11 extension classes covering ~85% of the API gaps in the official UiPath Python SDK.

## 📦 Installation

```bash
pip install cprima-forge-uipath-extensions \
  --extra-index-url https://www.myget.org/F/cprima-forge/python/
```

## ✨ What's New

### 🚀 Standalone Repository
- **New namespace:** `from cpmf.uipath_ext import AssetsExt, JobsExt`
- **New package name:** `cprima-forge-uipath-extensions`
- **Python >=3.11 required** (for UiPath LangChain SDK compatibility)

### 📚 11 Extension Classes (6,096 lines of code)

1. **FolderUtils** - Folder ID/Key conversion with caching
2. **FolderManagementExt** - Complete folder CRUD operations
3. **AssetsExt** - Asset management and cross-folder sharing
4. **JobsExt** - Job operations, bulk actions, and statistics
5. **QueuesExt** - Queue definitions and retention policies
6. **ProcessesExt** - Process/release version management
7. **SchedulesExt** - Time-based trigger management
8. **LibrariesExt** - Reusable package operations
9. **TasksExt** - Human-in-the-loop workflows
10. **ContextGroundingExt** - Storage inspection
11. **BucketExtensions** - Storage bucket operations

### 📖 Documentation Restructure

- **README:** Streamlined from 505 → 92 lines
- **API Reference:** Complete method signatures for all 11 classes
- **AI Agent Guide:** Development guide for Claude Code, Copilot, etc.
- **Best Practices:** Design patterns and conventions
- **Contributing:** Fork/submodule workflow and 4 ways to contribute

### 🌿 Git Flow Branch Strategy

- **`develop`** - Active development branch
- **`main`** - Reserved for stable releases (no direct development)
- Alpha releases tagged directly on `develop`

## 📊 Quick Stats

- **23 files changed:** 6,096 insertions, 32 deletions
- **Wheel size:** 40 KB
- **API coverage:** ~85% of missing Orchestrator API surface
- **Type hints:** Complete coverage for all public methods

## 🔧 Technical Details

**Requirements:**
- Python >=3.11
- uipath >=2.1.111

**License:** CC-BY-4.0

**Branch:** `develop` (active development)

## 🤝 Contributing

**This is fast-moving, community-driven code.** Contributions welcome!

- **[Open a PR](https://github.com/cprima-forge/uipath-extensions/pulls)**
- **[Submit an Issue](https://github.com/cprima-forge/uipath-extensions/issues/new)**
- **Fork & Use as Submodule:**
  ```bash
  git submodule add -b develop \
    https://github.com/YOUR_USERNAME/uipath-extensions \
    libs/uipath-extensions
  ```

See [AGENTS.md](docs/contributors/AGENTS.md) for development setup.

## 📝 Migration Guide

### Update Imports

```python
# OLD (monorepo)
from uipath_sdk_extensions import AssetsExt, JobsExt

# NEW (standalone)
from cpmf.uipath_ext import AssetsExt, JobsExt
```

### Update Installation

```bash
# Install from MyGet
pip install cprima-forge-uipath-extensions \
  --extra-index-url https://www.myget.org/F/cprima-forge/python/
```

## 📋 Full Changelog

### Features
- **feat: migrate extension library from coded-agents repo** (7d1b39e)
  - Add all 11 extension modules
  - Refactor namespace: `uipath_sdk_extensions` → `cpmf.uipath_ext`

### Documentation
- **docs: restructure for v0.0.5 standalone library** (edfb16a)
  - Create docs/users/ and docs/contributors/ folders
  - Generate API_REFERENCE.md (232 lines)
  - Create AGENTS.md guide (187 lines)
- **docs: streamline README** (89a3140)
  - Reduce from 505 → 92 lines
  - Add MyGet installation instructions
- **docs: add fork/submodule instructions** (d290f08)
  - Prominent CTA for contributions
  - Step-by-step contribution workflow
- **docs: remove first/second person language** (c89984a)
  - Neutral, third-person voice
- **docs: update branch references to develop** (2849ee6)

### Fixes
- **fix: update goreleaser config to version 2** (4121d29, ea35d51)

### Refactoring
- **refactor: move generate_api_ref.py to tools/** (ede811f)

## ⚠️ Known Limitations

- **Alpha release:** Breaking changes permitted in 0.0.x versions
- **MyGet only:** Not yet on PyPI (pending account unlock)
- **Windows cp1252:** All emoji removed for console compatibility

## 🎯 What's Next (v0.0.6+)

- Unit tests for all extension classes
- Async method variants
- Expanded Context Grounding capabilities
- Improved error messages and retry strategies
- PyPI publication

---

**Independent Community Project** - Not affiliated with or endorsed by UiPath, Inc.

**Full Release Notes:** [RELEASE_NOTES_v0.0.5.md](RELEASE_NOTES_v0.0.5.md)
