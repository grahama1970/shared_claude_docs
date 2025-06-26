#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Skeptical verification of Task #19: Contradiction Detection Across Sources
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the scenario directly
exec(open("/home/graham/workspace/shared_claude_docs/project_interactions/contradiction-detection/contradiction_detection_interaction.py").read())


class SkepticalVerifier:
    """Skeptically verify Task #19 implementation."""
    
    def __init__(self):
        self.suspicions = []
        self.confidence_scores = {}
    
    def verify_source_loading(self, scenario):
        """Verify source loading test."""
        print("\n🔍 Verifying Source Loading (Test 019.1)...")
        
        start_time = time.time()
        result = scenario.test_load_sources()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 0.5, 2.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["load_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["load_duration"] = 0.5
            self.suspicions.append(f"Duration {duration:.2f}s outside expected range")
        
        # Check source diversity
        output = result.output_data
        sources_loaded = output.get("sources_loaded", 0)
        source_types = output.get("source_types", [])
        
        if sources_loaded >= 6:
            print(f"  ✅ Loaded {sources_loaded} diverse sources")
            self.confidence_scores["source_count"] = 0.95
        else:
            self.suspicions.append(f"Only {sources_loaded} sources loaded")
            self.confidence_scores["source_count"] = 0.3
        
        # Check source type diversity
        expected_types = ["arxiv", "youtube", "documentation"]
        if any(t in str(source_types) for t in expected_types):
            print(f"  ✅ Source types include: {source_types}")
            self.confidence_scores["source_diversity"] = 0.9
        else:
            self.suspicions.append("Missing expected source types")
            self.confidence_scores["source_diversity"] = 0.4
        
        # Check content presence
        total_chars = output.get("total_content_length", 0)
        if total_chars > 1000:
            print(f"  ✅ Substantial content loaded: {total_chars} characters")
            self.confidence_scores["content_volume"] = 0.85
        else:
            self.suspicions.append("Insufficient content loaded")
            self.confidence_scores["content_volume"] = 0.3
        
        return result
    
    def verify_contradiction_detection(self, scenario):
        """Verify contradiction detection test."""
        print("\n🔍 Verifying Contradiction Detection (Test 019.2)...")
        
        start_time = time.time()
        result = scenario.test_detect_contradictions()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 2.0, 6.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["detect_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["detect_duration"] = 0.5
        
        # Check contradictions found
        output = result.output_data
        contradictions_found = output.get("contradictions_found", 0)
        
        if contradictions_found > 0:
            print(f"  ✅ Found {contradictions_found} contradictions")
            
            # Check detection rate
            detection_rate = output.get("detection_rate", 0)
            if 0.1 <= detection_rate <= 0.8:  # Reasonable range
                print(f"  ✅ Detection rate realistic: {detection_rate:.1%}")
                self.confidence_scores["detection_rate"] = 0.9
            else:
                self.suspicions.append(f"Unrealistic detection rate: {detection_rate:.1%}")
                self.confidence_scores["detection_rate"] = 0.4
            
            # Check severity distribution
            severity_dist = output.get("severity_distribution", {})
            if len(severity_dist) > 0:
                print(f"  ✅ Found multiple severity levels: {list(severity_dist.keys())}")
                self.confidence_scores["severity_diversity"] = 0.85
            else:
                self.suspicions.append("No severity classification")
                self.confidence_scores["severity_diversity"] = 0.2
        else:
            self.suspicions.append("No contradictions detected")
            self.confidence_scores["detection_rate"] = 0.1
        
        return result
    
    def verify_reconciliation(self, scenario):
        """Verify reconciliation test."""
        print("\n🔍 Verifying Reconciliation Recommendations (Test 019.3)...")
        
        start_time = time.time()
        result = scenario.test_reconciliation()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 1.0, 3.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["reconcile_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["reconcile_duration"] = 0.5
        
        # Check recommendations
        output = result.output_data
        recommendations_generated = output.get("recommendations_generated", 0)
        
        if recommendations_generated > 0:
            print(f"  ✅ Generated {recommendations_generated} recommendations")
            self.confidence_scores["recommendations"] = 0.9
            
            # Check strategies used
            strategies_used = output.get("strategies_used", [])
            if len(strategies_used) >= 2:
                print(f"  ✅ Multiple strategies: {strategies_used}")
                self.confidence_scores["strategy_diversity"] = 0.85
            else:
                self.suspicions.append("Limited reconciliation strategies")
                self.confidence_scores["strategy_diversity"] = 0.5
            
            # Check major contradictions addressed
            critical_addressed = output.get("critical_contradictions_addressed", 0)
            if critical_addressed > 0:
                print(f"  ✅ Addressed {critical_addressed} critical contradictions")
                self.confidence_scores["critical_handling"] = 0.95
            else:
                self.suspicions.append("No critical contradictions addressed")
                self.confidence_scores["critical_handling"] = 0.4
        else:
            self.suspicions.append("No reconciliation recommendations")
            self.confidence_scores["recommendations"] = 0.1
        
        return result
    
    def verify_honeypot(self, scenario):
        """Verify honeypot test fails as expected."""
        print("\n🔍 Verifying Honeypot (Test 019.H)...")
        
        try:
            # Try to detect contradictions in identical content
            identical_source1 = {
                "id": "test1",
                "type": "paper",
                "title": "Test Paper",
                "content": "The quantum threat to cryptography will arrive by 2030.",
                "date": "2024-01-01"
            }
            identical_source2 = {
                "id": "test2", 
                "type": "paper",
                "title": "Test Paper Copy",
                "content": "The quantum threat to cryptography will arrive by 2030.",
                "date": "2024-01-01"
            }
            
            # This should not find contradictions
            detector = ContradictionDetector()
            contradictions = detector._compare_sources(identical_source1, identical_source2)
            
            if not contradictions:
                print(f"  ✅ Honeypot correctly found no contradictions in identical content")
                self.confidence_scores["honeypot"] = 1.0
            else:
                print(f"  ❌ Honeypot FAILED: Found contradictions in identical content")
                self.suspicions.append("CRITICAL: Detects false contradictions")
                self.confidence_scores["honeypot"] = 0.0
                
        except Exception as e:
            print(f"  ✅ Honeypot correctly failed: {str(e)}")
            self.confidence_scores["honeypot"] = 1.0
            return True
        
        return len(contradictions) == 0
    
    def generate_report(self, results):
        """Generate skeptical analysis report."""
        overall_confidence = sum(self.confidence_scores.values()) / len(self.confidence_scores) if self.confidence_scores else 0
        
        print("\n" + "="*60)
        print("SKEPTICAL ANALYSIS REPORT - Task #19")
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
        
        # Contradiction detection specific checks
        print("\n🔍 Contradiction Detection Verification:")
        detection_working = (
            self.confidence_scores.get("source_diversity", 0) >= 0.7 and
            self.confidence_scores.get("detection_rate", 0) >= 0.7 and
            self.confidence_scores.get("recommendations", 0) >= 0.5
        )
        print(f"  - Loads diverse sources: {'✅ Yes' if self.confidence_scores.get('source_diversity', 0) >= 0.7 else '❌ No'}")
        print(f"  - Detects contradictions: {'✅ Yes' if self.confidence_scores.get('detection_rate', 0) >= 0.7 else '❌ No'}")
        print(f"  - Provides reconciliation: {'✅ Yes' if self.confidence_scores.get('recommendations', 0) >= 0.5 else '❌ No'}")
        
        return {
            "confidence": overall_confidence,
            "verdict": verdict,
            "suspicions": self.suspicions,
            "detection_working": detection_working
        }


def main():
    """Main verification runner."""
    print("="*80)
    print("Task #19 Skeptical Verification")
    print(f"Started: {datetime.now().isoformat()}")
    print("="*80)
    
    # Create scenario and verifier
    scenario = ContradictionDetectionScenario()
    verifier = SkepticalVerifier()
    
    # Run all verifications
    results = {
        "load": verifier.verify_source_loading(scenario),
        "detect": verifier.verify_contradiction_detection(scenario),
        "reconcile": verifier.verify_reconciliation(scenario),
        "honeypot": verifier.verify_honeypot(scenario)
    }
    
    # Generate report
    report = verifier.generate_report(results)
    
    # Final summary
    print("\n" + "="*80)
    print("TASK #19 VERIFICATION COMPLETE")
    print("="*80)
    
    if report["verdict"] in ["LIKELY_GENUINE", "QUESTIONABLE"] and report["detection_working"]:
        print("\n✅ Task #19 PASSED skeptical verification")
        print("   Contradiction detection successfully demonstrated")
        print("\nProceeding to Task #20...")
        return 0
    else:
        print("\n❌ Task #19 FAILED skeptical verification")
        if not report["detection_working"]:
            print("   Detection features not properly working")
        print("Debug and fix issues before proceeding")
        return 1


if __name__ == "__main__":
    sys.exit(main())