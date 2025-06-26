#!/bin/bash

echo "=== Verifying arangodb pyproject.toml ==="

cd /home/graham/workspace/experiments/arangodb

echo "Checking for syntax issues in pyproject.toml..."
echo ""

# Check line 70 and surrounding lines
echo "Lines 68-75 of pyproject.toml:"
sed -n '68,75p' pyproject.toml | cat -n

# Check for the specific issue
if grep -q '\[project\.scripts\]"' pyproject.toml; then
    echo ""
    echo "❌ Found issue: [project.scripts]\" instead of [project.scripts]"
    echo "Fixing..."
    
    # Fix all section headers
    sed -i 's/\[project\.scripts\]"/[project.scripts]/' pyproject.toml
    sed -i 's/\[project\.optional-dependencies\]"/[project.optional-dependencies]/' pyproject.toml
    sed -i 's/\[build-system\]"/[build-system]/' pyproject.toml
    sed -i 's/\[tool\.\([^]]*\)\]"/[tool.\1]/g' pyproject.toml
    
    echo "Fixed! New content:"
    sed -n '68,75p' pyproject.toml | cat -n
    
    # Validate
    echo ""
    echo "Validating fixed TOML..."
    python3 -c "import toml; toml.load(open('pyproject.toml'))" && echo "✅ TOML is valid!" || echo "❌ TOML still has issues"
else
    echo ""
    echo "✅ No stray quotes found in section headers"
    
    # Try to validate anyway
    echo "Validating TOML..."
    python3 -c "import toml; toml.load(open('pyproject.toml'))" && echo "✅ TOML is valid!" || echo "❌ TOML has issues"
fi

cd /home/graham/workspace/shared_claude_docs