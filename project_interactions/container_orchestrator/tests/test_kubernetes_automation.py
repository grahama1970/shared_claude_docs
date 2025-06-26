"""
Module: test_kubernetes_automation.py
Purpose: Test Kubernetes automation functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://github.com/pytest-dev/pytest-asyncio

Example Usage:
>>> pytest test_kubernetes_automation.py -v
"""

import pytest
import asyncio
import yaml
from typing import Dict, Any
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from container_orchestrator_interaction import (
    ContainerOrchestrator, AutoScalingPolicy, NetworkPolicy,
    ServiceConfig, ResourceType
)


class TestKubernetesAutomation:
    """Test Kubernetes automation features"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance"""
        return ContainerOrchestrator(clusters=["k8s-test"])
    
    @pytest.mark.asyncio
    async def test_auto_scaling_configuration(self, orchestrator):
        """Test auto-scaling policy configuration"""
        # Deploy service first
        await orchestrator.deploy_service(
            name="autoscale-app",
            image="nginx:latest",
            replicas=2
        )
        
        # Configure auto-scaling
        policy = AutoScalingPolicy(
            min_replicas=1,
            max_replicas=10,
            target_cpu_utilization=75,
            target_memory_utilization=80,
            scale_up_rate=2,
            scale_down_rate=1
        )
        
        result = await orchestrator.configure_auto_scaling(
            "autoscale-app", policy
        )
        
        assert result["status"] == "configured"
        assert result["auto_scaling"]["min_replicas"] == 1
        assert result["auto_scaling"]["max_replicas"] == 10
        assert result["auto_scaling"]["cpu_target"] == 75
        assert result["auto_scaling"]["memory_target"] == 80
    
    @pytest.mark.asyncio
    async def test_config_map_creation(self, orchestrator):
        """Test ConfigMap creation"""
        config_data = {
            "application.yaml": "server:\n  port: 8080\n  host: 0.0.0.0",
            "database.properties": "db.host=localhost\ndb.port=5432",
            "features.json": '{"feature_flags": {"new_ui": true}}'
        }
        
        result = await orchestrator.create_config_map(
            "app-config", config_data
        )
        
        assert result["status"] == "created"
        assert result["type"] == "configmap"
        assert result["items"] == 3
        assert "app-config" in orchestrator.configs
    
    @pytest.mark.asyncio
    async def test_secret_creation(self, orchestrator):
        """Test Secret creation"""
        secret_data = {
            "username": "admin",
            "password": "super-secret-password",
            "api_token": "abc123xyz789",
            "tls.crt": "-----BEGIN CERTIFICATE-----",
            "tls.key": "-----BEGIN PRIVATE KEY-----"
        }
        
        result = await orchestrator.create_secret(
            "app-secrets", secret_data, "kubernetes.io/tls"
        )
        
        assert result["status"] == "created"
        assert result["type"] == "secret"
        assert result["secret_type"] == "kubernetes.io/tls"
        assert set(result["keys"]) == set(secret_data.keys())
    
    @pytest.mark.asyncio
    async def test_network_policy_configuration(self, orchestrator):
        """Test network policy setup"""
        policy = NetworkPolicy(
            name="web-policy",
            pod_selector={"app": "web", "tier": "frontend"},
            ingress_rules=[
                {
                    "from": [
                        {"podSelector": {"app": "api"}},
                        {"namespaceSelector": {"name": "production"}}
                    ],
                    "ports": [
                        {"protocol": "TCP", "port": 80},
                        {"protocol": "TCP", "port": 443}
                    ]
                }
            ],
            egress_rules=[
                {
                    "to": [{"podSelector": {"app": "database"}}],
                    "ports": [{"protocol": "TCP", "port": 5432}]
                }
            ]
        )
        
        result = await orchestrator.configure_network_policy(policy)
        
        assert result["status"] == "configured"
        assert result["policy"] == "web-policy"
        assert result["rules"]["ingress"] == 1
        assert result["rules"]["egress"] == 1
    
    @pytest.mark.asyncio
    async def test_service_mesh_setup(self, orchestrator):
        """Test service mesh configuration"""
        services = ["frontend", "api", "auth", "database-proxy"]
        
        traffic_policy = {
            "connectionPool": {
                "tcp": {"maxConnections": 200},
                "http": {
                    "http1MaxPendingRequests": 50,
                    "http2MaxRequests": 100
                }
            },
            "loadBalancer": {"simple": "LEAST_REQUEST"},
            "outlierDetection": {
                "consecutiveErrors": 10,
                "interval": "60s",
                "baseEjectionTime": "60s",
                "maxEjectionPercent": 50
            }
        }
        
        result = await orchestrator.setup_service_mesh(
            "istio-production",
            services,
            mtls_enabled=True,
            traffic_policy=traffic_policy
        )
        
        assert result["status"] == "configured"
        assert result["mesh"] == "istio-production"
        assert result["services"] == 4
        assert result["mtls_enabled"] is True
        assert "connectionPool" in result["policies"]
    
    @pytest.mark.asyncio
    async def test_load_balancer_setup(self, orchestrator):
        """Test load balancer configuration"""
        # Deploy service first
        await orchestrator.deploy_service(
            name="lb-app",
            image="nginx:latest",
            replicas=4,
            ports=[80]
        )
        
        result = await orchestrator.setup_load_balancer(
            "lb-app",
            algorithm="least_connections",
            health_check_path="/healthz",
            sticky_sessions=True
        )
        
        assert result["status"] == "configured"
        assert result["algorithm"] == "least_connections"
        assert result["backends"] == 4
        assert result["sticky_sessions"] is True
    
    @pytest.mark.asyncio
    async def test_deployment_manifest_generation(self, orchestrator):
        """Test deployment manifest generation"""
        # Setup complete application
        await orchestrator.deploy_service(
            name="manifest-app",
            image="app:v1.0",
            replicas=3,
            ports=[8080]
        )
        
        await orchestrator.create_config_map(
            "manifest-app-config",
            {"app.conf": "debug=false"}
        )
        
        await orchestrator.create_secret(
            "manifest-app-secrets",
            {"api_key": "secret123"}
        )
        
        # Generate manifest
        manifest_yaml = await orchestrator.generate_deployment_manifest(
            "manifest-app",
            {"include_configs": True}
        )
        
        # Parse and validate YAML
        manifest = yaml.safe_load(manifest_yaml)
        assert manifest["kind"] == "List"
        assert len(manifest["items"]) >= 3  # Deployment, Service, ConfigMap
        
        # Check for required resources
        resource_kinds = {item["kind"] for item in manifest["items"]}
        assert "Deployment" in resource_kinds
        assert "Service" in resource_kinds
        assert "ConfigMap" in resource_kinds
    
    @pytest.mark.asyncio
    async def test_multi_cluster_management(self, orchestrator):
        """Test multi-cluster functionality"""
        multi_orchestrator = ContainerOrchestrator(
            clusters=["prod-us-east", "prod-us-west", "prod-eu"]
        )
        
        # Deploy to multiple clusters
        for i, cluster in enumerate(multi_orchestrator.clusters):
            await multi_orchestrator.deploy_service(
                name=f"multi-app-{cluster}",
                image="nginx:latest",
                replicas=2 + i
            )
        
        status = multi_orchestrator.get_cluster_status()
        assert len(status["clusters"]) == 3
        assert status["deployments"] == 3
        assert status["total_replicas"] == 9  # 2 + 3 + 4
    
    @pytest.mark.asyncio
    async def test_resource_validation(self, orchestrator):
        """Test resource configuration validation"""
        # Test with various resource configurations
        resources_configs = [
            {
                "requests": {"cpu": "100m", "memory": "128Mi"},
                "limits": {"cpu": "500m", "memory": "512Mi"}
            },
            {
                "requests": {"cpu": "1", "memory": "1Gi"},
                "limits": {"cpu": "2", "memory": "2Gi"}
            },
            {
                "requests": {"cpu": "250m", "memory": "256Mi"},
                "limits": {"cpu": "1000m", "memory": "1Gi"}
            }
        ]
        
        for i, resources in enumerate(resources_configs):
            result = await orchestrator.deploy_service(
                name=f"resource-app-{i}",
                image="nginx:latest",
                resources=resources
            )
            
            assert result["status"] == "deployed"
            deployment = orchestrator.deployments[f"resource-app-{i}"]
            container_resources = deployment["spec"]["template"]["spec"]["containers"][0]["resources"]
            assert container_resources == resources
    
    @pytest.mark.asyncio
    async def test_deployment_update_strategies(self, orchestrator):
        """Test various deployment update strategies"""
        # Deploy initial version
        await orchestrator.deploy_service(
            name="strategy-app",
            image="app:v1.0",
            replicas=5
        )
        
        # Test rolling update with different parameters
        update_configs = [
            {"max_surge": "50%", "max_unavailable": "0%"},
            {"max_surge": "25%", "max_unavailable": "25%"},
            {"max_surge": "1", "max_unavailable": "1"}
        ]
        
        for config in update_configs:
            result = await orchestrator.perform_rolling_update(
                "strategy-app",
                "app:v2.0",
                **config
            )
            
            assert result["status"] == "updating"
            deployment = orchestrator.deployments["strategy-app"]
            strategy = deployment["spec"]["strategy"]["rollingUpdate"]
            assert strategy["maxSurge"] == config["max_surge"]
            assert strategy["maxUnavailable"] == config["max_unavailable"]


def run_tests():
    """Run all Kubernetes automation tests"""
    print("Running Kubernetes Automation Tests\n" + "=" * 50)
    
    # Run with pytest
    test_file = Path(__file__)
    exit_code = pytest.main([str(test_file), "-v", "--tb=short"])
    
    return exit_code


if __name__ == "__main__":
    # Run tests
    exit_code = run_tests()
    
    # Also run a quick validation
    print("\nQuick Validation Test:")
    orchestrator = ContainerOrchestrator()
    
    # Test Kubernetes features
    async def validate_k8s_features():
        # Test auto-scaling
        await orchestrator.deploy_service("k8s-test", "nginx:latest")
        policy = AutoScalingPolicy(min_replicas=1, max_replicas=5)
        result = await orchestrator.configure_auto_scaling("k8s-test", policy)
        assert result["status"] == "configured"
        print("✅ Auto-scaling configuration validated")
        
        # Test network policy
        policy = NetworkPolicy(
            name="test-policy",
            pod_selector={"app": "test"}
        )
        result = await orchestrator.configure_network_policy(policy)
        assert result["status"] == "configured"
        print("✅ Network policy configuration validated")
    
    asyncio.run(validate_k8s_features())
    
    exit(exit_code)