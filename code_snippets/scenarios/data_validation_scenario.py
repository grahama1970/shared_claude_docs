"""
Data Validation Scenario
Validate extracted data against rules
"""

from utils.scenario_base import ScenarioBase, Message

class DataValidationScenario(ScenarioBase):
    """Validate extracted data meets specific criteria"""
    
    def __init__(self):
        super().__init__(
            "Data Validation",
            "Extract data and validate against business rules"
        )
        
    def setup_modules(self):
        return {
            "data_extractor": {
                "description": "Extracts structured data",
                "parameters": ["source_path", "data_type"],
                "output": ["extracted_data", "extraction_metadata"]
            },
            "validator": {
                "description": "Validates data against rules",
                "parameters": ["data", "validation_rules"],
                "output": ["is_valid", "validation_errors", "validation_report"]
            }
        }
    
    def create_workflow(self):
        return [
            Message(
                from_module="coordinator",
                to_module="data_extractor",
                content={
                    "task": "extract_form_data",
                    "source_path": "application_form.pdf",
                    "data_type": "form_fields",
                    "include_metadata": True
                },
                metadata={"step": "extract_data"}
            ),
            Message(
                from_module="data_extractor",
                to_module="validator",
                content={
                    "task": "validate_form_data",
                    "validation_rules": {
                        "required_fields": ["name", "email", "phone", "date"],
                        "email_format": True,
                        "phone_format": "US",
                        "date_range": {"min": "2024-01-01", "max": "2025-12-31"},
                        "field_lengths": {"name": {"min": 2, "max": 100}}
                    },
                    "generate_report": True
                },
                metadata={"step": "validate_data"}
            )
        ]
    
    def process_results(self, results):
        if len(results) > 0:
            extract_result = results[0]
            self.results["data_extracted"] = extract_result["content"].get("extracted_data") is not None
            self.results["field_count"] = len(extract_result["content"].get("extracted_data", {}))
            
        if len(results) > 1:
            validation_result = results[1]
            self.results["is_valid"] = validation_result["content"].get("is_valid", False)
            self.results["error_count"] = len(validation_result["content"].get("validation_errors", []))
            self.results["validation_report"] = validation_result["content"].get("validation_report", "")
