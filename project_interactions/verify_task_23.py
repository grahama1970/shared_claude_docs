#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Skeptical verification of Task #23: Distributed Training Orchestration
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the scenario directly
exec(open("/home/graham/workspace/shared_claude_docs/project_interactions/distributed_training/distributed_training_interaction.py").read())


class SkepticalVerifier:
    """Skeptically verify Task #23 implementation."""
    
    def __init__(self):
        self.suspicions = []
        self.confidence_scores = {}
    
    def verify_worker_initialization(self, scenario):
        """Verify worker initialization test."""
        print("\n🔍 Verifying Worker Initialization (Test 023.1)...")
        
        start_time = time.time()
        result = scenario.test_worker_initialization()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 1.0, 3.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["init_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["init_duration"] = 0.5
            self.suspicions.append(f"Duration {duration:.2f}s outside expected range")
        
        # Check worker creation
        if result.success:
            output = result.output_data
            workers_initialized = output.get("workers_initialized", 0)
            
            if workers_initialized >= 4:
                print(f"  ✅ Initialized {workers_initialized} workers")
                self.confidence_scores["worker_count"] = 0.95
                
                # Check worker health
                healthy_workers = output.get("healthy_workers", 0)
                if healthy_workers == workers_initialized:
                    print(f"  ✅ All workers healthy")
                    self.confidence_scores["worker_health"] = 1.0
                else:
                    self.suspicions.append(f"Only {healthy_workers}/{workers_initialized} workers healthy")
                    self.confidence_scores["worker_health"] = 0.5
            else:
                self.suspicions.append(f"Only {workers_initialized} workers initialized")
                self.confidence_scores["worker_count"] = 0.3
        else:
            self.suspicions.append("Worker initialization failed")
            self.confidence_scores["worker_count"] = 0.1
        
        return result
    
    def verify_data_sharding(self, scenario):
        """Verify data sharding test."""
        print("\n🔍 Verifying Data Sharding (Test 023.2)...")
        
        start_time = time.time()
        result = scenario.test_data_sharding()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 1.0, 3.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["shard_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["shard_duration"] = 0.5
        
        if result.success:
            output = result.output_data
            total_samples = output.get("total_samples", 0)
            shards_created = output.get("shards_created", 0)
            
            if shards_created > 0 and total_samples > 0:
                print(f"  ✅ Created {shards_created} shards for {total_samples} samples")
                self.confidence_scores["sharding"] = 0.9
                
                # Check shard balance
                max_shard_size = output.get("max_shard_size", 0)
                min_shard_size = output.get("min_shard_size", 0)
                if max_shard_size > 0 and (max_shard_size - min_shard_size) <= 1:
                    print(f"  ✅ Shards well-balanced: {min_shard_size}-{max_shard_size} samples")
                    self.confidence_scores["shard_balance"] = 0.95
                else:
                    self.suspicions.append("Shards not well-balanced")
                    self.confidence_scores["shard_balance"] = 0.4
            else:
                self.suspicions.append("No shards created")
                self.confidence_scores["sharding"] = 0.2
        else:
            self.suspicions.append("Data sharding failed")
            self.confidence_scores["sharding"] = 0.1
        
        return result
    
    def verify_gradient_aggregation(self, scenario):
        """Verify gradient aggregation test."""
        print("\n🔍 Verifying Gradient Aggregation (Test 023.3)...")
        
        start_time = time.time()
        result = scenario.test_gradient_aggregation()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 2.0, 5.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["agg_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["agg_duration"] = 0.5
        
        if result.success:
            output = result.output_data
            strategies_tested = output.get("strategies_tested", [])
            
            # Check multiple strategies
            expected_strategies = ["all_reduce", "ring_all_reduce"]
            if any(s in strategies_tested for s in expected_strategies):
                print(f"  ✅ Tested strategies: {strategies_tested}")
                self.confidence_scores["aggregation_strategies"] = 0.9
                
                # Check aggregation correctness
                if output.get("aggregation_correct", False):
                    print(f"  ✅ Gradient aggregation mathematically correct")
                    self.confidence_scores["aggregation_correctness"] = 0.95
                else:
                    self.suspicions.append("Gradient aggregation may be incorrect")
                    self.confidence_scores["aggregation_correctness"] = 0.3
            else:
                self.suspicions.append("Limited aggregation strategies tested")
                self.confidence_scores["aggregation_strategies"] = 0.4
        else:
            self.suspicions.append("Gradient aggregation failed")
            self.confidence_scores["aggregation_strategies"] = 0.1
        
        return result
    
    def verify_fault_tolerance(self, scenario):
        """Verify fault tolerance test."""
        print("\n🔍 Verifying Fault Tolerance (Test 023.4)...")
        
        start_time = time.time()
        result = scenario.test_fault_tolerance()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 3.0, 8.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["fault_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["fault_duration"] = 0.5
        
        if result.success:
            output = result.output_data
            workers_failed = output.get("workers_failed", 0)
            training_continued = output.get("training_continued", False)
            
            if workers_failed > 0 and training_continued:
                print(f"  ✅ Handled {workers_failed} worker failures")
                print(f"  ✅ Training continued successfully")
                self.confidence_scores["fault_handling"] = 0.95
                
                # Check data redistribution
                if output.get("data_redistributed", False):
                    print(f"  ✅ Data redistributed to healthy workers")
                    self.confidence_scores["data_recovery"] = 0.9
                else:
                    self.suspicions.append("Data not redistributed after failure")
                    self.confidence_scores["data_recovery"] = 0.3
            else:
                self.suspicions.append("Fault tolerance not demonstrated")
                self.confidence_scores["fault_handling"] = 0.2
        else:
            self.suspicions.append("Fault tolerance test failed")
            self.confidence_scores["fault_handling"] = 0.1
        
        return result
    
    def verify_honeypot(self, scenario):
        """Verify honeypot test fails as expected."""
        print("\n🔍 Verifying Honeypot (Test 023.H)...")
        
        try:
            # Try to create orchestrator with invalid config
            orchestrator = DistributedOrchestrator(num_workers=-5)  # Invalid number
            
            # This should fail
            orchestrator.initialize_workers()
            
            print(f"  ❌ Honeypot FAILED: Accepted invalid worker count")
            self.suspicions.append("CRITICAL: Accepts negative worker count")
            self.confidence_scores["honeypot"] = 0.0
                
        except Exception as e:
            print(f"  ✅ Honeypot correctly failed: {str(e)}")
            self.confidence_scores["honeypot"] = 1.0
            return True
        
        return False
    
    def generate_report(self, results):
        """Generate skeptical analysis report."""
        overall_confidence = sum(self.confidence_scores.values()) / len(self.confidence_scores) if self.confidence_scores else 0
        
        print("\n" + "="*60)
        print("SKEPTICAL ANALYSIS REPORT - Task #23")
        print("="*60)
        
        print(f"\nOverall Confidence: {overall_confidence:.1%}")
        
        print("\nConfidence Breakdown:")
        for metric, score in self.confidence_scores.items():
            print(f"  - {metric}: {score:.1%}")
        
        if self.suspicions:
            print("\n🚨 Suspicions Detected:")
            for suspicion in self.suspicions:
                print(f"  - {suspicion}")
        
        # Determine verdict
        if overall_confidence >= 0.85:
            verdict = "LIKELY_GENUINE"
            emoji = "✅"
        elif overall_confidence >= 0.7:
            verdict = "QUESTIONABLE" 
            emoji = "🟡"
        elif overall_confidence >= 0.5:
            verdict = "SUSPICIOUS"
            emoji = "⚠️"
        else:
            verdict = "FAKE_IMPLEMENTATION"
            emoji = "🚫"
        
        print(f"\n{emoji} VERDICT: {verdict}")
        
        # Distributed training specific checks
        print("\n🔄 Distributed Training Verification:")
        training_working = (
            self.confidence_scores.get("worker_count", 0) >= 0.7 and
            self.confidence_scores.get("sharding", 0) >= 0.7 and
            self.confidence_scores.get("fault_handling", 0) >= 0.5
        )
        print(f"  - Worker management: {'✅ Yes' if self.confidence_scores.get('worker_count', 0) >= 0.7 else '❌ No'}")
        print(f"  - Data sharding: {'✅ Yes' if self.confidence_scores.get('sharding', 0) >= 0.7 else '❌ No'}")
        print(f"  - Fault tolerance: {'✅ Yes' if self.confidence_scores.get('fault_handling', 0) >= 0.5 else '❌ No'}")
        
        return {
            "confidence": overall_confidence,
            "verdict": verdict,
            "suspicions": self.suspicions,
            "training_working": training_working
        }


def main():
    """Main verification runner."""
    print("="*80)
    print("Task #23 Skeptical Verification")
    print(f"Started: {datetime.now().isoformat()}")
    print("="*80)
    
    # Create scenario and verifier
    scenario = DistributedTrainingScenario()
    verifier = SkepticalVerifier()
    
    # Run all verifications
    results = {
        "init": verifier.verify_worker_initialization(scenario),
        "shard": verifier.verify_data_sharding(scenario),
        "aggregate": verifier.verify_gradient_aggregation(scenario),
        "fault": verifier.verify_fault_tolerance(scenario),
        "honeypot": verifier.verify_honeypot(scenario)
    }
    
    # Generate report
    report = verifier.generate_report(results)
    
    # Final summary
    print("\n" + "="*80)
    print("TASK #23 VERIFICATION COMPLETE")
    print("="*80)
    
    if report["verdict"] in ["LIKELY_GENUINE", "QUESTIONABLE"] and report["training_working"]:
        print("\n✅ Task #23 PASSED skeptical verification")
        print("   Distributed training orchestration successfully demonstrated")
        print("\nProceeding to Task #24...")
        return 0
    else:
        print("\n❌ Task #23 FAILED skeptical verification")
        if not report["training_working"]:
            print("   Training features not properly working")
        print("Debug and fix issues before proceeding")
        return 1


if __name__ == "__main__":
    sys.exit(main())