#!/bin/bash

# Run Big Picture Analysis for All Registered Projects

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Big Picture Analysis${NC}"
echo "======================="
echo ""
echo "This script analyzes all registered projects and generates"
echo "comprehensive documentation in docs/big_picture/"
echo ""

# Change to project root
cd "$(dirname "$0")/.."

# Create output directory if it doesn't exist
mkdir -p docs/big_picture

# Run the analyzer
echo -e "${YELLOW}Starting analysis...${NC}"
python3 utils/big_picture_analyzer.py

echo ""
echo -e "${GREEN}✅ Analysis complete!${NC}"
echo ""
echo "View the results:"
echo "  - Master index: docs/big_picture/000_INDEX.md"
echo "  - Individual analyses: docs/big_picture/00*_Describe_*.md"
echo ""
echo "To research specific topics with Perplexity AI, check the"
echo "'Missing Features' section in each project's analysis."