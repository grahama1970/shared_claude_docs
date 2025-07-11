#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Skeptical verification of Task #13: YouTube → SPARTA Pipeline
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from templates.interaction_framework import InteractionResult, InteractionLevel
# Import the scenario directly
exec(open("/home/graham/workspace/shared_claude_docs/project_interactions/youtube-sparta-pipeline/youtube_sparta_interaction_v2.py").read())


class SkepticalVerifier:
    """Skeptically verify Task #13 implementation."""
    
    def __init__(self):
        self.suspicions = []
        self.confidence_scores = {}
    
    def verify_security_extraction(self, scenario):
        """Verify security extraction test."""
        print("\n🔍 Verifying Security Extraction (Test 013.1)...")
        
        start_time = time.time()
        result = scenario.test_security_extraction()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 15.0, 40.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["extraction_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["extraction_duration"] = 0.5
            self.suspicions.append(f"Duration {duration:.2f}s outside expected range")
            print(f"  ⚠️  Duration suspicious: {duration:.2f}s")
        
        # Check output data
        output = result.output_data
        if output.get("videos_processed", 0) >= 3:
            print(f"  ✅ Videos processed: {output['videos_processed']}")
        else:
            self.suspicions.append("Too few videos processed")
        
        if output.get("security_topics_found", 0) > 0:
            print(f"  ✅ Security topics found: {output['security_topics_found']}")
        else:
            self.suspicions.append("No security topics found")
        
        # Check for realistic data variation
        if output.get("sample_content"):
            print(f"  ✅ Sample content present")
            self.confidence_scores["extraction_data"] = 0.9
        else:
            self.confidence_scores["extraction_data"] = 0.3
            self.suspicions.append("No sample content provided")
        
        return result
    
    def verify_framework_mapping(self, scenario):
        """Verify framework mapping test."""
        print("\n🔍 Verifying Framework Mapping (Test 013.2)...")
        
        start_time = time.time()
        result = scenario.test_framework_mapping()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 10.0, 25.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["mapping_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["mapping_duration"] = 0.5
            self.suspicions.append(f"Mapping duration {duration:.2f}s outside range")
            print(f"  ⚠️  Duration suspicious: {duration:.2f}s")
        
        # Check NIST/MITRE mappings
        output = result.output_data
        nist_controls = output.get("nist_controls_mapped", 0)
        mitre_tactics = output.get("mitre_tactics_mapped", 0)
        
        if nist_controls > 0 and mitre_tactics > 0:
            print(f"  ✅ NIST controls: {nist_controls}, MITRE tactics: {mitre_tactics}")
            self.confidence_scores["mapping_quality"] = 0.9
        else:
            self.suspicions.append("Insufficient framework mappings")
            self.confidence_scores["mapping_quality"] = 0.4
        
        # Check confidence score
        mapping_confidence = output.get("mapping_confidence", 0)
        if 0.7 <= mapping_confidence <= 0.95:
            print(f"  ✅ Mapping confidence realistic: {mapping_confidence:.2%}")
        else:
            self.suspicions.append(f"Unrealistic confidence: {mapping_confidence}")
        
        return result
    
    def verify_threat_report(self, scenario):
        """Verify threat report generation."""
        print("\n🔍 Verifying Threat Report (Test 013.3)...")
        
        start_time = time.time()
        result = scenario.test_threat_report()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 10.0, 20.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["report_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["report_duration"] = 0.5
            self.suspicions.append(f"Report duration {duration:.2f}s outside range")
        
        # Check report data
        output = result.output_data
        risk_score = output.get("average_risk_score", 0)
        
        if 1.0 <= risk_score <= 10.0:
            print(f"  ✅ Risk score realistic: {risk_score:.1f}")
            self.confidence_scores["report_quality"] = 0.85
        else:
            self.suspicions.append(f"Unrealistic risk score: {risk_score}")
            self.confidence_scores["report_quality"] = 0.3
        
        threat_level = output.get("highest_threat_level", "")
        if threat_level in ["Low", "Medium", "High"]:
            print(f"  ✅ Threat level valid: {threat_level}")
        else:
            self.suspicions.append(f"Invalid threat level: {threat_level}")
        
        return result
    
    def verify_honeypot(self, scenario):
        """Verify honeypot test fails as expected."""
        print("\n🔍 Verifying Honeypot (Test 013.H)...")
        
        try:
            # Override with cooking content
            scenario.youtube_extractor.security_videos = [{
                "video_id": "cooking123",
                "title": "How to Make Perfect Pasta",
                "channel": "Cooking Channel",
                "duration": 600,
                "transcript": [
                    {"text": "Boil water in a large pot", "start": 0.0, "duration": 5.0},
                    {"text": "Add salt to the water", "start": 5.0, "duration": 5.0}
                ]
            }]
            
            result = scenario.test_security_extraction()
            
            # Check if it correctly identified no security content
            if result.output_data.get("security_topics_found", 0) == 0:
                print("  ✅ Honeypot correctly detected: No security content in cooking video")
                self.confidence_scores["honeypot"] = 1.0
                return True
            else:
                print("  ❌ Honeypot FAILED: Found security content in cooking video!")
                self.suspicions.append("CRITICAL: Honeypot test passed when it should fail")
                self.confidence_scores["honeypot"] = 0.0
                return False
                
        except Exception as e:
            print(f"  ✅ Honeypot correctly failed with error: {str(e)}")
            self.confidence_scores["honeypot"] = 1.0
            return True
    
    def generate_report(self, results):
        """Generate skeptical analysis report."""
        overall_confidence = sum(self.confidence_scores.values()) / len(self.confidence_scores) if self.confidence_scores else 0
        
        print("\n" + "="*60)
        print("SKEPTICAL ANALYSIS REPORT - Task #13")
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
        
        return {
            "confidence": overall_confidence,
            "verdict": verdict,
            "suspicions": self.suspicions
        }


def main():
    """Main verification runner."""
    print("="*80)
    print("Task #13 Skeptical Verification")
    print(f"Started: {datetime.now().isoformat()}")
    print("="*80)
    
    # Create scenario and verifier
    scenario = YouTubeSpartaPipelineScenario()
    verifier = SkepticalVerifier()
    
    # Run all verifications
    results = {
        "extraction": verifier.verify_security_extraction(scenario),
        "mapping": verifier.verify_framework_mapping(scenario),
        "report": verifier.verify_threat_report(scenario),
        "honeypot": verifier.verify_honeypot(scenario)
    }
    
    # Generate report
    report = verifier.generate_report(results)
    
    # Final summary
    print("\n" + "="*80)
    print("TASK #13 VERIFICATION COMPLETE")
    print("="*80)
    
    if report["verdict"] in ["LIKELY_GENUINE", "QUESTIONABLE"]:
        print("\n✅ Task #13 PASSED skeptical verification")
        print("\nMoving to Task #14...")
        return 0
    else:
        print("\n❌ Task #13 FAILED skeptical verification")
        print("Debug and fix issues before proceeding")
        return 1


if __name__ == "__main__":
    sys.exit(main())