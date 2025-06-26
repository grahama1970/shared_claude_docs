#!/bin/bash
# Fix pytest configuration across all projects

echo "🔧 Fixing Pytest Configuration"
echo "============================================================"

# Projects to fix
projects=(
    "/home/graham/workspace/experiments/granger_hub"
    "/home/graham/workspace/experiments/rl_commons"
    "/home/graham/workspace/experiments/claude-test-reporter"
    "/home/graham/workspace/experiments/world_model"
    "/home/graham/workspace/experiments/sparta"
    "/home/graham/workspace/experiments/marker"
    "/home/graham/workspace/experiments/arangodb"
    "/home/graham/workspace/experiments/llm_call"
    "/home/graham/workspace/experiments/unsloth_wip"
)

for project in "${projects[@]}"; do
    if [ ! -d "$project" ]; then
        echo "❌ Skipping $(basename $project): does not exist"
        continue
    fi
    
    echo -e "\n📁 Processing $(basename $project)..."
    
    # Add pytest.ini if missing
    if [ ! -f "$project/pytest.ini" ]; then
        echo "  Creating pytest.ini..."
        cat > "$project/pytest.ini" << 'EOF'
[pytest]
markers =
    honeypot: test designed to fail for integrity verification
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
EOF
        echo "  ✅ Created pytest.ini"
    else
        # Check if honeypot marker exists
        if ! grep -q "honeypot:" "$project/pytest.ini"; then
            echo "  Adding honeypot marker to pytest.ini..."
            # Add honeypot marker after [pytest] section
            sed -i '/markers =/a\    honeypot: test designed to fail for integrity verification' "$project/pytest.ini" 2>/dev/null || \
            echo -e "\n    honeypot: test designed to fail for integrity verification" >> "$project/pytest.ini"
            echo "  ✅ Added honeypot marker"
        else
            echo "  ✓ Honeypot marker already exists"
        fi
    fi
    
    # Install pytest-json-report in the venv
    venv_path=""
    for venv_name in .venv venv env; do
        if [ -d "$project/$venv_name" ]; then
            venv_path="$project/$venv_name"
            break
        fi
    done
    
    if [ -n "$venv_path" ]; then
        echo "  Installing pytest-json-report..."
        (cd "$project" && source "$venv_path/bin/activate" && pip install pytest-json-report 2>/dev/null)
        if [ $? -eq 0 ]; then
            echo "  ✅ Installed pytest-json-report"
        else
            echo "  ⚠️  Could not install pytest-json-report"
        fi
    fi
done

echo -e "\n✨ Pytest configuration fixes complete"