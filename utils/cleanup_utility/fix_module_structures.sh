#!/bin/bash

# Fix module structures for projects with import issues

echo "🔧 Fixing module structures for Claude projects..."

# Function to fix module structure
fix_module_structure() {
    local project_path="$1"
    local project_name=$(basename "$project_path")
    local module_name="${project_name//-/_}"
    
    echo ""
    echo "Processing: $project_name"
    echo "Module name: $module_name"
    
    cd "$project_path" || return
    
    # Check current structure
    if [ -d "src" ]; then
        echo "  ✅ src/ directory exists"
        
        # Check if module directory exists
        if [ ! -d "src/$module_name" ]; then
            echo "  Creating src/$module_name directory..."
            mkdir -p "src/$module_name"
            
            # Create __init__.py
            touch "src/$module_name/__init__.py"
            
            # Move Python files from src to module directory
            echo "  Moving Python files to src/$module_name/..."
            for py_file in src/*.py; do
                if [ -f "$py_file" ] && [ "$(basename "$py_file")" != "__init__.py" ]; then
                    echo "    Moving $(basename "$py_file")"
                    mv "$py_file" "src/$module_name/"
                fi
            done
            
            # Ensure src/__init__.py exists
            touch "src/__init__.py"
        else
            echo "  ✅ Module structure already correct"
        fi
    else
        # No src directory, check if files are in root
        if ls *.py >/dev/null 2>&1; then
            echo "  Creating proper module structure..."
            mkdir -p "src/$module_name"
            
            # Move Python files to module directory
            for py_file in *.py; do
                if [ -f "$py_file" ] && [ "$py_file" != "setup.py" ] && [ "$py_file" != "conftest.py" ]; then
                    echo "    Moving $py_file to src/$module_name/"
                    mv "$py_file" "src/$module_name/"
                fi
            done
            
            # Create __init__.py files
            touch "src/__init__.py"
            touch "src/$module_name/__init__.py"
        fi
    fi
    
    # Fix imports in files
    echo "  Updating imports..."
    if [ -d "src/$module_name" ]; then
        # Update relative imports
        find "src/$module_name" -name "*.py" -exec sed -i \
            -e "s/^from \\.\\([a-zA-Z_]*\\)/from $module_name.\\1/g" \
            -e "s/^import \\.\\([a-zA-Z_]*\\)/import $module_name.\\1/g" {} \;
    fi
    
    # Ensure tests directory exists
    if [ ! -d "tests" ]; then
        echo "  Creating tests directory..."
        mkdir -p "tests"
        touch "tests/__init__.py"
        
        # Create a basic test file
        cat > "tests/test_import.py" << EOF
"""Basic import test for $module_name"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

def test_module_imports():
    """Test that the module can be imported"""
    try:
        import $module_name
        assert True
    except ImportError as e:
        assert False, f"Failed to import $module_name: {e}"

if __name__ == "__main__":
    test_module_imports()
    print("✅ Import test passed")
EOF
    fi
    
    # Commit changes if any
    if git status --porcelain | grep -q .; then
        echo "  Committing module structure fixes..."
        git add -A
        git commit -m "Fix module structure for proper imports"
    fi
}

# Fix claude_max_proxy
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1/2: Fixing claude_max_proxy"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fix_module_structure "/home/graham/workspace/experiments/claude_max_proxy"

# Fix claude-module-communicator
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2/2: Fixing claude-module-communicator"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fix_module_structure "/home/graham/workspace/experiments/claude-module-communicator"

echo ""
echo "✅ Module structure fixes complete!"
echo ""
echo "Next steps:"
echo "1. Run the enhanced cleanup utility again to verify fixes"
echo "2. Check import validation for both projects"