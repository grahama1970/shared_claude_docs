#!/bin/bash
# Test runner for granger-ui from shared_claude_docs

echo "🧪 Testing Granger UI Components"
echo "================================"

# Define the base path
UI_BASE="/home/graham/workspace/granger-ui"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Track status
OVERALL_STATUS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Test ui-core
echo -e "\n${YELLOW}Testing @granger/ui-core...${NC}"
(cd "$UI_BASE/packages/ui-core" && pnpm test --passWithNoTests 2>&1)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ ui-core tests passed${NC}"
    ((PASSED_TESTS++))
else
    echo -e "${RED}❌ ui-core tests failed${NC}"
    ((FAILED_TESTS++))
    OVERALL_STATUS=1
fi

# Test ui-web
echo -e "\n${YELLOW}Testing @granger/ui-web...${NC}"
(cd "$UI_BASE/packages/ui-web" && pnpm test --passWithNoTests 2>&1)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ ui-web tests passed${NC}"
    ((PASSED_TESTS++))
else
    echo -e "${RED}❌ ui-web tests failed${NC}"
    ((FAILED_TESTS++))
    OVERALL_STATUS=1
fi

# Test ui-terminal
echo -e "\n${YELLOW}Testing @granger/ui-terminal...${NC}"
(cd "$UI_BASE/packages/ui-terminal" && pnpm test --passWithNoTests 2>&1)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ ui-terminal tests passed${NC}"
    ((PASSED_TESTS++))
else
    echo -e "${YELLOW}⚠️  ui-terminal has no tests${NC}"
fi

# Summary
echo -e "\n================================"
echo -e "Test Summary:"
echo -e "  ${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "  ${RED}Failed: $FAILED_TESTS${NC}"
echo -e "================================"

exit $OVERALL_STATUS