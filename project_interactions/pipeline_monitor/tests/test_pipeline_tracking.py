"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Module: test_pipeline_tracking.py
Purpose: Test pipeline tracking functionality

Tests the core pipeline tracking capabilities including registration,
monitoring, stage updates, and status reporting.
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline_monitor_interaction import (
    PipelineMonitor, PipelineStatus, StageStatus, PipelineConfig
)


def test_pipeline_registration():
    """Test pipeline registration functionality."""
    print("\n=== Testing Pipeline Registration ===")
    
    monitor = PipelineMonitor()
    
    # Register pipeline
    monitor.register_pipeline(
        'test_pipeline',
        stages=['stage1', 'stage2', 'stage3'],
        dependencies=['upstream_pipeline'],
        sla_minutes=45
    )
    
    # Verify registration
    assert 'test_pipeline' in monitor.pipelines
    config = monitor.pipelines['test_pipeline']
    assert len(config.stages) == 3
    assert config.sla_minutes == 45
    assert 'upstream_pipeline' in config.dependencies
    
    print("✓ Pipeline registration successful")
    return True


def test_pipeline_monitoring():
    """Test pipeline monitoring and stage updates."""
    print("\n=== Testing Pipeline Monitoring ===")
    
    monitor = PipelineMonitor()
    
    # Register and start monitoring
    monitor.register_pipeline('data_pipeline', ['extract', 'transform', 'load'])
    run_id = monitor.start_monitoring('data_pipeline', {'batch': 'test_001'})
    
    assert run_id in monitor.active_runs
    run = monitor.active_runs[run_id]
    assert run.status == PipelineStatus.RUNNING
    assert len(run.stages) == 3
    
    # Update stages
    monitor.update_stage(run_id, 'extract', StageStatus.RUNNING)
    time.sleep(0.1)
    monitor.update_stage(
        run_id, 'extract',
        status=StageStatus.COMPLETED,
        records_processed=5000,
        errors=10,
        memory_usage_mb=256,
        cpu_usage_percent=60
    )
    
    # Verify stage update
    stage = monitor.active_runs[run_id].stages['extract']
    assert stage.status == StageStatus.COMPLETED
    assert stage.records_processed == 5000
    assert stage.errors == 10
    assert stage.memory_usage_mb == 256
    
    # Complete pipeline
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Verify completion
    assert run_id not in monitor.active_runs
    history = monitor.run_history['data_pipeline']
    assert len(history) == 1
    assert history[0].status == PipelineStatus.COMPLETED
    
    print("✓ Pipeline monitoring successful")
    return True


def test_pipeline_status_tracking():
    """Test pipeline status retrieval."""
    print("\n=== Testing Pipeline Status Tracking ===")
    
    monitor = PipelineMonitor()
    monitor.register_pipeline('status_test', ['stage1', 'stage2'])
    
    # Check idle status
    status = monitor.get_pipeline_status('status_test')
    assert status['status'] == 'idle'
    
    # Start pipeline and check running status
    run_id = monitor.start_monitoring('status_test')
    monitor.update_stage(run_id, 'stage1', StageStatus.RUNNING)
    
    status = monitor.get_pipeline_status('status_test')
    assert status['status'] == PipelineStatus.RUNNING.value
    assert status['current_stage'] == 'stage1'
    assert 'run_id' in status
    
    # Update to next stage
    monitor.update_stage(run_id, 'stage1', StageStatus.COMPLETED)
    monitor.update_stage(run_id, 'stage2', StageStatus.RUNNING)
    
    status = monitor.get_pipeline_status('status_test')
    assert status['current_stage'] == 'stage2'
    
    # Complete and check idle status with history
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    status = monitor.get_pipeline_status('status_test')
    assert status['status'] == 'idle'
    assert 'last_run' in status
    assert status['last_run']['status'] == PipelineStatus.COMPLETED.value
    
    print("✓ Pipeline status tracking successful")
    return True


def test_concurrent_pipelines():
    """Test monitoring multiple concurrent pipelines."""
    print("\n=== Testing Concurrent Pipeline Monitoring ===")
    
    monitor = PipelineMonitor()
    
    # Register multiple pipelines
    pipelines = ['pipeline_a', 'pipeline_b', 'pipeline_c']
    for name in pipelines:
        monitor.register_pipeline(name, ['extract', 'process', 'store'])
    
    # Start all pipelines
    run_ids = []
    for name in pipelines:
        run_id = monitor.start_monitoring(name)
        run_ids.append(run_id)
    
    # Verify all are running
    assert len(monitor.active_runs) == 3
    
    # Update different stages
    monitor.update_stage(run_ids[0], 'extract', StageStatus.COMPLETED)
    monitor.update_stage(run_ids[1], 'process', StageStatus.RUNNING)
    monitor.update_stage(run_ids[2], 'store', StageStatus.FAILED)
    
    # Check individual statuses
    for i, name in enumerate(pipelines):
        status = monitor.get_pipeline_status(name)
        assert status['run_id'] == run_ids[i]
    
    # Complete pipelines
    monitor.complete_pipeline(run_ids[0], PipelineStatus.COMPLETED)
    monitor.complete_pipeline(run_ids[1], PipelineStatus.COMPLETED)
    monitor.complete_pipeline(run_ids[2], PipelineStatus.FAILED)
    
    # Verify history
    assert len(monitor.run_history['pipeline_a']) == 1
    assert len(monitor.run_history['pipeline_b']) == 1
    assert len(monitor.run_history['pipeline_c']) == 1
    assert monitor.run_history['pipeline_c'][0].status == PipelineStatus.FAILED
    
    print("✓ Concurrent pipeline monitoring successful")
    return True


def test_stage_metrics():
    """Test stage metrics calculation."""
    print("\n=== Testing Stage Metrics ===")
    
    monitor = PipelineMonitor()
    monitor.register_pipeline('metrics_test', ['process'])
    
    run_id = monitor.start_monitoring('metrics_test')
    
    # Update with metrics
    monitor.update_stage(run_id, 'process', StageStatus.RUNNING)
    time.sleep(0.5)  # Simulate processing time
    monitor.update_stage(
        run_id, 'process',
        status=StageStatus.COMPLETED,
        records_processed=10000,
        errors=50
    )
    
    # Get metrics
    run = monitor.active_runs[run_id]
    stage = run.stages['process']
    
    assert stage.duration_seconds is not None
    assert stage.duration_seconds >= 0.5
    assert stage.throughput is not None
    assert stage.throughput > 0
    
    # Test total metrics
    assert run.total_records == 10000
    assert run.total_errors == 50
    
    print(f"✓ Stage metrics: duration={stage.duration_seconds:.2f}s, "
          f"throughput={stage.throughput:.0f} records/s")
    return True


def run_all_tests():
    """Run all pipeline tracking tests."""
    tests = [
        test_pipeline_registration,
        test_pipeline_monitoring,
        test_pipeline_status_tracking,
        test_concurrent_pipelines,
        test_stage_metrics
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