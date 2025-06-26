#!/usr/bin/env python3
"""
Module: test_18_llm_call_to_test_reporter_pipeline.py
Description: Test LLM Call → Test Reporter analysis pipeline
Level: 1
Modules: LLM Call, Test Reporter
Expected Bugs: Response parsing errors, metric calculation issues, report generation
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time
import json

class LLMCallToTestReporterPipelineTest(BaseInteractionTest):
    """Level 1: Test LLM Call to Test Reporter pipeline"""
    
    def __init__(self):
        super().__init__(
            test_name="LLM Call to Test Reporter Pipeline",
            level=1,
            modules=["LLM Call", "Test Reporter"]
        )
    
    def test_llm_quality_analysis(self):
        """Test analyzing LLM response quality with Test Reporter"""
        self.print_header()
        
        # Import modules
        try:
            from llm_call import llm_call, get_available_providers
            from claude_test_reporter import GrangerTestReporter
            from claude_test_reporter.skeptical_analyzer import SkepticalAnalyzer
            self.record_test("modules_import", True, {})
        except ImportError as e:
            self.add_bug(
                "Module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot run pipeline"
            )
            self.record_test("modules_import", False, {"error": str(e)})
            return
        
        # Initialize test reporter
        try:
            reporter = GrangerTestReporter(
                module_name="llm_quality_analysis",
                test_suite="llm_responses"
            )
            analyzer = SkepticalAnalyzer()
            self.record_test("reporter_init", True, {})
        except Exception as e:
            self.add_bug(
                "Test Reporter initialization failed",
                "CRITICAL",
                error=str(e)
            )
            self.record_test("reporter_init", False, {"error": str(e)})
            return
        
        # Test different prompt types
        test_prompts = [
            {
                "name": "Code generation",
                "prompt": "Write a Python function to calculate fibonacci numbers",
                "expected_quality": "high",
                "validation_checks": ["def ", "fibonacci", "return"]
            },
            {
                "name": "Factual question",
                "prompt": "What is the capital of France?",
                "expected_quality": "high",
                "validation_checks": ["Paris"]
            },
            {
                "name": "Creative writing",
                "prompt": "Write a haiku about programming",
                "expected_quality": "medium",
                "validation_checks": ["5-7-5 syllables", "three lines"]
            },
            {
                "name": "Nonsense prompt",
                "prompt": "asdkfj askdfj alskdfj",
                "expected_quality": "low",
                "validation_checks": []
            },
            {
                "name": "Empty prompt",
                "prompt": "",
                "expected_quality": "fail",
                "validation_checks": []
            }
        ]
        
        # Get available providers
        providers = get_available_providers()
        if not providers:
            self.add_bug(
                "No LLM providers available",
                "CRITICAL",
                impact="Cannot test LLM quality"
            )
            return
        
        provider = providers[0]  # Use first available
        
        for test in test_prompts:
            print(f"\nTesting: {test['name']}")
            pipeline_start = time.time()
            
            try:
                # Step 1: Make LLM call
                print(f"Calling LLM with prompt: {test['prompt'][:50]}...")
                call_start = time.time()
                
                try:
                    response = llm_call(
                        prompt=test["prompt"],
                        provider=provider,
                        max_tokens=200
                    )
                    call_duration = time.time() - call_start
                    
                    if response:
                        print(f"✅ Got response: {len(response)} chars in {call_duration:.2f}s")
                    else:
                        response = ""
                        print("❌ No response received")
                        
                except Exception as e:
                    response = ""
                    call_duration = time.time() - call_start
                    print(f"❌ LLM call failed: {str(e)[:50]}")
                
                # Step 2: Analyze response quality
                print("Analyzing response quality...")
                
                quality_metrics = {
                    "response_length": len(response),
                    "response_time": call_duration,
                    "contains_expected": 0,
                    "coherence_score": 0,
                    "completeness": 0
                }
                
                # Check for expected content
                for check in test["validation_checks"]:
                    if check.lower() in response.lower():
                        quality_metrics["contains_expected"] += 1
                
                # Calculate coherence (simple heuristic)
                if response:
                    # Check for complete sentences
                    sentences = response.count('.') + response.count('!') + response.count('?')
                    quality_metrics["coherence_score"] = min(sentences / 3, 1.0)
                    
                    # Check completeness
                    if len(response) > 50:
                        quality_metrics["completeness"] = 1.0
                    else:
                        quality_metrics["completeness"] = len(response) / 50
                
                # Step 3: Report to Test Reporter
                test_passed = False
                
                if test["expected_quality"] == "fail":
                    test_passed = not response or len(response) < 10
                elif test["expected_quality"] == "high":
                    test_passed = (
                        quality_metrics["contains_expected"] >= len(test["validation_checks"]) * 0.8 and
                        quality_metrics["coherence_score"] > 0.5 and
                        quality_metrics["completeness"] > 0.7
                    )
                elif test["expected_quality"] == "medium":
                    test_passed = (
                        quality_metrics["coherence_score"] > 0.3 and
                        quality_metrics["completeness"] > 0.5
                    )
                else:  # low quality
                    test_passed = len(response) > 0
                
                reporter.add_test_result(
                    test_name=f"llm_quality_{test['name']}",
                    status="PASS" if test_passed else "FAIL",
                    duration=call_duration,
                    metadata={
                        "prompt": test["prompt"],
                        "response_length": len(response),
                        "quality_metrics": quality_metrics,
                        "provider": provider
                    }
                )
                
                # Step 4: Use skeptical analyzer
                is_suspicious = analyzer.detect_lie_pattern({
                    "test": test["name"],
                    "passed": test_passed,
                    "duration": call_duration,
                    "metrics": quality_metrics
                })
                
                if is_suspicious:
                    self.add_bug(
                        "Suspicious LLM quality result",
                        "MEDIUM",
                        test=test["name"],
                        reason="Pattern suggests unreliable result"
                    )
                
                self.record_test(f"pipeline_{test['name']}", True, {
                    "response_length": len(response),
                    "call_duration": call_duration,
                    "quality_passed": test_passed,
                    "quality_metrics": quality_metrics,
                    "total_time": time.time() - pipeline_start
                })
                
                # Quality checks
                if test["expected_quality"] == "high" and not test_passed:
                    self.add_bug(
                        "Poor quality for expected high-quality prompt",
                        "HIGH",
                        prompt_type=test["name"],
                        metrics=quality_metrics
                    )
                
                if call_duration > 10:
                    self.add_bug(
                        "Slow LLM response",
                        "MEDIUM",
                        prompt_type=test["name"],
                        duration=f"{call_duration:.2f}s"
                    )
                    
            except Exception as e:
                self.add_bug(
                    f"Pipeline exception for {test['name']}",
                    "HIGH",
                    error=str(e)
                )
                self.record_test(f"pipeline_{test['name']}", False, {"error": str(e)})
        
        # Generate quality report
        self.generate_quality_report(reporter)
    
    def generate_quality_report(self, reporter):
        """Generate comprehensive quality report"""
        print("\n\nGenerating Quality Report...")
        
        try:
            # Generate HTML report with analysis
            html_report = reporter.generate_report(
                include_skeptical_analysis=True,
                detect_lies=True,
                include_performance_trends=True
            )
            
            if html_report:
                report_path = "llm_quality_analysis_report.html"
                with open(report_path, 'w') as f:
                    f.write(html_report)
                
                print(f"✅ Quality report generated: {report_path}")
                
                self.record_test("quality_report_generation", True, {
                    "report_size": len(html_report),
                    "report_path": report_path
                })
            else:
                self.add_bug(
                    "Failed to generate quality report",
                    "HIGH"
                )
                
        except Exception as e:
            self.add_bug(
                "Exception generating quality report",
                "HIGH",
                error=str(e)
            )
    
    def test_provider_comparison(self):
        """Test comparing multiple LLM providers"""
        print("\n\nTesting Provider Comparison...")
        
        try:
            from llm_call import llm_call, get_available_providers
            from claude_test_reporter import GrangerTestReporter
            
            providers = get_available_providers()
            
            if len(providers) < 2:
                print("❌ Need at least 2 providers for comparison")
                self.record_test("provider_comparison", False, {
                    "error": "Insufficient providers"
                })
                return
            
            reporter = GrangerTestReporter(
                module_name="provider_comparison",
                test_suite="llm_providers"
            )
            
            # Test prompt for comparison
            test_prompt = "Explain what a hash table is in simple terms"
            
            provider_results = {}
            
            for provider in providers[:3]:  # Test up to 3 providers
                print(f"\nTesting provider: {provider}")
                
                try:
                    start_time = time.time()
                    response = llm_call(
                        prompt=test_prompt,
                        provider=provider,
                        max_tokens=150
                    )
                    duration = time.time() - start_time
                    
                    if response:
                        # Analyze response
                        provider_results[provider] = {
                            "response_length": len(response),
                            "duration": duration,
                            "tokens_per_second": len(response.split()) / duration,
                            "contains_key_terms": sum(
                                1 for term in ["key", "value", "bucket", "collision"]
                                if term in response.lower()
                            )
                        }
                        
                        print(f"✅ {provider}: {len(response)} chars in {duration:.2f}s")
                        
                        # Report to test reporter
                        reporter.add_test_result(
                            test_name=f"provider_{provider}",
                            status="PASS",
                            duration=duration,
                            metadata=provider_results[provider]
                        )
                    else:
                        provider_results[provider] = {
                            "error": "No response",
                            "duration": duration
                        }
                        
                        reporter.add_test_result(
                            test_name=f"provider_{provider}",
                            status="FAIL",
                            duration=duration,
                            error="No response received"
                        )
                        
                except Exception as e:
                    provider_results[provider] = {
                        "error": str(e),
                        "duration": 0
                    }
                    print(f"❌ {provider} failed: {str(e)[:50]}")
            
            # Compare results
            print("\n📊 Provider Comparison:")
            
            best_speed = min(
                (p, r["duration"]) for p, r in provider_results.items()
                if "error" not in r
            ) if provider_results else (None, float('inf'))
            
            best_quality = max(
                (p, r.get("contains_key_terms", 0)) for p, r in provider_results.items()
                if "error" not in r
            ) if provider_results else (None, 0)
            
            if best_speed[0]:
                print(f"   Fastest: {best_speed[0]} ({best_speed[1]:.2f}s)")
            if best_quality[0]:
                print(f"   Best quality: {best_quality[0]} (score: {best_quality[1]})")
            
            self.record_test("provider_comparison", True, {
                "providers_tested": len(provider_results),
                "results": provider_results,
                "best_speed": best_speed,
                "best_quality": best_quality
            })
            
            # Generate comparison report
            comparison_report = reporter.generate_report()
            
            if comparison_report:
                with open("provider_comparison_report.html", 'w') as f:
                    f.write(comparison_report)
                print("\n✅ Comparison report generated")
                
        except Exception as e:
            self.add_bug(
                "Exception in provider comparison",
                "HIGH",
                error=str(e)
            )
            self.record_test("provider_comparison", False, {"error": str(e)})
    
    def run_tests(self):
        """Run all tests"""
        self.test_llm_quality_analysis()
        self.test_provider_comparison()
        return self.generate_report()


def main():
    """Run the test"""
    tester = LLMCallToTestReporterPipelineTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)