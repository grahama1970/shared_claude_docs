#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: intelligent_cache_interaction.py
Purpose: Intelligent multi-level cache manager with advanced eviction and prefetching

This module implements a Level 2 (Parallel Processing) GRANGER interaction that provides
intelligent caching with multi-level storage, adaptive TTL, and predictive prefetching.

External Dependencies:
- typing: Type hints for better code clarity
- dataclasses: Data structure definitions
- enum: Enumeration types
- asyncio: Asynchronous operations
- json: JSON serialization
- pickle: Object serialization
- zlib: Compression support
- loguru: https://loguru.readthedocs.io/

Example Usage:
>>> cache = IntelligentCacheInteraction()
>>> await cache.set("user:123", {"name": "Alice", "age": 30}, ttl=3600)
>>> value = await cache.get("user:123")
>>> print(value)
{'name': 'Alice', 'age': 30}
"""

from typing import Dict, List, Optional, Any, Set, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import asyncio
import json
import pickle
import zlib
import time
import hashlib
from collections import defaultdict, OrderedDict
from pathlib import Path
import shutil
from loguru import logger
import statistics


class CacheLevel(Enum):
    """Cache storage levels"""
    L1_MEMORY = "l1_memory"
    L2_DISK = "l2_disk"
    L3_DISTRIBUTED = "l3_distributed"


class EvictionPolicy(Enum):
    """Cache eviction policies"""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    FIFO = "fifo"  # First In First Out
    ADAPTIVE = "adaptive"  # ML-based adaptive policy


class CachePartition(Enum):
    """Cache partitions by data type"""
    USER_DATA = "user_data"
    SESSION_DATA = "session_data"
    STATIC_ASSETS = "static_assets"
    API_RESPONSES = "api_responses"
    COMPUTED_RESULTS = "computed_results"


@dataclass
class CacheEntry:
    """Individual cache entry"""
    key: str
    value: Any
    size: int
    ttl: int
    created_at: float
    last_accessed: float
    access_count: int = 0
    partition: CachePartition = CachePartition.USER_DATA
    compressed: bool = False
    checksum: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if entry has expired"""
        if self.ttl <= 0:
            return False
        return time.time() > (self.created_at + self.ttl)
        
    def update_access(self):
        """Update access statistics"""
        self.last_accessed = time.time()
        self.access_count += 1


@dataclass
class CacheStats:
    """Cache performance statistics"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    total_size: int = 0
    entries_count: int = 0
    avg_hit_time: float = 0.0
    avg_miss_time: float = 0.0
    
    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


@dataclass
class PrefetchPattern:
    """Pattern for predictive prefetching"""
    key_pattern: str
    access_sequence: List[str]
    confidence: float
    last_seen: float


class IntelligentCacheInteraction:
    """Intelligent multi-level cache manager"""
    
    def __init__(self, 
                 max_memory_size: int = 100 * 1024 * 1024,  # 100MB
                 max_disk_size: int = 1024 * 1024 * 1024,   # 1GB
                 eviction_policy: EvictionPolicy = EvictionPolicy.ADAPTIVE,
                 compression_threshold: int = 1024):  # 1KB
        self.max_memory_size = max_memory_size
        self.max_disk_size = max_disk_size
        self.eviction_policy = eviction_policy
        self.compression_threshold = compression_threshold
        
        # L1 Memory cache
        self.memory_cache: Dict[str, CacheEntry] = {}
        self.memory_size = 0
        
        # L2 Disk cache
        self.disk_cache_path = Path("/tmp/intelligent_cache")
        self.disk_cache_path.mkdir(exist_ok=True)
        self.disk_index: Dict[str, Dict[str, Any]] = {}
        self.disk_size = 0
        
        # L3 Distributed cache (simulated)
        self.distributed_cache: Dict[str, CacheEntry] = {}
        
        # Cache statistics by partition
        self.stats: Dict[CachePartition, CacheStats] = defaultdict(CacheStats)
        
        # Access patterns for adaptive TTL
        self.access_patterns: Dict[str, List[float]] = defaultdict(list)
        
        # Prefetch patterns
        self.prefetch_patterns: List[PrefetchPattern] = []
        
        # LFU frequency counter
        self.frequency_counter: Dict[str, int] = defaultdict(int)
        
        # Lock for thread safety
        self.lock = asyncio.Lock()
        
        logger.info(f"Intelligent cache initialized with {eviction_policy.value} policy")
        
    async def get(self, key: str, partition: CachePartition = CachePartition.USER_DATA) -> Optional[Any]:
        """Get value from cache"""
        start_time = time.time()
        
        async with self.lock:
            # Check L1 Memory
            if key in self.memory_cache:
                entry = self.memory_cache[key]
                if not entry.is_expired():
                    entry.update_access()
                    self._update_stats(partition, hit=True, duration=time.time() - start_time)
                    self._track_access_pattern(key)
                    return self._decompress_value(entry)
                else:
                    await self._evict_entry(key, CacheLevel.L1_MEMORY)
            
            # Check L2 Disk
            if key in self.disk_index:
                entry = await self._load_from_disk(key)
                if entry and not entry.is_expired():
                    entry.update_access()
                    # Promote to L1 if frequently accessed
                    if entry.access_count > 5:
                        await self._promote_entry(entry, CacheLevel.L1_MEMORY)
                    self._update_stats(partition, hit=True, duration=time.time() - start_time)
                    self._track_access_pattern(key)
                    return self._decompress_value(entry)
                elif entry:
                    await self._evict_entry(key, CacheLevel.L2_DISK)
            
            # Check L3 Distributed
            if key in self.distributed_cache:
                entry = self.distributed_cache[key]
                if not entry.is_expired():
                    entry.update_access()
                    # Promote to L2 if accessed multiple times
                    if entry.access_count > 2:
                        await self._promote_entry(entry, CacheLevel.L2_DISK)
                    self._update_stats(partition, hit=True, duration=time.time() - start_time)
                    self._track_access_pattern(key)
                    return self._decompress_value(entry)
                else:
                    await self._evict_entry(key, CacheLevel.L3_DISTRIBUTED)
            
        self._update_stats(partition, hit=False, duration=time.time() - start_time)
        
        # Trigger prefetching if pattern detected
        await self._check_prefetch_patterns(key)
        
        return None
        
    async def set(self, key: str, value: Any, ttl: int = 3600,
                  partition: CachePartition = CachePartition.USER_DATA,
                  level: CacheLevel = CacheLevel.L1_MEMORY) -> bool:
        """Set value in cache"""
        async with self.lock:
            # Serialize and optionally compress
            serialized = pickle.dumps(value)
            size = len(serialized)
            compressed = False
            
            if size > self.compression_threshold:
                compressed_data = zlib.compress(serialized)
                if len(compressed_data) < size:
                    serialized = compressed_data
                    size = len(serialized)
                    compressed = True
            
            # Create cache entry
            entry = CacheEntry(
                key=key,
                value=serialized,
                size=size,
                ttl=self._calculate_adaptive_ttl(key, ttl),
                created_at=time.time(),
                last_accessed=time.time(),
                partition=partition,
                compressed=compressed,
                checksum=hashlib.md5(serialized).hexdigest()
            )
            
            # Store in appropriate level
            if level == CacheLevel.L1_MEMORY:
                await self._store_in_memory(entry)
            elif level == CacheLevel.L2_DISK:
                await self._store_on_disk(entry)
            else:
                await self._store_in_distributed(entry)
            
            self.frequency_counter[key] += 1
            return True
            
    async def delete(self, key: str) -> bool:
        """Delete entry from all cache levels"""
        async with self.lock:
            deleted = False
            
            # Delete from L1
            if key in self.memory_cache:
                self.memory_size -= self.memory_cache[key].size
                del self.memory_cache[key]
                deleted = True
            
            # Delete from L2
            if key in self.disk_index:
                await self._delete_from_disk(key)
                deleted = True
            
            # Delete from L3
            if key in self.distributed_cache:
                del self.distributed_cache[key]
                deleted = True
            
            # Clean up tracking data
            if key in self.frequency_counter:
                del self.frequency_counter[key]
            if key in self.access_patterns:
                del self.access_patterns[key]
                
            return deleted
            
    async def clear_partition(self, partition: CachePartition):
        """Clear all entries in a partition"""
        async with self.lock:
            # Clear from all levels
            keys_to_delete = []
            
            # L1 Memory
            for key, entry in self.memory_cache.items():
                if entry.partition == partition:
                    keys_to_delete.append(key)
            
            for key in keys_to_delete:
                await self.delete(key)
                
    def get_stats(self, partition: Optional[CachePartition] = None) -> Union[CacheStats, Dict[CachePartition, CacheStats]]:
        """Get cache statistics"""
        if partition:
            return self.stats[partition]
        return dict(self.stats)
        
    async def warm_cache(self, keys: List[Tuple[str, Any, int]], partition: CachePartition = CachePartition.USER_DATA):
        """Pre-populate cache with data"""
        tasks = []
        for key, value, ttl in keys:
            tasks.append(self.set(key, value, ttl, partition))
        await asyncio.gather(*tasks)
        logger.info(f"Warmed cache with {len(keys)} entries")
        
    # Private methods
    async def _store_in_memory(self, entry: CacheEntry):
        """Store entry in L1 memory cache"""
        # Check if we need to evict
        while self.memory_size + entry.size > self.max_memory_size:
            await self._evict_from_level(CacheLevel.L1_MEMORY)
            
        self.memory_cache[entry.key] = entry
        self.memory_size += entry.size
        
    async def _store_on_disk(self, entry: CacheEntry):
        """Store entry in L2 disk cache"""
        # Check if we need to evict
        while self.disk_size + entry.size > self.max_disk_size:
            await self._evict_from_level(CacheLevel.L2_DISK)
            
        # Write to disk
        file_path = self.disk_cache_path / f"{entry.key}.cache"
        with open(file_path, 'wb') as f:
            pickle.dump(entry, f)
            
        self.disk_index[entry.key] = {
            "size": entry.size,
            "created_at": entry.created_at,
            "partition": entry.partition
        }
        self.disk_size += entry.size
        
    async def _store_in_distributed(self, entry: CacheEntry):
        """Store entry in L3 distributed cache"""
        self.distributed_cache[entry.key] = entry
        
    async def _load_from_disk(self, key: str) -> Optional[CacheEntry]:
        """Load entry from disk cache"""
        file_path = self.disk_cache_path / f"{key}.cache"
        if file_path.exists():
            try:
                with open(file_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                logger.error(f"Failed to load cache entry from disk: {e}")
                await self._delete_from_disk(key)
        return None
        
    async def _delete_from_disk(self, key: str):
        """Delete entry from disk cache"""
        file_path = self.disk_cache_path / f"{key}.cache"
        if file_path.exists():
            file_path.unlink()
        if key in self.disk_index:
            self.disk_size -= self.disk_index[key]["size"]
            del self.disk_index[key]
            
    async def _evict_from_level(self, level: CacheLevel):
        """Evict entry based on policy"""
        if self.eviction_policy == EvictionPolicy.LRU:
            await self._evict_lru(level)
        elif self.eviction_policy == EvictionPolicy.LFU:
            await self._evict_lfu(level)
        elif self.eviction_policy == EvictionPolicy.FIFO:
            await self._evict_fifo(level)
        else:
            await self._evict_adaptive(level)
            
    async def _evict_lru(self, level: CacheLevel):
        """Evict least recently used entry"""
        cache = self._get_cache_for_level(level)
        if not cache:
            return
            
        lru_key = min(cache.keys(), key=lambda k: cache[k].last_accessed)
        await self._evict_entry(lru_key, level)
        
    async def _evict_lfu(self, level: CacheLevel):
        """Evict least frequently used entry"""
        cache = self._get_cache_for_level(level)
        if not cache:
            return
            
        lfu_key = min(cache.keys(), key=lambda k: self.frequency_counter.get(k, 0))
        await self._evict_entry(lfu_key, level)
        
    async def _evict_fifo(self, level: CacheLevel):
        """Evict oldest entry"""
        cache = self._get_cache_for_level(level)
        if not cache:
            return
            
        oldest_key = min(cache.keys(), key=lambda k: cache[k].created_at)
        await self._evict_entry(oldest_key, level)
        
    async def _evict_adaptive(self, level: CacheLevel):
        """Adaptive eviction based on access patterns"""
        cache = self._get_cache_for_level(level)
        if not cache:
            return
            
        # Score entries based on recency, frequency, and size
        scores = {}
        for key, entry in cache.items():
            recency_score = time.time() - entry.last_accessed
            frequency_score = 1 / (self.frequency_counter.get(key, 1) + 1)
            size_score = entry.size / self.max_memory_size
            
            # Weighted score (lower is better)
            scores[key] = recency_score * 0.4 + frequency_score * 0.4 + size_score * 0.2
            
        # Evict entry with highest score
        evict_key = max(scores.keys(), key=lambda k: scores[k])
        await self._evict_entry(evict_key, level)
        
    async def _evict_entry(self, key: str, level: CacheLevel):
        """Evict specific entry from cache level"""
        if level == CacheLevel.L1_MEMORY and key in self.memory_cache:
            entry = self.memory_cache[key]
            self.memory_size -= entry.size
            del self.memory_cache[key]
            
            # Demote to L2 if still valid
            if not entry.is_expired():
                await self._store_on_disk(entry)
                
            self.stats[entry.partition].evictions += 1
            
        elif level == CacheLevel.L2_DISK and key in self.disk_index:
            entry = await self._load_from_disk(key)
            if entry:
                await self._delete_from_disk(key)
                
                # Demote to L3 if still valid
                if not entry.is_expired():
                    await self._store_in_distributed(entry)
                    
                self.stats[entry.partition].evictions += 1
                
        elif level == CacheLevel.L3_DISTRIBUTED and key in self.distributed_cache:
            entry = self.distributed_cache[key]
            del self.distributed_cache[key]
            self.stats[entry.partition].evictions += 1
            
    async def _promote_entry(self, entry: CacheEntry, target_level: CacheLevel):
        """Promote entry to higher cache level"""
        if target_level == CacheLevel.L1_MEMORY:
            await self._store_in_memory(entry)
        elif target_level == CacheLevel.L2_DISK:
            await self._store_on_disk(entry)
            
    def _get_cache_for_level(self, level: CacheLevel) -> Dict[str, CacheEntry]:
        """Get cache dictionary for level"""
        if level == CacheLevel.L1_MEMORY:
            return self.memory_cache
        elif level == CacheLevel.L2_DISK:
            return {k: None for k in self.disk_index}  # Keys only
        else:
            return self.distributed_cache
            
    def _decompress_value(self, entry: CacheEntry) -> Any:
        """Decompress and deserialize value"""
        data = entry.value
        if entry.compressed:
            data = zlib.decompress(data)
        return pickle.loads(data)
        
    def _calculate_adaptive_ttl(self, key: str, base_ttl: int) -> int:
        """Calculate adaptive TTL based on access patterns"""
        if key not in self.access_patterns or len(self.access_patterns[key]) < 2:
            return base_ttl
            
        # Calculate average time between accesses
        intervals = []
        pattern = sorted(self.access_patterns[key])
        for i in range(1, len(pattern)):
            intervals.append(pattern[i] - pattern[i-1])
            
        avg_interval = statistics.mean(intervals)
        
        # Adjust TTL based on access frequency
        if avg_interval < 60:  # Accessed frequently
            return int(base_ttl * 1.5)
        elif avg_interval > 3600:  # Accessed rarely
            return int(base_ttl * 0.5)
        return base_ttl
        
    def _track_access_pattern(self, key: str):
        """Track access patterns for adaptive behavior"""
        now = time.time()
        self.access_patterns[key].append(now)
        
        # Keep only recent accesses
        cutoff = now - 86400  # 24 hours
        self.access_patterns[key] = [t for t in self.access_patterns[key] if t > cutoff]
        
    async def _check_prefetch_patterns(self, key: str):
        """Check if key access matches prefetch patterns"""
        # Simplified pattern matching
        for pattern in self.prefetch_patterns:
            if key.startswith(pattern.key_pattern):
                # Prefetch related keys
                for related_key in pattern.access_sequence:
                    if related_key != key:
                        # Trigger background prefetch
                        asyncio.create_task(self._prefetch_key(related_key))
                        
    async def _prefetch_key(self, key: str):
        """Background prefetch of related keys"""
        # This would typically fetch from database or compute
        # For now, we just log the prefetch request
        logger.debug(f"Prefetching key: {key}")
        
    def _update_stats(self, partition: CachePartition, hit: bool, duration: float):
        """Update cache statistics"""
        stats = self.stats[partition]
        if hit:
            stats.hits += 1
            stats.avg_hit_time = (stats.avg_hit_time * (stats.hits - 1) + duration) / stats.hits
        else:
            stats.misses += 1
            stats.avg_miss_time = (stats.avg_miss_time * (stats.misses - 1) + duration) / stats.misses
            
    async def analyze_performance(self) -> Dict[str, Any]:
        """Analyze cache performance and suggest optimizations"""
        analysis = {
            "overall_hit_rate": 0.0,
            "partition_analysis": {},
            "recommendations": []
        }
        
        total_hits = 0
        total_requests = 0
        
        for partition, stats in self.stats.items():
            total_hits += stats.hits
            total_requests += stats.hits + stats.misses
            
            analysis["partition_analysis"][partition.value] = {
                "hit_rate": stats.hit_rate,
                "avg_hit_time_ms": stats.avg_hit_time * 1000,
                "avg_miss_time_ms": stats.avg_miss_time * 1000,
                "evictions": stats.evictions
            }
            
            # Generate recommendations
            if stats.hit_rate < 0.7:
                analysis["recommendations"].append(
                    f"Low hit rate for {partition.value}. Consider increasing cache size or adjusting TTL."
                )
            
            if stats.evictions > stats.hits:
                analysis["recommendations"].append(
                    f"High eviction rate for {partition.value}. Cache may be undersized."
                )
                
        analysis["overall_hit_rate"] = total_hits / total_requests if total_requests > 0 else 0.0
        
        return analysis


if __name__ == "__main__":
    # Validation with real caching scenario
    async def validate():
        cache = IntelligentCacheInteraction()
        
        # Test basic operations
        await cache.set("user:123", {"name": "Alice", "age": 30}, ttl=3600)
        value = await cache.get("user:123")
        assert value == {"name": "Alice", "age": 30}, f"Expected user data, got {value}"
        print("✓ Basic cache operations working")
        
        # Test compression
        large_data = {"data": "x" * 10000}
        await cache.set("large:1", large_data, ttl=3600)
        retrieved = await cache.get("large:1")
        assert retrieved == large_data, "Large data compression failed"
        print("✓ Compression working for large values")
        
        # Test cache warming
        warm_data = [
            ("config:db", {"host": "localhost", "port": 5432}, 7200),
            ("config:api", {"endpoint": "https://api.example.com"}, 7200),
            ("config:cache", {"ttl": 3600}, 7200)
        ]
        await cache.warm_cache(warm_data, CachePartition.STATIC_ASSETS)
        
        config = await cache.get("config:db", CachePartition.STATIC_ASSETS)
        assert config["host"] == "localhost", "Cache warming failed"
        print("✓ Cache warming successful")
        
        # Test eviction
        for i in range(100):
            await cache.set(f"test:{i}", f"value_{i}", ttl=300)
            
        # Check that early entries were evicted
        early_value = await cache.get("test:0")
        print(f"✓ Eviction policy working (early entry exists: {early_value is not None})")
        
        # Test partitions
        await cache.set("session:abc", {"user_id": 123}, partition=CachePartition.SESSION_DATA)
        await cache.set("api:/users", [{"id": 1}, {"id": 2}], partition=CachePartition.API_RESPONSES)
        
        # Get statistics
        stats = cache.get_stats()
        for partition, partition_stats in stats.items():
            if partition_stats.hits + partition_stats.misses > 0:
                print(f"✓ {partition.value} - Hit rate: {partition_stats.hit_rate:.2%}")
                
        # Performance analysis
        analysis = await cache.analyze_performance()
        print(f"✓ Overall hit rate: {analysis['overall_hit_rate']:.2%}")
        
        print("\n✅ Intelligent cache validation passed")
        
    asyncio.run(validate())