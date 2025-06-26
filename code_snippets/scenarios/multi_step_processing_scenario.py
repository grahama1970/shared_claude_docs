"""
Multi-Step Document Processing Scenario
Navigate to page, screenshot, detect tables, extract if found
"""

from utils.scenario_base import ScenarioBase, Message

class MultiStepProcessingScenario(ScenarioBase):
    """Complete workflow: navigate, screenshot, detect, extract"""
    
    def __init__(self):
        super().__init__(
            "Multi-Step Document Processing",
            "Navigate to page 40, screenshot, detect tables, extract if confidence > 95%"
        )
        
    def setup_modules(self):
        return {
            "pdf_navigator": {
                "description": "Navigates PDF pages and screenshots",
                "parameters": ["pdf_path", "page_number"],
                "output": ["screenshot_path", "page_content"]
            },
            "table_detector": {
                "description": "Detects tables in screenshots",
                "parameters": ["image_path"],
                "output": ["has_tables", "table_regions", "confidence"]
            },
            "marker_extractor": {
                "description": "Extracts tables with Marker",
                "parameters": ["pdf_path", "page_number", "regions"],
                "output": ["table_data", "extraction_quality"]
            },
            "decision_maker": {
                "description": "Makes extraction decision based on confidence",
                "parameters": ["confidence", "threshold"],
                "output": ["should_extract", "reason"]
            }
        }
    
    def create_workflow(self):
        return [
            # Step 1: Navigate and screenshot
            Message(
                from_module="coordinator",
                to_module="pdf_navigator",
                content={
                    "task": "navigate_and_screenshot",
                    "pdf_path": "sample_document.pdf",
                    "page_number": 40
                },
                metadata={"step": 1, "description": "Navigate to page 40"}
            ),
            
            # Step 2: Detect tables in screenshot
            Message(
                from_module="pdf_navigator",
                to_module="table_detector",
                content={
                    "task": "detect_tables_in_screenshot",
                    "analyze_layout": True
                },
                metadata={"step": 2, "description": "Detect tables"}
            ),
            
            # Step 3: Decision on extraction
            Message(
                from_module="table_detector",
                to_module="decision_maker",
                content={
                    "task": "evaluate_extraction",
                    "threshold": 0.95
                },
                metadata={"step": 3, "description": "Decide on extraction"}
            ),
            
            # Step 4: Conditional extraction
            Message(
                from_module="decision_maker",
                to_module="marker_extractor",
                content={
                    "task": "extract_if_approved",
                    "output_format": "markdown"
                },
                metadata={"step": 4, "description": "Extract tables", "conditional": True}
            )
        ]
    
    def process_results(self, results):
        self.results["steps_completed"] = len(results)
        
        # Navigation results
        if len(results) > 0:
            nav_result = results[0]
            self.results["screenshot_taken"] = nav_result["content"].get("screenshot_path") is not None
            self.results["page_number"] = 40
        
        # Detection results
        if len(results) > 1:
            detect_result = results[1]
            self.results["tables_detected"] = detect_result["content"].get("has_tables", False)
            self.results["detection_confidence"] = detect_result["content"].get("confidence", 0)
        
        # Decision results
        if len(results) > 2:
            decision_result = results[2]
            self.results["extraction_approved"] = decision_result["content"].get("should_extract", False)
            self.results["decision_reason"] = decision_result["content"].get("reason", "")
        
        # Extraction results
        if len(results) > 3:
            extract_result = results[3]
            self.results["tables_extracted"] = extract_result["content"].get("table_data") is not None
            self.results["extraction_quality"] = extract_result["content"].get("extraction_quality", "N/A")
