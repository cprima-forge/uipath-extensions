# Working with AI Coding Agents

> Guide for contributors using Claude Code, GitHub Copilot, or other AI coding assistants

## Quick Context for AI Agents

When working on this codebase, provide these key facts to your AI assistant:

### Project Overview
- **Package:** `cprima-forge-uipath-extensions`
- **Import:** `from cpmf.uipath_ext import <ClassName>`
- **Version:** 0.0.5 (alpha - breaking changes permitted)
- **Purpose:** Production SDK extension that fills ~85% of API gaps in official UiPath Python SDK
- **License:** CC-BY-4.0

### Architecture
- **Pattern:** Composition over inheritance - each extension wraps UiPath SDK
- **Structure:** One class per entity type (AssetsExt, JobsExt, etc.)
- **Returns:** Raw dictionaries/lists - no presentation logic in library
- **Naming:** Method prefixes are metadata (`list_*`, `get_*`, `create_*`, `delete_*`)

### 11 Extension Classes
1. `FolderUtils` - Folder ID/Key conversion
2. `FolderManagementExt` - Folder CRUD operations
3. `AssetsExt` - Asset management
4. `JobsExt` - Job operations
5. `QueuesExt` - Queue definitions
6. `ProcessesExt` - Process/release management
7. `SchedulesExt` - Process schedules
8. `LibrariesExt` - Library packages
9. `TasksExt` - Human-in-the-loop tasks
10. `ContextGroundingExt` - Context Grounding storage
11. `BucketExtensions` - Storage buckets

### Key Files
- `src/cpmf/uipath_ext/__init__.py` - Main exports + introspection helpers
- `src/cpmf/uipath_ext/{entity}.py` - Individual extension classes
- `docs/contributors/lib-best-practices.md` - Design principles
- `docs/users/API_REFERENCE.md` - Auto-generated method reference

### Code Style
- **Type hints:** Mandatory for all public methods
- **Docstrings:** Google-style with Args/Returns/Example
- **Errors:** Let exceptions bubble (don't swallow)
- **Testing:** Mock HTTP responses, never hit live APIs in unit tests
- **No emoji:** Windows cp1252 compatibility required

### Common Tasks

#### Adding a New Method
```python
def list_entities(
    self,
    folder_key: Optional[str] = None,
    filter_query: Optional[str] = None,
    top: Optional[int] = None
) -> List[Dict[str, Any]]:
    """List all entities in a folder.

    Args:
        folder_key: Folder GUID
        filter_query: OData $filter query
        top: Max results to return

    Returns:
        List of entity dictionaries

    Example:
        >>> ext = EntitiesExt(sdk)
        >>> items = ext.list_entities(folder_key="5ebb73...")
    """
    params = {}
    if filter_query:
        params["$filter"] = filter_query
    if top:
        params["$top"] = top

    headers = {}
    if folder_key:
        headers["x-uipath-folderkey"] = folder_key

    response = self.sdk.api_client.request(
        "GET",
        "/odata/Entities",
        params=params,
        headers=headers
    )
    return response.json().get("value", [])
```

#### Installation

```bash
# Install from MyGet feed (alpha releases)
uv pip install cprima-forge-uipath-extensions \
  --extra-index-url https://www.myget.org/F/cprima-forge/python/ \
  --index-strategy unsafe-best-match

# Or with pip:
pip install cprima-forge-uipath-extensions \
  --extra-index-url https://www.myget.org/F/cprima-forge/python/

# Install in editable mode (for development)
uv pip install -e .
```

#### Running Tests
```bash
# Run tests
pytest tests/

# Type check
mypy src/

# Lint
ruff check src/
```

#### Building
```bash
# Build wheel
uv build --wheel

# Test locally
uv pip install dist/cprima_forge_uipath_extensions-0.0.5-py3-none-any.whl
```

### API Documentation
- Official SDK: https://uipath.github.io/uipath-python/
- Orchestrator API: https://docs.uipath.com/orchestrator/reference
- OData: Use `/odata/` endpoints for CRUD operations

### Integration Points
- **Coded Agents Repo:** This library is used via git submodule in `rpapub/coded-agents`
- **Probe Scripts:** `tools/probes/uipath-sdk/` for live API testing
- **Import Path:** Changed from `uipath_sdk_extensions` to `cpmf.uipath_ext` in migration

### Constraints
- **Python:** >=3.11 (matches UiPath LangChain SDK requirement)
- **Dependencies:** Minimal - only `uipath>=2.1.111`
- **Trademark:** Namespace is `cpmf.uipath_ext` to avoid UiPath trademark issues
- **Windows:** No Unicode/emoji in any print statements or error messages

### Workflow for AI-Assisted Development

1. **Read `lib-best-practices.md` first** - understand design philosophy
2. **Check existing patterns** - find similar method in another extension class
3. **Follow naming conventions** - `list_*/get_*/create_*/delete_*` prefixes
4. **Add type hints** - all parameters and return types
5. **Write docstring** - include Example section
6. **Update `__init__.py`** - export new methods if adding to existing class
7. **Run linter** - `ruff check` before committing
8. **Test manually** - use probe scripts with live Orchestrator

### Helpful Agent Prompts

When asking your AI assistant for help:

```
"Add a method to JobsExt to filter jobs by state using OData $filter.
Follow the patterns in lib-best-practices.md. Include type hints and
docstring with example."
```

```
"Review this method signature for consistency with other methods in
AssetsExt. Check naming, type hints, and parameter order."
```

```
"Generate unit test mocks for this method that tests both success
and error cases. Don't hit live APIs."
```

### Version Management
- **Current:** 0.0.5 (develop branch)
- **Breaking changes:** Permitted in 0.0.x versions
- **Semver:** Will follow once reaching 1.0.0

### Getting Help
- GitHub Issues: https://github.com/cprima-forge/uipath-extensions/issues
- Read existing code in `src/cpmf/uipath_ext/` for patterns
- Check `docs/contributors/` for detailed guides

---

**Last Updated:** 2025-10-28 (v0.0.5)
