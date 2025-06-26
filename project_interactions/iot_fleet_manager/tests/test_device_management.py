"""
Module: test_device_management.py
Purpose: Test device management functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- asyncio: https://docs.python.org/3/library/asyncio.html

Example Usage:
>>> pytest test_device_management.py -v
"""

import asyncio
import pytest
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from iot_fleet_manager_interaction import (
    IoTFleetManager, Device, DeviceStatus, Protocol, 
    DeviceTwin, GeoLocation
)


class TestDeviceManagement:
    """Test device management operations"""
    
    @pytest.mark.asyncio
    async def test_device_registration(self):
        """Test device registration with metadata"""
        manager = IoTFleetManager()
        
        # Register device with full metadata
        device_id = await manager.register_device(
            "test-sensor-001",
            "temperature-sensor",
            {
                "location": {"lat": 37.7749, "lon": -122.4194},
                "capabilities": ["temperature", "humidity", "pressure"],
                "tags": ["outdoor", "weather-station", "roof"]
            }
        )
        
        assert device_id == "test-sensor-001"
        assert device_id in manager.devices
        
        device = manager.devices[device_id]
        assert device.device_type == "temperature-sensor"
        assert device.certificate_id is not None
        assert "temperature" in device.capabilities
        assert "outdoor" in device.tags
        assert device.location is not None
        assert device.location.latitude == 37.7749
    
    @pytest.mark.asyncio
    async def test_device_provisioning(self):
        """Test device provisioning process"""
        manager = IoTFleetManager()
        
        device_id = await manager.register_device("prov-test-001", "sensor")
        
        # Provision with configuration
        config = {
            "reporting_interval": 300,
            "temperature_unit": "fahrenheit",
            "alerts": {
                "high_temp": 100,
                "low_battery": 10
            }
        }
        
        result = await manager.provision_device(device_id, config)
        assert result is True
        
        # Check device status
        device = manager.devices[device_id]
        assert device.status == DeviceStatus.ONLINE
        
        # Check device twin
        twin = manager.device_twins[device_id]
        assert twin.desired["reporting_interval"] == 300
        assert twin.version > 1
    
    @pytest.mark.asyncio
    async def test_device_groups(self):
        """Test device grouping functionality"""
        manager = IoTFleetManager()
        
        # Register devices with different tags
        devices = []
        for i in range(5):
            tags = ["production"] if i < 3 else ["development"]
            if i % 2 == 0:
                tags.append("critical")
            
            device_id = await manager.register_device(
                f"group-test-{i:03d}",
                "sensor",
                {"tags": tags}
            )
            devices.append(device_id)
        
        # Check group membership
        assert len(manager.device_groups["tag:production"]) == 3
        assert len(manager.device_groups["tag:development"]) == 2
        assert len(manager.device_groups["tag:critical"]) == 3
        assert len(manager.device_groups["type:sensor"]) == 5
    
    @pytest.mark.asyncio
    async def test_certificate_management(self):
        """Test security certificate operations"""
        manager = IoTFleetManager()
        
        device_id = await manager.register_device("cert-test-001", "sensor")
        device = manager.devices[device_id]
        cert_id = device.certificate_id
        
        # Validate certificate
        assert manager.security_manager.validate_certificate(cert_id) is True
        
        # Revoke certificate
        assert manager.security_manager.revoke_certificate(cert_id) is True
        
        # Validate revoked certificate
        assert manager.security_manager.validate_certificate(cert_id) is False
    
    @pytest.mark.asyncio
    async def test_device_location_tracking(self):
        """Test device location management"""
        manager = IoTFleetManager()
        
        # Register devices at different locations
        locations = [
            (37.7749, -122.4194),  # San Francisco
            (37.7849, -122.4094),  # Nearby
            (40.7128, -74.0060),   # New York
        ]
        
        device_ids = []
        for i, (lat, lon) in enumerate(locations):
            device_id = await manager.register_device(
                f"loc-test-{i:03d}",
                "gps-tracker",
                {"location": {"lat": lat, "lon": lon}}
            )
            device_ids.append(device_id)
        
        # Find devices near San Francisco
        nearby = await manager.find_devices_in_radius(37.7749, -122.4194, 10.0)
        assert len(nearby) == 2
        assert device_ids[0] in nearby
        assert device_ids[1] in nearby
        assert device_ids[2] not in nearby
        
        # Update location
        await manager.update_device_location(
            device_ids[2], 37.7649, -122.4294
        )
        
        # Check updated location
        nearby = await manager.find_devices_in_radius(37.7749, -122.4194, 10.0)
        assert len(nearby) == 3
    
    @pytest.mark.asyncio
    async def test_device_status_tracking(self):
        """Test device status management"""
        manager = IoTFleetManager()
        
        device_id = await manager.register_device("status-test-001", "sensor")
        device = manager.devices[device_id]
        
        # Initial status
        assert device.status == DeviceStatus.OFFLINE
        
        # Provision changes status
        await manager.provision_device(device_id, {})
        assert device.status == DeviceStatus.ONLINE
        
        # Firmware update changes status
        await manager.update_firmware(
            "fw-001", "2.0.0", [device_id], "http://update.url"
        )
        
        # Wait a bit for status change
        await asyncio.sleep(0.1)
        assert device.status == DeviceStatus.UPDATING
        
        # Wait for completion
        await asyncio.sleep(1)
        assert device.status == DeviceStatus.ONLINE
        assert device.firmware_version == "2.0.0"


async def run_tests():
    """Run all device management tests"""
    print("🔧 Running Device Management Tests")
    print("=" * 50)
    
    test = TestDeviceManagement()
    
    tests = [
        ("Device Registration", test.test_device_registration),
        ("Device Provisioning", test.test_device_provisioning),
        ("Device Groups", test.test_device_groups),
        ("Certificate Management", test.test_certificate_management),
        ("Location Tracking", test.test_device_location_tracking),
        ("Status Tracking", test.test_device_status_tracking),
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
    print(f"Device Management Tests: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_tests())
    exit(0 if success else 1)