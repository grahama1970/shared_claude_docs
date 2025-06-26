"""
Test module for performance monitor interaction

Tests real-time performance monitoring capabilities including:
- Multi-module metric collection
- Anomaly detection
- Alert generation
- Performance bottleneck identification
"""

import asyncio
import pytest
import time
from typing import Dict, Any

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from performance_monitor_interaction import (
    PerformanceMonitor,
    ModuleMetrics,
    AlertLevel,
    AnomalyDetector
)


@pytest.mark.asyncio
async def test_module_metrics_recording():
    """Test that module metrics are properly recorded"""
    metrics = ModuleMetrics('test_module')
    
    # Add some requests
    for i in range(10):
        latency = 0.1 + i * 0.01
        metrics.add_request(latency, success=True)
    
    # Add some failed requests
    for i in range(2):
        metrics.add_request(0.2, success=False)
    
    stats = metrics.get_statistics()
    
    assert stats['latency_mean'] > 0
    assert stats['latency_p95'] > stats['latency_p50']
    assert stats['error_rate'] == 2 / 12  # 2 errors out of 12 requests
    assert metrics.request_count == 12


@pytest.mark.asyncio
async def test_performance_monitor_initialization():
    """Test performance monitor initialization"""
    monitor = PerformanceMonitor()
    
    assert monitor.thresholds['latency_p95'] == 0.500
    assert monitor.thresholds['error_rate'] == 0.05
    assert len(monitor.modules) == 0
    assert len(monitor.alerts) == 0


@pytest.mark.asyncio
async def test_single_module_monitoring():
    """Test monitoring a single module"""
    monitor = PerformanceMonitor()
    
    # Monitor for short duration
    result = await monitor.monitor_modules(['test_api'], duration=2.0)
    
    assert 'test_api' in result['modules']
    assert result['modules']['test_api']['metrics']['requests_per_second'] > 0
    assert result['summary']['total_modules'] == 1


@pytest.mark.asyncio
async def test_multi_module_parallel_monitoring():
    """Test monitoring multiple modules in parallel"""
    monitor = PerformanceMonitor()
    modules = ['api', 'database', 'cache']
    
    start_time = time.time()
    result = await monitor.monitor_modules(modules, duration=3.0)
    elapsed = time.time() - start_time
    
    # Should complete in roughly the duration time (parallel execution)
    assert elapsed < 4.0
    
    # All modules should be monitored
    for module in modules:
        assert module in result['modules']
        assert result['modules'][module]['total_requests'] > 0


@pytest.mark.asyncio
async def test_threshold_alert_generation():
    """Test that alerts are generated when thresholds are exceeded"""
    monitor = PerformanceMonitor()
    
    # Create a module with high latency
    module = ModuleMetrics('slow_service')
    
    # Add requests with high latency
    for _ in range(50):
        module.add_request(0.600)  # Above p95 threshold of 0.5s
    
    monitor.modules['slow_service'] = module
    stats = module.get_statistics()
    monitor.check_thresholds('slow_service', stats)
    
    # Should have generated alerts
    assert len(monitor.alerts) > 0
    
    # Check alert details
    latency_alerts = [a for a in monitor.alerts if a.metric_type == 'latency_p95']
    assert len(latency_alerts) > 0
    assert latency_alerts[0].level == AlertLevel.WARNING


@pytest.mark.asyncio
async def test_anomaly_detection():
    """Test anomaly detection functionality"""
    detector = AnomalyDetector(window_size=50)
    
    # Build baseline with normal values (with some variation)
    import random
    for _ in range(50):
        # Add small random variation to create a proper distribution
        value = 0.100 + random.uniform(-0.01, 0.01)
        detector.update_baseline('service', 'latency', value)
    
    # Normal value should not be anomalous
    z_score = detector.detect_anomaly('service', 'latency', 0.105)
    assert z_score is None
    
    # Extreme value should be anomalous
    z_score = detector.detect_anomaly('service', 'latency', 0.500)
    assert z_score is not None
    assert abs(z_score) > 3


@pytest.mark.asyncio
async def test_error_rate_monitoring():
    """Test error rate calculation and alerting"""
    monitor = PerformanceMonitor()
    module = ModuleMetrics('error_prone_service')
    
    # Add mix of successful and failed requests
    for i in range(100):
        success = i % 10 != 0  # 10% error rate
        module.add_request(0.100, success=success)
    
    monitor.modules['error_prone_service'] = module
    stats = module.get_statistics()
    
    assert abs(stats['error_rate'] - 0.10) < 0.01  # ~10% error rate
    
    # Check for error rate alerts
    monitor.check_thresholds('error_prone_service', stats)
    error_alerts = [a for a in monitor.alerts if a.metric_type == 'error_rate']
    assert len(error_alerts) > 0


@pytest.mark.asyncio
async def test_dashboard_data_structure():
    """Test dashboard data structure and content"""
    monitor = PerformanceMonitor()
    
    # Run short monitoring session
    await monitor.monitor_modules(['service1', 'service2'], duration=1.0)
    
    dashboard = monitor.get_dashboard_data()
    
    # Check structure
    assert 'timestamp' in dashboard
    assert 'modules' in dashboard
    assert 'alerts' in dashboard
    assert 'summary' in dashboard
    
    # Check summary
    assert dashboard['summary']['total_modules'] == 2
    assert 'active_alerts' in dashboard['summary']
    assert 'warning_alerts' in dashboard['summary']
    
    # Check module data
    for module_name in ['service1', 'service2']:
        assert module_name in dashboard['modules']
        module_data = dashboard['modules'][module_name]
        assert 'metrics' in module_data
        assert 'last_update' in module_data
        assert 'total_requests' in module_data


@pytest.mark.asyncio
async def test_performance_bottleneck_identification():
    """Test identification of performance bottlenecks"""
    monitor = PerformanceMonitor()
    
    # Create modules with different performance characteristics
    fast_module = ModuleMetrics('fast_service')
    slow_module = ModuleMetrics('slow_service')
    
    # Fast service
    for _ in range(50):
        fast_module.add_request(0.050)
    
    # Slow service (bottleneck)
    for _ in range(50):
        slow_module.add_request(0.900)
    
    monitor.modules['fast_service'] = fast_module
    monitor.modules['slow_service'] = slow_module
    
    dashboard = monitor.get_dashboard_data()
    
    # Identify slowest module
    slowest = None
    max_latency = 0
    
    for name, data in dashboard['modules'].items():
        latency = data['metrics']['latency_p95']
        if latency > max_latency:
            max_latency = latency
            slowest = name
    
    assert slowest == 'slow_service'
    assert max_latency > 0.800


@pytest.mark.asyncio
async def test_alert_severity_levels():
    """Test different alert severity levels"""
    monitor = PerformanceMonitor()
    module = ModuleMetrics('critical_service')
    
    # Create critical error rate (>10%)
    for i in range(100):
        success = i % 5 != 0  # 20% error rate
        module.add_request(0.100, success=success)
    
    monitor.modules['critical_service'] = module
    stats = module.get_statistics()
    monitor.check_thresholds('critical_service', stats)
    
    # Should have critical alert for high error rate
    critical_alerts = [a for a in monitor.alerts if a.level == AlertLevel.CRITICAL]
    assert len(critical_alerts) > 0


def test_expected_durations():
    """Test that monitoring operations complete within expected durations"""
    monitor = PerformanceMonitor()
    
    # Test short monitoring session
    start = time.time()
    asyncio.run(monitor.monitor_modules(['test'], duration=1.0))
    elapsed = time.time() - start
    
    # Should complete close to requested duration
    assert 0.9 < elapsed < 1.5


if __name__ == "__main__":
    # Run tests
    asyncio.run(test_module_metrics_recording())
    asyncio.run(test_performance_monitor_initialization())
    asyncio.run(test_single_module_monitoring())
    asyncio.run(test_multi_module_parallel_monitoring())
    asyncio.run(test_threshold_alert_generation())
    asyncio.run(test_anomaly_detection())
    asyncio.run(test_error_rate_monitoring())
    asyncio.run(test_dashboard_data_structure())
    asyncio.run(test_performance_bottleneck_identification())
    asyncio.run(test_alert_severity_levels())
    test_expected_durations()
    
    print("✅ All performance monitor tests passed!")