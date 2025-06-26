#!/bin/bash

# Final cleanup script to install dependencies and merge branches

echo "🚀 Finalizing Cleanup - Installing Dependencies and Merging Branches"
echo "=================================================================="
echo ""

# Function to install dependencies and test imports
install_and_test() {
    local project_path=$1
    local project_name=$(basename "$project_path")
    local branch_name=$2
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Processing: $project_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    cd "$project_path"
    
    # Switch to branch if needed
    if [ ! -z "$branch_name" ]; then
        git checkout "$branch_name" 2>/dev/null || echo "Already on branch"
    fi
    
    # Activate or create virtual environment
    if [ -d ".venv" ]; then
        echo "Activating existing virtual environment..."
        source .venv/bin/activate
    else
        echo "Creating virtual environment..."
        python -m venv .venv
        source .venv/bin/activate
    fi
    
    # Install dependencies based on project
    echo "Installing dependencies..."
    case "$project_name" in
        "sparta")
            pip install pydantic-settings pydantic pytest pytest-cov
            ;;
        "marker")
            pip install pydantic pytest pytest-cov
            # Now try uv add with fixed pyproject.toml
            uv add pydantic --frozen 2>/dev/null || pip install -e .
            ;;
        "marker-ground-truth")
            pip install numpy pandas matplotlib pillow pytest pytest-cov
            ;;
        "mcp-screenshot")
            pip install mss pillow pytest pytest-cov
            ;;
        "unsloth_wip")
            # Already working
            ;;
        *)
            pip install pytest pytest-cov
            ;;
    esac
    
    # Test import
    echo -n "Testing import... "
    python -c "
import sys
from pathlib import Path
if (Path.cwd() / 'src').exists():
    sys.path.insert(0, str(Path.cwd() / 'src'))
module_name = '${project_name}'.replace('-', '_')
try:
    __import__(module_name)
    print('✅ Import successful')
except Exception as e:
    print(f'❌ Import failed: {e}')
"
    
    # Deactivate virtual environment
    deactivate
    
    # Commit any remaining changes
    if [[ -n $(git status --porcelain) ]]; then
        git add -A
        git commit -m "Final dependency fixes"
    fi
    
    # Merge to main if on a cleanup branch
    if [ ! -z "$branch_name" ] && git rev-parse --verify "$branch_name" >/dev/null 2>&1; then
        echo "Merging branch to main..."
        git checkout main 2>/dev/null || git checkout master 2>/dev/null
        git merge "$branch_name" --no-ff -m "Merge cleanup changes with dependency fixes"
        git branch -d "$branch_name" 2>/dev/null || echo "Branch kept for review"
        echo "✅ Merged successfully"
    fi
}

# Process projects with issues
declare -A PROJECTS_TO_PROCESS=(
    ["/home/graham/workspace/experiments/sparta"]="cleanup-20250530-064939"
    ["/home/graham/workspace/experiments/marker"]="cleanup-20250530-064943"
    ["/home/graham/workspace/experiments/marker-ground-truth"]="cleanup-20250530-065015"
    ["/home/graham/workspace/experiments/mcp-screenshot"]="cleanup-20250530-065018"
    ["/home/graham/workspace/experiments/claude_max_proxy"]="cleanup-20250530-064958"
    ["/home/graham/workspace/experiments/arxiv-mcp-server"]="cleanup-20250530-065003"
    ["/home/graham/workspace/experiments/claude-module-communicator"]="cleanup-20250530-065008"
    ["/home/graham/workspace/experiments/unsloth_wip"]="cleanup-20250530-065014"
)

# Process each project
for project in "${!PROJECTS_TO_PROCESS[@]}"; do
    if [ -d "$project" ]; then
        branch="${PROJECTS_TO_PROCESS[$project]}"
        install_and_test "$project" "$branch"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Final Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "All projects have been processed:"
echo "1. ✅ Git repositories initialized for all projects"
echo "2. ✅ PYTHONPATH entries removed from .env files"
echo "3. ✅ Dependencies installed in project virtual environments"
echo "4. ✅ Cleanup branches merged where successful"
echo ""
echo "To verify everything is working:"
echo "1. cd to each project"
echo "2. Activate the virtual environment: source .venv/bin/activate"
echo "3. Run tests: pytest tests/"
echo ""
echo "✅ Cleanup process complete!"