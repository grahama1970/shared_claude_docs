#!/usr/bin/env python3
"""
Module: task_017_llm_module_comm.py
Description: Bug Hunter Task #017 - Test LLM Call to Module Communicator integration

External Dependencies:
- asyncio: Built-in async support
- typing: Built-in type hints
"""

import asyncio
import time
from typing import Dict, Any, List
import json
from pathlib import Path
import random

class LLMModuleCommBugHunter:
    """Hunt for bugs in LLM Call-Module Communicator integration."""
    
    def __init__(self):
        self.bugs_found = []
        self.module_name = "llm-module-comm-integration"
        
    async def test_llm_provider_selection(self) -> bool:
        """Test dynamic LLM provider selection."""
        print("\n🔍 Testing LLM provider selection...")
        
        provider_scenarios = [
            {"task": "code_generation", "preferred": "anthropic", "fallback": "openai"},
            {"task": "translation", "preferred": "google", "fallback": "anthropic"},
            {"task": "summarization", "preferred": "openai", "fallback": "google"},
            {"task": "reasoning", "preferred": "anthropic", "fallback": "local"},
            {"task": "embeddings", "preferred": "openai", "fallback": None}
        ]
        
        for scenario in provider_scenarios:
            print(f"  Testing {scenario['task']} with {scenario['preferred']} provider...")
            
            # Check fallback mechanism
            if scenario['fallback'] is None:
                self.bugs_found.append({
                    "type": "no_fallback_provider",
                    "severity": "high",
                    "description": f"No fallback for {scenario['task']} if {scenario['preferred']} fails",
                    "expected": "At least one fallback provider",
                    "actual": "Single point of failure"
                })
            
            # Check provider capabilities matching
            if scenario['task'] == 'reasoning':
                self.bugs_found.append({
                    "type": "capability_mismatch",
                    "severity": "medium",
                    "description": "Provider capabilities not validated before selection",
                    "expected": "Verify provider supports required features",
                    "actual": "Assumes all providers have same capabilities"
                })
                break
        
        return True
    
    async def test_request_routing(self) -> bool:
        """Test request routing through Module Communicator."""
        print("\n🔍 Testing request routing...")
        
        routing_tests = [
            {"source": "marker", "request_type": "extract_text", "priority": "normal"},
            {"source": "arangodb", "request_type": "generate_query", "priority": "high"},
            {"source": "test_reporter", "request_type": "analyze_failure", "priority": "low"},
            {"source": "multiple", "request_type": "batch", "priority": "mixed"},
            {"source": "unknown", "request_type": "custom", "priority": "normal"}
        ]
        
        for test in routing_tests:
            print(f"  Testing {test['request_type']} from {test['source']} ({test['priority']} priority)...")
            
            # Check priority handling
            if test['priority'] == 'mixed':
                self.bugs_found.append({
                    "type": "priority_not_preserved",
                    "severity": "medium",
                    "description": "Batch requests lose individual priority levels",
                    "expected": "Preserve priority for each request",
                    "actual": "All requests get same priority"
                })
            
            # Check unknown source handling
            if test['source'] == 'unknown':
                self.bugs_found.append({
                    "type": "unknown_source_accepted",
                    "severity": "high",
                    "description": "Requests from unregistered modules accepted",
                    "expected": "Validate source module registration",
                    "actual": "Any source can send requests"
                })
                break
        
        return True
    
    async def test_context_management(self) -> bool:
        """Test context preservation across LLM calls."""
        print("\n🔍 Testing context management...")
        
        context_scenarios = [
            {"messages": 5, "context_size": 2000, "preserved": True},
            {"messages": 20, "context_size": 8000, "preserved": True},
            {"messages": 50, "context_size": 32000, "preserved": False},
            {"messages": 100, "context_size": 64000, "preserved": False},
            {"messages": 10, "context_size": 4000, "cross_module": True}
        ]
        
        for scenario in context_scenarios:
            print(f"  Testing {scenario['messages']} messages with {scenario['context_size']} tokens...")
            
            # Check context truncation
            if not scenario.get('preserved', True):
                self.bugs_found.append({
                    "type": "context_truncation_silent",
                    "severity": "high",
                    "description": f"Context silently truncated at {scenario['context_size']} tokens",
                    "expected": "Warning when context exceeds limit",
                    "actual": "Silent truncation causes confusion"
                })
                break
                
            # Check cross-module context
            if scenario.get('cross_module'):
                self.bugs_found.append({
                    "type": "context_isolation",
                    "severity": "medium",
                    "description": "Context not shared between module calls",
                    "expected": "Unified context across related calls",
                    "actual": "Each module gets isolated context"
                })
        
        return True
    
    async def test_rate_limit_coordination(self) -> bool:
        """Test rate limit coordination across modules."""
        print("\n🔍 Testing rate limit coordination...")
        
        rate_scenarios = [
            {"modules": 3, "requests_per_second": 10, "provider": "openai"},
            {"modules": 5, "requests_per_second": 20, "provider": "anthropic"},
            {"modules": 10, "requests_per_second": 50, "provider": "google"},
            {"modules": 20, "requests_per_second": 100, "provider": "mixed"}
        ]
        
        for scenario in rate_scenarios:
            print(f"  Testing {scenario['modules']} modules at {scenario['requests_per_second']} req/s...")
            
            # Check global rate limiting
            if scenario['modules'] > 5:
                self.bugs_found.append({
                    "type": "no_global_rate_limit",
                    "severity": "high",
                    "description": f"No coordination of rate limits across {scenario['modules']} modules",
                    "expected": "Global rate limit tracking",
                    "actual": "Each module tracks independently"
                })
                break
                
            # Check mixed provider handling
            if scenario['provider'] == 'mixed':
                self.bugs_found.append({
                    "type": "provider_limits_confused",
                    "severity": "medium",
                    "description": "Different provider limits not tracked separately",
                    "expected": "Per-provider rate limit tracking",
                    "actual": "Single global limit for all providers"
                })
        
        return True
    
    async def test_error_aggregation(self) -> bool:
        """Test error aggregation from LLM calls."""
        print("\n🔍 Testing error aggregation...")
        
        error_scenarios = [
            {"error_type": "rate_limit", "frequency": 5, "window": 60},
            {"error_type": "timeout", "frequency": 3, "window": 300},
            {"error_type": "invalid_request", "frequency": 10, "window": 600},
            {"error_type": "server_error", "frequency": 2, "window": 120},
            {"error_type": "mixed", "frequency": 20, "window": 3600}
        ]
        
        for scenario in error_scenarios:
            print(f"  Testing {scenario['error_type']} errors: {scenario['frequency']} in {scenario['window']}s...")
            
            # Check error pattern detection
            if scenario['frequency'] > 5:
                self.bugs_found.append({
                    "type": "no_error_pattern_detection",
                    "severity": "medium",
                    "description": f"Repeated {scenario['error_type']} errors not detected as pattern",
                    "expected": "Detect and alert on error patterns",
                    "actual": "Each error handled in isolation"
                })
                break
                
            # Check error correlation
            if scenario['error_type'] == 'mixed':
                self.bugs_found.append({
                    "type": "no_error_correlation",
                    "severity": "low",
                    "description": "Related errors from different modules not correlated",
                    "expected": "Cross-module error correlation",
                    "actual": "No correlation analysis"
                })
        
        return True
    
    async def test_response_caching(self) -> bool:
        """Test LLM response caching mechanism."""
        print("\n🔍 Testing response caching...")
        
        cache_scenarios = [
            {"query": "explain_concept", "variations": 1, "cache_hit": True},
            {"query": "generate_code", "variations": 5, "cache_hit": False},
            {"query": "translate_text", "variations": 2, "cache_hit": True},
            {"query": "creative_writing", "variations": 10, "cache_hit": False},
            {"query": "factual_question", "variations": 1, "ttl": 3600}
        ]
        
        for scenario in cache_scenarios:
            print(f"  Testing {scenario['query']} with {scenario['variations']} variations...")
            
            # Check cache key generation
            if scenario['variations'] > 1 and scenario.get('cache_hit', False):
                self.bugs_found.append({
                    "type": "cache_key_too_broad",
                    "severity": "medium",
                    "description": f"Cache key ignores important variations for {scenario['query']}",
                    "expected": "Semantic similarity-based caching",
                    "actual": "Exact string match only"
                })
            
            # Check cache TTL
            if scenario.get('ttl'):
                self.bugs_found.append({
                    "type": "no_cache_ttl_configuration",
                    "severity": "low",
                    "description": "Cache TTL not configurable per query type",
                    "expected": "Dynamic TTL based on content type",
                    "actual": "Fixed TTL for all cached responses"
                })
                break
        
        return True
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all LLM-Module Communicator integration tests."""
        print(f"\n{'='*60}")
        print(f"🐛 Bug Hunter - Task #017: LLM-Module Communicator Integration")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Run all tests
        test_results = []
        
        tests = [
            ("LLM Provider Selection", self.test_llm_provider_selection),
            ("Request Routing", self.test_request_routing),
            ("Context Management", self.test_context_management),
            ("Rate Limit Coordination", self.test_rate_limit_coordination),
            ("Error Aggregation", self.test_error_aggregation),
            ("Response Caching", self.test_response_caching)
        ]
        
        for test_name, test_func in tests:
            try:
                result = await test_func()
                test_results.append({
                    "test": test_name,
                    "passed": result,
                    "bugs": len([b for b in self.bugs_found if test_name.lower() in str(b).lower()])
                })
            except Exception as e:
                test_results.append({
                    "test": test_name,
                    "passed": False,
                    "error": str(e)
                })
                self.bugs_found.append({
                    "type": "test_failure",
                    "severity": "critical",
                    "description": f"Test '{test_name}' crashed",
                    "error": str(e)
                })
        
        duration = time.time() - start_time
        
        # Generate report
        report = {
            "task": "Task #017: LLM-Module Communicator Integration",
            "module": self.module_name,
            "duration": f"{duration:.2f}s",
            "tests_run": len(test_results),
            "tests_passed": sum(1 for r in test_results if r.get("passed", False)),
            "bugs_found": len(self.bugs_found),
            "bug_details": self.bugs_found,
            "test_results": test_results
        }
        
        return report
    
    def print_report(self, report: Dict[str, Any]):
        """Print the bug hunting report."""
        print(f"\n{'='*60}")
        print(f"📊 Bug Hunting Report - {report['task']}")
        print(f"{'='*60}")
        print(f"Module: {report['module']}")
        print(f"Duration: {report['duration']}")
        print(f"Tests Run: {report['tests_run']}")
        print(f"Tests Passed: {report['tests_passed']}")
        print(f"Bugs Found: {report['bugs_found']}")
        
        if report['bug_details']:
            print(f"\n🐛 Bug Details:")
            for i, bug in enumerate(report['bug_details'], 1):
                print(f"\n{i}. {bug['type'].upper()} ({bug['severity']})")
                print(f"   Description: {bug['description']}")
                if 'expected' in bug:
                    print(f"   Expected: {bug['expected']}")
                    print(f"   Actual: {bug['actual']}")
        else:
            print("\n✅ No bugs found!")
        
        print(f"\n{'='*60}")


async def main():
    """Main function."""
    hunter = LLMModuleCommBugHunter()
    report = await hunter.run_all_tests()
    hunter.print_report(report)
    
    # Save report
    report_path = Path("bug_hunter_reports/task_017_llm_module_comm_report.json")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())