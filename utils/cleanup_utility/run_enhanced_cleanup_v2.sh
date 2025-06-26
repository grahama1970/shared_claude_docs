#!/bin/bash

# Enhanced Cleanup Utility v2 Runner
# Runs the enhanced cleanup utility with additional dependency and environment fixes

echo "🚀 Enhanced Project Cleanup Utility v2"
echo "========================================"
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
            echo "⚠️  Running in LIVE mode - changes will be applied!"
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
            echo "  --live        Run in live mode (applies changes)"
            echo "  --verbose     Enable verbose output"
            echo "  --sequential  Process projects sequentially"
            exit 1
            ;;
    esac
done

# Install dependencies if needed
if ! python -c "import toml" 2>/dev/null; then
    echo "📦 Installing required dependencies..."
    pip install toml tqdm
fi

# Run the enhanced cleanup utility v2
echo "Running enhanced cleanup utility v2..."
echo "Config: $CONFIG_FILE"
echo "Mode: ${DRY_RUN:+DRY RUN}${DRY_RUN:-LIVE}"
echo ""

python enhanced_cleanup_v2.py \
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
else
    echo ""
    echo "❌ Cleanup completed with errors. Check the reports for details."
fi

exit $EXIT_CODE