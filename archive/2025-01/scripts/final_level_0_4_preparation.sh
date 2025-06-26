#!/bin/bash
# Final preparation for Level 0-4 interaction testing

echo "🚀 Final Preparation for Level 0-4 Interaction Testing"
echo "======================================================"

# Install missing dependencies
echo -e "\n📦 Installing missing Python dependencies..."
(cd /home/graham/workspace/experiments/llm_call && uv add litellm)
(cd /home/graham/workspace/experiments/marker && uv add pdftext)
(cd /home/graham/workspace/experiments/annotator && uv add fastapi uvicorn)

# Run final verification
echo -e "\n✅ Running final Granger verification..."
/home/graham/.claude/commands/granger-verify-fix --all --quiet

# Check readiness
echo -e "\n🔍 Checking Level 0-4 readiness..."
python /home/graham/workspace/shared_claude_docs/prepare_for_interaction_testing.py

echo -e "\n✅ Preparation complete!"
echo "You can now run Level 0-4 tests with: ./run_interaction_tests.sh"