"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Module: test_telemetry_processing.py
Purpose: Test telemetry collection and processing functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- asyncio: https://docs.python.org/3/library/asyncio.html

Example Usage:
>>> pytest test_telemetry_processing.py -v
"""

import asyncio
import pytest
from datetime import datetime, timedelta
import random
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from iot_fleet_manager_interaction import (
    IoTFleetManager, TelemetryData, AnomalyDetector
)


class TestTelemetryProcessing:
    """Test telemetry collection and processing"""
    
    @pytest.mark.asyncio
    async def test_telemetry_collection(self):
        """Test basic telemetry collection"""
        manager = IoTFleetManager()
        
        device_id = await manager.register_device("telemetry-001", "sensor")
        
        # Collect various telemetry
        telemetry_points = [
            ("temperature", 25.5, "celsius"),
            ("humidity", 65.2, "percent"),
            ("pressure", 1013.25, "hPa"),
            ("battery", 87.5, "percent")
        ]
        
        for metric, value, unit in telemetry_points:
            await manager.collect_telemetry(device_id, metric, value, unit)
        
        # Retrieve telemetry
        all_telemetry = await manager.get_device_telemetry(device_id)
        assert len(all_telemetry) == 4
        
        # Check specific metric
        temp_telemetry = await manager.get_device_telemetry(device_id, metric="temperature")
        assert len(temp_telemetry) == 1
        assert temp_telemetry[0].value == 25.5
        assert temp_telemetry[0].unit == "celsius"
    
    @pytest.mark.asyncio
    async def test_telemetry_time_filtering(self):
        """Test telemetry filtering by time range"""
        manager = IoTFleetManager()
        
        device_id = await manager.register_device("time-filter-001", "sensor")
        
        # Collect telemetry over time
        start_time = datetime.now()
        
        for i in range(10):
            await manager.collect_telemetry(device_id, "temperature", 20 + i)
            await asyncio.sleep(0.1)
        
        mid_time = datetime.now()
        
        for i in range(10):
            await manager.collect_telemetry(device_id, "temperature", 30 + i)
            await asyncio.sleep(0.1)
        
        end_time = datetime.now()
        
        # Get all telemetry
        all_data = await manager.get_device_telemetry(device_id)
        assert len(all_data) == 20
        
        # Get first half
        first_half = await manager.get_device_telemetry(
            device_id, start_time=start_time, end_time=mid_time
        )
        assert len(first_half) <= 10
        
        # Get second half
        second_half = await manager.get_device_telemetry(
            device_id, start_time=mid_time, end_time=end_time
        )
        assert len(second_half) <= 10
    
    @pytest.mark.asyncio
    async def test_anomaly_detection_threshold(self):
        """Test anomaly detection with thresholds"""
        manager = IoTFleetManager()
        
        device_id = await manager.register_device("anomaly-thresh-001", "sensor")
        
        # Normal temperature
        anomaly = await manager.collect_telemetry(device_id, "temperature", 25)
        assert anomaly is None
        
        # Extremely high temperature
        anomaly = await manager.collect_telemetry(device_id, "temperature", 150)
        assert anomaly is not None
        assert anomaly["type"] == "threshold_violation"
        assert anomaly["metric"] == "temperature"
        
        # Extremely low temperature
        anomaly = await manager.collect_telemetry(device_id, "temperature", -50)
        assert anomaly is not None
        assert anomaly["type"] == "threshold_violation"
    
    @pytest.mark.asyncio
    async def test_anomaly_detection_statistical(self):
        """Test statistical anomaly detection"""
        manager = IoTFleetManager()
        
        device_id = await manager.register_device("anomaly-stat-001", "sensor")
        
        # Establish baseline with normal values
        for _ in range(50):
            value = 20 + random.gauss(0, 2)  # Mean 20, std 2
            await manager.collect_telemetry(device_id, "custom_metric", value)
        
        # Normal value - no anomaly
        anomaly = await manager.collect_telemetry(device_id, "custom_metric", 22)
        assert anomaly is None
        
        # Extreme outlier - should trigger anomaly
        anomaly = await manager.collect_telemetry(device_id, "custom_metric", 50)
        assert anomaly is not None
        assert anomaly["type"] == "statistical_anomaly"
        assert anomaly["z_score"] > 3
    
    @pytest.mark.asyncio
    async def test_device_metric_updates(self):
        """Test device metric updates from telemetry"""
        manager = IoTFleetManager()
        
        device_id = await manager.register_device("metric-update-001", "sensor")
        device = manager.devices[device_id]
        
        # Initial state
        assert device.battery_level is None
        assert device.signal_strength is None
        
        # Update battery
        await manager.collect_telemetry(device_id, "battery", 75.5, "percent")
        assert device.battery_level == 75.5
        
        # Update signal strength
        await manager.collect_telemetry(device_id, "signal_strength", -85, "dBm")
        assert device.signal_strength == -85
        
        # Last seen should be updated
        old_last_seen = device.last_seen
        await asyncio.sleep(0.1)
        await manager.collect_telemetry(device_id, "temperature", 25)
        assert device.last_seen > old_last_seen
    
    @pytest.mark.asyncio
    async def test_power_optimization(self):
        """Test power management optimization"""
        manager = IoTFleetManager()
        
        device_id = await manager.register_device("power-opt-001", "sensor")
        
        # Simulate high-frequency reporting
        for i in range(110):
            await manager.collect_telemetry(device_id, "temperature", 20 + random.random())
            await manager.collect_telemetry(device_id, "battery", 100 - i * 0.8)
            await asyncio.sleep(0.01)
        
        # Set low signal strength
        await manager.collect_telemetry(device_id, "signal_strength", -110)
        
        # Run optimization
        optimization = await manager.optimize_power_management(device_id)
        
        assert "recommendations" in optimization
        assert len(optimization["recommendations"]) > 0
        
        # Should recommend reducing frequency
        freq_recommendations = [
            r for r in optimization["recommendations"] 
            if r["action"] == "reduce_reporting_frequency"
        ]
        assert len(freq_recommendations) > 0
    
    @pytest.mark.asyncio
    async def test_edge_computing_integration(self):
        """Test edge computing with telemetry"""
        manager = IoTFleetManager()
        
        # Register edge gateway
        await manager.edge_computing.register_edge_gateway(
            "edge-telemetry-001",
            ["compute", "filter"]
        )
        
        # Deploy temperature converter function
        edge_function = """
async def process(data):
    if data.get('metric') == 'temperature' and data.get('unit') == 'celsius':
        # Convert to Fahrenheit
        data['value'] = data['value'] * 9/5 + 32
        data['unit'] = 'fahrenheit'
        data['processed_by'] = 'edge'
    return data
"""
        
        await manager.edge_computing.deploy_edge_function(
            "temp-converter",
            "edge-telemetry-001",
            edge_function
        )
        
        # Process telemetry through edge function
        data = {
            'metric': 'temperature',
            'value': 25,
            'unit': 'celsius'
        }
        
        processed = await manager.edge_computing.execute_edge_function(
            "temp-converter", data
        )
        
        assert processed['value'] == 77  # 25°C = 77°F
        assert processed['unit'] == 'fahrenheit'
        assert processed['processed_by'] == 'edge'
    
    @pytest.mark.asyncio
    async def test_telemetry_storage_limits(self):
        """Test telemetry storage limits"""
        manager = IoTFleetManager()
        
        device_id = await manager.register_device("storage-limit-001", "sensor")
        
        # Generate lots of telemetry
        for i in range(11000):
            await manager.collect_telemetry(
                device_id, 
                "test_metric", 
                i,
                metadata={"index": i}
            )
        
        # Should keep only last 10000 points
        assert len(manager.telemetry_store) == 10000
        
        # Verify we kept the most recent ones
        all_telemetry = await manager.get_device_telemetry(device_id)
        values = [t.value for t in all_telemetry]
        assert min(values) >= 1000  # Old values should be removed


async def run_tests():
    """Run all telemetry processing tests"""
    print("📊 Running Telemetry Processing Tests")
    print("=" * 50)
    
    test = TestTelemetryProcessing()
    
    tests = [
        ("Telemetry Collection", test.test_telemetry_collection),
        ("Time Filtering", test.test_telemetry_time_filtering),
        ("Threshold Anomaly Detection", test.test_anomaly_detection_threshold),
        ("Statistical Anomaly Detection", test.test_anomaly_detection_statistical),
        ("Device Metric Updates", test.test_device_metric_updates),
        ("Power Optimization", test.test_power_optimization),
        ("Edge Computing Integration", test.test_edge_computing_integration),
        ("Storage Limits", test.test_telemetry_storage_limits),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            await test_func()
            print(f"✅ {name}")
            passed += 1
        except Exception as e:
            print(f"❌ {name}: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Telemetry Processing Tests: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_tests())
    exit(0 if success else 1)