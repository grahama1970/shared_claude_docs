# API Gateway with Advanced Rate Limiting

A comprehensive API gateway implementation with multiple rate limiting algorithms, circuit breaker pattern, and advanced features.

## Features

### Core Gateway Features
- **Route Registration**: Dynamic route configuration with path prefix matching
- **Request Forwarding**: Proxy requests to backend services with retry logic
- **Method Filtering**: Control allowed HTTP methods per route
- **Health Checks**: Built-in health and metrics endpoints

### Rate Limiting Algorithms
1. **Sliding Window**: Smooth rate limiting over time windows
2. **Token Bucket**: Burst capacity with steady refill rate
3. **Fixed Window**: Traditional window-based limiting

### Advanced Features
- **Distributed Rate Limiting**: Redis support for multi-instance deployments
- **API Key Management**: Create and validate API keys with custom limits
- **Circuit Breaker**: Automatic failure detection and recovery
- **Response Caching**: TTL-based caching for GET requests
- **Middleware Pipeline**: Extensible request/response processing
- **Metrics Collection**: Comprehensive request and performance metrics

## Installation

```bash
# Install dependencies
uv add aiohttp redis cachetools loguru

# For tests
uv add --dev pytest pytest-asyncio freezegun
```

## Quick Start

```python
from api_gateway_interaction import APIGateway, RateLimitConfig, RateLimitAlgorithm

# Create gateway
gateway = APIGateway(
    redis_url="redis://localhost:6379",
    default_rate_limit=RateLimitConfig(
        requests_per_minute=60,
        algorithm=RateLimitAlgorithm.SLIDING_WINDOW
    )
)

# Register routes
gateway.register_route(
    "/api/users",
    "http://users-service:8001",
    cache_ttl=300,  # 5 minute cache
    require_auth=True
)

# Start gateway
await gateway.start(port=8080)
```

## Rate Limiting Configuration

### Sliding Window
```python
config = RateLimitConfig(
    requests_per_minute=100,
    algorithm=RateLimitAlgorithm.SLIDING_WINDOW
)
```

### Token Bucket (with burst)
```python
config = RateLimitConfig(
    requests_per_minute=60,
    burst_size=20,
    algorithm=RateLimitAlgorithm.TOKEN_BUCKET
)
```

### Fixed Window
```python
config = RateLimitConfig(
    requests_per_minute=1000,
    algorithm=RateLimitAlgorithm.FIXED_WINDOW
)
```

## API Key Management

```python
# Create API keys
basic_key = gateway.api_key_manager.create_api_key("Basic App")
premium_key = gateway.api_key_manager.create_api_key(
    "Premium App",
    RateLimitConfig(requests_per_minute=1000)
)

# Use in requests
headers = {"X-API-Key": premium_key}
```

## Middleware

### Built-in Middleware
- `logging_middleware`: Logs all requests
- `cors_middleware`: Handles CORS preflight

### Custom Middleware
```python
async def auth_middleware(request, route):
    if not request.headers.get("Authorization"):
        return web.json_response({"error": "Unauthorized"}, status=401)
    return None  # Continue processing

gateway.add_middleware(auth_middleware)
```

## Circuit Breaker

Automatically configured per backend URL:
- Opens after 5 consecutive failures
- Enters half-open state after 60 seconds
- Requires 3 successful requests to close

## Metrics

Access metrics at `/_metrics`:
```json
{
    "requests_total": 1000,
    "requests_success": 950,
    "requests_failed": 30,
    "requests_rate_limited": 20,
    "cache_hits": 100,
    "cache_misses": 200,
    "cache_size": 45,
    "circuit_breakers": {
        "http://backend:8001": {
            "state": "closed",
            "failures": 0
        }
    }
}
```

## Response Headers

Rate limit information in response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 75
X-RateLimit-Reset: 1640995200
Retry-After: 60  # When rate limited
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_rate_limiting.py -v

# Run verification script
python test_task_33.py
```

## Architecture

```
Client Request
     |
     v
[Middleware Pipeline]
     |
     v
[Authentication]
     |
     v
[Rate Limiting]
     |
     v
[Cache Check]
     |
     v
[Circuit Breaker]
     |
     v
[Backend Forward]
     |
     v
[Response Cache]
     |
     v
Client Response
```

## Performance Considerations

- **In-Memory Rate Limiting**: Fast but limited to single instance
- **Redis Rate Limiting**: Distributed but adds network latency
- **Caching**: Reduces backend load for GET requests
- **Circuit Breaker**: Prevents cascading failures
- **Connection Pooling**: Reuses HTTP connections

## Error Handling

- **404**: Route not found
- **405**: Method not allowed
- **401**: Authentication required or invalid API key
- **429**: Rate limit exceeded
- **500**: Internal server error or backend failure
- **503**: Circuit breaker open

## Advanced Usage

### Multiple Rate Limits
```python
# Per-route limits
gateway.register_route(
    "/api/expensive",
    "http://backend:8001",
    rate_limit=RateLimitConfig(
        requests_per_minute=10,
        requests_per_hour=100
    )
)
```

### Custom Circuit Breaker
```python
from api_gateway_interaction import CircuitBreaker

custom_cb = CircuitBreaker(
    failure_threshold=10,
    recovery_timeout=120,
    expected_exception=aiohttp.ClientError
)
```

### Redis Configuration
```python
gateway = APIGateway(
    redis_url="redis://username:password@redis-server:6379/0"
)
```

## License

MIT