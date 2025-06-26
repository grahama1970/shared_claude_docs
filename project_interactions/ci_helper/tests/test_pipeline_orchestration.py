"""
Module: test_pipeline_orchestration.py
Purpose: Test pipeline orchestration capabilities

External Dependencies:
- pytest: https://docs.pytest.org/

Example Usage:
>>> pytest test_pipeline_orchestration.py -v
"""

import pytest
from datetime import datetime
import uuid
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ci_helper_interaction import (
    CIHelperInteraction, CIPlatform, JobStatus,
    Pipeline, Job, QualityGate
)


class TestPipelineOrchestration:
    """Test pipeline orchestration functionality"""
    
    @pytest.fixture
    def ci_helper(self):
        """Create a CI helper instance"""
        return CIHelperInteraction()
    
    @pytest.fixture
    def sample_pipeline_config(self):
        """Sample pipeline configuration"""
        return {
            "name": "Test Pipeline",
            "stages": ["build", "test", "deploy"],
            "environment": "staging",
            "jobs": {
                "build": {
                    "compile": {
                        "commands": ["make build"],
                        "artifacts": ["bin/*"]
                    }
                },
                "test": {
                    "unit": {
                        "commands": ["make test"],
                        "parallel": True
                    },
                    "integration": {
                        "commands": ["make integration-test"],
                        "parallel": True
                    }
                },
                "deploy": {
                    "staging": {
                        "commands": ["make deploy-staging"],
                        "dependencies": ["unit", "integration"]
                    }
                }
            }
        }
    
    def test_create_pipeline(self, ci_helper, sample_pipeline_config):
        """Test pipeline creation"""
        pipeline = ci_helper.create_pipeline("github_actions", sample_pipeline_config)
        
        assert pipeline["name"] == "Test Pipeline"
        assert pipeline["platform"] == "github_actions"
        assert len(pipeline["stages"]) == 3
        assert len(pipeline["jobs"]) == 4
        assert "created_at" in pipeline
    
    def test_multiple_platforms(self, ci_helper):
        """Test pipeline creation for different platforms"""
        platforms = ["github_actions", "jenkins", "gitlab_ci", "circleci"]
        
        for platform in platforms:
            config = {
                "name": f"{platform} Pipeline",
                "stages": ["build", "test"]
            }
            
            pipeline = ci_helper.create_pipeline(platform, config)
            assert pipeline["platform"] == platform
    
    def test_pipeline_execution(self, ci_helper, sample_pipeline_config):
        """Test pipeline execution"""
        pipeline = ci_helper.create_pipeline("github_actions", sample_pipeline_config)
        execution = ci_helper.execute_pipeline(pipeline["id"])
        
        assert execution["pipeline_id"] == pipeline["id"]
        assert execution["status"] in [JobStatus.SUCCESS.value, JobStatus.FAILED.value]
        assert "stages" in execution
        assert len(execution["stages"]) == 3
        assert "started_at" in execution
        assert "completed_at" in execution
    
    def test_stage_execution_order(self, ci_helper):
        """Test that stages execute in correct order"""
        config = {
            "name": "Order Test Pipeline",
            "stages": ["first", "second", "third"],
            "jobs": {
                "first": {"job1": {"commands": ["echo first"]}},
                "second": {"job2": {"commands": ["echo second"]}},
                "third": {"job3": {"commands": ["echo third"]}}
            }
        }
        
        pipeline = ci_helper.create_pipeline("jenkins", config)
        execution = ci_helper.execute_pipeline(pipeline["id"])
        
        stages = list(execution["stages"].keys())
        assert stages == ["first", "second", "third"]
    
    def test_parallel_job_execution(self, ci_helper):
        """Test parallel job execution within a stage"""
        config = {
            "name": "Parallel Test Pipeline",
            "stages": ["test"],
            "jobs": {
                "test": {
                    "test1": {"commands": ["pytest test1"], "parallel": True},
                    "test2": {"commands": ["pytest test2"], "parallel": True},
                    "test3": {"commands": ["pytest test3"], "parallel": True}
                }
            }
        }
        
        pipeline = ci_helper.create_pipeline("gitlab_ci", config)
        execution = ci_helper.execute_pipeline(pipeline["id"])
        
        test_stage = execution["stages"]["test"]
        assert len(test_stage["jobs"]) == 3
        
        # Check all jobs have timestamps
        for job_result in test_stage["jobs"].values():
            assert "started_at" in job_result
            assert "completed_at" in job_result
    
    def test_job_dependencies(self, ci_helper):
        """Test job dependency handling"""
        config = {
            "name": "Dependency Pipeline",
            "stages": ["build", "deploy"],
            "jobs": {
                "build": {
                    "frontend": {"commands": ["npm build"]},
                    "backend": {"commands": ["go build"]}
                },
                "deploy": {
                    "deploy-app": {
                        "commands": ["deploy.sh"],
                        "dependencies": ["frontend", "backend"]
                    }
                }
            }
        }
        
        pipeline = ci_helper.create_pipeline("circleci", config)
        
        # Verify dependencies are stored
        deploy_jobs = [
            job for job_id, job in ci_helper.jobs.items()
            if job.stage == "deploy"
        ]
        
        assert len(deploy_jobs) == 1
        assert len(deploy_jobs[0].dependencies) == 2
    
    def test_artifact_creation(self, ci_helper):
        """Test artifact creation during job execution"""
        config = {
            "name": "Artifact Pipeline",
            "stages": ["build"],
            "jobs": {
                "build": {
                    "build-app": {
                        "commands": ["make build"],
                        "artifacts": ["dist/app.tar.gz", "dist/app.zip"]
                    }
                }
            }
        }
        
        pipeline = ci_helper.create_pipeline("github_actions", config)
        execution = ci_helper.execute_pipeline(pipeline["id"])
        
        assert len(execution["artifacts"]) == 2
        
        # Verify artifacts were created
        for artifact_id in execution["artifacts"]:
            assert artifact_id in ci_helper.artifacts
            artifact = ci_helper.artifacts[artifact_id]
            assert artifact.size > 0
            assert artifact.checksum
    
    def test_pipeline_parameters(self, ci_helper, sample_pipeline_config):
        """Test pipeline execution with parameters"""
        pipeline = ci_helper.create_pipeline("jenkins", sample_pipeline_config)
        
        parameters = {
            "version": "1.2.3",
            "skip_tests": False,
            "environment": "production"
        }
        
        execution = ci_helper.execute_pipeline(pipeline["id"], parameters)
        
        assert execution["parameters"] == parameters
    
    def test_quality_gates(self, ci_helper, sample_pipeline_config):
        """Test quality gate functionality"""
        pipeline = ci_helper.create_pipeline("gitlab_ci", sample_pipeline_config)
        
        # Add quality gates
        ci_helper.add_quality_gate(pipeline["id"], {
            "name": "Code Coverage",
            "metric": "code_coverage",
            "threshold": 80.0,
            "operator": "gte",
            "blocking": True
        })
        
        ci_helper.add_quality_gate(pipeline["id"], {
            "name": "Build Time",
            "metric": "build_time",
            "threshold": 600,  # 10 minutes
            "operator": "lt",
            "blocking": False
        })
        
        # Execute pipeline
        execution = ci_helper.execute_pipeline(pipeline["id"])
        
        # Quality gates should be checked
        assert pipeline["id"] in ci_helper.quality_gates
        assert len(ci_helper.quality_gates[pipeline["id"]]) == 2
    
    def test_pipeline_metrics(self, ci_helper, sample_pipeline_config):
        """Test pipeline metrics collection"""
        pipeline = ci_helper.create_pipeline("github_actions", sample_pipeline_config)
        
        # Execute pipeline multiple times
        for _ in range(3):
            ci_helper.execute_pipeline(pipeline["id"])
        
        metrics = ci_helper.get_pipeline_metrics(pipeline["id"])
        
        assert metrics["pipeline_id"] == pipeline["id"]
        assert "total_executions" in metrics
        assert "success_rate" in metrics
        assert "average_duration" in metrics
        assert "stage_metrics" in metrics
    
    def test_generate_platform_config(self, ci_helper, sample_pipeline_config):
        """Test platform-specific configuration generation"""
        pipeline = ci_helper.create_pipeline("github_actions", sample_pipeline_config)
        
        # Generate configs for different platforms
        platforms = ["github_actions", "jenkins", "gitlab_ci"]
        
        for platform in platforms:
            config = ci_helper.generate_pipeline_config(platform, pipeline["id"])
            assert isinstance(config, str)
            assert len(config) > 0
            
            # Check for platform-specific syntax
            if platform == "github_actions":
                assert "jobs:" in config
                assert "steps:" in config
            elif platform == "jenkins":
                assert "pipeline {" in config
                assert "stages {" in config
            elif platform == "gitlab_ci":
                assert "stages:" in config
                assert "script:" in config


if __name__ == "__main__":
    # Run specific tests with real data
    helper = CIHelperInteraction()
    
    # Test pipeline creation and execution
    config = {
        "name": "Production Pipeline",
        "stages": ["build", "test", "deploy"],
        "jobs": {
            "build": {
                "app-build": {
                    "commands": ["docker build -t app:latest ."],
                    "artifacts": ["app.tar"]
                }
            },
            "test": {
                "unit-tests": {
                    "commands": ["docker run app:latest pytest"],
                    "parallel": True
                }
            },
            "deploy": {
                "production": {
                    "commands": ["kubectl apply -f k8s/"],
                    "dependencies": ["unit-tests"]
                }
            }
        }
    }
    
    pipeline = helper.create_pipeline("github_actions", config)
    print(f"✅ Test pipeline creation: {pipeline['name']}")
    
    execution = helper.execute_pipeline(pipeline["id"])
    print(f"✅ Test pipeline execution: {execution['status']}")
    
    metrics = helper.get_pipeline_metrics(pipeline["id"])
    print(f"✅ Test metrics collection: {metrics['success_rate']}% success rate")
    
    print("\n✅ All pipeline orchestration tests passed")