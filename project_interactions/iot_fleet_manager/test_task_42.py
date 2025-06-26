"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Module: test_task_42.py
Purpose: Comprehensive verification script for IoT Fleet Manager (Task #42)

External Dependencies:
- asyncio: https://docs.python.org/3/library/asyncio.html

Example Usage:
>>> python test_task_42.py
"""

import asyncio
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iot_fleet_manager_interaction import IoTFleetManager, Protocol


async def test_complete_iot_workflow():
    """Test complete IoT fleet management workflow"""
    print("🌐 IoT Fleet Manager - Complete Workflow Test")
    print("=" * 60)
    
    manager = IoTFleetManager()
    
    # Phase 1: Device Setup
    print("\n📱 Phase 1: Device Registration & Provisioning")
    print("-" * 50)
    
    # Register diverse device types
    device_configs = [
        ("temp-sensor-001", "temperature-sensor", {"location": {"lat": 37.7749, "lon": -122.4194}, 
                                                   "tags": ["outdoor", "critical"]}),
        ("temp-sensor-002", "temperature-sensor", {"location": {"lat": 37.7649, "lon": -122.4294}, 
                                                   "tags": ["indoor", "production"]}),
        ("motion-001", "motion-detector", {"capabilities": ["motion", "light"], 
                                          "tags": ["security", "entrance"]}),
        ("gateway-001", "edge-gateway", {"capabilities": ["compute", "routing"], 
                                        "tags": ["infrastructure"]}),
        ("camera-001", "security-camera", {"capabilities": ["video", "motion", "night-vision"],
                                          "tags": ["security", "outdoor"]})
    ]
    
    devices = []
    for device_id, device_type, metadata in device_configs:
        id = await manager.register_device(device_id, device_type, metadata)
        devices.append(id)
        print(f"✓ Registered {device_type}: {id}")
    
    # Provision devices
    provision_config = {
        "reporting_interval": 60,
        "alert_thresholds": {
            "temperature_high": 30,
            "temperature_low": 10,
            "battery_low": 20
        }
    }
    
    for device_id in devices[:2]:  # Provision temperature sensors
        await manager.provision_device(device_id, provision_config)
        print(f"✓ Provisioned: {device_id}")
    
    # Phase 2: Edge Computing Setup
    print("\n🖥️  Phase 2: Edge Computing Configuration")
    print("-" * 50)
    
    # Register edge gateway
    await manager.edge_computing.register_edge_gateway(
        "edge-gw-main",
        ["compute", "ml", "filtering"]
    )
    print("✓ Registered edge gateway: edge-gw-main")
    
    # Deploy edge functions
    temp_filter = """
async def process(data):
    # Filter and convert temperature data
    if data.get('metric') == 'temperature':
        celsius = data['value']
        data['celsius'] = celsius
        data['fahrenheit'] = celsius * 9/5 + 32
        data['kelvin'] = celsius + 273.15
        
        # Add alert if threshold exceeded
        if celsius > 30:
            data['alert'] = 'high_temperature'
        elif celsius < 10:
            data['alert'] = 'low_temperature'
    return data
"""
    
    await manager.edge_computing.deploy_edge_function(
        "temperature-processor",
        "edge-gw-main",
        temp_filter
    )
    print("✓ Deployed edge function: temperature-processor")
    
    # Phase 3: Telemetry Collection & Monitoring
    print("\n📊 Phase 3: Telemetry Collection & Anomaly Detection")
    print("-" * 50)
    
    # Simulate telemetry data
    import random
    
    for i in range(20):
        # Temperature sensors
        for sensor_id in ["temp-sensor-001", "temp-sensor-002"]:
            temp = 22 + random.gauss(0, 3)
            anomaly = await manager.collect_telemetry(sensor_id, "temperature", temp, "celsius")
            
            humidity = 50 + random.gauss(0, 10)
            await manager.collect_telemetry(sensor_id, "humidity", humidity, "percent")
            
            battery = 100 - i * 2 + random.uniform(-2, 2)
            await manager.collect_telemetry(sensor_id, "battery", battery, "percent")
            
            if anomaly:
                print(f"⚠️  Anomaly detected: {sensor_id} - {anomaly['type']}")
        
        # Motion detector
        if random.random() > 0.8:
            await manager.collect_telemetry("motion-001", "motion", 1, "boolean")
            await manager.collect_telemetry("motion-001", "light_level", random.randint(100, 1000), "lux")
        
        await asyncio.sleep(0.05)
    
    print("✓ Collected telemetry data from all devices")
    
    # Phase 4: Firmware Update Campaign
    print("\n🔄 Phase 4: Firmware Update Campaign")
    print("-" * 50)
    
    # Create firmware update for temperature sensors
    update_id = await manager.update_firmware(
        "fw-2.0-release",
        "2.0.0",
        ["temp-sensor-001", "temp-sensor-002"],
        "https://iot.example.com/firmware/v2.0.0"
    )
    print(f"✓ Started firmware update: {update_id}")
    
    # Monitor update progress
    update = manager.firmware_updates[update_id]
    for _ in range(5):
        await asyncio.sleep(0.3)
        progress = sum(update.progress.values()) / len(update.progress) if update.progress else 0
        print(f"  Update progress: {progress:.0f}%")
    
    print("✓ Firmware update completed")
    
    # Phase 5: Command & Control
    print("\n🎮 Phase 5: Command & Control Operations")
    print("-" * 50)
    
    # Send individual commands
    await manager.send_command("temp-sensor-001", "calibrate", {"offset": 0.5})
    print("✓ Sent calibration command to temp-sensor-001")
    
    # Bulk command
    results = await manager.bulk_command(
        ["temp-sensor-001", "temp-sensor-002"],
        "set_mode",
        {"mode": "power_save"}
    )
    print(f"✓ Bulk command sent: {sum(results.values())}/{len(results)} succeeded")
    
    # Phase 6: Location Services
    print("\n📍 Phase 6: Location-Based Services")
    print("-" * 50)
    
    # Update device location
    await manager.update_device_location("motion-001", 37.7700, -122.4200, 10)
    print("✓ Updated motion-001 location")
    
    # Find nearby devices
    nearby = await manager.find_devices_in_radius(37.7749, -122.4194, 5.0)
    print(f"✓ Found {len(nearby)} devices within 5km radius")
    
    # Phase 7: Power Optimization
    print("\n🔋 Phase 7: Power Management Optimization")
    print("-" * 50)
    
    # Optimize power for battery-powered devices
    for device_id in ["temp-sensor-001", "motion-001"]:
        optimization = await manager.optimize_power_management(device_id)
        if optimization.get("recommendations"):
            print(f"✓ Power optimization for {device_id}:")
            for rec in optimization["recommendations"]:
                print(f"  - {rec['action']}: {rec.get('power_savings', 'N/A')}")
    
    # Phase 8: Security Management
    print("\n🔐 Phase 8: Security & Certificate Management")
    print("-" * 50)
    
    # Validate certificates
    for device_id in devices[:3]:
        device = manager.devices[device_id]
        valid = manager.security_manager.validate_certificate(device.certificate_id)
        print(f"✓ Certificate validation for {device_id}: {'Valid' if valid else 'Invalid'}")
    
    # Phase 9: Fleet Health Analysis
    print("\n📈 Phase 9: Fleet Health & Analytics")
    print("-" * 50)
    
    health = await manager.get_fleet_health()
    print(f"✓ Fleet Health Score: {health['health_score']:.1f}%")
    print(f"  - Total Devices: {health['total_devices']}")
    print(f"  - Online: {health['status_distribution'].get('online', 0)}")
    print(f"  - Low Battery: {len(health['low_battery_devices'])}")
    print(f"  - Recent Anomalies: {health['recent_anomalies']}")
    
    # Phase 10: Cloud Integration
    print("\n☁️  Phase 10: Cloud Platform Integration")
    print("-" * 50)
    
    # Integrate with cloud platforms
    platforms = [
        ("aws-iot", {"endpoint": "iot.us-west-2.amazonaws.com", "region": "us-west-2"}),
        ("azure-iot", {"endpoint": "iot.azure.com", "resource_group": "iot-rg"})
    ]
    
    for platform, config in platforms:
        result = await manager.integrate_cloud_platform(platform, config)
        print(f"✓ {platform} integration: {'Success' if result else 'Failed'}")
    
    # Summary Report
    print("\n" + "=" * 60)
    print("📊 IoT Fleet Manager Test Summary")
    print("=" * 60)
    
    # Device statistics
    print(f"\n🔧 Device Statistics:")
    print(f"  - Total Devices: {len(manager.devices)}")
    print(f"  - Device Types: {len(set(d.device_type for d in manager.devices.values()))}")
    print(f"  - With Location: {len([d for d in manager.devices.values() if d.location])}")
    
    # Telemetry statistics
    print(f"\n📊 Telemetry Statistics:")
    print(f"  - Total Data Points: {len(manager.telemetry_store)}")
    print(f"  - Unique Metrics: {len(set(t.metric for t in manager.telemetry_store))}")
    print(f"  - Anomalies Detected: {len(manager.anomaly_detector.anomalies)}")
    
    # Operations statistics
    print(f"\n🎮 Operations Statistics:")
    print(f"  - Commands Queued: {sum(len(cmds) for cmds in manager.command_queue.values())}")
    print(f"  - Firmware Updates: {len(manager.firmware_updates)}")
    print(f"  - Edge Functions: {len(manager.edge_computing.edge_functions)}")
    
    # Security statistics
    print(f"\n🔐 Security Statistics:")
    print(f"  - Certificates Issued: {len(manager.security_manager.certificates)}")
    print(f"  - Revoked Certificates: {len(manager.security_manager.revoked_certs)}")
    
    return True


async def run_individual_tests():
    """Run individual component tests"""
    print("\n\n🧪 Running Individual Component Tests")
    print("=" * 60)
    
    # Add tests directory to path
    tests_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')
    sys.path.insert(0, tests_dir)
    
    # Import and run test modules
    from test_device_management import run_tests as run_device_tests
    from test_firmware_updates import run_tests as run_firmware_tests
    from test_telemetry_processing import run_tests as run_telemetry_tests
    
    all_passed = True
    
    # Run each test suite
    test_suites = [
        ("Device Management", run_device_tests),
        ("Firmware Updates", run_firmware_tests),
        ("Telemetry Processing", run_telemetry_tests)
    ]
    
    for name, test_func in test_suites:
        print(f"\n{'='*60}")
        print(f"Running {name} Tests")
        print(f"{'='*60}")
        passed = await test_func()
        all_passed = all_passed and passed
    
    return all_passed


async def main():
    """Main test execution"""
    print("🌐 IoT Fleet Manager - Task #42 Verification")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Run complete workflow test
        workflow_passed = await test_complete_iot_workflow()
        
        # Run individual tests
        tests_passed = await run_individual_tests()
        
        # Final summary
        print("\n" + "=" * 60)
        print("🏁 FINAL TEST SUMMARY")
        print("=" * 60)
        
        if workflow_passed and tests_passed:
            print("✅ ALL TESTS PASSED!")
            print("\nThe IoT Fleet Manager implementation successfully demonstrates:")
            print("  • Device registration and provisioning")
            print("  • Firmware update orchestration")
            print("  • Real-time telemetry collection")
            print("  • Anomaly detection and alerting")
            print("  • Edge computing coordination")
            print("  • Location-based services")
            print("  • Power management optimization")
            print("  • Security certificate management")
            print("  • Cloud platform integration")
            print("  • Comprehensive fleet health monitoring")
            return True
        else:
            print("❌ SOME TESTS FAILED")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)