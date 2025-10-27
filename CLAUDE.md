# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Community-built extensions and utilities for the UiPath Python SDK. This is an independent, community-maintained project under the **cprima-forge** initiative, exploring advanced automation patterns and SDK integrations for the UiPath ecosystem.

**Key Information:**
- Python 3.11+ required
- PowerShell Core 7+ required (Windows cross-platform)
- License: CC-BY 4.0 (documentation and materials)
- Planned PyPI package: `cprima-forge-uipath-extensions`
- Planned import namespace: `cpmf.uipath_ext`
- Independent project, not affiliated with or endorsed by UiPath

## Repository Structure

This is a **hybrid documentation/code repository**:

1. **Documentation Site**: `docs/` contains a static HTML site hosted on GitHub Pages
2. **RFC Submodule**: `docs/rfc-gist/` is a Git submodule linking to a Gist containing the RFC
3. **Python Package**: Source code will be added in upcoming commits (currently in initial setup phase)
4. **Release Artifacts**: Uses GoReleaser for creating release archives (primarily for documentation distribution)

## Common Commands

### Development (using uv)

```bash
# Install package in development mode
make install-dev

# Run tests
make test

# Run tests with coverage
make test-cov

# Lint code
make lint

# Lint and auto-fix issues
make lint-fix

# Build package
make build

# Clean build artifacts
make clean
```

### RFC Management

The RFC is maintained as a Git submodule pointing to a GitHub Gist:

```bash
# Update RFC content and push changes
make update-rfc
```

**IMPORTANT**: The Makefile's `update-rfc` target uses `git push --force-with-lease` for the submodule. This is acceptable because it operates on the isolated `docs/rfc-gist` submodule, not the main repository. Never use force push on the main repository.

### Documentation Cleanup

```bash
# Remove standalone markdown separators (---) from all .md files
python ./tools/clean-md-separators.py
```

### Release Management

**Check version:**
```bash
make version
```

**Create git tag (if version changed):**
```bash
# Dry-run (shows what would happen)
make release-dry-run

# Create tag locally
make release

# Create tag + GitHub release via GoReleaser
make release-github
```

**Publish packages:**
```bash
# Dry-run (shows what would be published)
make publish-dry-run

# Publish to MyGet.org developer feed
make publish-myget

# Publish to PyPI
make publish-pypi

# Publish to TestPyPI (for testing)
make publish-testpypi
```

**How it works:**
- The `make release` command intelligently compares `pyproject.toml` version with latest git tag
- Only creates a new tag if the version has changed (idempotent)
- GoReleaser builds Python packages (`uv build`) and attaches them to GitHub releases
- Publishing is separate from tagging/releasing (publish after verifying the release)
- Uses `tools/release.sh` for tagging and `tools/publish.sh` for package publishing

## Development Notes

### Version Management

This project uses **single-source versioning** with `pyproject.toml` as the authoritative source:

**Version locations:**
- `pyproject.toml` (line 3) - **SINGLE SOURCE OF TRUTH** - manually update here for releases
- `src/cpmf/uipath_ext/__init__.py` - reads dynamically from package metadata via `importlib.metadata`
- Git tags - used by GoReleaser for releases (e.g., `v0.1.0`)

**Complete release workflow:**
1. Update version in `pyproject.toml` (e.g., `0.0.1` → `0.1.0`)
2. Commit changes: `git commit -am "Bump version to 0.1.0"`
3. Run: `make release-github` - creates tag and GitHub release with built packages
4. Push with tags: `git push origin main --tags`
5. Publish to MyGet: `make publish-myget` (requires `MYGET_FEED_URL` and `MYGET_API_KEY` env vars)
6. Publish to PyPI: `make publish-pypi` (when account is unlocked)

**Quick workflow (tag only, no GitHub release):**
1. Update version in `pyproject.toml`
2. Commit changes: `git commit -am "Bump version to 0.1.0"`
3. Run: `make release` - creates tag locally
4. Push: `git push origin main --tags`

**Publishing requirements:**
- **MyGet**: Set environment variables (PowerShell):
  ```powershell
  $env:MYGET_FEED_URL = "https://www.myget.org/F/your-feed/python/upload"
  $env:MYGET_API_KEY = "your-api-key"
  ```
- **PyPI**: Use `uv publish` with PyPI credentials (or token in `~/.pypirc`)

**Direct PowerShell usage (without Make):**
```powershell
# Release
pwsh -File ./tools/release.ps1
pwsh -File ./tools/release.ps1 -DryRun
pwsh -File ./tools/release.ps1 -GoReleaser

# Publish
pwsh -File ./tools/publish.ps1 -Repository myget
pwsh -File ./tools/publish.ps1 -Repository pypi
pwsh -File ./tools/publish.ps1 -DryRun
```

**Notes:**
- The `__version__` attribute in `__init__.py` automatically reflects the installed package version
- In development (uninstalled), `__version__` shows `"0.0.0.dev"`
- GoReleaser derives release version from git tags, not from the `pyproject.toml` version field
- Keep `pyproject.toml` version in sync with git tags for consistency

### Submodule Workflow

The `docs/rfc-gist/` directory is a Git submodule. When working with it:
- Changes to RFC content happen in the submodule
- The `make update-rfc` command handles commit amending and force-push within the submodule
- After updating the submodule, commit the submodule reference change in the main repo

### Documentation Site

`docs/index.html` is a standalone static page that:
- Uses Solarized Light color scheme with Orange (#cb4b16) brand color
- Dynamically fetches and renders the RFC from the Gist using marked.js
- Is served via GitHub Pages (`.nojekyll` ensures proper serving)

### Planned Architecture

Based on the README, the codebase will include:
- Modular utilities for UiPath Python SDK
- Extended client interfaces (Orchestrator, Data Service, Queues)
- Integration patterns with LangChain, LlamaIndex, and other agent frameworks
- Example connectors for automation developers
