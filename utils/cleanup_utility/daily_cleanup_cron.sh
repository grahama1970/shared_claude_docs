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
