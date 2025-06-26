"""
CWE Security Analysis Scenario
Check if code violates any CWEs from SPARTA's MITRE database
"""

from utils.scenario_base import ScenarioBase, Message

class CWESecurityAnalysisScenario(ScenarioBase):
    """Analyze code for CWE violations using SPARTA's security knowledge"""
    
    def __init__(self):
        super().__init__(
            "CWE Security Analysis",
            "Analyze code against MITRE CWE database from SPARTA"
        )
        
    def setup_modules(self):
        return {
            "code_parser": {
                "description": "Parses and analyzes source code",
                "parameters": ["code_path", "language", "parse_depth"],
                "output": ["ast", "code_patterns", "function_calls", "data_flows"]
            },
            "sparta": {
                "description": "SPARTA with MITRE CWE database",
                "parameters": ["cwe_categories", "code_patterns"],
                "output": ["cwe_violations", "severity_scores", "exploitation_likelihood"]
            },
            "vulnerability_analyzer": {
                "description": "Deep vulnerability analysis",
                "parameters": ["code_ast", "cwe_rules"],
                "output": ["vulnerabilities", "attack_vectors", "proof_of_concepts"]
            },
            "remediation_engine": {
                "description": "Suggests fixes for vulnerabilities",
                "parameters": ["vulnerabilities", "code_context"],
                "output": ["fixes", "secure_patterns", "implementation_guide"]
            }
        }
    
    def create_workflow(self):
        return [
            # Step 1: Parse the code
            Message(
                from_module="coordinator",
                to_module="code_parser",
                content={
                    "task": "parse_code",
                    "code_path": "src/authentication.py",
                    "language": "python",
                    "parse_depth": "comprehensive",
                    "extract_patterns": [
                        "input_validation",
                        "authentication_flows",
                        "cryptographic_operations",
                        "sql_queries",
                        "file_operations",
                        "network_requests"
                    ]
                },
                metadata={"step": 1, "description": "Parse source code"}
            ),
            
            # Step 2: Check against CWE database
            Message(
                from_module="code_parser",
                to_module="sparta",
                content={
                    "task": "check_cwe_violations",
                    "cwe_categories": [
                        "CWE-20",   # Improper Input Validation
                        "CWE-79",   # Cross-site Scripting
                        "CWE-89",   # SQL Injection
                        "CWE-200",  # Information Exposure
                        "CWE-287",  # Improper Authentication
                        "CWE-327",  # Broken Crypto
                        "CWE-798"   # Hard-coded Credentials
                    ],
                    "check_mode": "exhaustive",
                    "include_variants": True
                },
                metadata={"step": 2, "description": "Check CWE violations"}
            ),
            
            # Step 3: Deep vulnerability analysis
            Message(
                from_module="sparta",
                to_module="vulnerability_analyzer",
                content={
                    "task": "analyze_vulnerabilities",
                    "generate_poc": True,
                    "check_exploitability": True,
                    "simulate_attacks": True,
                    "owasp_mapping": True
                },
                metadata={"step": 3, "description": "Analyze vulnerabilities"}
            ),
            
            # Step 4: Generate remediation plan
            Message(
                from_module="vulnerability_analyzer",
                to_module="remediation_engine",
                content={
                    "task": "generate_fixes",
                    "fix_priority": "severity",
                    "include_code_snippets": True,
                    "validate_fixes": True,
                    "generate_tests": True
                },
                metadata={"step": 4, "description": "Generate remediation"}
            )
        ]
    
    def process_results(self, results):
        self.results["analysis_complete"] = len(results) == 4
        
        if len(results) > 0:
            parse_result = results[0]["content"]
            self.results["code_parsed"] = parse_result.get("ast") is not None
            self.results["patterns_found"] = len(parse_result.get("code_patterns", []))
            
        if len(results) > 1:
            cwe_result = results[1]["content"]
            violations = cwe_result.get("cwe_violations", [])
            self.results["cwe_violations"] = len(violations)
            self.results["critical_violations"] = len([
                v for v in violations 
                if v.get("severity") in ["critical", "high"]
            ])
            
        if len(results) > 2:
            vuln_result = results[2]["content"]
            self.results["exploitable_vulns"] = len([
                v for v in vuln_result.get("vulnerabilities", [])
                if v.get("exploitability") == "high"
            ])
            self.results["attack_vectors"] = vuln_result.get("attack_vectors", [])
            
        if len(results) > 3:
            fix_result = results[3]["content"]
            self.results["fixes_generated"] = len(fix_result.get("fixes", []))
            self.results["secure_patterns"] = fix_result.get("secure_patterns", [])
