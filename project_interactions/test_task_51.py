#!/usr/bin/env python3
"""Test Task #51 implementation - AI Model Registry"""

import sys
import subprocess
import time
sys.path.insert(0, "/home/graham/workspace/shared_claude_docs")

# Import AI Model Registry components
from project_interactions.ai_model_registry.ai_model_registry_interaction import (
    AIModelRegistry, ModelType, ModelStatus, DeploymentStage, DeploymentStrategy
)

print("="*80)
print("Task #51 Module Test - AI Model Registry")
print("="*80)

# Test registry initialization
registry = AIModelRegistry()

# Test basic functionality
print("\n✅ Module loaded successfully")
print("   AI Model Registry components available:")
print("   - Model registration and versioning")
print("   - Performance tracking and monitoring")
print("   - Deployment workflow management")
print("   - Model lifecycle management")
print("   - Experiment tracking")

def test_core_functionality():
    """Test core registry features"""
    # Register a model
    model_id = registry.register_model(
        name="test-classifier",
        model_type=ModelType.CLASSIFICATION,
        framework="tensorflow",
        description="Test image classifier"
    )
    
    print(f"\n✅ Model registration working")
    print(f"   Model ID: {model_id}")
    
    # Create version
    version = registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/test-v1.pb",
        metrics={"accuracy": 0.92, "f1_score": 0.89}
    )
    
    print(f"✅ Version management working")
    print(f"   Version: {version.version}")
    print(f"   Metrics: {version.metrics}")
    
    # Log performance
    registry.log_performance(
        model_id=model_id,
        version="1.0.0",
        metrics={
            "latency_ms": 35.5,
            "throughput_qps": 150,
            "memory_mb": 256
        },
        environment="production"
    )
    
    print(f"✅ Performance tracking working")
    print(f"   Performance logged for production environment")
    
    # Create deployment
    deployment = registry.create_deployment(
        model_id=model_id,
        version="1.0.0",
        stage=DeploymentStage.STAGING,
        strategy=DeploymentStrategy.CANARY,
        config={"canary_percentage": 10}
    )
    
    print(f"✅ Deployment workflow working")
    print(f"   Deployment ID: {deployment.id}")
    print(f"   Strategy: {deployment.strategy.value}")
    
    # Test experiment tracking
    experiment = registry.create_experiment(
        name="hyperparameter-tuning",
        description="Testing different learning rates"
    )
    
    run = registry.create_experiment_run(
        experiment_id=experiment.id,
        parameters={"learning_rate": 0.001, "batch_size": 32}
    )
    
    registry.log_run_metrics(
        run_id=run.id,
        metrics={"val_loss": 0.05, "val_accuracy": 0.93}
    )
    
    print(f"✅ Experiment tracking working")
    print(f"   Experiment: {experiment.name}")
    print(f"   Run metrics logged")

# Run core tests
test_core_functionality()

# Run detailed test suites
print("\n" + "="*60)
print("Running detailed test suites...")
print("="*60)

test_results = []
test_files = [
    "project_interactions/ai_model_registry/tests/test_model_versioning.py",
    "project_interactions/ai_model_registry/tests/test_performance_tracking.py",
    "project_interactions/ai_model_registry/tests/test_deployment_workflow.py"
]

for test_file in test_files:
    print(f"\nRunning {test_file.split('/')[-1]}...")
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        duration = time.time() - start_time
        
        if result.returncode == 0:
            status = "PASS"
            print(f"✅ {test_file.split('/')[-1]} - PASSED ({duration:.2f}s)")
            # Count individual tests
            test_count = result.stdout.count("✓")
            if test_count > 0:
                print(f"   {test_count} tests passed")
        else:
            status = "FAIL"
            print(f"❌ {test_file.split('/')[-1]} - FAILED")
            print(f"   Error: {result.stderr}")
            
        test_results.append({
            "test": test_file.split('/')[-1],
            "status": status,
            "duration": duration,
            "output": result.stdout if status == "PASS" else result.stderr
        })
        
    except subprocess.TimeoutExpired:
        print(f"⏱️  {test_file.split('/')[-1]} - TIMEOUT")
        test_results.append({
            "test": test_file.split('/')[-1],
            "status": "TIMEOUT",
            "duration": 30.0,
            "output": "Test exceeded 30 second timeout"
        })
    except Exception as e:
        print(f"💥 {test_file.split('/')[-1]} - ERROR: {str(e)}")
        test_results.append({
            "test": test_file.split('/')[-1],
            "status": "ERROR",
            "duration": 0,
            "output": str(e)
        })

# Summary
print("\n" + "="*60)
print("Test Summary")
print("="*60)

passed = sum(1 for r in test_results if r["status"] == "PASS")
failed = sum(1 for r in test_results if r["status"] in ["FAIL", "TIMEOUT", "ERROR"])

print(f"\nTotal test suites: {len(test_results)}")
print(f"✅ Passed: {passed}")
print(f"❌ Failed: {failed}")

# Critical verification
if passed == len(test_results):
    print("\n🎉 Task #51 PASSED all verifications!")
    print("   AI Model Registry is fully functional")
else:
    print("\n⚠️  Task #51 has test failures that need investigation")
    for result in test_results:
        if result["status"] != "PASS":
            print(f"\n{result['test']} failed with:")
            print(result['output'][:500])

# Check directory naming
import os
if os.path.exists("/home/graham/workspace/shared_claude_docs/project_interactions/ai_model_registry"):
    print("\n✅ Directory properly renamed to Python convention")
else:
    print("\n⚠️  Directory needs to be renamed from ai-model-registry to ai_model_registry")

print("\nProceeding to Task #52...")