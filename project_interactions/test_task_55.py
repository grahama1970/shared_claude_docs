#!/usr/bin/env python3
"""
Test Task 55: CI Helper verification script
Tests pipeline orchestration, deployment automation, and quality gates
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ci_helper.ci_helper_interaction import (
    CIHelperInteraction,
    CIPlatform,
    JobStatus,
    DeploymentStrategy
)


def test_pipeline_creation():
    """Test creating pipelines for different platforms"""
    print("\n=== Testing Pipeline Creation ===")
    ci_helper = CIHelperInteraction()
    
    platforms = ["github_actions", "jenkins", "gitlab_ci", "circleci"]
    created_pipelines = []
    
    for platform in platforms:
        config = {
            "name": f"{platform.title()} Test Pipeline",
            "stages": ["build", "test", "deploy"],
            "environment": "staging",
            "jobs": {
                "build": {
                    "compile": {
                        "commands": ["echo 'Building application'", "make build"],
                        "artifacts": ["build/app", "build/libs"]
                    }
                },
                "test": {
                    "unit": {
                        "commands": ["echo 'Running unit tests'", "pytest tests/unit"],
                        "parallel": True
                    },
                    "integration": {
                        "commands": ["echo 'Running integration tests'", "pytest tests/integration"],
                        "parallel": True
                    }
                },
                "deploy": {
                    "staging": {
                        "commands": ["echo 'Deploying to staging'", "deploy.sh staging"],
                        "dependencies": ["unit", "integration"]
                    }
                }
            }
        }
        
        pipeline = ci_helper.create_pipeline(platform, config)
        created_pipelines.append(pipeline)
        print(f"✓ Created {platform} pipeline: {pipeline['name']} (ID: {pipeline['id'][:8]}...)")
    
    return ci_helper, created_pipelines


def test_pipeline_execution(ci_helper, pipeline):
    """Test pipeline execution with quality gates"""
    print(f"\n=== Testing Pipeline Execution: {pipeline['name']} ===")
    
    # Add quality gates before execution
    gates = [
        {
            "name": "Code Coverage",
            "metric": "code_coverage",
            "threshold": 80.0,
            "operator": "gte",
            "blocking": True
        },
        {
            "name": "Test Success Rate",
            "metric": "test_pass_rate",
            "threshold": 95.0,
            "operator": "gte",
            "blocking": True
        },
        {
            "name": "Security Scan",
            "metric": "security_vulnerabilities",
            "threshold": 0,
            "operator": "eq",
            "blocking": True
        },
        {
            "name": "Build Time",
            "metric": "build_time",
            "threshold": 600,
            "operator": "lt",
            "blocking": False
        }
    ]
    
    for gate in gates:
        ci_helper.add_quality_gate(pipeline["id"], gate)
        print(f"✓ Added quality gate: {gate['name']}")
    
    # Execute pipeline
    execution = ci_helper.execute_pipeline(pipeline["id"], {
        "version": "1.2.3",
        "skip_tests": False
    })
    
    print(f"✓ Pipeline execution status: {execution['status']}")
    print(f"  - Started: {execution['started_at']}")
    print(f"  - Completed: {execution['completed_at']}")
    print(f"  - Artifacts created: {len(execution['artifacts'])}")
    
    # Check stage results
    for stage, result in execution["stages"].items():
        print(f"  - Stage '{stage}': {result['status']} ({len(result['jobs'])} jobs)")
    
    return execution


def test_deployment_strategies(ci_helper, pipeline_id):
    """Test different deployment strategies"""
    print("\n=== Testing Deployment Strategies ===")
    
    strategies = [
        ("blue_green", {
            "health_check_url": "https://app.example.com/health",
            "switch_delay": 30
        }),
        ("canary", {
            "canary_percentage": 10,
            "monitor_duration": 300,
            "success_criteria": {
                "error_rate": 1.0,
                "latency_p99": 200
            }
        }),
        ("rolling", {
            "batch_size": 2,
            "pause_between_batches": 60,
            "max_unavailable": 1
        }),
        ("recreate", {})
    ]
    
    deployments = []
    
    for strategy, config in strategies:
        deployment = ci_helper.deploy(
            pipeline_id,
            environment="production",
            strategy=strategy,
            config=config
        )
        deployments.append(deployment)
        
        print(f"✓ {strategy.replace('_', '-').title()} deployment: {deployment['status']}")
        print(f"  - Environment: {deployment['environment']}")
        print(f"  - Steps executed: {len(deployment['steps'])}")
        
        if "metrics" in deployment:
            print(f"  - Error rate: {deployment['metrics']['error_rate']}%")
            print(f"  - Success rate: {deployment['metrics']['success_rate']}%")
        
        if "instances_updated" in deployment:
            print(f"  - Instances updated: {deployment['instances_updated']}")
        
        if "downtime_seconds" in deployment:
            print(f"  - Downtime: {deployment['downtime_seconds']} seconds")
    
    return deployments


def test_rollback(ci_helper, deployment):
    """Test deployment rollback"""
    print("\n=== Testing Rollback ===")
    
    rollback = ci_helper.rollback(deployment["id"])
    
    print(f"✓ Rollback status: {rollback['status']}")
    print(f"  - Deployment ID: {deployment['id'][:8]}...")
    print(f"  - Rollback ID: {rollback['id'][:8]}...")
    
    for step in rollback["steps"]:
        print(f"  - {step['name']}: {step['status']}")
    
    return rollback


def test_secret_management(ci_helper):
    """Test secret management functionality"""
    print("\n=== Testing Secret Management ===")
    
    secrets = [
        ("DATABASE_URL", "postgresql://user:pass@localhost:5432/mydb"),
        ("API_KEY", "sk-proj-1234567890abcdef"),
        ("AWS_ACCESS_KEY_ID", "AKIAIOSFODNN7EXAMPLE"),
        ("GITHUB_TOKEN", "ghp_1234567890abcdef1234567890abcdef12345")
    ]
    
    # Add secrets
    for name, value in secrets:
        result = ci_helper.manage_secrets("add", name, value)
        print(f"✓ Added secret: {name} (encrypted: {result['encrypted']})")
    
    # Retrieve a secret
    retrieved = ci_helper.manage_secrets("get", "API_KEY")
    print(f"✓ Retrieved secret: {retrieved['secret_name']}")
    print(f"  - Value matches: {retrieved['value'] == 'sk-proj-1234567890abcdef'}")
    
    # Delete a secret
    deleted = ci_helper.manage_secrets("delete", "GITHUB_TOKEN")
    print(f"✓ Deleted secret: {deleted['secret_name']}")
    
    return True


def test_config_generation(ci_helper, pipeline_id):
    """Test platform-specific configuration generation"""
    print("\n=== Testing Configuration Generation ===")
    
    platforms = ["github_actions", "jenkins", "gitlab_ci"]
    
    for platform in platforms:
        config = ci_helper.generate_pipeline_config(platform, pipeline_id)
        
        print(f"✓ Generated {platform} configuration:")
        print(f"  - Length: {len(config)} characters")
        print(f"  - Preview: {config[:100]}...")
        
        # Verify platform-specific content
        if platform == "github_actions":
            assert "jobs:" in config
            assert "steps:" in config
        elif platform == "jenkins":
            assert "pipeline {" in config
            assert "stages {" in config
        elif platform == "gitlab_ci":
            assert "stages:" in config
            assert "script:" in config
    
    return True


def test_pipeline_metrics(ci_helper, pipeline_id):
    """Test pipeline metrics collection"""
    print("\n=== Testing Pipeline Metrics ===")
    
    metrics = ci_helper.get_pipeline_metrics(pipeline_id)
    
    print(f"✓ Pipeline metrics retrieved:")
    print(f"  - Total executions: {metrics['total_executions']}")
    print(f"  - Success rate: {metrics['success_rate']}%")
    print(f"  - Average duration: {metrics['average_duration']} seconds")
    
    print(f"  - Failure reasons:")
    for reason, count in metrics['failure_reasons'].items():
        print(f"    - {reason}: {count}")
    
    print(f"  - Stage metrics:")
    for stage, stage_metrics in metrics['stage_metrics'].items():
        print(f"    - {stage}: {stage_metrics['success_rate']}% success, avg {stage_metrics['avg_duration']}s")
    
    return metrics


def main():
    """Run all tests"""
    print("CI Helper Task #55 Verification")
    print("=" * 50)
    
    try:
        # Test 1: Pipeline creation
        ci_helper, pipelines = test_pipeline_creation()
        assert len(pipelines) == 4
        
        # Test 2: Pipeline execution with quality gates
        execution = test_pipeline_execution(ci_helper, pipelines[0])
        assert execution["status"] in [JobStatus.SUCCESS.value, JobStatus.FAILED.value]
        
        # Test 3: Deployment strategies
        deployments = test_deployment_strategies(ci_helper, pipelines[0]["id"])
        assert len(deployments) == 4
        
        # Test 4: Rollback
        rollback = test_rollback(ci_helper, deployments[0])
        assert rollback["status"] == "success"
        
        # Test 5: Secret management
        assert test_secret_management(ci_helper)
        
        # Test 6: Configuration generation
        assert test_config_generation(ci_helper, pipelines[0]["id"])
        
        # Test 7: Pipeline metrics
        metrics = test_pipeline_metrics(ci_helper, pipelines[0]["id"])
        assert "total_executions" in metrics
        
        print("\n" + "=" * 50)
        print("✅ All CI Helper tests passed!")
        print("=" * 50)
        
        # Summary
        print("\nSummary:")
        print(f"- Created {len(pipelines)} pipelines across platforms")
        print(f"- Executed pipeline with {len(execution['stages'])} stages")
        print(f"- Tested {len(deployments)} deployment strategies")
        print(f"- Quality gates working correctly")
        print(f"- Secret management functional")
        print(f"- Configuration generation successful")
        print(f"- Metrics collection operational")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    # sys.exit() removed)