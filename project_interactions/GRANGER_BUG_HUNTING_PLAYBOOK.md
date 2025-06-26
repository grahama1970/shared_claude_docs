# Granger Bug Hunting Playbook

> **A comprehensive guide based on real lessons learned from iterative bug hunting and security implementation**

## Table of Contents
1. [Core Principles](#core-principles)
2. [Bug Hunting Process](#bug-hunting-process)
3. [Testing Methodology](#testing-methodology)
4. [Security Implementation](#security-implementation)
5. [Validation & Verification](#validation--verification)
6. [Common Pitfalls](#common-pitfalls)
7. [Tools & Automation](#tools--automation)
8. [Incident Response](#incident-response)

---

## Core Principles

### 1. No Simulations or Mocks
**CRITICAL**: Never use simulated data or mock responses. Real bugs are only found through real interactions.

```python
# ❌ WRONG - Simulation
def test_auth():
    response = {"status": "success"}  # Simulated
    
# ✅ RIGHT - Real interaction
def test_auth():
    response = module.authenticate(token)  # Real call
```

### 2. Multi-AI Verification
Use multiple AI systems to grade test results:
- **Perplexity**: For research and validation
- **Gemini**: For critical assessment
- **Consensus required**: Both must agree for PASS

### 3. Iterative Improvement
- Start with basic tests
- Get external feedback
- Fix identified issues
- Repeat until secure

### 4. Documentation First
Document everything:
- Bug descriptions
- Root causes
- Fix implementations
- Test results

---

## Bug Hunting Process

### Phase 1: Initial Assessment
1. **Inventory modules**
   ```bash
   find /home/graham/workspace/experiments -name "*.py" -type f | grep -E "(auth|api|handler)"
   ```

2. **Identify attack surfaces**
   - Authentication endpoints
   - User input processing
   - Database queries
   - File operations
   - External API calls

3. **Create test matrix**
   | Module | Auth | SQL | XSS | CSRF | Path |
   |--------|------|-----|-----|------|------|
   | ArangoDB | ✓ | ✓ | - | - | ✓ |
   | Marker | ✓ | - | ✓ | - | ✓ |
   | ArXiv | ✓ | ✓ | - | - | - |

### Phase 2: Test Development
1. **Create real test scenarios**
   ```python
   # Real SQL injection test
   def test_sql_injection():
       malicious_query = "'; DROP TABLE users; --"
       
       # Real module call
       result = arangodb.query(malicious_query)
       
       # Check if blocked
       assert "error" in result
       assert "DROP TABLE" not in str(result)
   ```

2. **Test categories**
   - **Level 0**: Single module tests
   - **Level 1**: Cross-module integration
   - **Level 2**: Full pipeline tests
   - **Level 3**: Chaos engineering

### Phase 3: Bug Discovery
1. **Run tests with real modules**
2. **Document all findings**
3. **Categorize by severity**
   - CRITICAL: Remote code execution, data breach
   - HIGH: Authentication bypass, SQL injection
   - MEDIUM: Information disclosure, DoS
   - LOW: Missing headers, verbose errors

### Phase 4: Fix Implementation
1. **Create security middleware**
2. **Apply fixes systematically**
3. **Test each fix**
4. **Document changes**

---

## Testing Methodology

### Input Validation Tests
```python
test_inputs = [
    # SQL Injection
    "'; DROP TABLE users; --",
    "' OR '1'='1",
    "UNION SELECT * FROM passwords",
    
    # Path Traversal
    "../../../../etc/passwd",
    "..\\..\\..\\windows\\system32",
    
    # Command Injection
    "; cat /etc/passwd",
    "| rm -rf /",
    
    # XSS
    "<script>alert('XSS')</script>",
    "javascript:alert(1)",
    
    # Unicode/Encoding
    "🔥💣☠️" * 1000,
    "\x00\x01\x02",
    "%00%01%02"
]
```

### Authentication Tests
```python
auth_tests = [
    ("empty", ""),
    ("null", None),
    ("sql", "'; DROP TABLE users; --"),
    ("jwt_none", "eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0..."),
    ("long", "a" * 10000),
    ("special", "!@#$%^&*()"),
    ("unicode", "админ"),
]
```

### Error Handling Tests
1. **Trigger real errors**
2. **Check error messages**
3. **Verify no sensitive data**
4. **Ensure graceful degradation**

---

## Security Implementation

### 1. Token Validation
```python
class TokenValidator:
    def validate_token(self, token: Any) -> Tuple[bool, Optional[str]]:
        # Type check
        if not isinstance(token, str):
            return False, "Invalid token type"
            
        # Empty check
        if not token or token.strip() == "":
            return False, "Empty token"
            
        # Format check
        if not token.startswith("granger_"):
            return False, "Invalid token prefix"
            
        # Length check
        if len(token) < 20:
            return False, "Token too short"
            
        # Character check
        if not re.match(r"^granger_[a-zA-Z0-9_]+$", token):
            return False, "Invalid token format"
            
        return True, None
```

### 2. SQL Injection Protection
```python
class SQLInjectionProtector:
    def __init__(self):
        self.patterns = [
            r"('\s*OR\s*'1'\s*=\s*'1)",
            r"(--\s*$)",
            r"(;\s*DROP\s+TABLE)",
            r"(UNION\s+SELECT)",
        ]
        self.pattern = re.compile("|".join(self.patterns), re.IGNORECASE)
    
    def is_safe_input(self, user_input: str) -> Tuple[bool, Optional[str]]:
        if self.pattern.search(user_input):
            return False, "SQL injection detected"
        return True, None
```

### 3. Error Sanitization
```python
def remove_stack_traces(error: str) -> str:
    # Remove file paths
    cleaned = re.sub(r'File "[^"]+", line \d+', 'File [hidden]', error)
    
    # Remove sensitive keywords
    sensitive = ['password', 'secret', 'token', 'api_key']
    for word in sensitive:
        cleaned = re.sub(rf'\b{word}\b', '[redacted]', cleaned, flags=re.I)
    
    # Remove memory addresses
    cleaned = re.sub(r'at 0x[0-9a-fA-F]+', 'at [address]', cleaned)
    
    return cleaned
```

---

## Validation & Verification

### 1. Regression Testing
After each fix:
```bash
# Run security regression tests
pytest test_security_patches.py -v

# Run integration tests  
pytest test_integration_security.py -v

# Run bug hunt again
python comprehensive_bug_hunt_final.py
```

### 2. External Validation
```python
def get_ai_validation(scenario, result):
    prompt = f"""
    Scenario: {scenario}
    Result: {result}
    
    Grade this security test:
    1. Are vulnerabilities properly blocked?
    2. Are error messages safe?
    3. Is the response reasonable?
    
    Grade: PASS/FAIL
    Confidence: 0-100
    Bugs: [list any issues]
    """
    
    perplexity = call_perplexity(prompt)
    gemini = call_gemini(prompt)
    
    return combine_grades(perplexity, gemini)
```

### 3. Continuous Monitoring
- Set up security alerts
- Monitor for new CVEs
- Regular penetration testing
- Automated scanning

---

## Common Pitfalls

### 1. False Positives
**Problem**: Tests pass but bugs exist
**Solution**: Use real modules, verify actual behavior

### 2. Incomplete Coverage
**Problem**: Missing attack vectors
**Solution**: Use OWASP Top 10 as baseline

### 3. Breaking Functionality
**Problem**: Security fixes break features
**Solution**: Comprehensive integration testing

### 4. Performance Impact
**Problem**: Security slows system
**Solution**: Profile and optimize critical paths

---

## Tools & Automation

### CI/CD Integration
```yaml
name: Security Bug Hunt
on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Bandit
        run: bandit -r . -f json -o bandit.json
        
      - name: Run Safety
        run: safety check --json
        
      - name: Run Bug Hunt
        run: python comprehensive_bug_hunt_final.py
        
      - name: Check Results
        run: |
          if grep -q "FAIL" bug_hunt_report.md; then
            echo "Security issues found!"
            exit 1
          fi
```

### Automated Fixes
```python
def apply_security_patches():
    modules = find_all_modules()
    
    for module in modules:
        # Copy security middleware
        copy_security_middleware(module)
        
        # Patch authentication
        patch_auth_functions(module)
        
        # Patch SQL queries
        patch_sql_functions(module)
        
        # Patch error handlers
        patch_error_handlers(module)
```

---

## Incident Response

### If Vulnerability Found
1. **Immediate Actions**
   - Assess severity
   - Check if exploited
   - Prepare hotfix

2. **Communication**
   - Notify security team
   - Update status page
   - Prepare disclosure

3. **Fix & Deploy**
   - Develop fix
   - Test thoroughly
   - Deploy to production
   - Verify fix works

4. **Post-Mortem**
   - Document timeline
   - Identify root cause
   - Update playbook
   - Add regression test

---

## Key Takeaways

1. **Real Testing Only**: Never simulate - bugs hide in real interactions
2. **External Validation**: Get AI systems to verify your tests
3. **Iterative Process**: Each round makes the system more secure
4. **Document Everything**: Future you will thank present you
5. **Automate Security**: Make it part of every build

---

## Quick Reference

### Test Every Module For:
- [ ] Empty/null inputs
- [ ] SQL injection
- [ ] Command injection  
- [ ] Path traversal
- [ ] Authentication bypass
- [ ] JWT manipulation
- [ ] Error message leaks
- [ ] Resource exhaustion
- [ ] Unicode handling
- [ ] Race conditions

### Security Checklist:
- [ ] Token validation implemented
- [ ] SQL injection protection active
- [ ] Error messages sanitized
- [ ] Rate limiting configured
- [ ] Security headers set
- [ ] HTTPS enforced
- [ ] Logs sanitized
- [ ] Backups encrypted
- [ ] Access controls verified
- [ ] Monitoring enabled

---

*Last Updated: 2025-01-08*
*Based on: Granger Bug Hunt V1-V5 Experience*