#!/bin/bash

# Enhanced Project Cleanup Utility Runner
# For localhost execution with comprehensive validation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}🚀 Enhanced Project Cleanup Utility${NC}"
echo -e "${BLUE}================================================${NC}"

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "Python version: ${GREEN}${PYTHON_VERSION}${NC}"

# Check for required tools
echo -e "\n${YELLOW}Checking required tools...${NC}"

# Check ripgrep
if command -v rg &> /dev/null; then
    echo -e "  ✅ ripgrep installed ($(rg --version | head -1))"
else
    echo -e "  ${RED}❌ ripgrep not installed${NC}"
    echo "  Install with: curl -LO https://github.com/BurntSushi/ripgrep/releases/download/13.0.0/ripgrep_13.0.0_amd64.deb && sudo dpkg -i ripgrep_13.0.0_amd64.deb"
fi

# Check git
if command -v git &> /dev/null; then
    echo -e "  ✅ git installed ($(git --version))"
else
    echo -e "  ${RED}❌ git not installed${NC}"
fi

# Check pytest
if python3 -c "import pytest" 2>/dev/null; then
    echo -e "  ✅ pytest installed"
else
    echo -e "  ${YELLOW}⚠️  pytest not installed (some features limited)${NC}"
fi

# Check toml
if python3 -c "import toml" 2>/dev/null; then
    echo -e "  ✅ toml installed"
else
    echo -e "  ${YELLOW}⚠️  toml not installed (some features limited)${NC}"
fi

# Parse command line arguments
CONFIG_FILE="cleanup_config_localhost.json"
VERBOSE=""
DRY_RUN=""
SEQUENTIAL=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        --dry-run)
            DRY_RUN="--dry-run"
            shift
            ;;
        --sequential)
            SEQUENTIAL="--sequential"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --config FILE    Use custom config file (default: cleanup_config_localhost.json)"
            echo "  -v, --verbose    Enable verbose output"
            echo "  --dry-run       Perform dry run without making changes"
            echo "  --sequential    Process projects sequentially (default: parallel)"
            echo "  -h, --help      Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}Error: Configuration file not found: $CONFIG_FILE${NC}"
    echo "Using default localhost config..."
    CONFIG_FILE="cleanup_config_localhost.json"
fi

echo -e "\n${YELLOW}Configuration:${NC}"
echo -e "  Config file: ${BLUE}$CONFIG_FILE${NC}"
echo -e "  Mode: ${BLUE}${DRY_RUN:-LIVE}${NC}"
echo -e "  Processing: ${BLUE}${SEQUENTIAL:-PARALLEL}${NC}"

# Create reports directory
mkdir -p cleanup_reports

# Run the enhanced cleanup utility
echo -e "\n${GREEN}Starting cleanup...${NC}\n"

# Check if we're in a project with uv
if [ -f "../../pyproject.toml" ] && command -v uv &> /dev/null; then
    echo -e "Using ${BLUE}uv run${NC} for dependency management"
    cd ../.. && uv run python utils/cleanup_utility/enhanced_cleanup.py \
        --config "utils/cleanup_utility/$CONFIG_FILE" \
        $VERBOSE \
        $DRY_RUN \
        $SEQUENTIAL
else
    python3 enhanced_cleanup.py \
        --config "$CONFIG_FILE" \
        $VERBOSE \
        $DRY_RUN \
        $SEQUENTIAL
fi

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "\n${GREEN}✅ Cleanup completed successfully!${NC}"
    echo -e "Check the cleanup_reports/ directory for detailed reports."
else
    echo -e "\n${RED}❌ Cleanup completed with errors!${NC}"
    echo -e "Check the cleanup_reports/ directory for details."
fi

# Show latest report
LATEST_REPORT=$(ls -t cleanup_reports/comprehensive_report_*.md 2>/dev/null | head -1)
if [ -n "$LATEST_REPORT" ]; then
    echo -e "\n${YELLOW}Latest report: ${BLUE}$LATEST_REPORT${NC}"
    echo -e "\nTo view the report:"
    echo -e "  cat $LATEST_REPORT"
fi

exit $EXIT_CODE