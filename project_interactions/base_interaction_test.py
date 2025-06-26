#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: base_interaction_test.py
Description: Base class for all interaction tests with Test Reporter integration
"""

import json
import time
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys

sys.path.insert(0, '/home/graham/workspace/experiments')

# Import the test reporter for skeptical verification
try:
    from claude_test_reporter import GrangerTestReporter
    from claude_test_reporter.skeptical_analyzer import SkepticalAnalyzer
    TEST_REPORTER_AVAILABLE = True
except ImportError:
    TEST_REPORTER_AVAILABLE = False
    print("Warning: Test Reporter not available for verification")

class BaseInteractionTest:
    """Base class for all Granger interaction tests with skeptical verification"""
    
    def __init__(self, test_name: str, level: int, modules: List[str]):
        self.test_name = test_name
        self.level = level
        self.modules = modules
        self.bugs_found = []
        self.test_results = []
        self.start_time = time.time()
        
        # Initialize test reporter
        if TEST_REPORTER_AVAILABLE:
            self.reporter = GrangerTestReporter(
                module_name=test_name.lower().replace(' ', '_'),
                test_suite=f"level_{level}_tests"
            )
            self.skeptical_analyzer = SkepticalAnalyzer()
        else:
            self.reporter = None
            self.skeptical_analyzer = None
    
    def record_test(self, test_name: str, passed: bool, details: Dict[str, Any]):
        """Record test result for reporter verification"""
        duration = details.get("duration", time.time() - self.start_time)
        
        result = {
            "test": test_name,
            "passed": passed,
            "timestamp": time.time(),
            "duration": duration,
            "details": details
        }
        self.test_results.append(result)
        
        # Report to test reporter
        if self.reporter:
            self.reporter.add_test_result(
                test_name=test_name,
                status="PASS" if passed else "FAIL",
                duration=duration,
                error=details.get("error") if not passed else None,
                metadata={
                    "level": self.level,
                    "modules": self.modules,
                    "details": details
                }
            )
    
    def add_bug(self, bug: str, severity: str, **kwargs):
        """Add a bug finding with metadata"""
        bug_entry = {
            "bug": bug,
            "severity": severity,
            "timestamp": time.time(),
            "test_level": self.level,
            "modules": self.modules
        }
        bug_entry.update(kwargs)
        self.bugs_found.append(bug_entry)
        
        # Also record as failed test
        self.record_test(f"bug_check_{len(self.bugs_found)}", False, {
            "bug": bug,
            "severity": severity,
            **kwargs
        })
    
    def verify_results(self) -> Dict[str, Any]:
        """Use test reporter to skeptically verify results"""
        if not self.skeptical_analyzer:
            # Return default verification structure when analyzer not available
            pass_count = sum(1 for r in self.test_results if r["passed"])
            total_count = len(self.test_results)
            
            return {
                "verified": False,
                "reason": "Test Reporter not available",
                "confidence_score": 0.5,
                "total_tests": total_count,
                "passed_tests": pass_count,
                "failed_tests": total_count - pass_count,
                "bugs_found": len(self.bugs_found),
                "suspicious_patterns": []
            }
        
        # Analyze test patterns
        analysis = self.skeptical_analyzer.analyze_test_results(self.test_results)
        
        # Check for suspicious patterns
        suspicious_patterns = []
        
        # Pattern 1: Unrealistic pass rate
        pass_count = sum(1 for r in self.test_results if r["passed"])
        total_count = len(self.test_results)
        pass_rate = pass_count / total_count if total_count > 0 else 0
        
        if pass_rate == 1.0 and total_count > 5:
            suspicious_patterns.append({
                "pattern": "Perfect pass rate",
                "details": f"All {total_count} tests passed - statistically unlikely"
            })
        elif pass_rate == 0.0 and total_count > 5:
            suspicious_patterns.append({
                "pattern": "Complete failure",
                "details": f"All {total_count} tests failed - check test setup"
            })
        
        # Pattern 2: Timing anomalies
        durations = [r["duration"] for r in self.test_results if "duration" in r]
        if durations:
            avg_duration = sum(durations) / len(durations)
            
            # Check for suspiciously fast tests
            fast_tests = [d for d in durations if d < 0.01]
            if len(fast_tests) > len(durations) * 0.3:
                suspicious_patterns.append({
                    "pattern": "Unrealistic test speed",
                    "details": f"{len(fast_tests)} tests completed in <10ms"
                })
            
            # Check for identical durations
            unique_durations = len(set(durations))
            if unique_durations < len(durations) * 0.5:
                suspicious_patterns.append({
                    "pattern": "Identical durations",
                    "details": "Many tests have exact same duration"
                })
        
        # Pattern 3: Error message patterns
        errors = [r["details"].get("error", "") for r in self.test_results if not r["passed"]]
        if errors:
            unique_errors = len(set(errors))
            if unique_errors == 1 and len(errors) > 3:
                suspicious_patterns.append({
                    "pattern": "Identical errors",
                    "details": f"All {len(errors)} errors are identical"
                })
        
        # Pattern 4: Bug finding patterns
        if not self.bugs_found and total_count > 10:
            suspicious_patterns.append({
                "pattern": "No bugs found",
                "details": "Statistically unlikely to find zero bugs"
            })
        
        # Generate verification report
        verification = {
            "verified": len(suspicious_patterns) == 0,
            "total_tests": total_count,
            "passed_tests": pass_count,
            "failed_tests": total_count - pass_count,
            "bugs_found": len(self.bugs_found),
            "suspicious_patterns": suspicious_patterns,
            "confidence_score": max(0, 1.0 - (len(suspicious_patterns) * 0.2))
        }
        
        # Log suspicious patterns as bugs
        if suspicious_patterns:
            for pattern in suspicious_patterns:
                self.add_bug(
                    f"Test reliability issue: {pattern['pattern']}",
                    "HIGH",
                    details=pattern["details"],
                    impact="Test results may be unreliable"
                )
        
        return verification
    
    def generate_report(self) -> List[Dict[str, Any]]:
        """Generate comprehensive test report with verification"""
        print(f"\n\n{'='*60}")
        print(f"Test Report: {self.test_name}")
        print(f"Level: {self.level} | Modules: {', '.join(self.modules)}")
        print(f"{'='*60}")
        
        # Verify results first
        verification = self.verify_results()
        
        print(f"\n🔍 Verification Results:")
        print(f"  Confidence Score: {verification['confidence_score']:.0%}")
        print(f"  Total Tests: {verification['total_tests']}")
        print(f"  Passed: {verification['passed_tests']} | Failed: {verification['failed_tests']}")
        print(f"  Bugs Found: {verification['bugs_found']}")
        
        if verification['suspicious_patterns']:
            print(f"\n⚠️ Suspicious Patterns Detected:")
            for pattern in verification['suspicious_patterns']:
                print(f"  - {pattern['pattern']}: {pattern['details']}")
        
        # Bug summary
        if not self.bugs_found:
            print("\n✅ No bugs found!")
        else:
            print(f"\n🐛 Found {len(self.bugs_found)} bugs:\n")
            
            # Group by severity
            for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                bugs = [b for b in self.bugs_found if b.get("severity") == severity]
                if bugs:
                    print(f"\n{severity} ({len(bugs)} bugs):")
                    for bug in bugs[:5]:  # Show first 5
                        print(f"  - {bug['bug']}")
                        if "impact" in bug:
                            print(f"    Impact: {bug['impact']}")
                    if len(bugs) > 5:
                        print(f"  ... and {len(bugs) - 5} more")
        
        # Generate reports
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Save JSON bug report
        report_dir = Path("bug_reports")
        report_dir.mkdir(exist_ok=True)
        
        json_path = report_dir / f"level{self.level}_{self.test_name.lower().replace(' ', '_')}_{timestamp}.json"
        
        report_data = {
            "test_name": self.test_name,
            "level": self.level,
            "modules": self.modules,
            "timestamp": timestamp,
            "duration": time.time() - self.start_time,
            "verification": verification,
            "bugs": self.bugs_found,
            "test_results": self.test_results
        }
        
        json_path.write_text(json.dumps(report_data, indent=2))
        print(f"\n📄 JSON report: {json_path}")
        
        # Generate HTML report with test reporter
        if self.reporter:
            html_report = self.reporter.generate_report(
                include_skeptical_analysis=True,
                detect_lies=True,
                include_flaky_analysis=True
            )
            
            html_path = report_dir / f"level{self.level}_{self.test_name.lower().replace(' ', '_')}_{timestamp}.html"
            html_path.write_text(html_report)
            print(f"📊 HTML report: {html_path}")
        
        return self.bugs_found
    
    def print_header(self):
        """Print test header"""
        print(f"\n{'='*60}")
        print(f"Level {self.level} Test: {self.test_name}")
        print(f"Modules: {', '.join(self.modules)}")
        print(f"{'='*60}\n")