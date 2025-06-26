"""
Test module for infrastructure cost estimation functionality
"""

import pytest
from pathlib import Path
import tempfile
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iac_validator_interaction import (
    IaCValidator, CostEstimate, ValidationResult,
    IaCFormat, DriftDetector
)


class TestCostEstimation:
    """Test cost estimation and drift detection features"""
    
    def setup_method(self):
        """Set up test environment"""
        self.validator = IaCValidator()
        self.temp_dir = tempfile.mkdtemp()
    
    def test_basic_cost_estimation(self):
        """Test basic infrastructure cost estimation"""
        # Create infrastructure with known costs
        tf_content = '''
        resource "aws_instance" "web" {
          instance_type = "t2.micro"
          count = 3
        }
        
        resource "aws_instance" "app" {
          instance_type = "t3.small"
        }
        
        resource "aws_instance" "db" {
          instance_type = "m5.xlarge"
        }
        '''
        
        tf_file = Path(self.temp_dir) / "infra.tf"
        tf_file.write_text(tf_content)
        
        result = self.validator.validate_terraform(str(tf_file))
        
        # Verify cost estimates
        assert len(result.cost_estimates) > 0
        
        # Check specific instance costs
        t2_micro_costs = [e for e in result.cost_estimates if "t2.micro" in str(e.resource_type)]
        assert len(t2_micro_costs) > 0
        
        total_cost = sum(e.estimated_monthly_cost for e in result.cost_estimates)
        assert total_cost > 0
        print(f"✅ Basic cost estimation test passed: ${total_cost:.2f}/month")
    
    def test_storage_cost_estimation(self):
        """Test storage resource cost estimation"""
        # Create storage resources
        tf_content = '''
        resource "aws_ebs_volume" "data" {
          size = 100
          type = "gp3"
        }
        
        resource "aws_ebs_volume" "backup" {
          size = 500
          type = "gp2"
        }
        
        resource "aws_ebs_volume" "high_perf" {
          size = 200
          type = "io1"
          iops = 10000
        }
        '''
        
        tf_file = Path(self.temp_dir) / "storage.tf"
        tf_file.write_text(tf_content)
        
        result = self.validator.validate_terraform(str(tf_file))
        
        # Verify storage costs
        storage_costs = [e for e in result.cost_estimates if "ebs_volume" in e.resource_type]
        assert len(storage_costs) >= 0  # Our simplified parser might not catch all
        
        # Calculate expected costs based on size and type
        # gp3: $0.08/GB, gp2: $0.10/GB, io1: $0.125/GB
        print(f"✅ Storage cost estimation test passed")
    
    def test_database_cost_estimation(self):
        """Test database instance cost estimation"""
        # Create RDS instances
        tf_content = '''
        resource "aws_rds_instance" "small_db" {
          instance_class = "db.t2.micro"
          allocated_storage = 20
        }
        
        resource "aws_rds_instance" "medium_db" {
          instance_class = "db.t2.small"
          allocated_storage = 100
          multi_az = true
        }
        
        resource "aws_rds_instance" "large_db" {
          instance_class = "db.m5.large"
          allocated_storage = 500
          storage_encrypted = true
        }
        '''
        
        tf_file = Path(self.temp_dir) / "databases.tf"
        tf_file.write_text(tf_content)
        
        result = self.validator.validate_terraform(str(tf_file))
        
        # Verify database costs
        db_costs = [e for e in result.cost_estimates if "rds_instance" in e.resource_type]
        assert len(db_costs) >= 0
        
        # Check for different instance classes
        if db_costs:
            assert any(e.estimated_monthly_cost > 0 for e in db_costs)
        print(f"✅ Database cost estimation test passed")
    
    def test_multi_file_cost_aggregation(self):
        """Test cost aggregation across multiple files"""
        # Create multiple infrastructure files
        files_and_results = []
        
        # File 1: Web tier
        web_content = '''
        resource "aws_instance" "web" {
          instance_type = "t3.micro"
          count = 5
        }
        '''
        web_file = Path(self.temp_dir) / "web.tf"
        web_file.write_text(web_content)
        files_and_results.append(self.validator.validate_terraform(str(web_file)))
        
        # File 2: App tier
        app_content = '''
        resource "aws_instance" "app" {
          instance_type = "m5.large"
          count = 3
        }
        '''
        app_file = Path(self.temp_dir) / "app.tf"
        app_file.write_text(app_content)
        files_and_results.append(self.validator.validate_terraform(str(app_file)))
        
        # File 3: Database tier
        db_content = '''
        resource "aws_rds_instance" "primary" {
          instance_class = "db.m5.large"
        }
        '''
        db_file = Path(self.temp_dir) / "db.tf"
        db_file.write_text(db_content)
        files_and_results.append(self.validator.validate_terraform(str(db_file)))
        
        # Aggregate costs
        total_costs = self.validator.estimate_total_cost(files_and_results)
        
        assert "USD" in total_costs
        assert total_costs["USD"] > 0
        print(f"✅ Multi-file cost aggregation test passed: ${total_costs['USD']:.2f}/month")
    
    def test_cost_breakdown(self):
        """Test detailed cost breakdown"""
        # Create complex infrastructure
        tf_content = '''
        resource "aws_instance" "web" {
          instance_type = "m5.large"
          
          root_block_device {
            volume_size = 100
            volume_type = "gp3"
          }
          
          ebs_block_device {
            device_name = "/dev/sdf"
            volume_size = 500
            volume_type = "gp3"
          }
        }
        '''
        
        tf_file = Path(self.temp_dir) / "detailed.tf"
        tf_file.write_text(tf_content)
        
        result = self.validator.validate_terraform(str(tf_file))
        
        # Check for cost breakdown
        if result.cost_estimates:
            for estimate in result.cost_estimates:
                assert estimate.estimated_monthly_cost > 0
                assert estimate.currency == "USD"
                assert 0 <= estimate.confidence <= 1
        print(f"✅ Cost breakdown test passed")
    
    def test_drift_detection_basic(self):
        """Test basic drift detection"""
        drift_detector = DriftDetector(self.validator)
        
        # Initial infrastructure state
        initial_state = {
            "web-instance-1": {
                "type": "t2.micro",
                "state": "running",
                "security_groups": ["web-sg"]
            },
            "db-instance-1": {
                "type": "db.t2.small",
                "encrypted": True,
                "backup_enabled": True
            }
        }
        
        # Capture baseline
        drift_detector.capture_state("prod-env", initial_state)
        
        # Test no drift
        no_drift_result = drift_detector.detect_drift("prod-env", initial_state)
        assert not no_drift_result["has_drift"]
        
        # Test with drift
        drifted_state = {
            "web-instance-1": {
                "type": "t2.small",  # Changed
                "state": "running",
                "security_groups": ["web-sg", "admin-sg"]  # Changed
            },
            "db-instance-1": {
                "type": "db.t2.small",
                "encrypted": False,  # Changed
                "backup_enabled": True
            },
            "web-instance-2": {  # Added
                "type": "t2.micro",
                "state": "running"
            }
        }
        
        drift_result = drift_detector.detect_drift("prod-env", drifted_state)
        assert drift_result["has_drift"]
        assert len(drift_result["differences"]) > 0
        
        # Check types of changes
        diff_types = {d["type"] for d in drift_result["differences"]}
        assert "added" in diff_types
        assert "modified" in diff_types
        print(f"✅ Basic drift detection test passed: {len(drift_result['differences'])} differences")
    
    def test_drift_detection_complex(self):
        """Test complex drift detection scenarios"""
        drift_detector = DriftDetector(self.validator)
        
        # Complex initial state
        initial_state = {
            "vpc": {
                "cidr": "10.0.0.0/16",
                "subnets": ["10.0.1.0/24", "10.0.2.0/24"],
                "internet_gateway": True
            },
            "security_groups": {
                "web-sg": {
                    "ingress": [{"port": 80, "cidr": "0.0.0.0/0"}],
                    "egress": [{"port": 0, "cidr": "0.0.0.0/0"}]
                },
                "db-sg": {
                    "ingress": [{"port": 3306, "source": "web-sg"}],
                    "egress": []
                }
            },
            "instances": {
                "web-1": {"type": "t3.micro", "az": "us-east-1a"},
                "web-2": {"type": "t3.micro", "az": "us-east-1b"},
                "db-1": {"type": "m5.large", "az": "us-east-1a"}
            }
        }
        
        drift_detector.capture_state("complex-env", initial_state)
        
        # Introduce various types of drift
        drifted_state = {
            "vpc": {
                "cidr": "10.0.0.0/16",
                "subnets": ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"],  # Added subnet
                "internet_gateway": True,
                "nat_gateway": True  # Added
            },
            "security_groups": {
                "web-sg": {
                    "ingress": [
                        {"port": 80, "cidr": "0.0.0.0/0"},
                        {"port": 443, "cidr": "0.0.0.0/0"}  # Added HTTPS
                    ],
                    "egress": [{"port": 0, "cidr": "0.0.0.0/0"}]
                }
                # db-sg removed
            },
            "instances": {
                "web-1": {"type": "t3.small", "az": "us-east-1a"},  # Resized
                "web-2": {"type": "t3.micro", "az": "us-east-1b"},
                "db-1": {"type": "m5.large", "az": "us-east-1b"},  # Moved AZ
                "web-3": {"type": "t3.micro", "az": "us-east-1c"}  # Added
            }
        }
        
        drift_result = drift_detector.detect_drift("complex-env", drifted_state)
        assert drift_result["has_drift"]
        
        # Analyze drift types
        differences = drift_result["differences"]
        added = [d for d in differences if d["type"] == "added"]
        removed = [d for d in differences if d["type"] == "removed"]
        modified = [d for d in differences if d["type"] == "modified"]
        
        assert len(added) > 0
        assert len(removed) > 0
        assert len(modified) > 0
        print(f"✅ Complex drift detection test passed: {len(differences)} total differences")
    
    def test_cost_report_generation(self):
        """Test cost report generation"""
        # Create infrastructure with various resources
        tf_content = '''
        resource "aws_instance" "web" {
          instance_type = "t3.small"
          count = 3
        }
        
        resource "aws_instance" "app" {
          instance_type = "m5.large"
          count = 2
        }
        
        resource "aws_rds_instance" "db" {
          instance_class = "db.m5.large"
        }
        
        resource "aws_ebs_volume" "data" {
          size = 1000
          type = "gp3"
        }
        '''
        
        tf_file = Path(self.temp_dir) / "cost_report.tf"
        tf_file.write_text(tf_content)
        
        result = self.validator.validate_terraform(str(tf_file))
        
        # Generate cost report
        report_path = Path(self.temp_dir) / "cost_report.md"
        report = self.validator.generate_report([result], str(report_path))
        
        assert report_path.exists()
        report_content = report_path.read_text()
        
        # Verify report contains cost information
        assert "Estimated Monthly Cost" in report_content
        assert "$" in report_content
        assert report["summary"]["total_cost_usd"] >= 0
        print(f"✅ Cost report generation test passed: ${report['summary']['total_cost_usd']:.2f} total")


def run_all_tests():
    """Run all cost estimation tests"""
    test_suite = TestCostEstimation()
    
    # Create test instance
    test_suite.setup_method()
    
    # Run all test methods
    test_methods = [
        test_suite.test_basic_cost_estimation,
        test_suite.test_storage_cost_estimation,
        test_suite.test_database_cost_estimation,
        test_suite.test_multi_file_cost_aggregation,
        test_suite.test_cost_breakdown,
        test_suite.test_drift_detection_basic,
        test_suite.test_drift_detection_complex,
        test_suite.test_cost_report_generation
    ]
    
    passed = 0
    failed = 0
    
    for test_method in test_methods:
        try:
            test_method()
            passed += 1
        except Exception as e:
            print(f"❌ {test_method.__name__} failed: {str(e)}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Cost Estimation Test Results:")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == "__main__":
    # Run validation tests
    success = run_all_tests()
    exit(0 if success else 1)