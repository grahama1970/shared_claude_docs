"""
Module: test_deployment_strategies.py
Purpose: Test deployment strategy implementations

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://github.com/pytest-dev/pytest-asyncio

Example Usage:
>>> pytest test_deployment_strategies.py -v
"""

import pytest
import asyncio
from typing import Dict, Any, List
import sys
from pathlib import Path
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from container_orchestrator_interaction import (
    ContainerOrchestrator, DeploymentStrategy, ContainerConfig
)


class TestDeploymentStrategies:
    """Test various deployment strategies"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance"""
        return ContainerOrchestrator()
    
    @pytest.mark.asyncio
    async def test_rolling_update_strategy(self, orchestrator):
        """Test rolling update deployment strategy"""
        # Deploy initial version
        result = await orchestrator.deploy_service(
            name="rolling-app",
            image="app:v1.0",
            replicas=6,
            strategy=DeploymentStrategy.ROLLING_UPDATE
        )
        
        assert result["status"] == "deployed"
        assert result["strategy"] == "rolling_update"
        
        # Check deployment configuration
        deployment = orchestrator.deployments["rolling-app"]
        strategy = deployment["spec"]["strategy"]
        assert strategy["type"] == "RollingUpdate"
        assert strategy["rollingUpdate"]["maxSurge"] == "25%"
        assert strategy["rollingUpdate"]["maxUnavailable"] == "25%"
        
        # Perform update
        update_result = await orchestrator.perform_rolling_update(
            "rolling-app",
            "app:v2.0",
            max_surge="33%",
            max_unavailable="33%"
        )
        
        assert update_result["status"] == "updating"
        assert update_result["old_image"] == "app:v1.0"
        assert update_result["new_image"] == "app:v2.0"
    
    @pytest.mark.asyncio
    async def test_blue_green_strategy(self, orchestrator):
        """Test blue-green deployment strategy"""
        # Deploy blue environment
        blue_result = await orchestrator.deploy_service(
            name="bg-app-blue",
            image="app:v1.0",
            replicas=3,
            strategy=DeploymentStrategy.BLUE_GREEN
        )
        
        assert blue_result["status"] == "deployed"
        
        # Deploy green environment
        green_result = await orchestrator.deploy_service(
            name="bg-app-green",
            image="app:v2.0",
            replicas=3,
            strategy=DeploymentStrategy.BLUE_GREEN
        )
        
        assert green_result["status"] == "deployed"
        
        # Check strategy configuration
        blue_deployment = orchestrator.deployments["bg-app-blue"]
        strategy = blue_deployment["spec"]["strategy"]
        assert strategy["rollingUpdate"]["maxSurge"] == "100%"
        assert strategy["rollingUpdate"]["maxUnavailable"] == "0%"
    
    @pytest.mark.asyncio
    async def test_canary_deployment(self, orchestrator):
        """Test canary deployment strategy"""
        # Deploy stable version
        stable_result = await orchestrator.deploy_service(
            name="canary-app-stable",
            image="app:v1.0",
            replicas=9,
            strategy=DeploymentStrategy.CANARY
        )
        
        # Deploy canary version (10% of traffic)
        canary_result = await orchestrator.deploy_service(
            name="canary-app-canary",
            image="app:v2.0",
            replicas=1,
            strategy=DeploymentStrategy.CANARY
        )
        
        assert stable_result["status"] == "deployed"
        assert canary_result["status"] == "deployed"
        
        # Check canary configuration
        canary_deployment = orchestrator.deployments["canary-app-canary"]
        strategy = canary_deployment["spec"]["strategy"]
        assert strategy["rollingUpdate"]["maxSurge"] == "10%"
        assert strategy["rollingUpdate"]["maxUnavailable"] == "0%"
    
    @pytest.mark.asyncio
    async def test_recreate_strategy(self, orchestrator):
        """Test recreate deployment strategy"""
        result = await orchestrator.deploy_service(
            name="recreate-app",
            image="app:v1.0",
            replicas=4,
            strategy=DeploymentStrategy.RECREATE
        )
        
        assert result["status"] == "deployed"
        assert result["strategy"] == "recreate"
        
        # Check deployment configuration
        deployment = orchestrator.deployments["recreate-app"]
        strategy = deployment["spec"]["strategy"]
        assert strategy["type"] == "Recreate"
        assert "rollingUpdate" not in strategy
    
    @pytest.mark.asyncio
    async def test_progressive_canary_rollout(self, orchestrator):
        """Test progressive canary rollout"""
        # Start with 100% stable
        await orchestrator.deploy_service(
            name="prog-canary-stable",
            image="app:v1.0",
            replicas=10
        )
        
        # Progressive canary stages
        canary_stages = [
            {"replicas": 1, "percentage": 10},
            {"replicas": 2, "percentage": 20},
            {"replicas": 5, "percentage": 50},
            {"replicas": 10, "percentage": 100}
        ]
        
        for stage in canary_stages:
            # Scale canary
            await orchestrator.deploy_service(
                name="prog-canary-new",
                image="app:v2.0",
                replicas=stage["replicas"],
                strategy=DeploymentStrategy.CANARY
            )
            
            # Scale down stable
            stable_replicas = 10 - stage["replicas"]
            if stable_replicas > 0:
                await orchestrator.scale_deployment(
                    "prog-canary-stable",
                    stable_replicas
                )
            
            # Verify distribution
            canary_deployment = orchestrator.deployments["prog-canary-new"]
            assert canary_deployment["spec"]["replicas"] == stage["replicas"]
            
            if stable_replicas > 0:
                stable_deployment = orchestrator.deployments["prog-canary-stable"]
                assert stable_deployment["spec"]["replicas"] == stable_replicas
    
    @pytest.mark.asyncio
    async def test_rollback_scenarios(self, orchestrator):
        """Test rollback scenarios for different strategies"""
        strategies = [
            DeploymentStrategy.ROLLING_UPDATE,
            DeploymentStrategy.BLUE_GREEN,
            DeploymentStrategy.CANARY
        ]
        
        for strategy in strategies:
            app_name = f"rollback-{strategy.value}"
            
            # Deploy initial version
            await orchestrator.deploy_service(
                name=app_name,
                image="app:v1.0",
                replicas=3,
                strategy=strategy
            )
            
            # Update to new version
            await orchestrator.perform_rolling_update(
                app_name,
                "app:v2.0"
            )
            
            # Rollback
            rollback_result = await orchestrator.rollback_deployment(
                app_name,
                revision=1
            )
            
            assert rollback_result["status"] == "rolled_back"
            assert rollback_result["deployment"] == app_name
    
    @pytest.mark.asyncio
    async def test_deployment_health_checks(self, orchestrator):
        """Test health checks during deployment"""
        # Deploy with health checks
        await orchestrator.deploy_service(
            name="health-deploy",
            image="app:v1.0",
            replicas=3
        )
        
        # Monitor health during update
        await orchestrator.perform_rolling_update(
            "health-deploy",
            "app:v2.0"
        )
        
        # Check health status
        health_result = await orchestrator.monitor_container_health(
            "health-deploy"
        )
        
        assert health_result["deployment"] == "health-deploy"
        assert all(
            container["ready"] for container in health_result["containers"]
        )
    
    @pytest.mark.asyncio
    async def test_traffic_splitting(self, orchestrator):
        """Test traffic splitting between versions"""
        # Deploy v1 (70% traffic)
        v1_result = await orchestrator.deploy_service(
            name="split-app-v1",
            image="app:v1.0",
            replicas=7
        )
        
        # Deploy v2 (30% traffic)
        v2_result = await orchestrator.deploy_service(
            name="split-app-v2",
            image="app:v2.0",
            replicas=3
        )
        
        # Setup load balancer with traffic split
        lb_v1 = await orchestrator.setup_load_balancer(
            "split-app-v1",
            algorithm="weighted_round_robin"
        )
        
        lb_v2 = await orchestrator.setup_load_balancer(
            "split-app-v2",
            algorithm="weighted_round_robin"
        )
        
        assert lb_v1["backends"] == 7
        assert lb_v2["backends"] == 3
    
    @pytest.mark.asyncio
    async def test_deployment_validation(self, orchestrator):
        """Test deployment validation and checks"""
        # Deploy with specific configuration
        await orchestrator.deploy_service(
            name="validate-app",
            image="app:v1.0",
            replicas=5,
            ports=[8080, 8443],
            environment={
                "ENV": "production",
                "VERSION": "1.0.0"
            }
        )
        
        # Validate deployment exists
        assert "validate-app" in orchestrator.deployments
        
        # Validate service configuration
        assert "validate-app" in orchestrator.services
        service = orchestrator.services["validate-app"]
        assert len(service.ports) == 2
        
        # Validate container configuration
        deployment = orchestrator.deployments["validate-app"]
        container = deployment["spec"]["template"]["spec"]["containers"][0]
        assert len(container["env"]) == 2
        assert container["image"] == "app:v1.0"
    
    @pytest.mark.asyncio
    async def test_multi_stage_deployment(self, orchestrator):
        """Test multi-stage deployment process"""
        stages = [
            {"name": "dev", "replicas": 1, "image": "app:dev"},
            {"name": "staging", "replicas": 2, "image": "app:staging"},
            {"name": "production", "replicas": 5, "image": "app:v1.0"}
        ]
        
        deployment_results = []
        
        for stage in stages:
            result = await orchestrator.deploy_service(
                name=f"ms-app-{stage['name']}",
                image=stage["image"],
                replicas=stage["replicas"],
                environment={"STAGE": stage["name"]}
            )
            
            deployment_results.append(result)
            assert result["status"] == "deployed"
            assert result["replicas"] == stage["replicas"]
        
        # Verify all stages deployed
        status = orchestrator.get_cluster_status()
        assert status["deployments"] >= len(stages)


def run_tests():
    """Run all deployment strategy tests"""
    print("Running Deployment Strategy Tests\n" + "=" * 50)
    
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
    
    # Test different strategies
    async def validate_strategies():
        strategies_tested = []
        
        for strategy in DeploymentStrategy:
            result = await orchestrator.deploy_service(
                name=f"validate-{strategy.value}",
                image="nginx:latest",
                replicas=2,
                strategy=strategy
            )
            
            assert result["status"] == "deployed"
            assert result["strategy"] == strategy.value
            strategies_tested.append(strategy.value)
        
        print(f"✅ All deployment strategies validated: {strategies_tested}")
    
    asyncio.run(validate_strategies())
    
    exit(exit_code)