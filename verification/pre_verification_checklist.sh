#!/bin/bash
# Pre-Verification Checklist for Granger Ecosystem
# Based on TEST_VERIFICATION_TEMPLATE_GUIDE.md

echo "========================================="
echo "GRANGER ECOSYSTEM PRE-VERIFICATION CHECK"
echo "========================================="
echo "Date: $(date)"
echo ""

# List of core Granger modules to verify
MODULES=(
    "/home/graham/workspace/experiments/sparta"
    "/home/graham/workspace/experiments/marker"
    "/home/graham/workspace/experiments/arangodb"
    "/home/graham/workspace/experiments/youtube_transcripts"
    "/home/graham/workspace/experiments/llm_call"
    "/home/graham/workspace/experiments/unsloth_wip"
    "/home/graham/workspace/mcp-servers/arxiv-mcp-server"
    "/home/graham/workspace/experiments/granger_hub"
    "/home/graham/workspace/experiments/claude-test-reporter"
    "/home/graham/workspace/experiments/rl_commons"
    "/home/graham/workspace/experiments/world_model"
)

# Function to check a single module
check_module() {
    local module_path=$1
    local module_name=$(basename $module_path)
    
    echo ""
    echo "=== Checking $module_name ==="
    echo "Path: $module_path"
    
    if [ ! -d "$module_path" ]; then
        echo "❌ CRITICAL: Module directory not found!"
        return 1
    fi
    
    cd "$module_path"
    
    # 1. Check Python version requirement
    echo ""
    echo "1. Python Version Check:"
    if [ -f "pyproject.toml" ]; then
        python_req=$(grep -E "python.*=" pyproject.toml | grep -v python- | head -1)
        echo "   Required: $python_req"
        echo "   Current: $(python --version)"
    else
        echo "   ⚠️  No pyproject.toml found"
    fi
    
    # 2. Check project structure
    echo ""
    echo "2. Project Structure:"
    if [ -d "src" ]; then
        py_files=$(find src -name "*.py" -type f | wc -l)
        echo "   ✓ src/ directory exists"
        echo "   Python files in src/: $py_files"
    else
        echo "   ❌ No src/ directory found"
    fi
    
    # 3. Check for skeleton indicators
    echo ""
    echo "3. Skeleton Project Detection:"
    total_lines=$(find . -name "*.py" -not -path "./tests/*" -not -path "./.venv/*" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}')
    pass_count=$(grep -r "pass$" --include="*.py" . 2>/dev/null | grep -v test | wc -l)
    not_impl=$(grep -r "raise NotImplementedError" --include="*.py" . 2>/dev/null | wc -l)
    todos=$(grep -r "TODO\|FIXME\|XXX" --include="*.py" . 2>/dev/null | wc -l)
    
    echo "   Total lines: $total_lines"
    echo "   'pass' statements: $pass_count"
    echo "   NotImplementedError: $not_impl"
    echo "   TODOs: $todos"
    
    if [ $pass_count -gt 10 ] || [ $not_impl -gt 5 ]; then
        echo "   ⚠️  WARNING: Possible skeleton project!"
    fi
    
    # 4. Check for existing setup patterns
    echo ""
    echo "4. Setup Scripts:"
    setup_files=$(find . -name "*setup*.py" -o -name "*config*.py" | grep -v test | head -5)
    if [ -n "$setup_files" ]; then
        echo "$setup_files" | while read f; do echo "   - $f"; done
    else
        echo "   No setup files found"
    fi
    
    # 5. Check .env for service credentials
    echo ""
    echo "5. Environment Configuration:"
    if [ -f ".env" ]; then
        echo "   ✓ .env file exists"
        grep -E "(ARANGO|REDIS|POSTGRES|API_KEY|GEMINI|ANTHROPIC)" .env 2>/dev/null | sed 's/=.*/=***/' | head -5
    else
        echo "   ❌ No .env file"
    fi
    
    # 6. Check if tests can be collected
    echo ""
    echo "6. Test Collection:"
    if [ -d "tests" ]; then
        test_count=$(find tests -name "test_*.py" -type f | wc -l)
        echo "   Test files found: $test_count"
        
        # Try to collect tests
        echo "   Attempting test collection..."
        python -m pytest --collect-only --quiet 2>&1 | head -5
    else
        echo "   ❌ No tests/ directory"
    fi
    
    # 7. Check for mocks
    echo ""
    echo "7. Mock Detection:"
    mock_count=$(grep -r "mock\|Mock\|@patch" tests/ --include="*.py" 2>/dev/null | wc -l)
    echo "   Mock usage found: $mock_count instances"
    if [ $mock_count -gt 0 ]; then
        echo "   ❌ MOCKS DETECTED - must be removed!"
    fi
    
    # 8. Check for interaction capabilities
    echo ""
    echo "8. Granger Integration Check:"
    hub_integration=$(grep -r "granger_hub\|GrangerHub" src/ --include="*.py" 2>/dev/null | wc -l)
    message_handling=$(grep -r "handle_message\|process_message" src/ --include="*.py" 2>/dev/null | wc -l)
    
    echo "   Hub integration references: $hub_integration"
    echo "   Message handling functions: $message_handling"
    
    if [ $hub_integration -eq 0 ] && [ $message_handling -eq 0 ]; then
        echo "   ❌ No Granger integration found!"
    fi
    
    # 9. Check dependencies
    echo ""
    echo "9. Dependencies Status:"
    if command -v uv &> /dev/null; then
        echo "   Running uv pip list..."
        uv pip list | grep -E "(pytest|granger|arangodb|marker|sparta)" | head -5
    else
        echo "   ⚠️  uv not available"
    fi
    
    echo ""
    echo "--- End of $module_name check ---"
}

# Function to check services
check_services() {
    echo ""
    echo "=== SERVICE AVAILABILITY CHECK ==="
    
    # Check ArangoDB
    echo ""
    echo "ArangoDB:"
    if curl -s http://localhost:8529/_api/version >/dev/null 2>&1; then
        echo "   ✓ ArangoDB is running on port 8529"
    else
        echo "   ❌ ArangoDB not accessible"
    fi
    
    # Check Redis
    echo ""
    echo "Redis:"
    if command -v redis-cli &> /dev/null && redis-cli ping >/dev/null 2>&1; then
        echo "   ✓ Redis is running"
    else
        echo "   ❌ Redis not accessible"
    fi
    
    # Check Docker
    echo ""
    echo "Docker:"
    if docker ps >/dev/null 2>&1; then
        echo "   ✓ Docker is running"
        echo "   Containers:"
        docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "(arango|redis|postgres)"
    else
        echo "   ❌ Docker not running"
    fi
}

# Main execution
echo "Starting comprehensive pre-verification checks..."

# Check services first
check_services

# Check each module
for module in "${MODULES[@]}"; do
    check_module "$module"
done

echo ""
echo "========================================="
echo "PRE-VERIFICATION COMPLETE"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Fix any Python version mismatches"
echo "2. Install missing dependencies with uv"
echo "3. Start required services (ArangoDB, Redis, etc.)"
echo "4. Remove all mocks from test files"
echo "5. Implement missing Granger integrations"
echo ""