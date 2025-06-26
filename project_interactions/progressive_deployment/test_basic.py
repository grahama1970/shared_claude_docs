"""Basic test of progressive deployment components"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



from progressive_deployment_interaction import (
    DeploymentConfig, DeploymentStrategy, DeploymentStatus,
    DeploymentState, HealthMetrics, ServiceSimulator
)
from datetime import datetime

def test_components():
    """Test basic components of the deployment system"""
    print("Testing Progressive Deployment Components")
    print("=" * 60)
    
    # Test 1: Health Metrics
    print("\n1. Testing Health Metrics...")
    metrics = HealthMetrics(
        response_time_ms=500,
        error_rate=0.02,
        success_rate=0.98,
        cpu_usage=0.65,
        memory_usage=0.70,
        active_connections=250
    )
    
    thresholds = {
        "max_response_time_ms": 1000,
        "max_error_rate": 0.05,
        "min_success_rate": 0.95,
        "max_cpu_usage": 0.80,
        "max_memory_usage": 0.85
    }
    
    is_healthy, violations = metrics.is_healthy(thresholds)
    print(f"   Metrics healthy: {is_healthy}")
    print(f"   Response time: {metrics.response_time_ms}ms")
    print(f"   Error rate: {metrics.error_rate:.2%}")
    print(f"   CPU usage: {metrics.cpu_usage:.2%}")
    
    # Test 2: Deployment Configuration
    print("\n2. Testing Deployment Configuration...")
    config = DeploymentConfig(
        service_name="test-service",
        version="v1.0",
        strategy=DeploymentStrategy.CANARY,
        traffic_increment_percentage=20
    )
    print(f"   Service: {config.service_name}")
    print(f"   Version: {config.version}")
    print(f"   Strategy: {config.strategy.value}")
    print(f"   Traffic increment: {config.traffic_increment_percentage}%")
    
    # Test 3: Deployment State
    print("\n3. Testing Deployment State...")
    state = DeploymentState(
        deployment_id="test-deploy-123",
        config=config,
        status=DeploymentStatus.IN_PROGRESS,
        start_time=datetime.now()
    )
    
    state.add_event("test_started", {"test": True})
    state.current_traffic_percentage = 50
    
    print(f"   Deployment ID: {state.deployment_id}")
    print(f"   Status: {state.status.value}")
    print(f"   Traffic: {state.current_traffic_percentage}%")
    print(f"   Events: {len(state.events)}")
    
    # Test 4: Service Simulator
    print("\n4. Testing Service Simulator...")
    simulator = ServiceSimulator()
    
    # Normal metrics
    normal_metrics = simulator.get_metrics("v1.0", 50)
    print(f"   Normal response time: {normal_metrics.response_time_ms:.0f}ms")
    print(f"   Normal error rate: {normal_metrics.error_rate:.3f}")
    
    # Inject failure
    simulator.failure_injection = True
    failed_metrics = simulator.get_metrics("v1.0", 50)
    print(f"   Failed response time: {failed_metrics.response_time_ms:.0f}ms")
    print(f"   Failed error rate: {failed_metrics.error_rate:.3f}")
    
    # Test 5: State Serialization
    print("\n5. Testing State Serialization...")
    state_dict = state.to_dict()
    print(f"   Serialized keys: {list(state_dict.keys())}")
    print(f"   Can serialize: {'deployment_id' in state_dict}")
    
    print("\n" + "=" * 60)
    print("All component tests completed successfully!")
    
    return True

if __name__ == "__main__":
    success = test_components()
    exit(0 if success else 1)