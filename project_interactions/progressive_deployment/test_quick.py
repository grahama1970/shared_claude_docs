"""Quick test of progressive deployment system with reduced durations"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



from progressive_deployment_interaction import ProgressiveDeploymentSystem

def quick_test():
    """Run a quick canary deployment test"""
    print("Testing Progressive Deployment System - Quick Test")
    print("=" * 60)
    
    deployer = ProgressiveDeploymentSystem()
    
    # Test 1: Quick canary deployment
    print("\n1. Testing Canary Deployment (10% increments)...")
    result = deployer.deploy_with_canary("service-v1.0-quick", traffic_percentage=25)
    print(f"   Status: {result['status']}")
    print(f"   Deployment ID: {result['deployment_id']}")
    if 'duration' in result:
        print(f"   Duration: {result['duration']}")
    
    # Test 2: Check deployment history
    print("\n2. Testing Deployment History...")
    history = deployer.get_deployment_history()
    print(f"   Total deployments tracked: {len(history)}")
    if history:
        latest = history[-1]
        print(f"   Latest deployment: {latest['deployment_id']} - {latest['status']}")
    
    # Test 3: Feature flags
    print("\n3. Testing Feature Flag Deployment...")
    flags = {"feature_a": True, "feature_b": False}
    result = deployer.deploy_with_feature_flags("service-v2.0-features", flags)
    print(f"   Status: {result['status']}")
    if 'enabled_features' in result:
        print(f"   Enabled features: {result['enabled_features']}")
    
    print("\n" + "=" * 60)
    print("Quick test completed successfully!")

if __name__ == "__main__":
    quick_test()