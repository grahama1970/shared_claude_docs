#!/usr/bin/env python3
"""
Run all GRANGER task tests directly.

This script runs the interaction scenarios for Tasks 8-12 to verify implementation.
"""

import sys
import time
import traceback
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_task_8():
    """Run Task #8: Claude Max Proxy tests."""
    print("\n" + "="*80)
    print("Task #8: Claude Max Proxy - Multi-Model Orchestration")
    print("="*80)
    
    try:
        from project_interactions.claude_max_proxy.claude_max_proxy_interaction import MultiModelOrchestrationScenario
        
        scenario = MultiModelOrchestrationScenario()
        
        # Run tests
        tests = [
            ("test_response_validation", (5.0, 15.0)),
            ("test_conversation_persistence", (3.0, 10.0)),
            ("test_automatic_delegation", (2.0, 8.0))
        ]
        
        results = []
        for test_name, expected_duration in tests:
            print(f"\n  Running {test_name}...")
            start_time = time.time()
            
            try:
                method = getattr(scenario, test_name)
                result = method()
                duration = time.time() - start_time
                
                status = "✅ PASS" if result.success else "❌ FAIL"
                print(f"  {status} - Duration: {duration:.2f}s (expected: {expected_duration[0]}-{expected_duration[1]}s)")
                
                if result.output_data:
                    print(f"  Output: {list(result.output_data.keys())}")
                
                results.append(result.success)
                
            except Exception as e:
                print(f"  ❌ ERROR: {str(e)}")
                results.append(False)
        
        # Overall result
        overall = all(results)
        print(f"\n  Overall: {'✅ PASS' if overall else '❌ FAIL'} ({sum(results)}/{len(results)} tests passed)")
        return overall
        
    except Exception as e:
        print(f"  ❌ Failed to load module: {e}")
        traceback.print_exc()
        return False


def run_task_9():
    """Run Task #9: Unsloth tests."""
    print("\n" + "="*80)
    print("Task #9: Unsloth - Student-Teacher Learning")
    print("="*80)
    
    try:
        from project_interactions.unsloth.unsloth_interaction import StudentTeacherLearningScenario
        
        scenario = StudentTeacherLearningScenario()
        
        # Run tests
        tests = [
            ("test_student_learning", (60.0, 300.0)),
            ("test_grokking_patterns", (30.0, 120.0)),
            ("test_huggingface_deployment", (30.0, 90.0))
        ]
        
        results = []
        for test_name, expected_duration in tests:
            print(f"\n  Running {test_name}...")
            start_time = time.time()
            
            try:
                method = getattr(scenario, test_name)
                result = method()
                duration = time.time() - start_time
                
                status = "✅ PASS" if result.success else "❌ FAIL"
                print(f"  {status} - Duration: {duration:.2f}s (expected: {expected_duration[0]}-{expected_duration[1]}s)")
                
                if result.output_data:
                    print(f"  Output: {list(result.output_data.keys())}")
                
                results.append(result.success)
                
            except Exception as e:
                print(f"  ❌ ERROR: {str(e)}")
                results.append(False)
        
        # Overall result
        overall = all(results)
        print(f"\n  Overall: {'✅ PASS' if overall else '❌ FAIL'} ({sum(results)}/{len(results)} tests passed)")
        return overall
        
    except Exception as e:
        print(f"  ❌ Failed to load module: {e}")
        traceback.print_exc()
        return False


def run_task_10():
    """Run Task #10: Test Reporter tests."""
    print("\n" + "="*80)
    print("Task #10: Test Reporter - Flaky Test Detection")
    print("="*80)
    
    try:
        from project_interactions.test_reporter.test_reporter_interaction import FlakyTestDetectionScenario
        
        scenario = FlakyTestDetectionScenario()
        
        # Run tests
        tests = [
            ("test_detect_flaky_tests", (1.0, 5.0)),
            ("test_generate_dashboard", (0.5, 3.0)),
            ("test_track_history", (0.5, 2.0))
        ]
        
        results = []
        for test_name, expected_duration in tests:
            print(f"\n  Running {test_name}...")
            start_time = time.time()
            
            try:
                method = getattr(scenario, test_name)
                result = method()
                duration = time.time() - start_time
                
                status = "✅ PASS" if result.success else "❌ FAIL"
                print(f"  {status} - Duration: {duration:.2f}s (expected: {expected_duration[0]}-{expected_duration[1]}s)")
                
                if result.output_data:
                    print(f"  Output: {list(result.output_data.keys())}")
                
                results.append(result.success)
                
            except Exception as e:
                print(f"  ❌ ERROR: {str(e)}")
                results.append(False)
        
        # Overall result
        overall = all(results)
        print(f"\n  Overall: {'✅ PASS' if overall else '❌ FAIL'} ({sum(results)}/{len(results)} tests passed)")
        return overall
        
    except Exception as e:
        print(f"  ❌ Failed to load module: {e}")
        traceback.print_exc()
        return False


def run_task_11():
    """Run Task #11: ArXiv-Marker Pipeline tests."""
    print("\n" + "="*80)
    print("Task #11: ArXiv → Marker Pipeline (Level 1)")
    print("="*80)
    
    try:
        from project_interactions.arxiv_marker_pipeline.arxiv_marker_pipeline_interaction import ArxivMarkerPipelineScenario
        
        scenario = ArxivMarkerPipelineScenario()
        
        # Run tests
        tests = [
            ("test_search_and_download", (20.0, 60.0)),
            ("test_pdf_conversion", (15.0, 40.0)),
            ("test_quality_validation", (15.0, 30.0))
        ]
        
        results = []
        for test_name, expected_duration in tests:
            print(f"\n  Running {test_name}...")
            start_time = time.time()
            
            try:
                method = getattr(scenario, test_name)
                result = method()
                duration = time.time() - start_time
                
                status = "✅ PASS" if result.success else "❌ FAIL"
                print(f"  {status} - Duration: {duration:.2f}s (expected: {expected_duration[0]}-{expected_duration[1]}s)")
                
                if result.output_data:
                    print(f"  Output: {list(result.output_data.keys())}")
                
                results.append(result.success)
                
            except Exception as e:
                print(f"  ❌ ERROR: {str(e)}")
                results.append(False)
        
        # Overall result
        overall = all(results)
        print(f"\n  Overall: {'✅ PASS' if overall else '❌ FAIL'} ({sum(results)}/{len(results)} tests passed)")
        return overall
        
    except Exception as e:
        print(f"  ❌ Failed to load module: {e}")
        traceback.print_exc()
        return False


def run_task_12():
    """Run Task #12: Marker-ArangoDB Pipeline tests."""
    print("\n" + "="*80)
    print("Task #12: Marker → ArangoDB Pipeline (Level 1)")
    print("="*80)
    
    try:
        from project_interactions.marker_arangodb_pipeline.marker_arangodb_pipeline_interaction import MarkerArangoPipelineScenario
        
        scenario = MarkerArangoPipelineScenario()
        
        # Run tests
        tests = [
            ("test_entity_extraction", (5.0, 15.0)),
            ("test_graph_storage", (5.0, 20.0)),
            ("test_knowledge_search", (5.0, 10.0))
        ]
        
        results = []
        for test_name, expected_duration in tests:
            print(f"\n  Running {test_name}...")
            start_time = time.time()
            
            try:
                method = getattr(scenario, test_name)
                result = method()
                duration = time.time() - start_time
                
                status = "✅ PASS" if result.success else "❌ FAIL"
                print(f"  {status} - Duration: {duration:.2f}s (expected: {expected_duration[0]}-{expected_duration[1]}s)")
                
                if result.output_data:
                    print(f"  Output: {list(result.output_data.keys())}")
                
                results.append(result.success)
                
            except Exception as e:
                print(f"  ❌ ERROR: {str(e)}")
                results.append(False)
        
        # Overall result
        overall = all(results)
        print(f"\n  Overall: {'✅ PASS' if overall else '❌ FAIL'} ({sum(results)}/{len(results)} tests passed)")
        return overall
        
    except Exception as e:
        print(f"  ❌ Failed to load module: {e}")
        traceback.print_exc()
        return False


def main():
    """Main test runner."""
    print("="*80)
    print("GRANGER Task Tests - Direct Execution")
    print(f"Started: {datetime.now().isoformat()}")
    print("="*80)
    
    # Run all tasks
    task_results = {
        8: run_task_8(),
        9: run_task_9(),
        10: run_task_10(),
        11: run_task_11(),
        12: run_task_12()
    }
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    passed = sum(1 for v in task_results.values() if v)
    total = len(task_results)
    
    for task_num, result in task_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"Task #{task_num}: {status}")
    
    print(f"\nOverall: {passed}/{total} tasks passed")
    
    if passed == total:
        print("\n✅ SUCCESS: All GRANGER tasks verified!")
    else:
        print("\n❌ FAILURE: Some tasks need attention.")
    
    print(f"\nCompleted: {datetime.now().isoformat()}")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    # sys.exit() removed)