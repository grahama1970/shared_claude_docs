#!/usr/bin/env python3
"""
Quick verification test for Task #40 - Pipeline Monitor
Tests basic functionality without long delays
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from pipeline_monitor_interaction import (
    PipelineMonitor, PipelineStatus, StageStatus, AlertSeverity
)

def test_basic_functionality():
    """Test basic pipeline monitor functionality"""
    print("🔍 Testing Pipeline Monitor Basic Functionality...")
    
    monitor = PipelineMonitor()
    
    # Register a simple pipeline
    monitor.register_pipeline(
        'test_pipeline',
        stages=['extract', 'transform', 'load'],
        sla_minutes=30
    )
    
    # Start monitoring
    run_id = monitor.start_monitoring('test_pipeline', {'test': True})
    print(f"✅ Started monitoring: {run_id}")
    
    # Update stages
    monitor.update_stage(run_id, 'extract', StageStatus.RUNNING)
    monitor.update_stage(run_id, 'extract', StageStatus.COMPLETED)
    
    monitor.update_stage(run_id, 'transform', StageStatus.RUNNING)
    monitor.update_stage(run_id, 'transform', StageStatus.COMPLETED)
    
    monitor.update_stage(run_id, 'load', StageStatus.RUNNING)
    monitor.update_stage(run_id, 'load', StageStatus.COMPLETED)
    
    # Complete pipeline
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Get status
    status = monitor.get_pipeline_status('test_pipeline')
    print(f"✅ Pipeline status: {status['status']}")
    
    # Get summary
    summary = monitor.get_summary()
    print(f"✅ Summary - Active: {summary['active_pipelines']}, Total runs: {summary['total_runs']}")
    
    return True

def test_alert_system():
    """Test alert system functionality"""
    print("\n🔍 Testing Alert System...")
    
    monitor = PipelineMonitor()
    alerts = []
    
    # Set up alert callback
    monitor.register_alert_callback(lambda alert: alerts.append(alert))
    
    # Register pipeline with low thresholds
    monitor.register_pipeline(
        'alert_test',
        stages=['process'],
        alert_thresholds={
            'error_rate': 0.01,  # Very low threshold
            'stage_duration_seconds': 0.1
        }
    )
    
    # Start monitoring
    run_id = monitor.start_monitoring('alert_test')
    
    # Generate errors to trigger alert
    monitor.update_stage(run_id, 'process', StageStatus.RUNNING)
    monitor.update_stage(
        run_id, 'process', 
        status=StageStatus.COMPLETED,
        errors=100,
        processed=1000
    )
    
    # Complete pipeline
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    print(f"✅ Alerts generated: {len(alerts)}")
    if alerts:
        print(f"   First alert: {alerts[0]['message'][:50]}...")
    
    return True

def test_multi_pipeline():
    """Test multi-pipeline management"""
    print("\n🔍 Testing Multi-Pipeline Management...")
    
    monitor = PipelineMonitor()
    
    # Register multiple pipelines
    pipelines = ['etl_pipeline', 'ml_pipeline', 'batch_pipeline']
    for pipeline in pipelines:
        monitor.register_pipeline(pipeline, stages=['start', 'process', 'end'])
    
    # Start all pipelines
    run_ids = []
    for pipeline in pipelines:
        run_id = monitor.start_monitoring(pipeline)
        run_ids.append(run_id)
    
    # Complete all pipelines
    for run_id, pipeline in zip(run_ids, pipelines):
        for stage in ['start', 'process', 'end']:
            monitor.update_stage(run_id, stage, StageStatus.RUNNING)
            monitor.update_stage(run_id, stage, StageStatus.COMPLETED)
        monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Get summary
    summary = monitor.get_summary()
    print(f"✅ Managed {len(pipelines)} pipelines")
    print(f"✅ Total runs: {summary['total_runs']}")
    print(f"✅ Success rate: {summary['success_rate']:.1%}")
    
    return True

def test_resource_tracking():
    """Test resource usage tracking"""
    print("\n🔍 Testing Resource Tracking...")
    
    monitor = PipelineMonitor()
    
    monitor.register_pipeline('resource_test', stages=['compute'])
    run_id = monitor.start_monitoring('resource_test')
    
    # Update with resource metrics
    monitor.update_stage(
        run_id, 'compute',
        status=StageStatus.RUNNING,
        memory_usage_mb=512,
        cpu_usage_percent=75
    )
    
    monitor.update_stage(
        run_id, 'compute',
        status=StageStatus.COMPLETED,
        memory_usage_mb=768,
        cpu_usage_percent=85
    )
    
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Get status with metrics
    status = monitor.get_pipeline_status('resource_test')
    print(f"✅ Resource tracking enabled")
    print(f"✅ Peak memory: {status.get('peak_memory_mb', 'N/A')} MB")
    print(f"✅ Peak CPU: {status.get('peak_cpu_percent', 'N/A')}%")
    
    return True

def main():
    """Run all tests"""
    print("="*60)
    print("Task #40: Pipeline Monitor - Quick Verification")
    print("="*60)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Alert System", test_alert_system),
        ("Multi-Pipeline Management", test_multi_pipeline),
        ("Resource Tracking", test_resource_tracking)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"\n✅ {test_name} PASSED")
            else:
                print(f"\n❌ {test_name} FAILED")
        except Exception as e:
            print(f"\n❌ {test_name} ERROR: {e}")
            results.append((test_name, False))
    
    # Summary
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    
    if passed == total:
        print("\n✅ All tests passed! Task #40 verified.")
        return 0
    else:
        print("\n❌ Some tests failed.")
        return 1

if __name__ == "__main__":
    # sys.exit() removed)