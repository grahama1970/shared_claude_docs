#!/bin/bash

# Test script for enhanced cleanup utility

set -e

echo "Testing Enhanced Cleanup Utility"
echo "================================"

# Test Python imports
echo -n "Testing Python imports... "
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from enhanced_cleanup import EnhancedCleanupUtility
    print('✅ OK')
except Exception as e:
    print(f'❌ Failed: {e}')
    sys.exit(1)
"

# Test configuration loading
echo -n "Testing configuration loading... "
if [ -f cleanup_config_localhost.json ]; then
    echo "✅ OK"
else
    echo "❌ Failed: cleanup_config_localhost.json not found"
    exit 1
fi

# Test dry run on a single project
echo -e "\nTesting dry run on claude-test-reporter..."
python3 -c "
import sys
sys.path.insert(0, '.')
from enhanced_cleanup import EnhancedCleanupUtility

config = {
    'projects': ['/home/graham/workspace/experiments/claude-test-reporter/'],
    'parallel_workers': 1
}

try:
    utility = EnhancedCleanupUtility('cleanup_config_localhost.json', dry_run=True)
    utility.config = config  # Override with test config
    result = utility.analyze_project(config['projects'][0])
    
    print(f'✅ Analysis completed')
    print(f'   Status: {result.get(\"status\")}')
    print(f'   Issues: {len(result.get(\"issues\", []))}')
    print(f'   Warnings: {len(result.get(\"warnings\", []))}')
except Exception as e:
    print(f'❌ Failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

echo -e "\n✅ All tests passed!"
echo "You can now run: ./run_enhanced_cleanup.sh"