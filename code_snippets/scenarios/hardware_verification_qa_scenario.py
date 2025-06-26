"""
Hardware Verification Q&A Scenario
Extract tables with Marker and answer hardware verification questions
"""

from utils.scenario_base import ScenarioBase, Message

class HardwareVerificationQAScenario(ScenarioBase):
    """Extract hardware specs and answer verification questions"""
    
    def __init__(self):
        super().__init__(
            "Hardware Verification Q&A",
            "Extract PDF tables with Marker and answer hardware verification questions"
        )
        
    def setup_modules(self):
        return {
            "marker": {
                "description": "Advanced PDF extraction with table recognition",
                "parameters": ["pdf_path", "focus_tables", "preserve_formatting"],
                "output": ["tables", "table_metadata", "surrounding_text"]
            },
            "table_processor": {
                "description": "Processes and structures table data",
                "parameters": ["raw_tables", "table_type"],
                "output": ["structured_data", "column_types", "relationships"]
            },
            "hardware_knowledge_base": {
                "description": "Hardware verification rules and standards",
                "parameters": ["component_type", "verification_standard"],
                "output": ["verification_rules", "test_criteria", "compliance_thresholds"]
            },
            "verification_engine": {
                "description": "Answers hardware verification questions",
                "parameters": ["specs_data", "questions", "standards"],
                "output": ["answers", "verification_status", "discrepancies", "recommendations"]
            }
        }
    
    def create_workflow(self):
        return [
            # Step 1: Extract tables from hardware spec document
            Message(
                from_module="coordinator",
                to_module="marker",
                content={
                    "task": "extract_hardware_tables",
                    "pdf_path": "hardware_specification.pdf",
                    "focus_tables": True,
                    "preserve_formatting": True,
                    "extract_units": True,
                    "table_detection_mode": "aggressive",
                    "merge_split_tables": True
                },
                metadata={"step": 1, "description": "Extract specification tables"}
            ),
            
            # Step 2: Process and structure tables
            Message(
                from_module="marker",
                to_module="table_processor",
                content={
                    "task": "process_hardware_tables",
                    "table_type": "hardware_specifications",
                    "identify_parameters": True,
                    "extract_ranges": True,
                    "normalize_units": True,
                    "link_related_tables": True
                },
                metadata={"step": 2, "description": "Structure table data"}
            ),
            
            # Step 3: Load verification standards
            Message(
                from_module="table_processor",
                to_module="hardware_knowledge_base",
                content={
                    "task": "load_verification_standards",
                    "component_types": ["auto_detect"],
                    "standards": [
                        "IEEE_1149.1",  # JTAG
                        "JEDEC",        # Memory standards
                        "PCIe_5.0",     # Interface standards
                        "USB4",         # Connectivity
                        "MIL-STD-883"   # Military standards
                    ],
                    "include_test_procedures": True
                },
                metadata={"step": 3, "description": "Load verification standards"}
            ),
            
            # Step 4: Answer verification questions
            Message(
                from_module="hardware_knowledge_base",
                to_module="verification_engine",
                content={
                    "task": "answer_verification_questions",
                    "questions": [
                        "Does the power consumption meet the specified TDP limits?",
                        "Are all timing parameters within JEDEC specifications?",
                        "Do the signal integrity measurements pass PCIe 5.0 requirements?",
                        "What is the maximum operating frequency and is it within spec?",
                        "Are there any thermal violations under worst-case conditions?",
                        "Do the ESD protection levels meet industry standards?",
                        "Which components require additional verification testing?"
                    ],
                    "verification_depth": "comprehensive",
                    "cross_reference_tables": True,
                    "generate_test_plan": True
                },
                metadata={"step": 4, "description": "Answer verification questions"}
            )
        ]
    
    def process_results(self, results):
        self.results["workflow_stages"] = len(results)
        
        if len(results) > 0:
            table_result = results[0]["content"]
            self.results["tables_extracted"] = len(table_result.get("tables", []))
            self.results["extraction_quality"] = table_result.get("table_metadata", {}).get("quality_score", 0)
            
        if len(results) > 1:
            process_result = results[1]["content"]
            self.results["parameters_identified"] = len(process_result.get("structured_data", {}).get("parameters", []))
            self.results["data_structured"] = process_result.get("structured_data") is not None
            
        if len(results) > 2:
            standards_result = results[2]["content"]
            self.results["standards_loaded"] = len(standards_result.get("verification_rules", []))
            self.results["test_criteria"] = len(standards_result.get("test_criteria", []))
            
        if len(results) > 3:
            verification_result = results[3]["content"]
            answers = verification_result.get("answers", [])
            self.results["questions_answered"] = len(answers)
            self.results["verification_passed"] = verification_result.get("verification_status") == "PASS"
            self.results["discrepancies_found"] = len(verification_result.get("discrepancies", []))
            self.results["critical_issues"] = len([
                d for d in verification_result.get("discrepancies", [])
                if d.get("severity") == "critical"
            ])
