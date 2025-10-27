#!/usr/bin/env bash
# release.sh
#
# Intelligent release script that:
# 1. Reads version from pyproject.toml
# 2. Compares with latest git tag
# 3. Creates new tag only if version changed
# 4. Optionally triggers GoReleaser
#
# Usage:
#   ./tools/release.sh [--dry-run] [--goreleaser]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
DRY_RUN=false
RUN_GORELEASER=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --goreleaser)
            RUN_GORELEASER=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--dry-run] [--goreleaser]"
            exit 1
            ;;
    esac
done

# Get current version from pyproject.toml
CURRENT_VERSION=$(python ./tools/get-version.py)
echo -e "${GREEN}Current version in pyproject.toml: ${CURRENT_VERSION}${NC}"

# Get latest git tag (if any)
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "none")
if [ "$LATEST_TAG" = "none" ]; then
    echo -e "${YELLOW}No existing tags found${NC}"
    LATEST_VERSION="none"
else
    # Strip 'v' prefix if present
    LATEST_VERSION="${LATEST_TAG#v}"
    echo -e "${GREEN}Latest git tag: ${LATEST_TAG} (version: ${LATEST_VERSION})${NC}"
fi

# Compare versions
if [ "$LATEST_VERSION" = "$CURRENT_VERSION" ]; then
    echo -e "${YELLOW}Version unchanged (${CURRENT_VERSION}). No new tag needed.${NC}"
    exit 0
fi

# Version has changed - create new tag
NEW_TAG="v${CURRENT_VERSION}"
echo -e "${GREEN}Version changed: ${LATEST_VERSION} → ${CURRENT_VERSION}${NC}"
echo -e "${GREEN}Creating new tag: ${NEW_TAG}${NC}"

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would create tag: ${NEW_TAG}${NC}"
    if [ "$RUN_GORELEASER" = true ]; then
        echo -e "${YELLOW}[DRY RUN] Would run: goreleaser release${NC}"
    fi
    exit 0
fi

# Create the tag
git tag -a "$NEW_TAG" -m "Release version ${CURRENT_VERSION}"
echo -e "${GREEN}✓ Created tag: ${NEW_TAG}${NC}"

# Optionally run GoReleaser
if [ "$RUN_GORELEASER" = true ]; then
    echo -e "${GREEN}Running GoReleaser...${NC}"
    goreleaser release --clean
    echo -e "${GREEN}✓ Release created${NC}"
else
    echo -e "${YELLOW}Tag created locally. To push:${NC}"
    echo -e "  git push origin main --tags"
    echo -e "${YELLOW}To create GitHub release:${NC}"
    echo -e "  goreleaser release --clean"
fi
