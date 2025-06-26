"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_16_world_model_rl_pipeline.py
Description: Test World Model → RL Commons optimization pipeline
Level: 1
Modules: World Model, RL Commons, Test Reporter
Expected Bugs: State prediction errors, reward calculation issues, convergence problems
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time
import random

class WorldModelRLPipelineTest(BaseInteractionTest):
    """Level 1: Test World Model to RL Commons pipeline"""
    
    def __init__(self):
        super().__init__(
            test_name="World Model RL Pipeline",
            level=1,
            modules=["World Model", "RL Commons", "Test Reporter"]
        )
    
    def test_state_based_optimization(self):
        """Test using world model states for RL optimization"""
        self.print_header()
        
        # Import modules
        try:
            from world_model import WorldModel
            from rl_commons import ContextualBandit, OptimizationAgent
            self.record_test("modules_import", True, {})
        except ImportError as e:
            self.add_bug(
                "Module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot run pipeline"
            )
            self.record_test("modules_import", False, {"error": str(e)})
            return
        
        # Initialize components
        try:
            world_model = WorldModel()
            rl_agent = OptimizationAgent(
                actions=["scale_up", "scale_down", "maintain", "restart"],
                state_features=["cpu", "memory", "requests", "errors"]
            )
            self.record_test("components_init", True, {})
        except Exception as e:
            self.add_bug(
                "Component initialization failed",
                "CRITICAL",
                error=str(e)
            )
            self.record_test("components_init", False, {"error": str(e)})
            return
        
        # Test optimization scenarios
        test_scenarios = [
            {
                "name": "High load optimization",
                "states": [
                    {"cpu": 85, "memory": 70, "requests": 1000, "errors": 5},
                    {"cpu": 90, "memory": 80, "requests": 1200, "errors": 10},
                    {"cpu": 95, "memory": 85, "requests": 1500, "errors": 20}
                ],
                "expected_action": "scale_up"
            },
            {
                "name": "Low load optimization",
                "states": [
                    {"cpu": 10, "memory": 15, "requests": 50, "errors": 0},
                    {"cpu": 8, "memory": 12, "requests": 30, "errors": 0},
                    {"cpu": 5, "memory": 10, "requests": 20, "errors": 0}
                ],
                "expected_action": "scale_down"
            },
            {
                "name": "Error spike handling",
                "states": [
                    {"cpu": 50, "memory": 60, "requests": 500, "errors": 5},
                    {"cpu": 55, "memory": 65, "requests": 600, "errors": 50},
                    {"cpu": 60, "memory": 70, "requests": 700, "errors": 100}
                ],
                "expected_action": "restart"
            }
        ]
        
        for scenario in test_scenarios:
            print(f"\nTesting: {scenario['name']}")
            pipeline_start = time.time()
            
            try:
                # Step 1: Feed states to world model
                print("Updating world model with states...")
                
                for state in scenario["states"]:
                    world_model.update_state({
                        "module": "test_service",
                        "timestamp": time.time(),
                        **state
                    })
                    time.sleep(0.1)  # Simulate time passing
                
                # Step 2: Get world model prediction
                print("Getting world model prediction...")
                
                prediction = world_model.predict_next_state("test_service")
                
                if prediction:
                    print(f"✅ Predicted next state:")
                    print(f"   CPU: {prediction.get('cpu', 'N/A')}")
                    print(f"   Memory: {prediction.get('memory', 'N/A')}")
                else:
                    self.add_bug(
                        "World model prediction failed",
                        "HIGH",
                        scenario=scenario["name"]
                    )
                    prediction = scenario["states"][-1]  # Use last state as fallback
                
                # Step 3: Use RL to decide action
                print("RL agent deciding action...")
                
                # Convert state to context for RL
                context = {
                    "cpu": prediction.get("cpu", 50),
                    "memory": prediction.get("memory", 50),
                    "requests": prediction.get("requests", 100),
                    "errors": prediction.get("errors", 0)
                }
                
                action = rl_agent.select_action(context)
                
                print(f"✅ RL selected action: {action}")
                
                # Step 4: Simulate action execution and get reward
                print("Simulating action execution...")
                
                # Simulate outcome based on action
                if action == "scale_up" and scenario["expected_action"] == "scale_up":
                    reward = 0.9  # Good decision
                    new_cpu = context["cpu"] * 0.6  # Load distributed
                elif action == "scale_down" and scenario["expected_action"] == "scale_down":
                    reward = 0.8  # Good decision
                    new_cpu = context["cpu"] * 1.2  # Slightly increased load
                elif action == "restart" and scenario["expected_action"] == "restart":
                    reward = 0.7  # Good decision
                    new_errors = 0  # Errors cleared
                else:
                    reward = 0.2  # Poor decision
                
                # Update RL agent with reward
                rl_agent.update(action, reward, context)
                
                # Record results
                self.record_test(f"pipeline_{scenario['name']}", True, {
                    "states_processed": len(scenario["states"]),
                    "prediction_made": prediction is not None,
                    "action_selected": action,
                    "expected_action": scenario["expected_action"],
                    "reward": reward,
                    "total_time": time.time() - pipeline_start
                })
                
                # Check decision quality
                if action != scenario["expected_action"]:
                    self.add_bug(
                        "Suboptimal action selected",
                        "MEDIUM",
                        scenario=scenario["name"],
                        selected=action,
                        expected=scenario["expected_action"],
                        context=context
                    )
                
            except Exception as e:
                self.add_bug(
                    f"Pipeline exception for {scenario['name']}",
                    "HIGH",
                    error=str(e)
                )
                self.record_test(f"pipeline_{scenario['name']}", False, {"error": str(e)})
    
    def test_continuous_learning(self):
        """Test continuous learning from world model feedback"""
        print("\n\nTesting Continuous Learning...")
        
        try:
            from world_model import WorldModel
            from rl_commons import ContextualBandit
            
            world_model = WorldModel()
            bandit = ContextualBandit(
                actions=["aggressive", "moderate", "conservative"],
                context_features=["volatility", "trend", "volume"]
            )
            
            print("Running continuous learning loop...")
            
            learning_metrics = {
                "decisions": [],
                "rewards": [],
                "accuracy": []
            }
            
            # Simulate 50 time steps
            for t in range(50):
                # Generate market-like state
                volatility = random.uniform(0, 1)
                trend = random.uniform(-1, 1)
                volume = random.uniform(0, 1000)
                
                # Update world model
                world_model.update_state({
                    "module": "market_predictor",
                    "timestamp": time.time() + t,
                    "volatility": volatility,
                    "trend": trend,
                    "volume": volume
                })
                
                # Get RL decision
                context = {
                    "volatility": volatility,
                    "trend": trend,
                    "volume": volume / 1000  # Normalize
                }
                
                action = bandit.select_action(context)
                
                # Calculate reward based on "market" response
                if volatility > 0.7:  # High volatility
                    reward = 0.9 if action == "conservative" else 0.2
                elif trend > 0.5:  # Strong uptrend
                    reward = 0.8 if action == "aggressive" else 0.4
                else:  # Normal conditions
                    reward = 0.7 if action == "moderate" else 0.3
                
                # Update RL with reward
                bandit.update(action, reward, context)
                
                # Track metrics
                learning_metrics["decisions"].append(action)
                learning_metrics["rewards"].append(reward)
                
                # Calculate rolling accuracy (last 10 decisions)
                if len(learning_metrics["rewards"]) >= 10:
                    recent_avg = sum(learning_metrics["rewards"][-10:]) / 10
                    learning_metrics["accuracy"].append(recent_avg)
            
            # Analyze learning progress
            print(f"\n✅ Completed {len(learning_metrics['decisions'])} decisions")
            print(f"Average reward: {sum(learning_metrics['rewards'])/len(learning_metrics['rewards']):.3f}")
            
            if learning_metrics["accuracy"]:
                improvement = learning_metrics["accuracy"][-1] - learning_metrics["accuracy"][0]
                print(f"Learning improvement: {improvement:.3f}")
                
                self.record_test("continuous_learning", True, {
                    "decisions": len(learning_metrics["decisions"]),
                    "avg_reward": sum(learning_metrics["rewards"])/len(learning_metrics["rewards"]),
                    "improvement": improvement
                })
                
                # Check learning quality
                if improvement < 0:
                    self.add_bug(
                        "Negative learning (performance degraded)",
                        "HIGH",
                        initial_accuracy=learning_metrics["accuracy"][0],
                        final_accuracy=learning_metrics["accuracy"][-1]
                    )
                elif improvement < 0.1:
                    self.add_bug(
                        "Minimal learning improvement",
                        "MEDIUM",
                        improvement=improvement
                    )
            
        except Exception as e:
            self.add_bug(
                "Exception in continuous learning",
                "HIGH",
                error=str(e)
            )
            self.record_test("continuous_learning", False, {"error": str(e)})
    
    def test_anomaly_driven_optimization(self):
        """Test optimization triggered by anomaly detection"""
        print("\n\nTesting Anomaly-Driven Optimization...")
        
        try:
            from world_model import WorldModel
            from rl_commons import OptimizationAgent
            
            world_model = WorldModel()
            optimizer = OptimizationAgent(
                actions=["investigate", "mitigate", "escalate", "ignore"],
                state_features=["anomaly_score", "severity", "frequency", "impact"]
            )
            
            # Test anomaly scenarios
            anomaly_scenarios = [
                {
                    "name": "Memory leak",
                    "pattern": [
                        {"memory": 100, "cpu": 50},
                        {"memory": 200, "cpu": 50},
                        {"memory": 400, "cpu": 50},
                        {"memory": 800, "cpu": 50}
                    ],
                    "expected_action": "mitigate"
                },
                {
                    "name": "DDoS attack",
                    "pattern": [
                        {"requests": 100, "errors": 1},
                        {"requests": 10000, "errors": 500},
                        {"requests": 50000, "errors": 2000},
                        {"requests": 100000, "errors": 5000}
                    ],
                    "expected_action": "escalate"
                },
                {
                    "name": "Normal fluctuation",
                    "pattern": [
                        {"cpu": 40, "memory": 300},
                        {"cpu": 60, "memory": 350},
                        {"cpu": 45, "memory": 320},
                        {"cpu": 50, "memory": 330}
                    ],
                    "expected_action": "ignore"
                }
            ]
            
            for scenario in anomaly_scenarios:
                print(f"\nTesting: {scenario['name']}")
                
                # Feed pattern to world model
                for i, state in enumerate(scenario["pattern"]):
                    world_model.update_state({
                        "module": "monitored_service",
                        "timestamp": time.time() + i,
                        **state
                    })
                
                # Detect anomaly
                anomaly_score = world_model.detect_anomaly({
                    "module": "monitored_service",
                    **scenario["pattern"][-1]
                })
                
                if isinstance(anomaly_score, bool):
                    anomaly_score = 1.0 if anomaly_score else 0.0
                
                print(f"Anomaly score: {anomaly_score:.2f}")
                
                # Prepare context for optimization
                context = {
                    "anomaly_score": anomaly_score,
                    "severity": min(anomaly_score * 2, 1.0),  # Derived
                    "frequency": len(scenario["pattern"]) / 10,  # Normalized
                    "impact": anomaly_score * 0.8  # Estimated impact
                }
                
                # Get optimization decision
                action = optimizer.select_action(context)
                
                print(f"Optimizer action: {action}")
                
                self.record_test(f"anomaly_{scenario['name']}", True, {
                    "anomaly_score": anomaly_score,
                    "action": action,
                    "expected": scenario["expected_action"]
                })
                
                # Check decision quality
                if action != scenario["expected_action"]:
                    self.add_bug(
                        "Incorrect anomaly response",
                        "HIGH",
                        scenario=scenario["name"],
                        selected=action,
                        expected=scenario["expected_action"],
                        anomaly_score=anomaly_score
                    )
                
                # Simulate feedback
                if action == scenario["expected_action"]:
                    reward = 0.9
                else:
                    reward = 0.2
                
                optimizer.update(action, reward, context)
                
        except Exception as e:
            self.add_bug(
                "Exception in anomaly-driven optimization",
                "HIGH",
                error=str(e)
            )
            self.record_test("anomaly_optimization", False, {"error": str(e)})
    
    def run_tests(self):
        """Run all tests"""
        self.test_state_based_optimization()
        self.test_continuous_learning()
        self.test_anomaly_driven_optimization()
        return self.generate_report()


def main():
    """Run the test"""
    tester = WorldModelRLPipelineTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)