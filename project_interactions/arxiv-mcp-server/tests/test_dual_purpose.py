"""
Test module for arxiv-mcp-server dual-purpose research.

These tests validate GRANGER Task #002 requirements:
- Dual-purpose research benefits (Test 002.3)
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


class TestDualPurpose:
    """Test suite for dual-purpose research capabilities."""
    
    @pytest.fixture
    def scenario(self, tmp_path):
        """Create a scenario with temporary cache."""
        scenario = ResearchDiscoveryScenario()
        scenario.cache_file = tmp_path / "arxiv_cache.json"
        return scenario
    
    def test_benefits_both(self, scenario):
        """
        Test 002.3: Dual-purpose research benefits.
        Expected duration: 1.0s-5.0s (shorter because it's a focused search)
        """
        start_time = time.time()
        
        # Execute dual-purpose research
        result = scenario.dual_purpose_research(
            granger_need="multi-agent coordination optimization",
            client_need="distributed system fault tolerance"
        )
        
        duration = time.time() - start_time
        
        # Assertions
        assert result.success or result.error == "No dual-purpose research found", \
            f"Unexpected error: {result.error}"
        assert 1.0 <= duration <= 15.0, f"Duration {duration}s outside expected range"
        
        # Validate output structure
        output = result.output_data
        assert "dual_purpose_papers" in output
        assert "granger_benefits" in output
        assert "client_benefits" in output
        assert "overlap_strength" in output
        assert "recommendation" in output
        
        # If dual-purpose papers found
        if result.success:
            papers = output["dual_purpose_papers"]
            assert isinstance(papers, list)
            
            if papers:
                assert len(papers) <= 5, "Should return top 5 dual-purpose papers"
                
                for paper in papers:
                    assert "id" in paper
                    assert "title" in paper
                    assert "granger_relevance" in paper
                    assert "client_relevance" in paper
                    assert "dual_purpose_score" in paper
                    
                    # Both relevance scores should be above threshold
                    assert paper["granger_relevance"] >= 0.6
                    assert paper["client_relevance"] >= 0.6
                    
                    # Dual-purpose score should be average
                    expected_score = (paper["granger_relevance"] + paper["client_relevance"]) / 2
                    assert abs(paper["dual_purpose_score"] - expected_score) < 0.01
                
                # Papers should be sorted by dual-purpose score
                if len(papers) > 1:
                    scores = [p["dual_purpose_score"] for p in papers]
                    assert scores == sorted(scores, reverse=True)
            
            # Validate benefits
            granger_benefits = output["granger_benefits"]
            client_benefits = output["client_benefits"]
            
            for benefit in granger_benefits:
                assert "system" in benefit
                assert benefit["system"] == "GRANGER"
                assert "need" in benefit
                assert "paper_id" in benefit
                assert "benefits" in benefit
                assert "confidence" in benefit
                assert 0.5 <= benefit["confidence"] <= 1.0
            
            for benefit in client_benefits:
                assert "system" in benefit
                assert benefit["system"] == "Client"
                assert "need" in benefit
                assert "paper_id" in benefit
                assert "benefits" in benefit
                assert "confidence" in benefit
                assert 0.5 <= benefit["confidence"] <= 1.0
        
        # Validate recommendation
        recommendation = output["recommendation"]
        assert "action" in recommendation
        assert "confidence" in recommendation
        assert 0.0 <= recommendation["confidence"] <= 1.0
        
        if result.success and papers:
            assert recommendation["action"] == "implement_dual_purpose"
            assert "expected_granger_improvement" in recommendation
            assert "expected_client_improvement" in recommendation
            assert "implementation_priority" in recommendation
        else:
            assert recommendation["action"] == "continue_separate_research"
            assert "reason" in recommendation
        
        # Overlap strength should reflect findings
        overlap = output["overlap_strength"]
        assert 0.0 <= overlap <= 1.0
        if result.success and len(papers) > 3:
            assert overlap > 0.15, "Good overlap should be reflected in strength"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])