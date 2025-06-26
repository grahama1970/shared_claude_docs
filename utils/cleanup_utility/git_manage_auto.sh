#!/bin/bash

# Automated Git management script - no user interaction required
# Automatically initializes Git repos and commits changes

echo "🔐 Automated Git Management for All Projects"
echo "==========================================="
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

# Track statistics
REPOS_INITIALIZED=0
COMMITS_MADE=0
ALREADY_CLEAN=0
ERRORS=0

# Function to initialize git repo
init_git_repo() {
    local project_path=$1
    local project_name=$(basename "$project_path")
    
    echo "  Initializing Git repository..."
    cd "$project_path"
    
    git init > /dev/null 2>&1
    
    # Create .gitignore if it doesn't exist
    if [ ! -f .gitignore ]; then
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
    git add -A > /dev/null 2>&1
    
    # Make initial commit
    git commit -m "Initial commit - setting up Git repository

Initialized Git repository for $project_name project.
This commit includes all existing project files.
Automated by git_manage_auto.sh" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "  ✅ Git repository initialized"
        ((REPOS_INITIALIZED++))
    else
        echo "  ❌ Failed to initialize Git repository"
        ((ERRORS++))
    fi
}

# Function to commit uncommitted changes
commit_changes() {
    local project_path=$1
    local project_name=$(basename "$project_path")
    
    cd "$project_path"
    
    # Check if there are uncommitted changes
    if [[ -n $(git status --porcelain 2>/dev/null) ]]; then
        echo "  Found uncommitted changes. Committing..."
        
        # Add all changes
        git add -A > /dev/null 2>&1
        
        # Generate commit message with summary of changes
        local changed_files=$(git diff --cached --name-only 2>/dev/null | wc -l)
        local commit_msg="Auto-commit: Pre-cleanup checkpoint

Summary of changes:
- Modified/Added $changed_files files
- Timestamp: $(date '+%Y-%m-%d %H:%M:%S')
- Auto-committed by cleanup utility preparation"
        
        git commit -m "$commit_msg" > /dev/null 2>&1
        
        if [ $? -eq 0 ]; then
            echo "  ✅ Changes committed ($changed_files files)"
            ((COMMITS_MADE++))
        else
            echo "  ❌ Failed to commit changes"
            ((ERRORS++))
        fi
    else
        echo "  ✅ Working directory clean"
        ((ALREADY_CLEAN++))
    fi
}

# Main processing loop
for project in "${PROJECTS[@]}"; do
    project_name=$(basename "$project")
    echo ""
    echo "[$((${#project[@]}))/$((${#PROJECTS[@]}))] Processing: $project_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if [ ! -d "$project" ]; then
        echo "  ❌ Directory not found"
        ((ERRORS++))
        continue
    fi
    
    cd "$project"
    
    # Check if it's a Git repository
    if git rev-parse --git-dir > /dev/null 2>&1; then
        echo "  ✓ Git repository exists"
        commit_changes "$project"
    else
        echo "  ⚠️  Not a Git repository"
        init_git_repo "$project"
    fi
done

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Total projects:        ${#PROJECTS[@]}"
echo "  Repos initialized:     $REPOS_INITIALIZED"
echo "  Commits made:          $COMMITS_MADE"
echo "  Already clean:         $ALREADY_CLEAN"
echo "  Errors:                $ERRORS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✅ All projects are now Git-managed with clean working directories!"
    echo "   You can safely run the cleanup utility."
    exit 0
else
    echo "⚠️  Some operations failed. Please check the output above."
    exit 1
fi