#!/bin/bash
# Test runner for annotator project

echo "🧪 Testing Annotator (PDF Annotation Tool)"
echo "=========================================="

# Define the base path
ANNOTATOR_BASE="/home/graham/workspace/experiments/annotator"

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

# Run Python tests
echo -e "\n${YELLOW}Running Python Backend Tests...${NC}"
(cd "$ANNOTATOR_BASE" && python -m pytest tests/ -v --tb=short 2>&1)
PYTHON_STATUS=$?

if [ $PYTHON_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ Python tests passed${NC}"
    ((PASSED_TESTS++))
else
    echo -e "${RED}❌ Python tests failed${NC}"
    ((FAILED_TESTS++))
    OVERALL_STATUS=1
fi

# Check for JavaScript/Frontend tests
echo -e "\n${YELLOW}Checking for Frontend Tests...${NC}"
if [ -f "$ANNOTATOR_BASE/frontend/package.json" ]; then
    echo "Frontend package.json found, checking for tests..."
    (cd "$ANNOTATOR_BASE/frontend" && npm test 2>&1)
    FRONTEND_STATUS=$?
    
    if [ $FRONTEND_STATUS -eq 0 ]; then
        echo -e "${GREEN}✅ Frontend tests passed${NC}"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}❌ Frontend tests failed${NC}"
        ((FAILED_TESTS++))
        OVERALL_STATUS=1
    fi
else
    echo -e "${YELLOW}⚠️  No frontend test configuration found${NC}"
    ((SKIPPED_TESTS++))
fi

# Run coverage report
echo -e "\n${YELLOW}Generating Coverage Report...${NC}"
(cd "$ANNOTATOR_BASE" && python -m pytest tests/ --cov=src/annotator --cov-report=term-missing 2>&1)

# Summary
echo -e "\n=========================================="
echo -e "Test Summary for Annotator:"
echo -e "  ${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "  ${RED}Failed: $FAILED_TESTS${NC}"
echo -e "  ${YELLOW}Skipped: $SKIPPED_TESTS${NC}"
echo -e "=========================================="

exit $OVERALL_STATUS