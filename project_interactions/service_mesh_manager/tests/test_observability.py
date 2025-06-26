"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Module: test_observability.py
Purpose: Test observability features of service mesh manager

External Dependencies:
- pytest: https://docs.pytest.org/
- pathlib: https://docs.python.org/3/library/pathlib.html

Example Usage:
>>> pytest test_observability.py -v
test_telemetry_configuration PASSED
test_fault_injection PASSED
"""

import pytest
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from service_mesh_manager_interaction import (
    ServiceMeshManager, MeshProvider, ServiceEndpoint,
    ObservabilityConfig, FaultInjectionConfig
)


class TestObservability:
    """Test observability and chaos engineering features"""
    
    @pytest.fixture
    def manager(self):
        """Create service mesh manager instance"""
        return ServiceMeshManager(MeshProvider.ISTIO)
    
    @pytest.fixture
    def monitored_service(self):
        """Create service with monitoring requirements"""
        return ServiceEndpoint(
            name="monitored-app",
            namespace="observability",
            port=8080,
            labels={"monitoring": "enabled", "tier": "frontend"}
        )
    
    def test_telemetry_configuration(self, manager):
        """Test telemetry and observability configuration"""
        # Test default configuration
        default_config = manager.setup_observability("default")
        
        assert default_config["kind"] == "Telemetry"
        assert len(default_config["spec"]["metrics"]) > 0
        assert len(default_config["spec"]["accessLogging"]) > 0
        assert len(default_config["spec"]["tracing"]) > 0
        
        # Test custom configuration
        custom_obs = ObservabilityConfig(
            metrics_enabled=True,
            tracing_enabled=True,
            access_logs_enabled=True,
            tracing_sampling_rate=0.1,  # 10% sampling
            custom_metrics=["request_count", "request_duration", "response_size"],
            custom_dimensions={
                "method": "request.method | 'unknown'",
                "response_code": "response.code | 0",
                "custom_header": "request.headers['x-custom-id'] | 'none'"
            }
        )
        
        custom_config = manager.setup_observability("production", custom_obs)
        
        assert custom_config["spec"]["metrics"][0]["dimensions"] == custom_obs.custom_dimensions
        assert custom_config["spec"]["tracing"][0]["randomSamplingPercentage"] == 10.0
        
        print("✅ Telemetry configuration test passed")
    
    def test_metrics_configuration(self, manager):
        """Test metrics-specific configuration"""
        # Disable all but metrics
        metrics_only = ObservabilityConfig(
            metrics_enabled=True,
            tracing_enabled=False,
            access_logs_enabled=False,
            custom_metrics=["custom_counter", "custom_histogram"],
            custom_dimensions={
                "service_version": "source.labels['version'] | 'unknown'",
                "environment": "source.labels['env'] | 'prod'"
            }
        )
        
        config = manager.setup_observability("metrics-test", metrics_only)
        
        assert len(config["spec"]["metrics"]) > 0
        assert len(config["spec"]["tracing"]) == 0
        assert len(config["spec"]["accessLogging"]) == 0
        
        print("✅ Metrics configuration test passed")
    
    def test_distributed_tracing(self, manager):
        """Test distributed tracing configuration"""
        # Test different sampling rates
        sampling_rates = [0.01, 0.1, 0.5, 1.0]  # 1%, 10%, 50%, 100%
        
        for rate in sampling_rates:
            obs_config = ObservabilityConfig(
                tracing_enabled=True,
                tracing_sampling_rate=rate,
                metrics_enabled=False,
                access_logs_enabled=False
            )
            
            config = manager.setup_observability(f"trace-{int(rate*100)}", obs_config)
            
            assert len(config["spec"]["tracing"]) > 0
            expected_percentage = rate * 100
            assert config["spec"]["tracing"][0]["randomSamplingPercentage"] == expected_percentage
        
        print("✅ Distributed tracing test passed")
    
    def test_access_logging(self, manager):
        """Test access logging configuration"""
        # Configure access logging with custom provider
        access_log_config = {
            "apiVersion": "telemetry.istio.io/v1alpha1",
            "kind": "Telemetry",
            "metadata": {
                "name": "access-logs-custom",
                "namespace": "logging-test"
            },
            "spec": {
                "accessLogging": [{
                    "providers": [{"name": "otel"}],
                    "filter": {
                        "expression": "response.code >= 400"  # Log only errors
                    }
                }]
            }
        }
        
        success = manager.apply_configuration(access_log_config)
        assert success
        
        print("✅ Access logging test passed")
    
    def test_fault_injection_basic(self, manager, monitored_service):
        """Test basic fault injection"""
        manager.register_service(monitored_service)
        
        # Test delay injection
        delay_config = FaultInjectionConfig(
            delay={"fixedDelay": "5s", "percentage": {"value": 25}},
            percentage=25.0
        )
        
        fault_vs = manager.inject_fault(
            monitored_service.name,
            monitored_service.namespace,
            delay_config
        )
        
        assert fault_vs["kind"] == "VirtualService"
        assert "fault" in fault_vs["spec"]["http"][0]
        assert fault_vs["spec"]["http"][0]["fault"]["delay"]["fixedDelay"] == "5s"
        assert fault_vs["spec"]["http"][0]["fault"]["delay"]["percentage"]["value"] == 25
        
        print("✅ Basic fault injection test passed")
    
    def test_fault_injection_abort(self, manager, monitored_service):
        """Test abort fault injection"""
        manager.register_service(monitored_service)
        
        # Test abort injection
        abort_config = FaultInjectionConfig(
            abort={"httpStatus": 503, "percentage": {"value": 10}},
            percentage=10.0
        )
        
        fault_vs = manager.inject_fault(
            monitored_service.name,
            monitored_service.namespace,
            abort_config
        )
        
        assert "fault" in fault_vs["spec"]["http"][0]
        assert fault_vs["spec"]["http"][0]["fault"]["abort"]["httpStatus"] == 503
        assert fault_vs["spec"]["http"][0]["fault"]["abort"]["percentage"]["value"] == 10
        
        print("✅ Abort fault injection test passed")
    
    def test_fault_injection_combined(self, manager):
        """Test combined delay and abort fault injection"""
        service = ServiceEndpoint("chaos-test", "test", 8080)
        manager.register_service(service)
        
        # Combine delay and abort
        combined_config = FaultInjectionConfig(
            delay={"fixedDelay": "10s", "percentage": {"value": 50}},
            abort={"httpStatus": 500, "percentage": {"value": 20}},
            percentage=100.0  # Apply to all matching requests
        )
        
        fault_vs = manager.inject_fault(
            service.name,
            service.namespace,
            combined_config
        )
        
        fault_spec = fault_vs["spec"]["http"][0]["fault"]
        assert "delay" in fault_spec
        assert "abort" in fault_spec
        assert fault_spec["delay"]["percentage"]["value"] == 50
        assert fault_spec["abort"]["percentage"]["value"] == 20
        
        print("✅ Combined fault injection test passed")
    
    def test_service_health_monitoring(self, manager):
        """Test service health monitoring"""
        # Register multiple services
        services = []
        for i in range(5):
            service = ServiceEndpoint(
                name=f"service-{i}",
                namespace="health-test",
                port=8080 + i,
                labels={"app": f"service-{i}", "version": "v1"}
            )
            manager.register_service(service)
            services.append(service)
        
        # Check health for each service
        health_reports = []
        for service in services:
            health = manager.get_service_health(service.name, service.namespace)
            health_reports.append(health)
            
            # Validate health report structure
            assert "service" in health
            assert "namespace" in health
            assert "status" in health
            assert "endpoints" in health
            assert "success_rate" in health
            assert "latency_p50" in health
            assert "latency_p99" in health
            assert "circuit_breaker" in health
            
            # Validate value ranges
            assert health["endpoints"] > 0
            assert 0 <= health["success_rate"] <= 100
            assert health["latency_p50"] > 0
            assert health["latency_p99"] >= health["latency_p50"]
        
        # Simulate degraded service
        if health_reports:
            degraded_health = health_reports[0].copy()
            degraded_health["success_rate"] = 85.0  # Below 90% threshold
            print(f"⚠️  Simulated degraded service: {degraded_health['service']} - {degraded_health['success_rate']}% success rate")
        
        print(f"✅ Service health monitoring test passed - monitored {len(services)} services")
    
    def test_custom_metrics_export(self, manager):
        """Test custom metrics configuration and export"""
        # Define custom metrics
        custom_metrics_config = {
            "apiVersion": "telemetry.istio.io/v1alpha1",
            "kind": "Telemetry",
            "metadata": {
                "name": "custom-metrics",
                "namespace": "metrics"
            },
            "spec": {
                "metrics": [{
                    "providers": [{"name": "prometheus"}],
                    "dimensions": {
                        "request_protocol": "request.protocol | 'unknown'",
                        "response_code_class": "response.code / 100",
                        "source_workload": "source.workload.name | 'unknown'",
                        "destination_service": "destination.service.name | 'unknown'"
                    },
                    "metrics": [
                        {
                            "name": "request_count",
                            "dimensions": ["request_protocol", "response_code_class"]
                        },
                        {
                            "name": "request_duration",
                            "dimensions": ["source_workload", "destination_service"],
                            "unit": "MILLISECONDS"
                        }
                    ]
                }]
            }
        }
        
        success = manager.apply_configuration(custom_metrics_config)
        assert success
        
        print("✅ Custom metrics export test passed")
    
    def test_multi_cluster_observability(self, manager):
        """Test multi-cluster observability setup"""
        clusters = ["cluster-1", "cluster-2", "cluster-3"]
        
        for cluster in clusters:
            # Configure observability for each cluster
            obs_config = ObservabilityConfig(
                metrics_enabled=True,
                tracing_enabled=True,
                tracing_sampling_rate=0.05,  # 5% sampling for multi-cluster
                custom_dimensions={
                    "cluster_name": f"'{cluster}'",
                    "cluster_region": "'us-west-2'"
                }
            )
            
            config = manager.setup_observability(f"{cluster}-istio-system", obs_config)
            assert manager.apply_configuration(config)
        
        print(f"✅ Multi-cluster observability test passed - configured {len(clusters)} clusters")
    
    def test_configuration_export_and_validation(self, manager, tmp_path):
        """Test configuration export and validation"""
        # Create various configurations
        services = ["frontend", "backend", "database"]
        
        for svc in services:
            service = ServiceEndpoint(svc, "test", 8080)
            manager.register_service(service)
            
            # Add observability
            obs_config = ObservabilityConfig(
                metrics_enabled=True,
                tracing_enabled=True,
                tracing_sampling_rate=0.1
            )
            telemetry = manager.setup_observability(service.namespace, obs_config)
            manager.apply_configuration(telemetry)
            
            # Add fault injection
            if svc == "frontend":  # Only inject faults in frontend
                fault_config = FaultInjectionConfig(
                    delay={"fixedDelay": "2s", "percentage": {"value": 5}}
                )
                fault_vs = manager.inject_fault(svc, service.namespace, fault_config)
                manager.apply_configuration(fault_vs)
        
        # Export configurations
        export_dir = tmp_path / "observability-configs"
        exported_files = manager.export_configuration(export_dir)
        
        assert len(exported_files) > 0
        
        # Validate exported files
        for file_path in exported_files:
            assert file_path.exists()
            
            # Load and validate YAML
            with open(file_path, 'r') as f:
                config = yaml.safe_load(f)
                
            assert "apiVersion" in config
            assert "kind" in config
            assert "metadata" in config
            assert "spec" in config
        
        print(f"✅ Configuration export test passed - exported {len(exported_files)} configurations")


# Run validation
if __name__ == "__main__":
    test = TestObservability()
    manager = ServiceMeshManager()
    
    # Test observability features
    service = ServiceEndpoint("test-app", "default", 8080)
    
    test.test_telemetry_configuration(manager)
    test.test_metrics_configuration(manager)
    test.test_distributed_tracing(manager)
    test.test_fault_injection_basic(manager, service)
    test.test_fault_injection_abort(manager, service)
    test.test_service_health_monitoring(manager)
    test.test_multi_cluster_observability(manager)
    
    print("\n✅ All observability tests passed!")