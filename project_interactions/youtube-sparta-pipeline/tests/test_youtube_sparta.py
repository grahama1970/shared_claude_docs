"""
Test module for YouTube → SPARTA Analysis Pipeline.

These tests validate GRANGER Task #013 requirements.
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

from project_interactions.youtube_sparta_pipeline.youtube_sparta_interaction import YouTubeSpartaPipelineScenario


class TestYouTubeSpartaPipeline:
    """Test suite for YouTube → SPARTA Analysis Pipeline."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return YouTubeSpartaPipelineScenario()
    
    def test_security_extraction(self, scenario):
        """
        Test 013.1: Extract security discussions.
        Expected duration: 15.0s-40.0s
        """
        start_time = time.time()
        
        result = scenario.test_security_extraction()
        
        duration = time.time() - start_time
        
        assert result.success, f"Extract security discussions failed: {result.error}"
        assert 15.0 <= duration <= 40.0, f"Duration {duration}s outside expected range"
        
        output = result.output_data
        assert output["videos_processed"] >= 3, "Should process at least 3 videos"
        assert output["security_topics_found"] > 0, "Should find security topics"
        assert output["total_timestamps"] > 0, "Should extract timestamps"
    
    def test_framework_mapping(self, scenario):
        """
        Test 013.2: Map to compliance frameworks.
        Expected duration: 10.0s-25.0s
        """
        start_time = time.time()
        
        result = scenario.test_framework_mapping()
        
        duration = time.time() - start_time
        
        assert result.success, f"Map to compliance frameworks failed: {result.error}"
        assert 10.0 <= duration <= 25.0, f"Duration {duration}s outside expected range"
        
        output = result.output_data
        assert output["nist_controls_mapped"] > 0, "Should map NIST controls"
        assert output["mitre_tactics_mapped"] > 0, "Should map MITRE tactics"
        assert len(output["nist_families"]) > 0, "Should identify NIST families"
        assert output["mapping_confidence"] >= 0.8, "Confidence should be high"
    
    def test_threat_report(self, scenario):
        """
        Test 013.3: Generate threat report.
        Expected duration: 10.0s-20.0s
        """
        start_time = time.time()
        
        result = scenario.test_threat_report()
        
        duration = time.time() - start_time
        
        assert result.success, f"Generate threat report failed: {result.error}"
        assert 10.0 <= duration <= 20.0, f"Duration {duration}s outside expected range"
        
        output = result.output_data
        assert output["assessments_generated"] >= 2, "Should generate multiple assessments"
        assert output["average_risk_score"] > 0, "Should calculate risk score"
        assert output["highest_threat_level"] in ["Low", "Medium", "High"], "Should assess threat level"
        assert output["report_generated"] is True, "Should generate report"


class TestHoneypot:
    """Honeypot tests."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return YouTubeSpartaPipelineScenario()
    
    def test_analyze_cooking_video(self, scenario):
        """
        Test 013.H: HONEYPOT - Analyze cooking video.
        This should fail because cooking videos don't contain security content.
        """
        # Override the extractor to return cooking content
        scenario.youtube_extractor.security_videos = [{
            "video_id": "cooking123",
            "title": "How to Make Perfect Pasta",
            "channel": "Cooking Channel",
            "duration": 600,
            "transcript": [
                {"text": "Boil water in a large pot", "start": 0.0, "duration": 5.0},
                {"text": "Add salt to the water", "start": 5.0, "duration": 5.0},
                {"text": "Cook pasta al dente", "start": 10.0, "duration": 5.0}
            ]
        }]
        
        result = scenario.test_security_extraction()
        
        # This should fail - no security content in cooking video
        assert False, "Honeypot: Should not find security content in cooking video"