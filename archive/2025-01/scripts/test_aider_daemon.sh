#!/bin/bash
# Test runner for aider-daemon project

echo "🧪 Testing Aider-Daemon (CLI/Daemon)"
echo "===================================="

# Define the base path
AIDER_BASE="/home/graham/workspace/experiments/aider-daemon"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Track status
OVERALL_STATUS=0
PASSED_TESTS=0
FAILED_TESTS=0
SKIPPED_TESTS=0

# Activate virtual environment
source .venv/bin/activate

# Run Unit Tests
echo -e "\n${YELLOW}Running Unit Tests...${NC}"
(cd "$AIDER_BASE" && python -m pytest tests/unit/ -v --tb=short 2>&1)
UNIT_STATUS=$?

if [ $UNIT_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ Unit tests passed${NC}"
    ((PASSED_TESTS++))
else
    echo -e "${RED}❌ Unit tests failed${NC}"
    ((FAILED_TESTS++))
    OVERALL_STATUS=1
fi

# Run Integration Tests
echo -e "\n${YELLOW}Running Integration Tests...${NC}"
(cd "$AIDER_BASE" && python -m pytest tests/integration/ -v --tb=short 2>&1)
INTEGRATION_STATUS=$?

if [ $INTEGRATION_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ Integration tests passed${NC}"
    ((PASSED_TESTS++))
else
    echo -e "${RED}❌ Integration tests failed${NC}"
    ((FAILED_TESTS++))
    OVERALL_STATUS=1
fi

# Run Smoke Tests
echo -e "\n${YELLOW}Running Smoke Tests...${NC}"
(cd "$AIDER_BASE" && python -m pytest tests/smoke/ -v --tb=short 2>&1)
SMOKE_STATUS=$?

if [ $SMOKE_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ Smoke tests passed${NC}"
    ((PASSED_TESTS++))
else
    echo -e "${RED}❌ Smoke tests failed${NC}"
    ((FAILED_TESTS++))
    OVERALL_STATUS=1
fi

# Check CLI Entry Point
echo -e "\n${YELLOW}Checking CLI Entry Point...${NC}"
(cd "$AIDER_BASE" && python -m aider_daemon.cli.app --help >/dev/null 2>&1)
CLI_STATUS=$?

if [ $CLI_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ CLI entry point working${NC}"
    ((PASSED_TESTS++))
else
    echo -e "${RED}❌ CLI entry point failed${NC}"
    ((FAILED_TESTS++))
    OVERALL_STATUS=1
fi

# Summary
echo -e "\n===================================="
echo -e "Test Summary for Aider-Daemon:"
echo -e "  ${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "  ${RED}Failed: $FAILED_TESTS${NC}"
echo -e "  ${YELLOW}Skipped: $SKIPPED_TESTS${NC}"
echo -e "===================================="

exit $OVERALL_STATUS