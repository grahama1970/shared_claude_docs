"""
Test module for youtube-transcripts technical search.

These tests validate GRANGER Task #003 requirements:
- Search technical presentations (Test 003.1)
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
import time
import os
from pathlib import Path

from technical_content_mining_interaction import TechnicalContentMiningScenario


class TestYouTubeSearch:
    """Test suite for YouTube technical search capabilities."""
    
    @pytest.fixture
    def scenario(self, tmp_path):
        """Create a scenario with temporary cache."""
        scenario = TechnicalContentMiningScenario()
        scenario.cache_file = tmp_path / "youtube_cache.json"
        return scenario
    
    def test_technical_search(self, scenario):
        """
        Test 003.1: Search technical presentations.
        Expected duration: 5.0s-20.0s
        """
        start_time = time.time()
        
        # Execute search (will use simulation if no API key)
        result = scenario.search_technical_presentations(
            "python design patterns",
            max_results=20
        )
        
        duration = time.time() - start_time
        
        # Assertions
        assert result.success, f"Technical search failed: {result.error}"
        assert 5.0 <= duration <= 20.0, f"Duration {duration}s outside expected range"
        
        # Validate output structure
        output = result.output_data
        assert "videos" in output
        assert "total_found" in output
        assert "search_query" in output
        assert "timestamp" in output
        
        # Validate videos
        videos = output["videos"]
        assert len(videos) > 0, "No technical videos found"
        assert len(videos) <= 10, "Should return top 10 videos"
        
        # Check if using real API or simulation
        is_simulated = output.get("simulated", False)
        
        # Validate video data
        for video in videos:
            assert "id" in video
            assert "title" in video
            assert "channel" in video
            assert "technical_score" in video
            assert 0.0 <= video["technical_score"] <= 1.0
            
            # Check technical relevance
            title_lower = video["title"].lower()
            assert any(term in title_lower for term in 
                      ["tutorial", "course", "talk", "conference", "pattern", "python", "design"]), \
                   f"Video '{video['title']}' doesn't seem technical"
            
            # Validate additional fields
            if not is_simulated:
                assert "published_at" in video
                assert "duration" in video
                assert "view_count" in video
                assert video["view_count"] >= 0
                assert "has_transcript" in video
                assert "transcript_quality" in video
        
        # Videos should be sorted by technical score
        if len(videos) > 1:
            scores = [v["technical_score"] for v in videos]
            assert scores == sorted(scores, reverse=True), "Videos not sorted by technical score"
        
        # Query should include technical terms
        query = output["search_query"]
        assert "python" in query.lower()
        assert any(term in query.lower() for term in ["tutorial", "conference", "talk", "presentation"])
        
        # Duration check based on API availability
        if is_simulated:
            # Simulation should have consistent timing
            assert 3.0 <= duration <= 6.0, "Simulation timing inconsistent"
        else:
            # Real API can vary more
            assert 5.0 <= duration <= 20.0, "Real API timing out of range"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])