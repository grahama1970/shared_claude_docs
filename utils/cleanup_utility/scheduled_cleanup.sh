#!/bin/bash

# Scheduled Cleanup Script - Safe for automation
# This runs in READ-ONLY mode and sends reports

set -e

# Configuration
REPORT_EMAIL="your-email@example.com"
WEBHOOK_URL=""  # Optional: Slack/Discord webhook
LOG_DIR="/home/graham/logs/cleanup_reports"
CLEANUP_DIR="/home/graham/workspace/shared_claude_docs/utils/cleanup_utility"

# Create log directory
mkdir -p "$LOG_DIR"

# Timestamp
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOG_FILE="$LOG_DIR/cleanup_${TIMESTAMP}.log"

echo "Starting scheduled cleanup check at $(date)" > "$LOG_FILE"

# Change to cleanup directory
cd "$CLEANUP_DIR"

# Run in DRY-RUN mode only - no changes!
./run_enhanced_cleanup.sh --dry-run >> "$LOG_FILE" 2>&1

# Check if there were any critical issues
CRITICAL_ISSUES=$(grep -c "❌" "$CLEANUP_DIR/cleanup_reports/comprehensive_report_"*.md 2>/dev/null | tail -1 | cut -d: -f2 || echo "0")
WARNINGS=$(grep -c "⚠️" "$CLEANUP_DIR/cleanup_reports/comprehensive_report_"*.md 2>/dev/null | tail -1 | cut -d: -f2 || echo "0")

# Get the latest report
LATEST_REPORT=$(ls -t "$CLEANUP_DIR/cleanup_reports/comprehensive_report_"*.md 2>/dev/null | head -1)

# Create summary
{
    echo "# Cleanup Report Summary - $(date)"
    echo ""
    echo "- Critical Issues: $CRITICAL_ISSUES"
    echo "- Warnings: $WARNINGS"
    echo ""
    echo "## Projects with Issues:"
    grep -A5 "❌" "$LATEST_REPORT" 2>/dev/null | grep "###" | sed 's/### /- /' || echo "None"
    echo ""
    echo "Full report: $LATEST_REPORT"
} > "$LOG_DIR/summary_${TIMESTAMP}.txt"

# Optional: Send notification if issues found
if [ "$CRITICAL_ISSUES" -gt 0 ]; then
    echo "⚠️ Critical issues found in project cleanup check" >> "$LOG_FILE"
    
    # Email notification (requires mail/sendmail configured)
    if [ -n "$REPORT_EMAIL" ] && command -v mail &> /dev/null; then
        cat "$LOG_DIR/summary_${TIMESTAMP}.txt" | mail -s "Project Cleanup: $CRITICAL_ISSUES Critical Issues" "$REPORT_EMAIL"
    fi
    
    # Webhook notification (Slack/Discord)
    if [ -n "$WEBHOOK_URL" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"🚨 Project Cleanup: $CRITICAL_ISSUES critical issues found\"}" \
            "$WEBHOOK_URL" 2>/dev/null || true
    fi
fi

echo "Cleanup check completed at $(date)" >> "$LOG_FILE"

# Cleanup old logs (keep last 30 days)
find "$LOG_DIR" -name "cleanup_*.log" -mtime +30 -delete 2>/dev/null || true
find "$LOG_DIR" -name "summary_*.txt" -mtime +30 -delete 2>/dev/null || true

exit 0