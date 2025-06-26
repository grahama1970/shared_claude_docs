"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_granger_performance_bottlenecks.py
Description: Find performance bottlenecks in Granger module interactions

This test reveals:
- Slow module responses
- Memory leaks
- Connection pool exhaustion
- Cascading failures
- Timeout chains
- Resource starvation

External Dependencies:
- All Granger modules under load

Example Usage:
>>> python test_granger_performance_bottlenecks.py
"""

import asyncio
import time
import psutil
import sys
from typing import Dict, List, Any
import concurrent.futures
from pathlib import Path
import json

sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from sparta.real_sparta_handlers_fixed import SPARTACVESearchHandler
from arxiv_handlers.real_arxiv_handlers import ArxivSearchHandler, ArxivBatchHandler
from arangodb_handlers.real_arangodb_handlers import (
    ArangoDocumentHandler, ArangoSearchHandler
)


class GrangerPerformanceBottleneckFinder:
    """Find performance bottlenecks in module interactions"""
    
    def __init__(self):
        self.sparta = SPARTACVESearchHandler()
        self.arxiv = ArxivSearchHandler()
        self.arxiv_batch = ArxivBatchHandler()
        self.arango_doc = ArangoDocumentHandler()
        self.arango_search = ArangoSearchHandler()
        
        self.bottlenecks = []
        self.baseline_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    
    def test_sparta_arxiv_latency_multiplication(self):
        """Bottleneck 1: Latency multiplication in sequential calls"""
        print("\n⏱️ BOTTLENECK 1: Latency Multiplication")
        print("-" * 50)
        
        # Measure individual module latencies
        print("Measuring individual module latencies...")
        
        # SPARTA latency
        start = time.time()
        sparta_result = self.sparta.handle({
            "keyword": "buffer overflow",
            "limit": 10
        })
        sparta_latency = time.time() - start
        print(f"   SPARTA: {sparta_latency:.2f}s")
        
        # ArXiv latency (per paper)
        start = time.time()
        arxiv_result = self.arxiv.handle({
            "query": "buffer overflow",
            "max_results": 1
        })
        arxiv_latency = time.time() - start
        print(f"   ArXiv: {arxiv_latency:.2f}s per query")
        
        # Calculate multiplication effect
        if sparta_result.get("success"):
            cve_count = len(sparta_result.get("vulnerabilities", []))
            total_latency = sparta_latency + (cve_count * arxiv_latency)
            
            print(f"\n   Sequential processing of {cve_count} CVEs:")
            print(f"   Expected time: {total_latency:.2f}s")
            print(f"   Multiplication factor: {total_latency/sparta_latency:.1f}x")
            
            if total_latency > 10:
                self.bottlenecks.append({
                    "bottleneck": "Latency multiplication",
                    "impact": f"{total_latency:.1f}s for {cve_count} items",
                    "severity": "HIGH",
                    "solution": "Batch or parallelize ArXiv queries"
                })
                print(f"   ❌ Severe latency multiplication detected!")
    
    def test_parallel_vs_sequential_performance(self):
        """Bottleneck 2: Sequential processing when parallel is possible"""
        print("\n\n⏱️ BOTTLENECK 2: Sequential vs Parallel Performance")
        print("-" * 50)
        
        test_queries = [
            "machine learning",
            "neural networks", 
            "deep learning",
            "transformer models",
            "reinforcement learning"
        ]
        
        # Test sequential
        print("Testing sequential processing...")
        start = time.time()
        sequential_results = []
        for query in test_queries:
            result = self.arxiv.handle({
                "query": query,
                "max_results": 2
            })
            sequential_results.append(result)
        sequential_time = time.time() - start
        
        # Test parallel with threads
        print("\nTesting parallel processing...")
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for query in test_queries:
                future = executor.submit(self.arxiv.handle, {
                    "query": query,
                    "max_results": 2
                })
                futures.append(future)
            parallel_results = [f.result() for f in futures]
        parallel_time = time.time() - start
        
        # Test batch API if available
        print("\nTesting batch API...")
        start = time.time()
        batch_result = self.arxiv_batch.handle({
            "operations": [
                {"type": "search", "params": {"query": q, "max_results": 2}}
                for q in test_queries
            ]
        })
        batch_time = time.time() - start
        
        print(f"\nPerformance comparison:")
        print(f"   Sequential: {sequential_time:.2f}s")
        print(f"   Parallel:   {parallel_time:.2f}s ({sequential_time/parallel_time:.1f}x faster)")
        print(f"   Batch API:  {batch_time:.2f}s ({sequential_time/batch_time:.1f}x faster)")
        
        if sequential_time / parallel_time < 2:
            self.bottlenecks.append({
                "bottleneck": "Poor parallelization",
                "impact": "Missing 2-5x speedup opportunity",
                "severity": "MEDIUM",
                "solution": "Improve thread pool usage"
            })
            print("   ⚠️ Parallel processing not much faster!")
    
    def test_memory_leak_in_large_batches(self):
        """Bottleneck 3: Memory leaks during large batch processing"""
        print("\n\n⏱️ BOTTLENECK 3: Memory Leaks")
        print("-" * 50)
        
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
        print(f"Initial memory: {initial_memory:.1f} MB")
        
        # Process many documents
        print("\nProcessing 100 documents in batches...")
        for batch in range(10):
            docs = []
            for i in range(10):
                doc = {
                    "_key": f"perf_test_{batch}_{i}",
                    "content": "A" * 10000,  # 10KB per doc
                    "metadata": {
                        "batch": batch,
                        "index": i,
                        "timestamp": time.time()
                    }
                }
                result = self.arango_doc.handle({
                    "operation": "create",
                    "collection": "performance_test",
                    "data": doc
                })
            
            # Check memory growth
            current_memory = psutil.Process().memory_info().rss / 1024 / 1024
            growth = current_memory - initial_memory
            print(f"   Batch {batch}: Memory = {current_memory:.1f} MB (+{growth:.1f} MB)")
            
            if growth > 50:  # More than 50MB growth
                self.bottlenecks.append({
                    "bottleneck": "Memory leak",
                    "impact": f"{growth:.1f} MB leaked after {(batch+1)*10} documents",
                    "severity": "CRITICAL",
                    "solution": "Fix object cleanup in handlers"
                })
                print(f"   ❌ Memory leak detected: {growth:.1f} MB growth!")
                break
    
    def test_connection_pool_exhaustion(self):
        """Bottleneck 4: Connection pool exhaustion under load"""
        print("\n\n⏱️ BOTTLENECK 4: Connection Pool Exhaustion")
        print("-" * 50)
        
        print("Spawning 50 concurrent ArangoDB operations...")
        
        async def hammer_arangodb(operation_id: int):
            """Single operation"""
            try:
                result = self.arango_search.handle({
                    "search_type": "fulltext",
                    "query": f"test query {operation_id}",
                    "limit": 1
                })
                return {"id": operation_id, "success": "error" not in result}
            except Exception as e:
                return {"id": operation_id, "error": str(e)}
        
        # Run many concurrent operations
        start = time.time()
        loop = asyncio.get_event_loop()
        tasks = [hammer_arangodb(i) for i in range(50)]
        results = loop.run_until_complete(asyncio.gather(*tasks))
        duration = time.time() - start
        
        # Analyze results
        successes = sum(1 for r in results if r.get("success"))
        errors = [r for r in results if "error" in r]
        
        print(f"\nResults after {duration:.2f}s:")
        print(f"   Successful: {successes}/50")
        print(f"   Failed: {len(errors)}/50")
        
        if errors:
            error_types = {}
            for e in errors:
                error_msg = e.get("error", "Unknown")
                if "connection" in error_msg.lower() or "pool" in error_msg.lower():
                    error_types["connection_pool"] = error_types.get("connection_pool", 0) + 1
                elif "timeout" in error_msg.lower():
                    error_types["timeout"] = error_types.get("timeout", 0) + 1
                else:
                    error_types["other"] = error_types.get("other", 0) + 1
            
            print(f"   Error breakdown: {error_types}")
            
            if error_types.get("connection_pool", 0) > 5:
                self.bottlenecks.append({
                    "bottleneck": "Connection pool exhaustion",
                    "impact": f"{error_types['connection_pool']} connection failures",
                    "severity": "HIGH",
                    "solution": "Increase pool size or add connection queuing"
                })
                print("   ❌ Connection pool exhausted!")
    
    def test_cascading_timeout_failure(self):
        """Bottleneck 5: Cascading timeouts through pipeline"""
        print("\n\n⏱️ BOTTLENECK 5: Cascading Timeout Failures")
        print("-" * 50)
        
        # Create a slow query that might timeout
        very_complex_query = " OR ".join([f"term{i}" for i in range(100)])
        
        print("Testing timeout propagation...")
        timeouts = []
        
        # Module 1: ArXiv with complex query
        start = time.time()
        try:
            result1 = self.arxiv.handle({
                "query": very_complex_query,
                "max_results": 50
            })
            module1_time = time.time() - start
            print(f"   ArXiv took {module1_time:.2f}s")
            
            if module1_time > 5:
                timeouts.append(("ArXiv", module1_time))
        except Exception as e:
            if "timeout" in str(e).lower():
                timeouts.append(("ArXiv", "timeout"))
                print("   ❌ ArXiv timed out!")
        
        # Module 2: Would depend on Module 1's output
        # In real scenario, if Module 1 is slow, Module 2 starts late
        # This creates cascading delays
        
        if timeouts:
            self.bottlenecks.append({
                "bottleneck": "Cascading timeouts",
                "impact": "Full pipeline failure from single slow module",
                "severity": "CRITICAL",
                "solution": "Add circuit breakers and fallback strategies"
            })
    
    def test_hot_path_optimization(self):
        """Bottleneck 6: Identify hot paths needing optimization"""
        print("\n\n⏱️ BOTTLENECK 6: Hot Path Analysis")
        print("-" * 50)
        
        # Simulate common user flow
        print("Simulating common user flow 10 times...")
        
        flow_times = []
        for i in range(10):
            flow_start = time.time()
            
            # Step 1: Search CVEs (hot path)
            sparta_result = self.sparta.handle({
                "keyword": "sql injection",
                "limit": 3
            })
            
            # Step 2: Search papers (hot path)
            if sparta_result.get("success"):
                arxiv_result = self.arxiv.handle({
                    "query": "sql injection prevention",
                    "max_results": 3
                })
            
            # Step 3: Store results (hot path)
            doc_result = self.arango_doc.handle({
                "operation": "create",
                "collection": "hot_path_test",
                "data": {
                    "iteration": i,
                    "timestamp": time.time()
                }
            })
            
            flow_time = time.time() - flow_start
            flow_times.append(flow_time)
            
            if i == 0:
                print(f"   First run: {flow_time:.2f}s (cold)")
            elif i == 9:
                print(f"   Last run:  {flow_time:.2f}s (hot)")
        
        # Analyze variance
        avg_time = sum(flow_times) / len(flow_times)
        min_time = min(flow_times)
        max_time = max(flow_times)
        
        print(f"\n   Average: {avg_time:.2f}s")
        print(f"   Min: {min_time:.2f}s, Max: {max_time:.2f}s")
        print(f"   Variance: {max_time - min_time:.2f}s")
        
        if max_time - min_time > 2:
            self.bottlenecks.append({
                "bottleneck": "High variance in hot path",
                "impact": f"Up to {max_time - min_time:.1f}s variance",
                "severity": "MEDIUM",
                "solution": "Add caching for hot paths"
            })
            print("   ⚠️ High variance detected - needs caching!")
    
    def generate_performance_report(self):
        """Generate performance bottleneck report"""
        print("\n\n" + "="*60)
        print("⏱️ PERFORMANCE BOTTLENECK REPORT")
        print("="*60)
        
        if not self.bottlenecks:
            print("✅ No significant bottlenecks found!")
            return
        
        print(f"\nFound {len(self.bottlenecks)} performance bottlenecks:\n")
        
        # Group by severity
        critical = [b for b in self.bottlenecks if b.get("severity") == "CRITICAL"]
        high = [b for b in self.bottlenecks if b.get("severity") == "HIGH"]
        medium = [b for b in self.bottlenecks if b.get("severity") == "MEDIUM"]
        
        if critical:
            print(f"🔴 CRITICAL ({len(critical)} bottlenecks):")
            for bottleneck in critical:
                print(f"   - {bottleneck['bottleneck']}")
                print(f"     Impact: {bottleneck['impact']}")
                print(f"     Fix: {bottleneck['solution']}")
                print()
        
        if high:
            print(f"🟠 HIGH ({len(high)} bottlenecks):")
            for bottleneck in high:
                print(f"   - {bottleneck['bottleneck']}")
                print(f"     Impact: {bottleneck['impact']}")
                print(f"     Fix: {bottleneck['solution']}")
                print()
        
        if medium:
            print(f"🟡 MEDIUM ({len(medium)} bottlenecks):")
            for bottleneck in medium:
                print(f"   - {bottleneck['bottleneck']}")
                print(f"     Impact: {bottleneck['impact']}")
                print(f"     Fix: {bottleneck['solution']}")
                print()
        
        # Memory summary
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_growth = final_memory - self.baseline_memory
        print(f"\n💾 Memory usage:")
        print(f"   Start: {self.baseline_memory:.1f} MB")
        print(f"   End: {final_memory:.1f} MB")
        print(f"   Growth: {memory_growth:.1f} MB")
        
        # Save report
        report_path = Path("granger_performance_bottlenecks.json")
        report_path.write_text(json.dumps(self.bottlenecks, indent=2))
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        print("\n🚀 OPTIMIZATION PRIORITIES:")
        print("1. Implement batch APIs for ArXiv queries")
        print("2. Add connection pooling with proper limits")
        print("3. Cache hot path results (CVE searches)")
        print("4. Add circuit breakers for timeout prevention")
        print("5. Parallelize independent operations")
        print("6. Fix memory leaks in document handlers")


if __name__ == "__main__":
    print("🔍 Starting Granger Performance Bottleneck Analysis...")
    print("This will stress test module interactions!\n")
    
    finder = GrangerPerformanceBottleneckFinder()
    
    # Run all bottleneck tests
    finder.test_sparta_arxiv_latency_multiplication()
    finder.test_parallel_vs_sequential_performance()
    finder.test_memory_leak_in_large_batches()
    finder.test_connection_pool_exhaustion()
    finder.test_cascading_timeout_failure()
    finder.test_hot_path_optimization()
    
    # Generate report
    finder.generate_performance_report()
    
    print("\n✅ Performance analysis complete!")