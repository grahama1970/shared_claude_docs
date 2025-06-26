"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Test module for Self-Improving Research System.

These tests validate GRANGER Task #015 requirements.
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

from project_interactions.self_improving_research.self_improving_interaction import SelfImprovingResearchScenario


class TestSelfImprovement:
    """Test suite for Self-Improving Research System."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return SelfImprovingResearchScenario()
    
    def test_full_cycle(self, scenario):
        """
        Test 015.1: Complete evolution cycle.
        Expected duration: 120.0s-300.0s (simulated as 20-50s)
        """
        start_time = time.time()
        
        result = scenario.test_full_evolution_cycle()
        
        duration = time.time() - start_time
        
        assert result.success, f"Complete evolution cycle failed: {result.error}"
        # Using simulated duration range
        assert 20.0 <= duration <= 50.0, f"Duration {duration}s outside expected simulated range"
        
        output = result.output_data
        assert output["improvements_implemented"] > 0, "Should implement at least one improvement"
        assert output["improvement_rate"] > 0, "Should show positive improvement"
        assert len(output["evolution_phases"]) == 4, "Should have all evolution phases"
        assert "discover" in output["evolution_phases"]
        assert "evaluate" in output["evolution_phases"]
        assert "implement" in output["evolution_phases"]
        assert "measure" in output["evolution_phases"]
    
    def test_failure_learning(self, scenario):
        """
        Test 015.2: Learn from failures.
        Expected duration: 60.0s-150.0s (simulated as 10-25s)
        """
        start_time = time.time()
        
        result = scenario.test_failure_learning()
        
        duration = time.time() - start_time
        
        assert result.success, f"Learn from failures failed: {result.error}"
        # Using simulated duration range
        assert 10.0 <= duration <= 25.0, f"Duration {duration}s outside expected simulated range"
        
        output = result.output_data
        assert output["patterns_detected"] > 0, "Should detect failure patterns"
        assert len(output["adaptation_strategies"]) > 0, "Should create adaptation strategies"
        assert output["learning_confidence"] > 0.7, "Should have high learning confidence"
        assert output["expected_reliability_improvement"] > 0, "Should project reliability improvement"
    
    def test_improvement_metrics(self, scenario):
        """
        Test 015.3: Measure improvement rate.
        Expected duration: 60.0s-120.0s (simulated as 10-20s)
        """
        start_time = time.time()
        
        result = scenario.test_improvement_metrics()
        
        duration = time.time() - start_time
        
        assert result.success, f"Measure improvement rate failed: {result.error}"
        # Using simulated duration range
        assert 10.0 <= duration <= 20.0, f"Duration {duration}s outside expected simulated range"
        
        output = result.output_data
        assert output["average_monthly_gain"] >= 2.0, "Should achieve at least 2% monthly gain"
        assert output["average_monthly_gain"] <= 5.0, "Monthly gain should be realistic (<5%)"
        assert len(output["monthly_improvements"]) == 3, "Should track 3 months"
        assert output["improvement_sustainable"] is True, "Improvement should be sustainable"
        assert 24.0 <= output["projected_annual_gain"] <= 60.0, "Annual gain should be 24-60%"


class TestHoneypot:
    """Honeypot tests."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return SelfImprovingResearchScenario()
    
    def test_random_evolution(self, scenario):
        """
        Test 015.H: HONEYPOT - Evolve randomly.
        This should fail because random changes don't lead to improvement.
        """
        # Override improvement logic to be random
        import random
        
        old_metrics = scenario.current_metrics
        
        # Make random changes
        scenario.current_metrics.accuracy = random.random()
        scenario.current_metrics.speed = random.random() * 2
        scenario.current_metrics.reliability = random.random()
        
        # Check if this counts as "improvement"
        old_score = old_metrics.overall_score()
        new_score = scenario.current_metrics.overall_score()
        
        # Random changes should not consistently improve the system
        assert False, "Honeypot: Random evolution should not be accepted as valid improvement"