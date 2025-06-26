#!/bin/bash
# Fix all projects to use Python 3.10.11 with uv as per CLAUDE.md requirements

echo "🔧 Fixing ALL Projects to Python 3.10.11 with uv"
echo "============================================================"
echo "This follows CLAUDE.md requirements:"
echo "- ALL projects MUST use Python 3.10.11"
echo "- ALL package management MUST use uv"
echo "- NO pip allowed"
echo "============================================================"

# All Granger projects
projects=(
    "/home/graham/workspace/experiments/granger_hub"
    "/home/graham/workspace/experiments/rl_commons"
    "/home/graham/workspace/experiments/claude-test-reporter"
    "/home/graham/workspace/experiments/world_model"
    "/home/graham/workspace/experiments/sparta"
    "/home/graham/workspace/experiments/marker"
    "/home/graham/workspace/experiments/arangodb"
    "/home/graham/workspace/experiments/llm_call"
    "/home/graham/workspace/experiments/unsloth_wip"
    "/home/graham/workspace/experiments/youtube_transcripts"
    "/home/graham/workspace/experiments/darpa_crawl"
    "/home/graham/workspace/experiments/gitget"
    "/home/graham/workspace/mcp-servers/arxiv-mcp-server"
    "/home/graham/workspace/experiments/mcp-screenshot"
    "/home/graham/workspace/experiments/chat"
    "/home/graham/workspace/experiments/annotator"
    "/home/graham/workspace/experiments/aider-daemon"
    "/home/graham/workspace/experiments/runpod_ops"
    "/home/graham/workspace/granger-ui"
)

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ ERROR: uv is not installed!"
    echo "Install it first: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Process each project
for project in "${projects[@]}"; do
    project_name=$(basename "$project")
    
    if [ ! -d "$project" ]; then
        echo -e "\n❌ Skipping $project_name: directory does not exist"
        continue
    fi
    
    echo -e "\n📦 Processing $project_name..."
    cd "$project"
    
    # Check current Python version if venv exists
    if [ -d ".venv" ] || [ -d "venv" ] || [ -d "env" ]; then
        current_version="unknown"
        if [ -d ".venv" ] && [ -f ".venv/bin/python" ]; then
            current_version=$(.venv/bin/python --version 2>&1 | cut -d' ' -f2)
        elif [ -d "venv" ] && [ -f "venv/bin/python" ]; then
            current_version=$(venv/bin/python --version 2>&1 | cut -d' ' -f2)
        elif [ -d "env" ] && [ -f "env/bin/python" ]; then
            current_version=$(env/bin/python --version 2>&1 | cut -d' ' -f2)
        fi
        echo "  Current Python: $current_version"
        
        if [ "$current_version" = "3.10.11" ]; then
            echo "  ✅ Already using Python 3.10.11"
            continue
        fi
    fi
    
    # Remove old venv
    echo "  Removing old virtual environment..."
    rm -rf .venv venv env
    
    # Create new venv with Python 3.10.11
    echo "  Creating new venv with Python 3.10.11..."
    uv venv --python=3.10.11
    
    if [ $? -ne 0 ]; then
        echo "  ❌ Failed to create venv with Python 3.10.11"
        echo "  Make sure Python 3.10.11 is installed on your system"
        continue
    fi
    
    # Install dependencies
    echo "  Installing dependencies with uv..."
    
    # Check for different dependency files
    if [ -f "pyproject.toml" ]; then
        uv sync
    elif [ -f "requirements.txt" ]; then
        source .venv/bin/activate
        uv pip install -r requirements.txt
        deactivate
    else
        echo "  ⚠️  No dependency file found (pyproject.toml or requirements.txt)"
    fi
    
    # Install pytest-json-report if not already in dependencies
    echo "  Ensuring pytest-json-report is installed..."
    source .venv/bin/activate
    uv pip install pytest-json-report
    deactivate
    
    # Verify installation
    echo "  Verifying installation..."
    .venv/bin/python --version
    
    echo "  ✅ Done with $project_name"
done

echo -e "\n✨ Python version fixes complete!"
echo "All projects should now use Python 3.10.11 with uv"

# Summary check
echo -e "\n📊 Verification Summary:"
for project in "${projects[@]}"; do
    if [ -d "$project" ]; then
        project_name=$(basename "$project")
        if [ -f "$project/.venv/bin/python" ]; then
            version=$("$project/.venv/bin/python" --version 2>&1 | cut -d' ' -f2)
            if [ "$version" = "3.10.11" ]; then
                echo "  ✅ $project_name: $version"
            else
                echo "  ❌ $project_name: $version (WRONG VERSION!)"
            fi
        else
            echo "  ⚠️  $project_name: No .venv found"
        fi
    fi
done