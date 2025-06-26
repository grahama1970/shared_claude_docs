# Intelligent Cache Manager

A sophisticated multi-level caching system with advanced features including adaptive eviction policies, distributed cache coherence, and intelligent prefetching.

## Features

### Multi-Level Cache Architecture
- **L1 (Memory)**: Ultra-fast in-memory cache with configurable size limits
- **L2 (Disk)**: Persistent disk-based cache for larger datasets  
- **L3 (Distributed)**: Redis-based distributed cache for multi-instance deployments

### Advanced Eviction Policies
- **LRU (Least Recently Used)**: Classic eviction based on access recency
- **LFU (Least Frequently Used)**: Eviction based on access frequency
- **Adaptive**: Intelligent eviction using multiple factors:
  - Access recency and frequency
  - Entry size considerations
  - Access pattern regularity
  - TTL proximity

### Key Features
- **Compression**: Automatic compression for large values with configurable thresholds
- **TTL Support**: Time-to-live for automatic expiration
- **Multi-tenant Isolation**: Separate cache spaces for different tenants
- **Pattern Invalidation**: Regex-based cache invalidation
- **Cache Warming**: Preload cache with critical data
- **Predictive Prefetching**: Analyze miss patterns to prefetch related data
- **Real-time Analytics**: Detailed statistics and performance metrics
- **Concurrent Access**: Thread-safe operations with async support

## Installation

```bash
# Install dependencies
uv add aiofiles redis diskcache loguru lz4

# For distributed caching, ensure Redis is running:
# docker run -d -p 6379:6379 redis:alpine
```

## Quick Start

```python
import asyncio
from intelligent_cache_interaction import IntelligentCacheInteraction, CacheConfig, EvictionPolicy

async def main():
    # Configure cache
    config = CacheConfig(
        l1_size_mb=100,          # 100MB memory cache
        l2_size_mb=1000,         # 1GB disk cache
        l3_enabled=True,         # Enable Redis
        redis_url="redis://localhost:6379",
        eviction_policy=EvictionPolicy.ADAPTIVE,
        enable_compression=True,
        default_ttl_seconds=3600  # 1 hour default TTL
    )
    
    # Initialize cache
    cache = IntelligentCacheInteraction(config)
    await cache.initialize()
    
    # Store data
    await cache.set("user:123", {
        "name": "Alice",
        "email": "alice@example.com",
        "preferences": {"theme": "dark"}
    })
    
    # Retrieve data
    user = await cache.get("user:123")
    print(f"Retrieved: {user}")
    
    # Set with custom TTL
    await cache.set("session:abc", {"token": "xyz"}, ttl=300)  # 5 minutes
    
    # Pattern invalidation
    await cache.invalidate_pattern(r"user:.*")  # Clear all user cache
    
    # Get statistics
    stats = cache.get_stats()
    print(f"Cache hit rate: {stats.hit_rate:.2%}")
    
    # Detailed statistics
    detailed = await cache.get_detailed_stats()
    print(f"L1 size: {detailed['level_stats']['l1_size_mb']:.2f}MB")
    
    await cache.close()

asyncio.run(main())
```

## Advanced Usage

### Multi-Tenant Caching

```python
# Enable multi-tenant mode
config = CacheConfig(multi_tenant=True)
cache = IntelligentCacheInteraction(config)
await cache.initialize()

# Store tenant-specific data
await cache.set("config:db", "tenant1_db", tenant_id="tenant1")
await cache.set("config:db", "tenant2_db", tenant_id="tenant2")

# Retrieve tenant-specific data
db1 = await cache.get("config:db", tenant_id="tenant1")  # "tenant1_db"
db2 = await cache.get("config:db", tenant_id="tenant2")  # "tenant2_db"

# Clear specific tenant cache
await cache.clear(tenant_id="tenant1")
```

### Cache Warming

```python
# Define data loader
async def load_user_data(user_id: str):
    # Simulate database fetch
    return {"id": user_id, "name": f"User {user_id}"}

# Warm cache with user data
user_ids = ["user:1", "user:2", "user:3"]
await cache.warm_cache(user_ids, load_user_data)
```

### Custom Eviction Policies

The adaptive eviction policy considers multiple factors:

```python
# Configure adaptive eviction
config = CacheConfig(
    l1_size_mb=50,
    eviction_policy=EvictionPolicy.ADAPTIVE
)

# The adaptive policy will:
# - Keep frequently accessed items
# - Prefer evicting large, rarely-used items
# - Consider access pattern regularity
# - Factor in remaining TTL
```

### Compression Settings

```python
config = CacheConfig(
    enable_compression=True,
    compression_threshold_kb=10  # Compress items > 10KB
)

# Large items will be automatically compressed
large_data = {"data": ["item"] * 10000}
await cache.set("large", large_data)  # Automatically compressed
```

## Performance Optimization

### 1. Choose the Right Eviction Policy
- **LRU**: Best for general-purpose caching with temporal locality
- **LFU**: Ideal when certain items are consistently popular
- **Adaptive**: Best for mixed workloads with varying access patterns

### 2. Size Your Cache Levels Appropriately
```python
config = CacheConfig(
    l1_size_mb=100,    # Fast but limited
    l2_size_mb=10000,  # Larger persistent storage
    l3_enabled=True    # Distributed for scaling
)
```

### 3. Use Pattern Invalidation Wisely
```python
# Invalidate specific patterns instead of clearing entire cache
await cache.invalidate_pattern(r"api:v1:users:.*")  # Only user data
```

### 4. Monitor Cache Performance
```python
# Regular monitoring
stats = await cache.get_detailed_stats()
if stats["basic_stats"]["hit_rate"] < 0.8:
    # Consider increasing cache size or adjusting eviction policy
    pass
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest project_interactions/intelligent_cache/tests/ -v

# Run specific test category
pytest project_interactions/intelligent_cache/tests/test_cache_operations.py -v
pytest project_interactions/intelligent_cache/tests/test_eviction_policies.py -v
pytest project_interactions/intelligent_cache/tests/test_distributed_cache.py -v
```

## Architecture

```
┌─────────────────┐
│   Application   │
└────────┬────────┘
         │
┌────────▼────────┐
│   L1: Memory    │ ← Fast, Limited Size
│  (OrderedDict)  │
└────────┬────────┘
         │ Eviction/Demotion
┌────────▼────────┐
│    L2: Disk    │ ← Larger, Persistent
│  (DiskCache)   │
└────────┬────────┘
         │ Write-through
┌────────▼────────┐
│ L3: Distributed │ ← Scalable, Shared
│    (Redis)      │
└─────────────────┘
```

## Configuration Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `l1_size_mb` | int | 100 | L1 memory cache size in MB |
| `l2_size_mb` | int | 1000 | L2 disk cache size in MB |
| `l3_enabled` | bool | False | Enable Redis distributed cache |
| `redis_url` | str | None | Redis connection URL |
| `eviction_policy` | EvictionPolicy | LRU | Cache eviction strategy |
| `enable_compression` | bool | True | Enable automatic compression |
| `compression_threshold_kb` | int | 1 | Minimum size for compression |
| `default_ttl_seconds` | float | None | Default TTL for entries |
| `cache_warming_enabled` | bool | True | Enable cache warming |
| `prefetch_enabled` | bool | True | Enable predictive prefetching |
| `multi_tenant` | bool | False | Enable multi-tenant isolation |
| `cache_dir` | Path | ./cache_data | Directory for disk cache |

## Best Practices

1. **Start with conservative cache sizes** and increase based on monitoring
2. **Use TTLs** for time-sensitive data to prevent stale cache
3. **Enable compression** for large text/JSON data
4. **Monitor hit rates** and adjust configuration accordingly
5. **Use pattern invalidation** instead of clearing entire cache
6. **Implement cache warming** for critical data after restarts
7. **Consider multi-tenant mode** for SaaS applications

## License

MIT