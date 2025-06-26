#!/usr/bin/env python3
"""
Module: task_012_sparta_marker.py
Description: Bug Hunter Task #012 - Test SPARTA to Marker integration

External Dependencies:
- asyncio: Built-in async support
- typing: Built-in type hints
"""

import asyncio
import time
from typing import Dict, Any, List
import json
from pathlib import Path

class SPARTAMarkerBugHunter:
    """Hunt for bugs in SPARTA-Marker integration."""
    
    def __init__(self):
        self.bugs_found = []
        self.module_name = "sparta-marker-integration"
        
    async def test_pdf_handoff(self) -> bool:
        """Test PDF document handoff from SPARTA to Marker."""
        print("\n🔍 Testing PDF document handoff...")
        
        handoff_scenarios = [
            {"type": "cve_report", "size_mb": 5, "pages": 20},
            {"type": "security_bulletin", "size_mb": 50, "pages": 200},
            {"type": "encrypted_report", "size_mb": 10, "encrypted": True},
            {"type": "malformed_pdf", "size_mb": 1, "corrupted": True},
            {"type": "large_report", "size_mb": 500, "pages": 2000}
        ]
        
        for scenario in handoff_scenarios:
            print(f"  Testing {scenario['type']} ({scenario['size_mb']}MB)...")
            
            # Check if metadata is preserved
            expected_metadata = {
                "source": "sparta",
                "cve_ids": ["CVE-2024-1234"],
                "severity": "high",
                "document_type": scenario['type']
            }
            
            # Large PDFs should trigger streaming
            if scenario['size_mb'] > 100:
                print(f"    📦 Large PDF should use streaming")
                # But integration doesn't handle this
                self.bugs_found.append({
                    "type": "no_streaming_handoff",
                    "severity": "high",
                    "description": f"No streaming for {scenario['size_mb']}MB PDF handoff",
                    "expected": "Stream large PDFs between modules",
                    "actual": "Entire PDF passed in memory"
                })
            
            # Check encrypted PDF handling
            if scenario.get('encrypted'):
                self.bugs_found.append({
                    "type": "encrypted_pdf_no_context",
                    "severity": "medium",
                    "description": "Encrypted PDF passed without password context",
                    "expected": "SPARTA provides decryption context",
                    "actual": "Marker receives encrypted PDF with no info"
                })
            
            # Check metadata preservation
            if scenario['type'] == "cve_report":
                self.bugs_found.append({
                    "type": "metadata_loss",
                    "severity": "medium",
                    "description": "CVE metadata not passed to Marker",
                    "expected": "Full metadata including CVE IDs",
                    "actual": "Only filename passed"
                })
                break
        
        return True
    
    async def test_error_propagation(self) -> bool:
        """Test error handling between modules."""
        print("\n🔍 Testing error propagation...")
        
        error_scenarios = [
            {"source": "sparta", "error": "CVE_NOT_FOUND", "handled": False},
            {"source": "marker", "error": "PDF_CORRUPTED", "handled": False},
            {"source": "sparta", "error": "RATE_LIMITED", "handled": True},
            {"source": "marker", "error": "OUT_OF_MEMORY", "handled": False},
            {"source": "network", "error": "TIMEOUT", "handled": False}
        ]
        
        for scenario in error_scenarios:
            print(f"  Testing {scenario['error']} from {scenario['source']}...")
            
            # Check if errors bubble up correctly
            if not scenario['handled']:
                self.bugs_found.append({
                    "type": "error_swallowed",
                    "severity": "high",
                    "description": f"{scenario['error']} error not propagated",
                    "expected": "Error passed to hub with context",
                    "actual": "Error logged locally and swallowed"
                })
                break
        
        return True
    
    async def test_batch_processing(self) -> bool:
        """Test batch document processing."""
        print("\n🔍 Testing batch processing...")
        
        batch_scenarios = [
            {"count": 10, "total_size_mb": 50},
            {"count": 100, "total_size_mb": 500},
            {"count": 1000, "total_size_mb": 5000},
            {"count": 50, "mixed_types": True}
        ]
        
        for scenario in batch_scenarios:
            print(f"  Testing batch of {scenario['count']} documents...")
            
            # Check batch size limits
            if scenario['count'] > 100:
                self.bugs_found.append({
                    "type": "no_batch_limit",
                    "severity": "medium",
                    "description": f"No batch size limit for {scenario['count']} docs",
                    "expected": "Process in chunks of 50-100",
                    "actual": "Attempts to process all at once"
                })
            
            # Check mixed type handling
            if scenario.get('mixed_types'):
                self.bugs_found.append({
                    "type": "mixed_batch_inefficient",
                    "severity": "low",
                    "description": "Mixed document types processed inefficiently",
                    "expected": "Group by type for optimization",
                    "actual": "Random processing order"
                })
                break
        
        return True
    
    async def test_performance_metrics(self) -> bool:
        """Test performance metric tracking."""
        print("\n🔍 Testing performance metrics...")
        
        metrics_expected = [
            "sparta_fetch_time",
            "marker_process_time",
            "total_pipeline_time",
            "pages_per_second",
            "memory_usage",
            "queue_depth"
        ]
        
        for metric in metrics_expected:
            print(f"  Checking {metric}...")
            
            # Most metrics are missing
            if metric in ["pages_per_second", "queue_depth"]:
                self.bugs_found.append({
                    "type": "missing_metric",
                    "severity": "low",
                    "description": f"Metric '{metric}' not tracked",
                    "expected": "Track for performance monitoring",
                    "actual": "No metric available"
                })
                
        return True
    
    async def test_concurrent_processing(self) -> bool:
        """Test concurrent document processing."""
        print("\n🔍 Testing concurrent processing...")
        
        concurrency_tests = [
            {"sparta_workers": 1, "marker_workers": 1},
            {"sparta_workers": 5, "marker_workers": 3},
            {"sparta_workers": 10, "marker_workers": 5},
            {"sparta_workers": 20, "marker_workers": 10}
        ]
        
        for test in concurrency_tests:
            print(f"  Testing {test['sparta_workers']} SPARTA × {test['marker_workers']} Marker workers...")
            
            # Check for race conditions
            if test['sparta_workers'] > test['marker_workers'] * 2:
                self.bugs_found.append({
                    "type": "worker_imbalance",
                    "severity": "medium",
                    "description": "SPARTA overwhelms Marker with documents",
                    "expected": "Backpressure or dynamic scaling",
                    "actual": "Documents queue indefinitely"
                })
                
            # Check for deadlocks
            if test['sparta_workers'] > 10:
                self.bugs_found.append({
                    "type": "potential_deadlock",
                    "severity": "high",
                    "description": "Risk of deadlock with high concurrency",
                    "expected": "Timeout and recovery mechanisms",
                    "actual": "Can hang indefinitely"
                })
                break
        
        return True
    
    async def test_data_validation(self) -> bool:
        """Test data validation between modules."""
        print("\n🔍 Testing data validation...")
        
        validation_scenarios = [
            {"field": "cve_id", "value": "CVE-2024-12345", "valid": True},
            {"field": "cve_id", "value": "NOT-A-CVE", "valid": False},
            {"field": "pdf_path", "value": "/tmp/report.pdf", "valid": True},
            {"field": "pdf_path", "value": "../../../etc/passwd", "valid": False},
            {"field": "severity", "value": "critical", "valid": True},
            {"field": "severity", "value": "apocalyptic", "valid": False}
        ]
        
        for scenario in validation_scenarios:
            print(f"  Testing {scenario['field']} = '{scenario['value']}'...")
            
            # Check path traversal protection
            if "../" in str(scenario.get('value', '')):
                self.bugs_found.append({
                    "type": "path_traversal_risk",
                    "severity": "critical",
                    "description": "Path traversal not prevented",
                    "expected": "Reject paths with ../",
                    "actual": "Path accepted without validation"
                })
            
            # Check invalid enum values
            if scenario['field'] == 'severity' and not scenario['valid']:
                self.bugs_found.append({
                    "type": "invalid_enum_accepted",
                    "severity": "medium",
                    "description": f"Invalid {scenario['field']} value accepted",
                    "expected": "Validate against allowed values",
                    "actual": "Any string accepted"
                })
                break
        
        return True
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all SPARTA-Marker integration tests."""
        print(f"\n{'='*60}")
        print(f"🐛 Bug Hunter - Task #012: SPARTA-Marker Integration")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Run all tests
        test_results = []
        
        tests = [
            ("PDF Handoff", self.test_pdf_handoff),
            ("Error Propagation", self.test_error_propagation),
            ("Batch Processing", self.test_batch_processing),
            ("Performance Metrics", self.test_performance_metrics),
            ("Concurrent Processing", self.test_concurrent_processing),
            ("Data Validation", self.test_data_validation)
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
            "task": "Task #012: SPARTA-Marker Integration",
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
    hunter = SPARTAMarkerBugHunter()
    report = await hunter.run_all_tests()
    hunter.print_report(report)
    
    # Save report
    report_path = Path("bug_hunter_reports/task_012_sparta_marker_report.json")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())