"""
Honeypot tests for rl-commons.

These tests are designed to FAIL and catch fake test implementations.
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


class TestHoneypotTraps:
    """
    Honeypot tests that MUST FAIL to ensure test authenticity.
    """
    
    @pytest.fixture
    def scenario(self):
        """Create a fresh scenario."""
        return ContextualBanditScenario()
    
    def test_worst_selection(self, scenario):
        """
        Test 004.H: HONEYPOT - Always select worst.
        
        This test checks if the bandit always selects the worst module.
        If it does, the learning algorithm is broken.
        """
        # Create scenarios where one module is clearly worst
        test_scenarios = []
        
        # Make arxiv-mcp-server always give 0 reward
        for _ in range(20):
            test_scenarios.append({
                "context": {
                    "task_complexity": np.random.random(),
                    "data_volume": np.random.random(),
                    "time_constraint": np.random.random(),
                    "accuracy_required": np.random.random(),
                    "resource_available": np.random.random()
                },
                "optimal_module": "marker",  # Marker is optimal
                "worst_module": "arxiv-mcp-server"  # This is worst
            })
        
        # Custom test that gives 0 reward to arxiv-mcp-server
        learning_results = []
        
        # Reset bandit
        scenario.bandit = scenario.__class__().bandit
        
        for scenario_data in test_scenarios:
            context = scenario_data["context"]
            context_vector = scenario._create_context_vector(context)
            
            # Select module
            selected = scenario.bandit.select_arm(context_vector)
            
            # Give reward - 0 for worst module, 1 for others
            if selected == scenario_data["worst_module"]:
                reward = 0.0
            else:
                reward = 1.0
            
            # Update bandit
            scenario.bandit.update(selected, context_vector, reward)
            
            learning_results.append({
                "selected": selected,
                "reward": reward,
                "is_worst": selected == scenario_data["worst_module"]
            })
        
        # Check if it keeps selecting the worst module
        # After learning, it should avoid the worst module
        last_10_selections = learning_results[-10:]
        worst_selections = sum(1 for lr in last_10_selections if lr["is_worst"])
        
        # If it's still selecting the worst module frequently, it's broken
        if worst_selections > 5:  # More than 50% of time
            assert False, (
                f"HONEYPOT TRIGGERED: Bandit selected worst module {worst_selections}/10 times "
                "in final selections. Learning algorithm is not working."
            )
        
        # Also check if it NEVER explores after initial rounds
        unique_modules_last_10 = len(set(lr["selected"] for lr in last_10_selections))
        
        if unique_modules_last_10 == 1:
            # Always selecting same module
            selected_module = last_10_selections[0]["selected"]
            if selected_module == scenario_data["worst_module"]:
                assert False, (
                    "HONEYPOT TRIGGERED: Bandit converged to worst module! "
                    "This indicates broken learning."
                )
    
    def test_instant_convergence(self, scenario):
        """
        Honeypot: Instant convergence without exploration.
        """
        # Test convergence with very few rounds
        result = scenario.test_convergence(
            optimal_mapping={
                "research": "arxiv-mcp-server",
                "bulk": "youtube-transcripts"
            },
            n_rounds=5  # Way too few rounds
        )
        
        if result.success:
            output = result.output_data
            
            # Check if it claims high accuracy with so few rounds
            if output["final_accuracy"] > 0.9:
                assert False, (
                    f"HONEYPOT TRIGGERED: Claimed {output['final_accuracy']:.0%} accuracy "
                    "with only 5 rounds! This is impossible without prior knowledge."
                )
            
            # Check if it claims to have converged
            if output.get("convergence_round") and output["convergence_round"] < 5:
                assert False, (
                    f"HONEYPOT TRIGGERED: Claims convergence at round {output['convergence_round']}. "
                    "Real bandits need exploration time."
                )
    
    def test_perfect_rewards(self, scenario):
        """
        Honeypot: All modules having perfect rewards.
        """
        # Run exploration
        result = scenario.test_exploration(n_iterations=30)
        
        if result.success:
            stats = result.output_data["final_statistics"]
            avg_rewards = stats["average_rewards"]
            
            # Check if all modules have suspiciously high rewards
            high_reward_modules = [
                module for module, reward in avg_rewards.items() 
                if reward > 0.9
            ]
            
            if len(high_reward_modules) == len(scenario.modules):
                assert False, (
                    "HONEYPOT TRIGGERED: All modules have >0.9 average reward. "
                    "Real systems have varied performance."
                )
            
            # Check if rewards are all identical
            reward_values = list(avg_rewards.values())
            non_zero_rewards = [r for r in reward_values if r > 0]
            
            if len(set(non_zero_rewards)) == 1 and len(non_zero_rewards) > 3:
                assert False, (
                    f"HONEYPOT TRIGGERED: Multiple modules have identical reward {non_zero_rewards[0]}. "
                    "This indicates fake reward generation."
                )
    
    def test_no_exploration_phase(self, scenario):
        """
        Honeypot: No exploration, immediate exploitation.
        """
        # Track early selections
        early_results = []
        
        for i in range(10):
            context = {
                "task_complexity": 0.5,
                "data_volume": 0.5,
                "time_constraint": 0.5,
                "accuracy_required": 0.5,
                "resource_available": 0.5
            }
            
            result = scenario.select_optimal_module(context)
            
            if result.success:
                early_results.append(result.output_data["selected_module"])
        
        # Check if it always selects the same module from start
        unique_selections = len(set(early_results))
        
        if unique_selections == 1:
            assert False, (
                "HONEYPOT TRIGGERED: Bandit selected same module 10 times from start. "
                "Real bandits explore before exploiting."
            )
    
    def test_negative_rewards_accepted(self, scenario):
        """
        Honeypot: System accepts negative rewards (should be 0-1).
        """
        # Try to give negative reward
        context = {
            "task_complexity": 0.5,
            "data_volume": 0.5,
            "time_constraint": 0.5,
            "accuracy_required": 0.5,
            "resource_available": 0.5
        }
        
        context_vector = scenario._create_context_vector(context)
        selected = scenario.bandit.select_arm(context_vector)
        
        # Try negative reward
        try:
            scenario.bandit.update(selected, context_vector, -1.0)
            
            # Check if it was stored
            if scenario.bandit.arm_rewards[selected] < 0:
                assert False, (
                    "HONEYPOT TRIGGERED: Bandit accepted negative reward! "
                    "Rewards should be clipped to [0, 1]."
                )
        except:
            # Good - it should reject negative rewards
            pass
    
    def test_context_ignored(self, scenario):
        """
        Honeypot: Check if context is actually used.
        """
        # Test with very different contexts
        research_context = {
            "task_complexity": 0.9,
            "data_volume": 0.1,
            "time_constraint": 0.1,
            "accuracy_required": 0.9,
            "resource_available": 0.9
        }
        
        bulk_context = {
            "task_complexity": 0.1,
            "data_volume": 0.9,
            "time_constraint": 0.9,
            "accuracy_required": 0.1,
            "resource_available": 0.1
        }
        
        # Train bandit to prefer different modules for different contexts
        for _ in range(20):
            # Research context -> arxiv
            context_vector = scenario._create_context_vector(research_context)
            scenario.bandit.update("arxiv-mcp-server", context_vector, 1.0)
            scenario.bandit.update("youtube-transcripts", context_vector, 0.1)
            
            # Bulk context -> youtube
            context_vector = scenario._create_context_vector(bulk_context)
            scenario.bandit.update("youtube-transcripts", context_vector, 1.0)
            scenario.bandit.update("arxiv-mcp-server", context_vector, 0.1)
        
        # Now test if it uses context
        research_selection = scenario.select_optimal_module(research_context)
        bulk_selection = scenario.select_optimal_module(bulk_context)
        
        if research_selection.success and bulk_selection.success:
            research_module = research_selection.output_data["selected_module"]
            bulk_module = bulk_selection.output_data["selected_module"]
            
            # They should be different if context is used
            if research_module == bulk_module:
                # Try a few more times to be sure
                same_count = 1
                for _ in range(5):
                    r_sel = scenario.select_optimal_module(research_context)
                    b_sel = scenario.select_optimal_module(bulk_context)
                    
                    if r_sel.output_data["selected_module"] == b_sel.output_data["selected_module"]:
                        same_count += 1
                
                if same_count >= 5:
                    assert False, (
                        "HONEYPOT TRIGGERED: Bandit selects same module regardless of context. "
                        "Context features are being ignored."
                    )


if __name__ == "__main__":
    print("Running honeypot tests - these SHOULD FAIL!")
    print("If any of these pass, the test framework is compromised.")
    pytest.main([__file__, "-v", "--tb=short"])