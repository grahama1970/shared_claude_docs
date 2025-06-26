"""
Document Comparison Scenario
Compare two documents and highlight differences
"""

from utils.scenario_base import ScenarioBase, Message

class DocumentComparisonScenario(ScenarioBase):
    """Compare two documents for differences"""
    
    def __init__(self):
        super().__init__(
            "Document Comparison",
            "Compare two versions of a document and find changes"
        )
        
    def setup_modules(self):
        return {
            "document_loader": {
                "description": "Loads multiple documents",
                "parameters": ["document_paths"],
                "output": ["documents", "load_status"]
            },
            "diff_analyzer": {
                "description": "Analyzes differences between documents",
                "parameters": ["doc1", "doc2", "comparison_type"],
                "output": ["differences", "similarity_score", "change_summary"]
            }
        }
    
    def create_workflow(self):
        return [
            Message(
                from_module="coordinator",
                to_module="document_loader",
                content={
                    "task": "load_multiple",
                    "document_paths": [
                        "contract_v1.pdf",
                        "contract_v2.pdf"
                    ],
                    "extract_text": True
                },
                metadata={"step": "load_documents"}
            ),
            Message(
                from_module="document_loader",
                to_module="diff_analyzer",
                content={
                    "task": "compare_documents",
                    "comparison_type": "detailed",
                    "highlight_changes": True,
                    "ignore_formatting": False
                },
                metadata={"step": "analyze_differences"}
            )
        ]
    
    def process_results(self, results):
        if len(results) > 0:
            load_result = results[0]
            self.results["documents_loaded"] = load_result["content"].get("load_status") == "success"
            
        if len(results) > 1:
            diff_result = results[1]
            self.results["differences_found"] = len(diff_result["content"].get("differences", []))
            self.results["similarity_score"] = diff_result["content"].get("similarity_score", 0)
            self.results["change_summary"] = diff_result["content"].get("change_summary", "")
