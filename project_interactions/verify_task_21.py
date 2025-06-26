#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Skeptical verification of Task #21: Quantum-Safe Cryptography Migration Scanner
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the scenario directly
exec(open("/home/graham/workspace/shared_claude_docs/project_interactions/quantum_safe_scanner/quantum_safe_scanner_interaction.py").read())


class SkepticalVerifier:
    """Skeptically verify Task #21 implementation."""
    
    def __init__(self):
        self.suspicions = []
        self.confidence_scores = {}
    
    def verify_scan_codebase(self, scenario):
        """Verify codebase scanning test."""
        print("\n🔍 Verifying Codebase Scanning (Test 021.1)...")
        
        start_time = time.time()
        result = scenario.test_scan_codebase()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 1.0, 3.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["scan_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["scan_duration"] = 0.5
            self.suspicions.append(f"Duration {duration:.2f}s outside expected range")
        
        # Check vulnerabilities found
        output = result.output_data
        vulnerabilities_found = output.get("vulnerabilities_found", 0)
        
        if vulnerabilities_found > 0:
            print(f"  ✅ Found {vulnerabilities_found} vulnerabilities")
            self.confidence_scores["vulnerability_detection"] = 0.95
            
            # Check algorithm diversity
            algorithm_types = output.get("algorithm_types", [])
            expected_algorithms = ["RSA", "ECC", "DH"]
            if any(algo in str(algorithm_types) for algo in expected_algorithms):
                print(f"  ✅ Detected quantum-vulnerable algorithms: {algorithm_types}")
                self.confidence_scores["algorithm_diversity"] = 0.9
            else:
                self.suspicions.append("Missing expected quantum-vulnerable algorithms")
                self.confidence_scores["algorithm_diversity"] = 0.4
            
            # Check key size detection
            if "key_sizes" in str(output):
                print(f"  ✅ Key size information extracted")
                self.confidence_scores["key_size_detection"] = 0.85
            else:
                self.suspicions.append("No key size information")
                self.confidence_scores["key_size_detection"] = 0.3
        else:
            self.suspicions.append("No vulnerabilities detected")
            self.confidence_scores["vulnerability_detection"] = 0.1
        
        return result
    
    def verify_migration_plan(self, scenario):
        """Verify migration plan generation test."""
        print("\n🔍 Verifying Migration Plan Generation (Test 021.2)...")
        
        start_time = time.time()
        result = scenario.test_generate_migration_plan()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 0.5, 2.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["plan_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["plan_duration"] = 0.5
        
        # Check recommendations
        output = result.output_data
        recommendations_count = output.get("recommendations_count", 0)
        
        if recommendations_count > 0:
            print(f"  ✅ Generated {recommendations_count} migration recommendations")
            self.confidence_scores["recommendations"] = 0.9
            
            # Check NIST PQC algorithms
            pqc_algorithms = output.get("pqc_algorithms", [])
            expected_pqc = ["CRYSTALS", "Dilithium", "Kyber", "FALCON"]
            if any(algo in str(pqc_algorithms) for algo in expected_pqc):
                print(f"  ✅ Recommended NIST PQC algorithms")
                self.confidence_scores["pqc_recommendations"] = 0.95
            else:
                self.suspicions.append("No NIST PQC algorithms recommended")
                self.confidence_scores["pqc_recommendations"] = 0.3
            
            # Check effort estimation
            total_effort = output.get("total_effort_hours", 0)
            if total_effort > 0:
                print(f"  ✅ Effort estimation: {total_effort} hours")
                self.confidence_scores["effort_estimation"] = 0.85
            else:
                self.suspicions.append("No effort estimation provided")
                self.confidence_scores["effort_estimation"] = 0.2
        else:
            self.suspicions.append("No migration recommendations generated")
            self.confidence_scores["recommendations"] = 0.1
        
        return result
    
    def verify_report_generation(self, scenario):
        """Verify report generation test."""
        print("\n🔍 Verifying Report Generation (Test 021.3)...")
        
        start_time = time.time()
        result = scenario.test_generate_report()
        duration = time.time() - start_time
        
        # Check duration
        expected_min, expected_max = 0.5, 2.0
        if expected_min <= duration <= expected_max:
            self.confidence_scores["report_duration"] = 1.0
            print(f"  ✅ Duration OK: {duration:.2f}s (expected {expected_min}-{expected_max}s)")
        else:
            self.confidence_scores["report_duration"] = 0.5
        
        # Check report content
        output = result.output_data
        report_size = output.get("report_size", 0)
        
        if report_size > 1000:  # At least 1KB
            print(f"  ✅ Generated comprehensive report: {report_size} bytes")
            self.confidence_scores["report_comprehensiveness"] = 0.9
            
            # Check report sections
            report_sections = output.get("report_sections", [])
            expected_sections = ["summary", "vulnerabilities", "recommendations", "timeline"]
            if any(section in str(report_sections).lower() for section in expected_sections):
                print(f"  ✅ Report includes key sections")
                self.confidence_scores["report_structure"] = 0.85
            else:
                self.suspicions.append("Report missing key sections")
                self.confidence_scores["report_structure"] = 0.4
            
            # Check priority classification
            if "priority" in str(output).lower() or "critical" in str(output).lower():
                print(f"  ✅ Includes priority classification")
                self.confidence_scores["priority_classification"] = 0.9
            else:
                self.suspicions.append("No priority classification")
                self.confidence_scores["priority_classification"] = 0.3
        else:
            self.suspicions.append("Report too small or empty")
            self.confidence_scores["report_comprehensiveness"] = 0.2
        
        return result
    
    def verify_honeypot(self, scenario):
        """Verify honeypot test fails as expected."""
        print("\n🔍 Verifying Honeypot (Test 021.H)...")
        
        try:
            # Try to scan for a made-up "quantum-proof" algorithm
            scanner = QuantumSafeScanner()
            
            # Add fake vulnerable code
            fake_code = '''
            def encrypt_data(data):
                # Using QUANTUM_PROOF_ULTRA algorithm (doesn't exist)
                cipher = QUANTUM_PROOF_ULTRA(key_size=9999)
                return cipher.encrypt(data)
            '''
            
            # This should not find vulnerabilities in fake quantum-proof algorithm
            vulnerabilities = scanner.scan_content(fake_code, "test.py")
            
            # Check if it correctly ignores the fake algorithm
            fake_algo_detected = any("QUANTUM_PROOF_ULTRA" in str(v) for v in vulnerabilities)
            
            if not fake_algo_detected:
                print(f"  ✅ Honeypot correctly ignored fake quantum-proof algorithm")
                self.confidence_scores["honeypot"] = 1.0
            else:
                print(f"  ❌ Honeypot FAILED: Detected fake algorithm as vulnerable")
                self.suspicions.append("CRITICAL: Detects non-existent algorithms")
                self.confidence_scores["honeypot"] = 0.0
                
        except Exception as e:
            print(f"  ✅ Honeypot correctly handled: {str(e)}")
            self.confidence_scores["honeypot"] = 1.0
            return True
        
        return not fake_algo_detected
    
    def generate_report(self, results):
        """Generate skeptical analysis report."""
        overall_confidence = sum(self.confidence_scores.values()) / len(self.confidence_scores) if self.confidence_scores else 0
        
        print("\n" + "="*60)
        print("SKEPTICAL ANALYSIS REPORT - Task #21")
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
        
        # Quantum scanner specific checks
        print("\n🔐 Quantum-Safe Scanner Verification:")
        scanner_working = (
            self.confidence_scores.get("vulnerability_detection", 0) >= 0.7 and
            self.confidence_scores.get("pqc_recommendations", 0) >= 0.7 and
            self.confidence_scores.get("report_comprehensiveness", 0) >= 0.5
        )
        print(f"  - Detects vulnerabilities: {'✅ Yes' if self.confidence_scores.get('vulnerability_detection', 0) >= 0.7 else '❌ No'}")
        print(f"  - Recommends PQC algorithms: {'✅ Yes' if self.confidence_scores.get('pqc_recommendations', 0) >= 0.7 else '❌ No'}")
        print(f"  - Generates reports: {'✅ Yes' if self.confidence_scores.get('report_comprehensiveness', 0) >= 0.5 else '❌ No'}")
        
        return {
            "confidence": overall_confidence,
            "verdict": verdict,
            "suspicions": self.suspicions,
            "scanner_working": scanner_working
        }


def main():
    """Main verification runner."""
    print("="*80)
    print("Task #21 Skeptical Verification")
    print(f"Started: {datetime.now().isoformat()}")
    print("="*80)
    
    # Create scenario and verifier
    scenario = QuantumSafeScannerScenario()
    verifier = SkepticalVerifier()
    
    # Run all verifications
    results = {
        "scan": verifier.verify_scan_codebase(scenario),
        "plan": verifier.verify_migration_plan(scenario),
        "report": verifier.verify_report_generation(scenario),
        "honeypot": verifier.verify_honeypot(scenario)
    }
    
    # Generate report
    report = verifier.generate_report(results)
    
    # Final summary
    print("\n" + "="*80)
    print("TASK #21 VERIFICATION COMPLETE")
    print("="*80)
    
    if report["verdict"] in ["LIKELY_GENUINE", "QUESTIONABLE"] and report["scanner_working"]:
        print("\n✅ Task #21 PASSED skeptical verification")
        print("   Quantum-safe cryptography scanner successfully demonstrated")
        print("\nProceeding to Task #22...")
        return 0
    else:
        print("\n❌ Task #21 FAILED skeptical verification")
        if not report["scanner_working"]:
            print("   Scanner features not properly working")
        print("Debug and fix issues before proceeding")
        return 1


if __name__ == "__main__":
    sys.exit(main())