#!/bin/bash

# Run Enhanced Big Picture Analysis with Claude Interactions

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Enhanced Big Picture Analysis${NC}"
echo "=================================="
echo ""
echo "This enhanced version includes:"
echo "  • Security vulnerability scanning"
echo "  • Code complexity metrics"
echo "  • Documentation quality analysis"
echo "  • Git metrics and activity tracking"
echo "  • Overall health scoring"
echo "  • Claude instance interaction tests"
echo ""

# Change to project root
cd "$(dirname "$0")/.."

# Check for required tools
echo -e "${YELLOW}Checking required tools...${NC}"

tools_missing=false

# Check for Python tools
for tool in radon bandit pip-audit; do
    if ! command -v $tool &> /dev/null; then
        echo -e "${RED}  ❌ $tool not found${NC}"
        tools_missing=true
    else
        echo -e "${GREEN}  ✅ $tool found${NC}"
    fi
done

if [ "$tools_missing" = true ]; then
    echo ""
    echo -e "${YELLOW}Installing missing tools...${NC}"
    pip install radon bandit pip-audit safety
fi

# Create output directories
mkdir -p docs/big_picture/claude_interaction_tests
mkdir -p docs/big_picture/reports

# Run the enhanced analyzer
echo ""
echo -e "${YELLOW}Starting enhanced analysis...${NC}"
python3 utils/enhanced_big_picture_analyzer.py

echo ""
echo -e "${GREEN}✅ Enhanced analysis complete!${NC}"
echo ""
echo "📁 Results saved to:"
echo "  - Master index: docs/big_picture/000_INDEX_ENHANCED.md"
echo "  - Project analyses: docs/big_picture/00*_Describe_*.md"
echo "  - Interaction tests: docs/big_picture/claude_interaction_tests/"
echo ""
echo "🧪 To run generated interaction tests:"
echo "  cd docs/big_picture/claude_interaction_tests"
echo "  python3 <project>_interaction_*.py"