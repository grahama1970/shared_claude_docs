"""
Test module for marker-arangodb-pipeline Level 1: Marker → ArangoDB Pipeline.

These tests validate GRANGER Task #12 requirements.
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

from project_interactions.marker_arangodb_pipeline.marker_arangodb_pipeline_interaction import MarkerArangoPipelineScenario


class TestMarkerArangoPipeline:
    """Test suite for Level 1: Marker → ArangoDB Pipeline."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return MarkerArangoPipelineScenario()

    
    def test_entity_extraction(self, scenario):
        """
        Test 12.1: Extract entities from document.
        Expected duration: 5.0s-15.0s
        """
        start_time = time.time()
        
        result = scenario.test_entity_extraction()
        
        duration = time.time() - start_time
        
        assert result.success, f"Extract entities from document failed: {result.error}"
        assert 5.0 <= duration <= 15.0, f"Duration {duration}s outside expected range"

    
    def test_graph_storage(self, scenario):
        """
        Test 12.2: Store as graph relationships.
        Expected duration: 5.0s-20.0s
        """
        start_time = time.time()
        
        result = scenario.test_graph_storage()
        
        duration = time.time() - start_time
        
        assert result.success, f"Store as graph relationships failed: {result.error}"
        assert 5.0 <= duration <= 20.0, f"Duration {duration}s outside expected range"

    
    def test_knowledge_search(self, scenario):
        """
        Test 12.3: Search stored knowledge.
        Expected duration: 5.0s-10.0s
        """
        start_time = time.time()
        
        result = scenario.test_knowledge_search()
        
        duration = time.time() - start_time
        
        assert result.success, f"Search stored knowledge failed: {result.error}"
        assert 5.0 <= duration <= 10.0, f"Duration {duration}s outside expected range"



class TestHoneypot:
    """Honeypot tests."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return MarkerArangoPipelineScenario()
    
    def test_store_without_extraction(self, scenario):
        """
        Test 12.H: HONEYPOT - Store Without Extraction.
        """
        # This test should fail
        assert False, "Honeypot: This test should always fail"
