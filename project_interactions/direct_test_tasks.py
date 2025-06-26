#!/usr/bin/env python3
"""
Direct test of GRANGER tasks without complex imports.

This script directly tests the generated task implementations.
"""

import sys
import time
import random
from datetime import datetime
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the framework components directly
exec(open("/home/graham/workspace/shared_claude_docs/templates/interaction_framework.py").read())

# Now execute each task's interaction file directly
def test_task(task_num, module_name, class_name):
    """Test a single task by executing its code directly."""
    print(f"\n{'='*60}")
    print(f"Task #{task_num}: {module_name}")
    print('='*60)
    
    try:
        # Read and execute the interaction file
        interaction_file = f"/home/graham/workspace/shared_claude_docs/project_interactions/{module_name}/{module_name.replace('-', '_')}_interaction.py"
        
        # Read the file content
        with open(interaction_file, 'r') as f:
            content = f.read()
        
        # Replace the problematic import
        content = content.replace(
            "from shared_claude_docs.templates.interaction_framework import (",
            "# Import already done above\n# ("
        )
        
        # Execute the modified content
        exec(content, globals())
        
        # Create and run the scenario
        scenario_class = globals()[class_name]
        scenario = scenario_class()
        
        # Run the execute method
        result = scenario.execute()
        
        print(f"✅ Module loaded and executed successfully")
        print(f"   Module name: {scenario.module_name}")
        print(f"   Success: {result.success}")
        print(f"   Duration: {result.duration:.2f}s")
        print(f"   Test results: {result.output_data.get('test_results', [])}")
        
        return result.success
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test runner."""
    print("="*80)
    print("GRANGER Tasks 8-12 Direct Testing")
    print(f"Started: {datetime.now().isoformat()}")
    print("="*80)
    
    # Define tasks to test
    tasks = [
        (8, "claude-max-proxy", "MultiModelOrchestrationScenario"),
        (9, "unsloth", "StudentTeacherLearningScenario"),
        (10, "test-reporter", "FlakyTestDetectionScenario"),
        (11, "arxiv-marker-pipeline", "ArxivMarkerPipelineScenario"),
        (12, "marker-arangodb-pipeline", "MarkerArangoPipelineScenario")
    ]
    
    results = {}
    
    for task_num, module_name, class_name in tasks:
        results[task_num] = test_task(task_num, module_name, class_name)
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for task_num, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"Task #{task_num}: {status}")
    
    print(f"\nOverall: {passed}/{total} tasks passed")
    
    if passed == total:
        print("\n✅ SUCCESS: All GRANGER tasks 8-12 verified!")
        print("\nNext steps:")
        print("- Continue with Tasks 13-150 from the master task list")
        print("- Implement Level 2 and Level 3 interactions")
        print("- Deploy to production environments")
    else:
        print("\n❌ FAILURE: Some tasks failed verification.")
    
    print(f"\nCompleted: {datetime.now().isoformat()}")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    # sys.exit() removed)