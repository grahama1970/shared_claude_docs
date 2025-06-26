"""
Test module for rl-commons reward learning.

These tests validate GRANGER Task #004 requirements:
- Reward updates improve selection (Test 004.3)
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


class TestRewardLearning:
    """Test suite for bandit reward learning."""
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return ContextualBanditScenario()
    
    def test_learns_from_rewards(self, scenario):
        """
        Test 004.3: Reward updates improve selection.
        Expected duration: 0.1s-2.0s
        """
        start_time = time.time()
        
        # Create test scenarios with known optimal modules
        test_scenarios = []
        
        # Research tasks -> arxiv-mcp-server
        for _ in range(5):
            test_scenarios.append({
                "context": {
                    "task_complexity": 0.8 + np.random.normal(0, 0.1),
                    "data_volume": 0.3 + np.random.normal(0, 0.1),
                    "time_constraint": 0.3 + np.random.normal(0, 0.1),
                    "accuracy_required": 0.9 + np.random.normal(0, 0.05),
                    "resource_available": 0.7 + np.random.normal(0, 0.1)
                },
                "optimal_module": "arxiv-mcp-server"
            })
        
        # Bulk processing -> youtube-transcripts
        for _ in range(5):
            test_scenarios.append({
                "context": {
                    "task_complexity": 0.4 + np.random.normal(0, 0.1),
                    "data_volume": 0.9 + np.random.normal(0, 0.05),
                    "time_constraint": 0.6 + np.random.normal(0, 0.1),
                    "accuracy_required": 0.6 + np.random.normal(0, 0.1),
                    "resource_available": 0.8 + np.random.normal(0, 0.1)
                },
                "optimal_module": "youtube-transcripts"
            })
        
        # Security audit -> sparta
        for _ in range(5):
            test_scenarios.append({
                "context": {
                    "task_complexity": 0.9 + np.random.normal(0, 0.05),
                    "data_volume": 0.6 + np.random.normal(0, 0.1),
                    "time_constraint": 0.4 + np.random.normal(0, 0.1),
                    "accuracy_required": 0.95 + np.random.normal(0, 0.03),
                    "resource_available": 0.8 + np.random.normal(0, 0.1)
                },
                "optimal_module": "sparta"
            })
        
        # Document processing -> marker
        for _ in range(5):
            test_scenarios.append({
                "context": {
                    "task_complexity": 0.7 + np.random.normal(0, 0.1),
                    "data_volume": 0.5 + np.random.normal(0, 0.1),
                    "time_constraint": 0.5 + np.random.normal(0, 0.1),
                    "accuracy_required": 0.85 + np.random.normal(0, 0.05),
                    "resource_available": 0.7 + np.random.normal(0, 0.1)
                },
                "optimal_module": "marker"
            })
        
        # Shuffle scenarios
        np.random.shuffle(test_scenarios)
        
        # Run learning test
        result = scenario.test_reward_learning(test_scenarios)
        
        duration = time.time() - start_time
        
        # Assertions
        assert result.success, f"Learning test failed: {result.error}"
        assert 0.1 <= duration <= 2.0, f"Duration {duration}s outside expected range"
        
        # Validate output structure
        output = result.output_data
        assert "learning_results" in output
        assert "accuracy" in output
        assert "first_half_performance" in output
        assert "second_half_performance" in output
        assert "improvement" in output
        assert "final_weights" in output
        
        # Validate improvement
        improvement = output["improvement"]
        assert improvement > 0, f"No improvement in performance: {improvement:.3f}"
        
        # Check performance metrics
        first_half = output["first_half_performance"]
        second_half = output["second_half_performance"]
        
        assert 0.0 <= first_half <= 1.0
        assert 0.0 <= second_half <= 1.0
        assert second_half > first_half, "Performance should improve over time"
        
        # Validate accuracy
        accuracy = output["accuracy"]
        assert accuracy > 0.5, f"Accuracy {accuracy:.2%} too low (random is 16.7%)"
        
        # Validate learning results
        learning_results = output["learning_results"]
        assert len(learning_results) == 20, "Should have 20 learning iterations"
        
        correct_selections = 0
        rewards_over_time = []
        
        for i, lr in enumerate(learning_results):
            assert "context" in lr
            assert "selected" in lr
            assert "expected" in lr
            assert "reward" in lr
            assert "correct" in lr
            
            # Validate context values are properly clipped
            for feature, value in lr["context"].items():
                assert 0.0 <= value <= 1.0, f"Context value out of range: {feature}={value}"
            
            assert lr["selected"] in scenario.modules
            assert lr["expected"] in scenario.modules
            assert 0.0 <= lr["reward"] <= 1.0
            
            if lr["correct"]:
                correct_selections += 1
            
            rewards_over_time.append(lr["reward"])
        
        # Check learning progression
        # Later selections should be more accurate
        first_quarter_correct = sum(1 for lr in learning_results[:5] if lr["correct"])
        last_quarter_correct = sum(1 for lr in learning_results[-5:] if lr["correct"])
        
        assert last_quarter_correct >= first_quarter_correct, \
            "Selection accuracy should improve or stay same"
        
        # Validate final weights
        final_weights = output["final_weights"]
        assert isinstance(final_weights, dict)
        
        for module, weights in final_weights.items():
            assert module in scenario.modules
            assert isinstance(weights, list)
            assert len(weights) == len(scenario.context_features)
            
            # Weights should have been updated (not all zeros)
            assert any(w != 0.0 for w in weights), \
                f"Module {module} has no weight updates"
        
        # Check that frequently selected modules have more weight updates
        module_selections = {}
        for lr in learning_results:
            module = lr["selected"]
            module_selections[module] = module_selections.get(module, 0) + 1
        
        # Most selected modules should have non-zero weights
        most_selected = max(module_selections, key=module_selections.get)
        assert any(w != 0.0 for w in final_weights[most_selected]), \
            f"Most selected module {most_selected} has no weight updates"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])