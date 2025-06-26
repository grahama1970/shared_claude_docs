#!/bin/bash

# Simple wrapper to run all tests with claude-test-reporter

echo "🧪 Running all project tests with claude-test-reporter"
echo "=================================================="

cd "$(dirname "$0")"

# Run the test runner
python3 run_all_tests_with_reporter.py

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests completed successfully!"
    echo "📊 Check test_reports/ for detailed results"
else
    echo ""
    echo "❌ Some tests failed or encountered errors"
    echo "📊 Check test_reports/ for details"
    exit 1
fi