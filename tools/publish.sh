#!/usr/bin/env bash
# publish.sh
#
# Publishes Python package to specified repository index
#
# Usage:
#   ./tools/publish.sh [--repository <name>] [--dry-run]
#
# Repositories:
#   myget   - MyGet.org developer feed
#   pypi    - PyPI (default)
#   testpypi - TestPyPI (for testing)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
REPOSITORY="pypi"
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --repository)
            REPOSITORY="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--repository <name>] [--dry-run]"
            echo ""
            echo "Repositories:"
            echo "  myget     - MyGet.org developer feed"
            echo "  pypi      - PyPI (default)"
            echo "  testpypi  - TestPyPI (for testing)"
            echo ""
            echo "Options:"
            echo "  --dry-run  Show what would be published without uploading"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Get current version
CURRENT_VERSION=$(python ./tools/get-version.py)
echo -e "${GREEN}Current version: ${CURRENT_VERSION}${NC}"

# Check if dist/ exists and has files
if [ ! -d "dist" ] || [ -z "$(ls -A dist 2>/dev/null)" ]; then
    echo -e "${RED}Error: dist/ directory is empty or doesn't exist${NC}"
    echo -e "${YELLOW}Run 'make build' first to create distribution packages${NC}"
    exit 1
fi

# List packages to be uploaded
echo -e "${GREEN}Packages to upload:${NC}"
ls -lh dist/

# Build uv publish command based on repository
case $REPOSITORY in
    myget)
        echo -e "${GREEN}Publishing to MyGet.org...${NC}"
        if [ -z "${MYGET_FEED_URL:-}" ]; then
            echo -e "${RED}Error: MYGET_FEED_URL environment variable not set${NC}"
            echo -e "${YELLOW}Set it to your MyGet Python feed URL, e.g.:${NC}"
            echo -e "  export MYGET_FEED_URL=https://www.myget.org/F/your-feed/python/upload"
            exit 1
        fi
        if [ -z "${MYGET_API_KEY:-}" ]; then
            echo -e "${RED}Error: MYGET_API_KEY environment variable not set${NC}"
            echo -e "${YELLOW}Get your API key from MyGet feed settings${NC}"
            exit 1
        fi
        PUBLISH_CMD="uv publish --publish-url $MYGET_FEED_URL --username myget --password $MYGET_API_KEY"
        ;;
    pypi)
        echo -e "${GREEN}Publishing to PyPI...${NC}"
        PUBLISH_CMD="uv publish"
        ;;
    testpypi)
        echo -e "${GREEN}Publishing to TestPyPI...${NC}"
        PUBLISH_CMD="uv publish --publish-url https://test.pypi.org/legacy/"
        ;;
    *)
        echo -e "${RED}Error: Unknown repository '$REPOSITORY'${NC}"
        echo "Valid options: myget, pypi, testpypi"
        exit 1
        ;;
esac

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would execute:${NC}"
    echo -e "  ${PUBLISH_CMD}"
    exit 0
fi

# Execute publish
echo -e "${GREEN}Executing: ${PUBLISH_CMD}${NC}"
eval "$PUBLISH_CMD"

echo -e "${GREEN}✓ Package published successfully to ${REPOSITORY}!${NC}"
