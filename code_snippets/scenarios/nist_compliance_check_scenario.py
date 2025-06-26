"""
NIST Compliance Check Scenario
Extract requirements with Marker and check against NIST controls from SPARTA
"""

from utils.scenario_base import ScenarioBase, Message

class NISTComplianceCheckScenario(ScenarioBase):
    """Extract requirements and validate against NIST security controls"""
    
    def __init__(self):
        super().__init__(
            "NIST Compliance Check",
            "Extract 'shall' requirements with Marker and validate against SPARTA NIST controls"
        )
        
    def setup_modules(self):
        return {
            "marker": {
                "description": "PDF extraction focusing on requirements",
                "parameters": ["pdf_path", "extract_patterns"],
                "output": ["requirements", "requirement_locations", "context"]
            },
            "sparta": {
                "description": "SPARTA security knowledge base with NIST controls",
                "parameters": ["control_family", "requirements_list"],
                "output": ["violations", "applicable_controls", "compliance_score"]
            },
            "requirement_parser": {
                "description": "Parses and categorizes requirements",
                "parameters": ["raw_requirements", "categorize"],
                "output": ["parsed_requirements", "categories", "security_relevant"]
            },
            "compliance_reporter": {
                "description": "Generates compliance reports",
                "parameters": ["requirements", "violations", "controls"],
                "output": ["compliance_report", "risk_assessment", "remediation_steps"]
            }
        }
    
    def create_workflow(self):
        return [
            # Step 1: Extract requirements from document
            Message(
                from_module="coordinator",
                to_module="marker",
                content={
                    "task": "extract_requirements",
                    "pdf_path": "system_requirements.pdf",
                    "extract_patterns": [
                        r"shall\s+[^.]+\.",
                        r"must\s+[^.]+\.",
                        r"required\s+to\s+[^.]+\."
                    ],
                    "include_context": True,
                    "context_window": 2  # sentences before/after
                },
                metadata={"step": 1, "description": "Extract all requirements"}
            ),
            
            # Step 2: Parse and categorize requirements
            Message(
                from_module="marker",
                to_module="requirement_parser",
                content={
                    "task": "parse_requirements",
                    "categorize": True,
                    "identify_security_relevant": True,
                    "extract_entities": True
                },
                metadata={"step": 2, "description": "Parse and categorize"}
            ),
            
            # Step 3: Check against NIST controls
            Message(
                from_module="requirement_parser",
                to_module="sparta",
                content={
                    "task": "validate_nist_compliance",
                    "control_families": [
                        "AC",  # Access Control
                        "AU",  # Audit and Accountability
                        "SC",  # System and Communications Protection
                        "SI"   # System and Information Integrity
                    ],
                    "check_mode": "comprehensive",
                    "include_overlays": ["space_systems", "critical_infrastructure"]
                },
                metadata={"step": 3, "description": "Check NIST compliance"}
            ),
            
            # Step 4: Generate compliance report
            Message(
                from_module="sparta",
                to_module="compliance_reporter",
                content={
                    "task": "generate_compliance_report",
                    "report_format": "detailed",
                    "include_risk_matrix": True,
                    "generate_remediation_plan": True,
                    "prioritize_by_severity": True
                },
                metadata={"step": 4, "description": "Generate compliance report"}
            )
        ]
    
    def process_results(self, results):
        self.results["workflow_complete"] = len(results) == 4
        
        if len(results) > 0:
            extract_result = results[0]["content"]
            self.results["requirements_found"] = len(extract_result.get("requirements", []))
            self.results["extraction_success"] = extract_result.get("requirements") is not None
            
        if len(results) > 1:
            parse_result = results[1]["content"]
            self.results["security_requirements"] = len(parse_result.get("security_relevant", []))
            self.results["requirement_categories"] = parse_result.get("categories", [])
            
        if len(results) > 2:
            sparta_result = results[2]["content"]
            self.results["violations_found"] = len(sparta_result.get("violations", []))
            self.results["compliance_score"] = sparta_result.get("compliance_score", 0)
            self.results["applicable_controls"] = sparta_result.get("applicable_controls", [])
            
        if len(results) > 3:
            report_result = results[3]["content"]
            self.results["report_generated"] = report_result.get("compliance_report") is not None
            self.results["high_risk_items"] = len([
                r for r in report_result.get("risk_assessment", [])
                if r.get("severity") == "high"
            ])
