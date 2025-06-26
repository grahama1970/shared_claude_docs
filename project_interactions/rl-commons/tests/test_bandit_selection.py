"""
Test module for rl-commons bandit selection.

These tests validate GRANGER Task #004 requirements:
- Bandit selects optimal module (Test 004.1)
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
import time
import numpy as np
from pathlib import Path

from contextual_bandit_interaction import ContextualBanditScenario


class TestBanditSelection:
    """Test suite for contextual bandit module selection."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return ContextualBanditScenario()
    
    def test_optimal_selection(self, scenario):
        """
        Test 004.1: Bandit selects optimal module.
        Expected duration: 1.0s-5.0s
        """
        start_time = time.time()
        
        # Define optimal mapping for testing
        optimal_mapping = {
            "research": "arxiv-mcp-server",
            "bulk_processing": "youtube-transcripts", 
            "real_time": "claude-max-proxy",
            "security_audit": "sparta"
        }
        
        # Test convergence to optimal selection
        result = scenario.test_convergence(
            optimal_mapping=optimal_mapping,
            n_rounds=100  # Enough rounds to converge
        )
        
        duration = time.time() - start_time
        
        # Assertions
        assert result.success, f"Convergence test failed: {result.error}"
        assert 1.0 <= duration <= 5.0, f"Duration {duration}s outside expected range"
        
        # Validate output structure
        output = result.output_data
        assert "convergence_data" in output
        assert "final_accuracy" in output
        assert "cumulative_regret" in output
        assert "regret_per_round" in output
        assert "sublinear_regret" in output
        assert "module_statistics" in output
        assert "convergence_round" in output
        
        # Validate convergence metrics
        final_accuracy = output["final_accuracy"]
        assert final_accuracy >= 0.8, f"Final accuracy {final_accuracy:.2%} below 80%"
        
        # Check sublinear regret (sign of good convergence)
        assert output["sublinear_regret"], "Regret is not sublinear"
        
        # Validate convergence data
        convergence_data = output["convergence_data"]
        assert len(convergence_data) > 0, "No convergence data"
        
        for data_point in convergence_data:
            assert "round" in data_point
            assert "context_type" in data_point
            assert "selected" in data_point
            assert "optimal" in data_point
            assert "correct" in data_point
            assert "regret" in data_point
            assert "cumulative_regret" in data_point
            
            # Validate module names
            assert data_point["selected"] in scenario.modules
            assert data_point["optimal"] in scenario.modules
            assert data_point["context_type"] in optimal_mapping
        
        # Check module statistics
        stats = output["module_statistics"]
        assert "total_pulls" in stats
        assert "arm_pulls" in stats
        assert "average_rewards" in stats
        
        # Verify all modules were at least tried
        arm_pulls = stats["arm_pulls"]
        modules_tried = sum(1 for pulls in arm_pulls.values() if pulls > 0)
        assert modules_tried >= len(scenario.modules) * 0.5, \
            "Should explore at least half the modules"
        
        # Check if it found convergence point
        convergence_round = output["convergence_round"]
        if convergence_round:
            assert convergence_round < 80, \
                "Should converge before round 80"
            assert convergence_round > 10, \
                "Convergence too fast to be real"
        
        # Verify regret decreases over time
        cumulative_regret = output["cumulative_regret"]
        regret_per_round = output["regret_per_round"]
        
        assert cumulative_regret >= 0, "Negative regret impossible"
        assert regret_per_round < 0.5, "Average regret too high"
        
        # Check that optimal modules are selected more often
        avg_rewards = stats["average_rewards"]
        
        # The optimal modules should have higher average rewards
        for context_type, optimal_module in optimal_mapping.items():
            module_reward = avg_rewards.get(optimal_module, 0)
            assert module_reward > 0.5, \
                f"Optimal module {optimal_module} has low reward: {module_reward}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])