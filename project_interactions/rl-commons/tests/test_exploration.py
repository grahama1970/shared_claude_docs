"""
Test module for rl-commons exploration behavior.

These tests validate GRANGER Task #004 requirements:
- Exploration of new modules (Test 004.2)
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


class TestExploration:
    """Test suite for bandit exploration behavior."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return ContextualBanditScenario()
    
    def test_explores_new(self, scenario):
        """
        Test 004.2: Exploration of new modules.
        Expected duration: 0.5s-3.0s
        """
        start_time = time.time()
        
        # Test exploration with moderate iterations
        result = scenario.test_exploration(n_iterations=20)
        
        duration = time.time() - start_time
        
        # Assertions
        assert result.success, f"Exploration test failed: {result.error}"
        assert 0.5 <= duration <= 3.0, f"Duration {duration}s outside expected range"
        
        # Validate output structure
        output = result.output_data
        assert "exploration_results" in output
        assert "modules_explored" in output
        assert "exploration_rate" in output
        assert "final_statistics" in output
        assert "convergence_analysis" in output
        
        # Validate exploration metrics
        modules_explored = output["modules_explored"]
        exploration_rate = output["exploration_rate"]
        
        # Should explore multiple modules
        assert modules_explored >= 3, \
            f"Only explored {modules_explored} modules, expected at least 3"
        
        # Exploration rate should be reasonable
        assert exploration_rate >= 0.5, \
            f"Exploration rate {exploration_rate:.2%} too low"
        
        # Validate exploration results
        exploration_results = output["exploration_results"]
        assert len(exploration_results) == 20, "Should have 20 iterations"
        
        # Track which modules were selected
        selected_modules = set()
        rewards_by_iteration = []
        
        for i, result_item in enumerate(exploration_results):
            assert "iteration" in result_item
            assert "selected" in result_item
            assert "reward" in result_item
            assert "context" in result_item
            
            assert result_item["iteration"] == i + 1
            assert result_item["selected"] in scenario.modules
            assert 0.0 <= result_item["reward"] <= 1.0
            
            selected_modules.add(result_item["selected"])
            rewards_by_iteration.append(result_item["reward"])
            
            # Validate context
            context = result_item["context"]
            for feature in scenario.context_features:
                assert feature in context
                assert 0.0 <= context[feature] <= 1.0
        
        # Check that multiple modules were actually selected
        assert len(selected_modules) >= 3, \
            f"Only selected {len(selected_modules)} different modules"
        
        # Validate final statistics
        stats = output["final_statistics"]
        assert "total_pulls" in stats
        assert stats["total_pulls"] == 20
        
        arm_pulls = stats["arm_pulls"]
        assert sum(arm_pulls.values()) == 20, "Pull counts don't sum to total"
        
        # Check exploration pattern - shouldn't stick to one module too early
        first_10_modules = [r["selected"] for r in exploration_results[:10]]
        unique_in_first_10 = len(set(first_10_modules))
        
        assert unique_in_first_10 >= 3, \
            "Not enough exploration in first 10 iterations"
        
        # Validate convergence analysis
        convergence = output["convergence_analysis"]
        assert "converged" in convergence
        
        if convergence["converged"]:
            assert "converged_to" in convergence
            assert "confidence" in convergence
            assert convergence["converged_to"] in scenario.modules
            assert 0.0 <= convergence["confidence"] <= 1.0
        else:
            assert "reason" in convergence
            # With only 20 iterations, it's OK not to converge
            assert convergence["reason"] in ["Still exploring", "Too few iterations"]
        
        # Check reward improvement over time
        # Average rewards should generally improve
        first_half_avg = np.mean(rewards_by_iteration[:10])
        second_half_avg = np.mean(rewards_by_iteration[10:])
        
        # Some improvement expected, but not required to be large
        improvement = second_half_avg - first_half_avg
        assert improvement > -0.1, \
            f"Rewards decreased significantly: {improvement:.3f}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])