"""
Scientific Paper Validation Scenario
Extract PDF with Marker and find papers that support AND refute it using ArXiv
"""

from utils.scenario_base import ScenarioBase, Message

class ScientificPaperValidationScenario(ScenarioBase):
    """Extract research paper and find supporting/refuting evidence"""
    
    def __init__(self):
        super().__init__(
            "Scientific Paper Validation",
            "Extract PDF with Marker and find supporting AND refuting papers via ArXiv"
        )
        
    def setup_modules(self):
        return {
            "marker": {
                "description": "Advanced PDF extraction with section hierarchy",
                "parameters": ["pdf_path", "extract_citations", "extract_claims"],
                "output": ["sections", "claims", "citations", "methodology"]
            },
            "arxiv_bot": {
                "description": "ArXiv paper search and analysis",
                "parameters": ["search_queries", "find_supporting", "find_refuting"],
                "output": ["supporting_papers", "refuting_papers", "confidence_scores"]
            },
            "claim_analyzer": {
                "description": "Analyzes scientific claims for validation",
                "parameters": ["claims", "methodology"],
                "output": ["key_claims", "testable_hypotheses", "search_queries"]
            },
            "evidence_synthesizer": {
                "description": "Synthesizes supporting and refuting evidence",
                "parameters": ["original_paper", "supporting", "refuting"],
                "output": ["validation_report", "controversy_score", "consensus_level"]
            }
        }
    
    def create_workflow(self):
        return [
            # Step 1: Extract the PDF
            Message(
                from_module="coordinator",
                to_module="marker",
                content={
                    "task": "extract_scientific_paper",
                    "pdf_path": "research_paper.pdf",
                    "extract_citations": True,
                    "extract_claims": True,
                    "preserve_equations": True,
                    "extract_figures": True
                },
                metadata={"step": 1, "description": "Extract paper content and structure"}
            ),
            
            # Step 2: Analyze claims
            Message(
                from_module="marker",
                to_module="claim_analyzer",
                content={
                    "task": "identify_key_claims",
                    "extract_hypotheses": True,
                    "generate_search_queries": True
                },
                metadata={"step": 2, "description": "Analyze scientific claims"}
            ),
            
            # Step 3: Search for supporting papers
            Message(
                from_module="claim_analyzer",
                to_module="arxiv_bot",
                content={
                    "task": "find_related_papers",
                    "search_mode": "supporting",
                    "max_papers": 10,
                    "date_range": "last_5_years",
                    "categories": ["cs.AI", "cs.LG", "stat.ML"]
                },
                metadata={"step": 3, "description": "Find supporting evidence"}
            ),
            
            # Step 4: Search for refuting papers
            Message(
                from_module="claim_analyzer",
                to_module="arxiv_bot",
                content={
                    "task": "find_related_papers",
                    "search_mode": "refuting",
                    "include_contradictions": True,
                    "max_papers": 10
                },
                metadata={"step": 4, "description": "Find refuting evidence"}
            ),
            
            # Step 5: Synthesize validation report
            Message(
                from_module="arxiv_bot",
                to_module="evidence_synthesizer",
                content={
                    "task": "create_validation_report",
                    "include_controversy_analysis": True,
                    "calculate_consensus_score": True,
                    "generate_recommendations": True
                },
                metadata={"step": 5, "description": "Synthesize validation report"}
            )
        ]
    
    def process_results(self, results):
        self.results["steps_completed"] = len(results)
        
        if len(results) > 0:
            self.results["paper_extracted"] = True
            self.results["sections_found"] = results[0]["content"].get("sections", [])
            
        if len(results) > 1:
            self.results["claims_analyzed"] = True
            self.results["key_claims"] = results[1]["content"].get("key_claims", [])
            
        if len(results) > 2:
            self.results["supporting_papers"] = results[2]["content"].get("supporting_papers", [])
            
        if len(results) > 3:
            self.results["refuting_papers"] = results[3]["content"].get("refuting_papers", [])
            
        if len(results) > 4:
            self.results["validation_complete"] = True
            self.results["controversy_score"] = results[4]["content"].get("controversy_score", 0)
            self.results["consensus_level"] = results[4]["content"].get("consensus_level", "unknown")
