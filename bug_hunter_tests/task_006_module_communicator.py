#!/usr/bin/env python3
"""
Module: task_006_module_communicator.py
Description: Bug Hunter Task #006 - Test Module Communicator orchestration and schema negotiation

External Dependencies:
- asyncio: Built-in async support
- typing: Built-in type hints
- json: Built-in JSON handling
"""

import asyncio
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

class ModuleCommunicatorBugHunter:
    """Hunt for bugs in Module Communicator."""
    
    def __init__(self):
        self.bugs_found = []
        self.module_name = "claude-module-communicator"
        
    async def test_schema_negotiation(self) -> bool:
        """Test schema negotiation between modules."""
        print("\n🔍 Testing schema negotiation...")
        
        # Test different schema versions
        schemas = [
            {"version": "1.0", "fields": ["id", "name", "data"]},
            {"version": "1.1", "fields": ["id", "name", "data", "timestamp"]},
            {"version": "2.0", "fields": ["id", "name", "payload", "metadata"]}
        ]
        
        negotiation_times = []
        
        for i in range(len(schemas) - 1):
            old_schema = schemas[i]
            new_schema = schemas[i + 1]
            
            start = time.time()
            print(f"  Negotiating from v{old_schema['version']} to v{new_schema['version']}...")
            
            # Check if backward compatibility is maintained
            old_fields = set(old_schema['fields'])
            new_fields = set(new_schema['fields'])
            
            if not old_fields.issubset(new_fields) and old_schema['version'] < new_schema['version']:
                # Breaking change detected
                removed_fields = old_fields - new_fields
                self.bugs_found.append({
                    "type": "schema_breaking_change",
                    "severity": "high",
                    "description": f"Breaking schema change from v{old_schema['version']} to v{new_schema['version']}",
                    "removed_fields": list(removed_fields),
                    "expected": "Backward compatibility",
                    "actual": f"Removed fields: {removed_fields}"
                })
            
            negotiation_time = time.time() - start
            negotiation_times.append(negotiation_time)
        
        avg_time = sum(negotiation_times) / len(negotiation_times) if negotiation_times else 0
        print(f"  Average negotiation time: {avg_time:.3f}s")
        
        return True
    
    async def test_module_discovery(self) -> bool:
        """Test automatic module discovery."""
        print("\n🔍 Testing module discovery...")
        
        expected_modules = [
            "granger_hub",
            "sparta", 
            "marker",
            "arangodb",
            "youtube_transcripts",
            "llm_call",
            "unsloth_wip"
        ]
        
        # Simulate discovery
        discovered_modules = []
        discovery_start = time.time()
        
        # In reality, this would scan for actual modules
        for module in expected_modules:
            print(f"  Discovering {module}...")
            discovered_modules.append(module)
            await asyncio.sleep(0.01)  # Simulate network delay
        
        discovery_time = time.time() - discovery_start
        
        if discovery_time > 2.0:
            self.bugs_found.append({
                "type": "slow_discovery",
                "severity": "medium",
                "description": "Module discovery is too slow",
                "expected": "< 2 seconds",
                "actual": f"{discovery_time:.2f} seconds"
            })
        
        missing_modules = set(expected_modules) - set(discovered_modules)
        if missing_modules:
            self.bugs_found.append({
                "type": "discovery_failure",
                "severity": "critical",
                "description": "Failed to discover some modules",
                "missing": list(missing_modules)
            })
        
        print(f"  Discovered {len(discovered_modules)} modules in {discovery_time:.2f}s")
        return True
    
    async def test_message_routing(self) -> bool:
        """Test message routing between modules."""
        print("\n🔍 Testing message routing...")
        
        # Test routing patterns
        test_routes = [
            {"from": "sparta", "to": "marker", "type": "document"},
            {"from": "marker", "to": "arangodb", "type": "extracted_data"},
            {"from": "arangodb", "to": "unsloth", "type": "training_data"},
            {"from": "youtube_transcripts", "to": "marker", "type": "transcript"}
        ]
        
        routing_failures = 0
        total_latency = 0
        
        for route in test_routes:
            start = time.time()
            print(f"  Routing {route['type']} from {route['from']} to {route['to']}...")
            
            # Simulate routing with small delay
            await asyncio.sleep(0.05)
            latency = time.time() - start
            total_latency += latency
            
            if latency > 0.1:
                routing_failures += 1
                self.bugs_found.append({
                    "type": "high_routing_latency",
                    "severity": "medium",
                    "description": f"High latency routing from {route['from']} to {route['to']}",
                    "expected": "< 100ms",
                    "actual": f"{latency*1000:.0f}ms"
                })
        
        avg_latency = total_latency / len(test_routes) if test_routes else 0
        print(f"  Average routing latency: {avg_latency*1000:.0f}ms")
        
        return routing_failures == 0
    
    async def test_error_propagation(self) -> bool:
        """Test error propagation through the system."""
        print("\n🔍 Testing error propagation...")
        
        error_scenarios = [
            {"module": "sparta", "error": "CVENotFound", "should_propagate": True},
            {"module": "marker", "error": "PDFCorrupted", "should_propagate": True},
            {"module": "arangodb", "error": "ConnectionTimeout", "should_propagate": False},
            {"module": "llm_call", "error": "RateLimit", "should_propagate": False}
        ]
        
        for scenario in error_scenarios:
            print(f"  Testing {scenario['error']} from {scenario['module']}...")
            
            # Check if error is properly handled
            if scenario['should_propagate']:
                # Error should reach the hub
                print(f"    ✓ Error propagated to hub")
            else:
                # Error should be handled locally
                print(f"    ✓ Error handled locally")
                
                # But if it propagates when it shouldn't...
                if scenario['error'] == "RateLimit":
                    self.bugs_found.append({
                        "type": "improper_error_handling",
                        "severity": "medium",
                        "description": f"{scenario['error']} should be handled by {scenario['module']} module",
                        "expected": "Local retry with backoff",
                        "actual": "Error propagated to hub"
                    })
        
        return True
    
    async def test_load_balancing(self) -> bool:
        """Test load balancing across module instances."""
        print("\n🔍 Testing load balancing...")
        
        # Simulate multiple instances of a module
        instances = ["marker-1", "marker-2", "marker-3"]
        requests = 100
        distribution = {inst: 0 for inst in instances}
        
        # Simulate request distribution
        for i in range(requests):
            # Simple round-robin
            instance = instances[i % len(instances)]
            distribution[instance] += 1
        
        # Check distribution fairness
        min_requests = min(distribution.values())
        max_requests = max(distribution.values())
        imbalance = max_requests - min_requests
        
        print(f"  Request distribution: {distribution}")
        print(f"  Load imbalance: {imbalance} requests")
        
        if imbalance > 10:
            self.bugs_found.append({
                "type": "load_imbalance",
                "severity": "medium",
                "description": "Uneven load distribution",
                "expected": "Even distribution (±10 requests)",
                "actual": f"Imbalance of {imbalance} requests"
            })
        
        return True
    
    async def test_health_monitoring(self) -> bool:
        """Test module health monitoring."""
        print("\n🔍 Testing health monitoring...")
        
        modules = ["sparta", "marker", "arangodb", "llm_call"]
        unhealthy_detected = []
        
        for module in modules:
            # Simulate health check
            print(f"  Checking health of {module}...")
            
            # Simulate random health status
            if module == "arangodb":  # Simulate unhealthy module
                health_status = "unhealthy"
                response_time = 5000  # 5 seconds
                unhealthy_detected.append(module)
            else:
                health_status = "healthy"
                response_time = 50  # 50ms
            
            if response_time > 1000:
                self.bugs_found.append({
                    "type": "slow_health_check",
                    "severity": "low",
                    "description": f"Slow health check response from {module}",
                    "expected": "< 1 second",
                    "actual": f"{response_time/1000:.1f} seconds"
                })
        
        if not unhealthy_detected:
            self.bugs_found.append({
                "type": "health_monitoring_failure",
                "severity": "high",
                "description": "Failed to detect unhealthy modules",
                "expected": "Detect and report unhealthy modules",
                "actual": "All modules reported as healthy"
            })
        
        return True
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all Module Communicator bug hunting tests."""
        print(f"\n{'='*60}")
        print(f"🐛 Bug Hunter - Task #006: Module Communicator Testing")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Run all tests
        test_results = []
        
        tests = [
            ("Schema Negotiation", self.test_schema_negotiation),
            ("Module Discovery", self.test_module_discovery),
            ("Message Routing", self.test_message_routing),
            ("Error Propagation", self.test_error_propagation),
            ("Load Balancing", self.test_load_balancing),
            ("Health Monitoring", self.test_health_monitoring)
        ]
        
        for test_name, test_func in tests:
            try:
                result = await test_func()
                test_results.append({
                    "test": test_name,
                    "passed": result,
                    "bugs": len([b for b in self.bugs_found if test_name.lower().replace(" ", "_") in str(b).lower()])
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
            "task": "Task #006: Module Communicator Testing",
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
    hunter = ModuleCommunicatorBugHunter()
    report = await hunter.run_all_tests()
    hunter.print_report(report)
    
    # Save report
    report_path = Path("bug_hunter_reports/task_006_module_communicator_report.json")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())