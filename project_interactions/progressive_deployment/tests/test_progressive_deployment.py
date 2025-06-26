"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Test module for Task #020: Progressive Deployment with Rollback.

These tests validate GRANGER requirements for safe deployment strategies
including canary, blue-green, and feature flag deployments with automatic
health monitoring and rollback capabilities.
"""

import pytest
import asyncio
import time
import json
from pathlib import Path
from datetime import datetime

# Import from the module
import sys
sys.path.insert(0, "/home/graham/workspace/shared_claude_docs/project_interactions/progressive_deployment")

from progressive_deployment_interaction import (
    ProgressiveDeploymentSystem,
    DeploymentStrategy,
    DeploymentStatus,
    DeploymentConfig,
    DeploymentState,
    HealthMetrics
)


class TestProgressiveDeployment:
    """Test suite for Task #020: Progressive Deployment."""
    
    @pytest.fixture
    def deployer(self):
        """Create a fresh deployment system."""
        return ProgressiveDeploymentSystem(state_dir="./test_deployment_state")
    
    def test_canary_deployment_success(self, deployer):
        """
        Test 020.1: Successful canary deployment.
        Expected duration: 8.0s-15.0s
        """
        start_time = time.time()
        
        # Clear any failures and deploy
        deployer.clear_failures()
        result = deployer.deploy_with_canary("service-v1.5", traffic_percentage=20)
        
        duration = time.time() - start_time
        
        # Verify
        assert result["status"] == "completed", f"Deployment failed: {result}"
        assert 8.0 <= duration <= 15.0, f"Duration {duration:.2f}s outside expected range"
        assert "deployment_id" in result
        assert "duration" in result
        assert "final_metrics" in result
        
        # Check metrics
        metrics = result.get("final_metrics", {})
        assert metrics.get("avg_success_rate", 0) > 0.9, "Success rate too low"
        assert metrics.get("avg_error_rate", 1) < 0.1, "Error rate too high"
        
        print(f"✓ Canary deployment completed in {duration:.2f}s")
    
    def test_canary_deployment_rollback(self, deployer):
        """
        Test 020.2: Canary deployment with automatic rollback.
        Expected duration: 5.0s-12.0s
        """
        start_time = time.time()
        
        # Deploy version that triggers issues at higher traffic
        result = deployer.deploy_with_canary("service-v2.0", traffic_percentage=25)
        
        duration = time.time() - start_time
        
        # Verify rollback occurred
        assert result["status"] == "rolled_back", f"Expected rollback but got: {result['status']}"
        assert 5.0 <= duration <= 12.0, f"Duration {duration:.2f}s outside expected range"
        assert "reason" in result
        assert "final_traffic_percentage" in result
        assert result["final_traffic_percentage"] < 100, "Should have rolled back before 100%"
        
        print(f"✓ Canary rollback triggered correctly in {duration:.2f}s at {result['final_traffic_percentage']}% traffic")
    
    def test_blue_green_deployment(self, deployer):
        """
        Test 020.3: Blue-green deployment with instant switch.
        Expected duration: 13.0s-20.0s
        """
        start_time = time.time()
        
        # Clear failures and deploy
        deployer.clear_failures()
        result = deployer.deploy_blue_green("service-v3.0")
        
        duration = time.time() - start_time
        
        # Verify
        assert result["status"] == "completed", f"Deployment failed: {result}"
        assert 13.0 <= duration <= 20.0, f"Duration {duration:.2f}s outside expected range"
        assert result.get("switch_time") == "instant", "Should have instant traffic switch"
        
        print(f"✓ Blue-green deployment with instant switch in {duration:.2f}s")
    
    def test_feature_flag_deployment(self, deployer):
        """
        Test 020.4: Feature flag progressive deployment.
        Expected duration: 6.0s-12.0s
        """
        start_time = time.time()
        
        # Deploy with feature flags
        feature_flags = {
            "new_ui": True,
            "advanced_analytics": True,
            "experimental_feature": False
        }
        
        result = deployer.deploy_with_feature_flags("service-v4.0", feature_flags)
        
        duration = time.time() - start_time
        
        # Verify
        assert result["status"] in ["completed", "partial_success"]
        assert 6.0 <= duration <= 12.0, f"Duration {duration:.2f}s outside expected range"
        assert "enabled_features" in result
        assert len(result["enabled_features"]) >= 1, "Should enable at least one feature"
        
        # Check that non-enabled features weren't deployed
        assert "experimental_feature" not in result["enabled_features"]
        
        print(f"✓ Feature flag deployment enabled {len(result['enabled_features'])} features in {duration:.2f}s")
    
    def test_monitoring_and_metrics(self, deployer):
        """
        Test 020.5: Health monitoring and metrics collection.
        Expected duration: 1.0s-3.0s
        """
        start_time = time.time()
        
        # Create a test deployment state
        config = DeploymentConfig(
            service_name="monitor-test",
            version="v1.0",
            strategy=DeploymentStrategy.CANARY,
            monitoring_duration_minutes=0.1,  # 6 seconds for quick test
            health_check_interval_seconds=1
        )
        
        state = DeploymentState(
            deployment_id=f"test-monitor-{int(time.time())}",
            config=config,
            status=DeploymentStatus.MONITORING,
            start_time=datetime.now(),
            current_traffic_percentage=100
        )
        
        # Run monitoring
        result = asyncio.run(deployer._monitor_deployment_health(state, duration_minutes=0.1))
        
        duration = time.time() - start_time
        
        # Verify
        assert 1.0 <= duration <= 3.0, f"Duration {duration:.2f}s outside expected range"
        assert "healthy" in result
        assert "metrics" in result
        assert len(state.metrics_history) > 0, "Should collect metrics"
        
        # Check aggregated metrics
        metrics = result["metrics"]
        assert "avg_response_time_ms" in metrics
        assert "avg_success_rate" in metrics
        assert "max_error_rate" in metrics
        
        print(f"✓ Collected {len(state.metrics_history)} metrics in {duration:.2f}s")
    
    def test_state_persistence(self, deployer):
        """
        Test 020.6: Deployment state persistence.
        Expected duration: 0.1s-1.0s
        """
        start_time = time.time()
        
        # Create and save deployment state
        deployment_id = f"test-persist-{int(time.time())}"
        config = DeploymentConfig(
            service_name="persist-test",
            version="v1.0",
            strategy=DeploymentStrategy.CANARY
        )
        
        state = DeploymentState(
            deployment_id=deployment_id,
            config=config,
            status=DeploymentStatus.COMPLETED,
            start_time=datetime.now()
        )
        
        # Add test data
        state.add_event("test_event", {"key": "value"})
        state.metrics_history.append(HealthMetrics(
            response_time_ms=100,
            error_rate=0.01,
            success_rate=0.99,
            cpu_usage=0.5,
            memory_usage=0.6,
            active_connections=500
        ))
        
        # Save and load
        deployer._save_deployment_state(state)
        loaded = deployer.get_deployment_state(deployment_id)
        
        duration = time.time() - start_time
        
        # Verify
        assert 0.1 <= duration <= 1.0, f"Duration {duration:.2f}s outside expected range"
        assert loaded is not None, "Failed to load state"
        assert loaded["deployment_id"] == deployment_id
        assert loaded["status"] == "completed"
        assert len(loaded["events"]) > 0
        assert len(loaded["metrics_history"]) > 0
        
        print(f"✓ State persistence verified in {duration:.2f}s")


class TestHoneypot:
    """Honeypot tests for edge cases."""
    
    @pytest.fixture
    def deployer(self):
        """Create a fresh deployment system."""
        return ProgressiveDeploymentSystem(state_dir="./test_deployment_state")
    
    def test_critical_failure_rollback(self, deployer):
        """
        Test 020.H: HONEYPOT - Critical failure triggers immediate rollback.
        Expected duration: 2.0s-8.0s
        """
        start_time = time.time()
        
        # Inject critical failure
        deployer.simulate_failure("critical")
        
        try:
            # Attempt deployment
            result = deployer.deploy_with_canary("service-fail", traffic_percentage=10)
            
            duration = time.time() - start_time
            
            # Should have rolled back quickly
            assert result["status"] == "rolled_back", "Should rollback on critical failure"
            assert 2.0 <= duration <= 8.0, f"Duration {duration:.2f}s - should fail fast"
            assert result.get("final_traffic_percentage", 100) <= 10, "Should rollback at first increment"
            
            print("✓ Honeypot passed: Critical failure triggered immediate rollback")
            
        finally:
            deployer.clear_failures()