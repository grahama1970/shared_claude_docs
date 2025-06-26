"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""Test deployment workflow functionality"""

import sys
import time
from datetime import datetime
sys.path.insert(0, "/home/graham/workspace/shared_claude_docs")

from project_interactions.ai_model_registry.ai_model_registry_interaction import (
    AIModelRegistry, ModelType, ModelStatus, DeploymentStage, 
    DeploymentStrategy, Deployment
)


def test_deployment_creation():
    """Test deployment creation"""
    registry = AIModelRegistry()
    
    # Setup model
    model_id = registry.register_model(
        name="deploy-test",
        model_type=ModelType.CLASSIFICATION,
        framework="tensorflow"
    )
    
    version = registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/deploy.pb"
    )
    
    # Create deployment
    deployment = registry.create_deployment(
        model_id=model_id,
        version="1.0.0",
        stage=DeploymentStage.STAGING,
        strategy=DeploymentStrategy.BLUE_GREEN,
        config={
            "replicas": 3,
            "cpu_limit": "2",
            "memory_limit": "4Gi"
        }
    )
    
    assert deployment is not None, "Deployment creation failed"
    assert deployment.stage == DeploymentStage.STAGING, "Wrong deployment stage"
    assert deployment.config["replicas"] == 3, "Config not saved"
    
    print("✓ Deployment creation test passed")


def test_deployment_strategies():
    """Test different deployment strategies"""
    registry = AIModelRegistry()
    
    # Setup
    model_id = registry.register_model(
        name="strategy-test",
        model_type=ModelType.NLP,
        framework="transformers"
    )
    
    registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/v1.bin"
    )
    
    registry.create_version(
        model_id=model_id,
        version="2.0.0",
        path="/models/v2.bin"
    )
    
    # Test blue-green deployment
    bg_deploy = registry.create_deployment(
        model_id=model_id,
        version="2.0.0",
        stage=DeploymentStage.PRODUCTION,
        strategy=DeploymentStrategy.BLUE_GREEN
    )
    
    assert bg_deploy.strategy == DeploymentStrategy.BLUE_GREEN, "Wrong strategy"
    
    # Test canary deployment
    canary_deploy = registry.create_deployment(
        model_id=model_id,
        version="2.0.0",
        stage=DeploymentStage.PRODUCTION,
        strategy=DeploymentStrategy.CANARY,
        config={"canary_percentage": 10}
    )
    
    assert canary_deploy.config["canary_percentage"] == 10, "Canary config missing"
    
    # Test rolling update
    rolling_deploy = registry.create_deployment(
        model_id=model_id,
        version="2.0.0",
        stage=DeploymentStage.PRODUCTION,
        strategy=DeploymentStrategy.ROLLING,
        config={"max_surge": 1, "max_unavailable": 0}
    )
    
    assert rolling_deploy.config["max_surge"] == 1, "Rolling config missing"
    
    print("✓ Deployment strategies test passed")


def test_deployment_promotion():
    """Test deployment promotion through stages"""
    registry = AIModelRegistry()
    
    # Setup
    model_id = registry.register_model(
        name="promote-test",
        model_type=ModelType.REGRESSION,
        framework="scikit-learn"
    )
    
    registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/promote.pkl"
    )
    
    # Start in dev
    deployment = registry.create_deployment(
        model_id=model_id,
        version="1.0.0",
        stage=DeploymentStage.DEVELOPMENT
    )
    
    # Promote to staging
    promoted = registry.promote_deployment(
        deployment_id=deployment.id,
        target_stage=DeploymentStage.STAGING
    )
    
    assert promoted.stage == DeploymentStage.STAGING, "Promotion failed"
    assert promoted.model_id == model_id, "Model ID changed"
    
    # Promote to production
    prod = registry.promote_deployment(
        deployment_id=promoted.id,
        target_stage=DeploymentStage.PRODUCTION
    )
    
    assert prod.stage == DeploymentStage.PRODUCTION, "Production promotion failed"
    
    print("✓ Deployment promotion test passed")


def test_deployment_rollback():
    """Test deployment rollback"""
    registry = AIModelRegistry()
    
    # Setup with multiple versions
    model_id = registry.register_model(
        name="rollback-test",
        model_type=ModelType.CLASSIFICATION,
        framework="pytorch"
    )
    
    # Version 1 (stable)
    v1 = registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/v1.pt"
    )
    
    deploy1 = registry.create_deployment(
        model_id=model_id,
        version="1.0.0",
        stage=DeploymentStage.PRODUCTION
    )
    
    # Version 2 (problematic)
    v2 = registry.create_version(
        model_id=model_id,
        version="2.0.0",
        path="/models/v2.pt"
    )
    
    deploy2 = registry.create_deployment(
        model_id=model_id,
        version="2.0.0",
        stage=DeploymentStage.PRODUCTION
    )
    
    # Simulate issue and rollback
    rollback = registry.rollback_deployment(
        model_id=model_id,
        stage=DeploymentStage.PRODUCTION,
        target_version="1.0.0"
    )
    
    assert rollback.version == "1.0.0", "Rollback to wrong version"
    assert rollback.stage == DeploymentStage.PRODUCTION, "Wrong stage after rollback"
    
    print("✓ Deployment rollback test passed")


def test_deployment_monitoring():
    """Test deployment monitoring and health checks"""
    registry = AIModelRegistry()
    
    # Setup
    model_id = registry.register_model(
        name="monitor-test",
        model_type=ModelType.IMAGE_CLASSIFICATION,
        framework="tensorflow"
    )
    
    registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/monitor.pb"
    )
    
    deployment = registry.create_deployment(
        model_id=model_id,
        version="1.0.0",
        stage=DeploymentStage.PRODUCTION
    )
    
    # Log deployment metrics
    registry.log_deployment_metrics(
        deployment_id=deployment.id,
        metrics={
            "request_count": 1000,
            "error_count": 5,
            "avg_latency_ms": 45,
            "cpu_usage_percent": 65
        }
    )
    
    # Check deployment health
    health = registry.check_deployment_health(deployment.id)
    
    assert health["status"] == "healthy", "Deployment not healthy"
    assert health["error_rate"] == 0.005, "Wrong error rate calculation"
    assert health["metrics"]["request_count"] == 1000, "Metrics not stored"
    
    print("✓ Deployment monitoring test passed")


def test_multi_stage_deployment():
    """Test multi-stage deployment workflow"""
    registry = AIModelRegistry()
    
    # Setup
    model_id = registry.register_model(
        name="multistage-test",
        model_type=ModelType.CUSTOM,
        framework="custom"
    )
    
    registry.create_version(
        model_id=model_id,
        version="3.0.0",
        path="/models/v3.model"
    )
    
    # Get active deployments
    initial = registry.get_active_deployments(model_id)
    assert len(initial) == 0, "Unexpected active deployments"
    
    # Deploy to multiple stages
    dev_deploy = registry.create_deployment(
        model_id=model_id,
        version="3.0.0",
        stage=DeploymentStage.DEVELOPMENT
    )
    
    staging_deploy = registry.create_deployment(
        model_id=model_id,
        version="3.0.0",
        stage=DeploymentStage.STAGING
    )
    
    # Check active deployments
    active = registry.get_active_deployments(model_id)
    assert len(active) == 2, "Wrong number of active deployments"
    
    stages = {d.stage for d in active}
    assert DeploymentStage.DEVELOPMENT in stages, "Dev deployment missing"
    assert DeploymentStage.STAGING in stages, "Staging deployment missing"
    
    print("✓ Multi-stage deployment test passed")


def test_deployment_history():
    """Test deployment history tracking"""
    registry = AIModelRegistry()
    
    # Setup
    model_id = registry.register_model(
        name="history-test",
        model_type=ModelType.TIME_SERIES,
        framework="statsmodels"
    )
    
    # Create versions and deployments
    for i in range(3):
        version = f"{i+1}.0.0"
        registry.create_version(
            model_id=model_id,
            version=version,
            path=f"/models/v{i+1}.pkl"
        )
        
        registry.create_deployment(
            model_id=model_id,
            version=version,
            stage=DeploymentStage.PRODUCTION
        )
        
        time.sleep(0.01)  # Ensure different timestamps
    
    # Get deployment history
    history = registry.get_deployment_history(
        model_id=model_id,
        stage=DeploymentStage.PRODUCTION
    )
    
    assert len(history) == 3, "Incomplete deployment history"
    
    # Check chronological order
    timestamps = [d.created_at for d in history]
    assert timestamps == sorted(timestamps), "History not in order"
    
    # Check versions
    versions = [d.version for d in history]
    assert versions == ["1.0.0", "2.0.0", "3.0.0"], "Wrong version history"
    
    print("✓ Deployment history test passed")


if __name__ == "__main__":
    test_deployment_creation()
    test_deployment_strategies()
    test_deployment_promotion()
    test_deployment_rollback()
    test_deployment_monitoring()
    test_multi_stage_deployment()
    test_deployment_history()
    print("\n✅ All deployment workflow tests passed")