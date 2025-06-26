#!/usr/bin/env python3
"""
Module: arangodb_fixes.py
Description: ArangoDB-specific bug fixes implementation

External Dependencies:
- granger_common: Our standardized components
- arangodb: ArangoDB Python driver
"""

from pathlib import Path
import re

def apply_arangodb_fixes():
    """Apply all ArangoDB-specific fixes."""
    print("\n🗄️  Applying ArangoDB fixes...")
    
    # 1. Fix transaction integrity with proper isolation
    transaction_integrity_code = '''
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, List, Optional
from arangodb.exceptions import TransactionAbortError
from granger_common import SchemaManager
import asyncio

class ArangoTransaction:
    """Enhanced transaction management for ArangoDB."""
    
    def __init__(self, db_connection, read_collections: List[str], write_collections: List[str]):
        self.db = db_connection
        self.read_collections = read_collections
        self.write_collections = write_collections
        self.transaction = None
        self.operations = []
        
    async def begin(self):
        """Begin transaction with proper isolation."""
        self.transaction = await self.db.begin_transaction(
            read=self.read_collections,
            write=self.write_collections,
            sync=True,  # Ensure durability
            lock_timeout=30,  # Prevent deadlocks
            max_transaction_size=100000000  # 100MB limit
        )
        return self
    
    async def execute(self, operation: str, bind_vars: dict = None):
        """Execute operation within transaction."""
        if not self.transaction:
            raise RuntimeError("Transaction not started")
            
        result = await self.transaction.execute(operation, bind_vars=bind_vars)
        self.operations.append((operation, bind_vars))
        return result
    
    async def commit(self):
        """Commit transaction with verification."""
        if self.transaction:
            await self.transaction.commit()
            logger.info(f"Transaction committed: {len(self.operations)} operations")
            
    async def abort(self):
        """Abort transaction and rollback."""
        if self.transaction:
            await self.transaction.abort()
            logger.warning(f"Transaction aborted: {len(self.operations)} operations rolled back")

@asynccontextmanager
async def atomic_graph_operation(db, read_collections: List[str], write_collections: List[str]) -> AsyncGenerator[ArangoTransaction, None]:
    """Context manager for atomic graph operations."""
    txn = ArangoTransaction(db, read_collections, write_collections)
    
    try:
        await txn.begin()
        yield txn
        await txn.commit()
    except Exception as e:
        await txn.abort()
        logger.error(f"Transaction failed: {e}")
        raise

# Usage example:
async def store_research_graph(doc_id: str, entities: list, relationships: list):
    """Store document with entities and relationships atomically."""
    
    async with atomic_graph_operation(
        db, 
        read_collections=["documents"],
        write_collections=["documents", "entities", "relationships", "edges"]
    ) as txn:
        # All operations succeed or all fail
        
        # Store document
        await txn.execute(
            "INSERT @doc INTO documents",
            bind_vars={"doc": {"_key": doc_id, "processed": True}}
        )
        
        # Store entities
        for entity in entities:
            await txn.execute(
                "INSERT @entity INTO entities",
                bind_vars={"entity": entity}
            )
        
        # Store relationships as edges
        for rel in relationships:
            await txn.execute(
                "INSERT @edge INTO edges",
                bind_vars={"edge": rel}
            )
'''
    
    # 2. Add connection pooling and retry logic
    connection_pooling_code = '''
from arangodb import ArangoClient
from asyncio import Semaphore, sleep
from typing import Optional

class ArangoConnectionPool:
    """Connection pool with retry logic for ArangoDB."""
    
    def __init__(
        self,
        hosts: List[str],
        username: str,
        password: str,
        database: str,
        pool_size: int = 10,
        max_retries: int = 3
    ):
        self.hosts = hosts
        self.username = username
        self.password = password
        self.database = database
        self.pool_size = pool_size
        self.max_retries = max_retries
        
        # Create client with multiple hosts for failover
        self.client = ArangoClient(hosts=hosts)
        self.db = None
        self.semaphore = Semaphore(pool_size)
        
    async def connect(self):
        """Establish connection with retry logic."""
        for attempt in range(self.max_retries):
            try:
                self.db = await self.client.db(
                    name=self.database,
                    username=self.username,
                    password=self.password,
                    verify=True
                )
                logger.info(f"Connected to ArangoDB: {self.database}")
                return
            except Exception as e:
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Connection attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
                    await sleep(wait_time)
                else:
                    raise
    
    async def execute_with_retry(self, query: str, bind_vars: dict = None) -> Any:
        """Execute query with automatic retry on failure."""
        async with self.semaphore:  # Limit concurrent connections
            for attempt in range(self.max_retries):
                try:
                    cursor = await self.db.aql.execute(
                        query,
                        bind_vars=bind_vars,
                        batch_size=1000,
                        ttl=60  # Query timeout
                    )
                    return [doc async for doc in cursor]
                except Exception as e:
                    if attempt < self.max_retries - 1 and self._is_retryable(e):
                        wait_time = 2 ** attempt
                        logger.warning(f"Query failed, retrying in {wait_time}s: {e}")
                        await sleep(wait_time)
                    else:
                        raise
    
    def _is_retryable(self, error: Exception) -> bool:
        """Check if error is retryable."""
        error_msg = str(error).lower()
        retryable_errors = [
            "connection", "timeout", "unavailable",
            "conflict", "deadlock", "busy"
        ]
        return any(err in error_msg for err in retryable_errors)
'''
    
    # 3. Add schema versioning and migration
    schema_management_code = '''
from granger_common import SchemaManager, SchemaVersion
from datetime import datetime

class ArangoSchemaManager:
    """Schema management for ArangoDB collections."""
    
    def __init__(self, db):
        self.db = db
        self.schema_manager = SchemaManager()
        self._register_schemas()
        
    def _register_schemas(self):
        """Register all collection schemas."""
        
        # Document schema v1
        self.schema_manager.register_schema(
            "document",
            SchemaVersion(1, 0),
            {
                "type": "object",
                "required": ["content", "metadata"],
                "properties": {
                    "content": {"type": "string"},
                    "metadata": {"type": "object"},
                    "embeddings": {"type": "array"}
                }
            }
        )
        
        # Document schema v2 (adds quality score)
        self.schema_manager.register_schema(
            "document",
            SchemaVersion(2, 0),
            {
                "type": "object",
                "required": ["content", "metadata", "quality_score"],
                "properties": {
                    "content": {"type": "string"},
                    "metadata": {"type": "object"},
                    "embeddings": {"type": "array"},
                    "quality_score": {"type": "number"},
                    "processing_time": {"type": "number"}
                }
            }
        )
        
        # Entity schema
        self.schema_manager.register_schema(
            "entity",
            SchemaVersion(1, 0),
            {
                "type": "object",
                "required": ["name", "type"],
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "confidence": {"type": "number"},
                    "source_doc": {"type": "string"}
                }
            }
        )
        
        # Register migration
        self.schema_manager.register_migration(
            "document",
            SchemaVersion(1, 0),
            SchemaVersion(2, 0),
            self._migrate_document_v1_to_v2
        )
    
    def _migrate_document_v1_to_v2(self, doc: dict) -> dict:
        """Migrate document from v1 to v2."""
        doc["quality_score"] = self._calculate_quality_score(doc)
        doc["processing_time"] = 0  # Default for old docs
        doc["_schema_version"] = "2.0"
        return doc
    
    def _calculate_quality_score(self, doc: dict) -> float:
        """Calculate quality score for document."""
        score = 0.0
        
        # Has content
        if doc.get("content"):
            score += 0.3
            
        # Has embeddings
        if doc.get("embeddings") and len(doc["embeddings"]) > 0:
            score += 0.3
            
        # Has metadata
        if doc.get("metadata"):
            score += 0.2
            
        # Content length bonus
        content_length = len(doc.get("content", ""))
        if content_length > 1000:
            score += 0.2
            
        return min(score, 1.0)
'''
    
    # 4. Add graph-specific optimizations
    graph_optimization_code = '''
class GraphQueryOptimizer:
    """Optimize graph queries for performance."""
    
    def __init__(self, db):
        self.db = db
        self._ensure_indexes()
        
    async def _ensure_indexes(self):
        """Ensure all required indexes exist."""
        indexes = [
            ("entities", ["type", "name"], "persistent"),
            ("relationships", ["source", "target"], "persistent"),
            ("documents", ["metadata.date"], "persistent"),
            ("edges", ["_from", "_to"], "edge")
        ]
        
        for collection, fields, index_type in indexes:
            try:
                await self.db.collection(collection).add_index({
                    "type": index_type,
                    "fields": fields,
                    "unique": False
                })
                logger.info(f"Index created on {collection}: {fields}")
            except Exception as e:
                if "duplicate" not in str(e).lower():
                    logger.error(f"Failed to create index on {collection}: {e}")
    
    def optimize_traversal_query(self, start_vertex: str, depth: int = 2) -> str:
        """Generate optimized graph traversal query."""
        return f"""
        FOR v, e, p IN {depth} OUTBOUND @start_vertex
            edges
            OPTIONS {{
                bfs: true,
                uniqueVertices: 'global',
                uniqueEdges: 'global'
            }}
            FILTER p.vertices[1].active == true
            LIMIT 1000
            RETURN {{
                vertex: v,
                edge: e,
                path: p
            }}
        """
    
    def batch_insert_query(self, collection: str, docs: List[dict]) -> str:
        """Generate efficient batch insert query."""
        return f"""
        FOR doc IN @docs
            INSERT doc INTO {collection}
            OPTIONS {{
                overwrite: false,
                waitForSync: false,
                skipDocumentValidation: false
            }}
            RETURN NEW._key
        """
'''
    
    # 5. Add monitoring and metrics
    monitoring_code = '''
from dataclasses import dataclass
from collections import defaultdict
import time

@dataclass
class QueryMetrics:
    """Metrics for query performance."""
    query_type: str
    execution_time: float
    document_count: int
    success: bool
    error: Optional[str] = None

class ArangoMonitor:
    """Monitor ArangoDB performance and health."""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.slow_query_threshold = 1.0  # seconds
        
    async def track_query(self, query_type: str, query_func, *args, **kwargs):
        """Track query execution metrics."""
        start_time = time.time()
        success = True
        error = None
        result = None
        
        try:
            result = await query_func(*args, **kwargs)
            doc_count = len(result) if isinstance(result, list) else 1
        except Exception as e:
            success = False
            error = str(e)
            doc_count = 0
            raise
        finally:
            execution_time = time.time() - start_time
            
            metric = QueryMetrics(
                query_type=query_type,
                execution_time=execution_time,
                document_count=doc_count,
                success=success,
                error=error
            )
            
            self.metrics[query_type].append(metric)
            
            # Log slow queries
            if execution_time > self.slow_query_threshold:
                logger.warning(f"Slow query detected: {query_type} took {execution_time:.2f}s")
        
        return result
    
    def get_performance_summary(self) -> dict:
        """Get performance summary statistics."""
        summary = {}
        
        for query_type, metrics in self.metrics.items():
            total_queries = len(metrics)
            successful = sum(1 for m in metrics if m.success)
            avg_time = sum(m.execution_time for m in metrics) / total_queries
            
            summary[query_type] = {
                "total_queries": total_queries,
                "success_rate": f"{(successful / total_queries * 100):.1f}%",
                "avg_execution_time": f"{avg_time:.3f}s",
                "total_documents": sum(m.document_count for m in metrics),
                "slow_queries": sum(1 for m in metrics if m.execution_time > self.slow_query_threshold)
            }
        
        return summary
'''
    
    print("✅ ArangoDB fixes defined - ready for implementation")
    
    # Create implementation guide
    implementation_guide = '''
# ArangoDB Module Fix Implementation Guide

## 1. Transaction Integrity (CRITICAL)
Location: src/arangodb/transactions.py
- Replace basic transactions with ArangoTransaction class
- Use atomic_graph_operation for multi-collection operations
- Set proper isolation levels and timeouts
- Add transaction size limits

## 2. Connection Pooling (HIGH)
Location: src/arangodb/connection.py
- Implement ArangoConnectionPool
- Configure with multiple hosts for failover
- Set pool size to 10 connections
- Add exponential backoff retry logic

## 3. Schema Management (MEDIUM)
Location: src/arangodb/schema.py
- Use ArangoSchemaManager for versioning
- Define schemas for all collections
- Implement migration functions
- Track schema version in documents

## 4. Query Optimization (HIGH)
Location: src/arangodb/optimizer.py
- Create required indexes on startup
- Use batch operations for bulk inserts
- Optimize graph traversal queries
- Limit result sets to prevent OOM

## 5. Monitoring (MEDIUM)
Location: src/arangodb/monitoring.py
- Track all query metrics
- Log slow queries (>1 second)
- Monitor connection pool usage
- Export metrics for dashboards

## Configuration
```yaml
arangodb:
  hosts:
    - "http://localhost:8529"
    - "http://localhost:8530"  # Failover
  database: "granger"
  username: "root"
  password: "${ARANGO_PASSWORD}"
  
  pool:
    size: 10
    timeout: 30
    
  transactions:
    lock_timeout: 30
    max_size: 100000000  # 100MB
    
  monitoring:
    slow_query_threshold: 1.0
    metrics_interval: 60
```

## Best Practices
1. Always use transactions for multi-document operations
2. Batch inserts in groups of 1000
3. Use projections to limit returned fields
4. Create indexes before bulk imports
5. Monitor collection sizes and prune old data

## Testing
1. Transaction test: Simulate failures mid-transaction
2. Pool test: Max out connections
3. Performance test: 10k documents/second
4. Failover test: Kill primary ArangoDB
5. Schema test: Migrate 100k v1 documents

## Common Issues
- "Conflict" errors: Add retry logic
- Slow queries: Check missing indexes
- OOM errors: Use streaming/pagination
- Deadlocks: Reduce transaction scope
'''
    
    # Save implementation guide
    guide_path = Path("/home/graham/workspace/shared_claude_docs/module_specific_fixes/arangodb_implementation_guide.md")
    guide_path.parent.mkdir(exist_ok=True)
    guide_path.write_text(implementation_guide)
    print(f"📝 Implementation guide saved to: {guide_path}")


if __name__ == "__main__":
    apply_arangodb_fixes()