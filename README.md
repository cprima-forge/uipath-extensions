# cprima-forge-uipath-extensions

**Production-ready extensions for the UiPath Python SDK**

Version: **0.0.5** (Alpha) | **[Open a PR](https://github.com/cprima-forge/uipath-extensions/pulls)** | **[Submit Ideas](https://github.com/cprima-forge/uipath-extensions/issues/new)**

## Overview

Community-built extensions that fill ~85% of the API gaps in the official UiPath Python SDK. Provides 11 extension classes covering assets, jobs, queues, processes, schedules, libraries, tasks, folders, and storage operations.

**This is fast-moving code in active development.** Contributions, bug reports, and feature requests are welcome.

- **Package:** `cprima-forge-uipath-extensions`
- **Import:** `from cpmf.uipath_ext import <ClassName>`
- **License:** CC-BY-4.0
- **Python:** >=3.11
- **Dependencies:** `uipath>=2.1.111`

## Installation

### Option 1: Install from MyGet (Alpha Releases)

```bash
# With pip:
pip install cprima-forge-uipath-extensions \
  --extra-index-url https://www.myget.org/F/cprima-forge/python/

# Or with uv:
uv pip install cprima-forge-uipath-extensions \
  --extra-index-url https://www.myget.org/F/cprima-forge/python/ \
  --index-strategy unsafe-best-match
```

### Option 2: Fork and Use as Submodule (Recommended for Development)

Recommended approach for contributing or staying on the cutting edge:

```bash
# 1. Fork this repository on GitHub
#    Go to: https://github.com/cprima-forge/uipath-extensions
#    Click "Fork"

# 2. Add the fork as a submodule in a project
git submodule add -b develop \
  https://github.com/YOUR_USERNAME/uipath-extensions \
  libs/uipath-extensions

# 3. Install in editable mode
cd libs/uipath-extensions
uv pip install -e .

# 4. After making improvements, open a PR
git checkout -b feature/my-improvement
# ... make changes ...
git commit -am "feat: add awesome feature"
git push origin feature/my-improvement
# Open PR at: https://github.com/cprima-forge/uipath-extensions/compare
```

## Quick Start

```python
from uipath import UiPath
from cpmf.uipath_ext import AssetsExt, JobsExt, FolderUtils

sdk = UiPath()

# List assets
assets = AssetsExt(sdk)
asset_list = assets.list_assets(folder_key="5ebb73c3-...")

# Get job statistics
jobs = JobsExt(sdk)
stats = jobs.get_job_statistics(
    folder_key="5ebb73c3-...",
    process_name="OrderProcessing"
)

# Convert folder key to ID
utils = FolderUtils(sdk)
folder_id = utils.get_folder_id_from_key("5ebb73c3-...")
```

## 11 Extension Classes

1. **FolderUtils** - Folder ID/Key conversion
2. **FolderManagementExt** - Folder CRUD operations
3. **AssetsExt** - Asset management
4. **JobsExt** - Job operations
5. **QueuesExt** - Queue definitions
6. **ProcessesExt** - Process/release management
7. **SchedulesExt** - Schedule management
8. **LibrariesExt** - Library packages
9. **TasksExt** - Human-in-the-loop tasks
10. **ContextGroundingExt** - Context Grounding storage
11. **BucketExtensions** - Storage buckets

## Documentation

- **[API Reference](docs/users/API_REFERENCE.md)** - Complete method signatures and endpoints
- **[AI Agent Guide](docs/contributors/AGENTS.md)** - Guide for AI coding assistants
- **[Best Practices](docs/contributors/lib-best-practices.md)** - Design patterns

## Design Principles

- **Composition over Inheritance** - Wraps UiPath SDK, doesn't replace it
- **Type-Safe** - Full type hints for all public methods
- **Minimal Dependencies** - Only requires `uipath>=2.1.111`
- **Return Raw Data** - Methods return dictionaries/lists
- **Clear Naming** - Method prefixes indicate operation (`list_*`, `get_*`, `create_*`, `delete_*`)

## Contributing

This library is community-driven and benefits from real-world usage feedback.

### Ways to Contribute

1. **Open a Pull Request** - Add methods, fix bugs, improve docs
   - [View open PRs](https://github.com/cprima-forge/uipath-extensions/pulls)
   - [Create new PR](https://github.com/cprima-forge/uipath-extensions/compare)

2. **Submit Issues** - Report bugs, request features, share ideas
   - [View open issues](https://github.com/cprima-forge/uipath-extensions/issues)
   - [Create new issue](https://github.com/cprima-forge/uipath-extensions/issues/new)

3. **Test and Provide Feedback** - Use the library, report what works (or doesn't)

4. **Improve Documentation** - Examples, guides, API clarifications

See [docs/contributors/AGENTS.md](docs/contributors/AGENTS.md) for development setup and contribution guidelines.

## Links

- **GitHub:** https://github.com/cprima-forge/uipath-extensions
- **Official UiPath SDK:** https://github.com/UiPath/uipath-python
- **Orchestrator API:** https://docs.uipath.com/orchestrator/reference

---

**Independent Community Project** - Not affiliated with or endorsed by UiPath, Inc.
