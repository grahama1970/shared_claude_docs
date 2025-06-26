"""
Information Extraction Scenario
Extract specific information like dates, names, amounts from documents
"""

from utils.scenario_base import ScenarioBase, Message

class InfoExtractionScenario(ScenarioBase):
    """Extract structured information from documents"""
    
    def __init__(self):
        super().__init__(
            "Information Extraction",
            "Extract dates, names, amounts, and key terms from document"
        )
        
    def setup_modules(self):
        return {
            "text_extractor": {
                "description": "Extracts text from documents",
                "parameters": ["document_path"],
                "output": ["full_text", "page_texts"]
            },
            "entity_extractor": {
                "description": "Extracts named entities",
                "parameters": ["text", "entity_types"],
                "output": ["entities", "entity_counts"]
            },
            "data_formatter": {
                "description": "Formats extracted data",
                "parameters": ["entities", "format_type"],
                "output": ["formatted_data", "summary"]
            }
        }
    
    def create_workflow(self):
        return [
            Message(
                from_module="coordinator",
                to_module="text_extractor",
                content={
                    "task": "extract_text",
                    "document_path": "invoice.pdf",
                    "clean_text": True
                },
                metadata={"step": "extract_text"}
            ),
            Message(
                from_module="text_extractor",
                to_module="entity_extractor",
                content={
                    "task": "extract_entities",
                    "entity_types": [
                        "dates",
                        "person_names",
                        "company_names",
                        "monetary_amounts",
                        "invoice_numbers",
                        "addresses"
                    ],
                    "return_positions": True
                },
                metadata={"step": "extract_entities"}
            ),
            Message(
                from_module="entity_extractor",
                to_module="data_formatter",
                content={
                    "task": "format_extraction_results",
                    "format_type": "structured_json",
                    "include_summary": True
                },
                metadata={"step": "format_results"}
            )
        ]
    
    def process_results(self, results):
        if len(results) > 0:
            text_result = results[0]
            self.results["text_extracted"] = text_result["content"].get("full_text") is not None
        
        if len(results) > 1:
            entity_result = results[1]
            entities = entity_result["content"].get("entities", {})
            self.results["dates_found"] = len(entities.get("dates", []))
            self.results["amounts_found"] = len(entities.get("monetary_amounts", []))
            self.results["names_found"] = len(entities.get("person_names", [])) + len(entities.get("company_names", []))
            
        if len(results) > 2:
            format_result = results[2]
            self.results["formatted_data"] = format_result["content"].get("formatted_data")
            self.results["extraction_summary"] = format_result["content"].get("summary")
