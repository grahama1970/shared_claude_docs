#!/bin/bash

# Enhanced Cleanup Utility v3 Runner (Git-Safe Version)
# Runs the enhanced cleanup utility with Git safety measures

echo "🚀 Enhanced Project Cleanup Utility v3 (Git-Safe)"
echo "================================================"
echo ""
echo "This version includes Git safety features:"
echo "- Creates safety tags before making changes"
echo "- Works in feature branches"
echo "- Only merges if cleanup is successful"
echo "- Skips projects with uncommitted changes"
echo ""

# Set the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if we should use localhost config
if [[ "$1" == "--localhost" ]]; then
    CONFIG_FILE="cleanup_config_localhost.json"
    shift
else
    CONFIG_FILE="cleanup_config.json"
fi

# Default to dry-run mode for safety
DRY_RUN="--dry-run"
VERBOSE=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --live)
            DRY_RUN=""
            echo "⚠️  Running in LIVE mode with Git safety!"
            echo ""
            echo "This will:"
            echo "1. Create safety tags in each repository"
            echo "2. Create feature branches for changes"
            echo "3. Apply fixes to the feature branches"
            echo "4. Merge successful changes back to main branch"
            echo ""
            read -p "Are you sure you want to continue? (yes/no): " confirm
            if [[ "$confirm" != "yes" ]]; then
                echo "Aborted."
                exit 0
            fi
            shift
            ;;
        --verbose|-v)
            VERBOSE="--verbose"
            shift
            ;;
        --sequential)
            SEQUENTIAL="--sequential"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--localhost] [--live] [--verbose] [--sequential]"
            echo "  --localhost   Use localhost configuration"
            echo "  --live        Run in live mode (applies changes with Git safety)"
            echo "  --verbose     Enable verbose output"
            echo "  --sequential  Process projects sequentially (always used in live mode)"
            exit 1
            ;;
    esac
done

# Install dependencies if needed
if ! python -c "import toml" 2>/dev/null; then
    echo "📦 Installing required dependencies..."
    pip install toml tqdm
fi

# Check for git
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. This version requires Git for safety features."
    exit 1
fi

# Run the enhanced cleanup utility v3
echo "Running enhanced cleanup utility v3..."
echo "Config: $CONFIG_FILE"
echo "Mode: ${DRY_RUN:+DRY RUN}${DRY_RUN:-LIVE (Git-Safe)}"
echo ""

# Note: Live mode always runs sequentially for Git operations
if [[ -z "$DRY_RUN" ]]; then
    echo "ℹ️  Live mode requires sequential processing for Git operations"
    SEQUENTIAL="--sequential"
fi

python enhanced_cleanup_v3.py \
    --config "$CONFIG_FILE" \
    $DRY_RUN \
    $VERBOSE \
    $SEQUENTIAL

# Check exit code
EXIT_CODE=$?

if [[ $EXIT_CODE -eq 0 ]]; then
    echo ""
    echo "✅ Cleanup completed successfully!"
    echo ""
    echo "📄 Check the cleanup_reports/ directory for detailed reports:"
    ls -la cleanup_reports/comprehensive_report_*.md | tail -1
    ls -la cleanup_reports/summary_*.txt | tail -1
    
    if [[ -z "$DRY_RUN" ]]; then
        echo ""
        echo "🔐 Git Safety Information:"
        echo "- Each modified project has been tagged with 'pre-cleanup-*'"
        echo "- Changes were made in feature branches"
        echo "- Successful changes were automatically merged"
        echo "- Failed projects remain in their feature branches for review"
        echo ""
        echo "To review changes in a project:"
        echo "  cd /path/to/project"
        echo "  git log --oneline -n 5"
        echo ""
        echo "To rollback changes if needed:"
        echo "  git checkout pre-cleanup-<timestamp>"
    fi
else
    echo ""
    echo "❌ Cleanup completed with errors. Check the reports for details."
fi

exit $EXIT_CODE