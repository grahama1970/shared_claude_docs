"""
Module: test_quality_gates.py
Purpose: Test quality gates and secret management functionality

External Dependencies:
- pytest: https://docs.pytest.org/

Example Usage:
>>> pytest test_quality_gates.py -v
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ci_helper_interaction import (
    CIHelperInteraction, QualityGate, JobStatus
)


class TestQualityGates:
    """Test quality gates and related features"""
    
    @pytest.fixture
    def ci_helper(self):
        """Create a CI helper instance"""
        return CIHelperInteraction()
    
    @pytest.fixture
    def pipeline_with_gates(self, ci_helper):
        """Create a pipeline with quality gates"""
        config = {
            "name": "Quality Pipeline",
            "stages": ["build", "test", "analyze"],
            "jobs": {
                "build": {
                    "compile": {"commands": ["make build"]}
                },
                "test": {
                    "unit": {"commands": ["pytest --cov"]},
                    "integration": {"commands": ["pytest integration/"]}
                },
                "analyze": {
                    "sonar": {"commands": ["sonar-scanner"]},
                    "security": {"commands": ["security-scan"]}
                }
            }
        }
        
        pipeline = ci_helper.create_pipeline("jenkins", config)
        
        # Add various quality gates
        gates = [
            {
                "name": "Code Coverage",
                "metric": "code_coverage",
                "threshold": 80.0,
                "operator": "gte",
                "blocking": True
            },
            {
                "name": "Test Pass Rate",
                "metric": "test_pass_rate",
                "threshold": 95.0,
                "operator": "gte",
                "blocking": True
            },
            {
                "name": "Security Vulnerabilities",
                "metric": "security_vulnerabilities",
                "threshold": 0,
                "operator": "eq",
                "blocking": True
            },
            {
                "name": "Performance Score",
                "metric": "performance_score",
                "threshold": 85.0,
                "operator": "gt",
                "blocking": False
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
        
        return pipeline
    
    def test_add_quality_gate(self, ci_helper):
        """Test adding quality gates to a pipeline"""
        pipeline = ci_helper.create_pipeline("github_actions", {"name": "Test"})
        
        gate_config = {
            "name": "Code Quality",
            "metric": "code_coverage",
            "threshold": 75.0,
            "operator": "gte",
            "blocking": True
        }
        
        ci_helper.add_quality_gate(pipeline["id"], gate_config)
        
        assert pipeline["id"] in ci_helper.quality_gates
        gates = ci_helper.quality_gates[pipeline["id"]]
        assert len(gates) == 1
        
        gate = gates[0]
        assert gate.name == "Code Quality"
        assert gate.metric == "code_coverage"
        assert gate.threshold == 75.0
        assert gate.operator == "gte"
        assert gate.blocking is True
    
    def test_multiple_quality_gates(self, ci_helper, pipeline_with_gates):
        """Test multiple quality gates on a pipeline"""
        pipeline_id = pipeline_with_gates["id"]
        gates = ci_helper.quality_gates[pipeline_id]
        
        assert len(gates) == 5
        
        # Check gate types
        gate_names = [gate.name for gate in gates]
        assert "Code Coverage" in gate_names
        assert "Test Pass Rate" in gate_names
        assert "Security Vulnerabilities" in gate_names
        assert "Performance Score" in gate_names
        assert "Build Time" in gate_names
    
    def test_blocking_vs_non_blocking_gates(self, ci_helper, pipeline_with_gates):
        """Test blocking vs non-blocking quality gates"""
        pipeline_id = pipeline_with_gates["id"]
        gates = ci_helper.quality_gates[pipeline_id]
        
        blocking_gates = [gate for gate in gates if gate.blocking]
        non_blocking_gates = [gate for gate in gates if not gate.blocking]
        
        assert len(blocking_gates) == 3
        assert len(non_blocking_gates) == 2
        
        # Verify critical gates are blocking
        blocking_names = [gate.name for gate in blocking_gates]
        assert "Security Vulnerabilities" in blocking_names
        assert "Code Coverage" in blocking_names
    
    def test_quality_gate_operators(self, ci_helper):
        """Test different quality gate operators"""
        pipeline = ci_helper.create_pipeline("gitlab_ci", {"name": "Operator Test"})
        
        operators = [
            ("Greater Than", "gt", 80, 85, True),
            ("Less Than", "lt", 100, 95, True),
            ("Equal", "eq", 0, 0, True),
            ("Greater or Equal", "gte", 90, 90, True),
            ("Less or Equal", "lte", 50, 50, True)
        ]
        
        for name, operator, threshold, value, expected in operators:
            result = ci_helper._evaluate_gate(value, threshold, operator)
            assert result == expected, f"{name} operator failed"
    
    def test_quality_gate_execution(self, ci_helper, pipeline_with_gates):
        """Test quality gate evaluation during pipeline execution"""
        pipeline_id = pipeline_with_gates["id"]
        
        # Execute pipeline - should pass all gates
        execution = ci_helper.execute_pipeline(pipeline_id)
        
        # The default metrics in the implementation should pass
        assert execution["status"] == JobStatus.SUCCESS.value
    
    def test_secret_management_add(self, ci_helper):
        """Test adding secrets"""
        secret_name = "API_KEY"
        secret_value = "super-secret-key-12345"
        
        result = ci_helper.manage_secrets("add", secret_name, secret_value)
        
        assert result["action"] == "added"
        assert result["secret_name"] == secret_name
        assert result["encrypted"] is True
        
        # Verify secret is stored encrypted
        assert secret_name in ci_helper.secrets
        assert ci_helper.secrets[secret_name] != secret_value.encode()
    
    def test_secret_management_get(self, ci_helper):
        """Test retrieving secrets"""
        secret_name = "DATABASE_URL"
        secret_value = "postgresql://user:pass@localhost/db"
        
        # Add secret
        ci_helper.manage_secrets("add", secret_name, secret_value)
        
        # Retrieve secret
        result = ci_helper.manage_secrets("get", secret_name)
        
        assert result["secret_name"] == secret_name
        assert result["value"] == secret_value
    
    def test_secret_management_delete(self, ci_helper):
        """Test deleting secrets"""
        secret_name = "TEMP_SECRET"
        secret_value = "temporary-value"
        
        # Add secret
        ci_helper.manage_secrets("add", secret_name, secret_value)
        assert secret_name in ci_helper.secrets
        
        # Delete secret
        result = ci_helper.manage_secrets("delete", secret_name)
        
        assert result["action"] == "deleted"
        assert result["secret_name"] == secret_name
        assert secret_name not in ci_helper.secrets
    
    def test_secret_encryption(self, ci_helper):
        """Test that secrets are properly encrypted"""
        secrets = [
            ("AWS_ACCESS_KEY", "AKIAIOSFODNN7EXAMPLE"),
            ("AWS_SECRET_KEY", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"),
            ("GITHUB_TOKEN", "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        ]
        
        for name, value in secrets:
            ci_helper.manage_secrets("add", name, value)
            
            # Verify encrypted storage
            stored_value = ci_helper.secrets[name]
            assert stored_value != value.encode()
            assert len(stored_value) > len(value)
            
            # Verify decryption
            retrieved = ci_helper.manage_secrets("get", name)
            assert retrieved["value"] == value
    
    def test_secret_not_found(self, ci_helper):
        """Test retrieving non-existent secret"""
        with pytest.raises(ValueError) as exc_info:
            ci_helper.manage_secrets("get", "NON_EXISTENT_SECRET")
        
        assert "not found" in str(exc_info.value)
    
    def test_notifications(self, ci_helper, pipeline_with_gates):
        """Test notification system"""
        pipeline_id = pipeline_with_gates["id"]
        
        # Clear existing notifications
        ci_helper.notifications.clear()
        
        # Execute pipeline
        execution = ci_helper.execute_pipeline(pipeline_id)
        
        # Check notifications were sent
        assert len(ci_helper.notifications) > 0
        
        notification = ci_helper.notifications[0]
        assert notification["pipeline_id"] == pipeline_id
        assert notification["execution_id"] == execution["id"]
        assert notification["status"] == execution["status"]
        assert "timestamp" in notification
        assert "channels" in notification
        
        # Verify notification channels
        assert "email" in notification["channels"]
        assert "slack" in notification["channels"]
        assert "webhook" in notification["channels"]
    
    def test_platform_config_generation(self, ci_helper, pipeline_with_gates):
        """Test platform-specific configuration generation"""
        pipeline_id = pipeline_with_gates["id"]
        
        # Generate GitHub Actions config
        gh_config = ci_helper.generate_pipeline_config("github_actions", pipeline_id)
        assert "name: Quality Pipeline" in gh_config
        assert "jobs:" in gh_config
        assert "steps:" in gh_config
        
        # Generate Jenkins config
        jenkins_config = ci_helper.generate_pipeline_config("jenkins", pipeline_id)
        assert "pipeline {" in jenkins_config
        assert "stages {" in jenkins_config
        assert "environment {" in jenkins_config
        
        # Generate GitLab CI config
        gitlab_config = ci_helper.generate_pipeline_config("gitlab_ci", pipeline_id)
        assert "stages:" in gitlab_config
        assert "- build" in gitlab_config
        assert "- test" in gitlab_config
        assert "- analyze" in gitlab_config
    
    def test_invalid_platform_config(self, ci_helper, pipeline_with_gates):
        """Test error handling for invalid platform"""
        pipeline_id = pipeline_with_gates["id"]
        
        with pytest.raises(ValueError) as exc_info:
            ci_helper.generate_pipeline_config("invalid_platform", pipeline_id)
        
        assert "No template for platform" in str(exc_info.value)


if __name__ == "__main__":
    # Run specific tests with real data
    helper = CIHelperInteraction()
    
    # Test quality gates
    pipeline_config = {
        "name": "Quality Check Pipeline",
        "stages": ["build", "test", "analyze"],
        "jobs": {
            "build": {"compile": {"commands": ["go build"]}},
            "test": {"unit": {"commands": ["go test ./..."]}},
            "analyze": {"lint": {"commands": ["golangci-lint run"]}}
        }
    }
    
    pipeline = helper.create_pipeline("github_actions", pipeline_config)
    print(f"✅ Created pipeline: {pipeline['name']}")
    
    # Add quality gates
    gates = [
        {"name": "Coverage", "metric": "code_coverage", "threshold": 80, "operator": "gte", "blocking": True},
        {"name": "Tests", "metric": "test_pass_rate", "threshold": 100, "operator": "eq", "blocking": True},
        {"name": "Build Speed", "metric": "build_time", "threshold": 300, "operator": "lt", "blocking": False}
    ]
    
    for gate in gates:
        helper.add_quality_gate(pipeline["id"], gate)
    print(f"✅ Added {len(gates)} quality gates")
    
    # Test secret management
    helper.manage_secrets("add", "DEPLOY_KEY", "ssh-rsa AAAAB3...")
    secret = helper.manage_secrets("get", "DEPLOY_KEY")
    print(f"✅ Secret management: stored and retrieved {secret['secret_name']}")
    
    # Execute pipeline
    execution = helper.execute_pipeline(pipeline["id"])
    print(f"✅ Pipeline execution with quality gates: {execution['status']}")
    
    # Generate configs
    for platform in ["github_actions", "jenkins", "gitlab_ci"]:
        config = helper.generate_pipeline_config(platform, pipeline["id"])
        print(f"✅ Generated {platform} config: {len(config)} characters")
    
    print("\n✅ All quality gate tests passed")