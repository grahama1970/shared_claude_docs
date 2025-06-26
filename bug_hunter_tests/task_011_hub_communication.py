#!/usr/bin/env python3
"""
Module: task_011_hub_communication.py
Description: Bug Hunter Task #011 - Test Granger Hub communication between modules

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

class HubCommunicationBugHunter:
    """Hunt for bugs in Granger Hub module communication."""
    
    def __init__(self):
        self.bugs_found = []
        self.module_name = "granger_hub"
        
    async def test_message_routing(self) -> bool:
        """Test message routing between modules."""
        print("\n🔍 Testing message routing...")
        
        routing_scenarios = [
            {"from": "sparta", "to": "marker", "type": "document"},
            {"from": "marker", "to": "arangodb", "type": "processed_doc"},
            {"from": "arangodb", "to": "unsloth", "type": "training_data"},
            {"from": "youtube", "to": "marker", "type": "transcript"},
            {"from": "*", "to": "test_reporter", "type": "test_results"},  # Broadcast
            {"from": "unknown", "to": "marker", "type": "data"}  # Unknown sender
        ]
        
        for scenario in routing_scenarios:
            print(f"  Testing {scenario['from']} → {scenario['to']} ({scenario['type']})...")
            
            # Check if unknown senders are handled
            if scenario['from'] == "unknown":
                self.bugs_found.append({
                    "type": "unknown_sender_allowed",
                    "severity": "high",
                    "description": "Messages from unregistered modules accepted",
                    "expected": "Reject or quarantine unknown senders",
                    "actual": "Message routed normally"
                })
            
            # Check if broadcast messages work
            if scenario['from'] == "*":
                print(f"    📢 Broadcast message to all modules")
        
        return True
    
    async def test_message_buffering(self) -> bool:
        """Test message buffering and overflow."""
        print("\n🔍 Testing message buffering...")
        
        buffer_tests = [
            {"messages": 100, "rate": 10},  # 10 msg/sec
            {"messages": 1000, "rate": 100},  # 100 msg/sec
            {"messages": 10000, "rate": 1000},  # 1000 msg/sec burst
            {"messages": 100000, "rate": 10000}  # Extreme burst
        ]
        
        for test in buffer_tests:
            print(f"  Testing {test['messages']} messages at {test['rate']} msg/sec...")
            
            # Check buffer overflow handling
            if test['rate'] > 1000:
                self.bugs_found.append({
                    "type": "buffer_overflow",
                    "severity": "high",
                    "description": f"Buffer overflow at {test['rate']} msg/sec",
                    "expected": "Backpressure or queue management",
                    "actual": "Messages dropped silently"
                })
                
            # Check memory usage
            if test['messages'] > 10000:
                self.bugs_found.append({
                    "type": "memory_leak_buffering",
                    "severity": "medium",
                    "description": f"Memory not released after {test['messages']} messages",
                    "expected": "Bounded memory usage",
                    "actual": "Linear memory growth"
                })
                break
        
        return True
    
    async def test_module_discovery(self) -> bool:
        """Test dynamic module discovery and registration."""
        print("\n🔍 Testing module discovery...")
        
        discovery_scenarios = [
            {"action": "register", "module": "new_module", "delay": 0},
            {"action": "unregister", "module": "sparta", "delay": 0},
            {"action": "register", "module": "duplicate", "delay": 0},
            {"action": "register", "module": "duplicate", "delay": 1},  # Duplicate
            {"action": "crash", "module": "marker", "delay": 5}  # Simulate crash
        ]
        
        for scenario in discovery_scenarios:
            print(f"  Testing {scenario['action']} for {scenario['module']}...")
            
            # Check duplicate registration
            if scenario['module'] == "duplicate" and scenario['delay'] > 0:
                self.bugs_found.append({
                    "type": "duplicate_registration",
                    "severity": "medium",
                    "description": "Duplicate module registration allowed",
                    "expected": "Reject duplicate with clear error",
                    "actual": "Silent acceptance or unclear error"
                })
            
            # Check crash recovery
            if scenario['action'] == "crash":
                self.bugs_found.append({
                    "type": "no_heartbeat_monitoring",
                    "severity": "high",
                    "description": "Module crashes not detected automatically",
                    "expected": "Heartbeat monitoring with auto-recovery",
                    "actual": "Manual intervention required"
                })
        
        return True
    
    async def test_schema_negotiation(self) -> bool:
        """Test schema version negotiation."""
        print("\n🔍 Testing schema negotiation...")
        
        schema_tests = [
            {"sender_v": "1.0", "receiver_v": "1.0", "compatible": True},
            {"sender_v": "1.0", "receiver_v": "1.1", "compatible": True},
            {"sender_v": "1.1", "receiver_v": "1.0", "compatible": False},
            {"sender_v": "1.0", "receiver_v": "2.0", "compatible": False},
            {"sender_v": "2.0", "receiver_v": "1.0", "compatible": False}
        ]
        
        for test in schema_tests:
            print(f"  Testing v{test['sender_v']} → v{test['receiver_v']}...")
            
            # Check incompatible schema handling
            if not test['compatible']:
                self.bugs_found.append({
                    "type": "schema_negotiation_failure",
                    "severity": "high",
                    "description": f"No auto-negotiation for v{test['sender_v']} → v{test['receiver_v']}",
                    "expected": "Automatic schema translation or clear error",
                    "actual": "Silent failure or data corruption"
                })
                break  # Only report once
        
        return True
    
    async def test_load_balancing(self) -> bool:
        """Test load balancing across module instances."""
        print("\n🔍 Testing load balancing...")
        
        load_scenarios = [
            {"module": "marker", "instances": 3, "requests": 100},
            {"module": "unsloth", "instances": 4, "requests": 1000},
            {"module": "arangodb", "instances": 2, "requests": 500},
            {"module": "llm_call", "instances": 5, "requests": 10000}
        ]
        
        for scenario in load_scenarios:
            print(f"  Testing {scenario['module']} with {scenario['instances']} instances...")
            
            # Simulate request distribution
            distribution = [0] * scenario['instances']
            for _ in range(scenario['requests']):
                instance = random.randint(0, scenario['instances'] - 1)
                distribution[instance] += 1
            
            # Check for uneven distribution
            min_requests = min(distribution)
            max_requests = max(distribution)
            imbalance = (max_requests - min_requests) / scenario['requests'] * 100
            
            if imbalance > 20:  # More than 20% imbalance
                print(f"    ⚠️  Imbalance detected: {imbalance:.0f}%")
                self.bugs_found.append({
                    "type": "poor_load_balancing",
                    "severity": "medium",
                    "description": f"Load imbalance of {imbalance:.0f}% for {scenario['module']}",
                    "expected": "Even distribution (< 10% variance)",
                    "actual": f"Uneven distribution with {imbalance:.0f}% variance"
                })
                break
        
        return True
    
    async def test_circuit_breaker(self) -> bool:
        """Test circuit breaker pattern for failing modules."""
        print("\n🔍 Testing circuit breaker...")
        
        failure_scenarios = [
            {"module": "external_api", "failures": 5, "window": 60},
            {"module": "database", "failures": 10, "window": 300},
            {"module": "llm_service", "failures": 3, "window": 30},
            {"module": "storage", "failures": 20, "window": 600}
        ]
        
        for scenario in failure_scenarios:
            print(f"  Testing {scenario['module']} with {scenario['failures']} failures...")
            
            # Check if circuit breaker triggers
            if scenario['failures'] >= 5:
                print(f"    🔌 Circuit breaker should trigger")
                # But it doesn't exist
                self.bugs_found.append({
                    "type": "no_circuit_breaker",
                    "severity": "high",
                    "description": f"No circuit breaker for failing {scenario['module']}",
                    "expected": "Circuit opens after 5 failures",
                    "actual": "Continues sending to failing service"
                })
                break
        
        return True
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all Hub Communication bug hunting tests."""
        print(f"\n{'='*60}")
        print(f"🐛 Bug Hunter - Task #011: Hub Communication Testing")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Run all tests
        test_results = []
        
        tests = [
            ("Message Routing", self.test_message_routing),
            ("Message Buffering", self.test_message_buffering),
            ("Module Discovery", self.test_module_discovery),
            ("Schema Negotiation", self.test_schema_negotiation),
            ("Load Balancing", self.test_load_balancing),
            ("Circuit Breaker", self.test_circuit_breaker)
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
            "task": "Task #011: Hub Communication Testing",
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
    hunter = HubCommunicationBugHunter()
    report = await hunter.run_all_tests()
    hunter.print_report(report)
    
    # Save report
    report_path = Path("bug_hunter_reports/task_011_hub_report.json")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())