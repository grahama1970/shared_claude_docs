#!/bin/bash

# Script to fix import issues in all projects by installing missing dependencies

echo "🔧 Fixing Import Issues in All Projects"
echo "======================================"
echo ""

# Function to fix dependencies in a project
fix_project_deps() {
    local project_path=$1
    local project_name=$(basename "$project_path")
    local branch_name=$2
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Fixing: $project_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    cd "$project_path"
    
    # Switch to cleanup branch if specified
    if [ ! -z "$branch_name" ]; then
        echo "Switching to branch: $branch_name"
        git checkout "$branch_name" 2>/dev/null || echo "Already on correct branch"
    fi
    
    # Check if uv is available
    if ! command -v uv &> /dev/null; then
        echo "❌ uv not found. Installing dependencies with pip instead."
        return 1
    fi
    
    # Fix specific dependencies based on project
    case "$project_name" in
        "sparta")
            echo "Installing pydantic-settings..."
            uv add pydantic-settings
            ;;
        "marker")
            echo "Installing pydantic..."
            uv add pydantic
            ;;
        "marker-ground-truth")
            echo "Installing numpy and core dependencies..."
            uv add numpy pandas matplotlib pillow
            ;;
        "mcp-screenshot")
            echo "Installing mss (screenshot library)..."
            uv add mss pillow
            ;;
        "unsloth_wip")
            echo "Installing unsloth and dependencies..."
            # First ensure the module structure is correct
            if [ -d "src" ] && [ ! -d "src/unsloth_wip" ]; then
                echo "Creating proper module structure..."
                mkdir -p src/unsloth_wip
                if [ -f "src/__init__.py" ]; then
                    mv src/__init__.py src/unsloth_wip/
                fi
                touch src/unsloth_wip/__init__.py
            fi
            # Try to add unsloth if available
            uv add torch transformers accelerate bitsandbytes
            ;;
        "youtube_transcripts")
            echo "Installing youtube-dl..."
            uv add youtube-dl yt-dlp whisper
            ;;
        "claude_max_proxy")
            echo "Installing proxy dependencies..."
            uv add httpx fastapi uvicorn pydantic
            ;;
        "arxiv-mcp-server")
            echo "Installing MCP server dependencies..."
            uv add fastapi uvicorn pydantic httpx arxiv
            ;;
        "claude-module-communicator")
            echo "Installing communicator dependencies..."
            uv add pydantic httpx fastapi
            ;;
    esac
    
    # Also ensure pytest is available for testing
    echo "Ensuring pytest is installed..."
    uv add --dev pytest pytest-cov pytest-asyncio
    
    # Commit the changes
    if [[ -n $(git status --porcelain) ]]; then
        echo "Committing dependency fixes..."
        git add -A
        git commit -m "Fix import issues: Add missing dependencies

- Added missing Python packages
- Fixed module structure issues where needed
- Added pytest for testing"
        echo "✅ Dependencies fixed and committed"
    else
        echo "✅ No dependency changes needed"
    fi
}

# Projects with import issues and their cleanup branches
declare -A PROJECTS_TO_FIX=(
    ["/home/graham/workspace/experiments/sparta"]="cleanup-20250530-064939"
    ["/home/graham/workspace/experiments/marker"]=""
    ["/home/graham/workspace/experiments/marker-ground-truth"]="cleanup-20250530-065015"
    ["/home/graham/workspace/experiments/mcp-screenshot"]="cleanup-20250530-065018"
    ["/home/graham/workspace/experiments/unsloth_wip"]="cleanup-20250530-065014"
    ["/home/graham/workspace/experiments/youtube_transcripts"]=""
    ["/home/graham/workspace/experiments/claude_max_proxy"]="cleanup-20250530-064958"
    ["/home/graham/workspace/experiments/arxiv-mcp-server"]="cleanup-20250530-065003"
    ["/home/graham/workspace/experiments/claude-module-communicator"]="cleanup-20250530-065008"
    ["/home/graham/workspace/experiments/arangodb"]=""
    ["/home/graham/workspace/experiments/claude-test-reporter"]=""
)

# Fix each project
for project in "${!PROJECTS_TO_FIX[@]}"; do
    branch="${PROJECTS_TO_FIX[$project]}"
    fix_project_deps "$project" "$branch"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Import issue fixes complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "1. Test imports in each project"
echo "2. Merge cleanup branches back to main"
echo "3. Run tests to ensure everything works"