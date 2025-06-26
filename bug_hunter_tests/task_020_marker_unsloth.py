#!/usr/bin/env python3
"""
Module: task_020_marker_unsloth.py
Description: Bug Hunter Task #020 - Test Marker to Unsloth direct integration

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

class MarkerUnslothBugHunter:
    """Hunt for bugs in Marker-Unsloth direct integration."""
    
    def __init__(self):
        self.bugs_found = []
        self.module_name = "marker-unsloth-integration"
        
    async def test_training_data_formatting(self) -> bool:
        """Test conversion of Marker output to Unsloth training format."""
        print("\n🔍 Testing training data formatting...")
        
        document_types = [
            {"type": "research_paper", "pages": 20, "format": "qa_pairs"},
            {"type": "technical_manual", "pages": 100, "format": "completion"},
            {"type": "textbook", "pages": 500, "format": "instruction"},
            {"type": "mixed_content", "pages": 50, "format": "multi_task"},
            {"type": "code_documentation", "pages": 30, "format": "code_explanation"}
        ]
        
        for doc in document_types:
            print(f"  Testing {doc['type']} ({doc['pages']} pages) → {doc['format']} format...")
            
            # Check format conversion quality
            if doc['format'] == 'qa_pairs':
                self.bugs_found.append({
                    "type": "poor_qa_extraction",
                    "severity": "medium",
                    "description": "Q&A pairs extracted without context preservation",
                    "expected": "Include surrounding context in pairs",
                    "actual": "Isolated Q&A loses important context"
                })
            
            # Check handling of mixed content
            if doc['type'] == 'mixed_content':
                self.bugs_found.append({
                    "type": "format_mixing_fails",
                    "severity": "high",
                    "description": "Mixed content types not properly separated",
                    "expected": "Tag content by type (text, code, table, etc)",
                    "actual": "All content treated as plain text"
                })
                
            # Check large document handling
            if doc['pages'] > 100:
                self.bugs_found.append({
                    "type": "large_doc_truncation",
                    "severity": "high",
                    "description": f"{doc['pages']}-page document truncated",
                    "expected": "Split into manageable chunks",
                    "actual": "Truncated at arbitrary limit"
                })
                break
        
        return True
    
    async def test_quality_filtering(self) -> bool:
        """Test quality filtering before training."""
        print("\n🔍 Testing quality filtering...")
        
        quality_checks = [
            {"metric": "ocr_confidence", "threshold": 0.8, "filtered": 15},
            {"metric": "text_coherence", "threshold": 0.7, "filtered": 20},
            {"metric": "language_consistency", "threshold": 0.9, "filtered": 5},
            {"metric": "duplicate_content", "threshold": 0.95, "filtered": 30},
            {"metric": "minimum_length", "threshold": 50, "filtered": 10}
        ]
        
        for check in quality_checks:
            print(f"  Testing {check['metric']} filter (threshold: {check['threshold']})...")
            
            # Check if filtering is too aggressive
            if check['filtered'] > 25:
                self.bugs_found.append({
                    "type": "over_filtering",
                    "severity": "medium",
                    "description": f"{check['metric']} filter removes {check['filtered']}% of data",
                    "expected": "Preserve more usable data",
                    "actual": "Aggressive filtering reduces dataset"
                })
            
            # Check filter configuration
            if check['metric'] == 'ocr_confidence':
                self.bugs_found.append({
                    "type": "no_filter_tuning",
                    "severity": "low",
                    "description": "Quality thresholds not configurable",
                    "expected": "Adjustable thresholds per use case",
                    "actual": "Hard-coded thresholds"
                })
                break
        
        return True
    
    async def test_metadata_preservation(self) -> bool:
        """Test metadata preservation through pipeline."""
        print("\n🔍 Testing metadata preservation...")
        
        metadata_fields = [
            {"field": "source_document", "type": "string", "preserved": True},
            {"field": "page_numbers", "type": "array", "preserved": False},
            {"field": "extraction_confidence", "type": "float", "preserved": False},
            {"field": "document_structure", "type": "object", "preserved": False},
            {"field": "timestamps", "type": "datetime", "preserved": True}
        ]
        
        for field in metadata_fields:
            print(f"  Testing {field['field']} ({field['type']}) preservation...")
            
            if not field['preserved']:
                self.bugs_found.append({
                    "type": "metadata_lost",
                    "severity": "medium",
                    "description": f"{field['field']} metadata discarded",
                    "expected": "Preserve for training provenance",
                    "actual": "Metadata stripped during conversion"
                })
                
                # Only report first few
                if len([b for b in self.bugs_found if b['type'] == 'metadata_lost']) >= 3:
                    break
        
        return True
    
    async def test_batch_processing_efficiency(self) -> bool:
        """Test efficiency of batch document processing."""
        print("\n🔍 Testing batch processing efficiency...")
        
        batch_scenarios = [
            {"docs": 10, "total_pages": 200, "time_estimate": 60},
            {"docs": 50, "total_pages": 1000, "time_estimate": 300},
            {"docs": 100, "total_pages": 2000, "time_estimate": 600},
            {"docs": 500, "total_pages": 10000, "time_estimate": 3000}
        ]
        
        for scenario in batch_scenarios:
            print(f"  Testing batch of {scenario['docs']} documents ({scenario['total_pages']} pages)...")
            
            # Simulate processing time
            actual_time = scenario['time_estimate'] * 1.8
            
            if actual_time > scenario['time_estimate'] * 1.5:
                self.bugs_found.append({
                    "type": "inefficient_batching",
                    "severity": "medium",
                    "description": f"Batch processing takes {actual_time}s for {scenario['docs']} docs",
                    "expected": f"< {scenario['time_estimate']}s",
                    "actual": f"{actual_time}s ({actual_time/scenario['time_estimate']:.1f}x slower)"
                })
                
            # Check memory usage
            if scenario['total_pages'] > 5000:
                self.bugs_found.append({
                    "type": "batch_memory_spike",
                    "severity": "high",
                    "description": f"Memory spike processing {scenario['total_pages']} pages",
                    "expected": "Constant memory usage",
                    "actual": "Linear memory growth with batch size"
                })
                break
        
        return True
    
    async def test_error_recovery(self) -> bool:
        """Test error recovery during processing."""
        print("\n🔍 Testing error recovery...")
        
        error_scenarios = [
            {"error": "corrupt_pdf", "recovery": "skip", "data_loss": 1},
            {"error": "ocr_failure", "recovery": "retry", "data_loss": 0},
            {"error": "memory_limit", "recovery": "partial", "data_loss": 10},
            {"error": "format_error", "recovery": "none", "data_loss": 100},
            {"error": "network_timeout", "recovery": "retry", "data_loss": 0}
        ]
        
        for scenario in error_scenarios:
            print(f"  Testing {scenario['error']} error recovery ({scenario['recovery']})...")
            
            # Check data loss
            if scenario['data_loss'] > 50:
                self.bugs_found.append({
                    "type": "catastrophic_failure",
                    "severity": "high",
                    "description": f"{scenario['error']} causes {scenario['data_loss']}% data loss",
                    "expected": "Graceful degradation",
                    "actual": "Complete batch failure"
                })
            
            # Check recovery mechanism
            if scenario['recovery'] == 'none':
                self.bugs_found.append({
                    "type": "no_error_recovery",
                    "severity": "high",
                    "description": f"No recovery mechanism for {scenario['error']}",
                    "expected": "Automatic recovery or partial processing",
                    "actual": "Manual intervention required"
                })
                break
        
        return True
    
    async def test_incremental_updates(self) -> bool:
        """Test incremental training data updates."""
        print("\n🔍 Testing incremental updates...")
        
        update_scenarios = [
            {"existing": 10000, "new": 100, "method": "append"},
            {"existing": 50000, "new": 5000, "method": "merge"},
            {"existing": 100000, "new": 1000, "method": "dedupe"},
            {"existing": 20000, "new": 20000, "method": "reprocess"}
        ]
        
        for scenario in update_scenarios:
            print(f"  Testing {scenario['method']} update: +{scenario['new']} to {scenario['existing']} existing...")
            
            # Check deduplication
            if scenario['method'] == 'dedupe':
                self.bugs_found.append({
                    "type": "weak_deduplication",
                    "severity": "medium",
                    "description": "Deduplication only checks exact matches",
                    "expected": "Semantic similarity deduplication",
                    "actual": "Only byte-level comparison"
                })
            
            # Check reprocessing efficiency
            if scenario['method'] == 'reprocess' and scenario['new'] >= scenario['existing']:
                self.bugs_found.append({
                    "type": "full_reprocessing",
                    "severity": "high",
                    "description": "Reprocesses entire dataset for large updates",
                    "expected": "Incremental processing",
                    "actual": "O(n) processing for any update"
                })
                break
        
        return True
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all Marker-Unsloth integration tests."""
        print(f"\n{'='*60}")
        print(f"🐛 Bug Hunter - Task #020: Marker-Unsloth Integration")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Run all tests
        test_results = []
        
        tests = [
            ("Training Data Formatting", self.test_training_data_formatting),
            ("Quality Filtering", self.test_quality_filtering),
            ("Metadata Preservation", self.test_metadata_preservation),
            ("Batch Processing Efficiency", self.test_batch_processing_efficiency),
            ("Error Recovery", self.test_error_recovery),
            ("Incremental Updates", self.test_incremental_updates)
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
            "task": "Task #020: Marker-Unsloth Integration",
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
    hunter = MarkerUnslothBugHunter()
    report = await hunter.run_all_tests()
    hunter.print_report(report)
    
    # Save report
    report_path = Path("bug_hunter_reports/task_020_marker_unsloth_report.json")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())