"""
Test module for Terraform validation functionality
"""

import pytest
from pathlib import Path
import tempfile
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iac_validator_interaction import (
    IaCValidator, IaCFormat, ValidationSeverity,
    ValidationIssue, ComplianceFramework
)


class TestTerraformValidation:
    """Test Terraform validation features"""
    
    def setup_method(self):
        """Set up test environment"""
        self.validator = IaCValidator()
        self.temp_dir = tempfile.mkdtemp()
    
    def test_valid_terraform_configuration(self):
        """Test validation of valid Terraform configuration"""
        # Create valid Terraform file
        tf_content = '''
        resource "aws_instance" "web" {
          instance_type = "t2.micro"
          ami           = "ami-12345678"
          
          tags = {
            Name = "WebServer"
          }
        }
        
        resource "aws_s3_bucket" "data" {
          bucket = "my-data-bucket"
          encrypted = true
        }
        '''
        
        tf_file = Path(self.temp_dir) / "main.tf"
        tf_file.write_text(tf_content)
        
        result = self.validator.validate_terraform(str(tf_file))
        
        assert result.format == IaCFormat.TERRAFORM
        assert len([i for i in result.issues if i.severity == ValidationSeverity.CRITICAL]) == 0
        print(f"✅ Valid Terraform configuration test passed")
    
    def test_security_group_validation(self):
        """Test security group validation rules"""
        # Create Terraform with security issues
        tf_content = '''
        resource "aws_security_group" "bad" {
          name = "bad-sg"
          
          ingress {
            from_port   = 22
            to_port     = 22
            protocol    = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
          }
          
          ingress {
            from_port   = 3389
            to_port     = 3389
            protocol    = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
          }
        }
        '''
        
        tf_file = Path(self.temp_dir) / "security.tf"
        tf_file.write_text(tf_content)
        
        result = self.validator.validate_terraform(str(tf_file))
        
        # Should have critical security issues
        critical_issues = [i for i in result.issues if i.severity == ValidationSeverity.CRITICAL]
        assert len(critical_issues) > 0
        assert any("SSH" in i.message for i in critical_issues)
        assert not result.is_valid
        print(f"✅ Security group validation test passed: {len(critical_issues)} issues found")
    
    def test_encryption_validation(self):
        """Test encryption at rest validation"""
        # Create resources without encryption
        tf_content = '''
        resource "aws_s3_bucket" "unencrypted" {
          bucket = "my-bucket"
          encrypted = false
        }
        
        resource "aws_rds_instance" "database" {
          instance_class = "db.t2.micro"
          encrypted = false
        }
        
        resource "aws_ebs_volume" "data" {
          size = 100
          encrypted = false
        }
        '''
        
        tf_file = Path(self.temp_dir) / "unencrypted.tf"
        tf_file.write_text(tf_content)
        
        result = self.validator.validate_terraform(str(tf_file))
        
        # Should have encryption issues
        encryption_issues = [i for i in result.issues if "encrypt" in i.message.lower()]
        assert len(encryption_issues) >= 3
        assert all(i.severity == ValidationSeverity.ERROR for i in encryption_issues)
        print(f"✅ Encryption validation test passed: {len(encryption_issues)} issues found")
    
    def test_cost_estimation(self):
        """Test infrastructure cost estimation"""
        # Create resources with known costs
        tf_content = '''
        resource "aws_instance" "web" {
          instance_type = "t2.micro"
        }
        
        resource "aws_instance" "app" {
          instance_type = "m5.large"
        }
        
        resource "aws_rds_instance" "db" {
          instance_class = "db.t2.small"
        }
        '''
        
        tf_file = Path(self.temp_dir) / "resources.tf"
        tf_file.write_text(tf_content)
        
        result = self.validator.validate_terraform(str(tf_file))
        
        # Should have cost estimates
        assert len(result.cost_estimates) > 0
        total_cost = sum(e.estimated_monthly_cost for e in result.cost_estimates)
        assert total_cost > 0
        print(f"✅ Cost estimation test passed: ${total_cost:.2f} monthly")
    
    def test_resource_dependencies(self):
        """Test resource dependency extraction"""
        # Create resources with dependencies
        tf_content = '''
        resource "aws_vpc" "main" {
          cidr_block = "10.0.0.0/16"
        }
        
        resource "aws_subnet" "public" {
          vpc_id = "${aws_vpc.main.id}"
          cidr_block = "10.0.1.0/24"
        }
        
        resource "aws_instance" "web" {
          subnet_id = "${aws_subnet.public.id}"
        }
        '''
        
        tf_file = Path(self.temp_dir) / "dependencies.tf"
        tf_file.write_text(tf_content)
        
        result = self.validator.validate_terraform(str(tf_file))
        
        # Should have dependency graph
        assert len(result.resource_graph) > 0
        print(f"✅ Resource dependency test passed: {len(result.resource_graph)} resources")
    
    def test_compliance_checking(self):
        """Test compliance framework checking"""
        # Create non-compliant resources
        tf_content = '''
        resource "aws_security_group" "web" {
          name = "web-sg"
          
          ingress {
            from_port   = 22
            to_port     = 22
            protocol    = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
          }
        }
        
        resource "aws_s3_bucket" "data" {
          bucket = "sensitive-data"
          encrypted = false
        }
        '''
        
        tf_file = Path(self.temp_dir) / "noncompliant.tf"
        tf_file.write_text(tf_content)
        
        result = self.validator.validate_terraform(str(tf_file))
        
        # Should fail compliance checks
        assert ComplianceFramework.CIS in result.compliance_status
        assert not result.compliance_status[ComplianceFramework.CIS]
        assert ComplianceFramework.NIST in result.compliance_status
        assert not result.compliance_status[ComplianceFramework.NIST]
        print(f"✅ Compliance checking test passed")
    
    def test_multiple_resources(self):
        """Test validation with multiple resource types"""
        # Create complex Terraform configuration
        tf_content = '''
        variable "region" {
          default = "us-east-1"
        }
        
        resource "aws_vpc" "main" {
          cidr_block = "10.0.0.0/16"
          enable_dns_hostnames = true
        }
        
        resource "aws_internet_gateway" "main" {
          vpc_id = "${aws_vpc.main.id}"
        }
        
        resource "aws_subnet" "public" {
          vpc_id = "${aws_vpc.main.id}"
          cidr_block = "10.0.1.0/24"
          map_public_ip_on_launch = true
        }
        
        resource "aws_security_group" "web" {
          vpc_id = "${aws_vpc.main.id}"
          
          ingress {
            from_port   = 80
            to_port     = 80
            protocol    = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
          }
          
          egress {
            from_port   = 0
            to_port     = 0
            protocol    = "-1"
            cidr_blocks = ["0.0.0.0/0"]
          }
        }
        
        resource "aws_instance" "web" {
          instance_type = "t3.micro"
          subnet_id = "${aws_subnet.public.id}"
          vpc_security_group_ids = ["${aws_security_group.web.id}"]
        }
        '''
        
        tf_file = Path(self.temp_dir) / "infrastructure.tf"
        tf_file.write_text(tf_content)
        
        result = self.validator.validate_terraform(str(tf_file))
        
        # Should parse all resources
        assert len(result.resource_graph) >= 5
        assert result.format == IaCFormat.TERRAFORM
        print(f"✅ Multiple resources test passed: {len(result.resource_graph)} resources")
    
    def test_invalid_terraform_syntax(self):
        """Test handling of invalid Terraform syntax"""
        # Create invalid Terraform file
        tf_content = '''
        resource "aws_instance" {
          # Missing resource name
          instance_type = "t2.micro"
        }
        
        resource aws_s3_bucket "data" {
          # Missing quotes
          bucket = my-bucket
        }
        '''
        
        tf_file = Path(self.temp_dir) / "invalid.tf"
        tf_file.write_text(tf_content)
        
        result = self.validator.validate_terraform(str(tf_file))
        
        # Should have parsing errors
        parsing_errors = [i for i in result.issues if i.category == "parsing"]
        assert len(parsing_errors) > 0 or len(result.issues) > 0
        print(f"✅ Invalid syntax test passed: {len(result.issues)} issues found")


def run_all_tests():
    """Run all Terraform validation tests"""
    test_suite = TestTerraformValidation()
    
    # Create test instance
    test_suite.setup_method()
    
    # Run all test methods
    test_methods = [
        test_suite.test_valid_terraform_configuration,
        test_suite.test_security_group_validation,
        test_suite.test_encryption_validation,
        test_suite.test_cost_estimation,
        test_suite.test_resource_dependencies,
        test_suite.test_compliance_checking,
        test_suite.test_multiple_resources,
        test_suite.test_invalid_terraform_syntax
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
    print(f"Terraform Validation Test Results:")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == "__main__":
    # Run validation tests
    success = run_all_tests()
    exit(0 if success else 1)