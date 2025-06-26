"""
Module: test_traffic_management.py
Purpose: Test traffic management features of service mesh manager

External Dependencies:
- pytest: https://docs.pytest.org/
- asyncio: https://docs.python.org/3/library/asyncio.html

Example Usage:
>>> pytest test_traffic_management.py -v
test_retry_policy_configuration PASSED
test_circuit_breaker_configuration PASSED
"""

import pytest
import asyncio
from pathlib import Path
import json
from typing import Dict, Any
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from service_mesh_manager_interaction import (
    ServiceMeshManager, MeshProvider, LoadBalancerType,
    RetryPolicy, CircuitBreakerConfig, TimeoutPolicy,
    ServiceEndpoint, TrafficSplitConfig
)


class TestTrafficManagement:
    """Test traffic management capabilities"""
    
    @pytest.fixture
    def manager(self):
        """Create service mesh manager instance"""
        return ServiceMeshManager(MeshProvider.ISTIO)
    
    @pytest.fixture
    def sample_service(self):
        """Create sample service endpoint"""
        return ServiceEndpoint(
            name="test-service",
            namespace="test",
            port=8080,
            version="v1",
            labels={"app": "test", "env": "qa"}
        )
    
    def test_retry_policy_configuration(self, manager, sample_service):
        """Test retry policy configuration"""
        manager.register_service(sample_service)
        
        retry_policy = RetryPolicy(
            attempts=5,
            per_try_timeout="15s",
            retry_on=["5xx", "reset", "retriable-4xx"],
            retry_on_status_codes=[502, 503, 504],
            backoff_base_interval="2s",
            backoff_max_interval="60s"
        )
        
        policy = manager.create_traffic_policy(
            sample_service.name,
            namespace=sample_service.namespace,
            retry_policy=retry_policy
        )
        
        assert policy["kind"] == "DestinationRule"
        assert "retryPolicy" in policy["spec"]["trafficPolicy"]
        assert policy["spec"]["trafficPolicy"]["retryPolicy"]["attempts"] == 5
        assert policy["spec"]["trafficPolicy"]["retryPolicy"]["perTryTimeout"] == "15s"
        assert "5xx,reset,retriable-4xx" in policy["spec"]["trafficPolicy"]["retryPolicy"]["retryOn"]
        
        print("✅ Retry policy configuration test passed")
    
    def test_circuit_breaker_configuration(self, manager, sample_service):
        """Test circuit breaker configuration"""
        manager.register_service(sample_service)
        
        circuit_breaker = CircuitBreakerConfig(
            consecutive_errors=10,
            interval="60s",
            base_ejection_time="120s",
            max_ejection_percent=75,
            min_healthy_percent=25
        )
        
        policy = manager.create_traffic_policy(
            sample_service.name,
            namespace=sample_service.namespace,
            circuit_breaker=circuit_breaker
        )
        
        assert "connectionPool" in policy["spec"]["trafficPolicy"]
        assert "outlierDetection" in policy["spec"]["trafficPolicy"]
        
        outlier = policy["spec"]["trafficPolicy"]["outlierDetection"]
        assert outlier["consecutiveErrors"] == 10
        assert outlier["interval"] == "60s"
        assert outlier["baseEjectionTime"] == "120s"
        assert outlier["maxEjectionPercent"] == 75
        
        print("✅ Circuit breaker configuration test passed")
    
    def test_load_balancer_strategies(self, manager, sample_service):
        """Test different load balancer strategies"""
        manager.register_service(sample_service)
        
        strategies = [
            LoadBalancerType.ROUND_ROBIN,
            LoadBalancerType.LEAST_REQUEST,
            LoadBalancerType.RANDOM,
            LoadBalancerType.CONSISTENT_HASH
        ]
        
        for strategy in strategies:
            policy = manager.create_traffic_policy(
                sample_service.name,
                namespace=sample_service.namespace,
                load_balancer=strategy
            )
            
            lb_config = policy["spec"]["trafficPolicy"]["loadBalancer"]
            assert "simple" in lb_config
            assert lb_config["simple"] == strategy.value.upper()
        
        print("✅ Load balancer strategies test passed")
    
    def test_canary_deployment(self, manager):
        """Test canary deployment configuration"""
        # Register both versions
        stable = ServiceEndpoint(
            name="canary-app",
            namespace="prod",
            port=8080,
            version="v1"
        )
        canary = ServiceEndpoint(
            name="canary-app",
            namespace="prod",
            port=8080,
            version="v2"
        )
        
        manager.register_service(stable)
        manager.register_service(canary)
        
        # Create canary deployment
        vs = manager.create_canary_deployment(
            "canary-app",
            namespace="prod",
            stable_version="v1",
            canary_version="v2",
            canary_weight=30,
            header_based_routing={"x-canary": "true"}
        )
        
        assert vs.name == "canary-app-canary"
        assert len(vs.http_routes) == 2
        
        # Check header-based route
        header_route = vs.http_routes[0]
        assert "match" in header_route
        assert "headers" in header_route["match"][0]
        
        # Check weight-based route
        weight_route = vs.http_routes[1]
        assert len(weight_route["route"]) == 2
        assert weight_route["route"][0]["weight"] == 70  # stable
        assert weight_route["route"][1]["weight"] == 30  # canary
        
        print("✅ Canary deployment test passed")
    
    def test_timeout_policies(self, manager, sample_service):
        """Test timeout configuration"""
        manager.register_service(sample_service)
        
        timeout_policy = TimeoutPolicy(
            request_timeout="10s",
            idle_timeout="300s",
            stream_idle_timeout="60s"
        )
        
        policy = manager.create_traffic_policy(
            sample_service.name,
            namespace=sample_service.namespace,
            timeout_policy=timeout_policy
        )
        
        assert policy["spec"]["trafficPolicy"]["timeout"] == "10s"
        
        print("✅ Timeout policies test passed")
    
    def test_traffic_splitting(self, manager):
        """Test traffic splitting for multiple versions"""
        service_name = "multi-version-app"
        namespace = "test"
        
        # Register multiple versions
        versions = ["v1", "v2", "v3"]
        for version in versions:
            service = ServiceEndpoint(
                name=service_name,
                namespace=namespace,
                port=8080,
                version=version
            )
            manager.register_service(service)
        
        # Create traffic split
        weight_distribution = {"v1": 50, "v2": 30, "v3": 20}
        
        policy = manager.create_traffic_policy(
            service_name,
            namespace=namespace,
            weight_distribution=weight_distribution
        )
        
        assert "subsets" in policy["spec"]
        assert len(policy["spec"]["subsets"]) == 3
        
        for subset in policy["spec"]["subsets"]:
            version = subset["name"]
            assert version in versions
            assert subset["labels"]["version"] == version
        
        print("✅ Traffic splitting test passed")
    
    def test_traffic_mirroring(self, manager):
        """Test traffic mirroring configuration"""
        service = ServiceEndpoint(
            name="mirrored-service",
            namespace="prod",
            port=8080
        )
        manager.register_service(service)
        
        mirror_config = manager.setup_traffic_mirroring(
            service.name,
            namespace=service.namespace,
            mirror_destination="mirrored-service-shadow",
            mirror_percentage=50.0
        )
        
        assert mirror_config["kind"] == "VirtualService"
        assert "mirror" in mirror_config["spec"]["http"][0]
        assert mirror_config["spec"]["http"][0]["mirror"]["host"] == "mirrored-service-shadow"
        assert mirror_config["spec"]["http"][0]["mirrorPercentage"]["value"] == 50.0
        
        print("✅ Traffic mirroring test passed")
    
    def test_complex_traffic_policy(self, manager):
        """Test complex traffic policy with multiple features"""
        service = ServiceEndpoint(
            name="complex-service",
            namespace="production",
            port=8080
        )
        manager.register_service(service)
        
        # Create comprehensive policy
        retry = RetryPolicy(attempts=3, per_try_timeout="5s")
        circuit = CircuitBreakerConfig(consecutive_errors=5)
        timeout = TimeoutPolicy(request_timeout="30s")
        
        policy = manager.create_traffic_policy(
            service.name,
            namespace=service.namespace,
            retry_policy=retry,
            circuit_breaker=circuit,
            timeout_policy=timeout,
            load_balancer=LoadBalancerType.LEAST_REQUEST
        )
        
        traffic_policy = policy["spec"]["trafficPolicy"]
        assert "retryPolicy" in traffic_policy
        assert "connectionPool" in traffic_policy
        assert "outlierDetection" in traffic_policy
        assert "timeout" in traffic_policy
        assert "loadBalancer" in traffic_policy
        
        # Apply configuration
        success = manager.apply_configuration(policy)
        assert success
        
        print("✅ Complex traffic policy test passed")
    
    @pytest.mark.asyncio
    async def test_service_health_monitoring(self, manager):
        """Test service health monitoring"""
        services = [
            ServiceEndpoint(f"service-{i}", "test", 8080)
            for i in range(3)
        ]
        
        for service in services:
            manager.register_service(service)
        
        # Get health for each service
        health_reports = []
        for service in services:
            health = manager.get_service_health(service.name, service.namespace)
            health_reports.append(health)
            
            assert "status" in health
            assert "success_rate" in health
            assert "latency_p50" in health
            assert "latency_p99" in health
            assert health["success_rate"] >= 0 and health["success_rate"] <= 100
        
        print(f"✅ Service health monitoring test passed - checked {len(health_reports)} services")
    
    def test_export_configurations(self, manager, tmp_path):
        """Test configuration export"""
        # Create multiple configurations
        services = ["web", "api", "database"]
        
        for svc in services:
            service = ServiceEndpoint(svc, "test", 8080)
            manager.register_service(service)
            
            policy = manager.create_traffic_policy(
                svc,
                namespace="test",
                retry_policy=RetryPolicy(attempts=3)
            )
            manager.apply_configuration(policy)
        
        # Export configurations
        export_dir = tmp_path / "mesh-configs"
        exported_files = manager.export_configuration(export_dir)
        
        assert len(exported_files) >= len(services)
        
        for file_path in exported_files:
            assert file_path.exists()
            assert file_path.suffix == ".yaml"
        
        print(f"✅ Configuration export test passed - exported {len(exported_files)} files")


# Run validation
if __name__ == "__main__":
    test = TestTrafficManagement()
    manager = ServiceMeshManager()
    
    # Test basic functionality
    service = ServiceEndpoint("test-app", "default", 8080)
    
    test.test_retry_policy_configuration(manager, service)
    test.test_circuit_breaker_configuration(manager, service)
    test.test_load_balancer_strategies(manager, service)
    test.test_canary_deployment(manager)
    test.test_timeout_policies(manager, service)
    
    print("\n✅ All traffic management tests passed!")