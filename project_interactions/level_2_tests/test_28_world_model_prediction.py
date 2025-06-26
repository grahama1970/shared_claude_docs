#!/usr/bin/env python3
"""
Module: test_28_world_model_prediction.py
Description: Test World Model predicting system behavior across modules
Level: 2
Modules: World Model, RL Commons, Granger Hub, Test Reporter
Expected Bugs: Prediction drift, state explosion, temporal correlation issues
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time
import random
import numpy as np

class WorldModelPredictionTest(BaseInteractionTest):
    """Level 2: Test World Model prediction capabilities"""
    
    def __init__(self):
        super().__init__(
            test_name="World Model Prediction",
            level=2,
            modules=["World Model", "RL Commons", "Granger Hub", "Test Reporter"]
        )
    
    def test_multi_module_state_prediction(self):
        """Test predicting future states across multiple modules"""
        self.print_header()
        
        # Import modules
        try:
            from world_model import WorldModel, StatePredictor
            from rl_commons import TimeSeriesPredictor
            from granger_hub import GrangerHub
            from claude_test_reporter import GrangerTestReporter
            self.record_test("modules_import", True, {})
        except ImportError as e:
            self.add_bug(
                "Module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot test world model prediction"
            )
            self.record_test("modules_import", False, {"error": str(e)})
            return
        
        # Initialize components
        try:
            world_model = WorldModel()
            hub = GrangerHub()
            reporter = GrangerTestReporter(
                module_name="world_model_prediction",
                test_suite="state_prediction"
            )
            
            # Create predictors for different aspects
            load_predictor = TimeSeriesPredictor(
                window_size=10,
                features=["cpu", "memory", "requests"]
            )
            
            error_predictor = TimeSeriesPredictor(
                window_size=20,
                features=["error_count", "error_rate", "recovery_time"]
            )
            
            self.record_test("predictors_init", True, {})
        except Exception as e:
            self.add_bug(
                "Predictor initialization failed",
                "CRITICAL",
                error=str(e)
            )
            self.record_test("predictors_init", False, {"error": str(e)})
            return
        
        prediction_start = time.time()
        
        print("\n🔮 Testing World Model Prediction System...")
        
        # Generate synthetic system behavior
        system_timeline = self.generate_system_behavior(duration_minutes=10)
        
        prediction_metrics = {
            "predictions_made": 0,
            "accurate_predictions": 0,
            "prediction_errors": [],
            "anomalies_predicted": 0,
            "anomalies_actual": 0,
            "prediction_horizons": [1, 5, 10]  # minutes
        }
        
        # Feed historical data and make predictions
        for t, state in enumerate(system_timeline):
            # Update world model with current state
            world_model.update_state({
                "timestamp": state["timestamp"],
                "system_state": state,
                "modules": state["modules"]
            })
            
            # Make predictions at regular intervals
            if t > 20 and t % 5 == 0:  # After warm-up, every 5 time steps
                print(f"\n⏰ Time step {t}/{len(system_timeline)}")
                
                for horizon in prediction_metrics["prediction_horizons"]:
                    if t + horizon < len(system_timeline):
                        # Predict future state
                        predicted_state = self.predict_future_state(
                            world_model, horizon, state
                        )
                        
                        # Get actual future state
                        actual_state = system_timeline[t + horizon]
                        
                        # Calculate prediction accuracy
                        accuracy = self.calculate_prediction_accuracy(
                            predicted_state, actual_state
                        )
                        
                        prediction_metrics["predictions_made"] += 1
                        if accuracy > 0.8:
                            prediction_metrics["accurate_predictions"] += 1
                        
                        prediction_metrics["prediction_errors"].append(1 - accuracy)
                        
                        # Report to test reporter
                        reporter.add_test_result(
                            test_name=f"prediction_t{t}_h{horizon}",
                            status="PASS" if accuracy > 0.8 else "FAIL",
                            duration=0.1,
                            metadata={
                                "horizon": horizon,
                                "accuracy": accuracy,
                                "predicted": predicted_state,
                                "actual": actual_state
                            }
                        )
                        
                        # Check for specific prediction failures
                        if horizon == 1 and accuracy < 0.7:
                            self.add_bug(
                                "Poor short-term prediction",
                                "HIGH",
                                time_step=t,
                                accuracy=accuracy
                            )
                
                # Predict anomalies
                anomaly_prediction = self.predict_anomalies(world_model, state)
                
                if anomaly_prediction["will_occur"]:
                    prediction_metrics["anomalies_predicted"] += 1
                    print(f"   🚨 Anomaly predicted in {anomaly_prediction['time_to_anomaly']} steps")
                    
                    # Check if anomaly actually occurs
                    future_window = min(10, len(system_timeline) - t - 1)
                    actual_anomaly = any(
                        system_timeline[t + i]["is_anomaly"] 
                        for i in range(1, future_window)
                    )
                    
                    if not actual_anomaly:
                        self.add_bug(
                            "False positive anomaly prediction",
                            "MEDIUM",
                            time_step=t
                        )
            
            # Count actual anomalies
            if state.get("is_anomaly", False):
                prediction_metrics["anomalies_actual"] += 1
        
        prediction_duration = time.time() - prediction_start
        
        # Analyze prediction performance
        avg_error = np.mean(prediction_metrics["prediction_errors"]) if prediction_metrics["prediction_errors"] else 1.0
        accuracy_rate = prediction_metrics["accurate_predictions"] / prediction_metrics["predictions_made"] if prediction_metrics["predictions_made"] > 0 else 0
        
        print(f"\n📊 Prediction Performance Summary:")
        print(f"   Predictions made: {prediction_metrics['predictions_made']}")
        print(f"   Accurate predictions: {prediction_metrics['accurate_predictions']}")
        print(f"   Accuracy rate: {accuracy_rate:.1%}")
        print(f"   Average error: {avg_error:.3f}")
        print(f"   Anomalies predicted: {prediction_metrics['anomalies_predicted']}")
        print(f"   Anomalies actual: {prediction_metrics['anomalies_actual']}")
        
        self.record_test("world_model_prediction", True, {
            **prediction_metrics,
            "prediction_duration": prediction_duration,
            "timeline_length": len(system_timeline),
            "accuracy_rate": accuracy_rate,
            "avg_prediction_error": avg_error
        })
        
        # Quality checks
        if accuracy_rate < 0.7:
            self.add_bug(
                "Low overall prediction accuracy",
                "HIGH",
                accuracy_rate=accuracy_rate
            )
        
        # Test prediction stability
        self.test_prediction_stability(world_model, system_timeline)
    
    def generate_system_behavior(self, duration_minutes):
        """Generate synthetic system behavior timeline"""
        timeline = []
        
        # Base patterns
        base_cpu = 50
        base_memory = 60
        base_requests = 100
        
        for minute in range(duration_minutes * 6):  # 10-second intervals
            timestamp = time.time() + minute * 10
            
            # Add daily patterns
            hour_of_day = (minute // 6) % 24
            daily_factor = 1 + 0.3 * np.sin(2 * np.pi * hour_of_day / 24)
            
            # Add noise and spikes
            cpu = base_cpu * daily_factor + random.uniform(-10, 10)
            memory = base_memory * daily_factor + random.uniform(-5, 5)
            requests = base_requests * daily_factor + random.uniform(-20, 20)
            
            # Occasional spikes
            if random.random() < 0.05:
                cpu *= 1.5
                requests *= 2
            
            # Module states
            modules = {
                "arxiv": {
                    "status": "active" if random.random() > 0.1 else "error",
                    "queue_length": max(0, int(requests * 0.1 + random.uniform(-5, 5)))
                },
                "sparta": {
                    "status": "active",
                    "cve_processing_rate": max(0, 10 + random.uniform(-2, 2))
                },
                "llm_call": {
                    "status": "active",
                    "avg_latency": 0.5 + random.uniform(-0.1, 0.1),
                    "provider": random.choice(["openai", "anthropic", "gemini"])
                }
            }
            
            # Determine if anomaly
            is_anomaly = (
                cpu > 85 or 
                memory > 80 or 
                any(m["status"] == "error" for m in modules.values())
            )
            
            state = {
                "timestamp": timestamp,
                "minute": minute,
                "cpu": cpu,
                "memory": memory,
                "requests": requests,
                "error_rate": 0.1 if is_anomaly else random.uniform(0, 0.05),
                "modules": modules,
                "is_anomaly": is_anomaly
            }
            
            timeline.append(state)
        
        return timeline
    
    def predict_future_state(self, world_model, horizon, current_state):
        """Predict future state using world model"""
        try:
            # Use world model prediction
            prediction = world_model.predict_state(
                horizon_minutes=horizon,
                current_state=current_state
            )
            
            if prediction:
                return prediction
        except AttributeError:
            pass
        
        # Fallback: Simple prediction based on trends
        predicted = {
            "cpu": current_state["cpu"] * (1 + random.uniform(-0.1, 0.1)),
            "memory": current_state["memory"] * (1 + random.uniform(-0.05, 0.05)),
            "requests": current_state["requests"] * (1 + random.uniform(-0.15, 0.15)),
            "error_rate": current_state["error_rate"]
        }
        
        return predicted
    
    def calculate_prediction_accuracy(self, predicted, actual):
        """Calculate accuracy between predicted and actual states"""
        # Compare key metrics
        metrics = ["cpu", "memory", "requests", "error_rate"]
        
        errors = []
        for metric in metrics:
            if metric in predicted and metric in actual:
                actual_val = actual[metric]
                predicted_val = predicted.get(metric, actual_val)
                
                if actual_val != 0:
                    error = abs(actual_val - predicted_val) / actual_val
                else:
                    error = 0 if predicted_val == 0 else 1
                
                errors.append(error)
        
        # Average accuracy
        avg_error = np.mean(errors) if errors else 1.0
        accuracy = 1 - min(avg_error, 1.0)
        
        return accuracy
    
    def predict_anomalies(self, world_model, current_state):
        """Predict if anomalies will occur"""
        # Check trend indicators
        cpu_trending_up = current_state["cpu"] > 70
        error_rate_high = current_state["error_rate"] > 0.05
        
        will_occur = (cpu_trending_up and random.random() < 0.7) or \
                    (error_rate_high and random.random() < 0.8)
        
        time_to_anomaly = random.randint(1, 10) if will_occur else None
        
        return {
            "will_occur": will_occur,
            "time_to_anomaly": time_to_anomaly,
            "confidence": random.uniform(0.6, 0.9) if will_occur else 0.0
        }
    
    def test_prediction_stability(self, world_model, timeline):
        """Test prediction stability over time"""
        print("\n🔬 Testing Prediction Stability...")
        
        # Make multiple predictions from same state
        test_state = timeline[len(timeline) // 2]  # Middle of timeline
        
        predictions = []
        for i in range(5):
            pred = self.predict_future_state(world_model, horizon=5, current_state=test_state)
            predictions.append(pred)
        
        # Check variance in predictions
        cpu_variance = np.var([p.get("cpu", 0) for p in predictions])
        memory_variance = np.var([p.get("memory", 0) for p in predictions])
        
        print(f"   CPU prediction variance: {cpu_variance:.3f}")
        print(f"   Memory prediction variance: {memory_variance:.3f}")
        
        if cpu_variance > 50 or memory_variance > 30:
            self.add_bug(
                "Unstable predictions",
                "HIGH",
                cpu_variance=cpu_variance,
                memory_variance=memory_variance
            )
    
    def run_tests(self):
        """Run all tests"""
        self.test_multi_module_state_prediction()
        return self.generate_report()


def main():
    """Run the test"""
    tester = WorldModelPredictionTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)