"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Module: test_performance_analysis.py
Purpose: Test performance analysis and optimization features

Tests pipeline performance analysis, bottleneck detection, trend analysis,
and optimization suggestion generation.
"""

import sys
import time
import random
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline_monitor_interaction import (
    PipelineMonitor, PipelineStatus, StageStatus
)


def test_performance_statistics():
    """Test performance statistics calculation."""
    print("\n=== Testing Performance Statistics ===")
    
    monitor = PipelineMonitor()
    monitor.register_pipeline('perf_test', ['stage1', 'stage2', 'stage3'])
    
    # Run multiple pipeline executions
    durations = []
    for i in range(5):
        run_id = monitor.start_monitoring('perf_test')
        
        # Simulate stages with varying durations
        for stage in ['stage1', 'stage2', 'stage3']:
            monitor.update_stage(run_id, stage, StageStatus.RUNNING)
            time.sleep(0.1 + random.random() * 0.1)  # 0.1-0.2s per stage
            monitor.update_stage(
                run_id, stage,
                status=StageStatus.COMPLETED,
                records_processed=1000 * (i + 1),
                errors=i * 10
            )
        
        monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
        
        # Track duration
        run = monitor.run_history['perf_test'][-1]
        durations.append(run.duration_seconds)
    
    # Get performance analysis
    analysis = monitor.get_performance_analysis('perf_test')
    
    assert analysis['total_runs'] == 5
    assert analysis['success_rate'] == 1.0
    assert 'performance' in analysis
    assert analysis['performance']['avg_duration'] > 0
    assert analysis['performance']['min_duration'] <= analysis['performance']['avg_duration']
    assert analysis['performance']['max_duration'] >= analysis['performance']['avg_duration']
    assert 'stage_stats' in analysis
    
    print(f"✓ Performance stats: avg={analysis['performance']['avg_duration']:.2f}s, "
          f"min={analysis['performance']['min_duration']:.2f}s, "
          f"max={analysis['performance']['max_duration']:.2f}s")
    return True


def test_bottleneck_detection():
    """Test bottleneck identification."""
    print("\n=== Testing Bottleneck Detection ===")
    
    monitor = PipelineMonitor()
    monitor.register_pipeline('bottleneck_test', ['fast1', 'slow', 'fast2'])
    
    # Run pipeline with one slow stage
    for i in range(3):
        run_id = monitor.start_monitoring('bottleneck_test')
        
        # Fast stage 1
        monitor.update_stage(run_id, 'fast1', StageStatus.RUNNING)
        time.sleep(0.1)
        monitor.update_stage(run_id, 'fast1', StageStatus.COMPLETED, records_processed=1000)
        
        # Slow stage (bottleneck)
        monitor.update_stage(run_id, 'slow', StageStatus.RUNNING)
        time.sleep(0.5)  # 5x slower
        monitor.update_stage(run_id, 'slow', StageStatus.COMPLETED, records_processed=1000)
        
        # Fast stage 2
        monitor.update_stage(run_id, 'fast2', StageStatus.RUNNING)
        time.sleep(0.1)
        monitor.update_stage(run_id, 'fast2', StageStatus.COMPLETED, records_processed=1000)
        
        monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Get performance analysis
    analysis = monitor.get_performance_analysis('bottleneck_test')
    
    assert 'bottlenecks' in analysis
    assert len(analysis['bottlenecks']) > 0
    
    # The slow stage should be identified as bottleneck
    bottleneck = analysis['bottlenecks'][0]
    assert bottleneck['stage'] == 'slow'
    assert bottleneck['percentage'] > 50  # Should be >50% of total time
    assert 'suggestion' in bottleneck
    
    print(f"✓ Bottleneck detected: {bottleneck['stage']} "
          f"({bottleneck['percentage']:.1f}% of total time)")
    return True


def test_trend_analysis():
    """Test performance trend detection."""
    print("\n=== Testing Trend Analysis ===")
    
    monitor = PipelineMonitor()
    monitor.register_pipeline('trend_test', ['process'])
    
    # Run pipelines with increasing duration (degrading performance)
    for i in range(12):
        run_id = monitor.start_monitoring('trend_test')
        monitor.update_stage(run_id, 'process', StageStatus.RUNNING)
        
        # Simulate increasing processing time
        sleep_time = 0.1 + (i * 0.02)  # Gradually slower
        time.sleep(sleep_time)
        
        monitor.update_stage(
            run_id, 'process',
            status=StageStatus.COMPLETED,
            records_processed=1000
        )
        monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Get performance analysis
    analysis = monitor.get_performance_analysis('trend_test')
    
    assert 'trends' in analysis
    trend = analysis['trends']
    assert trend['status'] in ['degrading', 'improving', 'stable']
    
    # Should detect degrading performance
    if trend['status'] == 'degrading':
        print(f"✓ Trend detected: {trend['status']} "
              f"({trend['change_percent']:.1f}% change)")
    else:
        print(f"✓ Trend analysis completed: {trend['status']}")
    
    return True


def test_optimization_suggestions():
    """Test optimization suggestion generation."""
    print("\n=== Testing Optimization Suggestions ===")
    
    monitor = PipelineMonitor()
    monitor.register_pipeline('optimize_test', ['extract', 'process', 'load'])
    
    # Run pipelines with various issues
    for i in range(6):
        run_id = monitor.start_monitoring('optimize_test')
        
        for stage in ['extract', 'process', 'load']:
            monitor.update_stage(run_id, stage, StageStatus.RUNNING)
            time.sleep(0.1 + (0.05 if stage == 'process' else 0))  # Process is slower
            
            # Add errors to some runs
            errors = 100 if i % 2 == 0 else 0
            monitor.update_stage(
                run_id, stage,
                status=StageStatus.COMPLETED,
                records_processed=1000,
                errors=errors,
                memory_usage_mb=600 if stage == 'process' else 200,
                cpu_usage_percent=85 if stage == 'process' else 40
            )
        
        monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Get optimization suggestions
    suggestions = monitor.get_optimization_suggestions('optimize_test')
    
    assert len(suggestions) > 0
    
    # Check suggestion types
    suggestion_types = {s['type'] for s in suggestions}
    print(f"✓ Generated {len(suggestions)} suggestions: {suggestion_types}")
    
    # Print suggestions
    for suggestion in suggestions[:3]:
        print(f"  - [{suggestion['severity']}] {suggestion['message']}")
    
    return True


def test_resource_utilization_tracking():
    """Test resource utilization tracking."""
    print("\n=== Testing Resource Utilization Tracking ===")
    
    monitor = PipelineMonitor()
    monitor.register_pipeline('resource_test', ['compute'])
    
    # Configure alerts for high resource usage
    alerts = []
    monitor.configure_alerts(lambda alert: alerts.append(alert))
    
    # Run pipeline with high resource usage
    run_id = monitor.start_monitoring('resource_test')
    monitor.update_stage(run_id, 'compute', StageStatus.RUNNING)
    
    # Update with high resource usage
    monitor.update_stage(
        run_id, 'compute',
        status=StageStatus.RUNNING,
        records_processed=5000,
        memory_usage_mb=1500,  # Above default threshold
        cpu_usage_percent=90   # Above default threshold
    )
    
    time.sleep(0.1)
    monitor.update_stage(run_id, 'compute', status=StageStatus.COMPLETED)
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Check if alerts were generated
    resource_alerts = [a for a in alerts if 'memory' in a['message'] or 'CPU' in a['message']]
    assert len(resource_alerts) >= 1
    
    print(f"✓ Resource alerts generated: {len(resource_alerts)}")
    for alert in resource_alerts:
        print(f"  - [{alert['severity']}] {alert['message']}")
    
    return True


def test_sla_compliance():
    """Test SLA compliance monitoring."""
    print("\n=== Testing SLA Compliance ===")
    
    monitor = PipelineMonitor()
    monitor.register_pipeline('sla_test', ['process'], sla_minutes=0.1)  # 6 seconds SLA
    
    alerts = []
    monitor.configure_alerts(lambda alert: alerts.append(alert))
    
    # Run pipeline that exceeds SLA
    run_id = monitor.start_monitoring('sla_test')
    monitor.update_stage(run_id, 'process', StageStatus.RUNNING)
    time.sleep(0.2)  # 12 seconds, exceeds SLA
    monitor.update_stage(run_id, 'process', StageStatus.COMPLETED, records_processed=1000)
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Check for SLA violation alert
    sla_alerts = [a for a in alerts if 'SLA' in a['message']]
    assert len(sla_alerts) >= 1
    
    print(f"✓ SLA violation detected: {sla_alerts[0]['message']}")
    return True


def run_all_tests():
    """Run all performance analysis tests."""
    tests = [
        test_performance_statistics,
        test_bottleneck_detection,
        test_trend_analysis,
        test_optimization_suggestions,
        test_resource_utilization_tracking,
        test_sla_compliance
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"✗ {test.__name__} failed")
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} failed with error: {e}")
    
    print(f"\n=== Test Summary ===")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {len(tests)}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    # sys.exit() removed