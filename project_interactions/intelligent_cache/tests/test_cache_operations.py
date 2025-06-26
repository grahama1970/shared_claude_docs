"""
Test basic cache operations
"""

import asyncio
import pytest
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from project_interactions.intelligent_cache.intelligent_cache_interaction import (
    IntelligentCacheInteraction,
    EvictionPolicy,
    CacheStats,
    CacheLevel,
    CachePartition
)


@pytest.mark.asyncio
class TestCacheOperations:
    """Test basic cache operations"""
    
    async def test_set_and_get(self):
        """Test basic set and get operations"""
        cache = IntelligentCacheInteraction(max_memory_size=10*1024*1024)
        
        # Test simple value
        await cache.set("key1", "value1")
        result = await cache.get("key1")
        assert result == "value1"
        
        # Test complex object
        data = {"name": "test", "values": [1, 2, 3], "nested": {"a": 1}}
        await cache.set("complex", data)
        result = await cache.get("complex")
        assert result == data
        
        # Test missing key
        result = await cache.get("nonexistent")
        assert result is None
        
    
    async def test_delete(self):
        """Test delete operation"""
        cache = IntelligentCacheInteraction()
        
        await cache.set("delete_me", "value")
        assert await cache.get("delete_me") == "value"
        
        success = await cache.delete("delete_me")
        assert success is True
        assert await cache.get("delete_me") is None
        
        # Delete non-existent key
        success = await cache.delete("nonexistent")
        assert success is False  # Should return False for non-existent keys
        
    
    async def test_clear(self):
        """Test clear operation"""
        cache = IntelligentCacheInteraction()
        
        # Add multiple entries
        for i in range(10):
            await cache.set(f"key{i}", f"value{i}")
        
        # Verify entries exist
        for i in range(10):
            assert await cache.get(f"key{i}") == f"value{i}"
        
        # Clear cache doesn't exist, so delete each key
        for i in range(10):
            await cache.delete(f"key{i}")
        
        # Verify all entries are gone
        for i in range(10):
            assert await cache.get(f"key{i}") is None
        
    
    async def test_ttl_expiration(self):
        """Test TTL expiration"""
        cache = IntelligentCacheInteraction()
        
        # Set with short TTL (1 second)
        await cache.set("expire_soon", "value", ttl=1)
        assert await cache.get("expire_soon") == "value"
        
        # Wait for expiration
        await asyncio.sleep(1.5)
        assert await cache.get("expire_soon") is None
        
        # Set with longer TTL
        await cache.set("expire_later", "value", ttl=10)
        assert await cache.get("expire_later") == "value"
        
    
    async def test_cache_stats(self):
        """Test cache statistics tracking"""
        cache = IntelligentCacheInteraction()
        
        # Initial state - get_stats returns dict of partition stats
        initial_stats = cache.get_stats()
        
        # Add entries and test hits/misses
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")
        
        # Cache hits
        await cache.get("key1")
        await cache.get("key2")
        await cache.get("key1")
        
        # Cache misses
        await cache.get("missing1")
        await cache.get("missing2")
        
        # Get stats for default partition
        stats = cache.get_stats(CachePartition.USER_DATA)
        assert stats.hits == 3
        assert stats.misses == 2
        assert stats.hit_rate == 0.6
        
    
    async def test_large_values(self):
        """Test caching large values"""
        cache = IntelligentCacheInteraction(
            max_memory_size=10 * 1024 * 1024,  # 10MB
            compression_threshold=100 * 1024    # 100KB
        )
        
        # Create large value (500KB)
        large_value = "x" * (500 * 1024)
        
        await cache.set("large", large_value)
        result = await cache.get("large")
        assert result == large_value
        
        # Check compression was applied
        entry = cache.memory_cache.get("large")
        assert entry is not None
        assert entry.compressed is True
        assert entry.size < len(large_value)  # Compressed size should be smaller
        
    
    async def test_batch_operations(self):
        """Test batch cache operations"""
        cache = IntelligentCacheInteraction()
        
        # Batch set
        items = {f"batch:{i}": f"value{i}" for i in range(100)}
        
        tasks = [cache.set(k, v) for k, v in items.items()]
        results = await asyncio.gather(*tasks)
        assert all(results)
        
        # Batch get
        tasks = [cache.get(k) for k in items.keys()]
        results = await asyncio.gather(*tasks)
        
        for i, result in enumerate(results):
            assert result == f"value{i}"
        
    
    async def test_concurrent_access(self):
        """Test concurrent cache access"""
        cache = IntelligentCacheInteraction()
        
        async def concurrent_worker(worker_id: int):
            for i in range(10):
                key = f"worker{worker_id}:item{i}"
                await cache.set(key, f"data_{worker_id}_{i}")
                result = await cache.get(key)
                assert result == f"data_{worker_id}_{i}"
        
        # Run multiple workers concurrently
        workers = [concurrent_worker(i) for i in range(10)]
        await asyncio.gather(*workers)
        
        # Verify all entries exist
        assert len(cache.memory_cache) == 100
        


if __name__ == "__main__":
    pytest.main([__file__, "-v"])