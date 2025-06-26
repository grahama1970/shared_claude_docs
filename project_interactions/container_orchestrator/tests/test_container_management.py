"""
Module: test_container_management.py
Purpose: Test container management functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://github.com/pytest-dev/pytest-asyncio

Example Usage:
>>> pytest test_container_management.py -v
"""

import pytest
import asyncio
from typing import Dict, Any
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from container_orchestrator_interaction import (
    ContainerOrchestrator, ContainerConfig, DeploymentStrategy
)


class TestContainerManagement:
    """Test container management operations"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance"""
        return ContainerOrchestrator(clusters=["test-cluster"])
    
    @pytest.mark.asyncio
    async def test_deploy_service(self, orchestrator):
        """Test service deployment"""
        result = await orchestrator.deploy_service(
            name="test-app",
            image="nginx:latest",
            replicas=2,
            ports=[8080]
        )
        
        assert result["status"] == "deployed"
        assert result["service"] == "test-app"
        assert result["replicas"] == 2
        assert len(result["endpoints"]) == 2
        assert "deployment_id" in result
    
    @pytest.mark.asyncio
    async def test_scale_deployment(self, orchestrator):
        """Test deployment scaling"""
        # First deploy
        await orchestrator.deploy_service(
            name="scale-app",
            image="nginx:latest",
            replicas=1
        )
        
        # Then scale
        result = await orchestrator.scale_deployment("scale-app", 5)
        
        assert result["status"] == "scaled"
        assert result["old_replicas"] == 1
        assert result["new_replicas"] == 5
    
    @pytest.mark.asyncio
    async def test_deployment_strategies(self, orchestrator):
        """Test different deployment strategies"""
        strategies = [
            DeploymentStrategy.ROLLING_UPDATE,
            DeploymentStrategy.BLUE_GREEN,
            DeploymentStrategy.CANARY,
            DeploymentStrategy.RECREATE
        ]
        
        for strategy in strategies:
            result = await orchestrator.deploy_service(
                name=f"app-{strategy.value}",
                image="nginx:latest",
                replicas=1,
                strategy=strategy
            )
            
            assert result["status"] == "deployed"
            assert result["strategy"] == strategy.value
    
    @pytest.mark.asyncio
    async def test_container_config(self, orchestrator):
        """Test container configuration"""
        result = await orchestrator.deploy_service(
            name="config-app",
            image="app:latest",
            replicas=1,
            ports=[80, 443],
            environment={
                "DATABASE_URL": "postgres://localhost",
                "API_KEY": "test-key"
            },
            resources={
                "requests": {"cpu": "200m", "memory": "256Mi"},
                "limits": {"cpu": "1000m", "memory": "1Gi"}
            }
        )
        
        assert result["status"] == "deployed"
        deployment = orchestrator.deployments["config-app"]
        container = deployment["spec"]["template"]["spec"]["containers"][0]
        
        assert len(container["ports"]) == 2
        assert len(container["env"]) == 2
        assert container["resources"]["requests"]["cpu"] == "200m"
    
    @pytest.mark.asyncio
    async def test_rolling_update(self, orchestrator):
        """Test rolling update functionality"""
        # Deploy initial version
        await orchestrator.deploy_service(
            name="update-app",
            image="nginx:1.19",
            replicas=3
        )
        
        # Perform rolling update
        result = await orchestrator.perform_rolling_update(
            "update-app",
            "nginx:1.21",
            max_surge="50%",
            max_unavailable="0%"
        )
        
        assert result["status"] == "updating"
        assert result["old_image"] == "nginx:1.19"
        assert result["new_image"] == "nginx:1.21"
        assert result["total_replicas"] == 3
    
    @pytest.mark.asyncio
    async def test_rollback_deployment(self, orchestrator):
        """Test deployment rollback"""
        # Deploy and update
        await orchestrator.deploy_service(
            name="rollback-app",
            image="nginx:1.19"
        )
        await orchestrator.perform_rolling_update(
            "rollback-app",
            "nginx:1.21"
        )
        
        # Rollback
        result = await orchestrator.rollback_deployment("rollback-app")
        
        assert result["status"] == "rolled_back"
        assert result["deployment"] == "rollback-app"
    
    @pytest.mark.asyncio
    async def test_monitor_health(self, orchestrator):
        """Test container health monitoring"""
        await orchestrator.deploy_service(
            name="health-app",
            image="nginx:latest",
            replicas=3
        )
        
        result = await orchestrator.monitor_container_health("health-app")
        
        assert result["deployment"] == "health-app"
        assert result["replicas"]["desired"] == 3
        assert result["replicas"]["ready"] == 3
        assert len(result["containers"]) == 3
        
        for container in result["containers"]:
            assert container["ready"] is True
            assert container["status"] == "Running"
    
    @pytest.mark.asyncio
    async def test_resource_optimization(self, orchestrator):
        """Test resource optimization recommendations"""
        await orchestrator.deploy_service(
            name="optimize-app",
            image="nginx:latest"
        )
        
        result = await orchestrator.optimize_resource_allocation("optimize-app")
        
        assert "recommended_resources" in result
        assert "reasoning" in result
        assert "potential_savings" in result
    
    @pytest.mark.asyncio
    async def test_deployment_not_found(self, orchestrator):
        """Test operations on non-existent deployment"""
        result = await orchestrator.scale_deployment("non-existent", 5)
        assert "error" in result
        
        result = await orchestrator.monitor_container_health("non-existent")
        assert "error" in result
    
    def test_cluster_status(self, orchestrator):
        """Test cluster status reporting"""
        status = orchestrator.get_cluster_status()
        
        assert "clusters" in status
        assert status["clusters"] == ["test-cluster"]
        assert status["deployments"] == 0
        assert status["services"] == 0


def run_tests():
    """Run all container management tests"""
    print("Running Container Management Tests\n" + "=" * 50)
    
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
    
    # Test basic deployment
    result = asyncio.run(orchestrator.deploy_service(
        "validation-app",
        "nginx:latest",
        replicas=2
    ))
    
    assert result["status"] == "deployed"
    assert len(result["endpoints"]) == 2
    print("✅ Basic deployment validation passed")
    
    exit(exit_code)