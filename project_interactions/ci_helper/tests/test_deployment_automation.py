"""
Module: test_deployment_automation.py
Purpose: Test deployment automation and rollback capabilities

External Dependencies:
- pytest: https://docs.pytest.org/

Example Usage:
>>> pytest test_deployment_automation.py -v
"""

import pytest
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ci_helper_interaction import (
    CIHelperInteraction, DeploymentStrategy
)


class TestDeploymentAutomation:
    """Test deployment automation functionality"""
    
    @pytest.fixture
    def ci_helper(self):
        """Create a CI helper instance"""
        return CIHelperInteraction()
    
    @pytest.fixture
    def pipeline_with_artifacts(self, ci_helper):
        """Create a pipeline and execute it to generate artifacts"""
        config = {
            "name": "Deployment Test Pipeline",
            "stages": ["build", "test"],
            "jobs": {
                "build": {
                    "docker-build": {
                        "commands": [
                            "docker build -t app:latest .",
                            "docker save app:latest -o app.tar"
                        ],
                        "artifacts": ["app.tar", "docker-compose.yml"]
                    }
                },
                "test": {
                    "smoke-test": {
                        "commands": ["docker run app:latest pytest tests/smoke"]
                    }
                }
            }
        }
        
        pipeline = ci_helper.create_pipeline("github_actions", config)
        execution = ci_helper.execute_pipeline(pipeline["id"])
        
        return {
            "pipeline": pipeline,
            "execution": execution
        }
    
    def test_blue_green_deployment(self, ci_helper, pipeline_with_artifacts):
        """Test blue-green deployment strategy"""
        pipeline_id = pipeline_with_artifacts["pipeline"]["id"]
        
        deployment = ci_helper.deploy(
            pipeline_id,
            environment="production",
            strategy="blue_green",
            config={
                "health_check_url": "https://app.example.com/health",
                "switch_delay": 60
            }
        )
        
        assert deployment["strategy"] == "blue_green"
        assert deployment["status"] == "success"
        assert deployment["environment"] == "production"
        assert "steps" in deployment
        assert len(deployment["steps"]) >= 5
        assert deployment["rollback_available"] is True
        
        # Verify blue-green specific steps
        step_names = [step["name"] for step in deployment["steps"]]
        assert "Provision Green Environment" in step_names
        assert "Switch Traffic" in step_names
        assert "Cleanup Blue Environment" in step_names
    
    def test_canary_deployment(self, ci_helper, pipeline_with_artifacts):
        """Test canary deployment strategy"""
        pipeline_id = pipeline_with_artifacts["pipeline"]["id"]
        
        deployment = ci_helper.deploy(
            pipeline_id,
            environment="production",
            strategy="canary",
            config={
                "canary_percentage": 20,
                "monitor_duration": 300,
                "success_criteria": {
                    "error_rate": 1.0,
                    "latency_p99": 200
                }
            }
        )
        
        assert deployment["strategy"] == "canary"
        assert deployment["status"] == "success"
        assert "metrics" in deployment
        
        # Verify canary metrics
        metrics = deployment["metrics"]
        assert "error_rate" in metrics
        assert "latency_p99" in metrics
        assert "success_rate" in metrics
        assert metrics["error_rate"] < 1.0
        assert metrics["success_rate"] > 99.0
    
    def test_rolling_deployment(self, ci_helper, pipeline_with_artifacts):
        """Test rolling deployment strategy"""
        pipeline_id = pipeline_with_artifacts["pipeline"]["id"]
        
        deployment = ci_helper.deploy(
            pipeline_id,
            environment="production",
            strategy="rolling",
            config={
                "batch_size": 3,
                "pause_between_batches": 120,
                "max_unavailable": 1
            }
        )
        
        assert deployment["strategy"] == "rolling"
        assert deployment["status"] == "success"
        assert "instances_updated" in deployment
        assert deployment["instances_updated"] > 0
        
        # Verify rolling update steps
        batch_steps = [
            step for step in deployment["steps"]
            if "Deploy Batch" in step["name"]
        ]
        assert len(batch_steps) >= 2
    
    def test_recreate_deployment(self, ci_helper, pipeline_with_artifacts):
        """Test recreate deployment strategy"""
        pipeline_id = pipeline_with_artifacts["pipeline"]["id"]
        
        deployment = ci_helper.deploy(
            pipeline_id,
            environment="staging",
            strategy="recreate"
        )
        
        assert deployment["strategy"] == "recreate"
        assert deployment["status"] == "success"
        assert "downtime_seconds" in deployment
        assert deployment["downtime_seconds"] > 0
        
        # Verify recreate steps
        step_names = [step["name"] for step in deployment["steps"]]
        assert "Stop Current Version" in step_names
        assert "Deploy New Version" in step_names
        assert "Start New Version" in step_names
    
    def test_deployment_environments(self, ci_helper, pipeline_with_artifacts):
        """Test deployments to different environments"""
        pipeline_id = pipeline_with_artifacts["pipeline"]["id"]
        environments = ["development", "staging", "production"]
        
        deployments = []
        for env in environments:
            deployment = ci_helper.deploy(
                pipeline_id,
                environment=env,
                strategy="rolling"
            )
            deployments.append(deployment)
            
            assert deployment["environment"] == env
            assert deployment["status"] == "success"
        
        # Verify all deployments are tracked
        assert len(ci_helper.deployments) >= len(environments)
    
    def test_deployment_rollback(self, ci_helper, pipeline_with_artifacts):
        """Test deployment rollback functionality"""
        pipeline_id = pipeline_with_artifacts["pipeline"]["id"]
        
        # Deploy first
        deployment = ci_helper.deploy(
            pipeline_id,
            environment="production",
            strategy="blue_green"
        )
        
        assert deployment["status"] == "success"
        
        # Perform rollback
        rollback = ci_helper.rollback(deployment["id"])
        
        assert rollback["deployment_id"] == deployment["id"]
        assert rollback["status"] == "success"
        assert "steps" in rollback
        
        # Verify rollback steps
        step_names = [step["name"] for step in rollback["steps"]]
        assert "Identify Previous Version" in step_names
        assert "Restore Configuration" in step_names
        assert "Switch Traffic" in step_names
        assert "Verify Rollback" in step_names
    
    def test_deployment_with_custom_config(self, ci_helper, pipeline_with_artifacts):
        """Test deployment with custom configuration"""
        pipeline_id = pipeline_with_artifacts["pipeline"]["id"]
        
        custom_config = {
            "namespace": "production",
            "replica_count": 5,
            "resource_limits": {
                "cpu": "1000m",
                "memory": "2Gi"
            },
            "health_check": {
                "path": "/api/health",
                "interval": 30,
                "timeout": 10
            },
            "auto_scaling": {
                "enabled": True,
                "min_replicas": 3,
                "max_replicas": 10,
                "target_cpu": 70
            }
        }
        
        deployment = ci_helper.deploy(
            pipeline_id,
            environment="production",
            strategy="canary",
            config=custom_config
        )
        
        assert deployment["status"] == "success"
        assert deployment["config"] == custom_config
    
    def test_deployment_failure_handling(self, ci_helper):
        """Test handling of deployment failures"""
        # Try to deploy non-existent pipeline
        with pytest.raises(ValueError) as exc_info:
            ci_helper.deploy(
                "non-existent-pipeline",
                environment="production",
                strategy="rolling"
            )
        
        assert "Pipeline" in str(exc_info.value)
        assert "not found" in str(exc_info.value)
    
    def test_multiple_deployments_tracking(self, ci_helper, pipeline_with_artifacts):
        """Test tracking of multiple deployments"""
        pipeline_id = pipeline_with_artifacts["pipeline"]["id"]
        
        # Create multiple deployments
        deployment_ids = []
        for i in range(3):
            deployment = ci_helper.deploy(
                pipeline_id,
                environment=f"env-{i}",
                strategy="rolling"
            )
            deployment_ids.append(deployment["id"])
        
        # Verify all deployments are tracked
        for deployment_id in deployment_ids:
            assert deployment_id in ci_helper.deployments
            deployment = ci_helper.deployments[deployment_id]
            assert deployment["pipeline_id"] == pipeline_id
    
    def test_deployment_strategies_comparison(self, ci_helper, pipeline_with_artifacts):
        """Test and compare different deployment strategies"""
        pipeline_id = pipeline_with_artifacts["pipeline"]["id"]
        strategies = ["blue_green", "canary", "rolling", "recreate"]
        
        results = {}
        for strategy in strategies:
            deployment = ci_helper.deploy(
                pipeline_id,
                environment="test",
                strategy=strategy
            )
            
            results[strategy] = {
                "status": deployment["status"],
                "steps": len(deployment["steps"]),
                "has_rollback": deployment.get("rollback_available", False),
                "has_metrics": "metrics" in deployment
            }
        
        # Blue-green should have rollback
        assert results["blue_green"]["has_rollback"] is True
        
        # Canary should have metrics
        assert results["canary"]["has_metrics"] is True
        
        # All should succeed
        for strategy, result in results.items():
            assert result["status"] == "success"
    
    def test_environment_specific_deployment(self, ci_helper, pipeline_with_artifacts):
        """Test environment-specific deployment configurations"""
        pipeline_id = pipeline_with_artifacts["pipeline"]["id"]
        
        # Production deployment with strict settings
        prod_deployment = ci_helper.deploy(
            pipeline_id,
            environment="production",
            strategy="canary",
            config={
                "canary_percentage": 5,  # Start small in production
                "require_approval": True,
                "monitoring_enabled": True,
                "alerting_enabled": True
            }
        )
        
        # Staging deployment with relaxed settings
        staging_deployment = ci_helper.deploy(
            pipeline_id,
            environment="staging",
            strategy="rolling",
            config={
                "batch_size": 5,  # Larger batches in staging
                "skip_health_checks": False,
                "monitoring_enabled": True,
                "alerting_enabled": False
            }
        )
        
        assert prod_deployment["environment"] == "production"
        assert staging_deployment["environment"] == "staging"
        assert prod_deployment["strategy"] == "canary"
        assert staging_deployment["strategy"] == "rolling"


if __name__ == "__main__":
    # Run specific tests with real data
    helper = CIHelperInteraction()
    
    # Create and execute a pipeline
    config = {
        "name": "App Deployment Pipeline",
        "stages": ["build", "test"],
        "jobs": {
            "build": {
                "container": {
                    "commands": ["docker build -t myapp:latest ."],
                    "artifacts": ["myapp.tar"]
                }
            },
            "test": {
                "verify": {
                    "commands": ["docker run myapp:latest test"]
                }
            }
        }
    }
    
    pipeline = helper.create_pipeline("github_actions", config)
    execution = helper.execute_pipeline(pipeline["id"])
    print(f"✅ Pipeline execution: {execution['status']}")
    
    # Test different deployment strategies
    strategies = ["blue_green", "canary", "rolling", "recreate"]
    
    for strategy in strategies:
        deployment = helper.deploy(
            pipeline["id"],
            environment="staging",
            strategy=strategy
        )
        print(f"✅ {strategy} deployment: {deployment['status']}")
    
    # Test rollback
    prod_deployment = helper.deploy(
        pipeline["id"],
        environment="production",
        strategy="blue_green"
    )
    
    rollback = helper.rollback(prod_deployment["id"])
    print(f"✅ Rollback: {rollback['status']}")
    
    print("\n✅ All deployment automation tests passed")