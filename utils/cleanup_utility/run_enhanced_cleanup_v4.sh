#!/bin/bash

# Enhanced Cleanup Utility v4 Runner (Auto-Fix Version)
# Runs the enhanced cleanup utility with automatic fixes and daily run capabilities

echo "🚀 Enhanced Project Cleanup Utility v4 (Auto-Fix)"
echo "================================================="
echo ""
echo "This version includes:"
echo "- Automatic Git repository initialization"
echo "- Auto-commit of uncommitted changes"
echo "- Automatic dependency installation"
echo "- TOML syntax error fixes"
echo "- Module structure fixes"
echo "- Optional scenario testing"
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
SCENARIOS=""
NO_AUTO_FIX=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --live)
            DRY_RUN=""
            echo "⚠️  Running in LIVE mode with auto-fixes!"
            echo ""
            echo "This will:"
            echo "1. Initialize Git repos where needed"
            echo "2. Auto-commit any uncommitted changes"
            echo "3. Create safety tags and feature branches"
            echo "4. Apply automated fixes (dependencies, syntax, etc.)"
            echo "5. Merge successful changes back to main"
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
        --scenarios)
            SCENARIOS="--scenarios"
            echo "✅ Will run interaction scenarios after cleanup"
            shift
            ;;
        --no-auto-fix)
            NO_AUTO_FIX="--no-auto-fix"
            echo "⚠️  Auto-fix disabled"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--localhost] [--live] [--verbose] [--sequential] [--scenarios] [--no-auto-fix]"
            echo "  --localhost    Use localhost configuration"
            echo "  --live         Run in live mode (applies changes with auto-fixes)"
            echo "  --verbose      Enable verbose output"
            echo "  --sequential   Process projects sequentially"
            echo "  --scenarios    Run interaction scenarios after cleanup"
            echo "  --no-auto-fix  Disable automatic dependency installation"
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

# Run the enhanced cleanup utility v4
echo "Running enhanced cleanup utility v4..."
echo "Config: $CONFIG_FILE"
echo "Mode: ${DRY_RUN:+DRY RUN}${DRY_RUN:-LIVE (Auto-Fix)}"
echo "Auto-Fix: ${NO_AUTO_FIX:+DISABLED}${NO_AUTO_FIX:-ENABLED}"
echo ""

# Note: Live mode always runs sequentially for Git operations
if [[ -z "$DRY_RUN" ]]; then
    echo "ℹ️  Live mode requires sequential processing for Git operations"
    SEQUENTIAL="--sequential"
fi

python enhanced_cleanup_v4.py \
    --config "$CONFIG_FILE" \
    $DRY_RUN \
    $VERBOSE \
    $SEQUENTIAL \
    $SCENARIOS \
    $NO_AUTO_FIX

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
        echo "- Projects with issues remain in feature branches for review"
        echo ""
        echo "🔧 Auto-Fix Summary:"
        echo "- Missing dependencies were installed automatically"
        echo "- TOML syntax errors were fixed"
        echo "- Module structures were corrected where needed"
        echo "- PYTHONPATH entries were cleaned from .env files"
        echo ""
        echo "To review changes in a project:"
        echo "  cd /path/to/project"
        echo "  git log --oneline -n 5"
        echo ""
        echo "To rollback changes if needed:"
        echo "  git checkout pre-cleanup-<timestamp>"
    fi
    
    if [[ ! -z "$SCENARIOS" ]]; then
        echo ""
        echo "🎭 Scenario test results are included in the comprehensive report"
    fi
else
    echo ""
    echo "❌ Cleanup completed with errors. Check the reports for details."
fi

# Suggest cron setup for daily runs
if [[ -z "$DRY_RUN" ]]; then
    echo ""
    echo "💡 To run this cleanup daily, add to your crontab:"
    echo "   crontab -e"
    echo "   # Add this line for daily cleanup at 6 AM:"
    echo "   0 6 * * * $SCRIPT_DIR/run_enhanced_cleanup_v4.sh --localhost --live --scenarios >> $SCRIPT_DIR/cleanup_daily.log 2>&1"
fi

exit $EXIT_CODE