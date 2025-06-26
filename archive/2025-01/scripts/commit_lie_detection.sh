#!/bin/bash
# Commit and push lie detection enhancements to claude-test-reporter

set -e

echo "📦 Committing lie detection enhancements to claude-test-reporter..."

# Navigate to claude-test-reporter
cd /home/graham/workspace/experiments/claude-test-reporter

# Add all changes
git add -A

# Create detailed commit message
git commit -m "feat: Add comprehensive lie detection analyzers to prevent test deception

- Add MockDetector to identify inappropriate mock usage in integration tests
- Add RealTimeTestMonitor to force actual test execution and catch instant-pass tests  
- Add ImplementationVerifier to detect skeleton code and empty functions
- Add HoneypotEnforcer to ensure honeypot tests fail as designed
- Add IntegrationTester for real module communication testing
- Add PatternAnalyzer to detect repeated deception patterns
- Add ClaimVerifier to cross-check claims against implementations
- Enhance HallucinationMonitor with Claude-specific detection
- Add ComprehensiveAnalyzer to orchestrate all analyzers
- Create EnhancedMultiProjectDashboard with trust scores and deception metrics
- Add comprehensive test suite for all analyzers
- Integrate with granger-verify command for automatic lie detection
- Add detailed documentation in docs/lie_detection_guide.md

This system detects when Claude (or other AI) lies about:
- Tests passing when they don't
- Features being implemented when they're skeleton code
- Integration tests using mocks instead of real components
- Honeypot tests being manipulated to pass
- Instant test completion indicating fake testing

Trust scores and deception metrics are calculated and displayed in dashboards.

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
"

# Push to remote
echo "🚀 Pushing to remote repository..."
git push

echo "✅ Changes committed and pushed successfully!"

# Return to shared_claude_docs
cd /home/graham/workspace/shared_claude_docs

echo ""
echo "📦 Installing claude-test-reporter in editable mode..."
uv pip install -e /home/graham/workspace/experiments/claude-test-reporter

echo ""
echo "🧪 Testing imports..."
python -c "
from claude_test_reporter.analyzers.mock_detector import MockDetector
from claude_test_reporter.analyzers.realtime_monitor import RealTimeTestMonitor
from claude_test_reporter.analyzers.implementation_verifier import ImplementationVerifier
from claude_test_reporter.analyzers.honeypot_enforcer import HoneypotEnforcer
from claude_test_reporter.analyzers.comprehensive_analyzer import ComprehensiveAnalyzer
print('✅ All analyzer imports successful!')
"

echo ""
echo "🎉 Lie detection system successfully integrated!"