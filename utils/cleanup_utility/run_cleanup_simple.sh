#!/bin/bash

# Enhanced Project Cleanup Utility Runner - Simplified Version
# This script runs the cleanup utility across all configured projects

CONFIG_FILE="cleanup_config.json"
REPORT_DIR="cleanup_reports"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file $CONFIG_FILE not found!"
    exit 1
fi

# Create reports directory
mkdir -p "$REPORT_DIR"

echo "================================================"
echo "Enhanced Project Cleanup Utility"
echo "================================================"
echo "Timestamp: $TIMESTAMP"
echo "Config: $CONFIG_FILE"
echo ""

# Define projects directly (extracted from config)
PROJECTS=(
    "/home/graham/workspace/experiments/sparta/"
    "/home/graham/workspace/experiments/marker/"
    "/home/graham/workspace/experiments/chat/"
    "/home/graham/workspace/experiments/arangodb/"
    "/home/graham/workspace/experiments/youtube_transcripts/"
    "/home/graham/workspace/experiments/claude_max_proxy/"
    "/home/graham/workspace/mcp-servers/arxiv-mcp-server/"
    "/home/graham/workspace/experiments/claude-module-communicator/"
    "/home/graham/workspace/experiments/claude-test-reporter/"
    "/home/graham/workspace/experiments/unsloth_wip/"
    "/home/graham/workspace/experiments/marker-ground-truth/"
    "/home/graham/workspace/experiments/mcp-screenshot/"
)

echo "Projects to process:"
for PROJECT in "${PROJECTS[@]}"; do
    echo "  - $PROJECT"
done
echo ""

# Summary variables
TOTAL_PROJECTS=0
SUCCESSFUL_PROJECTS=0
FAILED_PROJECTS=0

# Process each project
for PROJECT in "${PROJECTS[@]}"; do
    TOTAL_PROJECTS=$((TOTAL_PROJECTS + 1))
    PROJECT_SUCCESS=true
    
    echo ""
    echo "================================================"
    echo "Processing: $PROJECT"
    echo "================================================"
    
    if [ ! -d "$PROJECT" ]; then
        echo "Error: Project directory not found: $PROJECT"
        FAILED_PROJECTS=$((FAILED_PROJECTS + 1))
        continue
    fi
    
    PROJECT_NAME=$(basename "$PROJECT")
    ANALYSIS_DIR="$REPORT_DIR/$TIMESTAMP-$PROJECT_NAME"
    mkdir -p "$ANALYSIS_DIR"
    
    cd "$PROJECT"
    
    # Phase 1: Git safety
    echo "🔒 Creating safety branch..."
    git fetch origin 2>/dev/null
    git checkout main 2>/dev/null || git checkout master 2>/dev/null
    git pull origin main 2>/dev/null || git pull origin master 2>/dev/null
    CLEANUP_BRANCH="cleanup-$TIMESTAMP"
    git checkout -b "$CLEANUP_BRANCH" 2>/dev/null
    git tag "pre-cleanup-$TIMESTAMP" 2>/dev/null
    
    # Phase 2: Analysis
    echo "🔍 Analyzing project structure..."
    
    # Check for README.md
    if [ -f README.md ]; then
        echo "  ✅ README.md found"
        grep -iE "feature|capability|function|support|provide|implement" README.md > "$ANALYSIS_DIR/claimed_features.txt" 2>/dev/null || true
    else
        echo "  ⚠️  No README.md found"
        echo "Missing README.md" > "$ANALYSIS_DIR/issues.txt"
    fi
    
    # Check for claude-test-reporter
    if [ -f pyproject.toml ]; then
        if grep -q "claude-test-reporter" pyproject.toml; then
            echo "  ✅ claude-test-reporter configured"
        else
            echo "  ❌ claude-test-reporter missing"
            echo "Missing claude-test-reporter in pyproject.toml" >> "$ANALYSIS_DIR/issues.txt"
        fi
    else
        echo "  ⚠️  No pyproject.toml found"
        echo "Missing pyproject.toml" >> "$ANALYSIS_DIR/issues.txt"
    fi
    
    # Check for slash commands (Claude projects)
    if [ -f CLAUDE.md ] || grep -qiE "claude|assistant|cli|command" README.md 2>/dev/null; then
        echo "  🔍 Checking slash commands..."
        if grep -qE "/[a-zA-Z]+" README.md CLAUDE.md 2>/dev/null; then
            echo "    ✅ Slash commands documented"
        else
            echo "    ⚠️  No slash commands documented"
            echo "Missing slash command documentation" >> "$ANALYSIS_DIR/issues.txt"
        fi
        
        if find . -name "*.py" -type f | xargs grep -l "handle_command\|command_handler\|slash_command\|@command" 2>/dev/null | head -1 > /dev/null; then
            echo "    ✅ Command handlers found"
        else
            echo "    ❌ No command handlers found"
            echo "Missing command handler implementation" >> "$ANALYSIS_DIR/issues.txt"
        fi
    fi
    
    # Check for MCP implementation
    if [[ "$PROJECT_NAME" == *"mcp"* ]] || grep -qiE "mcp|model.*context.*protocol" README.md pyproject.toml 2>/dev/null; then
        echo "  🔍 Checking MCP implementation..."
        
        if [ -f "mcp.json" ] || [ -f "server.json" ] || [ -f ".mcp/config.json" ]; then
            echo "    ✅ MCP configuration found"
        else
            echo "    ❌ No MCP configuration file"
            echo "Missing MCP configuration file" >> "$ANALYSIS_DIR/issues.txt"
        fi
        
        # Check for required methods
        for method in "handle_request" "handle_response" "get_capabilities" "initialize"; do
            if find . -name "*.py" -type f | xargs grep -q "def $method" 2>/dev/null; then
                echo "    ✅ Method $method found"
            else
                echo "    ❌ Method $method missing"
                echo "Missing MCP method: $method" >> "$ANALYSIS_DIR/issues.txt"
            fi
        done
    fi
    
    # Run ripgrep analysis if available
    if command -v rg &> /dev/null; then
        echo "  📊 Running code analysis..."
        rg --files > "$ANALYSIS_DIR/all_files.txt" 2>/dev/null || true
        rg -t py "TODO|FIXME|HACK" > "$ANALYSIS_DIR/technical_debt.txt" 2>/dev/null || true
        rg --files -g "*.py" -g "!src/**" -g "!tests/**" -g "!setup.py" -g "!conf*.py" > "$ANALYSIS_DIR/misplaced_python_files.txt" 2>/dev/null || true
    fi
    
    # Phase 3: Run tests
    echo "🧪 Running tests..."
    TEST_EXIT_CODE=0
    if [ -d tests ]; then
        if command -v pytest &> /dev/null; then
            pytest -v tests/ --cov=src/ --cov-report=json > "$ANALYSIS_DIR/test_results.log" 2>&1 || TEST_EXIT_CODE=$?
            
            if [ $TEST_EXIT_CODE -eq 0 ]; then
                echo "  ✅ Tests passed"
            else
                echo "  ❌ Tests failed (exit code: $TEST_EXIT_CODE)"
                PROJECT_SUCCESS=false
            fi
        else
            echo "  ⚠️  pytest not installed"
        fi
    else
        echo "  ⚠️  No tests directory found"
    fi
    
    # Phase 4: Commit or rollback
    if [ $TEST_EXIT_CODE -eq 0 ] && [ "$PROJECT_SUCCESS" = true ]; then
        echo "✅ Committing changes..."
        git add -A 2>/dev/null
        git commit -m "Automated cleanup: structure, imports, and dependencies" 2>/dev/null || echo "  No changes to commit"
        SUCCESSFUL_PROJECTS=$((SUCCESSFUL_PROJECTS + 1))
    else
        echo "⚠️  Rolling back changes..."
        git checkout main 2>/dev/null || git checkout master 2>/dev/null
        git branch -D "$CLEANUP_BRANCH" 2>/dev/null
        FAILED_PROJECTS=$((FAILED_PROJECTS + 1))
    fi
    
    # Save project status
    if [ "$PROJECT_SUCCESS" = true ]; then
        echo "SUCCESS" > "$ANALYSIS_DIR/status.txt"
    else
        echo "FAILED" > "$ANALYSIS_DIR/status.txt"
    fi
    
    cd - > /dev/null
done

echo ""
echo "================================================"
echo "Cleanup Complete!"
echo "================================================"
echo "Total projects: $TOTAL_PROJECTS"
echo "Successful: $SUCCESSFUL_PROJECTS"
echo "Failed: $FAILED_PROJECTS"
echo ""
echo "Reports saved to: $REPORT_DIR/$TIMESTAMP-*"
echo ""

# Generate summary report
SUMMARY_REPORT="$REPORT_DIR/cleanup_summary_$TIMESTAMP.md"
{
    echo "# Project Cleanup Summary"
    echo "Generated: $(date)"
    echo ""
    echo "## Summary"
    echo "- Total projects: $TOTAL_PROJECTS"
    echo "- Successful: $SUCCESSFUL_PROJECTS"
    echo "- Failed: $FAILED_PROJECTS"
    echo ""
    echo "## Projects Processed"
    for PROJECT in "${PROJECTS[@]}"; do
        PROJECT_NAME=$(basename "$PROJECT")
        STATUS_FILE="$REPORT_DIR/$TIMESTAMP-$PROJECT_NAME/status.txt"
        if [ -f "$STATUS_FILE" ]; then
            STATUS=$(cat "$STATUS_FILE")
            if [ "$STATUS" = "SUCCESS" ]; then
                echo "- ✅ $PROJECT"
            else
                echo "- ❌ $PROJECT"
            fi
        else
            echo "- ⚠️  $PROJECT (not processed)"
        fi
        
        # Include issues if any
        ISSUES_FILE="$REPORT_DIR/$TIMESTAMP-$PROJECT_NAME/issues.txt"
        if [ -f "$ISSUES_FILE" ] && [ -s "$ISSUES_FILE" ]; then
            echo "  Issues:"
            while IFS= read -r issue; do
                echo "    - $issue"
            done < "$ISSUES_FILE"
        fi
    done
} > "$SUMMARY_REPORT"

echo "Summary report: $SUMMARY_REPORT"

# Display the summary
cat "$SUMMARY_REPORT"
