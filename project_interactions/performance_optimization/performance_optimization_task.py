#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
GRANGER Phase 2 Task #011: Performance Optimization

This module implements performance optimizations for the GRANGER system based on
the integration testing results from Tasks 1-10.

Key Optimizations:
1. Connection pooling for ArangoDB
2. Caching for ArXiv searches and downloads
3. Batch processing for document storage
4. Parallel execution for multi-module operations
5. Retry logic with exponential backoff

Performance Targets:
- ArXiv search: <2s (from 4.67s)
- PDF download: <1s per PDF with caching
- ArangoDB storage: <0.5s per document
- Full pipeline: <10s (from 15-30s)
"""

import os
import sys
import time
import json
import asyncio
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache, wraps
from datetime import datetime, timedelta
import pickle

# Add paths for modules
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')
sys.path.insert(0, '/home/graham/workspace/experiments')

# Import handlers
from arxiv_handlers.real_arxiv_handlers import (
    ArxivSearchHandler,
    ArxivDownloadHandler
)
from arangodb_handlers.real_arangodb_handlers import (
    ArangoDocumentHandler,
    ArangoSearchHandler
)


class PerformanceMetrics:
    """Track performance metrics for optimization"""
    
    def __init__(self):
        self.metrics = {
            "cache_hits": 0,
            "cache_misses": 0,
            "api_calls": 0,
            "api_time": 0.0,
            "db_operations": 0,
            "db_time": 0.0,
            "parallel_tasks": 0,
            "retry_count": 0
        }
        
    def record_cache_hit(self):
        self.metrics["cache_hits"] += 1
        
    def record_cache_miss(self):
        self.metrics["cache_misses"] += 1
        
    def record_api_call(self, duration: float):
        self.metrics["api_calls"] += 1
        self.metrics["api_time"] += duration
        
    def record_db_operation(self, duration: float):
        self.metrics["db_operations"] += 1
        self.metrics["db_time"] += duration
        
    def record_parallel_task(self):
        self.metrics["parallel_tasks"] += 1
        
    def record_retry(self):
        self.metrics["retry_count"] += 1
        
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        total_cache = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        cache_ratio = self.metrics["cache_hits"] / total_cache if total_cache > 0 else 0
        
        avg_api_time = self.metrics["api_time"] / self.metrics["api_calls"] if self.metrics["api_calls"] > 0 else 0
        avg_db_time = self.metrics["db_time"] / self.metrics["db_operations"] if self.metrics["db_operations"] > 0 else 0
        
        return {
            "cache_hit_ratio": f"{cache_ratio:.2%}",
            "total_api_calls": self.metrics["api_calls"],
            "avg_api_time": f"{avg_api_time:.3f}s",
            "total_db_operations": self.metrics["db_operations"],
            "avg_db_time": f"{avg_db_time:.3f}s",
            "parallel_tasks": self.metrics["parallel_tasks"],
            "retry_count": self.metrics["retry_count"]
        }


class CacheManager:
    """Manage caching for expensive operations"""
    
    def __init__(self, cache_dir: str = "/tmp/granger_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.memory_cache = {}  # In-memory cache for fast access
        self.cache_ttl = timedelta(hours=24)  # Cache time-to-live
        
    def _get_cache_key(self, operation: str, params: Dict[str, Any]) -> str:
        """Generate cache key from operation and parameters"""
        key_data = f"{operation}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
        
    def get(self, operation: str, params: Dict[str, Any]) -> Optional[Any]:
        """Get cached result if available"""
        cache_key = self._get_cache_key(operation, params)
        
        # Check memory cache first
        if cache_key in self.memory_cache:
            timestamp, data = self.memory_cache[cache_key]
            if datetime.now() - timestamp < self.cache_ttl:
                return data
                
        # Check disk cache
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    timestamp, data = pickle.load(f)
                if datetime.now() - timestamp < self.cache_ttl:
                    # Load into memory cache
                    self.memory_cache[cache_key] = (timestamp, data)
                    return data
            except:
                pass
                
        return None
        
    def set(self, operation: str, params: Dict[str, Any], data: Any):
        """Cache result"""
        cache_key = self._get_cache_key(operation, params)
        timestamp = datetime.now()
        
        # Store in memory
        self.memory_cache[cache_key] = (timestamp, data)
        
        # Store on disk
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump((timestamp, data), f)
        except:
            pass  # Ignore cache write errors
            
    def clear(self):
        """Clear all caches"""
        self.memory_cache.clear()
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()


class ConnectionPool:
    """Connection pool for ArangoDB"""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.connections = []
        self.available = []
        self.lock = asyncio.Lock()
        
    async def get_connection(self):
        """Get a connection from the pool"""
        async with self.lock:
            if self.available:
                return self.available.pop()
            elif len(self.connections) < self.max_connections:
                # Create new connection
                handler = ArangoDocumentHandler()
                if handler.connect():
                    self.connections.append(handler)
                    return handler
            else:
                # Wait for available connection
                while not self.available:
                    await asyncio.sleep(0.1)
                return self.available.pop()
                
    async def release_connection(self, handler):
        """Return connection to pool"""
        async with self.lock:
            self.available.append(handler)


def with_retry(max_retries: int = 3, backoff_factor: float = 2.0):
    """Decorator for retry logic with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            metrics = kwargs.get('metrics')
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if metrics:
                        metrics.record_retry()
                    
                    if attempt == max_retries - 1:
                        raise
                        
                    # Exponential backoff
                    wait_time = backoff_factor ** attempt
                    time.sleep(wait_time)
                    
            return None
        return wrapper
    return decorator


class OptimizedArxivHandler:
    """Optimized ArXiv handler with caching and parallelization"""
    
    def __init__(self, cache_manager: CacheManager, metrics: PerformanceMetrics):
        self.cache = cache_manager
        self.metrics = metrics
        self.search_handler = ArxivSearchHandler()
        self.download_handler = ArxivDownloadHandler()
        
    @with_retry(max_retries=3)
    def search_papers(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Search papers with caching"""
        # Check cache
        cache_params = {"query": query, "max_results": max_results}
        cached_result = self.cache.get("arxiv_search", cache_params)
        
        if cached_result:
            self.metrics.record_cache_hit()
            return cached_result
            
        self.metrics.record_cache_miss()
        
        # Make real API call
        start_time = time.time()
        result = self.search_handler.handle({
            "query": query,
            "max_results": max_results,
            "sort_by": "relevance"
        })
        duration = time.time() - start_time
        
        self.metrics.record_api_call(duration)
        
        # Cache successful results
        if "error" not in result:
            self.cache.set("arxiv_search", cache_params, result)
            
        return result
        
    def download_papers_parallel(self, paper_ids: List[str], max_workers: int = 5) -> Dict[str, Any]:
        """Download multiple papers in parallel"""
        self.metrics.record_parallel_task()
        
        results = {
            "downloaded": 0,
            "failed": 0,
            "paths": [],
            "errors": []
        }
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit download tasks
            future_to_id = {}
            for paper_id in paper_ids:
                # Check cache first
                cached_path = self.cache.get("arxiv_download", {"paper_id": paper_id})
                if cached_path and Path(cached_path).exists():
                    self.metrics.record_cache_hit()
                    results["downloaded"] += 1
                    results["paths"].append(cached_path)
                else:
                    self.metrics.record_cache_miss()
                    future = executor.submit(self._download_single, paper_id)
                    future_to_id[future] = paper_id
                    
            # Collect results
            for future in as_completed(future_to_id):
                paper_id = future_to_id[future]
                try:
                    path = future.result()
                    if path:
                        results["downloaded"] += 1
                        results["paths"].append(path)
                        # Cache successful download
                        self.cache.set("arxiv_download", {"paper_id": paper_id}, path)
                except Exception as e:
                    results["failed"] += 1
                    results["errors"].append(f"{paper_id}: {str(e)}")
                    
        return results
        
    @with_retry(max_retries=2)
    def _download_single(self, paper_id: str) -> Optional[str]:
        """Download single paper"""
        start_time = time.time()
        result = self.download_handler.handle({"paper_ids": [paper_id]})
        duration = time.time() - start_time
        
        self.metrics.record_api_call(duration)
        
        if "error" not in result and result.get("paths"):
            return result["paths"][0]
        return None


class OptimizedArangoHandler:
    """Optimized ArangoDB handler with connection pooling and batch operations"""
    
    def __init__(self, connection_pool: ConnectionPool, metrics: PerformanceMetrics):
        self.pool = connection_pool
        self.metrics = metrics
        
    async def store_documents_batch(self, documents: List[Dict[str, Any]], 
                                  collection: str = "granger_documents",
                                  batch_size: int = 100) -> Dict[str, Any]:
        """Store multiple documents in batches"""
        self.metrics.record_parallel_task()
        
        results = {
            "stored": 0,
            "failed": 0,
            "errors": []
        }
        
        # Process in batches
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            # Get connection from pool
            handler = await self.pool.get_connection()
            
            try:
                start_time = time.time()
                
                # Store batch
                for doc in batch:
                    try:
                        result = handler.handle({
                            "operation": "create",
                            "collection": collection,
                            "data": doc
                        })
                        
                        if "error" not in result:
                            results["stored"] += 1
                        else:
                            results["failed"] += 1
                            results["errors"].append(result["error"])
                    except Exception as e:
                        results["failed"] += 1
                        results["errors"].append(str(e))
                        
                duration = time.time() - start_time
                self.metrics.record_db_operation(duration)
                
            finally:
                # Return connection to pool
                await self.pool.release_connection(handler)
                
        return results
        
    async def parallel_search(self, queries: List[str], 
                            search_type: str = "hybrid",
                            max_workers: int = 5) -> Dict[str, Any]:
        """Execute multiple searches in parallel"""
        self.metrics.record_parallel_task()
        
        results = {
            "total_results": 0,
            "search_results": {},
            "errors": []
        }
        
        tasks = []
        for query in queries:
            task = self._search_single(query, search_type)
            tasks.append(task)
            
        # Execute searches in parallel
        search_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for query, result in zip(queries, search_results):
            if isinstance(result, Exception):
                results["errors"].append(f"{query}: {str(result)}")
            else:
                results["search_results"][query] = result
                results["total_results"] += result.get("result_count", 0)
                
        return results
        
    async def _search_single(self, query: str, search_type: str) -> Dict[str, Any]:
        """Execute single search"""
        handler = await self.pool.get_connection()
        
        try:
            start_time = time.time()
            
            # Create search handler
            search_handler = ArangoSearchHandler()
            search_handler.client = handler.client
            search_handler.db = handler.db
            
            result = search_handler.handle({
                "search_type": search_type,
                "query": query,
                "limit": 10
            })
            
            duration = time.time() - start_time
            self.metrics.record_db_operation(duration)
            
            return result
            
        finally:
            await self.pool.release_connection(handler)


class PerformanceOptimizer:
    """Main performance optimization orchestrator"""
    
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.cache = CacheManager()
        self.connection_pool = ConnectionPool(max_connections=10)
        self.arxiv_handler = OptimizedArxivHandler(self.cache, self.metrics)
        self.arango_handler = OptimizedArangoHandler(self.connection_pool, self.metrics)
        
    async def run_optimized_pipeline(self, query: str = "machine learning security") -> Dict[str, Any]:
        """Run optimized GRANGER pipeline"""
        print(f"\n{'='*80}")
        print("GRANGER Performance Optimization Test")
        print(f"Query: '{query}'")
        print(f"{'='*80}\n")
        
        pipeline_start = time.time()
        results = {
            "papers_found": 0,
            "papers_downloaded": 0,
            "documents_stored": 0,
            "search_results": 0,
            "total_duration": 0,
            "optimization_gains": {}
        }
        
        # Phase 1: Optimized ArXiv Search (with caching)
        print("📚 Phase 1: Optimized ArXiv Search")
        search_start = time.time()
        
        search_result = self.arxiv_handler.search_papers(query, max_results=10)
        
        search_duration = time.time() - search_start
        
        if "error" not in search_result:
            papers = search_result.get("papers", [])
            results["papers_found"] = len(papers)
            print(f"✅ Found {len(papers)} papers in {search_duration:.2f}s")
            
            # Phase 2: Parallel PDF Downloads
            if papers:
                print("\n📥 Phase 2: Parallel PDF Downloads")
                download_start = time.time()
                
                paper_ids = [p["pdf_url"].split("/")[-1].replace(".pdf", "") 
                           for p in papers[:5]]  # Limit to 5
                
                download_result = self.arxiv_handler.download_papers_parallel(paper_ids)
                
                download_duration = time.time() - download_start
                results["papers_downloaded"] = download_result["downloaded"]
                
                print(f"✅ Downloaded {download_result['downloaded']} PDFs in {download_duration:.2f}s")
                
                # Phase 3: Batch Document Storage
                if download_result["downloaded"] > 0:
                    print("\n💾 Phase 3: Batch Document Storage")
                    storage_start = time.time()
                    
                    # Prepare documents for batch storage
                    documents = []
                    for i, paper in enumerate(papers[:download_result["downloaded"]]):
                        doc = {
                            "type": "research_paper",
                            "arxiv_id": paper.get("id", ""),
                            "title": paper.get("title", ""),
                            "authors": paper.get("authors", []),
                            "abstract": paper.get("summary", ""),
                            "optimized": True,
                            "timestamp": datetime.now().isoformat()
                        }
                        documents.append(doc)
                        
                    # Store in batches
                    storage_result = await self.arango_handler.store_documents_batch(documents)
                    
                    storage_duration = time.time() - storage_start
                    results["documents_stored"] = storage_result["stored"]
                    
                    print(f"✅ Stored {storage_result['stored']} documents in {storage_duration:.2f}s")
                    
                    # Phase 4: Parallel Search Validation
                    print("\n🔍 Phase 4: Parallel Search Validation")
                    search_val_start = time.time()
                    
                    # Search for stored documents
                    search_queries = [
                        query,
                        papers[0]["title"][:50] if papers else "",
                        "optimized research paper"
                    ]
                    
                    search_val_result = await self.arango_handler.parallel_search(
                        search_queries, 
                        search_type="bm25"  # Use BM25 for now due to API issues
                    )
                    
                    search_val_duration = time.time() - search_val_start
                    results["search_results"] = search_val_result["total_results"]
                    
                    print(f"✅ Found {search_val_result['total_results']} results in {search_val_duration:.2f}s")
        
        # Calculate total duration
        results["total_duration"] = time.time() - pipeline_start
        
        # Performance summary
        print(f"\n{'='*80}")
        print("Performance Optimization Results")
        print(f"{'='*80}")
        
        metrics_summary = self.metrics.get_summary()
        
        print(f"Total Pipeline Duration: {results['total_duration']:.2f}s")
        print(f"Cache Hit Ratio: {metrics_summary['cache_hit_ratio']}")
        print(f"Average API Time: {metrics_summary['avg_api_time']}")
        print(f"Average DB Time: {metrics_summary['avg_db_time']}")
        print(f"Parallel Tasks: {metrics_summary['parallel_tasks']}")
        print(f"Retry Count: {metrics_summary['retry_count']}")
        
        # Compare with baseline (from previous tests)
        baseline_duration = 15.0  # Average from Level 2/3 tests
        optimization_gain = (baseline_duration - results["total_duration"]) / baseline_duration
        
        print(f"\nOptimization Gain: {optimization_gain:.1%} faster than baseline")
        
        results["metrics"] = metrics_summary
        results["optimization_gains"]["percentage"] = f"{optimization_gain:.1%}"
        
        return results
        
    def cleanup(self):
        """Clean up resources"""
        self.cache.clear()


async def run_performance_tests():
    """Run comprehensive performance optimization tests"""
    optimizer = PerformanceOptimizer()
    
    try:
        # Test 1: Cold cache
        print("\n🧪 Test 1: Cold Cache Performance")
        cold_results = await optimizer.run_optimized_pipeline("buffer overflow mitigation")
        
        # Test 2: Warm cache
        print("\n\n🧪 Test 2: Warm Cache Performance")
        warm_results = await optimizer.run_optimized_pipeline("buffer overflow mitigation")
        
        # Test 3: Different query
        print("\n\n🧪 Test 3: Parallel Operations")
        parallel_results = await optimizer.run_optimized_pipeline("quantum computing security")
        
        # Generate comparison report
        print(f"\n\n{'='*80}")
        print("Performance Optimization Report")
        print(f"{'='*80}")
        
        print("\nTest Comparison:")
        print(f"Cold Cache: {cold_results['total_duration']:.2f}s")
        print(f"Warm Cache: {warm_results['total_duration']:.2f}s")
        print(f"Parallel Ops: {parallel_results['total_duration']:.2f}s")
        
        cache_improvement = (cold_results['total_duration'] - warm_results['total_duration']) / cold_results['total_duration']
        print(f"\nCache Improvement: {cache_improvement:.1%}")
        
        # Success criteria
        success = all([
            cold_results['total_duration'] < 10.0,  # Target: <10s
            warm_results['total_duration'] < 5.0,   # Target: <5s with cache
            cache_improvement > 0.3                  # Target: >30% improvement
        ])
        
        print(f"\nOptimization Success: {'✅ PASSED' if success else '❌ FAILED'}")
        
        return success
        
    finally:
        optimizer.cleanup()


if __name__ == "__main__":
    # Set environment
    os.environ['ARANGO_HOST'] = 'http://localhost:8529'
    os.environ['ARANGO_USER'] = 'root'
    os.environ['ARANGO_PASSWORD'] = 'openSesame'
    
    # Run async tests
    success = asyncio.run(run_performance_tests())
    
    # Exit code
    exit(0 if success else 1)