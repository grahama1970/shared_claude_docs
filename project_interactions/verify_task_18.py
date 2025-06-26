#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Skeptical verification of Task #18: Compliance Framework Mapping
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the scenario directly
import sys
sys.path.insert(0, "/home/graham/workspace/shared_claude_docs")
from project_interactions.sparta_arangodb_compliance.compliance_mapping_interaction import ComplianceMappingScenario


class SkepticalVerifier:
    """Skeptically verify Task #18 implementation."""
    
    def __init__(self):
        self.suspicions = []
        self.confidence_scores = {}
    
    def verify_load_controls(self, scenario):
        """Verify control loading test."""
        print("\n🔍 Verifying Control Loading (Test 018.1)...")
        
        start_time = time.time()
        result = scenario.test_load_controls()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 0.5, 2.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["load_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["load_duration"] = 0.5
            self.suspicions.append(f"Duration {duration:.2f}s outside expected range")
        
        # Check control count
        output = result.output_data
        controls_loaded = output.get("controls_loaded", 0)
        
        if controls_loaded >= 5:
            print(f"  ✅ Loaded {controls_loaded} controls")
            self.confidence_scores["control_count"] = 0.95
        else:
            self.suspicions.append(f"Only {controls_loaded} controls loaded")
            self.confidence_scores["control_count"] = 0.3
        
        # Check implementation status distribution
        status_dist = output.get("implementation_status", {})
        if all(status in ["Implemented", "Partial", "Not Implemented"] for status in status_dist.keys()):
            print(f"  ✅ Valid implementation statuses: {list(status_dist.keys())}")
            self.confidence_scores["status_validity"] = 1.0
        else:
            self.suspicions.append("Invalid implementation statuses")
            self.confidence_scores["status_validity"] = 0.0
        
        # Check for NIST control format
        sample_controls = output.get("sample_controls", [])
        if sample_controls and all("NIST" in str(c) for c in sample_controls[:2]):
            print(f"  ✅ Controls follow NIST format")
            self.confidence_scores["nist_format"] = 0.9
        else:
            self.suspicions.append("Controls don't follow NIST format")
            self.confidence_scores["nist_format"] = 0.4
        
        return result
    
    def verify_framework_mapping(self, scenario):
        """Verify framework mapping test."""
        print("\n🔍 Verifying Framework Mapping (Test 018.2)...")
        
        start_time = time.time()
        result = scenario.test_map_frameworks()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 1.0, 4.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["map_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["map_duration"] = 0.5
        
        # Check mappings
        output = result.output_data
        mappings_created = output.get("mappings_created", 0)
        frameworks = output.get("frameworks_mapped", [])
        
        if mappings_created > 0:
            print(f"  ✅ Created {mappings_created} framework mappings")
            
            # Check for expected frameworks
            expected_frameworks = ["NIST 800-53", "ISO 27001", "SOC 2"]
            if any(fw in str(frameworks) for fw in expected_frameworks):
                print(f"  ✅ Mapped to compliance frameworks: {frameworks}")
                self.confidence_scores["framework_diversity"] = 0.9
            else:
                self.suspicions.append("Missing expected compliance frameworks")
                self.confidence_scores["framework_diversity"] = 0.4
        else:
            self.suspicions.append("No framework mappings created")
            self.confidence_scores["framework_diversity"] = 0.1
        
        # Check graph structure
        if output.get("vertices_created", 0) > 0 and output.get("edges_created", 0) > 0:
            print(f"  ✅ Graph structure: {output['vertices_created']} vertices, {output['edges_created']} edges")
            self.confidence_scores["graph_structure"] = 0.95
        else:
            self.suspicions.append("No graph structure created")
            self.confidence_scores["graph_structure"] = 0.2
        
        return result
    
    def verify_gap_analysis(self, scenario):
        """Verify gap analysis test."""
        print("\n🔍 Verifying Gap Analysis (Test 018.3)...")
        
        start_time = time.time()
        result = scenario.test_gap_analysis()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 1.0, 3.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["gap_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["gap_duration"] = 0.5
        
        # Check gaps identified
        output = result.output_data
        gaps_identified = output.get("gaps_identified", 0)
        
        if gaps_identified > 0:
            print(f"  ✅ Identified {gaps_identified} compliance gaps")
            
            # Check critical gaps
            critical_gaps = output.get("critical_gaps", 0)
            if critical_gaps > 0:
                print(f"  ✅ Found {critical_gaps} critical gaps")
                self.confidence_scores["gap_detection"] = 0.95
            else:
                print(f"  ⚠️  No critical gaps found")
                self.confidence_scores["gap_detection"] = 0.7
            
            # Check recommendations
            recommendations = output.get("recommendations_generated", 0)
            if recommendations > 0:
                print(f"  ✅ Generated {recommendations} recommendations")
                self.confidence_scores["recommendations"] = 0.9
            else:
                self.suspicions.append("No recommendations generated")
                self.confidence_scores["recommendations"] = 0.3
            
            # Check report sections
            report_sections = output.get("report_sections", [])
            expected_sections = ["summary", "gaps", "recommendations"]
            if any(section in str(report_sections).lower() for section in expected_sections):
                print(f"  ✅ Report includes key sections")
                self.confidence_scores["report_quality"] = 0.85
            else:
                self.suspicions.append("Report missing key sections")
                self.confidence_scores["report_quality"] = 0.4
        else:
            self.suspicions.append("No compliance gaps identified")
            self.confidence_scores["gap_detection"] = 0.1
        
        return result
    
    def verify_honeypot(self, scenario):
        """Verify honeypot test fails as expected."""
        print("\n🔍 Verifying Honeypot (Test 018.H)...")
        
        try:
            # Try to map an invalid control
            fake_control = {
                "control_id": "FAKE-CTRL-999",
                "title": "Completely Invalid Control",
                "family": "INVALID",
                "implementation_status": "Unknown"
            }
            
            # This should fail or be handled gracefully
            mappings = scenario.mapper.map_control_to_frameworks(fake_control)
            
            if not mappings:
                print(f"  ✅ Honeypot correctly returned no mappings for invalid control")
                self.confidence_scores["honeypot"] = 1.0
            else:
                print(f"  ❌ Honeypot FAILED: Generated mappings for fake control")
                self.suspicions.append("CRITICAL: Maps non-existent controls")
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
        print("SKEPTICAL ANALYSIS REPORT - Task #18")
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
        
        # Compliance specific checks
        print("\n📋 Compliance Mapping Verification:")
        compliance_working = (
            self.confidence_scores.get("control_count", 0) >= 0.7 and
            self.confidence_scores.get("framework_diversity", 0) >= 0.7 and
            self.confidence_scores.get("gap_detection", 0) >= 0.5
        )
        print(f"  - Loads SPARTA controls: {'✅ Yes' if self.confidence_scores.get('control_count', 0) >= 0.7 else '❌ No'}")
        print(f"  - Maps to frameworks: {'✅ Yes' if self.confidence_scores.get('framework_diversity', 0) >= 0.7 else '❌ No'}")
        print(f"  - Performs gap analysis: {'✅ Yes' if self.confidence_scores.get('gap_detection', 0) >= 0.5 else '❌ No'}")
        
        return {
            "confidence": overall_confidence,
            "verdict": verdict,
            "suspicions": self.suspicions,
            "compliance_working": compliance_working
        }


def main():
    """Main verification runner."""
    print("="*80)
    print("Task #18 Skeptical Verification")
    print(f"Started: {datetime.now().isoformat()}")
    print("="*80)
    
    # Create scenario and verifier
    scenario = ComplianceMappingScenario()
    verifier = SkepticalVerifier()
    
    # Run all verifications
    results = {
        "load": verifier.verify_load_controls(scenario),
        "map": verifier.verify_framework_mapping(scenario),
        "gap": verifier.verify_gap_analysis(scenario),
        "honeypot": verifier.verify_honeypot(scenario)
    }
    
    # Generate report
    report = verifier.generate_report(results)
    
    # Final summary
    print("\n" + "="*80)
    print("TASK #18 VERIFICATION COMPLETE")
    print("="*80)
    
    if report["verdict"] in ["LIKELY_GENUINE", "QUESTIONABLE"] and report["compliance_working"]:
        print("\n✅ Task #18 PASSED skeptical verification")
        print("   Compliance framework mapping successfully demonstrated")
        print("\nProceeding to Task #19...")
        return 0
    else:
        print("\n❌ Task #18 FAILED skeptical verification")
        if not report["compliance_working"]:
            print("   Compliance features not properly working")
        print("Debug and fix issues before proceeding")
        return 1


if __name__ == "__main__":
    sys.exit(main())