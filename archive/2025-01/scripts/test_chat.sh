#!/bin/bash
# Test runner for chat project (React/FastAPI)

echo "🧪 Testing Chat Interface (React/FastAPI)"
echo "========================================="

# Define the base path
CHAT_BASE="/home/graham/workspace/experiments/chat"

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

# Run Python Backend Tests
echo -e "\n${YELLOW}Running Python Backend Tests...${NC}"
(cd "$CHAT_BASE" && python -m pytest tests/backend/ -v --tb=short 2>&1)
PYTHON_STATUS=$?

if [ $PYTHON_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ Python backend tests passed${NC}"
    ((PASSED_TESTS++))
else
    echo -e "${RED}❌ Python backend tests failed${NC}"
    ((FAILED_TESTS++))
    OVERALL_STATUS=1
fi

# Run Frontend React Tests
echo -e "\n${YELLOW}Running React Frontend Tests...${NC}"
(cd "$CHAT_BASE/frontend" && npm test -- --watchAll=false --passWithNoTests 2>&1)
REACT_STATUS=$?

if [ $REACT_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ React frontend tests passed${NC}"
    ((PASSED_TESTS++))
else
    echo -e "${RED}❌ React frontend tests failed${NC}"
    ((FAILED_TESTS++))
    OVERALL_STATUS=1
fi

# Run Integration Tests
echo -e "\n${YELLOW}Running Integration Tests...${NC}"
(cd "$CHAT_BASE" && python -m pytest tests/integration/ -v --tb=short 2>&1)
INTEGRATION_STATUS=$?

if [ $INTEGRATION_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ Integration tests passed${NC}"
    ((PASSED_TESTS++))
else
    echo -e "${RED}❌ Integration tests failed${NC}"
    ((FAILED_TESTS++))
    OVERALL_STATUS=1
fi

# Check Docker Configuration
echo -e "\n${YELLOW}Checking Docker Configuration...${NC}"
if [ -f "$CHAT_BASE/docker-compose.yml" ]; then
    docker compose -f "$CHAT_BASE/docker-compose.yml" config >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Docker configuration valid${NC}"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}❌ Docker configuration invalid${NC}"
        ((FAILED_TESTS++))
    fi
else
    echo -e "${YELLOW}⚠️  No docker-compose.yml found${NC}"
    ((SKIPPED_TESTS++))
fi

# Summary
echo -e "\n========================================="
echo -e "Test Summary for Chat Interface:"
echo -e "  ${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "  ${RED}Failed: $FAILED_TESTS${NC}"
echo -e "  ${YELLOW}Skipped: $SKIPPED_TESTS${NC}"
echo -e "========================================="

exit $OVERALL_STATUS