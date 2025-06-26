"""
PDF Page Screenshot Scenario
Simple scenario: Navigate to page 40 of a PDF and take a screenshot
"""

from utils.scenario_base import ScenarioBase, Message

class PDFPageScreenshotScenario(ScenarioBase):
    """Navigate to a specific page in a PDF and take a screenshot"""
    
    def __init__(self):
        super().__init__(
            "PDF Page Screenshot",
            "Navigate to page 40 of a PDF and capture a screenshot"
        )
        
    def setup_modules(self):
        return {
            "pdf_navigator": {
                "description": "Navigates to specific pages in PDF documents",
                "parameters": ["pdf_path", "page_number"],
                "output": ["screenshot_path", "page_info"]
            }
        }
    
    def create_workflow(self):
        return [
            Message(
                from_module="coordinator",
                to_module="pdf_navigator",
                content={
                    "task": "navigate_and_screenshot",
                    "pdf_path": "sample_document.pdf",
                    "page_number": 40,
                    "output_format": "png"
                },
                metadata={"step": "navigate_to_page"}
            )
        ]
    
    def process_results(self, results):
        if results:
            nav_result = results[0]
            self.results["screenshot_path"] = nav_result["content"].get("screenshot_path")
            self.results["page_info"] = nav_result["content"].get("page_info")
            self.results["success"] = nav_result["content"].get("success", False)
