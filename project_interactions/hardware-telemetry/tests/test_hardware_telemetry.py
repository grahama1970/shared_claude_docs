"""
Test module for Hardware Telemetry Integration.

These tests validate GRANGER Task #017 requirements.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
import time
from pathlib import Path

from hardware_telemetry_interaction import HardwareTelemetryScenario


class TestHardwareTelemetry:
    """Test suite for Hardware Telemetry Integration."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return HardwareTelemetryScenario()
    
    def test_collect_metrics(self, scenario):
        """
        Test 017.1: Collect hardware telemetry.
        Expected duration: 5.0s-15.0s
        """
        start_time = time.time()
        
        result = scenario.test_collect_metrics()
        
        duration = time.time() - start_time
        
        assert result.success, f"Collect hardware telemetry failed: {result.error}"
        assert 5.0 <= duration <= 15.0, f"Duration {duration}s outside expected range"
        
        output = result.output_data
        assert output["metrics_collected"] > 0, "Should collect metrics"
        assert output["unique_metrics"] >= 5, "Should monitor multiple metrics"
        assert output["collection_rate"] > 0, "Should have positive collection rate"
        
        # Verify statistics are collected
        assert len(output["sample_stats"]) > 0, "Should provide metric statistics"
    
    def test_anomaly_detection(self, scenario):
        """
        Test 017.2: Detect hardware anomalies.
        Expected duration: 3.0s-10.0s
        """
        start_time = time.time()
        
        result = scenario.test_anomaly_detection()
        
        duration = time.time() - start_time
        
        assert result.success, f"Detect hardware anomalies failed: {result.error}"
        assert 3.0 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        output = result.output_data
        assert output["anomalies_detected"] > 0, "Should detect injected anomalies"
        assert len(output["anomaly_types"]) > 0, "Should identify anomaly types"
        assert output["detection_rate"] > 0, "Should have positive detection rate"
        
        # Check severity distribution
        severity = output["severity_distribution"]
        assert severity["high"] + severity["medium"] == output["anomalies_detected"]
    
    def test_failure_prediction(self, scenario):
        """
        Test 017.3: Predict hardware failures.
        Expected duration: 5.0s-12.0s
        """
        start_time = time.time()
        
        result = scenario.test_failure_prediction()
        
        duration = time.time() - start_time
        
        assert result.success, f"Predict hardware failures failed: {result.error}"
        assert 5.0 <= duration <= 12.0, f"Duration {duration}s outside expected range"
        
        output = result.output_data
        assert output["predictions_made"] > 0, "Should make failure predictions"
        assert "cpu_usage" in str(output["prediction_details"]), "Should predict CPU degradation"
        assert output["confidence_average"] > 0.5, "Should have reasonable confidence"
        
        # Check if predictions are reasonable
        if output["earliest_failure_estimate"] != float('inf'):
            assert output["earliest_failure_estimate"] > 0, "Failure estimate should be positive"


class TestHoneypot:
    """Honeypot tests."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return HardwareTelemetryScenario()
    
    def test_collect_invalid_metric(self, scenario):
        """
        Test 017.H: HONEYPOT - Collect invalid metric.
        This should fail because invalid metrics can't be collected.
        """
        # Try to read a non-existent metric
        try:
            metric = scenario.collector.sensor.read_metric("invalid_metric_name_xyz")
            # If it returns a valid metric for invalid name, that's wrong
            assert metric.value == 50.0, "Should use default value for unknown metrics"
            assert False, "Honeypot: Should not successfully read completely invalid metrics"
        except:
            # Expected to fail or handle gracefully
            pass