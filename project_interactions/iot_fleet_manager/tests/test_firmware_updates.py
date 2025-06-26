"""
Module: test_firmware_updates.py
Purpose: Test firmware update functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- asyncio: https://docs.python.org/3/library/asyncio.html

Example Usage:
>>> pytest test_firmware_updates.py -v
"""

import asyncio
import pytest
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from iot_fleet_manager_interaction import (
    IoTFleetManager, FirmwareUpdate, UpdateStatus, DeviceStatus
)


class TestFirmwareUpdates:
    """Test firmware update operations"""
    
    @pytest.mark.asyncio
    async def test_create_firmware_update(self):
        """Test creating firmware update campaign"""
        manager = IoTFleetManager()
        
        # Register devices
        devices = []
        for i in range(3):
            device_id = await manager.register_device(f"fw-device-{i:03d}", "iot-device")
            devices.append(device_id)
        
        # Create firmware update
        update_id = await manager.update_firmware(
            "fw-update-test-001",
            "2.5.0",
            devices,
            "https://updates.example.com/firmware/v2.5.0.bin"
        )
        
        assert update_id in manager.firmware_updates
        
        update = manager.firmware_updates[update_id]
        assert update.version == "2.5.0"
        assert len(update.target_devices) == 3
        assert update.status == UpdateStatus.PENDING
    
    @pytest.mark.asyncio
    async def test_firmware_update_progress(self):
        """Test firmware update progress tracking"""
        manager = IoTFleetManager()
        
        # Register device
        device_id = await manager.register_device("fw-progress-001", "device")
        
        # Start update
        update_id = await manager.update_firmware(
            "fw-progress-update",
            "3.0.0",
            [device_id],
            "https://updates.example.com/v3.0.0"
        )
        
        update = manager.firmware_updates[update_id]
        
        # Check initial state
        assert update.status == UpdateStatus.PENDING
        
        # Wait for progress
        await asyncio.sleep(0.3)
        
        # Check progress
        assert device_id in update.progress
        assert update.progress[device_id] > 0
        
        # Wait for completion
        await asyncio.sleep(1)
        
        # Check completion
        assert update.status == UpdateStatus.COMPLETED
        assert update.progress[device_id] == 100.0
        
        # Check device updated
        device = manager.devices[device_id]
        assert device.firmware_version == "3.0.0"
    
    @pytest.mark.asyncio
    async def test_bulk_firmware_update(self):
        """Test updating multiple devices"""
        manager = IoTFleetManager()
        
        # Register many devices
        devices = []
        for i in range(10):
            device_id = await manager.register_device(
                f"bulk-fw-{i:03d}", 
                "sensor",
                {"tags": ["group1"] if i < 5 else ["group2"]}
            )
            devices.append(device_id)
        
        # Update only group1 devices
        group1_devices = devices[:5]
        update_id = await manager.update_firmware(
            "bulk-update-001",
            "4.0.0",
            group1_devices,
            "https://updates.example.com/v4.0.0"
        )
        
        # Wait for completion
        await asyncio.sleep(1.5)
        
        # Verify only group1 devices updated
        for i, device_id in enumerate(devices):
            device = manager.devices[device_id]
            if i < 5:
                assert device.firmware_version == "4.0.0"
            else:
                assert device.firmware_version == "1.0.0"  # Default version
    
    @pytest.mark.asyncio
    async def test_firmware_update_status_transitions(self):
        """Test firmware update status transitions"""
        manager = IoTFleetManager()
        
        device_id = await manager.register_device("fw-status-001", "device")
        
        # Track status changes
        update_id = await manager.update_firmware(
            "status-update-001",
            "5.0.0",
            [device_id],
            "https://updates.example.com/v5.0.0"
        )
        
        update = manager.firmware_updates[update_id]
        device = manager.devices[device_id]
        
        # Initial status
        assert update.status == UpdateStatus.PENDING
        assert device.status == DeviceStatus.OFFLINE
        
        # Provision device first
        await manager.provision_device(device_id, {})
        assert device.status == DeviceStatus.ONLINE
        
        # Wait for update to start
        await asyncio.sleep(0.1)
        assert device.status == DeviceStatus.UPDATING
        
        # Wait for completion
        await asyncio.sleep(1.5)
        assert device.status == DeviceStatus.ONLINE
        assert update.status == UpdateStatus.COMPLETED
    
    @pytest.mark.asyncio
    async def test_concurrent_updates(self):
        """Test handling concurrent firmware updates"""
        manager = IoTFleetManager()
        
        # Register devices
        devices = []
        for i in range(6):
            device_id = await manager.register_device(f"concurrent-{i:03d}", "device")
            devices.append(device_id)
        
        # Start multiple updates concurrently
        update_tasks = []
        
        # Update 1: devices 0-2 to version 2.0
        task1 = manager.update_firmware(
            "concurrent-update-1",
            "2.0.0",
            devices[:3],
            "https://updates.example.com/v2.0.0"
        )
        update_tasks.append(task1)
        
        # Update 2: devices 3-5 to version 3.0
        task2 = manager.update_firmware(
            "concurrent-update-2",
            "3.0.0",
            devices[3:],
            "https://updates.example.com/v3.0.0"
        )
        update_tasks.append(task2)
        
        # Wait for all updates to complete
        update_ids = await asyncio.gather(*update_tasks)
        await asyncio.sleep(1.5)
        
        # Verify correct versions
        for i, device_id in enumerate(devices):
            device = manager.devices[device_id]
            if i < 3:
                assert device.firmware_version == "2.0.0"
            else:
                assert device.firmware_version == "3.0.0"
    
    @pytest.mark.asyncio
    async def test_update_validation(self):
        """Test firmware update validation"""
        manager = IoTFleetManager()
        
        # Test with non-existent devices
        update_id = await manager.update_firmware(
            "invalid-update-001",
            "1.0.0",
            ["non-existent-device"],
            "https://updates.example.com/v1.0.0"
        )
        
        # Update should be created but won't affect any devices
        update = manager.firmware_updates[update_id]
        assert len(update.target_devices) == 1
        
        # Wait for processing
        await asyncio.sleep(1.5)
        
        # No progress should be recorded for non-existent device
        assert len(update.progress) == 0


async def run_tests():
    """Run all firmware update tests"""
    print("🔄 Running Firmware Update Tests")
    print("=" * 50)
    
    test = TestFirmwareUpdates()
    
    tests = [
        ("Create Firmware Update", test.test_create_firmware_update),
        ("Update Progress Tracking", test.test_firmware_update_progress),
        ("Bulk Firmware Update", test.test_bulk_firmware_update),
        ("Status Transitions", test.test_firmware_update_status_transitions),
        ("Concurrent Updates", test.test_concurrent_updates),
        ("Update Validation", test.test_update_validation),
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
    print(f"Firmware Update Tests: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_tests())
    exit(0 if success else 1)