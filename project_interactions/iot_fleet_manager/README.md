# IoT Fleet Manager - Task #42

A comprehensive Level 3 (Orchestration) IoT device fleet management system with advanced features for device provisioning, monitoring, firmware updates, and edge computing coordination.

## Features

### Core Capabilities
- **Device Management**
  - Device registration and provisioning
  - Certificate-based security
  - Device twin state management
  - Grouping and tagging system

- **Firmware Updates**
  - Orchestrated update campaigns
  - Progress tracking
  - Bulk update support
  - Version management

- **Telemetry & Monitoring**
  - Real-time data collection
  - Anomaly detection (threshold & statistical)
  - Time-series data storage
  - Metric filtering and queries

- **Command & Control**
  - Individual device commands
  - Bulk operations
  - Command queuing
  - Status tracking

### Advanced Features
- **Edge Computing**
  - Edge gateway registration
  - Function deployment
  - Distributed processing
  - Resource management

- **Location Services**
  - Geolocation tracking
  - Radius-based device search
  - Location updates
  - Distance calculations

- **Power Management**
  - Battery monitoring
  - Power optimization recommendations
  - Sleep mode configuration
  - Reporting frequency adjustment

- **Protocol Support**
  - MQTT
  - CoAP
  - HTTP
  - WebSocket

- **Cloud Integration**
  - AWS IoT
  - Azure IoT
  - Google Cloud IoT
  - Platform-agnostic design

## Usage

```python
from iot_fleet_manager_interaction import IoTFleetManager

# Initialize manager
manager = IoTFleetManager()

# Register device
device_id = await manager.register_device(
    "sensor-001",
    "temperature-sensor",
    {
        "location": {"lat": 37.7749, "lon": -122.4194},
        "capabilities": ["temperature", "humidity"],
        "tags": ["outdoor", "production"]
    }
)

# Provision device
await manager.provision_device(device_id, {
    "reporting_interval": 300,
    "temperature_unit": "celsius"
})

# Collect telemetry
await manager.collect_telemetry(device_id, "temperature", 25.5, "celsius")

# Update firmware
await manager.update_firmware(
    "fw-update-001",
    "2.0.0",
    [device_id],
    "https://updates.example.com/v2.0.0"
)

# Get fleet health
health = await manager.get_fleet_health()
print(f"Fleet health score: {health['health_score']}%")
```

## Testing

Run all tests:
```bash
python test_task_42.py
```

Run individual test suites:
```bash
cd tests
python test_device_management.py
python test_firmware_updates.py
python test_telemetry_processing.py
```

## Architecture

The system follows a modular architecture with these key components:

1. **IoTFleetManager** - Main orchestration class
2. **SecurityManager** - Certificate and authentication handling
3. **EdgeComputing** - Edge gateway coordination
4. **AnomalyDetector** - Real-time anomaly detection

## Security

- Certificate-based device authentication
- Secure command channels
- Certificate revocation support
- Validation and expiry management

## Performance

- Efficient telemetry storage (10,000 point limit)
- Asynchronous operations throughout
- Batch processing support
- Optimized location calculations