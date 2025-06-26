#!/usr/bin/env python3
"""
Module: prepare_for_interaction_testing.py
Description: Prepares all projects for Level 0-4 interaction testing by verifying basic functionality

External Dependencies:
- None (uses only standard library)

Sample Input:
>>> python prepare_for_interaction_testing.py

Expected Output:
>>> Preparing projects for Level 0-4 testing...
>>> ✅ Level 0: Basic module imports working
>>> ✅ Level 1: Single module interactions ready
>>> ...

Example Usage:
>>> python prepare_for_interaction_testing.py
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Add project paths to Python path
PROJECT_PATHS = [
    '/home/graham/workspace/experiments/aider-daemon/src',
    '/home/graham/workspace/experiments/annotator/src',
    '/home/graham/workspace/experiments/chat/backend',
    '/home/graham/workspace/experiments/arangodb/src',
    '/home/graham/workspace/experiments/arxiv-mcp-server/src',
    '/home/graham/workspace/experiments/marker/src',
    '/home/graham/workspace/experiments/sparta/src',
    '/home/graham/workspace/experiments/llm_call/src',
    '/home/graham/workspace/experiments/granger_hub/src',
    '/home/graham/workspace/experiments/rl_commons/src',
    '/home/graham/workspace/experiments/claude-test-reporter/src',
]

for path in PROJECT_PATHS:
    if Path(path).exists():
        sys.path.insert(0, path)

# Colors
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def test_level_0_readiness():
    """Test Level 0: Basic module imports"""
    print(f"\n{BLUE}Testing Level 0: Basic Module Imports{NC}")
    print("-" * 50)
    
    modules_to_test = [
        ('arangodb', 'arangodb.core'),
        ('arxiv-mcp-server', 'arxiv_mcp_server'),
        ('marker', 'marker.core'),
        ('sparta', 'sparta'),
        ('llm_call', 'llm_call'),
    ]
    
    failures = []
    for name, module in modules_to_test:
        try:
            __import__(module)
            print(f"{GREEN}✅ {name}: {module}{NC}")
        except ImportError as e:
            print(f"{RED}❌ {name}: {module} - {str(e)}{NC}")
            failures.append(name)
    
    return len(failures) == 0, failures

def test_level_1_readiness():
    """Test Level 1: Single module interactions"""
    print(f"\n{BLUE}Testing Level 1: Single Module Interactions{NC}")
    print("-" * 50)
    
    test_files = [
        '/home/graham/workspace/shared_claude_docs/project_interactions/arangodb/level_0_tests/test_query.py',
        '/home/graham/workspace/shared_claude_docs/project_interactions/arxiv-mcp-server/level_0_tests/test_search_papers.py',
    ]
    
    available_tests = []
    for test_file in test_files:
        if Path(test_file).exists():
            available_tests.append(test_file)
            print(f"{GREEN}✅ Found: {Path(test_file).name}{NC}")
        else:
            print(f"{YELLOW}⚠️  Missing: {Path(test_file).name}{NC}")
    
    return len(available_tests) > 0, available_tests

def test_level_2_readiness():
    """Test Level 2: Two module interactions"""
    print(f"\n{BLUE}Testing Level 2: Two Module Interactions{NC}")
    print("-" * 50)
    
    test_file = Path('/home/graham/workspace/shared_claude_docs/project_interactions/level_2_tests/test_arxiv_marker_arangodb.py')
    
    if test_file.exists():
        print(f"{GREEN}✅ Level 2 test file exists{NC}")
        return True, []
    else:
        print(f"{RED}❌ Level 2 test file missing{NC}")
        return False, ["test_arxiv_marker_arangodb.py"]

def test_level_3_readiness():
    """Test Level 3: Full pipeline interactions"""
    print(f"\n{BLUE}Testing Level 3: Full Pipeline Interactions{NC}")
    print("-" * 50)
    
    test_file = Path('/home/graham/workspace/shared_claude_docs/project_interactions/level_3_tests/test_full_granger_pipeline.py')
    
    if test_file.exists():
        print(f"{GREEN}✅ Level 3 test file exists{NC}")
        return True, []
    else:
        print(f"{RED}❌ Level 3 test file missing{NC}")
        return False, ["test_full_granger_pipeline.py"]

def test_level_4_readiness():
    """Test Level 4: UI interactions"""
    print(f"\n{BLUE}Testing Level 4: UI Interactions{NC}")
    print("-" * 50)
    
    ui_projects = {
        'granger-ui': '/home/graham/workspace/granger-ui',
        'annotator': '/home/graham/workspace/experiments/annotator',
        'chat': '/home/graham/workspace/experiments/chat',
        'aider-daemon': '/home/graham/workspace/experiments/aider-daemon',
    }
    
    ready = []
    for name, path in ui_projects.items():
        if Path(path).exists():
            print(f"{GREEN}✅ {name} project exists{NC}")
            ready.append(name)
        else:
            print(f"{RED}❌ {name} project missing{NC}")
    
    return len(ready) == len(ui_projects), ready

def check_scenario_readiness():
    """Check if granger_hub scenarios are accessible"""
    print(f"\n{BLUE}Testing Scenario Availability{NC}")
    print("-" * 50)
    
    scenarios_path = Path('/home/graham/workspace/experiments/granger_hub/scenarios')
    
    if not scenarios_path.exists():
        print(f"{RED}❌ Scenarios directory not found{NC}")
        return False, []
    
    scenario_files = list(scenarios_path.glob('*.py'))
    print(f"{GREEN}✅ Found {len(scenario_files)} scenario files{NC}")
    
    # List a few scenarios
    for scenario in scenario_files[:5]:
        print(f"   - {scenario.name}")
    
    if len(scenario_files) > 5:
        print(f"   ... and {len(scenario_files) - 5} more")
    
    return len(scenario_files) > 0, scenario_files

def create_test_runner_script():
    """Create a script to run interaction tests"""
    script_content = '''#!/bin/bash
# Run Level 0-4 Interaction Tests

echo "🧪 Running Granger Interaction Tests"
echo "===================================="

# Activate virtual environment
source /home/graham/workspace/shared_claude_docs/.venv/bin/activate

# Level 0 Tests
echo -e "\\n📊 Level 0: Basic Module Tests"
cd /home/graham/workspace/shared_claude_docs/project_interactions
python -m pytest arangodb/level_0_tests/test_query.py -v || true
python -m pytest arxiv-mcp-server/level_0_tests/test_search_papers.py -v || true

# Level 1 Tests
echo -e "\\n📊 Level 1: Single Module Interactions"
# Add Level 1 tests here

# Level 2 Tests
echo -e "\\n📊 Level 2: Two Module Interactions"
python -m pytest level_2_tests/test_arxiv_marker_arangodb.py -v || true

# Level 3 Tests
echo -e "\\n📊 Level 3: Full Pipeline Tests"
python -m pytest level_3_tests/test_full_granger_pipeline.py -v || true

# Level 4 Tests
echo -e "\\n📊 Level 4: UI Interaction Tests"
# Add UI tests here

echo -e "\\n✅ Test run complete!"
'''
    
    script_path = Path('/home/graham/workspace/shared_claude_docs/run_interaction_tests.sh')
    script_path.write_text(script_content)
    script_path.chmod(0o755)
    
    print(f"\n{GREEN}✅ Created test runner script: run_interaction_tests.sh{NC}")

def main():
    """Main preparation function"""
    print(f"{BLUE}🚀 Preparing for Level 0-4 Interaction Testing{NC}")
    print("=" * 60)
    
    # Run all level checks
    results = {}
    
    level0_ready, level0_issues = test_level_0_readiness()
    results['Level 0'] = (level0_ready, level0_issues)
    
    level1_ready, level1_tests = test_level_1_readiness()
    results['Level 1'] = (level1_ready, level1_tests)
    
    level2_ready, level2_issues = test_level_2_readiness()
    results['Level 2'] = (level2_ready, level2_issues)
    
    level3_ready, level3_issues = test_level_3_readiness()
    results['Level 3'] = (level3_ready, level3_issues)
    
    level4_ready, level4_projects = test_level_4_readiness()
    results['Level 4'] = (level4_ready, level4_projects)
    
    scenarios_ready, scenario_files = check_scenario_readiness()
    
    # Create test runner script
    create_test_runner_script()
    
    # Summary
    print(f"\n{BLUE}{'=' * 60}{NC}")
    print(f"{BLUE}Summary:{NC}")
    
    all_ready = True
    for level, (ready, _) in results.items():
        status = f"{GREEN}✅ Ready{NC}" if ready else f"{RED}❌ Not Ready{NC}"
        print(f"{level}: {status}")
        if not ready:
            all_ready = False
    
    print(f"Scenarios: {GREEN}✅ Ready{NC}" if scenarios_ready else f"{RED}❌ Not Ready{NC}")
    
    print(f"\n{BLUE}Overall Status:{NC}")
    if all_ready and scenarios_ready:
        print(f"{GREEN}✅ All levels ready for interaction testing!{NC}")
        print(f"\n{YELLOW}Run ./run_interaction_tests.sh to start testing{NC}")
        return 0
    else:
        print(f"{YELLOW}⚠️  Some levels need attention{NC}")
        print(f"\n{YELLOW}Recommendations:{NC}")
        print("1. Run ./fix_ui_projects.sh to install dependencies")
        print("2. Run ./fix_annotator_deps.sh for annotator")
        print("3. Check import errors and fix missing modules")
        return 1

if __name__ == "__main__":
    # sys.exit() removed)