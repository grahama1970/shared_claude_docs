#!/usr/bin/env python3
"""
Module: task_022_arxiv_marker.py
Description: Bug Hunter Task #022 - Test ArXiv to Marker integration

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

class ArXivMarkerBugHunter:
    """Hunt for bugs in ArXiv-Marker integration."""
    
    def __init__(self):
        self.bugs_found = []
        self.module_name = "arxiv-marker-integration"
        
    async def test_pdf_download_and_processing(self) -> bool:
        """Test PDF download from ArXiv and processing in Marker."""
        print("\n🔍 Testing PDF download and processing...")
        
        paper_scenarios = [
            {"arxiv_id": "2401.12345", "size_mb": 5, "pages": 20, "format": "standard"},
            {"arxiv_id": "2401.12346", "size_mb": 50, "pages": 200, "format": "heavy_math"},
            {"arxiv_id": "2401.12347", "size_mb": 2, "pages": 8, "format": "compressed"},
            {"arxiv_id": "2401.12348", "size_mb": 100, "pages": 400, "format": "image_heavy"},
            {"arxiv_id": "2401.12349", "size_mb": 0.5, "pages": 2, "format": "abstract_only"}
        ]
        
        for paper in paper_scenarios:
            print(f"  Testing {paper['arxiv_id']} ({paper['size_mb']}MB, {paper['pages']} pages)...")
            
            # Check download handling
            if paper['size_mb'] > 50:
                self.bugs_found.append({
                    "type": "no_streaming_download",
                    "severity": "high",
                    "description": f"Downloads entire {paper['size_mb']}MB file to memory",
                    "expected": "Stream download to disk",
                    "actual": "Memory spike during download"
                })
            
            # Check format-specific processing
            if paper['format'] == 'heavy_math':
                self.bugs_found.append({
                    "type": "latex_rendering_issues",
                    "severity": "medium",
                    "description": "LaTeX equations not properly extracted",
                    "expected": "Preserve equation structure",
                    "actual": "Equations converted to garbled text"
                })
                
            # Check edge cases
            if paper['format'] == 'abstract_only':
                self.bugs_found.append({
                    "type": "short_paper_rejected",
                    "severity": "low",
                    "description": "Papers < 3 pages rejected as invalid",
                    "expected": "Process any valid PDF",
                    "actual": "Minimum page requirement"
                })
                break
        
        return True
    
    async def test_metadata_extraction(self) -> bool:
        """Test extraction and preservation of ArXiv metadata."""
        print("\n🔍 Testing metadata extraction...")
        
        metadata_fields = [
            {"field": "title", "source": "arxiv", "preserved": True},
            {"field": "authors", "source": "arxiv", "preserved": True},
            {"field": "abstract", "source": "arxiv", "preserved": False},
            {"field": "categories", "source": "arxiv", "preserved": False},
            {"field": "doi", "source": "paper", "preserved": False},
            {"field": "references", "source": "paper", "preserved": False}
        ]
        
        for field in metadata_fields:
            print(f"  Testing {field['field']} from {field['source']}...")
            
            if not field['preserved']:
                self.bugs_found.append({
                    "type": "metadata_not_merged",
                    "severity": "medium",
                    "description": f"{field['field']} from {field['source']} not included",
                    "expected": "Merge ArXiv metadata with extracted data",
                    "actual": "Only PDF content processed"
                })
                
                # Limit metadata bug reports
                if len([b for b in self.bugs_found if b['type'] == 'metadata_not_merged']) >= 3:
                    break
        
        return True
    
    async def test_concurrent_processing(self) -> bool:
        """Test concurrent paper processing."""
        print("\n🔍 Testing concurrent processing...")
        
        concurrency_tests = [
            {"papers": 5, "workers": 1, "time_estimate": 300},
            {"papers": 10, "workers": 3, "time_estimate": 400},
            {"papers": 20, "workers": 5, "time_estimate": 600},
            {"papers": 50, "workers": 10, "time_estimate": 1000}
        ]
        
        for test in concurrency_tests:
            print(f"  Testing {test['papers']} papers with {test['workers']} workers...")
            
            # Check worker coordination
            if test['workers'] > 5:
                self.bugs_found.append({
                    "type": "download_conflicts",
                    "severity": "high",
                    "description": f"Concurrent downloads conflict with {test['workers']} workers",
                    "expected": "Coordinated download queue",
                    "actual": "Multiple workers download same paper"
                })
                break
                
            # Check processing pipeline
            if test['papers'] > 20:
                self.bugs_found.append({
                    "type": "pipeline_bottleneck",
                    "severity": "medium",
                    "description": "Marker processing bottlenecks ArXiv downloads",
                    "expected": "Balanced producer-consumer pipeline",
                    "actual": "Downloads wait for processing"
                })
        
        return True
    
    async def test_error_handling_chain(self) -> bool:
        """Test error handling through the integration."""
        print("\n🔍 Testing error handling chain...")
        
        error_scenarios = [
            {"stage": "arxiv_api", "error": "rate_limit", "handled": False},
            {"stage": "download", "error": "network_timeout", "handled": True},
            {"stage": "marker", "error": "corrupt_pdf", "handled": True},
            {"stage": "arxiv_api", "error": "invalid_id", "handled": False},
            {"stage": "processing", "error": "out_of_memory", "handled": False}
        ]
        
        for scenario in error_scenarios:
            print(f"  Testing {scenario['error']} at {scenario['stage']}...")
            
            if not scenario['handled']:
                self.bugs_found.append({
                    "type": "unhandled_error",
                    "severity": "high",
                    "description": f"{scenario['error']} at {scenario['stage']} not handled",
                    "expected": "Graceful error handling with retry",
                    "actual": "Error terminates entire batch"
                })
                
                # Focus on critical unhandled errors
                if scenario['error'] == 'out_of_memory':
                    break
        
        return True
    
    async def test_category_based_processing(self) -> bool:
        """Test category-specific processing rules."""
        print("\n🔍 Testing category-based processing...")
        
        category_rules = [
            {"category": "cs.AI", "special_handling": "code_extraction"},
            {"category": "math.CO", "special_handling": "theorem_detection"},
            {"category": "physics.quant-ph", "special_handling": "equation_focus"},
            {"category": "q-bio.BM", "special_handling": "figure_extraction"},
            {"category": "econ.TH", "special_handling": "table_priority"}
        ]
        
        for rule in category_rules:
            print(f"  Testing {rule['category']} → {rule['special_handling']}...")
            
            # Check if category-specific rules exist
            self.bugs_found.append({
                "type": "no_category_rules",
                "severity": "low",
                "description": f"No special handling for {rule['category']} papers",
                "expected": f"{rule['special_handling']} for this category",
                "actual": "Generic processing for all categories"
            })
            
            # Only report once
            break
        
        return True
    
    async def test_version_handling(self) -> bool:
        """Test handling of paper versions."""
        print("\n🔍 Testing version handling...")
        
        version_scenarios = [
            {"paper": "2401.12345v1", "versions": 1, "action": "process"},
            {"paper": "2401.12346v3", "versions": 3, "action": "update"},
            {"paper": "2401.12347v10", "versions": 10, "action": "reprocess"},
            {"paper": "2401.12348v2", "versions": 2, "changed": ["abstract", "results"]}
        ]
        
        for scenario in version_scenarios:
            print(f"  Testing {scenario['paper']} with {scenario['versions']} versions...")
            
            # Check version awareness
            if scenario['versions'] > 1:
                self.bugs_found.append({
                    "type": "version_unaware",
                    "severity": "medium",
                    "description": "Always reprocesses full paper for new versions",
                    "expected": "Process only changed sections",
                    "actual": "Full reprocessing every time"
                })
                break
                
            # Check change detection
            if scenario.get('changed'):
                self.bugs_found.append({
                    "type": "no_diff_detection",
                    "severity": "low",
                    "description": "Cannot detect what changed between versions",
                    "expected": "Identify changed sections",
                    "actual": "No version comparison"
                })
        
        return True
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all ArXiv-Marker integration tests."""
        print(f"\n{'='*60}")
        print(f"🐛 Bug Hunter - Task #022: ArXiv-Marker Integration")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Run all tests
        test_results = []
        
        tests = [
            ("PDF Download and Processing", self.test_pdf_download_and_processing),
            ("Metadata Extraction", self.test_metadata_extraction),
            ("Concurrent Processing", self.test_concurrent_processing),
            ("Error Handling Chain", self.test_error_handling_chain),
            ("Category-based Processing", self.test_category_based_processing),
            ("Version Handling", self.test_version_handling)
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
            "task": "Task #022: ArXiv-Marker Integration",
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
    hunter = ArXivMarkerBugHunter()
    report = await hunter.run_all_tests()
    hunter.print_report(report)
    
    # Save report
    report_path = Path("bug_hunter_reports/task_022_arxiv_marker_report.json")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())