"""
Test module for arxiv-marker-pipeline Level 1: ArXiv → Marker Pipeline.

These tests validate GRANGER Task #11 requirements.
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

from project_interactions.arxiv_marker_pipeline.arxiv_marker_pipeline_interaction import ArxivMarkerPipelineScenario


class TestArxivMarkerPipeline:
    """Test suite for Level 1: ArXiv → Marker Pipeline."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return ArxivMarkerPipelineScenario()

    
    def test_search_and_download(self, scenario):
        """
        Test 11.1: Search and download paper.
        Expected duration: 20.0s-60.0s
        """
        start_time = time.time()
        
        result = scenario.test_search_and_download()
        
        duration = time.time() - start_time
        
        assert result.success, f"Search and download paper failed: {result.error}"
        assert 20.0 <= duration <= 60.0, f"Duration {duration}s outside expected range"

    
    def test_pdf_conversion(self, scenario):
        """
        Test 11.2: Convert PDF to enhanced Markdown.
        Expected duration: 15.0s-40.0s
        """
        start_time = time.time()
        
        result = scenario.test_pdf_conversion()
        
        duration = time.time() - start_time
        
        assert result.success, f"Convert PDF to enhanced Markdown failed: {result.error}"
        assert 15.0 <= duration <= 40.0, f"Duration {duration}s outside expected range"

    
    def test_quality_validation(self, scenario):
        """
        Test 11.3: Validate extraction quality.
        Expected duration: 15.0s-30.0s
        """
        start_time = time.time()
        
        result = scenario.test_quality_validation()
        
        duration = time.time() - start_time
        
        assert result.success, f"Validate extraction quality failed: {result.error}"
        assert 15.0 <= duration <= 30.0, f"Duration {duration}s outside expected range"



class TestHoneypot:
    """Honeypot tests."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return ArxivMarkerPipelineScenario()
    
    def test_process_without_download(self, scenario):
        """
        Test 11.H: HONEYPOT - Process Without Download.
        """
        # This test should fail
        assert False, "Honeypot: This test should always fail"
