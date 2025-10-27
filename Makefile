# Makefile for cprima-forge/uipath-extensions
# Windows-compatible (requires PowerShell Core 7+)

GIST_PATH := docs/rfc-gist
PWSH := pwsh

# Development commands (using uv)
.PHONY: install
install:
	uv pip install -e .

.PHONY: install-dev
install-dev:
	uv pip install -e ".[dev]"

.PHONY: sync
sync:
	uv pip sync requirements.txt

.PHONY: test
test:
	uv run pytest

.PHONY: test-cov
test-cov:
	uv run pytest --cov=cpmf.uipath_ext --cov-report=html --cov-report=term

.PHONY: lint
lint:
	uv run ruff check src/ tests/

.PHONY: lint-fix
lint-fix:
	uv run ruff check --fix src/ tests/
	uv run ruff format src/ tests/

.PHONY: build
build:
	uv build

.PHONY: clean
clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# RFC management
.PHONY: update-rfc
update-rfc:
	cd $(GIST_PATH) && \
	git add . && \
	git commit --amend --no-edit || echo "No previous commit to amend." && \
	git push --force-with-lease

# Release management
.PHONY: version
version:
	@python ./tools/get-version.py

.PHONY: release
release:
	@$(PWSH) -ExecutionPolicy Bypass -File ./tools/release.ps1

.PHONY: release-dry-run
release-dry-run:
	@$(PWSH) -ExecutionPolicy Bypass -File ./tools/release.ps1 -DryRun

.PHONY: release-github
release-github:
	@$(PWSH) -ExecutionPolicy Bypass -File ./tools/release.ps1 -GoReleaser

# Package publishing
.PHONY: publish-myget
publish-myget:
	@$(PWSH) -ExecutionPolicy Bypass -File ./tools/publish.ps1 -Repository myget

.PHONY: publish-pypi
publish-pypi:
	@$(PWSH) -ExecutionPolicy Bypass -File ./tools/publish.ps1 -Repository pypi

.PHONY: publish-testpypi
publish-testpypi:
	@$(PWSH) -ExecutionPolicy Bypass -File ./tools/publish.ps1 -Repository testpypi

.PHONY: publish-dry-run
publish-dry-run:
	@$(PWSH) -ExecutionPolicy Bypass -File ./tools/publish.ps1 -DryRun
