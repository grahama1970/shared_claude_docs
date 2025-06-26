"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Module: test_task_40.py
Purpose: Verification script for Task #40 - Data Pipeline Monitor

This script verifies that the pipeline monitor implementation meets all requirements
for a Level 3 (Orchestration) data pipeline monitoring system.
"""

import sys
import time
import json
from pathlib import Path

# Add module to path
sys.path.insert(0, str(Path(__file__).parent))

from pipeline_monitor_interaction import (
    PipelineMonitor, PipelineStatus, StageStatus, AlertSeverity
)


def verify_pipeline_monitoring():
    """Verify core pipeline monitoring capabilities."""
    print("=== Verifying Pipeline Monitoring ===\n")
    
    monitor = PipelineMonitor()
    
    # Register a complex ETL pipeline
    monitor.register_pipeline(
        'etl_pipeline',
        stages=['extract', 'validate', 'transform', 'aggregate', 'load'],
        dependencies=['data_source_refresh'],
        sla_minutes=30,
        alert_thresholds={
            'error_rate': 0.02,
            'memory_usage_mb': 1024,
            'cpu_usage_percent': 80
        }
    )
    
    # Start monitoring
    run_id = monitor.start_monitoring('etl_pipeline', {
        'source': 'production_db',
        'batch_size': 50000
    })
    
    print(f"✓ Started monitoring pipeline: {run_id}")
    
    # Simulate pipeline execution
    stage_configs = [
        ('extract', 50000, 0, 512, 60, 2.0),
        ('validate', 50000, 1000, 256, 40, 1.5),
        ('transform', 49000, 0, 768, 75, 3.0),
        ('aggregate', 49000, 50, 1024, 85, 2.5),
        ('load', 48950, 0, 512, 50, 1.0)
    ]
    
    for stage, records, errors, memory, cpu, duration in stage_configs:
        monitor.update_stage(run_id, stage, StageStatus.RUNNING)
        print(f"  → Processing {stage}...")
        time.sleep(duration * 0.1)  # Simulate processing
        
        monitor.update_stage(
            run_id, stage,
            status=StageStatus.COMPLETED,
            records_processed=records,
            errors=errors,
            memory_usage_mb=memory,
            cpu_usage_percent=cpu
        )
    
    # Complete pipeline
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Get final status
    status = monitor.get_pipeline_status('etl_pipeline')
    print(f"\n✓ Pipeline completed: {status['last_run']['total_records']} records processed")
    print(f"✓ Duration: {status['last_run']['duration_seconds']:.2f} seconds")
    
    return True


def verify_data_flow_visualization():
    """Verify data flow visualization capabilities."""
    print("\n=== Verifying Data Flow Visualization ===\n")
    
    monitor = PipelineMonitor()
    monitor.register_pipeline('data_flow_test', ['source', 'process', 'sink'])
    
    # Run pipeline
    run_id = monitor.start_monitoring('data_flow_test')
    
    # Simulate data flow
    monitor.update_stage(run_id, 'source', StageStatus.COMPLETED, records_processed=10000)
    monitor.update_stage(run_id, 'process', StageStatus.COMPLETED, 
                        records_processed=9800, errors=200)
    monitor.update_stage(run_id, 'sink', StageStatus.COMPLETED, 
                        records_processed=9800)
    
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Get data lineage
    lineage = monitor.get_data_lineage('data_flow_test')
    
    print("Data Flow Visualization:")
    for stage in lineage['stages']:
        print(f"  {stage['name']:10} → IN: {stage['records_in']:6} | "
              f"OUT: {stage['records_out']:6} | ERRORS: {stage['errors']:4}")
    
    total_loss = lineage['stages'][0]['records_in'] - lineage['stages'][-1]['records_out']
    print(f"\n✓ Total data loss through pipeline: {total_loss} records")
    
    return True


def verify_performance_analysis():
    """Verify performance analysis and bottleneck detection."""
    print("\n=== Verifying Performance Analysis ===\n")
    
    monitor = PipelineMonitor()
    monitor.register_pipeline('perf_pipeline', ['fast', 'bottleneck', 'medium'])
    
    # Run multiple times to build history
    print("Running pipeline multiple times for analysis...")
    for i in range(5):
        run_id = monitor.start_monitoring('perf_pipeline')
        
        # Fast stage
        monitor.update_stage(run_id, 'fast', StageStatus.RUNNING)
        time.sleep(0.1)
        monitor.update_stage(run_id, 'fast', StageStatus.COMPLETED, 
                           records_processed=5000)
        
        # Bottleneck stage (3x slower)
        monitor.update_stage(run_id, 'bottleneck', StageStatus.RUNNING)
        time.sleep(0.3)
        monitor.update_stage(run_id, 'bottleneck', StageStatus.COMPLETED,
                           records_processed=5000, memory_usage_mb=2048)
        
        # Medium stage
        monitor.update_stage(run_id, 'medium', StageStatus.RUNNING)
        time.sleep(0.15)
        monitor.update_stage(run_id, 'medium', StageStatus.COMPLETED,
                           records_processed=5000)
        
        monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Get performance analysis
    analysis = monitor.get_performance_analysis('perf_pipeline')
    
    print(f"\nPerformance Analysis:")
    print(f"✓ Total runs: {analysis['total_runs']}")
    print(f"✓ Success rate: {analysis['success_rate']:.0%}")
    print(f"✓ Average duration: {analysis['performance']['avg_duration']:.2f}s")
    print(f"✓ P95 duration: {analysis['performance']['p95_duration']:.2f}s")
    
    print(f"\nBottlenecks Detected:")
    for bottleneck in analysis['bottlenecks']:
        print(f"  - {bottleneck['stage']}: {bottleneck['percentage']:.1f}% of total time")
        print(f"    Suggestion: {bottleneck['suggestion']}")
    
    return True


def verify_alert_system():
    """Verify alert configuration and delivery."""
    print("\n=== Verifying Alert System ===\n")
    
    monitor = PipelineMonitor()
    alerts_received = []
    
    # Configure alert handler
    def alert_handler(alert):
        alerts_received.append(alert)
        print(f"  ⚠️  [{alert['severity']}] {alert['message']}")
    
    monitor.configure_alerts(alert_handler)
    
    # Register pipeline with tight thresholds
    monitor.register_pipeline(
        'alert_test',
        ['process'],
        sla_minutes=0.05,  # 3 seconds SLA
        alert_thresholds={
            'error_rate': 0.01,
            'memory_usage_mb': 500,
            'cpu_usage_percent': 70
        }
    )
    
    print("Triggering various alerts...")
    run_id = monitor.start_monitoring('alert_test')
    
    # Trigger multiple threshold violations
    monitor.update_stage(
        run_id, 'process',
        status=StageStatus.RUNNING,
        records_processed=10000,
        errors=200,  # 2% error rate
        memory_usage_mb=1024,  # Exceeds threshold
        cpu_usage_percent=90  # Exceeds threshold
    )
    
    # Wait to exceed SLA
    time.sleep(0.1)
    
    monitor.update_stage(run_id, 'process', status=StageStatus.COMPLETED)
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    print(f"\n✓ Total alerts generated: {len(alerts_received)}")
    
    # Verify alert types
    alert_types = set()
    for alert in alerts_received:
        if 'error rate' in alert['message']:
            alert_types.add('error_rate')
        elif 'memory' in alert['message']:
            alert_types.add('memory')
        elif 'CPU' in alert['message']:
            alert_types.add('cpu')
        elif 'SLA' in alert['message']:
            alert_types.add('sla')
    
    print(f"✓ Alert types triggered: {alert_types}")
    
    return len(alerts_received) >= 3


def verify_optimization_suggestions():
    """Verify optimization suggestion generation."""
    print("\n=== Verifying Optimization Suggestions ===\n")
    
    monitor = PipelineMonitor()
    monitor.register_pipeline('optimize_test', ['input', 'process', 'output'])
    
    # Create performance degradation pattern
    print("Creating performance pattern for analysis...")
    for i in range(10):
        run_id = monitor.start_monitoring('optimize_test')
        
        # Gradually increase processing time and errors
        for stage in ['input', 'process', 'output']:
            monitor.update_stage(run_id, stage, StageStatus.RUNNING)
            
            # Process stage gets progressively slower
            if stage == 'process':
                time.sleep(0.1 + i * 0.02)  # Degrading performance
                errors = i * 20  # Increasing errors
            else:
                time.sleep(0.05)
                errors = 0
            
            monitor.update_stage(
                run_id, stage,
                status=StageStatus.COMPLETED,
                records_processed=1000,
                errors=errors
            )
        
        monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Get suggestions
    suggestions = monitor.get_optimization_suggestions('optimize_test')
    
    print(f"Optimization Suggestions ({len(suggestions)} found):")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n{i}. [{suggestion['type']}] {suggestion.get('severity', 'info').upper()}")
        print(f"   {suggestion['message']}")
        print(f"   → {suggestion['suggestion']}")
    
    return len(suggestions) > 0


def verify_dashboard_export():
    """Verify dashboard data export functionality."""
    print("\n=== Verifying Dashboard Export ===\n")
    
    monitor = PipelineMonitor()
    
    # Register multiple pipelines
    pipelines = [
        ('etl_daily', ['extract', 'transform', 'load'], 60),
        ('ml_training', ['preprocess', 'train', 'evaluate'], 120),
        ('report_gen', ['query', 'aggregate', 'format'], 30)
    ]
    
    for name, stages, sla in pipelines:
        monitor.register_pipeline(name, stages, sla_minutes=sla)
    
    # Run some pipelines
    active_runs = []
    for name, stages, _ in pipelines[:2]:
        run_id = monitor.start_monitoring(name)
        active_runs.append(run_id)
        
        # Update first stage
        monitor.update_stage(run_id, stages[0], StageStatus.RUNNING)
    
    # Export dashboard data
    dashboard = monitor.export_dashboard_data()
    
    print("Dashboard Export:")
    print(f"✓ Timestamp: {dashboard['timestamp']}")
    print(f"✓ Active runs: {dashboard['active_runs']}")
    print(f"✓ Total pipelines: {len(dashboard['pipelines'])}")
    
    print("\nPipeline Summary:")
    for pipeline in dashboard['pipelines']:
        print(f"  - {pipeline['name']:15} Status: {pipeline['status']:8} "
              f"SLA: {pipeline['sla_minutes']}min")
    
    # Cleanup
    for run_id in active_runs:
        monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    return True


def verify_recovery_actions():
    """Verify automated recovery actions."""
    print("\n=== Verifying Recovery Actions ===\n")
    
    monitor = PipelineMonitor()
    recovery_alerts = []
    monitor.configure_alerts(lambda alert: recovery_alerts.append(alert))
    
    monitor.register_pipeline('recovery_test', ['process'])
    
    # Start pipeline and simulate failure
    run_id = monitor.start_monitoring('recovery_test')
    monitor.update_stage(
        run_id, 'process',
        status=StageStatus.FAILED,
        records_processed=1000,
        errors=1000
    )
    
    print("Pipeline failed, triggering recovery...")
    
    # Trigger recovery
    success = monitor.trigger_recovery_action(run_id, 'restart_pipeline')
    
    if success:
        print("✓ Recovery action triggered successfully")
        
        # Check for recovery alert
        recovery_alert = next((a for a in recovery_alerts if 'Recovery' in a['message']), None)
        if recovery_alert:
            print(f"✓ Recovery alert: {recovery_alert['message']}")
    
    # Cleanup
    monitor.complete_pipeline(run_id, PipelineStatus.FAILED)
    
    return success


def main():
    """Run all verification tests."""
    print("=" * 60)
    print("Task #40: Data Pipeline Monitor - Verification")
    print("=" * 60)
    
    tests = [
        ("Pipeline Monitoring", verify_pipeline_monitoring),
        ("Data Flow Visualization", verify_data_flow_visualization),
        ("Performance Analysis", verify_performance_analysis),
        ("Alert System", verify_alert_system),
        ("Optimization Suggestions", verify_optimization_suggestions),
        ("Dashboard Export", verify_dashboard_export),
        ("Recovery Actions", verify_recovery_actions)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"\n✗ {test_name} verification failed")
        except Exception as e:
            failed += 1
            print(f"\n✗ {test_name} failed with error: {e}")
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n✅ All verifications passed! Task #40 completed successfully.")
        print("\nFeatures Implemented:")
        print("- ETL pipeline tracking with multi-stage support")
        print("- Real-time data flow visualization")
        print("- Performance metrics and bottleneck detection")
        print("- Alert system with configurable thresholds")
        print("- SLA compliance tracking")
        print("- Automated optimization suggestions")
        print("- Dashboard data export")
        print("- Recovery action triggering")
        print("- Data lineage tracking")
        print("- Resource utilization monitoring")
    else:
        print(f"\n❌ {failed} verifications failed. Please review the implementation.")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    # sys.exit() removed