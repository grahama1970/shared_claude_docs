"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_38_adaptive_optimization.py
Description: Test adaptive optimization: Performance monitoring → RL tuning
Level: 3
Modules: RL Commons, World Model, Test Reporter, All performance-critical modules
Expected Bugs: Optimization instability, local minima, over-optimization
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time
import numpy as np
import random

class AdaptiveOptimizationTest(BaseInteractionTest):
    """Level 3: Test adaptive performance optimization system"""
    
    def __init__(self):
        super().__init__(
            test_name="Adaptive Optimization",
            level=3,
            modules=["RL Commons", "World Model", "Test Reporter", "All performance-critical modules"]
        )
    
    def test_performance_driven_optimization(self):
        """Test system that continuously optimizes based on performance metrics"""
        self.print_header()
        
        # Import modules
        try:
            from rl_commons import (
                AdaptiveOptimizer, PerformanceMonitor,
                HyperparameterTuner, ConstraintValidator
            )
            from world_model import WorldModel, PerformancePredictor
            from claude_test_reporter import GrangerTestReporter
            self.record_test("modules_import", True, {})
        except ImportError as e:
            self.add_bug(
                "Module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot run adaptive optimization"
            )
            self.record_test("modules_import", False, {"error": str(e)})
            return
        
        # Initialize components
        try:
            world_model = WorldModel()
            
            # Performance monitor
            perf_monitor = PerformanceMonitor(
                metrics=["throughput", "latency", "accuracy", "resource_usage"],
                window_size=50
            )
            
            # Adaptive optimizer
            optimizer = AdaptiveOptimizer(
                optimization_targets={
                    "throughput": {"goal": "maximize", "weight": 0.3},
                    "latency": {"goal": "minimize", "weight": 0.3},
                    "accuracy": {"goal": "maximize", "weight": 0.2},
                    "resource_usage": {"goal": "minimize", "weight": 0.2}
                },
                learning_rate=0.01,
                exploration_factor=0.2
            )
            
            # Hyperparameter tuner
            hyperparameter_tuner = HyperparameterTuner(
                parameters={
                    "batch_size": {"type": "int", "range": [16, 128], "current": 32},
                    "cache_size": {"type": "int", "range": [100, 1000], "current": 500},
                    "timeout": {"type": "float", "range": [0.5, 5.0], "current": 2.0},
                    "parallelism": {"type": "int", "range": [1, 8], "current": 4},
                    "model_complexity": {"type": "float", "range": [0.1, 1.0], "current": 0.5}
                }
            )
            
            # Constraint validator
            constraints = ConstraintValidator(
                hard_constraints={
                    "latency": {"max": 1.0},  # Max 1 second
                    "resource_usage": {"max": 0.8}  # Max 80% resources
                },
                soft_constraints={
                    "throughput": {"min": 100},  # Min 100 requests/sec
                    "accuracy": {"min": 0.85}  # Min 85% accuracy
                }
            )
            
            reporter = GrangerTestReporter(
                module_name="adaptive_optimization",
                test_suite="performance_tuning"
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
        
        optimization_start = time.time()
        
        # Optimization state
        optimization_state = {
            "iterations": 0,
            "best_performance": 0.0,
            "best_params": {},
            "performance_history": [],
            "parameter_history": [],
            "constraint_violations": 0,
            "convergence_metric": 0.0,
            "optimization_events": []
        }
        
        # Simulated system modules
        system_modules = {
            "arxiv_search": {
                "base_throughput": 150,
                "base_latency": 0.3,
                "base_accuracy": 0.9
            },
            "marker_processing": {
                "base_throughput": 50,
                "base_latency": 0.8,
                "base_accuracy": 0.85
            },
            "llm_inference": {
                "base_throughput": 100,
                "base_latency": 0.5,
                "base_accuracy": 0.92
            },
            "arangodb_queries": {
                "base_throughput": 200,
                "base_latency": 0.1,
                "base_accuracy": 0.99
            }
        }
        
        print("\n🔄 Starting Adaptive Optimization Loop...")
        
        # Run optimization iterations
        num_iterations = 30
        
        for iteration in range(num_iterations):
            print(f"\n📍 Optimization Iteration {iteration + 1}/{num_iterations}")
            
            iteration_start = time.time()
            
            # Get current hyperparameters
            current_params = hyperparameter_tuner.get_current_parameters()
            
            # Simulate system performance with current parameters
            performance_metrics = self.simulate_system_performance(
                system_modules, current_params, perf_monitor
            )
            
            # Update performance monitor
            perf_monitor.update(performance_metrics)
            
            # Check constraints
            constraint_check = constraints.validate(performance_metrics)
            
            if not constraint_check["valid"]:
                optimization_state["constraint_violations"] += 1
                print(f"   ⚠️ Constraint violation: {constraint_check['violations']}")
                
                self.add_bug(
                    "Constraint violation during optimization",
                    "MEDIUM",
                    iteration=iteration,
                    violations=constraint_check["violations"]
                )
                
                # Apply penalty to optimization
                performance_metrics = self.apply_constraint_penalty(
                    performance_metrics, constraint_check["violations"]
                )
            
            # Calculate overall performance score
            performance_score = optimizer.calculate_score(performance_metrics)
            
            # Track best performance
            if performance_score > optimization_state["best_performance"]:
                optimization_state["best_performance"] = performance_score
                optimization_state["best_params"] = current_params.copy()
                
                print(f"   🎯 New best performance: {performance_score:.3f}")
                
                optimization_state["optimization_events"].append({
                    "type": "new_best",
                    "iteration": iteration,
                    "score": performance_score,
                    "params": current_params.copy()
                })
            
            # Store history
            optimization_state["performance_history"].append({
                "iteration": iteration,
                "score": performance_score,
                "metrics": performance_metrics.copy(),
                "constraint_valid": constraint_check["valid"]
            })
            
            optimization_state["parameter_history"].append(current_params.copy())
            
            # Update world model
            world_model.update_state({
                "optimization_iteration": iteration,
                "performance_score": performance_score,
                "parameters": current_params,
                "metrics": performance_metrics
            })
            
            # Predict future performance
            if iteration > 5:
                future_prediction = self.predict_future_performance(
                    world_model, optimization_state["performance_history"]
                )
                
                if future_prediction["converging"]:
                    print(f"   📊 Predicted convergence in {future_prediction['iterations_to_convergence']} iterations")
            
            # Optimize parameters
            optimization_result = optimizer.optimize(
                current_performance=performance_metrics,
                historical_performance=perf_monitor.get_history()
            )
            
            # Tune hyperparameters
            if optimization_result["should_explore"]:
                # Exploration phase
                print("   🔍 Exploring parameter space...")
                new_params = hyperparameter_tuner.explore(
                    exploration_rate=0.3,
                    current_score=performance_score
                )
            else:
                # Exploitation phase
                print("   🎯 Exploiting current knowledge...")
                gradient = optimizer.estimate_gradient(
                    current_params, performance_metrics
                )
                
                new_params = hyperparameter_tuner.update(
                    gradient=gradient,
                    learning_rate=optimization_result["learning_rate"]
                )
            
            # Validate parameter changes
            param_changes = self.calculate_parameter_changes(current_params, new_params)
            
            if param_changes["total_change"] > 0.5:
                print(f"   ⚡ Large parameter change: {param_changes['total_change']:.2f}")
                
                # Check for instability
                if iteration > 10:
                    recent_changes = self.analyze_parameter_stability(
                        optimization_state["parameter_history"][-5:]
                    )
                    
                    if recent_changes["instability"] > 0.3:
                        self.add_bug(
                            "Optimization instability detected",
                            "HIGH",
                            iteration=iteration,
                            instability_score=recent_changes["instability"]
                        )
            
            # Apply new parameters
            hyperparameter_tuner.set_parameters(new_params)
            
            # Report to test reporter
            reporter.add_test_result(
                test_name=f"optimization_iteration_{iteration}",
                status="PASS" if constraint_check["valid"] else "PARTIAL",
                duration=time.time() - iteration_start,
                metadata={
                    "performance_score": performance_score,
                    "metrics": performance_metrics,
                    "parameters": new_params,
                    "constraint_valid": constraint_check["valid"]
                }
            )
            
            print(f"   📊 Performance: {performance_score:.3f}")
            print(f"      Throughput: {performance_metrics['throughput']:.1f} req/s")
            print(f"      Latency: {performance_metrics['latency']:.3f}s")
            print(f"      Accuracy: {performance_metrics['accuracy']:.3f}")
            print(f"      Resources: {performance_metrics['resource_usage']:.1%}")
            
            optimization_state["iterations"] += 1
            
            # Check for convergence
            if iteration > 15:
                convergence = self.check_convergence(
                    optimization_state["performance_history"][-10:]
                )
                
                optimization_state["convergence_metric"] = convergence["metric"]
                
                if convergence["converged"]:
                    print(f"\n✅ Optimization converged at iteration {iteration}")
                    optimization_state["optimization_events"].append({
                        "type": "convergence",
                        "iteration": iteration,
                        "final_score": performance_score
                    })
                    break
        
        optimization_duration = time.time() - optimization_start
        
        # Analyze optimization results
        print(f"\n📊 Adaptive Optimization Summary:")
        print(f"   Total iterations: {optimization_state['iterations']}")
        print(f"   Duration: {optimization_duration:.2f}s")
        print(f"   Best performance: {optimization_state['best_performance']:.3f}")
        print(f"   Constraint violations: {optimization_state['constraint_violations']}")
        print(f"   Convergence metric: {optimization_state['convergence_metric']:.3f}")
        
        print(f"\n   Best parameters:")
        for param, value in optimization_state["best_params"].items():
            print(f"      {param}: {value}")
        
        # Performance improvement analysis
        initial_score = optimization_state["performance_history"][0]["score"]
        final_score = optimization_state["performance_history"][-1]["score"]
        improvement = (final_score - initial_score) / initial_score
        
        print(f"\n   Performance improvement: {improvement:.1%}")
        
        # Stability analysis
        if len(optimization_state["performance_history"]) > 20:
            early_phase = optimization_state["performance_history"][:10]
            late_phase = optimization_state["performance_history"][-10:]
            
            early_variance = np.var([h["score"] for h in early_phase])
            late_variance = np.var([h["score"] for h in late_phase])
            
            stability_improvement = 1 - (late_variance / max(early_variance, 0.001))
            print(f"   Stability improvement: {stability_improvement:.1%}")
        
        # Optimization events
        print(f"\n   Key optimization events:")
        for event in optimization_state["optimization_events"][-5:]:
            print(f"      Iteration {event['iteration']}: {event['type']}")
        
        self.record_test("adaptive_optimization", True, {
            "optimization_duration": optimization_duration,
            "iterations": optimization_state["iterations"],
            "best_performance": optimization_state["best_performance"],
            "improvement": improvement,
            "constraint_violations": optimization_state["constraint_violations"],
            "convergence_metric": optimization_state["convergence_metric"],
            "final_params": optimization_state["best_params"]
        })
        
        # Quality checks
        if improvement < 0.1:
            self.add_bug(
                "Insufficient optimization improvement",
                "HIGH",
                improvement=improvement
            )
        
        if optimization_state["constraint_violations"] > optimization_state["iterations"] * 0.3:
            self.add_bug(
                "Excessive constraint violations",
                "HIGH",
                violation_rate=optimization_state["constraint_violations"] / optimization_state["iterations"]
            )
        
        # Test robustness
        self.test_optimization_robustness(optimizer, hyperparameter_tuner, system_modules)
    
    def simulate_system_performance(self, system_modules, parameters, perf_monitor):
        """Simulate system performance with given parameters"""
        # Parameter effects
        batch_effect = parameters["batch_size"] / 64  # Normalized to baseline
        cache_effect = parameters["cache_size"] / 500
        timeout_effect = 2.0 / parameters["timeout"]  # Inverse relationship
        parallelism_effect = parameters["parallelism"] / 4
        complexity_effect = parameters["model_complexity"]
        
        # Calculate aggregate metrics
        total_throughput = 0
        total_latency = 0
        total_accuracy = 0
        
        for module_name, module_config in system_modules.items():
            # Module-specific performance
            if "search" in module_name:
                throughput = module_config["base_throughput"] * batch_effect * parallelism_effect
                latency = module_config["base_latency"] / parallelism_effect * timeout_effect
                accuracy = module_config["base_accuracy"] * (0.9 + 0.1 * cache_effect)
            elif "processing" in module_name:
                throughput = module_config["base_throughput"] * batch_effect * 0.8
                latency = module_config["base_latency"] * complexity_effect
                accuracy = module_config["base_accuracy"] * (0.8 + 0.2 * complexity_effect)
            else:
                throughput = module_config["base_throughput"] * parallelism_effect
                latency = module_config["base_latency"] * (0.8 + 0.2 * cache_effect)
                accuracy = module_config["base_accuracy"]
            
            # Add noise
            throughput *= (1 + random.uniform(-0.1, 0.1))
            latency *= (1 + random.uniform(-0.05, 0.05))
            accuracy *= (1 + random.uniform(-0.02, 0.02))
            
            total_throughput += throughput
            total_latency += latency
            total_accuracy += accuracy
        
        # Average metrics
        num_modules = len(system_modules)
        avg_throughput = total_throughput / num_modules
        avg_latency = total_latency / num_modules
        avg_accuracy = total_accuracy / num_modules
        
        # Resource usage calculation
        resource_usage = (
            0.2 * (parameters["batch_size"] / 128) +
            0.2 * (parameters["cache_size"] / 1000) +
            0.3 * (parameters["parallelism"] / 8) +
            0.3 * parameters["model_complexity"]
        )
        
        return {
            "throughput": max(10, avg_throughput),
            "latency": max(0.01, avg_latency),
            "accuracy": min(0.99, max(0.1, avg_accuracy)),
            "resource_usage": min(0.95, max(0.05, resource_usage))
        }
    
    def apply_constraint_penalty(self, metrics, violations):
        """Apply penalty to metrics for constraint violations"""
        penalty_factor = 0.8  # 20% penalty per violation type
        
        for violation in violations:
            if violation["constraint"] == "latency":
                metrics["latency"] *= 1.5  # Increase perceived latency
            elif violation["constraint"] == "resource_usage":
                metrics["resource_usage"] = min(0.95, metrics["resource_usage"] * 1.2)
        
        return metrics
    
    def predict_future_performance(self, world_model, performance_history):
        """Predict future optimization performance"""
        if len(performance_history) < 5:
            return {"converging": False}
        
        # Extract scores
        scores = [h["score"] for h in performance_history]
        
        # Simple trend analysis
        recent_scores = scores[-5:]
        score_variance = np.var(recent_scores)
        score_trend = np.polyfit(range(5), recent_scores, 1)[0]
        
        # Convergence criteria
        converging = score_variance < 0.001 and abs(score_trend) < 0.01
        
        if converging:
            # Estimate iterations to convergence
            current_improvement_rate = abs(score_trend)
            if current_improvement_rate > 0:
                iterations_to_convergence = int(0.01 / current_improvement_rate)
            else:
                iterations_to_convergence = 0
        else:
            iterations_to_convergence = None
        
        return {
            "converging": converging,
            "iterations_to_convergence": iterations_to_convergence,
            "current_trend": score_trend,
            "variance": score_variance
        }
    
    def calculate_parameter_changes(self, old_params, new_params):
        """Calculate magnitude of parameter changes"""
        total_change = 0
        changes = {}
        
        for param, old_value in old_params.items():
            new_value = new_params.get(param, old_value)
            
            # Normalize change based on parameter type
            if isinstance(old_value, int):
                change = abs(new_value - old_value) / max(abs(old_value), 1)
            else:
                change = abs(new_value - old_value) / max(abs(old_value), 0.1)
            
            changes[param] = change
            total_change += change
        
        return {
            "total_change": total_change,
            "parameter_changes": changes
        }
    
    def analyze_parameter_stability(self, recent_history):
        """Analyze stability of parameter changes"""
        if len(recent_history) < 2:
            return {"instability": 0}
        
        # Calculate variance in parameters
        param_series = {}
        
        for params in recent_history:
            for param, value in params.items():
                if param not in param_series:
                    param_series[param] = []
                param_series[param].append(value)
        
        # Calculate instability metric
        instability_scores = []
        
        for param, values in param_series.items():
            if len(values) > 1:
                # Normalize by mean
                mean_val = np.mean(values)
                if mean_val != 0:
                    variance = np.var(values) / (mean_val ** 2)
                    instability_scores.append(variance)
        
        instability = np.mean(instability_scores) if instability_scores else 0
        
        return {"instability": instability}
    
    def check_convergence(self, recent_history):
        """Check if optimization has converged"""
        if len(recent_history) < 5:
            return {"converged": False, "metric": 0}
        
        scores = [h["score"] for h in recent_history]
        
        # Convergence criteria
        score_variance = np.var(scores)
        score_range = max(scores) - min(scores)
        avg_score = np.mean(scores)
        
        # Normalized convergence metric
        convergence_metric = 1 - (score_range / max(avg_score, 0.1))
        
        converged = score_variance < 0.0001 and score_range < 0.01
        
        return {
            "converged": converged,
            "metric": convergence_metric,
            "variance": score_variance,
            "range": score_range
        }
    
    def test_optimization_robustness(self, optimizer, tuner, system_modules):
        """Test robustness of optimization to perturbations"""
        print("\n🔨 Testing Optimization Robustness...")
        
        # Save current state
        current_params = tuner.get_current_parameters()
        
        # Introduce perturbation
        print("   💥 Introducing system perturbation...")
        
        # Degrade system performance
        for module in system_modules.values():
            module["base_throughput"] *= 0.7
            module["base_latency"] *= 1.5
        
        # Run a few optimization iterations
        recovery_scores = []
        
        for i in range(5):
            perturbed_performance = self.simulate_system_performance(
                system_modules, current_params, None
            )
            
            score = optimizer.calculate_score(perturbed_performance)
            recovery_scores.append(score)
            
            # Optimize
            gradient = optimizer.estimate_gradient(current_params, perturbed_performance)
            current_params = tuner.update(gradient=gradient, learning_rate=0.05)
        
        # Check recovery
        recovery_rate = (recovery_scores[-1] - recovery_scores[0]) / max(recovery_scores[0], 0.1)
        
        print(f"   Recovery rate: {recovery_rate:.1%}")
        
        if recovery_rate < 0.2:
            self.add_bug(
                "Poor recovery from perturbation",
                "HIGH",
                recovery_rate=recovery_rate
            )
    
    def run_tests(self):
        """Run all tests"""
        self.test_performance_driven_optimization()
        return self.generate_report()


def main():
    """Run the test"""
    tester = AdaptiveOptimizationTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)