"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_09_rl_commons_decision.py
Description: Test RL Commons decision making and learning with verification
Level: 0
Modules: RL Commons, Test Reporter
Expected Bugs: Learning convergence issues, exploration/exploitation balance, reward calculation
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')
sys.path.insert(0, '/home/graham/workspace/experiments/rl_commons/src')

from base_interaction_test import BaseInteractionTest
import random

class RLCommonsDecisionTest(BaseInteractionTest):
    """Level 0: Test RL Commons decision making functionality"""
    
    def __init__(self):
        super().__init__(
            test_name="RL Commons Decision Making",
            level=0,
            modules=["RL Commons", "Test Reporter"]
        )
    
    def test_contextual_bandit(self):
        """Test contextual bandit decision making"""
        self.print_header()
        
        # Import RL Commons
        try:
            from rl_commons import ContextualBandit
            self.record_test("rl_commons_import", True, {})
        except ImportError as e:
            self.add_bug(
                "RL Commons module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot use RL functionality"
            )
            self.record_test("rl_commons_import", False, {"error": str(e)})
            return
        
        # Test bandit scenarios
        test_scenarios = [
            {
                "name": "Simple 3-armed bandit",
                "actions": ["action_a", "action_b", "action_c"],
                "context_features": ["time_of_day", "load"],
                "exploration_rate": 0.1
            },
            {
                "name": "High exploration",
                "actions": ["explore1", "explore2"],
                "context_features": ["feature1"],
                "exploration_rate": 0.9
            },
            {
                "name": "No exploration",
                "actions": ["exploit1", "exploit2"],
                "context_features": ["feature1"],
                "exploration_rate": 0.0
            },
            {
                "name": "Many actions",
                "actions": [f"action_{i}" for i in range(50)],
                "context_features": ["f1", "f2", "f3"],
                "exploration_rate": 0.2
            },
            {
                "name": "Empty actions",
                "actions": [],
                "context_features": ["feature1"],
                "exploration_rate": 0.1
            },
            {
                "name": "Invalid exploration rate",
                "actions": ["a1", "a2"],
                "context_features": ["f1"],
                "exploration_rate": 1.5  # Invalid > 1
            }
        ]
        
        for scenario in test_scenarios:
            print(f"\nTesting: {scenario['name']}")
            
            try:
                # Initialize bandit
                bandit = ContextualBandit(
                    actions=scenario["actions"],
                    context_features=scenario["context_features"],
                    exploration_rate=scenario["exploration_rate"]
                )
                
                if scenario["name"] in ["Empty actions", "Invalid exploration rate"]:
                    self.add_bug(
                        f"Invalid scenario accepted: {scenario['name']}",
                        "HIGH",
                        details=scenario
                    )
                
                # Test decision making
                decisions_made = {}
                exploration_count = 0
                
                for i in range(100):
                    # Create context
                    context = {
                        feature: random.random() 
                        for feature in scenario["context_features"]
                    }
                    
                    # Get action
                    action = bandit.select_action(context)
                    
                    if action:
                        decisions_made[action] = decisions_made.get(action, 0) + 1
                        
                        # Check if exploring
                        if hasattr(bandit, 'last_was_exploration'):
                            if bandit.last_was_exploration:
                                exploration_count += 1
                        
                        # Simulate reward
                        reward = random.random()
                        bandit.update(action, reward, context)
                    else:
                        self.add_bug(
                            "No action selected",
                            "HIGH",
                            scenario=scenario["name"],
                            context=context
                        )
                
                # Analyze results
                print(f"✅ Made 100 decisions")
                print(f"   Actions used: {len(decisions_made)}")
                print(f"   Exploration rate: {exploration_count/100:.2%}")
                
                self.record_test(f"bandit_{scenario['name']}", True, {
                    "decisions": decisions_made,
                    "exploration_rate": exploration_count/100
                })
                
                # Check exploration rate accuracy
                if scenario["exploration_rate"] < 1.0:
                    expected = scenario["exploration_rate"]
                    actual = exploration_count / 100
                    error = abs(expected - actual)
                    
                    if error > 0.2:  # More than 20% error
                        self.add_bug(
                            "Exploration rate inaccurate",
                            "MEDIUM",
                            expected=expected,
                            actual=actual,
                            error=error
                        )
                
                # Check action distribution
                if scenario["name"] == "No exploration" and len(decisions_made) > 1:
                    # Should converge to single best action
                    max_count = max(decisions_made.values())
                    if max_count < 80:  # Less than 80% on best action
                        self.add_bug(
                            "Poor exploitation convergence",
                            "MEDIUM",
                            distribution=decisions_made
                        )
                        
            except Exception as e:
                error_msg = str(e)
                print(f"💥 Exception: {error_msg[:100]}")
                
                if scenario["name"] not in ["Empty actions", "Invalid exploration rate"]:
                    self.add_bug(
                        f"Unexpected error in {scenario['name']}",
                        "HIGH",
                        error=error_msg
                    )
                
                self.record_test(f"bandit_{scenario['name']}", False, {"error": error_msg})
    
    def test_reward_learning(self):
        """Test reward learning and adaptation"""
        print("\n\nTesting Reward Learning...")
        
        try:
            from rl_commons import ContextualBandit
            
            # Create bandit with clear optimal action
            bandit = ContextualBandit(
                actions=["bad", "medium", "good"],
                context_features=["feature1"],
                exploration_rate=0.1
            )
            
            # Train with consistent rewards
            print("Training with consistent rewards...")
            for i in range(200):
                context = {"feature1": 0.5}
                action = bandit.select_action(context)
                
                # Give consistent rewards
                if action == "bad":
                    reward = 0.1
                elif action == "medium":
                    reward = 0.5
                elif action == "good":
                    reward = 0.9
                else:
                    reward = 0.0
                
                bandit.update(action, reward, context)
            
            # Test if learned optimal action
            print("Testing learned behavior...")
            good_selections = 0
            
            for i in range(50):
                context = {"feature1": 0.5}
                action = bandit.select_action(context)
                if action == "good":
                    good_selections += 1
            
            print(f"✅ Selected optimal action {good_selections}/50 times")
            
            if good_selections < 35:  # Less than 70% optimal
                self.add_bug(
                    "Poor reward learning",
                    "HIGH",
                    optimal_selections=good_selections,
                    total=50,
                    percentage=good_selections/50
                )
            
            self.record_test("reward_learning", True, {
                "optimal_rate": good_selections/50
            })
            
            # Test adaptation to reward change
            print("\nTesting adaptation to reward change...")
            
            # Change rewards
            for i in range(100):
                context = {"feature1": 0.5}
                action = bandit.select_action(context)
                
                # Reverse rewards
                if action == "bad":
                    reward = 0.9  # Now best
                elif action == "good":
                    reward = 0.1  # Now worst
                else:
                    reward = 0.5
                
                bandit.update(action, reward, context)
            
            # Check if adapted
            bad_selections = 0
            for i in range(50):
                context = {"feature1": 0.5}
                action = bandit.select_action(context)
                if action == "bad":  # Now optimal
                    bad_selections += 1
            
            if bad_selections < 20:  # Less than 40% adaptation
                self.add_bug(
                    "Poor adaptation to reward change",
                    "HIGH",
                    new_optimal_selections=bad_selections,
                    total=50
                )
            else:
                print(f"✅ Adapted to new optimal: {bad_selections}/50")
                
        except Exception as e:
            self.add_bug(
                "Exception in reward learning",
                "HIGH",
                error=str(e)
            )
            self.record_test("reward_learning", False, {"error": str(e)})
    
    def test_multi_armed_scaling(self):
        """Test scaling with many arms"""
        print("\n\nTesting Multi-Armed Scaling...")
        
        try:
            from rl_commons import ContextualBandit
            import time
            
            # Test with increasing number of arms
            arm_counts = [10, 50, 100, 500]
            
            for n_arms in arm_counts:
                print(f"\nTesting with {n_arms} arms...")
                
                start_time = time.time()
                
                bandit = ContextualBandit(
                    actions=[f"arm_{i}" for i in range(n_arms)],
                    context_features=["f1", "f2"],
                    exploration_rate=0.2
                )
                
                # Make decisions
                for i in range(100):
                    context = {"f1": random.random(), "f2": random.random()}
                    action = bandit.select_action(context)
                    reward = random.random()
                    bandit.update(action, reward, context)
                
                duration = time.time() - start_time
                decisions_per_second = 100 / duration
                
                print(f"✅ Completed in {duration:.3f}s ({decisions_per_second:.0f} decisions/sec)")
                
                self.record_test(f"scaling_{n_arms}_arms", True, {
                    "arms": n_arms,
                    "duration": duration,
                    "decisions_per_second": decisions_per_second
                })
                
                # Performance check
                if decisions_per_second < 100:  # Less than 100 decisions/sec
                    self.add_bug(
                        "Poor scaling performance",
                        "MEDIUM",
                        arms=n_arms,
                        decisions_per_second=decisions_per_second
                    )
                
                # Memory check
                if hasattr(bandit, 'get_memory_usage'):
                    memory_mb = bandit.get_memory_usage()
                    memory_per_arm = memory_mb / n_arms
                    
                    if memory_per_arm > 1:  # More than 1MB per arm
                        self.add_bug(
                            "Excessive memory usage",
                            "MEDIUM",
                            total_mb=memory_mb,
                            per_arm_mb=memory_per_arm,
                            arms=n_arms
                        )
                        
        except Exception as e:
            self.add_bug(
                "Exception in scaling test",
                "HIGH",
                error=str(e)
            )
            self.record_test("scaling_test", False, {"error": str(e)})
    
    def run_tests(self):
        """Run all tests"""
        self.test_contextual_bandit()
        self.test_reward_learning()
        self.test_multi_armed_scaling()
        return self.generate_report()


def main():
    """Run the test"""
    tester = RLCommonsDecisionTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)