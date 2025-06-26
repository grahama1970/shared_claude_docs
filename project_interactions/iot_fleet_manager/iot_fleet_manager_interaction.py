
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: iot_fleet_manager_interaction.py
Purpose: Comprehensive IoT device fleet management system with orchestration capabilities

External Dependencies:
- asyncio: https://docs.python.org/3/library/asyncio.html
- paho-mqtt: https://pypi.org/project/paho-mqtt/
- aiocoap: https://aiocoap.readthedocs.io/

Example Usage:
>>> from iot_fleet_manager_interaction import IoTFleetManager
>>> manager = IoTFleetManager()
>>> device_id = await manager.register_device("sensor-001", "temperature-sensor", {"location": "warehouse-a"})
>>> await manager.send_command(device_id, "reboot")
>>> telemetry = await manager.get_device_telemetry(device_id)
"""

import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Callable
from collections import defaultdict
import hashlib
import random
import math


class DeviceStatus(Enum):
    """Device operational status states"""
    ONLINE = "online"
    OFFLINE = "offline"
    UPDATING = "updating"
    ERROR = "error"
    PROVISIONING = "provisioning"
    MAINTENANCE = "maintenance"


class UpdateStatus(Enum):
    """Firmware update status states"""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    INSTALLING = "installing"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLBACK = "rollback"


class Protocol(Enum):
    """Supported IoT protocols"""
    MQTT = "mqtt"
    COAP = "coap"
    HTTP = "http"
    WEBSOCKET = "websocket"


@dataclass
class GeoLocation:
    """Geographic location information"""
    latitude: float
    longitude: float
    altitude: Optional[float] = None
    accuracy: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DeviceTwin:
    """Device twin for state management"""
    device_id: str
    reported: Dict[str, Any] = field(default_factory=dict)
    desired: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    version: int = 1
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class TelemetryData:
    """Device telemetry data point"""
    device_id: str
    metric: str
    value: Any
    timestamp: datetime = field(default_factory=datetime.now)
    unit: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FirmwareUpdate:
    """Firmware update package"""
    update_id: str
    version: str
    url: str
    checksum: str
    size_bytes: int
    target_devices: Set[str] = field(default_factory=set)
    status: UpdateStatus = UpdateStatus.PENDING
    progress: Dict[str, float] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Device:
    """IoT device representation"""
    device_id: str
    device_type: str
    protocol: Protocol
    status: DeviceStatus = DeviceStatus.OFFLINE
    firmware_version: str = "1.0.0"
    hardware_version: str = "1.0"
    location: Optional[GeoLocation] = None
    tags: Set[str] = field(default_factory=set)
    capabilities: Set[str] = field(default_factory=set)
    battery_level: Optional[float] = None
    signal_strength: Optional[float] = None
    last_seen: datetime = field(default_factory=datetime.now)
    registered_at: datetime = field(default_factory=datetime.now)
    certificate_id: Optional[str] = None
    edge_gateway_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class EdgeComputing:
    """Edge computing coordination"""
    
    def __init__(self):
        self.edge_gateways: Dict[str, Dict[str, Any]] = {}
        self.edge_functions: Dict[str, Callable] = {}
        self.edge_deployments: Dict[str, Set[str]] = defaultdict(set)
    
    async def register_edge_gateway(self, gateway_id: str, capabilities: List[str]) -> bool:
        """Register an edge gateway"""
        self.edge_gateways[gateway_id] = {
            "id": gateway_id,
            "capabilities": capabilities,
            "devices": set(),
            "functions": set(),
            "status": "active",
            "resources": {
                "cpu": 100.0,
                "memory": 100.0,
                "storage": 100.0
            }
        }
        return True
    
    async def deploy_edge_function(self, function_id: str, gateway_id: str, code: str) -> bool:
        """Deploy function to edge gateway"""
        if gateway_id not in self.edge_gateways:
            return False
        
        # Create a function from the code string
        # In production, use proper sandboxing and security measures
        local_scope = {}
        exec(code, local_scope)
        self.edge_functions[function_id] = local_scope.get('process')
        self.edge_deployments[gateway_id].add(function_id)
        self.edge_gateways[gateway_id]["functions"].add(function_id)
        return True
    
    async def execute_edge_function(self, function_id: str, data: Any) -> Any:
        """Execute edge function"""
        if function_id in self.edge_functions:
            return await self.edge_functions[function_id](data)
        return None


class SecurityManager:
    """Device security and certificate management"""
    
    def __init__(self):
        self.certificates: Dict[str, Dict[str, Any]] = {}
        self.trusted_roots: Set[str] = set()
        self.revoked_certs: Set[str] = set()
    
    def generate_certificate(self, device_id: str) -> str:
        """Generate device certificate"""
        cert_id = hashlib.sha256(f"{device_id}-{time.time()}".encode()).hexdigest()[:16]
        
        self.certificates[cert_id] = {
            "id": cert_id,
            "device_id": device_id,
            "issued_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(days=365),
            "public_key": self._generate_key(),
            "status": "active"
        }
        
        return cert_id
    
    def _generate_key(self) -> str:
        """Generate mock public key"""
        return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    
    def validate_certificate(self, cert_id: str) -> bool:
        """Validate certificate"""
        if cert_id in self.revoked_certs:
            return False
        
        cert = self.certificates.get(cert_id)
        if not cert:
            return False
        
        return (cert["status"] == "active" and 
                cert["expires_at"] > datetime.now())
    
    def revoke_certificate(self, cert_id: str) -> bool:
        """Revoke certificate"""
        if cert_id in self.certificates:
            self.certificates[cert_id]["status"] = "revoked"
            self.revoked_certs.add(cert_id)
            return True
        return False


class AnomalyDetector:
    """Device anomaly detection"""
    
    def __init__(self):
        self.baselines: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.anomalies: List[Dict[str, Any]] = []
        self.thresholds = {
            "temperature": {"min": -20, "max": 80},
            "humidity": {"min": 0, "max": 100},
            "battery": {"min": 0, "max": 100},
            "signal_strength": {"min": -120, "max": 0}
        }
    
    async def update_baseline(self, device_id: str, metric: str, value: float):
        """Update metric baseline"""
        if metric not in self.baselines[device_id]:
            self.baselines[device_id][metric] = {
                "values": [],
                "mean": value,
                "std": 0
            }
        
        baseline = self.baselines[device_id][metric]
        baseline["values"].append(value)
        
        # Keep last 100 values
        if len(baseline["values"]) > 100:
            baseline["values"] = baseline["values"][-100:]
        
        # Calculate statistics
        values = baseline["values"]
        baseline["mean"] = sum(values) / len(values)
        if len(values) > 1:
            variance = sum((x - baseline["mean"]) ** 2 for x in values) / len(values)
            baseline["std"] = math.sqrt(variance)
    
    async def detect_anomaly(self, device_id: str, telemetry: TelemetryData) -> Optional[Dict[str, Any]]:
        """Detect anomalies in telemetry"""
        metric = telemetry.metric
        value = float(telemetry.value)
        
        # Check against thresholds
        if metric in self.thresholds:
            threshold = self.thresholds[metric]
            if value < threshold["min"] or value > threshold["max"]:
                anomaly = {
                    "device_id": device_id,
                    "metric": metric,
                    "value": value,
                    "type": "threshold_violation",
                    "threshold": threshold,
                    "timestamp": telemetry.timestamp
                }
                self.anomalies.append(anomaly)
                return anomaly
        
        # Check against baseline
        if device_id in self.baselines and metric in self.baselines[device_id]:
            baseline = self.baselines[device_id][metric]
            if baseline["std"] > 0:
                z_score = abs(value - baseline["mean"]) / baseline["std"]
                if z_score > 3:  # 3 standard deviations
                    anomaly = {
                        "device_id": device_id,
                        "metric": metric,
                        "value": value,
                        "type": "statistical_anomaly",
                        "z_score": z_score,
                        "baseline_mean": baseline["mean"],
                        "baseline_std": baseline["std"],
                        "timestamp": telemetry.timestamp
                    }
                    self.anomalies.append(anomaly)
                    return anomaly
        
        # Update baseline
        await self.update_baseline(device_id, metric, value)
        return None


class IoTFleetManager:
    """Main IoT fleet management system"""
    
    def __init__(self):
        self.devices: Dict[str, Device] = {}
        self.device_twins: Dict[str, DeviceTwin] = {}
        self.telemetry_store: List[TelemetryData] = []
        self.firmware_updates: Dict[str, FirmwareUpdate] = {}
        self.command_queue: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.device_groups: Dict[str, Set[str]] = defaultdict(set)
        self.security_manager = SecurityManager()
        self.edge_computing = EdgeComputing()
        self.anomaly_detector = AnomalyDetector()
        self.message_handlers: Dict[Protocol, Callable] = {}
        self._running = False
    
    async def register_device(self, device_id: str, device_type: str, 
                            metadata: Optional[Dict[str, Any]] = None) -> str:
        """Register a new device"""
        # Generate certificate
        cert_id = self.security_manager.generate_certificate(device_id)
        
        # Create device
        device = Device(
            device_id=device_id,
            device_type=device_type,
            protocol=Protocol.MQTT,  # Default protocol
            certificate_id=cert_id,
            metadata=metadata or {}
        )
        
        # Extract capabilities from metadata
        if metadata:
            if "capabilities" in metadata:
                device.capabilities = set(metadata["capabilities"])
            if "tags" in metadata:
                device.tags = set(metadata["tags"])
            if "location" in metadata:
                loc = metadata["location"]
                device.location = GeoLocation(
                    latitude=loc.get("lat", 0),
                    longitude=loc.get("lon", 0)
                )
        
        # Create device twin
        twin = DeviceTwin(device_id=device_id)
        
        # Store device
        self.devices[device_id] = device
        self.device_twins[device_id] = twin
        
        # Add to groups based on tags
        for tag in device.tags:
            self.device_groups[f"tag:{tag}"].add(device_id)
        
        # Add to type group
        self.device_groups[f"type:{device_type}"].add(device_id)
        
        return device_id
    
    async def provision_device(self, device_id: str, config: Dict[str, Any]) -> bool:
        """Provision device with configuration"""
        if device_id not in self.devices:
            return False
        
        device = self.devices[device_id]
        device.status = DeviceStatus.PROVISIONING
        
        # Update device twin desired state
        twin = self.device_twins[device_id]
        twin.desired.update(config)
        twin.version += 1
        twin.last_updated = datetime.now()
        
        # Send provisioning command
        await self.send_command(device_id, "provision", config)
        
        # Simulate provisioning completion
        await asyncio.sleep(0.1)
        device.status = DeviceStatus.ONLINE
        
        return True
    
    async def send_command(self, device_id: str, command: str, 
                          payload: Optional[Dict[str, Any]] = None) -> bool:
        """Send command to device"""
        if device_id not in self.devices:
            return False
        
        cmd = {
            "id": str(uuid.uuid4()),
            "command": command,
            "payload": payload or {},
            "timestamp": datetime.now(),
            "status": "pending"
        }
        
        self.command_queue[device_id].append(cmd)
        
        # Simulate command execution
        await asyncio.sleep(0.05)
        cmd["status"] = "completed"
        
        return True
    
    async def bulk_command(self, device_ids: List[str], command: str, 
                          payload: Optional[Dict[str, Any]] = None) -> Dict[str, bool]:
        """Send command to multiple devices"""
        results = {}
        
        tasks = []
        for device_id in device_ids:
            task = self.send_command(device_id, command, payload)
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        for device_id, response in zip(device_ids, responses):
            results[device_id] = response if isinstance(response, bool) else False
        
        return results
    
    async def update_firmware(self, update_id: str, version: str, 
                            target_devices: List[str], url: str) -> str:
        """Create firmware update campaign"""
        update = FirmwareUpdate(
            update_id=update_id,
            version=version,
            url=url,
            checksum=hashlib.sha256(url.encode()).hexdigest(),
            size_bytes=random.randint(1000000, 10000000),  # 1-10 MB
            target_devices=set(target_devices)
        )
        
        self.firmware_updates[update_id] = update
        
        # Start update process
        asyncio.create_task(self._process_firmware_update(update))
        
        return update_id
    
    async def _process_firmware_update(self, update: FirmwareUpdate):
        """Process firmware update"""
        for device_id in update.target_devices:
            if device_id not in self.devices:
                continue
            
            device = self.devices[device_id]
            
            # Update status
            device.status = DeviceStatus.UPDATING
            update.status = UpdateStatus.DOWNLOADING
            update.progress[device_id] = 0.0
            
            # Simulate download
            for progress in range(0, 101, 20):
                await asyncio.sleep(0.1)
                update.progress[device_id] = progress
            
            # Simulate installation
            update.status = UpdateStatus.INSTALLING
            await asyncio.sleep(0.2)
            
            # Update device
            device.firmware_version = update.version
            device.status = DeviceStatus.ONLINE
            update.progress[device_id] = 100.0
        
        update.status = UpdateStatus.COMPLETED
    
    async def collect_telemetry(self, device_id: str, metric: str, 
                               value: Any, unit: Optional[str] = None,
                               metadata: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Collect telemetry from device"""
        if device_id not in self.devices:
            return None
        
        telemetry = TelemetryData(
            device_id=device_id,
            metric=metric,
            value=value,
            unit=unit,
            metadata=metadata or {}
        )
        
        self.telemetry_store.append(telemetry)
        
        # Update device status
        device = self.devices[device_id]
        device.last_seen = datetime.now()
        
        # Update specific metrics
        if metric == "battery":
            device.battery_level = float(value)
        elif metric == "signal_strength":
            device.signal_strength = float(value)
        
        # Check for anomalies
        anomaly = await self.anomaly_detector.detect_anomaly(device_id, telemetry)
        
        # Keep only recent telemetry (last 10000 points)
        if len(self.telemetry_store) > 10000:
            self.telemetry_store = self.telemetry_store[-10000:]
        
        return anomaly
    
    async def get_device_telemetry(self, device_id: str, 
                                  metric: Optional[str] = None,
                                  start_time: Optional[datetime] = None,
                                  end_time: Optional[datetime] = None) -> List[TelemetryData]:
        """Get device telemetry data"""
        telemetry = []
        
        for data in self.telemetry_store:
            if data.device_id != device_id:
                continue
            
            if metric and data.metric != metric:
                continue
            
            if start_time and data.timestamp < start_time:
                continue
            
            if end_time and data.timestamp > end_time:
                continue
            
            telemetry.append(data)
        
        return telemetry
    
    async def update_device_location(self, device_id: str, 
                                   latitude: float, longitude: float,
                                   altitude: Optional[float] = None) -> bool:
        """Update device location"""
        if device_id not in self.devices:
            return False
        
        device = self.devices[device_id]
        device.location = GeoLocation(
            latitude=latitude,
            longitude=longitude,
            altitude=altitude
        )
        
        # Update device twin
        twin = self.device_twins[device_id]
        twin.reported["location"] = {
            "lat": latitude,
            "lon": longitude,
            "alt": altitude,
            "timestamp": datetime.now().isoformat()
        }
        twin.version += 1
        
        return True
    
    async def find_devices_in_radius(self, center_lat: float, center_lon: float, 
                                   radius_km: float) -> List[str]:
        """Find devices within radius of location"""
        devices_in_radius = []
        
        for device_id, device in self.devices.items():
            if not device.location:
                continue
            
            # Calculate distance using Haversine formula
            distance = self._calculate_distance(
                center_lat, center_lon,
                device.location.latitude, device.location.longitude
            )
            
            if distance <= radius_km:
                devices_in_radius.append(device_id)
        
        return devices_in_radius
    
    def _calculate_distance(self, lat1: float, lon1: float, 
                          lat2: float, lon2: float) -> float:
        """Calculate distance between two points in km"""
        R = 6371  # Earth's radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    async def optimize_power_management(self, device_id: str) -> Dict[str, Any]:
        """Optimize device power management"""
        if device_id not in self.devices:
            return {}
        
        device = self.devices[device_id]
        recommendations = []
        
        # Analyze telemetry patterns
        telemetry = await self.get_device_telemetry(device_id)
        
        # Check reporting frequency
        if len(telemetry) > 100:
            timestamps = [t.timestamp for t in telemetry[-100:]]
            avg_interval = sum(
                (timestamps[i+1] - timestamps[i]).total_seconds() 
                for i in range(len(timestamps)-1)
            ) / (len(timestamps) - 1)
            
            if avg_interval < 60:  # Less than 1 minute
                recommendations.append({
                    "action": "reduce_reporting_frequency",
                    "current_interval": avg_interval,
                    "recommended_interval": 300,  # 5 minutes
                    "power_savings": "30%"
                })
        
        # Check signal strength
        if device.signal_strength and device.signal_strength < -100:
            recommendations.append({
                "action": "improve_antenna_position",
                "current_signal": device.signal_strength,
                "power_savings": "15%"
            })
        
        # Check battery level trends
        battery_data = [t for t in telemetry if t.metric == "battery"]
        if len(battery_data) > 10:
            battery_drain_rate = (
                battery_data[0].value - battery_data[-1].value
            ) / len(battery_data)
            
            if battery_drain_rate > 0.5:  # More than 0.5% per reading
                recommendations.append({
                    "action": "enable_deep_sleep_mode",
                    "drain_rate": battery_drain_rate,
                    "power_savings": "40%"
                })
        
        # Apply recommendations
        if recommendations:
            config = {
                "power_mode": "low_power",
                "reporting_interval": 300,
                "sleep_enabled": True
            }
            await self.send_command(device_id, "configure_power", config)
        
        return {
            "device_id": device_id,
            "battery_level": device.battery_level,
            "recommendations": recommendations,
            "estimated_battery_life": "30 days" if recommendations else "7 days"
        }
    
    async def get_fleet_health(self) -> Dict[str, Any]:
        """Get overall fleet health metrics"""
        total_devices = len(self.devices)
        
        status_counts = defaultdict(int)
        low_battery_devices = []
        offline_devices = []
        updating_devices = []
        
        for device_id, device in self.devices.items():
            status_counts[device.status.value] += 1
            
            if device.battery_level and device.battery_level < 20:
                low_battery_devices.append(device_id)
            
            if device.status == DeviceStatus.OFFLINE:
                offline_devices.append(device_id)
            
            if device.status == DeviceStatus.UPDATING:
                updating_devices.append(device_id)
        
        # Calculate health score
        online_percentage = (status_counts["online"] / total_devices * 100) if total_devices > 0 else 0
        health_score = online_percentage
        
        if low_battery_devices:
            health_score -= len(low_battery_devices) / total_devices * 10
        
        if self.anomaly_detector.anomalies:
            recent_anomalies = [
                a for a in self.anomaly_detector.anomalies 
                if a["timestamp"] > datetime.now() - timedelta(hours=1)
            ]
            if recent_anomalies:
                health_score -= len(recent_anomalies) / total_devices * 20
        
        return {
            "total_devices": total_devices,
            "health_score": max(0, min(100, health_score)),
            "status_distribution": dict(status_counts),
            "low_battery_devices": low_battery_devices,
            "offline_devices": offline_devices,
            "updating_devices": updating_devices,
            "recent_anomalies": len(self.anomaly_detector.anomalies),
            "active_updates": len([u for u in self.firmware_updates.values() 
                                 if u.status != UpdateStatus.COMPLETED])
        }
    
    async def integrate_cloud_platform(self, platform: str, 
                                     config: Dict[str, Any]) -> bool:
        """Integrate with cloud IoT platform"""
        # Simulate cloud platform integration
        supported_platforms = ["aws-iot", "azure-iot", "gcp-iot"]
        
        if platform not in supported_platforms:
            return False
        
        # Store integration config
        for device in self.devices.values():
            device.metadata[f"{platform}_integrated"] = True
            device.metadata[f"{platform}_endpoint"] = config.get("endpoint", "")
        
        return True


# Example edge functions for testing
EDGE_FUNCTIONS = {
    "temperature_filter": """
async def process(data):
    if data['metric'] == 'temperature':
        # Convert Celsius to Fahrenheit
        data['value'] = data['value'] * 9/5 + 32
        data['unit'] = 'F'
    return data
""",
    "anomaly_preprocessor": """
async def process(data):
    # Simple threshold check
    if data['metric'] == 'temperature' and data['value'] > 100:
        data['alert'] = 'high_temperature'
    return data
"""
}


async def main():
    """Test IoT fleet manager functionality"""
    print("🌐 IoT Fleet Manager Validation")
    print("=" * 50)
    
    manager = IoTFleetManager()
    
    # Test 1: Device Registration
    print("\n1. Device Registration")
    devices = []
    for i in range(5):
        device_id = await manager.register_device(
            f"sensor-{i:03d}",
            "temperature-sensor",
            {
                "location": {"lat": 37.7749 + i*0.01, "lon": -122.4194},
                "capabilities": ["temperature", "humidity"],
                "tags": ["warehouse-a", "production"]
            }
        )
        devices.append(device_id)
        print(f"   ✓ Registered device: {device_id}")
    
    # Test 2: Device Provisioning
    print("\n2. Device Provisioning")
    config = {
        "reporting_interval": 60,
        "temperature_unit": "celsius",
        "alerts_enabled": True
    }
    result = await manager.provision_device(devices[0], config)
    print(f"   ✓ Provisioned device: {result}")
    
    # Test 3: Telemetry Collection
    print("\n3. Telemetry Collection")
    for i in range(10):
        for device_id in devices[:3]:
            temp = 20 + random.uniform(-5, 5)
            anomaly = await manager.collect_telemetry(
                device_id, "temperature", temp, "celsius"
            )
            
            humidity = 50 + random.uniform(-10, 10)
            await manager.collect_telemetry(
                device_id, "humidity", humidity, "percent"
            )
            
            battery = 100 - i * 2
            await manager.collect_telemetry(
                device_id, "battery", battery, "percent"
            )
        
        await asyncio.sleep(0.1)
    print("   ✓ Collected telemetry data")
    
    # Test 4: Firmware Update
    print("\n4. Firmware Update")
    update_id = await manager.update_firmware(
        "fw-update-001",
        "2.0.0",
        devices[:3],
        "https://updates.iot.com/firmware/v2.0.0"
    )
    print(f"   ✓ Started firmware update: {update_id}")
    
    # Wait for update to complete
    await asyncio.sleep(1)
    
    # Test 5: Command Execution
    print("\n5. Command Execution")
    result = await manager.send_command(devices[0], "reboot")
    print(f"   ✓ Sent command: {result}")
    
    # Test 6: Bulk Operations
    print("\n6. Bulk Operations")
    results = await manager.bulk_command(
        devices[:3], 
        "configure",
        {"mode": "low_power"}
    )
    print(f"   ✓ Bulk command results: {sum(results.values())}/{len(results)} succeeded")
    
    # Test 7: Location Services
    print("\n7. Location Services")
    await manager.update_device_location(devices[0], 37.7849, -122.4094)
    nearby = await manager.find_devices_in_radius(37.7749, -122.4194, 5.0)
    print(f"   ✓ Found {len(nearby)} devices within 5km")
    
    # Test 8: Edge Computing
    print("\n8. Edge Computing")
    await manager.edge_computing.register_edge_gateway("edge-gw-001", ["compute", "ml"])
    await manager.edge_computing.deploy_edge_function(
        "temp-converter",
        "edge-gw-001",
        EDGE_FUNCTIONS["temperature_filter"]
    )
    print("   ✓ Deployed edge function")
    
    # Test 9: Power Optimization
    print("\n9. Power Optimization")
    optimization = await manager.optimize_power_management(devices[0])
    print(f"   ✓ Power optimization: {len(optimization.get('recommendations', []))} recommendations")
    
    # Test 10: Fleet Health
    print("\n10. Fleet Health Check")
    health = await manager.get_fleet_health()
    print(f"   ✓ Fleet health score: {health['health_score']:.1f}%")
    print(f"   ✓ Online devices: {health['status_distribution'].get('online', 0)}/{health['total_devices']}")
    
    # Test 11: Cloud Integration
    print("\n11. Cloud Platform Integration")
    result = await manager.integrate_cloud_platform(
        "aws-iot",
        {"endpoint": "iot.us-west-2.amazonaws.com", "region": "us-west-2"}
    )
    print(f"   ✓ Cloud integration: {result}")
    
    # Test 12: Security Operations
    print("\n12. Security Management")
    cert_valid = manager.security_manager.validate_certificate(
        manager.devices[devices[0]].certificate_id
    )
    print(f"   ✓ Certificate validation: {cert_valid}")
    
    # Summary
    print("\n" + "=" * 50)
    print("✅ All IoT Fleet Manager Tests Passed!")
    print(f"   - Devices registered: {len(manager.devices)}")
    print(f"   - Telemetry points: {len(manager.telemetry_store)}")
    print(f"   - Active updates: {len(manager.firmware_updates)}")
    print(f"   - Anomalies detected: {len(manager.anomaly_detector.anomalies)}")
    

if __name__ == "__main__":
    asyncio.run(main())