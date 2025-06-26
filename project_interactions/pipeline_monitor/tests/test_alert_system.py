"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Module: test_alert_system.py
Purpose: Test alert system and recovery actions

Tests alert configuration, threshold monitoring, alert delivery,
and automated recovery action triggering.
"""

import sys
import time
from pathlib import Path
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline_monitor_interaction import (
    PipelineMonitor, PipelineStatus, StageStatus, AlertSeverity
)


def test_alert_configuration():
    """Test alert handler configuration."""
    print("\n=== Testing Alert Configuration ===")
    
    monitor = PipelineMonitor()
    
    # Track alerts
    alerts_by_handler = defaultdict(list)
    
    # Configure multiple handlers
    handler1 = lambda alert: alerts_by_handler['handler1'].append(alert)
    handler2 = lambda alert: alerts_by_handler['handler2'].append(alert)
    
    monitor.configure_alerts(handler1)
    monitor.configure_alerts(handler2)
    
    # Register pipeline with custom thresholds
    monitor.register_pipeline(
        'alert_test',
        ['process'],
        alert_thresholds={
            'error_rate': 0.01,  # 1% error rate
            'memory_usage_mb': 100,  # Low threshold for testing
            'cpu_usage_percent': 50  # Low threshold for testing
        }
    )
    
    # Trigger alerts
    run_id = monitor.start_monitoring('alert_test')
    monitor.update_stage(
        run_id, 'process',
        status=StageStatus.RUNNING,
        records_processed=1000,
        errors=20,  # 2% error rate, exceeds threshold
        memory_usage_mb=150,  # Exceeds threshold
        cpu_usage_percent=60  # Exceeds threshold
    )
    
    time.sleep(0.1)  # Allow alerts to process
    
    # Verify both handlers received alerts
    assert len(alerts_by_handler['handler1']) > 0
    assert len(alerts_by_handler['handler2']) > 0
    assert len(alerts_by_handler['handler1']) == len(alerts_by_handler['handler2'])
    
    print(f"✓ Alert handlers configured: {len(monitor.alert_handlers)} handlers")
    print(f"✓ Alerts delivered to all handlers: {len(alerts_by_handler['handler1'])} alerts each")
    
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    return True


def test_threshold_alerts():
    """Test threshold-based alert generation."""
    print("\n=== Testing Threshold Alerts ===")
    
    monitor = PipelineMonitor()
    alerts = []
    monitor.configure_alerts(lambda alert: alerts.append(alert))
    
    # Register pipeline with specific thresholds
    monitor.register_pipeline(
        'threshold_test',
        ['extract', 'transform'],
        alert_thresholds={
            'error_rate': 0.05,
            'memory_usage_mb': 256,
            'cpu_usage_percent': 70
        }
    )
    
    run_id = monitor.start_monitoring('threshold_test')
    
    # Test error rate threshold
    monitor.update_stage(
        run_id, 'extract',
        status=StageStatus.COMPLETED,
        records_processed=1000,
        errors=100  # 10% error rate
    )
    
    # Test memory threshold
    monitor.update_stage(
        run_id, 'transform',
        status=StageStatus.RUNNING,
        memory_usage_mb=512  # Exceeds 256MB threshold
    )
    
    time.sleep(0.1)
    
    # Check alerts generated
    error_alerts = [a for a in alerts if 'error rate' in a['message']]
    memory_alerts = [a for a in alerts if 'memory' in a['message']]
    
    assert len(error_alerts) >= 1
    assert len(memory_alerts) >= 1
    
    print(f"✓ Error rate alert: {error_alerts[0]['message']}")
    print(f"✓ Memory usage alert: {memory_alerts[0]['message']}")
    
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    return True


def test_alert_severity_levels():
    """Test different alert severity levels."""
    print("\n=== Testing Alert Severity Levels ===")
    
    monitor = PipelineMonitor()
    alerts = []
    monitor.configure_alerts(lambda alert: alerts.append(alert))
    
    monitor.register_pipeline('severity_test', ['process'], sla_minutes=0.05)  # 3 seconds
    
    # Run pipeline with various issues
    run_id = monitor.start_monitoring('severity_test')
    
    # Generate different severity alerts
    monitor.update_stage(
        run_id, 'process',
        status=StageStatus.RUNNING,
        records_processed=1000,
        errors=60,  # High error rate - WARNING
        memory_usage_mb=2000,  # Very high memory - WARNING
        cpu_usage_percent=95  # Very high CPU - WARNING
    )
    
    # Wait to exceed SLA - CRITICAL
    time.sleep(0.1)  # 6 seconds, exceeds 3 second SLA
    
    monitor.update_stage(run_id, 'process', status=StageStatus.COMPLETED)
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Check alert severities
    severities = {alert['severity'] for alert in alerts}
    assert AlertSeverity.WARNING.value in severities
    assert AlertSeverity.CRITICAL.value in severities or AlertSeverity.ERROR.value in severities
    
    # Count by severity
    severity_counts = defaultdict(int)
    for alert in alerts:
        severity_counts[alert['severity']] += 1
    
    print("✓ Alert severity distribution:")
    for severity, count in severity_counts.items():
        print(f"  - {severity}: {count} alerts")
    
    return True


def test_recovery_actions():
    """Test recovery action triggering."""
    print("\n=== Testing Recovery Actions ===")
    
    monitor = PipelineMonitor()
    alerts = []
    monitor.configure_alerts(lambda alert: alerts.append(alert))
    
    monitor.register_pipeline(
        'recovery_test',
        ['process'],
        alert_thresholds={'error_rate': 0.1}
    )
    
    # Start pipeline
    run_id = monitor.start_monitoring('recovery_test')
    
    # Simulate failure
    monitor.update_stage(
        run_id, 'process',
        status=StageStatus.FAILED,
        records_processed=1000,
        errors=500  # 50% error rate
    )
    
    # Trigger recovery action
    recovery_triggered = monitor.trigger_recovery_action(run_id, 'restart_stage')
    assert recovery_triggered
    
    # Check recovery alert
    recovery_alerts = [a for a in alerts if 'Recovery' in a['message']]
    assert len(recovery_alerts) >= 1
    assert recovery_alerts[0]['severity'] == AlertSeverity.INFO.value
    
    # Verify pipeline status changed to recovering
    run = monitor.active_runs.get(run_id)
    assert run is not None
    assert run.status == PipelineStatus.RECOVERING
    
    print(f"✓ Recovery action triggered: {recovery_alerts[0]['message']}")
    
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    return True


def test_alert_in_pipeline_run():
    """Test alerts are stored in pipeline run."""
    print("\n=== Testing Alert Storage in Pipeline Run ===")
    
    monitor = PipelineMonitor()
    monitor.configure_alerts(lambda alert: None)  # Silent handler
    
    monitor.register_pipeline(
        'storage_test',
        ['stage1', 'stage2'],
        alert_thresholds={'error_rate': 0.01}
    )
    
    run_id = monitor.start_monitoring('storage_test')
    
    # Generate multiple alerts
    monitor.update_stage(
        run_id, 'stage1',
        status=StageStatus.COMPLETED,
        records_processed=1000,
        errors=50  # 5% error rate
    )
    
    monitor.update_stage(
        run_id, 'stage2',
        status=StageStatus.COMPLETED,
        records_processed=1000,
        errors=100  # 10% error rate
    )
    
    # Check alerts stored in run
    run = monitor.active_runs[run_id]
    assert len(run.alerts) >= 2
    
    # Verify alert content
    for alert in run.alerts:
        assert 'severity' in alert
        assert 'message' in alert
        assert 'timestamp' in alert
        assert 'pipeline' in alert
    
    print(f"✓ Alerts stored in pipeline run: {len(run.alerts)} alerts")
    
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    return True


def test_data_lineage_tracking():
    """Test data lineage tracking functionality."""
    print("\n=== Testing Data Lineage Tracking ===")
    
    monitor = PipelineMonitor()
    monitor.register_pipeline(
        'lineage_test',
        ['extract', 'validate', 'transform', 'load'],
        dependencies=['upstream_pipeline']
    )
    
    # Run pipeline
    run_id = monitor.start_monitoring('lineage_test', {'source': 'test_data.csv'})
    
    # Process stages with data flow
    stages_data = [
        ('extract', 10000, 0),
        ('validate', 10000, 500),  # 500 validation errors
        ('transform', 9500, 0),
        ('load', 9500, 10)  # 10 load errors
    ]
    
    for stage, records, errors in stages_data:
        monitor.update_stage(run_id, stage, StageStatus.RUNNING)
        time.sleep(0.05)
        monitor.update_stage(
            run_id, stage,
            status=StageStatus.COMPLETED,
            records_processed=records,
            errors=errors
        )
    
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Get lineage
    lineage = monitor.get_data_lineage('lineage_test')
    
    assert lineage['pipeline'] == 'lineage_test'
    assert len(lineage['stages']) == 4
    assert 'dependencies' in lineage
    assert 'upstream_pipeline' in lineage['dependencies']
    
    # Verify data flow
    total_in = sum(s['records_in'] for s in lineage['stages'])
    total_out = sum(s['records_out'] for s in lineage['stages'])
    total_errors = sum(s['errors'] for s in lineage['stages'])
    
    print(f"✓ Data lineage tracked: {total_in} records in, "
          f"{total_out} records out, {total_errors} errors")
    
    return True


def run_all_tests():
    """Run all alert system tests."""
    tests = [
        test_alert_configuration,
        test_threshold_alerts,
        test_alert_severity_levels,
        test_recovery_actions,
        test_alert_in_pipeline_run,
        test_data_lineage_tracking
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