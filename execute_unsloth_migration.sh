#!/bin/bash
# Migration script: unsloth_wip → fine_tuning
# Run this from the shared_claude_docs directory

set -e  # Exit on error

echo "=== Migration Script: unsloth_wip → fine_tuning ==="
echo "This script will update all references in the shared_claude_docs repository"
echo ""

# Confirmation
read -p "Are you sure you want to proceed? (y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Migration cancelled."
    exit 0
fi

echo ""
echo "Starting migration..."

# Create backup
echo "1. Creating backup of key files..."
cp docs/GRANGER_PROJECTS.md docs/GRANGER_PROJECTS.md.backup
cp CLAUDE.md CLAUDE.md.backup
cp pyproject.toml pyproject.toml.backup

# Update all occurrences
echo "2. Updating all references to unsloth_wip..."

# Update in markdown files
find . -type f -name "*.md" -not -path "./repos/*" -not -path "./.git/*" -exec sed -i 's/unsloth_wip/fine_tuning/g' {} +

# Update GitHub URLs
find . -type f \( -name "*.md" -o -name "*.toml" -o -name "*.py" \) -not -path "./repos/*" -not -path "./.git/*" -exec sed -i 's|git+https://github.com/grahama1970/unsloth_wip\.git|git+https://github.com/grahama1970/fine_tuning.git|g' {} +

# Update local paths
find . -type f \( -name "*.md" -o -name "*.toml" -o -name "*.py" \) -not -path "./repos/*" -not -path "./.git/*" -exec sed -i 's|/experiments/unsloth_wip/|/experiments/fine_tuning/|g' {} +

# Update Python imports
find . -type f -name "*.py" -not -path "./repos/*" -not -path "./.git/*" -exec sed -i 's/from unsloth_wip/from fine_tuning/g' {} +
find . -type f -name "*.py" -not -path "./repos/*" -not -path "./.git/*" -exec sed -i 's/import unsloth_wip/import fine_tuning/g' {} +

# Special case: Update "Unsloth" standalone references in CLAUDE.md
sed -i 's/\*\*Unsloth:\*\*/\*\*Fine Tuning:\*\*/g' CLAUDE.md

# Update pyproject.toml package name
sed -i 's/"unsloth @/"fine_tuning @/g' pyproject.toml

echo ""
echo "3. Summary of changes:"
echo "   - Updated all markdown files"
echo "   - Updated all Python files"
echo "   - Updated pyproject.toml dependencies"
echo "   - Updated GitHub URLs"
echo "   - Updated local paths"

echo ""
echo "4. Files with changes:"
git diff --name-only | head -20

echo ""
echo "=== Migration Complete! ==="
echo ""
echo "Next steps:"
echo "1. Review the changes: git diff"
echo "2. Navigate to the actual project: cd /home/graham/workspace/experiments/unsloth_wip"
echo "3. Rename the GitHub repo: gh repo rename fine_tuning"
echo "4. Rename the local directory: mv /home/graham/workspace/experiments/unsloth_wip /home/graham/workspace/experiments/fine_tuning"
echo "5. Update the project's own pyproject.toml name field"
echo "6. Commit changes here: git add -A && git commit -m 'Rename unsloth_wip to fine_tuning'"
echo ""
echo "Backup files created:"
echo "  - docs/GRANGER_PROJECTS.md.backup"
echo "  - CLAUDE.md.backup"
echo "  - pyproject.toml.backup"