"""
Table Detection and Extraction Scenario
Detect tables in a document and extract them if confidence > 95%
"""

from utils.scenario_base import ScenarioBase, Message

class TableDetectionExtractionScenario(ScenarioBase):
    """Detect tables and conditionally extract based on confidence"""
    
    def __init__(self):
        super().__init__(
            "Table Detection and Extraction",
            "Detect tables in document and extract if confidence > 95%"
        )
        
    def setup_modules(self):
        return {
            "table_detector": {
                "description": "Detects tables in documents",
                "parameters": ["document_path", "page_range"],
                "output": ["tables_found", "confidence_scores", "locations"]
            },
            "marker_extractor": {
                "description": "Extracts tables using Marker tool",
                "parameters": ["document_path", "table_locations", "confidence_threshold"],
                "output": ["extracted_tables", "extraction_quality"]
            }
        }
    
    def create_workflow(self):
        return [
            Message(
                from_module="coordinator",
                to_module="table_detector",
                content={
                    "task": "detect_tables",
                    "document_path": "sample_document.pdf",
                    "page_range": "all",
                    "return_confidence": True
                },
                metadata={"step": "detect_tables"}
            ),
            Message(
                from_module="table_detector",
                to_module="marker_extractor",
                content={
                    "task": "extract_high_confidence_tables",
                    "confidence_threshold": 0.95,
                    "format": "markdown"
                },
                metadata={"step": "conditional_extraction"}
            )
        ]
    
    def process_results(self, results):
        detection_result = results[0] if results else None
        extraction_result = results[1] if len(results) > 1 else None
        
        if detection_result:
            self.results["tables_found"] = detection_result["content"].get("tables_found", 0)
            self.results["confidence_scores"] = detection_result["content"].get("confidence_scores", [])
            
        if extraction_result:
            self.results["extracted_tables"] = extraction_result["content"].get("extracted_tables", [])
            self.results["high_confidence_count"] = len([
                score for score in self.results.get("confidence_scores", [])
                if score > 0.95
            ])
