# Infrastructure as Code Validator

A comprehensive IaC validation system with multi-format support, security compliance checking, cost estimation, and drift detection capabilities.

## Features

### Multi-Format Support
- **Terraform** (.tf, .tfvars) - HCL configuration validation
- **CloudFormation** (.json, .yaml) - AWS template validation  
- **Kubernetes** (.yaml) - Manifest validation
- **Ansible** (.yaml) - Playbook validation
- **Helm** Charts (planned)
- **Docker Compose** (planned)

### Security & Compliance
- **Policy as Code** - Custom rule engine for security policies
- **Compliance Frameworks** - CIS, NIST, PCI-DSS, HIPAA, SOC2, ISO27001
- **Security Scanning** - Detect common security misconfigurations
- **CVE Detection** - Identify vulnerable container images (planned)
- **Best Practices** - Enforce infrastructure best practices

### Cost Management
- **Cost Estimation** - Estimate monthly infrastructure costs
- **Resource Pricing** - AWS instance, storage, and database pricing
- **Cost Aggregation** - Total costs across multiple files
- **Cost Breakdown** - Detailed cost analysis by resource

### Drift Detection
- **State Tracking** - Capture and track infrastructure state
- **Change Detection** - Identify added, removed, and modified resources
- **Drift Analysis** - Compare desired vs actual state
- **History Tracking** - Track changes over time

### Reporting & Integration
- **Validation Reports** - Detailed markdown reports with issues and recommendations
- **CI/CD Integration** - Exit codes and structured output for pipelines
- **Multiple Output Formats** - JSON, YAML, Markdown
- **Issue Tracking** - Severity levels, categories, and fix suggestions

## Installation

```bash
# Clone the repository
git clone <repository>

# Install dependencies
pip install pyyaml jsonschema
```

## Usage

### Basic Validation

```python
from iac_validator_interaction import IaCValidator

# Initialize validator
validator = IaCValidator()

# Validate Terraform
result = validator.validate_terraform("main.tf")
print(f"Valid: {result.is_valid}")
print(f"Issues: {len(result.issues)}")

# Validate CloudFormation
cf_result = validator.validate_cloudformation("template.yaml")

# Validate Kubernetes
k8s_result = validator.validate_kubernetes("deployment.yaml")

# Validate Ansible
ansible_result = validator.validate_ansible("playbook.yaml")
```

### Custom Policy Rules

```python
from iac_validator_interaction import PolicyRule, ValidationIssue, ValidationSeverity

class CustomRule(PolicyRule):
    def evaluate(self, resource, context):
        # Implement custom validation logic
        if resource.get("type") == "aws_instance":
            if not resource.get("properties", {}).get("monitoring"):
                return ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    category="monitoring",
                    message="Instance monitoring not enabled",
                    file=context.get("file", ""),
                    rule_id=self.rule_id
                )
        return None

# Add custom rule
validator.add_custom_rule(CustomRule(
    "MON001", "Instance Monitoring",
    "Ensure monitoring is enabled",
    ValidationSeverity.WARNING, "monitoring"
))
```

### Cost Estimation

```python
# Get cost estimates from validation results
total_cost = sum(e.estimated_monthly_cost for e in result.cost_estimates)
print(f"Estimated monthly cost: ${total_cost:.2f}")

# Aggregate costs across multiple files
results = [
    validator.validate_terraform("web.tf"),
    validator.validate_terraform("app.tf"),
    validator.validate_terraform("db.tf")
]

total_costs = validator.estimate_total_cost(results)
print(f"Total infrastructure cost: ${total_costs['USD']:.2f}/month")
```

### Drift Detection

```python
from iac_validator_interaction import DriftDetector

# Initialize drift detector
drift_detector = DriftDetector(validator)

# Capture baseline state
initial_state = {
    "instance-1": {"type": "t2.micro", "state": "running"},
    "bucket-1": {"encryption": True}
}
drift_detector.capture_state("prod-env", initial_state)

# Check for drift
current_state = {
    "instance-1": {"type": "t2.small", "state": "running"},  # Changed
    "bucket-1": {"encryption": True},
    "instance-2": {"type": "t2.micro", "state": "running"}  # Added
}

drift_result = drift_detector.detect_drift("prod-env", current_state)
if drift_result["has_drift"]:
    print(f"Drift detected: {len(drift_result['differences'])} changes")
```

### Generate Reports

```python
# Generate validation report
results = [
    validator.validate_terraform("main.tf"),
    validator.validate_cloudformation("template.yaml"),
    validator.validate_kubernetes("deployment.yaml")
]

report = validator.generate_report(results, "validation_report.md")
print(f"Report generated with {report['summary']['total_issues']} issues")
```

## Validation Rules

### Security Rules
- **SEC001**: Open Security Groups - Detect unrestricted access (0.0.0.0/0)
- **SEC002**: Encryption at Rest - Ensure resources are encrypted
- **SEC003**: Privileged Containers - Detect containers running as root
- **SEC004**: Network Policies - Ensure network segmentation

### Compliance Rules
- **CIS**: Center for Internet Security benchmarks
- **NIST**: National Institute of Standards and Technology
- **PCI-DSS**: Payment Card Industry Data Security Standard
- **HIPAA**: Health Insurance Portability and Accountability Act

### Best Practices
- Resource naming conventions
- Tagging requirements
- Backup configurations
- Monitoring and logging
- High availability setup

## CI/CD Integration

### GitHub Actions

```yaml
- name: Validate Infrastructure
  run: |
    python -m iac_validator_interaction validate \
      --format terraform \
      --path ./infrastructure \
      --output report.md \
      --fail-on error
```

### Jenkins Pipeline

```groovy
stage('IaC Validation') {
    steps {
        script {
            def result = sh(
                script: 'python validate_infrastructure.py',
                returnStatus: true
            )
            if (result != 0) {
                error "Infrastructure validation failed"
            }
        }
    }
}
```

## Architecture

The validator follows a modular architecture:

1. **Parser Layer** - Format-specific parsers for each IaC language
2. **Rule Engine** - Extensible policy evaluation system
3. **Cost Database** - Pricing information for cloud resources
4. **State Tracker** - Drift detection and state management
5. **Report Generator** - Multiple output format support

## Contributing

1. Add new IaC format support by implementing format-specific validator
2. Create custom policy rules by extending `PolicyRule` class
3. Update cost database with new resource types and pricing
4. Add compliance framework mappings

## License

MIT License