#!/usr/bin/env python3
"""
Module: test_08_world_model_state_tracking.py
Description: Test World Model state tracking and prediction with verification
Level: 0
Modules: World Model, Test Reporter
Expected Bugs: State persistence issues, prediction accuracy, memory leaks
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')
sys.path.insert(0, '/home/graham/workspace/experiments/world_model/src')

from base_interaction_test import BaseInteractionTest
import time

class WorldModelStateTrackingTest(BaseInteractionTest):
    """Level 0: Test World Model state tracking functionality"""
    
    def __init__(self):
        super().__init__(
            test_name="World Model State Tracking",
            level=0,
            modules=["World Model", "Test Reporter"]
        )
    
    def test_state_tracking(self):
        """Test tracking various system states"""
        self.print_header()
        
        # Import World Model
        try:
            from world_model import WorldModel, SystemState
            self.record_test("world_model_import", True, {})
        except ImportError as e:
            self.add_bug(
                "World Model module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot use World Model functionality"
            )
            self.record_test("world_model_import", False, {"error": str(e)})
            return
        
        # Initialize world model
        try:
            model = WorldModel()
            self.record_test("world_model_init", True, {})
        except Exception as e:
            self.add_bug(
                "World Model initialization failure",
                "CRITICAL",
                error=str(e)
            )
            self.record_test("world_model_init", False, {"error": str(e)})
            return
        
        # Test state tracking scenarios
        test_states = [
            {
                "name": "Normal module state",
                "state": {
                    "module": "arxiv-mcp-server",
                    "status": "running",
                    "cpu": 15.5,
                    "memory": 256.7,
                    "requests": 42
                }
            },
            {
                "name": "Error state",
                "state": {
                    "module": "marker",
                    "status": "error",
                    "error": "PDF parsing failed",
                    "error_count": 5
                }
            },
            {
                "name": "High resource usage",
                "state": {
                    "module": "unsloth",
                    "status": "training",
                    "cpu": 95.2,
                    "memory": 15360.0,
                    "gpu": 98.5
                }
            },
            {
                "name": "Empty state",
                "state": {}
            },
            {
                "name": "Invalid metrics",
                "state": {
                    "module": "test",
                    "cpu": -50,  # Invalid
                    "memory": "not_a_number",  # Invalid
                    "requests": None
                }
            },
            {
                "name": "Rapid state changes",
                "state": {
                    "module": "granger_hub",
                    "connections": 1000,
                    "throughput": 50000
                }
            }
        ]
        
        for test in test_states:
            print(f"\nTesting: {test['name']}")
            
            try:
                # Track state
                result = model.update_state(test["state"])
                
                if result:
                    print(f"✅ State tracked successfully")
                    self.record_test(f"track_{test['name']}", True, {
                        "state_id": result.get("id")
                    })
                    
                    # Verify state retrieval
                    if "module" in test["state"]:
                        retrieved = model.get_module_state(test["state"]["module"])
                        
                        if not retrieved:
                            self.add_bug(
                                "Cannot retrieve tracked state",
                                "HIGH",
                                module=test["state"]["module"]
                            )
                        elif retrieved != test["state"]:
                            self.add_bug(
                                "State retrieval mismatch",
                                "HIGH",
                                module=test["state"]["module"],
                                stored=test["state"],
                                retrieved=retrieved
                            )
                    
                    # Check validation
                    if test["name"] == "Invalid metrics" and "error" not in str(result):
                        self.add_bug(
                            "Invalid metrics accepted",
                            "MEDIUM",
                            state=test["state"]
                        )
                    
                    if test["name"] == "Empty state":
                        self.add_bug(
                            "Empty state accepted",
                            "MEDIUM",
                            impact="No validation"
                        )
                else:
                    if test["name"] not in ["Empty state", "Invalid metrics"]:
                        self.add_bug(
                            "State tracking failed",
                            "HIGH",
                            test=test["name"]
                        )
                    self.record_test(f"track_{test['name']}", False, {})
                    
            except Exception as e:
                self.add_bug(
                    f"Exception tracking {test['name']}",
                    "HIGH",
                    error=str(e)
                )
                self.record_test(f"track_{test['name']}", False, {"error": str(e)})
    
    def test_prediction_accuracy(self):
        """Test predictive capabilities"""
        print("\n\nTesting Prediction Accuracy...")
        
        try:
            from world_model import WorldModel
            model = WorldModel()
            
            # Create historical data
            print("Creating historical data...")
            historical_states = []
            
            for i in range(10):
                state = {
                    "module": "test_module",
                    "timestamp": time.time() + i * 60,
                    "cpu": 20 + i * 5,  # Linear increase
                    "memory": 100 + i * 10,
                    "requests": 100 + i * i  # Quadratic increase
                }
                model.update_state(state)
                historical_states.append(state)
                time.sleep(0.1)  # Small delay
            
            # Test predictions
            print("Testing predictions...")
            
            # Predict next state
            prediction = model.predict_next_state("test_module", horizon=1)
            
            if prediction:
                print(f"✅ Got prediction:")
                print(f"   CPU: {prediction.get('cpu', 'N/A')}")
                print(f"   Memory: {prediction.get('memory', 'N/A')}")
                
                self.record_test("prediction_basic", True, prediction)
                
                # Check prediction quality
                if "cpu" in prediction:
                    # Expected next CPU value should be around 70
                    error = abs(prediction["cpu"] - 70)
                    if error > 20:
                        self.add_bug(
                            "Poor CPU prediction accuracy",
                            "MEDIUM",
                            predicted=prediction["cpu"],
                            expected_range="50-90",
                            error=error
                        )
                
                # Test anomaly detection
                anomaly_state = {
                    "module": "test_module",
                    "cpu": 500,  # Way out of range
                    "memory": 50000  # Way out of range
                }
                
                is_anomaly = model.detect_anomaly(anomaly_state)
                
                if not is_anomaly:
                    self.add_bug(
                        "Anomaly detection failed",
                        "HIGH",
                        state=anomaly_state,
                        impact="Cannot detect abnormal states"
                    )
                else:
                    print("✅ Anomaly correctly detected")
                    self.record_test("anomaly_detection", True, {})
            else:
                self.add_bug(
                    "No prediction generated",
                    "HIGH",
                    historical_points=len(historical_states)
                )
                self.record_test("prediction_basic", False, {})
                
        except AttributeError as e:
            print(f"❌ Prediction not implemented: {e}")
            self.record_test("prediction_import", False, {"error": "Not implemented"})
        except Exception as e:
            self.add_bug(
                "Exception in prediction",
                "HIGH",
                error=str(e)
            )
            self.record_test("prediction_test", False, {"error": str(e)})
    
    def test_memory_management(self):
        """Test memory management and cleanup"""
        print("\n\nTesting Memory Management...")
        
        try:
            from world_model import WorldModel
            model = WorldModel()
            
            # Add many states to test memory limits
            print("Adding 1000 states...")
            start_memory = model.get_memory_usage() if hasattr(model, 'get_memory_usage') else 0
            
            for i in range(1000):
                state = {
                    "module": f"module_{i % 10}",
                    "timestamp": time.time() + i,
                    "cpu": i % 100,
                    "memory": i * 10
                }
                model.update_state(state)
            
            # Check memory usage
            if hasattr(model, 'get_memory_usage'):
                end_memory = model.get_memory_usage()
                memory_growth = end_memory - start_memory
                
                print(f"Memory growth: {memory_growth:.2f}MB")
                
                if memory_growth > 100:  # More than 100MB for 1000 states
                    self.add_bug(
                        "Excessive memory usage",
                        "HIGH",
                        growth_mb=memory_growth,
                        states=1000
                    )
                
                self.record_test("memory_usage", True, {
                    "growth_mb": memory_growth,
                    "states": 1000
                })
            
            # Test cleanup
            if hasattr(model, 'cleanup_old_states'):
                old_count = model.get_state_count() if hasattr(model, 'get_state_count') else 0
                model.cleanup_old_states(max_age_minutes=5)
                new_count = model.get_state_count() if hasattr(model, 'get_state_count') else 0
                
                if old_count == new_count and old_count > 100:
                    self.add_bug(
                        "Cleanup not working",
                        "MEDIUM",
                        states_before=old_count,
                        states_after=new_count
                    )
                else:
                    print(f"✅ Cleaned up {old_count - new_count} old states")
                    self.record_test("cleanup", True, {
                        "removed": old_count - new_count
                    })
                    
        except Exception as e:
            self.add_bug(
                "Exception in memory management test",
                "MEDIUM",
                error=str(e)
            )
            self.record_test("memory_management", False, {"error": str(e)})
    
    def run_tests(self):
        """Run all tests"""
        self.test_state_tracking()
        self.test_prediction_accuracy()
        self.test_memory_management()
        return self.generate_report()


def main():
    """Run the test"""
    tester = WorldModelStateTrackingTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)