#!/bin/bash

echo "=== Checking numpy requirements across packages ==="

# Check arangodb requirements
echo "arangodb numpy requirement:"
cd /home/graham/workspace/experiments/arangodb
grep -A5 -B5 "numpy" pyproject.toml | grep -E "numpy|dependencies"

echo ""
echo "aider-daemon numpy requirement:"
cd /home/graham/workspace/experiments/aider-daemon
grep -A5 -B5 "numpy" pyproject.toml | grep -E "numpy|dependencies" || echo "Not found in pyproject.toml"

echo ""
echo "marker numpy requirement:"
cd /home/graham/workspace/experiments/marker
grep -A5 -B5 "numpy" pyproject.toml | grep -E "numpy|dependencies"

cd /home/graham/workspace/shared_claude_docs