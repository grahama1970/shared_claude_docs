# Granger Hub Orchestration Example: CWE Security Analysis

Here's a concrete example showing how granger_hub orchestrates multiple modules for security analysis:

## User Request
```python
granger_hub.analyze_code_security("src/authentication.py")
```

## How Granger Hub Orchestrates This

### Step 1: Code Parser Module
```python
# Hub calls code parser first
parse_result = code_parser.handle({
    "task": "parse_code",
    "code_path": "src/authentication.py",
    "language": "python",
    "extract_patterns": [
        "input_validation",
        "authentication_flows",
        "cryptographic_operations",
        "sql_queries"
    ]
})
# Returns: AST, code patterns, function calls, data flows
```

### Step 2: SPARTA Module (with CVE/CWE Knowledge)
```python
# Hub sends parsed patterns to SPARTA
cwe_result = sparta.handle({
    "task": "check_cwe_violations",
    "code_patterns": parse_result["code_patterns"],
    "cwe_categories": [
        "CWE-20",   # Improper Input Validation
        "CWE-79",   # Cross-site Scripting
        "CWE-89",   # SQL Injection
        "CWE-287",  # Improper Authentication
        "CWE-327",  # Broken Crypto
        "CWE-798"   # Hard-coded Credentials
    ]
})
# Returns: CWE violations, severity scores, exploitation likelihood
```

### Step 3: Vulnerability Analyzer Module
```python
# Hub sends both code and CWEs for deep analysis
vuln_result = vulnerability_analyzer.handle({
    "task": "analyze_vulnerabilities",
    "code_ast": parse_result["ast"],
    "cwe_rules": cwe_result["cwe_violations"],
    "generate_poc": True,
    "check_exploitability": True
})
# Returns: vulnerabilities, attack vectors, proof of concepts
```

### Step 4: ArXiv Module (Find Research on Fixes)
```python
# Hub searches for papers about these vulnerabilities
research_result = arxiv.handle({
    "query": "CWE-89 SQL injection prevention authentication",
    "evidence_type": "supporting",
    "max_results": 5
})
# Returns: Papers about secure coding practices
```

### Step 5: Remediation Engine Module
```python
# Hub combines all info for remediation
fix_result = remediation_engine.handle({
    "task": "generate_fixes",
    "vulnerabilities": vuln_result["vulnerabilities"],
    "code_context": parse_result["ast"],
    "research_papers": research_result["papers"],
    "fix_priority": "severity",
    "generate_tests": True
})
# Returns: Code fixes, secure patterns, test cases
```

### Step 6: ArangoDB Storage
```python
# Hub stores everything with relationships
# Store the analysis session
arango.handle({
    "operation": "create",
    "collection": "security_analyses",
    "data": {
        "file": "src/authentication.py",
        "timestamp": datetime.now(),
        "cwe_violations": len(cwe_result["cwe_violations"]),
        "critical_issues": vuln_result["critical_count"]
    }
})

# Store CWE violations
for violation in cwe_result["cwe_violations"]:
    arango.handle({
        "operation": "create",
        "collection": "cwe_violations",
        "data": violation
    })

# Create relationships
arango.handle({
    "operation": "create_edge",
    "from": "files/authentication_py",
    "to": f"cwe_violations/{violation['id']}",
    "edge_type": "contains_vulnerability"
})
```

## The Complete Result

The hub returns a comprehensive security report:
```python
{
    "file": "src/authentication.py",
    "security_score": 3.2,  # Out of 10
    "cwe_violations": [
        {
            "cwe_id": "CWE-89",
            "severity": "critical",
            "line_numbers": [45, 67, 89],
            "description": "SQL Injection vulnerability",
            "exploitability": "high",
            "proof_of_concept": "'; DROP TABLE users; --"
        },
        {
            "cwe_id": "CWE-798",
            "severity": "high", 
            "line_numbers": [12],
            "description": "Hard-coded database password",
            "exploitability": "medium"
        }
    ],
    "recommended_fixes": [
        {
            "vulnerability": "CWE-89",
            "fix": "Use parameterized queries",
            "code_snippet": "cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))",
            "research_backed": True,
            "papers": ["arxiv:2301.12345"]
        }
    ],
    "knowledge_graph_id": "security_analysis_123456"
}
```

## Key Points About This Orchestration

1. **Sequential Dependencies**: Each module builds on previous results
2. **Intelligent Routing**: Hub knows which module to call based on outputs
3. **Enrichment**: Each step adds more context and value
4. **Research Integration**: Combines security knowledge with academic research
5. **Persistent Knowledge**: Everything stored in graph for future learning

This shows how granger_hub acts as an intelligent orchestrator, not just passing messages but understanding the flow and making decisions about which modules to engage and how to combine their outputs.