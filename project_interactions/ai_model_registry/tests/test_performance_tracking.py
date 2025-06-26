"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""Test performance tracking functionality"""

import sys
import time
from datetime import datetime, timedelta
sys.path.insert(0, "/home/graham/workspace/shared_claude_docs")

from project_interactions.ai_model_registry.ai_model_registry_interaction import (
    AIModelRegistry, ModelType, PerformanceMetric
)


def test_performance_logging():
    """Test performance metric logging"""
    registry = AIModelRegistry()
    
    # Register model and version
    model_id = registry.register_model(
        name="perf-test",
        model_type=ModelType.CLASSIFICATION,
        framework="tensorflow"
    )
    
    version = registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/perf.pb"
    )
    
    # Log performance metrics
    registry.log_performance(
        model_id=model_id,
        version="1.0.0",
        metrics={
            "latency_ms": 45.2,
            "throughput_qps": 220,
            "memory_mb": 512,
            "accuracy": 0.94
        },
        environment="production"
    )
    
    # Get performance history
    history = registry.get_performance_history(model_id, "1.0.0")
    assert len(history) > 0, "No performance history"
    assert history[0].metrics["latency_ms"] == 45.2, "Metric not logged"
    
    print("✓ Performance logging test passed")


def test_performance_aggregation():
    """Test performance metric aggregation"""
    registry = AIModelRegistry()
    
    # Setup
    model_id = registry.register_model(
        name="agg-test",
        model_type=ModelType.REGRESSION,
        framework="scikit-learn"
    )
    
    registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/agg.pkl"
    )
    
    # Log multiple metrics
    for i in range(5):
        registry.log_performance(
            model_id=model_id,
            version="1.0.0",
            metrics={
                "latency_ms": 40 + i * 2,
                "accuracy": 0.90 + i * 0.01
            }
        )
        time.sleep(0.01)
    
    # Get aggregated stats
    stats = registry.get_performance_stats(model_id, "1.0.0")
    
    assert stats["latency_ms"]["count"] == 5, "Wrong metric count"
    assert stats["latency_ms"]["mean"] == 44.0, "Wrong mean calculation"
    assert abs(stats["accuracy"]["max"] - 0.94) < 0.0001, f"Wrong max value: {stats['accuracy']['max']}"
    assert abs(stats["accuracy"]["min"] - 0.90) < 0.0001, f"Wrong min value: {stats['accuracy']['min']}"
    
    print("✓ Performance aggregation test passed")


def test_performance_comparison():
    """Test performance comparison between versions"""
    registry = AIModelRegistry()
    
    # Create model with two versions
    model_id = registry.register_model(
        name="compare-test",
        model_type=ModelType.IMAGE_CLASSIFICATION,
        framework="pytorch"
    )
    
    # Version 1
    v1 = registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/v1.pt"
    )
    
    registry.log_performance(
        model_id=model_id,
        version="1.0.0",
        metrics={"latency_ms": 100, "accuracy": 0.85}
    )
    
    # Version 2
    v2 = registry.create_version(
        model_id=model_id,
        version="2.0.0",
        path="/models/v2.pt"
    )
    
    registry.log_performance(
        model_id=model_id,
        version="2.0.0",
        metrics={"latency_ms": 80, "accuracy": 0.91}
    )
    
    # Compare versions
    comparison = registry.compare_versions(
        model_id=model_id,
        version1="1.0.0",
        version2="2.0.0",
        metrics=["latency_ms", "accuracy"]
    )
    
    assert comparison["latency_ms"]["improvement"] == 20.0, "Wrong latency improvement"
    assert comparison["accuracy"]["improvement"] == -0.06, "Wrong accuracy improvement"
    assert comparison["latency_ms"]["percent_change"] == 20.0, "Wrong percent change"
    
    print("✓ Performance comparison test passed")


def test_performance_alerts():
    """Test performance degradation alerts"""
    registry = AIModelRegistry()
    
    # Setup
    model_id = registry.register_model(
        name="alert-test",
        model_type=ModelType.NLP,
        framework="transformers"
    )
    
    registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/alert.bin"
    )
    
    # Set performance thresholds
    registry.set_performance_thresholds(
        model_id=model_id,
        version="1.0.0",
        thresholds={
            "latency_ms": {"max": 100},
            "accuracy": {"min": 0.90}
        }
    )
    
    # Log normal performance
    alerts = registry.log_performance(
        model_id=model_id,
        version="1.0.0",
        metrics={"latency_ms": 90, "accuracy": 0.92},
        check_alerts=True
    )
    
    assert len(alerts) == 0, "False alerts triggered"
    
    # Log degraded performance
    alerts = registry.log_performance(
        model_id=model_id,
        version="1.0.0",
        metrics={"latency_ms": 120, "accuracy": 0.88},
        check_alerts=True
    )
    
    assert len(alerts) == 2, "Alerts not triggered"
    assert any("latency_ms" in alert for alert in alerts), "Latency alert missing"
    assert any("accuracy" in alert for alert in alerts), "Accuracy alert missing"
    
    print("✓ Performance alerts test passed")


def test_performance_trends():
    """Test performance trend analysis"""
    registry = AIModelRegistry()
    
    # Setup
    model_id = registry.register_model(
        name="trend-test",
        model_type=ModelType.TIME_SERIES,
        framework="prophet"
    )
    
    registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/trend.pkl"
    )
    
    # Simulate degrading performance over time
    base_time = datetime.now()
    for i in range(10):
        registry.log_performance(
            model_id=model_id,
            version="1.0.0",
            metrics={
                "latency_ms": 50 + i * 5,  # Increasing latency
                "error_rate": 0.01 + i * 0.002  # Increasing errors
            },
            timestamp=base_time + timedelta(hours=i)
        )
    
    # Analyze trends
    trends = registry.analyze_performance_trends(
        model_id=model_id,
        version="1.0.0",
        window_hours=24
    )
    
    assert trends["latency_ms"]["trend"] == "increasing", "Latency trend not detected"
    assert trends["error_rate"]["trend"] == "increasing", "Error trend not detected"
    assert trends["latency_ms"]["change_rate"] > 0, "Positive change rate expected"
    
    print("✓ Performance trends test passed")


def test_environment_specific_tracking():
    """Test environment-specific performance tracking"""
    registry = AIModelRegistry()
    
    # Setup
    model_id = registry.register_model(
        name="env-test",
        model_type=ModelType.CUSTOM,
        framework="custom"
    )
    
    registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/env.model"
    )
    
    # Log metrics for different environments
    registry.log_performance(
        model_id=model_id,
        version="1.0.0",
        metrics={"latency_ms": 30, "cpu_usage": 25},
        environment="development"
    )
    
    registry.log_performance(
        model_id=model_id,
        version="1.0.0",
        metrics={"latency_ms": 45, "cpu_usage": 40},
        environment="staging"
    )
    
    registry.log_performance(
        model_id=model_id,
        version="1.0.0",
        metrics={"latency_ms": 60, "cpu_usage": 55},
        environment="production"
    )
    
    # Get environment-specific stats
    prod_stats = registry.get_performance_stats(
        model_id=model_id,
        version="1.0.0",
        environment="production"
    )
    
    dev_stats = registry.get_performance_stats(
        model_id=model_id,
        version="1.0.0",
        environment="development"
    )
    
    assert prod_stats["latency_ms"]["mean"] == 60, "Wrong production stats"
    assert dev_stats["latency_ms"]["mean"] == 30, "Wrong development stats"
    
    print("✓ Environment-specific tracking test passed")


if __name__ == "__main__":
    test_performance_logging()
    test_performance_aggregation()
    test_performance_comparison()
    test_performance_alerts()
    test_performance_trends()
    test_environment_specific_tracking()
    print("\n✅ All performance tracking tests passed")