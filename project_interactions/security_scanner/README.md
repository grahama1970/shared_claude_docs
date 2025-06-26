# Security Scanner Interaction

A comprehensive security vulnerability scanner that detects OWASP Top 10 vulnerabilities, dependency issues, and provides actionable remediation suggestions.

## Features

### Vulnerability Detection
- **OWASP Top 10** - All major vulnerability categories
- **Multi-language support** - Python, JavaScript, Java, PHP, Ruby, Go, C#, C/C++
- **Dependency scanning** - Python, NPM, Maven vulnerabilities
- **Secret detection** - API keys, passwords, tokens, certificates
- **Code analysis** - AST-based analysis for accuracy

### Security Checks
- SQL Injection (CWE-89)
- Cross-Site Scripting (XSS) (CWE-79)
- Command Injection (CWE-78)
- XML External Entity (XXE) (CWE-611)
- Path Traversal (CWE-22)
- Weak Cryptography (CWE-327)
- Hardcoded Secrets (CWE-798)
- Insecure Deserialization (CWE-502)
- Using Components with Known Vulnerabilities (CWE-1035)

### Advanced Features
- **Risk scoring** - Severity-based prioritization
- **False positive management** - Mark and track false positives
- **Compliance checking** - PCI-DSS, HIPAA, OWASP compliance
- **CI/CD integration** - Exit codes and JSON reports
- **Parallel scanning** - Fast multi-threaded analysis
- **Remediation suggestions** - Specific fixes for each vulnerability

## Usage

```python
from security_scanner_interaction import SecurityScannerInteraction

# Initialize scanner
scanner = SecurityScannerInteraction()

# Scan a project
result = scanner.scan_project(
    "/path/to/project",
    scan_dependencies=True,
    compliance_checks=['OWASP', 'PCI-DSS']
)

# Generate report
report = scanner.generate_report(result, format='markdown')
print(report)

# Check specific results
print(f"Total vulnerabilities: {result.total_vulnerabilities}")
print(f"Critical issues: {result.severity_counts.get('critical', 0)}")
print(f"OWASP compliant: {result.compliance_status.get('OWASP', False)}")
```

## Vulnerability Types

### Injection Vulnerabilities
- SQL Injection through string concatenation
- Command injection via subprocess/os.system
- LDAP/XPath injection patterns
- Code injection through eval/exec

### Authentication & Access
- Broken authentication patterns
- Insufficient access controls
- Session management issues

### Data Exposure
- Hardcoded credentials and secrets
- Sensitive data in logs
- Weak encryption algorithms
- Missing encryption

### Configuration
- Security misconfiguration
- Default credentials
- Verbose error messages
- Debug mode enabled

## Remediation Examples

### SQL Injection
```python
# Vulnerable
query = f"SELECT * FROM users WHERE id = {user_id}"

# Remediation
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

### XSS Prevention
```javascript
// Vulnerable
element.innerHTML = userInput;

// Remediation
element.textContent = userInput;
// Or use a sanitization library
```

### Secret Management
```python
# Vulnerable
API_KEY = "sk-1234567890"

# Remediation
API_KEY = os.environ.get('API_KEY')
# Or use a secrets management service
```

## Compliance Checking

### PCI-DSS
- No critical vulnerabilities
- No hardcoded payment data
- Strong cryptography required
- Audit logging present

### HIPAA
- Encryption for PHI data
- Access controls implemented
- Audit trails maintained
- No weak cryptography

### OWASP Top 10
- Checks all OWASP categories
- Fails on high/critical issues
- Provides specific guidance

## Integration

### CI/CD Pipeline
```bash
# Run scan in CI
python -m security_scanner_interaction /path/to/code

# Check exit code
if [ $? -ne 0 ]; then
    echo "Security vulnerabilities found!"
    exit 1
fi
```

### JSON Output
```python
# Get JSON report for automation
json_report = scanner.generate_report(result, format='json')
data = json.loads(json_report)

# Process vulnerabilities
for vuln in data['vulnerabilities']:
    if vuln['severity'] == 'critical':
        # Handle critical issues
        pass
```

## Performance

- Parallel file scanning (8 workers)
- Efficient regex patterns
- AST caching for Python files
- Incremental scanning support
- ~1000 files/second on modern hardware

## Configuration

```python
# Custom configuration
config = {
    'exclude_paths': ['tests', 'docs'],
    'severity_threshold': 'medium',
    'max_file_size': 10_000_000,  # 10MB
    'timeout': 300  # 5 minutes
}

scanner = SecurityScannerInteraction(config)
```

## False Positive Management

```python
# Mark false positive
scanner.mark_false_positive(
    file_path="src/config.py",
    line_number=42,
    secret_type="api_key"
)

# False positives are remembered across scans
```

## Dependencies

- Python 3.8+
- No external security tools required
- Optional: bandit, safety, semgrep for enhanced scanning

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test category
python -m pytest tests/test_vulnerability_detection.py

# Run with coverage
python -m pytest --cov=security_scanner_interaction tests/
```