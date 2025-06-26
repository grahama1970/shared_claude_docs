#!/usr/bin/env python3
"""Comprehensive test for Tasks #26-30"""

import sys
import asyncio
import time
import json
import os
from datetime import datetime
from pathlib import Path

sys.path.insert(0, "/home/graham/workspace/shared_claude_docs/project_interactions")

# Import all components for tasks 26-30
from performance_monitor.performance_monitor_interaction import PerformanceMonitor, AlertLevel
from doc_generator.doc_generator_interaction import DocumentationGenerator
from dependency_analyzer.dependency_analyzer_interaction import DependencyAnalyzer
from cache_manager.cache_manager_interaction import CacheManagerSystem
from data_fusion.data_fusion_interaction import MultiModalFusionPipeline, ModalityData

def run_tests():
    """Run comprehensive tests for tasks 26-30"""
    test_results = []
    failed_tests = []
    
    print("="*80)
    print("Tasks #26-30: Comprehensive Test Suite")
    print("="*80)
    
    # Test 26: Performance Monitor
    print("\n1. Testing Task #26 - Performance Monitor...")
    start_time = time.time()
    try:
        async def test_performance_monitor():
            monitor = PerformanceMonitor()
            dashboard = await monitor.monitor_modules(
                module_names=["test_module"],
                duration=0.5
            )
            return (
                'modules' in dashboard and
                'summary' in dashboard and
                len(dashboard.get('modules', {})) > 0
            )
        
        success = asyncio.run(test_performance_monitor())
        duration = time.time() - start_time
        
        test_result = {
            "name": "Task #26: Performance Monitor",
            "desc": "Real-time performance monitoring",
            "result": "Monitor active with dashboard" if success else "Monitor failed",
            "status": "Pass" if success else "Fail",
            "duration": duration
        }
        test_results.append(test_result)
        
        if success:
            print(f"   ✅ Performance monitoring working ({duration:.2f}s)")
        else:
            print(f"   ❌ Performance monitoring failed ({duration:.2f}s)")
            failed_tests.append(("Task #26", "Monitor failed"))
            
    except Exception as e:
        test_result = {
            "name": "Task #26: Performance Monitor",
            "desc": "Real-time performance monitoring",
            "result": str(e),
            "status": "Fail",
            "duration": time.time() - start_time,
            "error": str(e)
        }
        test_results.append(test_result)
        failed_tests.append(("Task #26", str(e)))
        print(f"   ❌ Error: {e}")
    
    # Test 27: Documentation Generator
    print("\n2. Testing Task #27 - Documentation Generator...")
    start_time = time.time()
    try:
        generator = DocumentationGenerator()
        
        # Generate docs for this test file
        module_info = generator.generate_from_module(__file__)
        
        success = (
            module_info is not None and
            hasattr(module_info, 'functions') and
            len(module_info.functions) > 0
        )
        
        duration = time.time() - start_time
        
        test_result = {
            "name": "Task #27: Doc Generator",
            "desc": "Automated documentation generation",
            "result": f"Found {len(module_info.functions)} functions" if success else "Generation failed",
            "status": "Pass" if success else "Fail",
            "duration": duration
        }
        test_results.append(test_result)
        
        if success:
            print(f"   ✅ Documentation generation working ({duration:.2f}s)")
            print(f"      Functions documented: {len(module_info.functions)}")
        else:
            print(f"   ❌ Documentation generation failed ({duration:.2f}s)")
            failed_tests.append(("Task #27", "Generation failed"))
            
    except Exception as e:
        test_result = {
            "name": "Task #27: Doc Generator",
            "desc": "Automated documentation generation",
            "result": str(e),
            "status": "Fail",
            "duration": time.time() - start_time,
            "error": str(e)
        }
        test_results.append(test_result)
        failed_tests.append(("Task #27", str(e)))
        print(f"   ❌ Error: {e}")
    
    # Test 28: Dependency Analyzer
    print("\n3. Testing Task #28 - Dependency Analyzer...")
    start_time = time.time()
    try:
        async def test_dependency_analyzer():
            analyzer = DependencyAnalyzer()
            
            # Analyze this directory
            current_dir = os.path.dirname(__file__)
            analysis = await analyzer.analyze_modules([current_dir])
            
            return (
                hasattr(analysis, 'modules') and
                hasattr(analysis, 'dependencies') and
                hasattr(analysis, 'recommendations')
            )
        
        success = asyncio.run(test_dependency_analyzer())
        duration = time.time() - start_time
        
        test_result = {
            "name": "Task #28: Dependency Analyzer",
            "desc": "Cross-module dependency analysis",
            "result": "Analysis complete" if success else "Analysis failed",
            "status": "Pass" if success else "Fail",
            "duration": duration
        }
        test_results.append(test_result)
        
        if success:
            print(f"   ✅ Dependency analysis working ({duration:.2f}s)")
        else:
            print(f"   ❌ Dependency analysis failed ({duration:.2f}s)")
            failed_tests.append(("Task #28", "Analysis failed"))
            
    except Exception as e:
        test_result = {
            "name": "Task #28: Dependency Analyzer",
            "desc": "Cross-module dependency analysis",
            "result": str(e),
            "status": "Fail",
            "duration": time.time() - start_time,
            "error": str(e)
        }
        test_results.append(test_result)
        failed_tests.append(("Task #28", str(e)))
        print(f"   ❌ Error: {e}")
    
    # Test 29: Cache Manager
    print("\n4. Testing Task #29 - Cache Manager...")
    start_time = time.time()
    try:
        async def test_cache_manager():
            cache = CacheManagerSystem()
            await cache.initialize()
            
            # Test basic operations
            await cache.set("test_module", "test_key", {"data": "test"})
            value = await cache.get("test_module", "test_key")
            
            # Test invalidation
            await cache.invalidate("test_module", "test_key")
            value_after = await cache.get("test_module", "test_key")
            
            await cache.shutdown()
            
            return value is not None and value_after is None
        
        success = asyncio.run(test_cache_manager())
        duration = time.time() - start_time
        
        test_result = {
            "name": "Task #29: Cache Manager",
            "desc": "Intelligent cache management",
            "result": "Cache operations working" if success else "Cache failed",
            "status": "Pass" if success else "Fail",
            "duration": duration
        }
        test_results.append(test_result)
        
        if success:
            print(f"   ✅ Cache management working ({duration:.2f}s)")
        else:
            print(f"   ❌ Cache management failed ({duration:.2f}s)")
            failed_tests.append(("Task #29", "Cache operations failed"))
            
    except Exception as e:
        test_result = {
            "name": "Task #29: Cache Manager",
            "desc": "Intelligent cache management",
            "result": str(e),
            "status": "Fail",
            "duration": time.time() - start_time,
            "error": str(e)
        }
        test_results.append(test_result)
        failed_tests.append(("Task #29", str(e)))
        print(f"   ❌ Error: {e}")
    
    # Test 30: Data Fusion
    print("\n5. Testing Task #30 - Multi-Modal Data Fusion...")
    start_time = time.time()
    try:
        pipeline = MultiModalFusionPipeline()
        
        # Test fusion
        data = ModalityData(
            text="Test document",
            structured={"category": "test", "value": 0.5}
        )
        
        features = pipeline.extract_features(data)
        
        # Check if we got features dict
        success = (
            features is not None and
            isinstance(features, dict) and
            any(v is not None for v in features.values())
        )
        
        duration = time.time() - start_time
        
        test_result = {
            "name": "Task #30: Data Fusion",
            "desc": "Multi-modal data fusion",
            "result": f"Fused {len(features)} modalities" if success else "Fusion failed",
            "status": "Pass" if success else "Fail",
            "duration": duration
        }
        test_results.append(test_result)
        
        if success:
            print(f"   ✅ Data fusion working ({duration:.2f}s)")
            print(f"      Modalities fused: {list(features.keys())}")
        else:
            print(f"   ❌ Data fusion failed ({duration:.2f}s)")
            failed_tests.append(("Task #30", "Fusion failed"))
            
    except Exception as e:
        test_result = {
            "name": "Task #30: Data Fusion",
            "desc": "Multi-modal data fusion",
            "result": str(e),
            "status": "Fail",
            "duration": time.time() - start_time,
            "error": str(e)
        }
        test_results.append(test_result)
        failed_tests.append(("Task #30", str(e)))
        print(f"   ❌ Error: {e}")
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for r in test_results if r["status"] == "Pass")
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {len(failed_tests)}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests:
        print("\nFailed Tests:")
        for test_name, error in failed_tests:
            print(f"  - {test_name}: {error}")
    
    # Generate test report
    generate_report(test_results)
    
    return 0 if len(failed_tests) == 0 else 1


def generate_report(test_results):
    """Generate markdown test report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path("../docs/reports")
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / f"test_report_tasks_026_030_{timestamp}.md"
    
    content = f"""# Test Report - Tasks #026-030
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary
This report covers the testing of Tasks #026-030:
- Task #026: Performance Monitor - Real-time performance monitoring
- Task #027: Documentation Generator - Automated documentation generation
- Task #028: Dependency Analyzer - Cross-module dependency analysis
- Task #029: Cache Manager - Intelligent cache management
- Task #030: Data Fusion - Multi-modal data fusion pipeline

## Test Results

| Task | Name | Description | Result | Status | Duration |
|------|------|-------------|--------|--------|----------|
"""
    
    for r in test_results:
        status = "✅ Pass" if r["status"] == "Pass" else "❌ Fail"
        error = r.get("error", "")
        content += f"| {r['name'].split(':')[0]} | {r['name'].split(':')[1].strip()} | {r['desc']} | {r['result']} | {status} | {r['duration']:.2f}s |\n"
    
    # Summary stats
    total = len(test_results)
    passed = sum(1 for r in test_results if r["status"] == "Pass")
    content += f"""

## Summary Statistics
- **Total Tasks Tested**: {total}
- **Passed**: {passed}
- **Failed**: {total - passed}
- **Success Rate**: {(passed/total)*100:.1f}%

## Task Completion Status
"""
    
    for i, r in enumerate(test_results, 26):
        status = "✅ COMPLETE" if r["status"] == "Pass" else "❌ INCOMPLETE"
        content += f"- Task #{i}: {status}\n"
    
    content += f"""

## Conclusion
Tasks #026-030 represent advanced system capabilities including performance monitoring,
documentation generation, dependency analysis, caching, and multi-modal data fusion.
{"All tasks have been successfully implemented and verified." if passed == total else f"{total - passed} tasks require additional work."}
"""
    
    report_path.write_text(content)
    print(f"\n📄 Test report generated: {report_path}")


if __name__ == "__main__":
    exit_code = run_tests()
    exit(exit_code)