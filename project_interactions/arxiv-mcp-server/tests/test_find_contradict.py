"""
Test module for arxiv-mcp-server find-contradict tool.

These tests validate GRANGER Task #002 requirements:
- Find contradicting research (Test 002.2)
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
import time
from pathlib import Path

from research_discovery_interaction import ResearchDiscoveryScenario


class TestFindContradict:
    """Test suite for find-contradict capabilities."""
    
    @pytest.fixture
    def scenario(self, tmp_path):
        """Create a scenario with temporary cache."""
        scenario = ResearchDiscoveryScenario()
        scenario.cache_file = tmp_path / "arxiv_cache.json"
        return scenario
    
    def test_finds_contradictions(self, scenario):
        """
        Test 002.2: Find contradicting research.
        Expected duration: 5.0s-15.0s
        """
        start_time = time.time()
        
        # Execute with real ArXiv API
        result = scenario.find_contradicting_research(
            "transformer architectures",
            max_results=10
        )
        
        duration = time.time() - start_time
        
        # Assertions
        assert result.success, f"Finding contradictions failed: {result.error}"
        assert 5.0 <= duration <= 15.0, f"Duration {duration}s outside expected range"
        
        # Validate output structure
        output = result.output_data
        assert "papers" in output
        assert "contradictions" in output
        assert "total_found" in output
        assert "confidence_in_technique" in output
        
        # Success even if no contradictions found (that's useful info)
        papers = output["papers"]
        assert isinstance(papers, list)
        
        # If contradictions found, validate them
        if papers:
            assert len(papers) <= 5, "Should return top 5 contradictions"
            
            for paper in papers:
                assert "id" in paper
                assert "title" in paper
                assert "summary" in paper
                assert "contradiction_score" in paper
                assert 0.6 <= paper["contradiction_score"] <= 1.0
                assert "authors" in paper
                assert "pdf_url" in paper
            
            # Papers should be sorted by contradiction score
            if len(papers) > 1:
                scores = [p["contradiction_score"] for p in papers]
                assert scores == sorted(scores, reverse=True), "Papers not sorted by contradiction score"
        
        # Validate contradiction evidence
        contradictions = output["contradictions"]
        for evidence in contradictions:
            assert "paper_id" in evidence
            assert "evidence_type" in evidence
            assert evidence["evidence_type"] == "contradict"
            assert "relevant_excerpts" in evidence
            assert "confidence" in evidence
            assert 0.5 <= evidence["confidence"] <= 1.0
        
        # Confidence in technique should be calculated
        confidence = output["confidence_in_technique"]
        assert 0.0 <= confidence <= 1.0
        
        # More contradictions should lower confidence
        if len(papers) > 5:
            assert confidence < 0.5, "High contradictions should lower confidence"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])