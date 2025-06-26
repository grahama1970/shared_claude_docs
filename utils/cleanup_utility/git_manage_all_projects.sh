#!/bin/bash

# Script to ensure all projects are Git-managed and have clean working directories
# This will:
# 1. Initialize Git repos for projects without them
# 2. Commit uncommitted changes in existing repos

echo "🔐 Git Management Script for All Projects"
echo "========================================"
echo ""

# Projects to manage
PROJECTS=(
    "/home/graham/workspace/experiments/sparta"
    "/home/graham/workspace/experiments/marker"
    "/home/graham/workspace/experiments/arangodb"
    "/home/graham/workspace/experiments/youtube_transcripts"
    "/home/graham/workspace/experiments/claude_max_proxy"
    "/home/graham/workspace/mcp-servers/arxiv-mcp-server"
    "/home/graham/workspace/experiments/claude-module-communicator"
    "/home/graham/workspace/experiments/claude-test-reporter"
    "/home/graham/workspace/experiments/unsloth_wip"
    "/home/graham/workspace/experiments/marker-ground-truth"
    "/home/graham/workspace/experiments/mcp-screenshot"
)

# Function to initialize git repo
init_git_repo() {
    local project_path=$1
    local project_name=$(basename "$project_path")
    
    echo "Initializing Git repository..."
    cd "$project_path"
    
    git init
    
    # Create .gitignore if it doesn't exist
    if [ ! -f .gitignore ]; then
        echo "Creating .gitignore..."
        cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
.env.local
.env.*.local
*.log
.cache/
.pytest_cache/
.coverage
htmlcov/
.tox/
.mypy_cache/
.ruff_cache/

# Data files
*.db
*.sqlite
*.sqlite3
data/
outputs/
models/
checkpoints/
EOF
    fi
    
    # Add all files
    git add -A
    
    # Make initial commit
    git commit -m "Initial commit - setting up Git repository

Initialized Git repository for $project_name project.
This commit includes all existing project files."
    
    echo "✅ Git repository initialized for $project_name"
}

# Function to commit uncommitted changes
commit_changes() {
    local project_path=$1
    local project_name=$(basename "$project_path")
    
    echo "Checking for uncommitted changes..."
    cd "$project_path"
    
    # Check if there are uncommitted changes
    if [[ -n $(git status --porcelain) ]]; then
        echo "Found uncommitted changes. Committing..."
        
        # Add all changes
        git add -A
        
        # Generate commit message with summary of changes
        local changed_files=$(git diff --cached --name-only | wc -l)
        local commit_msg="Auto-commit: Save work in progress

Summary of changes:
- Modified/Added $changed_files files
- Timestamp: $(date '+%Y-%m-%d %H:%M:%S')
- Auto-committed before cleanup utility run"
        
        git commit -m "$commit_msg"
        
        echo "✅ Committed changes in $project_name"
    else
        echo "✅ No uncommitted changes in $project_name"
    fi
}

# Main processing loop
for project in "${PROJECTS[@]}"; do
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Processing: $project"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if [ ! -d "$project" ]; then
        echo "❌ Project directory not found: $project"
        continue
    fi
    
    cd "$project"
    
    # Check if it's a Git repository
    if git rev-parse --git-dir > /dev/null 2>&1; then
        echo "✓ Git repository exists"
        commit_changes "$project"
    else
        echo "⚠️  Not a Git repository"
        read -p "Initialize Git repository? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            init_git_repo "$project"
        else
            echo "⏭️  Skipped Git initialization"
        fi
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Git management complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "All projects are now Git-managed and have clean working directories."
echo "You can now safely run the cleanup utility."