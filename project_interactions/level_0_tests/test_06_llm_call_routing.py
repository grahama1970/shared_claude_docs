#!/usr/bin/env python3
"""
Module: test_06_llm_call_routing.py
Description: Test LLM Call routing and provider selection with verification
Level: 0
Modules: LLM Call, Test Reporter
Expected Bugs: Provider failures, API key issues, routing logic errors
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest

class LLMCallRoutingTest(BaseInteractionTest):
    """Level 0: Test LLM Call routing functionality"""
    
    def __init__(self):
        super().__init__(
            test_name="LLM Call Routing",
            level=0,
            modules=["LLM Call", "Test Reporter"]
        )
    
    def test_provider_selection(self):
        """Test routing to different LLM providers"""
        self.print_header()
        
        # Import LLM Call
        try:
            from llm_call import llm_call, get_available_providers
            self.record_test("llm_call_import", True, {})
        except ImportError as e:
            self.add_bug(
                "LLM Call module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot use LLM functionality"
            )
            self.record_test("llm_call_import", False, {"error": str(e)})
            return
        
        # Test provider availability
        print("Testing provider availability...")
        try:
            providers = get_available_providers()
            print(f"Available providers: {providers}")
            self.record_test("get_providers", True, {"providers": providers})
            
            if not providers:
                self.add_bug(
                    "No LLM providers available",
                    "HIGH",
                    impact="Cannot make any LLM calls"
                )
        except Exception as e:
            self.add_bug(
                "Exception getting providers",
                "HIGH",
                error=str(e)
            )
            self.record_test("get_providers", False, {"error": str(e)})
        
        # Test routing to different providers
        test_prompts = [
            {
                "name": "Simple prompt",
                "prompt": "Say hello",
                "provider": "openai"
            },
            {
                "name": "Long prompt",
                "prompt": "Explain " * 500,  # Very long
                "provider": "anthropic"
            },
            {
                "name": "Code generation",
                "prompt": "Write a Python function to sort a list",
                "provider": "gemini"
            },
            {
                "name": "Invalid provider",
                "prompt": "Test",
                "provider": "invalid_provider"
            },
            {
                "name": "Empty prompt",
                "prompt": "",
                "provider": "openai"
            }
        ]
        
        for test in test_prompts:
            print(f"\nTesting: {test['name']} with {test['provider']}")
            
            try:
                result = llm_call(
                    prompt=test["prompt"],
                    provider=test["provider"],
                    max_tokens=50
                )
                
                if result:
                    print(f"✅ Got response: {len(result)} chars")
                    self.record_test(f"llm_call_{test['name']}", True, {
                        "provider": test["provider"],
                        "response_length": len(result)
                    })
                    
                    # Check for quality issues
                    if test["name"] == "Empty prompt" and result:
                        self.add_bug(
                            "Empty prompt returns response",
                            "MEDIUM",
                            provider=test["provider"],
                            response=result[:50]
                        )
                else:
                    if test["name"] != "Invalid provider":
                        self.add_bug(
                            f"No response for {test['name']}",
                            "HIGH",
                            provider=test["provider"]
                        )
                    self.record_test(f"llm_call_{test['name']}", False, {
                        "provider": test["provider"],
                        "error": "No response"
                    })
                    
            except Exception as e:
                error_msg = str(e)
                print(f"💥 Exception: {error_msg[:100]}")
                
                # Check error quality
                if test["name"] == "Invalid provider" and "provider" not in error_msg.lower():
                    self.add_bug(
                        "Poor error for invalid provider",
                        "LOW",
                        error=error_msg
                    )
                
                self.record_test(f"llm_call_{test['name']}", False, {
                    "provider": test["provider"],
                    "error": error_msg
                })
    
    def test_fallback_behavior(self):
        """Test provider fallback when primary fails"""
        print("\n\nTesting Fallback Behavior...")
        
        try:
            from llm_call import llm_call_with_fallback
            
            # Test with invalid API key to force fallback
            original_key = os.environ.get("OPENAI_API_KEY")
            os.environ["OPENAI_API_KEY"] = "invalid_key"
            
            result = llm_call_with_fallback(
                prompt="Test fallback",
                providers=["openai", "anthropic", "gemini"],
                max_tokens=50
            )
            
            if result:
                print(f"✅ Fallback worked: {result['provider']} responded")
                self.record_test("fallback_success", True, {
                    "final_provider": result.get("provider")
                })
            else:
                self.add_bug(
                    "Fallback failed with all providers",
                    "HIGH",
                    impact="No resilience to provider failures"
                )
                self.record_test("fallback_success", False, {})
            
            # Restore key
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key
                
        except ImportError:
            print("❌ Fallback functionality not available")
            self.record_test("fallback_import", False, {"error": "Not implemented"})
        except Exception as e:
            self.add_bug(
                "Exception in fallback test",
                "MEDIUM",
                error=str(e)
            )
            self.record_test("fallback_test", False, {"error": str(e)})
    
    def test_cost_optimization(self):
        """Test cost-aware routing"""
        print("\n\nTesting Cost Optimization...")
        
        try:
            from llm_call import estimate_cost, get_cheapest_provider
            
            # Test cost estimation
            test_cases = [
                {"tokens": 100, "provider": "openai"},
                {"tokens": 1000, "provider": "anthropic"},
                {"tokens": 10000, "provider": "gemini"}
            ]
            
            for test in test_cases:
                cost = estimate_cost(
                    tokens=test["tokens"],
                    provider=test["provider"]
                )
                
                if cost is not None and cost >= 0:
                    print(f"✅ {test['provider']}: ${cost:.4f} for {test['tokens']} tokens")
                    self.record_test(f"cost_estimate_{test['provider']}", True, {
                        "cost": cost,
                        "tokens": test["tokens"]
                    })
                else:
                    self.add_bug(
                        f"Invalid cost for {test['provider']}",
                        "MEDIUM",
                        tokens=test["tokens"],
                        cost=cost
                    )
                    self.record_test(f"cost_estimate_{test['provider']}", False, {})
            
            # Test cheapest provider selection
            cheapest = get_cheapest_provider(tokens=1000)
            if cheapest:
                print(f"\n✅ Cheapest provider for 1000 tokens: {cheapest}")
                self.record_test("cheapest_provider", True, {"provider": cheapest})
            else:
                self.add_bug(
                    "Cannot determine cheapest provider",
                    "MEDIUM",
                    impact="Cost optimization not working"
                )
                
        except ImportError:
            print("❌ Cost optimization not available")
            self.record_test("cost_optimization", False, {"error": "Not implemented"})
        except Exception as e:
            self.add_bug(
                "Exception in cost optimization",
                "MEDIUM",
                error=str(e)
            )
    
    def run_tests(self):
        """Run all tests"""
        self.test_provider_selection()
        self.test_fallback_behavior()
        self.test_cost_optimization()
        return self.generate_report()


def main():
    """Run the test"""
    tester = LLMCallRoutingTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)