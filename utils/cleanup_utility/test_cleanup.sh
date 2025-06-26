#!/bin/bash

echo "Testing Cleanup Utility Setup"
echo "============================"
echo ""

# Check for required files
echo "Checking required files..."
for file in cleanup_config.json requirements.txt simple_cleanup.py install_dependencies.sh run_cleanup_simple.sh; do
    if [ -f "$file" ]; then
        echo "  ✅ $file exists"
    else
        echo "  ❌ $file missing"
    fi
done

echo ""
echo "Checking Python dependencies..."
python3 -c "import json; print('  ✅ json available')" 2>/dev/null || echo "  ❌ json missing"
python3 -c "import toml; print('  ✅ toml available')" 2>/dev/null || echo "  ⚠️  toml missing (optional)"
python3 -c "import tqdm; print('  ✅ tqdm available')" 2>/dev/null || echo "  ⚠️  tqdm missing (optional)"

echo ""
echo "Checking system tools..."
command -v rg &> /dev/null && echo "  ✅ ripgrep installed" || echo "  ⚠️  ripgrep not installed"
command -v git &> /dev/null && echo "  ✅ git installed" || echo "  ❌ git not installed"
command -v pytest &> /dev/null && echo "  ✅ pytest installed" || echo "  ⚠️  pytest not installed"

echo ""
echo "Configuration:"
if [ -f cleanup_config.json ]; then
    echo "Projects configured:"
    python3 -c "
import json
with open('cleanup_config.json') as f:
    config = json.load(f)
    for p in config['projects']:
        print(f'  - {p}')
"
fi

echo ""
echo "Ready to run cleanup? Use one of these commands:"
echo "  ./run_cleanup_simple.sh    # Run bash-based cleanup"
echo "  python3 simple_cleanup.py  # Run Python-based cleanup"
echo ""
echo "To install dependencies first:"
echo "  ./install_dependencies.sh"
