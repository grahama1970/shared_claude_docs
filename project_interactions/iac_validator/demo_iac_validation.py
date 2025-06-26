#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Demo script showcasing IaC Validator capabilities
"""

from pathlib import Path
import tempfile
import json
import yaml
from datetime import datetime
from iac_validator_interaction import (
    IaCValidator, DriftDetector, PolicyRule,
    ValidationSeverity, ValidationIssue, ComplianceFramework
)


def create_demo_files(temp_dir: Path) -> dict:
    """Create demo IaC files for validation"""
    files = {}
    
    # Terraform file with issues
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
    
    resource "aws_instance" "web" {
      instance_type = "m5.large"
      ami           = "ami-12345678"
    }
    
    resource "aws_s3_bucket" "logs" {
      bucket = "app-logs"
      encrypted = false
    }
    '''
    tf_file = temp_dir / "infrastructure.tf"
    tf_file.write_text(tf_content)
    files["terraform"] = str(tf_file)
    
    # CloudFormation template
    cf_template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Resources": {
            "WebServer": {
                "Type": "AWS::EC2::Instance",
                "Properties": {
                    "InstanceType": "t3.medium",
                    "SecurityGroups": ["WebSecurityGroup"]
                }
            },
            "WebSecurityGroup": {
                "Type": "AWS::EC2::SecurityGroup",
                "Properties": {
                    "SecurityGroupIngress": [{
                        "IpProtocol": "tcp",
                        "FromPort": 443,
                        "ToPort": 443,
                        "CidrIp": "0.0.0.0/0"
                    }]
                }
            }
        }
    }
    cf_file = temp_dir / "stack.json"
    cf_file.write_text(json.dumps(cf_template, indent=2))
    files["cloudformation"] = str(cf_file)
    
    # Kubernetes manifest
    k8s_content = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: nginx:latest
        ports:
        - containerPort: 80
        securityContext:
          runAsUser: 1000
          runAsNonRoot: true
          readOnlyRootFilesystem: true
"""
    k8s_file = temp_dir / "deployment.yaml"
    k8s_file.write_text(k8s_content)
    files["kubernetes"] = str(k8s_file)
    
    return files


def demo_basic_validation(validator: IaCValidator, files: dict):
    """Demonstrate basic validation"""
    print("\n" + "="*60)
    print("BASIC VALIDATION DEMO")
    print("="*60)
    
    # Validate each file type
    results = []
    
    # Terraform
    print("\n1. Validating Terraform configuration...")
    tf_result = validator.validate_terraform(files["terraform"])
    results.append(tf_result)
    print(f"   - Valid: {tf_result.is_valid}")
    print(f"   - Issues: {len(tf_result.issues)}")
    print(f"   - Critical issues: {len([i for i in tf_result.issues if i.severity == ValidationSeverity.CRITICAL])}")
    
    # CloudFormation
    print("\n2. Validating CloudFormation template...")
    cf_result = validator.validate_cloudformation(files["cloudformation"])
    results.append(cf_result)
    print(f"   - Valid: {cf_result.is_valid}")
    print(f"   - Issues: {len(cf_result.issues)}")
    
    # Kubernetes
    print("\n3. Validating Kubernetes manifest...")
    k8s_result = validator.validate_kubernetes(files["kubernetes"])
    results.append(k8s_result)
    print(f"   - Valid: {k8s_result.is_valid}")
    print(f"   - Security findings: {len(k8s_result.security_findings)}")
    
    return results


def demo_cost_estimation(validator: IaCValidator, results: list):
    """Demonstrate cost estimation"""
    print("\n" + "="*60)
    print("COST ESTIMATION DEMO")
    print("="*60)
    
    total_costs = validator.estimate_total_cost(results)
    
    print("\nEstimated Monthly Costs:")
    for currency, amount in total_costs.items():
        print(f"   - {currency}: ${amount:.2f}")
    
    # Breakdown by resource
    print("\nCost Breakdown:")
    for result in results:
        if result.cost_estimates:
            print(f"\n   {result.format.value}:")
            for estimate in result.cost_estimates:
                print(f"     - {estimate.resource_name}: ${estimate.estimated_monthly_cost:.2f}/month")


def demo_custom_policies(validator: IaCValidator, files: dict):
    """Demonstrate custom policy rules"""
    print("\n" + "="*60)
    print("CUSTOM POLICY RULES DEMO")
    print("="*60)
    
    # Create custom tagging policy
    class TaggingPolicy(PolicyRule):
        def evaluate(self, resource, context):
            if resource.get("type") in ["aws_instance", "aws_s3_bucket"]:
                tags = resource.get("properties", {}).get("tags", {})
                if "Environment" not in tags:
                    return ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        category="governance",
                        message=f"Resource {resource.get('name')} missing Environment tag",
                        file=context.get("file", ""),
                        rule_id=self.rule_id,
                        fix_suggestion="Add Environment tag (e.g., dev, staging, prod)"
                    )
            return None
    
    # Add custom rule
    tagging_rule = TaggingPolicy(
        "GOV001", "Resource Tagging",
        "Ensure all resources have required tags",
        ValidationSeverity.WARNING, "governance"
    )
    validator.add_custom_rule(tagging_rule)
    
    # Re-validate with custom rule
    print("\nRe-validating with custom tagging policy...")
    result = validator.validate_terraform(files["terraform"])
    
    custom_issues = [i for i in result.issues if i.rule_id == "GOV001"]
    print(f"   - Tagging violations: {len(custom_issues)}")
    for issue in custom_issues[:3]:  # Show first 3
        print(f"     • {issue.message}")


def demo_drift_detection(validator: IaCValidator):
    """Demonstrate drift detection"""
    print("\n" + "="*60)
    print("DRIFT DETECTION DEMO")
    print("="*60)
    
    drift_detector = DriftDetector(validator)
    
    # Initial state
    print("\n1. Capturing initial infrastructure state...")
    initial_state = {
        "web-asg": {
            "min_size": 2,
            "max_size": 10,
            "desired_capacity": 3,
            "instance_type": "t3.micro"
        },
        "rds-primary": {
            "instance_class": "db.t3.medium",
            "storage": 100,
            "encrypted": True,
            "multi_az": True
        },
        "s3-assets": {
            "versioning": True,
            "encryption": "AES256",
            "lifecycle_rules": 2
        }
    }
    drift_detector.capture_state("production", initial_state)
    print("   ✓ State captured")
    
    # Simulate drift
    print("\n2. Checking current state (with drift)...")
    current_state = {
        "web-asg": {
            "min_size": 2,
            "max_size": 20,  # Changed
            "desired_capacity": 5,  # Changed
            "instance_type": "t3.small"  # Changed
        },
        "rds-primary": {
            "instance_class": "db.t3.medium",
            "storage": 200,  # Changed
            "encrypted": True,
            "multi_az": False  # Changed
        },
        "s3-assets": {
            "versioning": True,
            "encryption": "AES256",
            "lifecycle_rules": 2
        },
        "s3-backups": {  # New resource
            "versioning": True,
            "encryption": "AES256"
        }
    }
    
    drift_result = drift_detector.detect_drift("production", current_state)
    
    if drift_result["has_drift"]:
        print("   ⚠️  Drift detected!")
        print(f"\n   Changes found: {len(drift_result['differences'])}")
        
        # Group by type
        by_type = {}
        for diff in drift_result["differences"]:
            diff_type = diff["type"]
            if diff_type not in by_type:
                by_type[diff_type] = []
            by_type[diff_type].append(diff)
        
        for diff_type, diffs in by_type.items():
            print(f"\n   {diff_type.upper()} ({len(diffs)}):")
            for diff in diffs[:3]:  # Show first 3
                if diff_type == "added":
                    print(f"     + {diff['resource']}")
                elif diff_type == "removed":
                    print(f"     - {diff['resource']}")
                elif diff_type == "modified":
                    print(f"     ~ {diff['resource']}")


def demo_compliance_report(validator: IaCValidator, results: list):
    """Demonstrate compliance reporting"""
    print("\n" + "="*60)
    print("COMPLIANCE REPORT DEMO")
    print("="*60)
    
    # Analyze compliance across all results
    compliance_summary = {}
    
    for framework in ComplianceFramework:
        compliant_count = sum(1 for r in results if r.compliance_status.get(framework, True))
        compliance_summary[framework] = {
            "compliant": compliant_count,
            "total": len(results),
            "percentage": (compliant_count / len(results)) * 100
        }
    
    print("\nCompliance Summary:")
    print(f"{'Framework':<15} {'Compliant':<10} {'Percentage':<10}")
    print("-" * 35)
    
    for framework, stats in compliance_summary.items():
        status = "✅" if stats["percentage"] == 100 else "⚠️"
        print(f"{framework.value:<15} {stats['compliant']}/{stats['total']:<10} {stats['percentage']:.0f}% {status}")
    
    # Generate full report
    print("\n4. Generating validation report...")
    report_path = Path(tempfile.gettempdir()) / "iac_validation_demo_report.md"
    report = validator.generate_report(results, str(report_path))
    print(f"   ✓ Report generated: {report_path}")
    print(f"   - Total issues: {report['summary']['total_issues']}")
    print(f"   - Critical issues: {report['summary']['critical_issues']}")
    print(f"   - Estimated cost: ${report['summary']['total_cost_usd']:.2f}/month")


def main():
    """Run the complete demo"""
    print("="*60)
    print("INFRASTRUCTURE AS CODE VALIDATOR - DEMO")
    print("="*60)
    print(f"Started: {datetime.now()}")
    
    # Initialize
    validator = IaCValidator()
    temp_dir = Path(tempfile.mkdtemp())
    
    # Create demo files
    files = create_demo_files(temp_dir)
    
    # Run demos
    results = demo_basic_validation(validator, files)
    demo_cost_estimation(validator, results)
    demo_custom_policies(validator, files)
    demo_drift_detection(validator)
    demo_compliance_report(validator, results)
    
    print("\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)
    print(f"Completed: {datetime.now()}")
    
    print("\nKey Features Demonstrated:")
    print("✅ Multi-format IaC validation (Terraform, CloudFormation, Kubernetes)")
    print("✅ Security policy enforcement with severity levels")
    print("✅ Cost estimation and budget tracking")
    print("✅ Custom policy rule creation")
    print("✅ Infrastructure drift detection")
    print("✅ Compliance framework validation")
    print("✅ Comprehensive reporting")


if __name__ == "__main__":
    main()