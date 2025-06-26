"""
Test module for Visualization Intelligence.

These tests validate GRANGER Task #016 requirements.
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

from project_interactions.viz_intelligence.viz_intelligence_interaction import VisualizationIntelligenceScenario


class TestVisualizationIntelligence:
    """Test suite for Visualization Intelligence."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return VisualizationIntelligenceScenario()
    
    def test_detects_unsuitable(self, scenario):
        """
        Test 016.1: Detect ungraphable data.
        Expected duration: 1.0s-5.0s
        """
        start_time = time.time()
        
        result = scenario.test_detects_unsuitable()
        
        duration = time.time() - start_time
        
        assert result.success, f"Detect ungraphable data failed: {result.error}"
        assert 1.0 <= duration <= 5.0, f"Duration {duration}s outside expected range"
        
        output = result.output_data
        assert output["detection_accuracy"] == 1.0, "Should correctly identify all unsuitable data"
        assert output["correctly_identified"] == len(result.input_data["datasets_tested"])
        
        # Check that recommendations are NOT graphs
        for rec in output["recommendations"]:
            assert rec["recommended"] != "graph", f"{rec['dataset']} incorrectly recommended for graphing"
    
    def test_alternatives(self, scenario):
        """
        Test 016.2: Suggest alternative viz.
        Expected duration: 1.0s-3.0s
        """
        start_time = time.time()
        
        result = scenario.test_alternatives()
        
        duration = time.time() - start_time
        
        assert result.success, f"Suggest alternative viz failed: {result.error}"
        assert 1.0 <= duration <= 3.0, f"Duration {duration}s outside expected range"
        
        output = result.output_data
        assert output["all_have_alternatives"] is True
        assert output["total_alternatives"] > 0
        
        # Each dataset should have at least 1 alternative
        for suggestion in output["suggestions"]:
            assert suggestion["alternatives_count"] >= 1, f"{suggestion['dataset']} missing alternatives"
    
    def test_sparse_data(self, scenario):
        """
        Test 016.3: Handle sparse data.
        Expected duration: 2.0s-10.0s
        """
        start_time = time.time()
        
        result = scenario.test_sparse_data()
        
        duration = time.time() - start_time
        
        assert result.success, f"Handle sparse data failed: {result.error}"
        assert 2.0 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        output = result.output_data
        assert output["handling_rate"] == 1.0, "Should handle all sparse data gracefully"
        
        # Check each sparse dataset is handled properly
        for handling in output["handling_results"]:
            assert handling["handling"] == "graceful", f"{handling['dataset']} not handled gracefully"
            assert handling["sparsity"] > 0.8, "Test data should be very sparse"


class TestHoneypot:
    """Honeypot tests."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return VisualizationIntelligenceScenario()
    
    def test_force_graph(self, scenario):
        """
        Test 016.H: HONEYPOT - Force graph everything.
        This should fail because forcing graphs on unsuitable data produces bad visualizations.
        """
        # Create obviously unsuitable data
        bad_data = {
            "name": "impossible_to_graph",
            "type": "mixed",
            "values": [None] * 50 + ["text", "more text", 123, {"nested": "dict"}, ["list"]],
            "dimensions": ["chaos", "madness", "impossibility", "futility", "despair"]
        }
        
        # Try to analyze
        analysis = scenario.analyzer.analyze_dataset(bad_data)
        recommendation = scenario.recommender.recommend(analysis)
        
        # If system recommends graphing this chaos, it fails
        assert recommendation["primary"] != "graph", "Honeypot: Should not recommend graph for chaotic mixed data"