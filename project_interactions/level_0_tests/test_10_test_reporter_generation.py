"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_10_test_reporter_generation.py
Description: Test Claude Test Reporter report generation and lie detection
Level: 0
Modules: Claude Test Reporter
Expected Bugs: Report formatting issues, lie detection false positives/negatives, performance
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time
import random

class TestReporterGenerationTest(BaseInteractionTest):
    """Level 0: Test Claude Test Reporter functionality"""
    
    def __init__(self):
        super().__init__(
            test_name="Test Reporter Generation",
            level=0,
            modules=["Claude Test Reporter"]
        )
    
    def test_basic_report_generation(self):
        """Test basic report generation functionality"""
        self.print_header()
        
        # Import Test Reporter
        try:
            from claude_test_reporter import GrangerTestReporter
            from claude_test_reporter.skeptical_analyzer import SkepticalAnalyzer
            self.record_test("test_reporter_import", True, {})
        except ImportError as e:
            self.add_bug(
                "Test Reporter module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot use Test Reporter functionality"
            )
            self.record_test("test_reporter_import", False, {"error": str(e)})
            return
        
        # Test report generation scenarios
        test_scenarios = [
            {
                "name": "All tests passing",
                "results": [
                    {"test": "test_1", "status": "PASS", "duration": 0.5},
                    {"test": "test_2", "status": "PASS", "duration": 0.3},
                    {"test": "test_3", "status": "PASS", "duration": 0.7}
                ]
            },
            {
                "name": "Mixed results",
                "results": [
                    {"test": "test_1", "status": "PASS", "duration": 0.5},
                    {"test": "test_2", "status": "FAIL", "duration": 0.3, "error": "AssertionError"},
                    {"test": "test_3", "status": "SKIP", "duration": 0.0}
                ]
            },
            {
                "name": "All tests failing",
                "results": [
                    {"test": "test_1", "status": "FAIL", "duration": 0.1, "error": "Error 1"},
                    {"test": "test_2", "status": "FAIL", "duration": 0.1, "error": "Error 2"},
                    {"test": "test_3", "status": "FAIL", "duration": 0.1, "error": "Error 3"}
                ]
            },
            {
                "name": "Flaky test pattern",
                "results": [
                    {"test": "flaky_test", "status": "PASS", "duration": 0.5},
                    {"test": "flaky_test", "status": "FAIL", "duration": 0.5, "error": "Random fail"},
                    {"test": "flaky_test", "status": "PASS", "duration": 0.5},
                    {"test": "flaky_test", "status": "FAIL", "duration": 0.5, "error": "Random fail"}
                ]
            },
            {
                "name": "Suspiciously fast tests",
                "results": [
                    {"test": "test_1", "status": "PASS", "duration": 0.001},
                    {"test": "test_2", "status": "PASS", "duration": 0.001},
                    {"test": "test_3", "status": "PASS", "duration": 0.001}
                ]
            },
            {
                "name": "Empty results",
                "results": []
            }
        ]
        
        for scenario in test_scenarios:
            print(f"\nTesting: {scenario['name']}")
            
            try:
                # Create reporter
                reporter = GrangerTestReporter(
                    module_name=f"test_{scenario['name'].lower().replace(' ', '_')}",
                    test_suite="level_0_verification"
                )
                
                # Add test results
                for result in scenario["results"]:
                    reporter.add_test_result(
                        test_name=result["test"],
                        status=result["status"],
                        duration=result.get("duration", 0),
                        error=result.get("error")
                    )
                
                # Generate report
                html_report = reporter.generate_report(
                    include_skeptical_analysis=True,
                    detect_lies=True,
                    include_flaky_analysis=True
                )
                
                if html_report:
                    print(f"✅ Generated report: {len(html_report)} bytes")
                    self.record_test(f"report_{scenario['name']}", True, {
                        "report_size": len(html_report),
                        "test_count": len(scenario["results"])
                    })
                    
                    # Check report quality
                    if len(html_report) < 1000 and scenario["results"]:
                        self.add_bug(
                            "Suspiciously small report",
                            "MEDIUM",
                            scenario=scenario["name"],
                            size=len(html_report)
                        )
                    
                    # Check for expected content
                    if scenario["name"] == "Flaky test pattern" and "flaky" not in html_report.lower():
                        self.add_bug(
                            "Flaky test not detected",
                            "HIGH",
                            scenario=scenario["name"]
                        )
                    
                    if scenario["name"] == "Suspiciously fast tests" and "suspicious" not in html_report.lower():
                        self.add_bug(
                            "Fast tests not flagged as suspicious",
                            "HIGH",
                            scenario=scenario["name"]
                        )
                else:
                    if scenario["results"]:  # Should generate report if has results
                        self.add_bug(
                            "No report generated",
                            "HIGH",
                            scenario=scenario["name"]
                        )
                    self.record_test(f"report_{scenario['name']}", False, {})
                    
            except Exception as e:
                self.add_bug(
                    f"Exception generating report for {scenario['name']}",
                    "HIGH",
                    error=str(e)
                )
                self.record_test(f"report_{scenario['name']}", False, {"error": str(e)})
    
    def test_lie_detection(self):
        """Test lie detection capabilities"""
        print("\n\nTesting Lie Detection...")
        
        try:
            from claude_test_reporter import GrangerTestReporter
            from claude_test_reporter.skeptical_analyzer import SkepticalAnalyzer
            
            # Create analyzer
            analyzer = SkepticalAnalyzer()
            
            # Test lie detection scenarios
            lie_scenarios = [
                {
                    "name": "Obvious lie - all pass instantly",
                    "results": [
                        {"test": f"test_{i}", "passed": True, "duration": 0.0001}
                        for i in range(100)
                    ],
                    "expected_lie": True
                },
                {
                    "name": "Legitimate results",
                    "results": [
                        {
                            "test": f"test_{i}", 
                            "passed": random.choice([True, False]), 
                            "duration": random.uniform(0.1, 2.0)
                        }
                        for i in range(20)
                    ],
                    "expected_lie": False
                },
                {
                    "name": "Identical error messages",
                    "results": [
                        {
                            "test": f"test_{i}", 
                            "passed": False, 
                            "duration": 0.5,
                            "error": "Exact same error message"
                        }
                        for i in range(10)
                    ],
                    "expected_lie": True
                },
                {
                    "name": "Perfect sequential timing",
                    "results": [
                        {
                            "test": f"test_{i}", 
                            "passed": True, 
                            "duration": 1.000  # Exactly 1 second each
                        }
                        for i in range(20)
                    ],
                    "expected_lie": True
                }
            ]
            
            for scenario in lie_scenarios:
                print(f"\nTesting: {scenario['name']}")
                
                analysis = analyzer.analyze_test_results(scenario["results"])
                
                # Check if lies detected
                lies_detected = len(analysis.get("suspicious_patterns", [])) > 0
                confidence = analysis.get("confidence_score", 1.0)
                
                print(f"   Lies detected: {lies_detected}")
                print(f"   Confidence: {confidence:.0%}")
                
                self.record_test(f"lie_detection_{scenario['name']}", True, {
                    "lies_detected": lies_detected,
                    "confidence": confidence,
                    "patterns": analysis.get("suspicious_patterns", [])
                })
                
                # Verify detection accuracy
                if scenario["expected_lie"] and not lies_detected:
                    self.add_bug(
                        "Failed to detect obvious lie",
                        "CRITICAL",
                        scenario=scenario["name"],
                        patterns=analysis.get("suspicious_patterns", [])
                    )
                elif not scenario["expected_lie"] and lies_detected:
                    self.add_bug(
                        "False positive lie detection",
                        "HIGH",
                        scenario=scenario["name"],
                        patterns=analysis.get("suspicious_patterns", [])
                    )
                    
        except Exception as e:
            self.add_bug(
                "Exception in lie detection",
                "HIGH",
                error=str(e)
            )
            self.record_test("lie_detection", False, {"error": str(e)})
    
    def test_performance_analysis(self):
        """Test performance analysis features"""
        print("\n\nTesting Performance Analysis...")
        
        try:
            from claude_test_reporter import GrangerTestReporter
            
            reporter = GrangerTestReporter(
                module_name="performance_test",
                test_suite="level_0"
            )
            
            # Add performance test results
            print("Adding performance test results...")
            
            # Simulate test runs with degrading performance
            for run in range(5):
                for i in range(10):
                    base_duration = 0.5 + (run * 0.2)  # Performance degrades
                    duration = base_duration + random.uniform(-0.1, 0.1)
                    
                    reporter.add_test_result(
                        test_name=f"perf_test_{i}",
                        status="PASS",
                        duration=duration,
                        metadata={"run": run}
                    )
            
            # Generate performance report
            report = reporter.generate_report(
                include_performance_trends=True,
                include_regression_detection=True
            )
            
            if report:
                print("✅ Generated performance report")
                
                # Check if regression detected
                if "regression" not in report.lower():
                    self.add_bug(
                        "Performance regression not detected",
                        "HIGH",
                        impact="Cannot track performance degradation"
                    )
                
                self.record_test("performance_analysis", True, {
                    "report_generated": True,
                    "regression_detected": "regression" in report.lower()
                })
            else:
                self.add_bug(
                    "No performance report generated",
                    "HIGH"
                )
                self.record_test("performance_analysis", False, {})
                
        except AttributeError:
            print("❌ Performance analysis not implemented")
            self.record_test("performance_features", False, {"error": "Not implemented"})
        except Exception as e:
            self.add_bug(
                "Exception in performance analysis",
                "HIGH",
                error=str(e)
            )
            self.record_test("performance_analysis", False, {"error": str(e)})
    
    def run_tests(self):
        """Run all tests"""
        self.test_basic_report_generation()
        self.test_lie_detection()
        self.test_performance_analysis()
        return self.generate_report()


def main():
    """Run the test"""
    tester = TestReporterGenerationTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)