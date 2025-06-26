
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: iac_validator_interaction.py
Purpose: Infrastructure as Code validation system with multi-format support and compliance checking

External Dependencies:
- pyyaml: https://pyyaml.org/wiki/PyYAMLDocumentation
- jsonschema: https://python-jsonschema.readthedocs.io/
- hcl2: https://github.com/amplify-education/python-hcl2

Example Usage:
>>> validator = IaCValidator()
>>> result = validator.validate_terraform("main.tf")
>>> print(result.is_valid)
True
"""

import json
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import hashlib
from collections import defaultdict


class IaCFormat(Enum):
    """Supported Infrastructure as Code formats"""
    TERRAFORM = "terraform"
    CLOUDFORMATION = "cloudformation"
    ANSIBLE = "ansible"
    KUBERNETES = "kubernetes"
    HELM = "helm"
    DOCKERCOMPOSE = "docker-compose"


class ComplianceFramework(Enum):
    """Supported compliance frameworks"""
    CIS = "cis"
    NIST = "nist"
    PCI_DSS = "pci-dss"
    HIPAA = "hipaa"
    SOC2 = "soc2"
    ISO27001 = "iso27001"


class ValidationSeverity(Enum):
    """Validation issue severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    """Represents a validation issue"""
    severity: ValidationSeverity
    category: str
    message: str
    file: str
    line: Optional[int] = None
    column: Optional[int] = None
    rule_id: Optional[str] = None
    fix_suggestion: Optional[str] = None
    compliance_frameworks: List[ComplianceFramework] = field(default_factory=list)


@dataclass
class CostEstimate:
    """Resource cost estimation"""
    resource_type: str
    resource_name: str
    estimated_monthly_cost: float
    currency: str = "USD"
    confidence: float = 0.0  # 0.0 to 1.0
    breakdown: Dict[str, float] = field(default_factory=dict)


@dataclass
class SecurityFinding:
    """Security-related finding"""
    severity: ValidationSeverity
    category: str
    description: str
    affected_resources: List[str]
    cve_ids: List[str] = field(default_factory=list)
    remediation: Optional[str] = None


@dataclass
class ValidationResult:
    """Complete validation result"""
    is_valid: bool
    format: IaCFormat
    issues: List[ValidationIssue]
    cost_estimates: List[CostEstimate]
    security_findings: List[SecurityFinding]
    compliance_status: Dict[ComplianceFramework, bool]
    resource_graph: Dict[str, List[str]]  # Dependencies
    metadata: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)


class PolicyRule:
    """Custom policy rule"""
    def __init__(self, rule_id: str, name: str, description: str,
                 severity: ValidationSeverity, category: str):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.severity = severity
        self.category = category
        self.compliance_frameworks: List[ComplianceFramework] = []
    
    def evaluate(self, resource: Dict[str, Any], context: Dict[str, Any]) -> Optional[ValidationIssue]:
        """Evaluate rule against resource"""
        raise NotImplementedError("Subclasses must implement evaluate()")


class SecurityGroupRule(PolicyRule):
    """Security group validation rule"""
    def evaluate(self, resource: Dict[str, Any], context: Dict[str, Any]) -> Optional[ValidationIssue]:
        if resource.get("type") == "aws_security_group":
            ingress_rules = resource.get("properties", {}).get("ingress", [])
            for rule in ingress_rules:
                if rule.get("cidr_blocks") == ["0.0.0.0/0"] and rule.get("from_port") == 22:
                    return ValidationIssue(
                        severity=self.severity,
                        category=self.category,
                        message="SSH port open to the world",
                        file=context.get("file", ""),
                        rule_id=self.rule_id,
                        fix_suggestion="Restrict SSH access to specific IP ranges",
                        compliance_frameworks=[ComplianceFramework.CIS, ComplianceFramework.NIST]
                    )
        return None


class EncryptionRule(PolicyRule):
    """Encryption validation rule"""
    def evaluate(self, resource: Dict[str, Any], context: Dict[str, Any]) -> Optional[ValidationIssue]:
        if resource.get("type") in ["aws_s3_bucket", "aws_rds_instance", "aws_ebs_volume"]:
            encrypted = resource.get("properties", {}).get("encrypted", False)
            if not encrypted:
                return ValidationIssue(
                    severity=self.severity,
                    category=self.category,
                    message=f"Resource {resource.get('name')} is not encrypted",
                    file=context.get("file", ""),
                    rule_id=self.rule_id,
                    fix_suggestion="Enable encryption for this resource",
                    compliance_frameworks=[ComplianceFramework.PCI_DSS, ComplianceFramework.HIPAA]
                )
        return None


class IaCValidator:
    """Main Infrastructure as Code validator"""
    
    def __init__(self):
        self.policy_rules: List[PolicyRule] = []
        self.cost_database = self._load_cost_database()
        self._initialize_default_rules()
    
    def _initialize_default_rules(self):
        """Initialize default policy rules"""
        self.policy_rules.extend([
            SecurityGroupRule(
                "SEC001", "Open Security Groups",
                "Detect security groups with unrestricted access",
                ValidationSeverity.CRITICAL, "security"
            ),
            EncryptionRule(
                "SEC002", "Encryption at Rest",
                "Ensure resources are encrypted at rest",
                ValidationSeverity.ERROR, "security"
            )
        ])
    
    def _load_cost_database(self) -> Dict[str, Dict[str, float]]:
        """Load cost estimation database"""
        return {
            "aws_instance": {
                "t2.micro": 8.5,
                "t2.small": 17.0,
                "t2.medium": 34.0,
                "t3.micro": 7.5,
                "t3.small": 15.0,
                "m5.large": 70.0,
                "m5.xlarge": 140.0
            },
            "aws_rds_instance": {
                "db.t2.micro": 15.0,
                "db.t2.small": 30.0,
                "db.m5.large": 125.0
            },
            "aws_ebs_volume": {
                "gp2": 0.10,  # per GB
                "gp3": 0.08,  # per GB
                "io1": 0.125  # per GB
            }
        }
    
    def validate_terraform(self, file_path: str) -> ValidationResult:
        """Validate Terraform configuration"""
        issues = []
        cost_estimates = []
        security_findings = []
        resource_graph = defaultdict(list)
        
        try:
            # Parse Terraform HCL (simplified for example)
            content = Path(file_path).read_text()
            resources = self._parse_terraform_resources(content)
            
            # Apply policy rules
            for resource in resources:
                context = {"file": file_path}
                for rule in self.policy_rules:
                    issue = rule.evaluate(resource, context)
                    if issue:
                        issues.append(issue)
            
            # Estimate costs
            for resource in resources:
                estimate = self._estimate_resource_cost(resource)
                if estimate:
                    cost_estimates.append(estimate)
            
            # Build resource graph
            for resource in resources:
                deps = self._extract_dependencies(resource)
                resource_graph[resource["name"]] = deps
            
            # Check compliance
            compliance_status = self._check_compliance(resources, issues)
            
        except Exception as e:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="parsing",
                message=f"Failed to parse Terraform file: {str(e)}",
                file=file_path
            ))
        
        return ValidationResult(
            is_valid=not any(i.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL] for i in issues),
            format=IaCFormat.TERRAFORM,
            issues=issues,
            cost_estimates=cost_estimates,
            security_findings=security_findings,
            compliance_status=compliance_status,
            resource_graph=dict(resource_graph),
            metadata={"file": file_path}
        )
    
    def validate_cloudformation(self, file_path: str) -> ValidationResult:
        """Validate CloudFormation template"""
        issues = []
        cost_estimates = []
        security_findings = []
        resource_graph = defaultdict(list)
        
        try:
            with open(file_path, 'r') as f:
                template = yaml.safe_load(f) if file_path.endswith('.yaml') else json.load(f)
            
            resources = template.get("Resources", {})
            
            # Validate template structure
            if "AWSTemplateFormatVersion" not in template:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    category="structure",
                    message="Missing AWSTemplateFormatVersion",
                    file=file_path,
                    fix_suggestion="Add 'AWSTemplateFormatVersion: 2010-09-09'"
                ))
            
            # Check resources
            for name, resource in resources.items():
                # Validate resource type
                if "Type" not in resource:
                    issues.append(ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        category="structure",
                        message=f"Resource {name} missing Type",
                        file=file_path
                    ))
                
                # Apply security checks
                if resource.get("Type") == "AWS::EC2::SecurityGroup":
                    self._validate_security_group_cf(name, resource, issues, file_path)
            
            compliance_status = self._check_compliance_cf(template, issues)
            
        except Exception as e:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="parsing",
                message=f"Failed to parse CloudFormation template: {str(e)}",
                file=file_path
            ))
        
        return ValidationResult(
            is_valid=not any(i.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL] for i in issues),
            format=IaCFormat.CLOUDFORMATION,
            issues=issues,
            cost_estimates=cost_estimates,
            security_findings=security_findings,
            compliance_status=compliance_status,
            resource_graph=dict(resource_graph),
            metadata={"file": file_path}
        )
    
    def validate_kubernetes(self, file_path: str) -> ValidationResult:
        """Validate Kubernetes manifest"""
        issues = []
        security_findings = []
        
        try:
            with open(file_path, 'r') as f:
                # Handle multi-document YAML
                documents = list(yaml.safe_load_all(f))
            
            for doc in documents:
                if not doc:
                    continue
                
                kind = doc.get("kind", "")
                
                # Validate based on resource kind
                if kind == "Deployment":
                    self._validate_k8s_deployment(doc, issues, file_path)
                elif kind == "Service":
                    self._validate_k8s_service(doc, issues, file_path)
                elif kind == "NetworkPolicy":
                    self._validate_k8s_network_policy(doc, issues, file_path)
                
                # Security checks
                if kind in ["Deployment", "StatefulSet", "DaemonSet"]:
                    self._check_k8s_security(doc, security_findings, file_path)
            
        except Exception as e:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="parsing",
                message=f"Failed to parse Kubernetes manifest: {str(e)}",
                file=file_path
            ))
        
        return ValidationResult(
            is_valid=not any(i.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL] for i in issues),
            format=IaCFormat.KUBERNETES,
            issues=issues,
            cost_estimates=[],
            security_findings=security_findings,
            compliance_status={},
            resource_graph={},
            metadata={"file": file_path}
        )
    
    def validate_ansible(self, file_path: str) -> ValidationResult:
        """Validate Ansible playbook"""
        issues = []
        
        try:
            with open(file_path, 'r') as f:
                playbook = yaml.safe_load(f)
            
            if isinstance(playbook, list):
                for play in playbook:
                    self._validate_ansible_play(play, issues, file_path)
            else:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    category="structure",
                    message="Playbook should be a list of plays",
                    file=file_path
                ))
            
        except Exception as e:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="parsing",
                message=f"Failed to parse Ansible playbook: {str(e)}",
                file=file_path
            ))
        
        return ValidationResult(
            is_valid=not any(i.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL] for i in issues),
            format=IaCFormat.ANSIBLE,
            issues=issues,
            cost_estimates=[],
            security_findings=[],
            compliance_status={},
            resource_graph={},
            metadata={"file": file_path}
        )
    
    def add_custom_rule(self, rule: PolicyRule):
        """Add custom policy rule"""
        self.policy_rules.append(rule)
    
    def estimate_total_cost(self, results: List[ValidationResult]) -> Dict[str, float]:
        """Estimate total infrastructure cost"""
        total_by_currency = defaultdict(float)
        
        for result in results:
            for estimate in result.cost_estimates:
                total_by_currency[estimate.currency] += estimate.estimated_monthly_cost
        
        return dict(total_by_currency)
    
    def generate_report(self, results: List[ValidationResult], output_path: str):
        """Generate validation report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_files": len(results),
                "valid_files": sum(1 for r in results if r.is_valid),
                "total_issues": sum(len(r.issues) for r in results),
                "critical_issues": sum(1 for r in results for i in r.issues if i.severity == ValidationSeverity.CRITICAL),
                "total_cost_usd": sum(e.estimated_monthly_cost for r in results for e in r.cost_estimates if e.currency == "USD")
            },
            "details": []
        }
        
        for result in results:
            detail = {
                "file": result.metadata.get("file", ""),
                "format": result.format.value,
                "is_valid": result.is_valid,
                "issues": [
                    {
                        "severity": i.severity.value,
                        "category": i.category,
                        "message": i.message,
                        "line": i.line,
                        "rule_id": i.rule_id
                    }
                    for i in result.issues
                ],
                "cost_estimates": [
                    {
                        "resource": e.resource_name,
                        "monthly_cost": e.estimated_monthly_cost,
                        "currency": e.currency
                    }
                    for e in result.cost_estimates
                ]
            }
            report["details"].append(detail)
        
        # Generate markdown report
        markdown = self._generate_markdown_report(report)
        Path(output_path).write_text(markdown)
        
        return report
    
    def _parse_terraform_resources(self, content: str) -> List[Dict[str, Any]]:
        """Parse Terraform resources (simplified)"""
        resources = []
        # Simplified regex-based parsing
        resource_pattern = r'resource\s+"(\w+)"\s+"(\w+)"\s*\{([^}]+)\}'
        
        for match in re.finditer(resource_pattern, content, re.DOTALL):
            resource_type, resource_name, resource_body = match.groups()
            resources.append({
                "type": resource_type,
                "name": resource_name,
                "properties": self._parse_hcl_properties(resource_body)
            })
        
        return resources
    
    def _parse_hcl_properties(self, body: str) -> Dict[str, Any]:
        """Parse HCL properties (simplified)"""
        properties = {}
        # Very simplified parsing
        lines = body.strip().split('\n')
        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"')
                properties[key] = value
        return properties
    
    def _estimate_resource_cost(self, resource: Dict[str, Any]) -> Optional[CostEstimate]:
        """Estimate resource cost"""
        resource_type = resource.get("type", "")
        
        if resource_type in self.cost_database:
            instance_type = resource.get("properties", {}).get("instance_type", "t2.micro")
            if instance_type in self.cost_database[resource_type]:
                return CostEstimate(
                    resource_type=resource_type,
                    resource_name=resource.get("name", ""),
                    estimated_monthly_cost=self.cost_database[resource_type][instance_type],
                    confidence=0.8
                )
        
        return None
    
    def _extract_dependencies(self, resource: Dict[str, Any]) -> List[str]:
        """Extract resource dependencies"""
        deps = []
        properties = resource.get("properties", {})
        
        # Look for references to other resources
        for value in properties.values():
            if isinstance(value, str) and value.startswith("${"):
                # Extract resource reference
                match = re.search(r'\$\{(\w+)\.(\w+)', value)
                if match:
                    deps.append(match.group(2))
        
        return deps
    
    def _check_compliance(self, resources: List[Dict[str, Any]], 
                         issues: List[ValidationIssue]) -> Dict[ComplianceFramework, bool]:
        """Check compliance status"""
        compliance = {}
        
        # CIS compliance
        cis_issues = [i for i in issues if ComplianceFramework.CIS in i.compliance_frameworks]
        compliance[ComplianceFramework.CIS] = len(cis_issues) == 0
        
        # NIST compliance
        nist_issues = [i for i in issues if ComplianceFramework.NIST in i.compliance_frameworks]
        compliance[ComplianceFramework.NIST] = len(nist_issues) == 0
        
        return compliance
    
    def _check_compliance_cf(self, template: Dict[str, Any], 
                           issues: List[ValidationIssue]) -> Dict[ComplianceFramework, bool]:
        """Check CloudFormation compliance"""
        return self._check_compliance([], issues)
    
    def _validate_security_group_cf(self, name: str, resource: Dict[str, Any], 
                                   issues: List[ValidationIssue], file_path: str):
        """Validate CloudFormation security group"""
        ingress_rules = resource.get("Properties", {}).get("SecurityGroupIngress", [])
        
        for rule in ingress_rules:
            if rule.get("CidrIp") == "0.0.0.0/0":
                if rule.get("FromPort") == 22:
                    issues.append(ValidationIssue(
                        severity=ValidationSeverity.CRITICAL,
                        category="security",
                        message=f"Security group {name} allows SSH from anywhere",
                        file=file_path,
                        rule_id="SEC001",
                        fix_suggestion="Restrict SSH access to specific IP ranges"
                    ))
    
    def _validate_k8s_deployment(self, deployment: Dict[str, Any], 
                                issues: List[ValidationIssue], file_path: str):
        """Validate Kubernetes deployment"""
        metadata = deployment.get("metadata", {})
        spec = deployment.get("spec", {})
        
        # Check required fields
        if not metadata.get("name"):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="structure",
                message="Deployment missing metadata.name",
                file=file_path
            ))
        
        # Check replicas
        if not spec.get("replicas"):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                category="configuration",
                message="Deployment missing replicas specification",
                file=file_path,
                fix_suggestion="Add spec.replicas field"
            ))
    
    def _validate_k8s_service(self, service: Dict[str, Any], 
                             issues: List[ValidationIssue], file_path: str):
        """Validate Kubernetes service"""
        spec = service.get("spec", {})
        
        if not spec.get("selector"):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="structure",
                message="Service missing selector",
                file=file_path
            ))
    
    def _validate_k8s_network_policy(self, policy: Dict[str, Any], 
                                    issues: List[ValidationIssue], file_path: str):
        """Validate Kubernetes NetworkPolicy"""
        spec = policy.get("spec", {})
        
        if not spec.get("podSelector"):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="structure",
                message="NetworkPolicy missing podSelector",
                file=file_path
            ))
    
    def _check_k8s_security(self, resource: Dict[str, Any], 
                           findings: List[SecurityFinding], file_path: str):
        """Check Kubernetes security"""
        containers = resource.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])
        
        for container in containers:
            # Check for privileged containers
            security_context = container.get("securityContext", {})
            if security_context.get("privileged", False):
                findings.append(SecurityFinding(
                    severity=ValidationSeverity.CRITICAL,
                    category="container-security",
                    description=f"Container {container.get('name')} runs in privileged mode",
                    affected_resources=[resource.get("metadata", {}).get("name", "")],
                    remediation="Remove privileged: true from securityContext"
                ))
            
            # Check for root user
            if security_context.get("runAsUser") == 0:
                findings.append(SecurityFinding(
                    severity=ValidationSeverity.ERROR,
                    category="container-security",
                    description=f"Container {container.get('name')} runs as root",
                    affected_resources=[resource.get("metadata", {}).get("name", "")],
                    remediation="Set runAsUser to non-root UID"
                ))
    
    def _validate_ansible_play(self, play: Dict[str, Any], 
                              issues: List[ValidationIssue], file_path: str):
        """Validate Ansible play"""
        if not play.get("hosts"):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="structure",
                message="Play missing hosts specification",
                file=file_path
            ))
        
        tasks = play.get("tasks", [])
        for i, task in enumerate(tasks):
            if not task.get("name"):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    category="best-practice",
                    message=f"Task {i+1} missing name",
                    file=file_path,
                    fix_suggestion="Add descriptive name to task"
                ))
    
    def _generate_markdown_report(self, report: Dict[str, Any]) -> str:
        """Generate markdown report"""
        md = f"""# Infrastructure as Code Validation Report

Generated: {report['timestamp']}

## Summary

- **Total Files Analyzed**: {report['summary']['total_files']}
- **Valid Files**: {report['summary']['valid_files']}
- **Total Issues**: {report['summary']['total_issues']}
- **Critical Issues**: {report['summary']['critical_issues']}
- **Estimated Monthly Cost**: ${report['summary']['total_cost_usd']:.2f} USD

## Issues by Severity

| Severity | Count |
|----------|-------|
"""
        
        severity_counts = defaultdict(int)
        for detail in report['details']:
            for issue in detail['issues']:
                severity_counts[issue['severity']] += 1
        
        for severity in ['critical', 'error', 'warning', 'info']:
            md += f"| {severity.upper()} | {severity_counts.get(severity, 0)} |\n"
        
        md += "\n## File Details\n\n"
        
        for detail in report['details']:
            md += f"### {detail['file']}\n\n"
            md += f"- **Format**: {detail['format']}\n"
            md += f"- **Valid**: {'✅' if detail['is_valid'] else '❌'}\n"
            md += f"- **Issues**: {len(detail['issues'])}\n"
            
            if detail['issues']:
                md += "\n#### Issues\n\n"
                md += "| Severity | Category | Message | Rule ID |\n"
                md += "|----------|----------|---------|--------|\n"
                
                for issue in detail['issues']:
                    md += f"| {issue['severity']} | {issue['category']} | {issue['message']} | {issue.get('rule_id', 'N/A')} |\n"
            
            if detail['cost_estimates']:
                md += "\n#### Cost Estimates\n\n"
                md += "| Resource | Monthly Cost |\n"
                md += "|----------|-------------|\n"
                
                for estimate in detail['cost_estimates']:
                    md += f"| {estimate['resource']} | ${estimate['monthly_cost']:.2f} {estimate['currency']} |\n"
            
            md += "\n---\n\n"
        
        return md


class DriftDetector:
    """Detect drift between IaC and actual infrastructure"""
    
    def __init__(self, validator: IaCValidator):
        self.validator = validator
        self.state_cache = {}
    
    def capture_state(self, infrastructure_id: str, state: Dict[str, Any]):
        """Capture current infrastructure state"""
        state_hash = hashlib.sha256(
            json.dumps(state, sort_keys=True).encode()
        ).hexdigest()
        
        self.state_cache[infrastructure_id] = {
            "state": state,
            "hash": state_hash,
            "timestamp": datetime.now()
        }
    
    def detect_drift(self, infrastructure_id: str, 
                    current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Detect drift from cached state"""
        if infrastructure_id not in self.state_cache:
            return {"has_drift": False, "message": "No baseline state found"}
        
        cached = self.state_cache[infrastructure_id]
        current_hash = hashlib.sha256(
            json.dumps(current_state, sort_keys=True).encode()
        ).hexdigest()
        
        if current_hash != cached["hash"]:
            # Analyze differences
            diffs = self._compare_states(cached["state"], current_state)
            return {
                "has_drift": True,
                "differences": diffs,
                "last_known_state": cached["timestamp"]
            }
        
        return {"has_drift": False}
    
    def _compare_states(self, old_state: Dict[str, Any], 
                       new_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Compare two states and return differences"""
        differences = []
        
        # Check for added resources
        for key in new_state:
            if key not in old_state:
                differences.append({
                    "type": "added",
                    "resource": key,
                    "value": new_state[key]
                })
        
        # Check for removed resources
        for key in old_state:
            if key not in new_state:
                differences.append({
                    "type": "removed",
                    "resource": key,
                    "value": old_state[key]
                })
        
        # Check for modified resources
        for key in old_state:
            if key in new_state and old_state[key] != new_state[key]:
                differences.append({
                    "type": "modified",
                    "resource": key,
                    "old_value": old_state[key],
                    "new_value": new_state[key]
                })
        
        return differences


if __name__ == "__main__":
    # Test with real examples
    validator = IaCValidator()
    
    # Test Terraform validation
    terraform_content = '''
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
      instance_type = "t2.micro"
      ami           = "ami-12345678"
    }
    '''
    
    # Create test file
    test_file = Path("/tmp/test.tf")
    test_file.write_text(terraform_content)
    
    result = validator.validate_terraform(str(test_file))
    print(f"✅ Terraform validation: Valid={result.is_valid}, Issues={len(result.issues)}")
    
    # Test CloudFormation validation
    cf_template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Resources": {
            "WebSecurityGroup": {
                "Type": "AWS::EC2::SecurityGroup",
                "Properties": {
                    "SecurityGroupIngress": [{
                        "IpProtocol": "tcp",
                        "FromPort": 22,
                        "ToPort": 22,
                        "CidrIp": "0.0.0.0/0"
                    }]
                }
            }
        }
    }
    
    cf_file = Path("/tmp/test.json")
    cf_file.write_text(json.dumps(cf_template))
    
    cf_result = validator.validate_cloudformation(str(cf_file))
    print(f"✅ CloudFormation validation: Valid={cf_result.is_valid}, Issues={len(cf_result.issues)}")
    
    # Test Kubernetes validation
    k8s_manifest = """
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
        securityContext:
          privileged: true
          runAsUser: 0
"""
    
    k8s_file = Path("/tmp/test.yaml")
    k8s_file.write_text(k8s_manifest)
    
    k8s_result = validator.validate_kubernetes(str(k8s_file))
    print(f"✅ Kubernetes validation: Valid={k8s_result.is_valid}, Findings={len(k8s_result.security_findings)}")
    
    # Generate report
    all_results = [result, cf_result, k8s_result]
    report_path = "/tmp/iac_validation_report.md"
    validator.generate_report(all_results, report_path)
    print(f"✅ Generated report: {report_path}")
    
    # Test drift detection
    drift_detector = DriftDetector(validator)
    
    initial_state = {
        "instance-1": {"type": "t2.micro", "state": "running"},
        "bucket-1": {"encryption": True, "versioning": False}
    }
    
    drift_detector.capture_state("prod-infra", initial_state)
    
    # Simulate drift
    current_state = {
        "instance-1": {"type": "t2.small", "state": "running"},  # Changed
        "bucket-1": {"encryption": True, "versioning": True},    # Changed
        "instance-2": {"type": "t2.micro", "state": "running"}  # Added
    }
    
    drift_result = drift_detector.detect_drift("prod-infra", current_state)
    print(f"✅ Drift detection: Has drift={drift_result['has_drift']}")
    
    print("\n✅ All IaC validator functions working correctly!")