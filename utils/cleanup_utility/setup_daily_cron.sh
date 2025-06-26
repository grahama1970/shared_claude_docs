#!/bin/bash

# Setup script for daily automated cleanup runs

echo "🕐 Setting up daily automated cleanup..."
echo "========================================"

# Create log directory
LOG_DIR="/home/graham/workspace/shared_claude_docs/utils/cleanup_utility/daily_logs"
mkdir -p "$LOG_DIR"

# Create the cron job script
CRON_SCRIPT="/home/graham/workspace/shared_claude_docs/utils/cleanup_utility/daily_cleanup_cron.sh"
cat > "$CRON_SCRIPT" << 'EOF'
#!/bin/bash

# Daily cleanup script for Claude companion projects
# Runs at 6 AM every day

# Set up environment
export PATH="/home/graham/.local/bin:$PATH"
export PYTHONPATH=""

# Log file with date
LOG_FILE="/home/graham/workspace/shared_claude_docs/utils/cleanup_utility/daily_logs/cleanup_$(date +%Y%m%d).log"

# Change to cleanup utility directory
cd /home/graham/workspace/shared_claude_docs/utils/cleanup_utility

# Start logging
echo "========================================" >> "$LOG_FILE"
echo "Daily Cleanup Run: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Run the cleanup utility with scenarios
python enhanced_cleanup_v4.py \
    --config cleanup_config_localhost.json \
    --scenarios \
    >> "$LOG_FILE" 2>&1

# Check exit status
if [ $? -eq 0 ]; then
    echo "✅ Cleanup completed successfully at $(date)" >> "$LOG_FILE"
else
    echo "❌ Cleanup failed at $(date)" >> "$LOG_FILE"
fi

# Rotate logs (keep last 30 days)
find /home/graham/workspace/shared_claude_docs/utils/cleanup_utility/daily_logs \
    -name "cleanup_*.log" -mtime +30 -delete

# Optional: Send notification (uncomment and configure as needed)
# mail -s "Daily Cleanup Report $(date +%Y-%m-%d)" your@email.com < "$LOG_FILE"
EOF

# Make the script executable
chmod +x "$CRON_SCRIPT"

# Check if cron job already exists
CRON_EXISTS=$(crontab -l 2>/dev/null | grep -c "daily_cleanup_cron.sh")

if [ "$CRON_EXISTS" -eq 0 ]; then
    # Add the cron job
    echo "Adding cron job..."
    (crontab -l 2>/dev/null; echo "0 6 * * * $CRON_SCRIPT") | crontab -
    echo "✅ Cron job added successfully!"
else
    echo "ℹ️  Cron job already exists"
fi

# Show current crontab
echo ""
echo "Current crontab entries:"
echo "========================"
crontab -l | grep -E "(cleanup|daily)" || echo "No cleanup-related entries found"

echo ""
echo "✅ Daily cleanup automation setup complete!"
echo ""
echo "The cleanup will run automatically at 6 AM every day."
echo "Logs will be saved to: $LOG_DIR"
echo ""
echo "To monitor the cron job:"
echo "  - View logs: ls -la $LOG_DIR"
echo "  - Check cron status: systemctl status cron"
echo "  - View crontab: crontab -l"
echo "  - Remove cron job: crontab -e (then delete the line)"
echo ""
echo "To test the cron script manually:"
echo "  $CRON_SCRIPT"