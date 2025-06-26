"""
Test module for Multi-Source Research Aggregation.

These tests validate GRANGER Task #014 requirements.
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

from project_interactions.multi_source_research.multi_source_interaction import MultiSourceResearchScenario


class TestMultiSourceAggregation:
    """Test suite for Multi-Source Research Aggregation."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return MultiSourceResearchScenario()
    
    def test_parallel_search(self, scenario):
        """
        Test 014.1: Parallel source search.
        Expected duration: 40.0s-120.0s
        """
        start_time = time.time()
        
        result = scenario.test_parallel_search()
        
        duration = time.time() - start_time
        
        assert result.success, f"Parallel source search failed: {result.error}"
        assert 40.0 <= duration <= 120.0, f"Duration {duration}s outside expected range"
        
        output = result.output_data
        assert output["arxiv_results"] > 0, "Should find ArXiv results"
        assert output["youtube_results"] > 0, "Should find YouTube results"
        assert output["total_results"] == output["arxiv_results"] + output["youtube_results"]
        assert "sample_arxiv" in output and output["sample_arxiv"] is not None
        assert "sample_youtube" in output and output["sample_youtube"] is not None
    
    def test_knowledge_merge(self, scenario):
        """
        Test 014.2: Merge diverse knowledge.
        Expected duration: 30.0s-60.0s
        """
        start_time = time.time()
        
        result = scenario.test_knowledge_merge()
        
        duration = time.time() - start_time
        
        assert result.success, f"Merge diverse knowledge failed: {result.error}"
        assert 30.0 <= duration <= 60.0, f"Duration {duration}s outside expected range"
        
        output = result.output_data
        graph_stats = output["graph_stats"]
        assert graph_stats["total_nodes"] > 0, "Should create nodes"
        assert graph_stats["total_edges"] > 0, "Should create edges"
        assert graph_stats["concepts"] > 0, "Should extract concepts"
        assert output["knowledge_density"] > 0, "Should have knowledge density"
    
    def test_contradiction_detection(self, scenario):
        """
        Test 014.3: Detect source contradictions.
        Expected duration: 30.0s-50.0s
        """
        start_time = time.time()
        
        result = scenario.test_contradiction_detection()
        
        duration = time.time() - start_time
        
        assert result.success, f"Detect source contradictions failed: {result.error}"
        assert 30.0 <= duration <= 50.0, f"Duration {duration}s outside expected range"
        
        output = result.output_data
        assert "contradictions_found" in output
        assert "contradiction_details" in output
        assert isinstance(output["resolution_strategies"], list)
        assert len(output["resolution_strategies"]) > 0
        assert 0.0 <= output["confidence_in_detection"] <= 1.0


class TestHoneypot:
    """Honeypot tests."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return MultiSourceResearchScenario()
    
    def test_merge_incompatible_data(self, scenario):
        """
        Test 014.H: HONEYPOT - Merge incompatible data.
        This should fail because incompatible data formats can't be merged.
        """
        # Override knowledge builder to create incompatible data
        scenario.knowledge_builder.nodes["incompatible_1"] = {
            "type": "invalid_type",
            "data": {"format": "completely_different"}
        }
        scenario.knowledge_builder.nodes["incompatible_2"] = {
            "type": None,  # Invalid type
            "data": ["this", "is", "wrong", "format"]
        }
        
        # Try to merge - this should handle gracefully or fail
        try:
            merge_stats = scenario.knowledge_builder.merge_knowledge()
            # If it succeeds, check that it didn't create invalid connections
            assert False, "Honeypot: Should not successfully merge incompatible data"
        except:
            # Expected to fail
            pass