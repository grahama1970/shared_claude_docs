"""
Test module for youtube-transcripts progressive search.

These tests validate GRANGER Task #003 requirements:
- Progressive search expansion (Test 003.3)
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

from technical_content_mining_interaction import TechnicalContentMiningScenario


class TestProgressiveSearch:
    """Test suite for progressive search expansion."""
    
    @pytest.fixture
    def scenario(self, tmp_path):
        """Create a scenario with temporary cache."""
        scenario = TechnicalContentMiningScenario()
        scenario.cache_file = tmp_path / "youtube_cache.json"
        return scenario
    
    def test_widens_search(self, scenario):
        """
        Test 003.3: Progressive search expansion.
        Expected duration: 3.0s-15.0s
        """
        start_time = time.time()
        
        # Execute progressive search with a specific technical topic
        result = scenario.progressive_search_expansion(
            "golang concurrency",
            max_iterations=3
        )
        
        duration = time.time() - start_time
        
        # Assertions
        assert result.success, f"Progressive search failed: {result.error}"
        assert 3.0 <= duration <= 20.0, f"Duration {duration}s outside expected range"
        
        # Validate output structure
        output = result.output_data
        assert "videos" in output
        assert "total_found" in output
        assert "queries_used" in output
        assert "iteration_results" in output
        assert "expansion_effectiveness" in output
        
        # Validate progressive expansion
        queries = output["queries_used"]
        assert len(queries) >= 1, "Should have at least one query"
        assert len(queries) <= 3, "Should not exceed max iterations"
        
        # First query should be the original
        assert queries[0] == "golang concurrency"
        
        # Subsequent queries should be expanded
        if len(queries) > 1:
            assert queries[1] != queries[0], "Second query should be different"
            # Should contain expansion terms
            assert any(term in queries[1].lower() for term in 
                      ["implementation", "tutorial", "conference", "talk", "advanced"])
        
        # Validate iteration results
        iteration_results = output["iteration_results"]
        assert len(iteration_results) == len(queries)
        
        total_videos_found = 0
        for i, iter_result in enumerate(iteration_results):
            assert "iteration" in iter_result
            assert "query" in iter_result
            assert "new_videos" in iter_result
            
            assert iter_result["iteration"] == i + 1
            assert iter_result["query"] == queries[i]
            
            if "error" not in iter_result:
                assert iter_result["new_videos"] >= 0
                total_videos_found += iter_result["new_videos"]
            
            # First iteration should find some videos
            if i == 0 and "error" not in iter_result:
                assert iter_result["new_videos"] > 0, "First search should find videos"
        
        # Validate videos
        videos = output["videos"]
        assert len(videos) > 0, "Should find at least some videos"
        assert len(videos) <= 15, "Should return top 15 videos"
        
        # All videos should be unique
        video_ids = [v["id"] for v in videos]
        assert len(video_ids) == len(set(video_ids)), "Videos should be unique"
        
        # Videos should be sorted by technical score
        if len(videos) > 1:
            scores = [v.get("technical_score", 0) for v in videos]
            assert scores == sorted(scores, reverse=True), "Videos not sorted by score"
        
        # Validate expansion effectiveness
        effectiveness = output["expansion_effectiveness"]
        assert "effectiveness" in effectiveness
        assert "best_iteration" in effectiveness
        assert "diminishing_returns" in effectiveness
        assert "total_new_videos" in effectiveness
        
        assert 0.0 <= effectiveness["effectiveness"] <= 1.0
        assert 1 <= effectiveness["best_iteration"] <= len(queries)
        assert isinstance(effectiveness["diminishing_returns"], bool)
        
        # If multiple iterations, check for reasonable expansion
        if len(queries) > 1 and total_videos_found > 5:
            assert effectiveness["effectiveness"] > 0.3, \
                "Expansion should be somewhat effective"
        
        # Check timing distribution
        # With 3 iterations and delays, should take reasonable time
        if len(queries) == 3:
            assert duration >= 5.0, "Three iterations should take some time"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])