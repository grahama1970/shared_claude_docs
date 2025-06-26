"""
Document Q&A Scenario
Load a document and answer specific questions about it
"""

from utils.scenario_base import ScenarioBase, Message

class DocumentQAScenario(ScenarioBase):
    """Simple question answering about a document"""
    
    def __init__(self):
        super().__init__(
            "Document Q&A",
            "Load document and answer questions about its content"
        )
        
    def setup_modules(self):
        return {
            "document_loader": {
                "description": "Loads and parses documents",
                "parameters": ["document_path", "extract_text"],
                "output": ["text_content", "metadata", "page_count"]
            },
            "qa_engine": {
                "description": "Answers questions about document content",
                "parameters": ["document_text", "questions"],
                "output": ["answers", "confidence_scores", "relevant_sections"]
            }
        }
    
    def create_workflow(self):
        return [
            Message(
                from_module="coordinator",
                to_module="document_loader",
                content={
                    "task": "load_document",
                    "document_path": "research_paper.pdf",
                    "extract_text": True,
                    "preserve_formatting": False
                },
                metadata={"step": "load_document"}
            ),
            Message(
                from_module="document_loader",
                to_module="qa_engine",
                content={
                    "task": "answer_questions",
                    "questions": [
                        "What is the main hypothesis?",
                        "What methodology was used?",
                        "What were the key findings?",
                        "Are there any limitations mentioned?"
                    ],
                    "return_sources": True
                },
                metadata={"step": "answer_questions"}
            )
        ]
    
    def process_results(self, results):
        if results:
            # Document loading results
            if len(results) > 0:
                doc_result = results[0]
                self.results["page_count"] = doc_result["content"].get("page_count", 0)
                self.results["document_loaded"] = doc_result["content"].get("text_content") is not None
            
            # Q&A results
            if len(results) > 1:
                qa_result = results[1]
                self.results["answers"] = qa_result["content"].get("answers", [])
                self.results["confidence_scores"] = qa_result["content"].get("confidence_scores", [])
                self.results["relevant_sections"] = qa_result["content"].get("relevant_sections", [])
