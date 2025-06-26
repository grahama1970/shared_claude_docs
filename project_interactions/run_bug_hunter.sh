#!/bin/bash
# run_bug_hunter.sh - Autonomous bug hunting execution script

set -e

echo "🎯 Granger Bug Hunter - Autonomous Testing System"
echo "================================================"

# Default values
DURATION_HOURS=1.0
FOCUS_MODULES=""
OUTPUT_DIR="bug_hunt_reports"
GITHUB_ISSUES=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --duration)
            DURATION_HOURS="$2"
            shift 2
            ;;
        --focus)
            FOCUS_MODULES="$2"
            shift 2
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --create-issues)
            GITHUB_ISSUES=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --duration HOURS     Duration of bug hunt in hours (default: 1.0)"
            echo "  --focus MODULES      Comma-separated list of modules to focus on"
            echo "  --output-dir DIR     Output directory for reports (default: bug_hunt_reports)"
            echo "  --create-issues      Create GitHub issues for critical bugs"
            echo "  --help               Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Timestamp for this run
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_NAME="bug_hunt_${TIMESTAMP}"

echo "⚙️  Configuration:"
echo "  Duration: ${DURATION_HOURS} hours"
echo "  Focus: ${FOCUS_MODULES:-All modules}"
echo "  Output: ${OUTPUT_DIR}/${REPORT_NAME}"
echo ""

# Step 1: Verify preconditions per TEST_VERIFICATION_TEMPLATE_GUIDE
echo "🔍 Step 1: Verifying preconditions..."

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
if [[ "$PYTHON_VERSION" < "3.10" ]]; then
    echo "❌ Python 3.10+ required, found $PYTHON_VERSION"
    exit 1
fi

# Check for required services
echo "  Checking ArangoDB..."
if ! curl -s http://localhost:8529/_api/version > /dev/null 2>&1; then
    echo "❌ ArangoDB not running on localhost:8529"
    echo "  Start with: docker run -p 8529:8529 -e ARANGO_NO_AUTH=1 arangodb"
    exit 1
fi

# Check for mocks (banned)
echo "  Checking for mock usage..."
if grep -r "mock\|Mock\|@patch" project_interactions/tests/ --include="*.py" 2>/dev/null | grep -v "honeypot"; then
    echo "❌ Mock usage detected in tests - this is forbidden!"
    exit 1
fi

# Check module availability
echo "  Checking Granger modules..."
python3 -c "
import sys
sys.path.extend([
    '/home/graham/workspace/experiments/arangodb/src',
    '/home/graham/workspace/experiments/marker/src',
    '/home/graham/workspace/experiments/sparta/src',
    '/home/graham/workspace/mcp-servers/arxiv-mcp-server/src',
    '/home/graham/workspace/experiments/memvid/src',
])
modules_found = 0
for module in ['arangodb', 'marker', 'sparta', 'arxiv_mcp_server', 'memvid']:
    try:
        __import__(module)
        modules_found += 1
    except:
        pass
if modules_found < 2:
    print(f'❌ Only {modules_found} modules available, need at least 2')
    sys.exit(1)
print(f'✅ {modules_found} modules available')
"

echo "✅ Preconditions verified"
echo ""

# Step 2: Run honeypot tests
echo "🍯 Step 2: Running honeypot tests (should fail)..."

# Create temporary honeypot test
cat > /tmp/test_honeypot_temp.py << 'EOF'
import pytest
import time

class TestHoneypot:
    @pytest.mark.honeypot
    def test_impossible_assertion(self):
        """This should always fail"""
        assert 1 == 2
        
    @pytest.mark.honeypot
    def test_instant_operation(self):
        """Operations cannot be instant"""
        start = time.time()
        # Simulate heavy operation
        result = sum(i*i for i in range(1000000))
        duration = time.time() - start
        assert duration < 0.0001, f"Too slow: {duration}s"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
EOF

# Run honeypot tests
if python3 /tmp/test_honeypot_temp.py 2>&1 | grep -q "2 failed"; then
    echo "✅ Honeypot tests correctly failing"
else
    echo "❌ Honeypot tests not failing - framework compromised!"
    exit 1
fi

rm /tmp/test_honeypot_temp.py
echo ""

# Step 3: Run the bug hunter
echo "🏃 Step 3: Running autonomous bug hunt..."

# Build command
CMD="python3 -m project_interactions.granger_bug_hunter"
CMD="$CMD --duration $DURATION_HOURS"
CMD="$CMD --output ${OUTPUT_DIR}/${REPORT_NAME}.md"

if [ -n "$FOCUS_MODULES" ]; then
    CMD="$CMD --focus $FOCUS_MODULES"
fi

# Execute bug hunt
echo "Executing: $CMD"
if $CMD; then
    HUNT_SUCCESS=true
    echo "✅ Bug hunt completed successfully"
else
    HUNT_SUCCESS=false
    echo "⚠️  Bug hunt completed with critical issues found"
fi

# Step 4: Generate additional reports
echo ""
echo "📊 Step 4: Generating reports..."

# Generate JSON report
python3 -c "
from project_interactions.granger_bug_hunter_reporter import create_json_report
import json

with open('bug_hunt_report.json', 'r') as f:
    results = json.load(f)
    
create_json_report(results, '${OUTPUT_DIR}/${REPORT_NAME}.json')
print('✅ JSON report generated')
"

# Generate visual dashboard if matplotlib available
python3 -c "
from project_interactions.granger_bug_hunter_reporter import create_bug_dashboard
import json

try:
    with open('bug_hunt_report.json', 'r') as f:
        results = json.load(f)
    
    dashboard_path = create_bug_dashboard(results, '${OUTPUT_DIR}')
    if dashboard_path:
        print(f'✅ Visual dashboard generated: {dashboard_path}')
    else:
        print('⚠️  Visualization libraries not available')
except Exception as e:
    print(f'⚠️  Dashboard generation failed: {e}')
"

# Step 5: Create GitHub issues if requested
if [ "$GITHUB_ISSUES" = true ]; then
    echo ""
    echo "🐛 Step 5: Creating GitHub issues..."
    
    python3 scripts/create_bug_issues.py "${OUTPUT_DIR}/${REPORT_NAME}.json"
    echo "✅ GitHub issues created"
fi

# Step 6: Summary
echo ""
echo "📈 Summary Report"
echo "================"

python3 -c "
import json

with open('${OUTPUT_DIR}/${REPORT_NAME}.json', 'r') as f:
    results = json.load(f)
    
print(f\"Total Bugs Found: {results.get('total_bugs_found', 0)}\")
print(f\"Critical Bugs: {results.get('critical_bugs', 0)}\")
print(f\"High Priority: {results.get('high_bugs', 0)}\")
print(f\"Tests Run: {results.get('tests_run', 0)}\")
print(f\"Duration: {results.get('duration_hours', 0):.1f} hours\")
print()
print('Bugs by Module:')
for module, count in results.get('bugs_by_module', {}).items():
    print(f\"  {module}: {count}\")
"

echo ""
echo "📄 Reports saved to: ${OUTPUT_DIR}/"
echo "  - ${REPORT_NAME}.md (Markdown report)"
echo "  - ${REPORT_NAME}.json (JSON data)"

# Exit with appropriate code
if [ "$HUNT_SUCCESS" = true ]; then
    echo ""
    echo "✅ Bug hunt completed - no critical issues"
    exit 0
else
    echo ""
    echo "❌ Bug hunt found critical issues requiring attention"
    exit 1
fi