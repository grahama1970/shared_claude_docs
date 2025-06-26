"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_module_interaction_patterns.py
Description: Test various Granger module interaction patterns to find weaknesses

This test explores:
- Data format inconsistencies between modules
- Error propagation issues
- Module coupling problems
- Interface contract violations

External Dependencies:
- Available Granger modules

Example Usage:
>>> python test_module_interaction_patterns.py
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

# Import what we can test
from arxiv_handlers.real_arxiv_handlers import (
    ArxivSearchHandler,
    ArxivEvidenceHandler,
    ArxivCitationHandler
)


class ModuleInteractionPatternTester:
    """Test interaction patterns to find design weaknesses"""
    
    def __init__(self):
        self.arxiv_search = ArxivSearchHandler()
        self.arxiv_evidence = ArxivEvidenceHandler()
        self.arxiv_citation = ArxivCitationHandler()
        self.weaknesses = []
    
    def test_data_transformation_overhead(self):
        """Weakness 1: Excessive data transformations between modules"""
        print("\n🔍 PATTERN TEST 1: Data Transformation Overhead")
        print("-" * 50)
        
        # Get paper from search
        result = self.arxiv_search.handle({
            "query": "transformer architecture",
            "max_results": 1
        })
        
        if "error" not in result and result.get("papers"):
            paper = result["papers"][0]
            original_size = len(json.dumps(paper))
            print(f"Original paper data size: {original_size} bytes")
            
            # Simulate what happens in real pipeline
            transformations = []
            
            # Transform 1: Search result → Evidence finder format
            evidence_format = {
                "paper_id": paper["id"],
                "title": paper["title"],
                "abstract": paper["summary"],
                "search_text": paper["title"] + " " + paper["summary"]
            }
            transform1_size = len(json.dumps(evidence_format))
            transformations.append(("Search→Evidence", transform1_size))
            
            # Transform 2: Evidence → Citation format
            citation_format = {
                "entry_id": paper["id"].split("/")[-1],
                "full_id": paper["id"],
                "metadata": {
                    "title": paper["title"],
                    "authors": paper["authors"]
                }
            }
            transform2_size = len(json.dumps(citation_format))
            transformations.append(("Evidence→Citation", transform2_size))
            
            # Transform 3: Citation → Storage format (simulated)
            storage_format = {
                "_key": paper["id"].replace("/", "_").replace(".", "_"),
                "type": "paper",
                "data": paper,
                "indexed_fields": {
                    "title": paper["title"],
                    "authors": ", ".join(paper["authors"][:3])
                }
            }
            transform3_size = len(json.dumps(storage_format))
            transformations.append(("Citation→Storage", transform3_size))
            
            print("\nData transformations:")
            total_overhead = 0
            for name, size in transformations:
                overhead = size - original_size
                total_overhead += abs(overhead)
                print(f"   {name}: {size} bytes ({overhead:+d} bytes)")
            
            if total_overhead > original_size:
                self.weaknesses.append({
                    "weakness": "Excessive data transformation",
                    "overhead": f"{total_overhead} bytes across {len(transformations)} transforms",
                    "impact": "Performance and memory waste",
                    "severity": "MEDIUM"
                })
                print(f"\n❌ Total transformation overhead: {total_overhead} bytes!")
    
    def test_error_context_loss(self):
        """Weakness 2: Error context lost between modules"""
        print("\n\n🔍 PATTERN TEST 2: Error Context Loss")
        print("-" * 50)
        
        # Trigger various errors and see what's preserved
        error_tests = [
            {
                "module": "search",
                "params": {"query": "", "max_results": 5},  # Empty query
                "expected_context": ["query", "validation", "empty"]
            },
            {
                "module": "evidence", 
                "params": {"claim": "a" * 1000, "evidence_type": "invalid_type"},
                "expected_context": ["evidence_type", "validation", "invalid"]
            },
            {
                "module": "citation",
                "params": {"paper_id": "invalid/id/format", "direction": "citing"},
                "expected_context": ["paper_id", "format", "invalid"]
            }
        ]
        
        for test in error_tests:
            print(f"\nTesting {test['module']} error handling...")
            
            if test["module"] == "search":
                result = self.arxiv_search.handle(test["params"])
            elif test["module"] == "evidence":
                result = self.arxiv_evidence.handle(test["params"])
            else:
                result = self.arxiv_citation.handle(test["params"])
            
            if "error" in result:
                error_msg = result["error"].lower()
                context_preserved = sum(1 for ctx in test["expected_context"] if ctx in error_msg)
                context_ratio = context_preserved / len(test["expected_context"])
                
                print(f"   Error: {result['error'][:50]}...")
                print(f"   Context preserved: {context_preserved}/{len(test['expected_context'])} ({context_ratio:.0%})")
                
                if context_ratio < 0.5:
                    self.weaknesses.append({
                        "weakness": "Poor error context preservation",
                        "module": test["module"],
                        "context_loss": f"Only {context_ratio:.0%} of context preserved",
                        "impact": "Difficult debugging across modules",
                        "severity": "HIGH"
                    })
                    print("   ❌ Insufficient error context!")
    
    def test_interface_assumptions(self):
        """Weakness 3: Hidden interface assumptions"""
        print("\n\n🔍 PATTERN TEST 3: Hidden Interface Assumptions")
        print("-" * 50)
        
        # Test what happens with unexpected but valid inputs
        
        # Test 1: Very specific query that might return 0 results
        print("\nTest 1: Zero result handling...")
        result = self.arxiv_search.handle({
            "query": "quantum blockchain transformer NFT metaverse",
            "max_results": 10
        })
        
        if result.get("paper_count", 0) == 0:
            # What if next module expects at least 1 paper?
            print("   Got 0 papers - testing evidence handler with empty input...")
            
            # Try to find evidence for non-existent papers
            evidence_result = self.arxiv_evidence.handle({
                "claim": "based on the papers",  # Assumes papers exist
                "evidence_type": "supporting"
            })
            
            if "error" not in evidence_result and evidence_result.get("evidence_count") > 0:
                self.weaknesses.append({
                    "weakness": "Module assumes previous results exist",
                    "scenario": "Evidence search without prior papers",
                    "impact": "False positive results",
                    "severity": "HIGH"
                })
                print("   ❌ Evidence handler returned results without papers!")
        
        # Test 2: Module expects specific data format
        print("\nTest 2: Data format assumptions...")
        
        # Citation handler might expect specific ID format
        test_ids = [
            "2301.12345",      # Standard format
            "cs/0301012",      # Old format
            "math.GT/0301012", # With category
            "2301.12345v3",    # With version
            "http://arxiv.org/abs/2301.12345"  # Full URL
        ]
        
        format_support = {}
        for test_id in test_ids:
            try:
                result = self.arxiv_citation.handle({
                    "paper_id": test_id,
                    "direction": "citing",
                    "max_results": 1
                })
                format_support[test_id] = "error" not in result
            except Exception as e:
                format_support[test_id] = False
        
        supported = sum(format_support.values())
        print(f"   ID format support: {supported}/{len(test_ids)}")
        
        if supported < len(test_ids):
            self.weaknesses.append({
                "weakness": "Inconsistent ID format handling",
                "supported_formats": supported,
                "total_formats": len(test_ids),
                "impact": "Integration failures with different sources",
                "severity": "MEDIUM"
            })
            print("   ❌ Not all ID formats supported!")
    
    def test_module_coupling(self):
        """Weakness 4: Tight coupling between modules"""
        print("\n\n🔍 PATTERN TEST 4: Module Coupling")
        print("-" * 50)
        
        # Test if modules can work independently
        print("Testing module independence...")
        
        # Can evidence handler work without prior search?
        print("\n1. Evidence handler standalone:")
        try:
            result = self.arxiv_evidence.handle({
                "claim": "deep learning improves accuracy",
                "evidence_type": "supporting",
                "max_results": 2
            })
            
            if "error" not in result:
                print("   ✅ Can work independently")
            else:
                print(f"   ❌ Error: {result['error'][:50]}")
        except Exception as e:
            self.weaknesses.append({
                "weakness": "Module cannot work standalone",
                "module": "evidence",
                "error": str(e)[:50],
                "impact": "Tight coupling limits reusability",
                "severity": "MEDIUM"
            })
            print(f"   ❌ Exception: {str(e)[:50]}")
        
        # Can citation handler work with just an ID?
        print("\n2. Citation handler standalone:")
        try:
            result = self.arxiv_citation.handle({
                "paper_id": "2301.12345",
                "direction": "cited_by",
                "max_results": 2
            })
            
            if "error" not in result:
                print("   ✅ Can work independently")
            else:
                print(f"   ❌ Error: {result['error'][:50]}")
        except Exception as e:
            self.weaknesses.append({
                "weakness": "Module cannot work standalone",
                "module": "citation",
                "error": str(e)[:50],
                "impact": "Tight coupling limits reusability",
                "severity": "MEDIUM"
            })
            print(f"   ❌ Exception: {str(e)[:50]}")
    
    def test_state_management(self):
        """Weakness 5: State management between calls"""
        print("\n\n🔍 PATTERN TEST 5: State Management")
        print("-" * 50)
        
        # Test if modules maintain state between calls
        print("Testing for hidden state...")
        
        # Make same call multiple times
        results = []
        for i in range(3):
            result = self.arxiv_search.handle({
                "query": "machine learning",
                "max_results": 1
            })
            if "error" not in result and result.get("papers"):
                paper_id = result["papers"][0]["id"]
                results.append(paper_id)
                print(f"   Call {i+1}: {paper_id}")
        
        # Check if results are consistent
        if len(set(results)) != 1 and len(results) == 3:
            self.weaknesses.append({
                "weakness": "Inconsistent results between calls",
                "variation": f"{len(set(results))} different results in {len(results)} calls",
                "impact": "Non-deterministic behavior",
                "severity": "HIGH"
            })
            print("   ❌ Results vary between calls!")
        
        # Test if modules share state (they shouldn't)
        print("\nTesting for shared state...")
        
        # Create multiple handler instances
        handler1 = ArxivSearchHandler()
        handler2 = ArxivSearchHandler()
        
        # Modify one (if possible)
        handler1.client = None  # Try to break it
        
        # Test if other still works
        try:
            result = handler2.handle({
                "query": "test",
                "max_results": 1
            })
            
            if "error" in result and "client" in result["error"].lower():
                self.weaknesses.append({
                    "weakness": "Shared state between instances",
                    "impact": "One instance can break others",
                    "severity": "CRITICAL"
                })
                print("   ❌ Instances share state!")
            else:
                print("   ✅ Instances are isolated")
        except Exception as e:
            print(f"   Test inconclusive: {str(e)[:50]}")
    
    def generate_weakness_report(self):
        """Generate module interaction weakness report"""
        print("\n\n" + "="*60)
        print("🔍 MODULE INTERACTION WEAKNESS REPORT")
        print("="*60)
        
        if not self.weaknesses:
            print("✅ No significant weaknesses found!")
            return
        
        print(f"\nFound {len(self.weaknesses)} design weaknesses:\n")
        
        # Group by severity
        critical = [w for w in self.weaknesses if w.get("severity") == "CRITICAL"]
        high = [w for w in self.weaknesses if w.get("severity") == "HIGH"]
        medium = [w for w in self.weaknesses if w.get("severity") == "MEDIUM"]
        
        if critical:
            print(f"🔴 CRITICAL ({len(critical)} weaknesses):")
            for weakness in critical:
                print(f"   - {weakness['weakness']}")
                print(f"     Impact: {weakness['impact']}")
                print()
        
        if high:
            print(f"🟠 HIGH ({len(high)} weaknesses):")
            for weakness in high:
                print(f"   - {weakness['weakness']}")
                print(f"     Impact: {weakness['impact']}")
                print()
        
        if medium:
            print(f"🟡 MEDIUM ({len(medium)} weaknesses):")
            for weakness in medium:
                print(f"   - {weakness['weakness']}")
                print(f"     Impact: {weakness['impact']}")
                print()
        
        # Save report
        report_path = Path("module_interaction_weaknesses.json")
        report_path.write_text(json.dumps(self.weaknesses, indent=2))
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        print("\n🏗️ ARCHITECTURAL RECOMMENDATIONS:")
        print("1. Standardize data formats across all modules")
        print("2. Preserve full error context through pipeline")
        print("3. Document and validate interface contracts")
        print("4. Ensure modules can work independently")
        print("5. Eliminate shared state between instances")
        print("6. Add integration tests for all module pairs")


if __name__ == "__main__":
    print("🔍 Starting Granger Module Interaction Pattern Analysis...")
    print("This will test design patterns and find weaknesses!\n")
    
    tester = ModuleInteractionPatternTester()
    
    # Run all pattern tests
    tester.test_data_transformation_overhead()
    tester.test_error_context_loss()
    tester.test_interface_assumptions()
    tester.test_module_coupling()
    tester.test_state_management()
    
    # Generate report
    tester.generate_weakness_report()
    
    print("\n✅ Pattern analysis complete!")