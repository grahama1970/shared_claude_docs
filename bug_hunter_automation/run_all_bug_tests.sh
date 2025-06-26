#!/bin/bash
"""
Bug Hunter Automation Script
Runs all bug hunting tests systematically
"""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🐛 GRANGER Bug Hunter Automation${NC}"
echo "=================================="
date

# Ensure we're in the right directory
cd /home/graham/workspace/shared_claude_docs

# Activate virtual environment
source .venv/bin/activate

# Create results directory
mkdir -p bug_hunter_results
mkdir -p bug_hunter_reports

# Function to run a test and capture results
run_test() {
    local test_num=$1
    local test_name=$2
    local test_file=$3
    
    echo -e "\n${YELLOW}Running Task #${test_num}: ${test_name}${NC}"
    
    if [ -f "$test_file" ]; then
        # Run test with timeout
        timeout 60s python "$test_file" 2>&1 | tee "bug_hunter_results/task_${test_num}_output.log"
        
        # Check exit status
        if [ ${PIPESTATUS[0]} -eq 124 ]; then
            echo -e "${RED}❌ Test timed out after 60 seconds${NC}"
            echo "{\"task\": \"${test_num}\", \"status\": \"timeout\", \"module\": \"${test_name}\"}" > "bug_hunter_results/task_${test_num}_result.json"
        elif [ ${PIPESTATUS[0]} -eq 0 ]; then
            echo -e "${GREEN}✅ Test completed successfully${NC}"
        else
            echo -e "${RED}❌ Test failed with error${NC}"
        fi
    else
        echo -e "${RED}❌ Test file not found: $test_file${NC}"
    fi
}

# Run ecosystem health check
echo -e "\n${YELLOW}Task #001: Ecosystem Health Check${NC}"
python /home/graham/.claude/commands/granger-verify --test --auto --output bug_hunter_reports/ecosystem_health.md

# Run Level 0 tests
run_test "002" "SPARTA CVE Check" "bug_hunter_tests/task_002_sparta_cve_direct.py"
run_test "003" "ArXiv MCP Search" "bug_hunter_tests/task_003_arxiv_quick.py"
run_test "004" "ArangoDB Operations" "bug_hunter_tests/task_004_arangodb.py"

# Aggregate results
echo -e "\n${YELLOW}Generating Summary Report...${NC}"
python - << EOF
import json
import glob
from datetime import datetime

results = []
for result_file in glob.glob("bug_hunter_results/task_*_result.json"):
    try:
        with open(result_file) as f:
            results.append(json.load(f))
    except:
        pass

# Load detailed bug reports
bugs_found = []
for bug_file in glob.glob("bug_hunter_results_*.json"):
    try:
        with open(bug_file) as f:
            data = json.load(f)
            if "bugs_found" in data:
                bugs_found.extend(data["bugs_found"])
    except:
        pass

summary = {
    "timestamp": datetime.now().isoformat(),
    "tests_run": len(results),
    "total_bugs_found": len(bugs_found),
    "bugs": bugs_found,
    "test_results": results
}

with open("bug_hunter_results/automation_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"\\nTotal bugs found: {len(bugs_found)}")
for i, bug in enumerate(bugs_found, 1):
    print(f"  {i}. {bug}")
EOF

echo -e "\n${GREEN}✅ Bug Hunter Automation Complete${NC}"
echo "Results saved in bug_hunter_results/"
echo "Reports saved in bug_hunter_reports/"