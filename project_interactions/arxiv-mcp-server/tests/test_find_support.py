"""
Test module for arxiv-mcp-server find-support tool.

These tests validate GRANGER Task #002 requirements:
- Find supporting evidence for technique (Test 002.1)
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


class TestFindSupport:
    """Test suite for find-support capabilities."""
    
    @pytest.fixture
    def scenario(self, tmp_path):
        """Create a scenario with temporary cache."""
        scenario = ResearchDiscoveryScenario()
        scenario.cache_file = tmp_path / "arxiv_cache.json"
        return scenario
    
    def test_finds_evidence(self, scenario):
        """
        Test 002.1: Find supporting evidence for technique.
        Expected duration: 5.0s-15.0s
        """
        start_time = time.time()
        
        # Execute with real ArXiv API
        result = scenario.find_supporting_evidence(
            "multi-agent reinforcement learning",
            max_results=10
        )
        
        duration = time.time() - start_time
        
        # Assertions
        assert result.success, f"Finding support failed: {result.error}"
        assert 5.0 <= duration <= 15.0, f"Duration {duration}s outside expected range"
        
        # Validate output structure
        output = result.output_data
        assert "papers" in output
        assert "evidence_items" in output
        assert "total_found" in output
        assert "search_query" in output
        
        # Validate papers
        papers = output["papers"]
        assert len(papers) > 0, "No supporting papers found"
        assert len(papers) <= 5, "Should return top 5 papers"
        
        # Validate paper quality scores
        for paper in papers:
            assert "id" in paper
            assert "title" in paper
            assert "summary" in paper
            assert "quality_score" in paper
            assert 0.7 <= paper["quality_score"] <= 1.0, "Quality score out of range"
            assert "authors" in paper
            assert len(paper["authors"]) > 0
            assert "pdf_url" in paper
            
        # Validate evidence extraction
        evidence_items = output["evidence_items"]
        for evidence in evidence_items:
            assert "paper_id" in evidence
            assert "evidence_type" in evidence
            assert evidence["evidence_type"] == "support"
            assert "relevant_excerpts" in evidence
            assert len(evidence["relevant_excerpts"]) > 0
            assert "confidence" in evidence
            assert 0.5 <= evidence["confidence"] <= 1.0
        
        # Papers should be sorted by quality
        if len(papers) > 1:
            qualities = [p["quality_score"] for p in papers]
            assert qualities == sorted(qualities, reverse=True), "Papers not sorted by quality"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])