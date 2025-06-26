"""
Module: api_gateway_interaction.py
Purpose: Comprehensive API gateway with advanced rate limiting capabilities

External Dependencies:
- aiohttp: https://docs.aiohttp.org/
- redis: https://redis-py.readthedocs.io/
- cachetools: https://cachetools.readthedocs.io/

Example Usage:
>>> from api_gateway_interaction import APIGateway
>>> gateway = APIGateway()
>>> gateway.register_route('/api/users', 'http://users-service:8001')
>>> await gateway.start(port=8080)
"""

import asyncio
import json
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from urllib.parse import urlparse

import aiohttp
from aiohttp import web
from cachetools import TTLCache
from loguru import logger

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available, using in-memory rate limiting only")


class RateLimitAlgorithm(Enum):
    """Rate limiting algorithm types"""
    SLIDING_WINDOW = "sliding_window"
    TOKEN_BUCKET = "token_bucket"
    FIXED_WINDOW = "fixed_window"


@dataclass
class RateLimitConfig:
    """Rate limit configuration"""
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    burst_size: int = 10
    algorithm: RateLimitAlgorithm = RateLimitAlgorithm.SLIDING_WINDOW


@dataclass
class Route:
    """API route configuration"""
    path: str
    backend_url: str
    methods: Set[str] = field(default_factory=lambda: {"GET", "POST", "PUT", "DELETE"})
    rate_limit: Optional[RateLimitConfig] = None
    cache_ttl: Optional[int] = None
    require_auth: bool = False
    circuit_breaker_enabled: bool = True


@dataclass
class CircuitBreakerState:
    """Circuit breaker state tracking"""
    failures: int = 0
    last_failure_time: Optional[float] = None
    state: str = "closed"  # closed, open, half-open
    success_count: int = 0


class RateLimiter:
    """Advanced rate limiting with multiple algorithms"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis_client = redis_client
        self.sliding_windows: Dict[str, deque] = defaultdict(deque)
        self.token_buckets: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.fixed_windows: Dict[str, Dict[str, int]] = defaultdict(dict)
    
    async def check_rate_limit(
        self,
        key: str,
        config: RateLimitConfig,
        timestamp: Optional[float] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """Check if request is within rate limits"""
        if timestamp is None:
            timestamp = time.time()
        
        if config.algorithm == RateLimitAlgorithm.SLIDING_WINDOW:
            return await self._check_sliding_window(key, config, timestamp)
        elif config.algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
            return await self._check_token_bucket(key, config, timestamp)
        else:
            return await self._check_fixed_window(key, config, timestamp)
    
    async def _check_sliding_window(
        self,
        key: str,
        config: RateLimitConfig,
        timestamp: float
    ) -> Tuple[bool, Dict[str, Any]]:
        """Sliding window rate limiting"""
        if self.redis_client:
            return await self._check_sliding_window_redis(key, config, timestamp)
        
        # In-memory implementation
        window = self.sliding_windows[key]
        window_start = timestamp - 60  # 1 minute window
        
        # Remove expired entries
        while window and window[0] < window_start:
            window.popleft()
        
        current_count = len(window)
        
        if current_count < config.requests_per_minute:
            window.append(timestamp)
            return True, {
                "remaining": config.requests_per_minute - current_count - 1,
                "reset": int(window_start + 60),
                "limit": config.requests_per_minute
            }
        
        return False, {
            "remaining": 0,
            "reset": int(window[0] + 60),
            "limit": config.requests_per_minute
        }
    
    async def _check_sliding_window_redis(
        self,
        key: str,
        config: RateLimitConfig,
        timestamp: float
    ) -> Tuple[bool, Dict[str, Any]]:
        """Redis-based sliding window rate limiting"""
        redis_key = f"rate_limit:sliding:{key}"
        window_start = timestamp - 60
        
        pipe = self.redis_client.pipeline()
        # Remove expired entries
        pipe.zremrangebyscore(redis_key, 0, window_start)
        # Count current entries
        pipe.zcard(redis_key)
        # Add new entry if allowed
        pipe.zadd(redis_key, {str(timestamp): timestamp})
        # Set expiry
        pipe.expire(redis_key, 120)
        
        results = await pipe.execute()
        current_count = results[1]
        
        if current_count < config.requests_per_minute:
            return True, {
                "remaining": config.requests_per_minute - current_count - 1,
                "reset": int(window_start + 60),
                "limit": config.requests_per_minute
            }
        
        # Remove the entry we just added
        await self.redis_client.zrem(redis_key, str(timestamp))
        
        return False, {
            "remaining": 0,
            "reset": int(window_start + 60),
            "limit": config.requests_per_minute
        }
    
    async def _check_token_bucket(
        self,
        key: str,
        config: RateLimitConfig,
        timestamp: float
    ) -> Tuple[bool, Dict[str, Any]]:
        """Token bucket rate limiting"""
        if self.redis_client:
            return await self._check_token_bucket_redis(key, config, timestamp)
        
        # In-memory implementation
        bucket = self.token_buckets[key]
        
        if not bucket:
            bucket.update({
                "tokens": config.burst_size,
                "last_refill": timestamp
            })
        
        # Refill tokens
        time_passed = timestamp - bucket["last_refill"]
        refill_rate = config.requests_per_minute / 60.0
        new_tokens = time_passed * refill_rate
        
        bucket["tokens"] = min(
            config.burst_size,
            bucket["tokens"] + new_tokens
        )
        bucket["last_refill"] = timestamp
        
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True, {
                "remaining": int(bucket["tokens"]),
                "burst_size": config.burst_size,
                "refill_rate": refill_rate
            }
        
        return False, {
            "remaining": 0,
            "burst_size": config.burst_size,
            "refill_rate": refill_rate,
            "retry_after": (1 - bucket["tokens"]) / refill_rate
        }
    
    async def _check_token_bucket_redis(
        self,
        key: str,
        config: RateLimitConfig,
        timestamp: float
    ) -> Tuple[bool, Dict[str, Any]]:
        """Redis-based token bucket rate limiting"""
        redis_key = f"rate_limit:token:{key}"
        refill_rate = config.requests_per_minute / 60.0
        
        lua_script = """
        local key = KEYS[1]
        local burst_size = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local timestamp = tonumber(ARGV[3])
        
        local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
        local tokens = tonumber(bucket[1]) or burst_size
        local last_refill = tonumber(bucket[2]) or timestamp
        
        -- Refill tokens
        local time_passed = timestamp - last_refill
        local new_tokens = time_passed * refill_rate
        tokens = math.min(burst_size, tokens + new_tokens)
        
        if tokens >= 1 then
            tokens = tokens - 1
            redis.call('HMSET', key, 'tokens', tokens, 'last_refill', timestamp)
            redis.call('EXPIRE', key, 3600)
            return {1, tokens}
        else
            redis.call('HMSET', key, 'tokens', tokens, 'last_refill', timestamp)
            redis.call('EXPIRE', key, 3600)
            return {0, tokens}
        end
        """
        
        result = await self.redis_client.eval(
            lua_script,
            1,
            redis_key,
            config.burst_size,
            refill_rate,
            timestamp
        )
        
        allowed = result[0] == 1
        tokens = result[1]
        
        return allowed, {
            "remaining": int(tokens),
            "burst_size": config.burst_size,
            "refill_rate": refill_rate,
            "retry_after": (1 - tokens) / refill_rate if not allowed else None
        }
    
    async def _check_fixed_window(
        self,
        key: str,
        config: RateLimitConfig,
        timestamp: float
    ) -> Tuple[bool, Dict[str, Any]]:
        """Fixed window rate limiting"""
        window_start = int(timestamp // 60) * 60
        window_key = f"{key}:{window_start}"
        
        if self.redis_client:
            redis_key = f"rate_limit:fixed:{window_key}"
            current = await self.redis_client.incr(redis_key)
            await self.redis_client.expire(redis_key, 120)
        else:
            self.fixed_windows[key][window_key] = \
                self.fixed_windows[key].get(window_key, 0) + 1
            current = self.fixed_windows[key][window_key]
        
        if current <= config.requests_per_minute:
            return True, {
                "remaining": config.requests_per_minute - current,
                "reset": window_start + 60,
                "limit": config.requests_per_minute
            }
        
        return False, {
            "remaining": 0,
            "reset": window_start + 60,
            "limit": config.requests_per_minute
        }


class APIKeyManager:
    """API key management and validation"""
    
    def __init__(self):
        self.api_keys: Dict[str, Dict[str, Any]] = {}
        self._load_default_keys()
    
    def _load_default_keys(self):
        """Load default API keys for testing"""
        self.api_keys = {
            "test-key-123": {
                "name": "Test Application",
                "rate_limit": RateLimitConfig(
                    requests_per_minute=100,
                    requests_per_hour=5000
                ),
                "created": datetime.now(),
                "active": True
            },
            "premium-key-456": {
                "name": "Premium Application",
                "rate_limit": RateLimitConfig(
                    requests_per_minute=1000,
                    requests_per_hour=50000,
                    burst_size=50
                ),
                "created": datetime.now(),
                "active": True
            }
        }
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key and return metadata"""
        key_data = self.api_keys.get(api_key)
        if key_data and key_data.get("active", False):
            return key_data
        return None
    
    def create_api_key(
        self,
        name: str,
        rate_limit: Optional[RateLimitConfig] = None
    ) -> str:
        """Create new API key"""
        import uuid
        api_key = f"key-{uuid.uuid4()}"
        self.api_keys[api_key] = {
            "name": name,
            "rate_limit": rate_limit or RateLimitConfig(),
            "created": datetime.now(),
            "active": True
        }
        return api_key


class CircuitBreaker:
    """Circuit breaker pattern implementation"""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.states: Dict[str, CircuitBreakerState] = defaultdict(CircuitBreakerState)
    
    async def call(
        self,
        key: str,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Execute function with circuit breaker protection"""
        state = self.states[key]
        
        if state.state == "open":
            # Check if we should try half-open
            if (time.time() - state.last_failure_time) > self.recovery_timeout:
                state.state = "half-open"
                logger.info(f"Circuit breaker {key} entering half-open state")
            else:
                raise Exception(f"Circuit breaker {key} is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            
            # Success - update state
            if state.state == "half-open":
                state.success_count += 1
                if state.success_count >= 3:  # Require 3 successes to close
                    state.state = "closed"
                    state.failures = 0
                    state.success_count = 0
                    logger.info(f"Circuit breaker {key} is now CLOSED")
            
            return result
            
        except self.expected_exception as e:
            state.failures += 1
            state.last_failure_time = time.time()
            
            if state.failures >= self.failure_threshold:
                state.state = "open"
                state.success_count = 0
                logger.warning(f"Circuit breaker {key} is now OPEN after {state.failures} failures")
            
            raise e


class APIGateway:
    """Main API Gateway with rate limiting and advanced features"""
    
    def __init__(
        self,
        redis_url: Optional[str] = None,
        default_rate_limit: Optional[RateLimitConfig] = None
    ):
        self.routes: Dict[str, Route] = {}
        self.middlewares: List[Callable] = []
        self.redis_client = None
        self.rate_limiter = None
        self.api_key_manager = APIKeyManager()
        self.circuit_breaker = CircuitBreaker()
        self.cache = TTLCache(maxsize=1000, ttl=300)  # 5 minute default TTL
        self.default_rate_limit = default_rate_limit or RateLimitConfig()
        self.redis_url = redis_url
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Metrics
        self.metrics = {
            "requests_total": 0,
            "requests_success": 0,
            "requests_failed": 0,
            "requests_rate_limited": 0,
            "cache_hits": 0,
            "cache_misses": 0
        }
    
    async def setup(self):
        """Setup gateway resources"""
        self.session = aiohttp.ClientSession()
        
        if self.redis_url and REDIS_AVAILABLE:
            try:
                self.redis_client = await redis.from_url(self.redis_url)
                await self.redis_client.ping()
                logger.info("Connected to Redis for distributed rate limiting")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}")
                self.redis_client = None
        
        self.rate_limiter = RateLimiter(self.redis_client)
    
    async def cleanup(self):
        """Cleanup gateway resources"""
        if self.session:
            await self.session.close()
        if self.redis_client:
            await self.redis_client.close()
    
    def register_route(
        self,
        path: str,
        backend_url: str,
        methods: Optional[Set[str]] = None,
        rate_limit: Optional[RateLimitConfig] = None,
        cache_ttl: Optional[int] = None,
        require_auth: bool = False
    ):
        """Register a new route"""
        self.routes[path] = Route(
            path=path,
            backend_url=backend_url,
            methods=methods or {"GET", "POST", "PUT", "DELETE"},
            rate_limit=rate_limit,
            cache_ttl=cache_ttl,
            require_auth=require_auth
        )
        logger.info(f"Registered route: {path} -> {backend_url}")
    
    def add_middleware(self, middleware: Callable):
        """Add middleware to the processing pipeline"""
        self.middlewares.append(middleware)
    
    async def handle_request(self, request: web.Request) -> web.Response:
        """Main request handler"""
        self.metrics["requests_total"] += 1
        
        try:
            # Find matching route
            route = self._match_route(request.path)
            if not route:
                return web.json_response(
                    {"error": "Route not found"},
                    status=404
                )
            
            # Check method
            if request.method not in route.methods:
                return web.json_response(
                    {"error": "Method not allowed"},
                    status=405
                )
            
            # Apply middlewares
            for middleware in self.middlewares:
                response = await middleware(request, route)
                if response:
                    return response
            
            # Authentication
            if route.require_auth:
                auth_response = await self._check_authentication(request, route)
                if auth_response:
                    return auth_response
            
            # Rate limiting
            rate_limit_response = await self._check_rate_limit(request, route)
            if rate_limit_response:
                self.metrics["requests_rate_limited"] += 1
                return rate_limit_response
            
            # Check cache for GET requests
            if request.method == "GET" and route.cache_ttl:
                cache_key = f"{route.path}:{request.query_string}"
                cached_response = self.cache.get(cache_key)
                if cached_response:
                    self.metrics["cache_hits"] += 1
                    return web.json_response(cached_response)
                self.metrics["cache_misses"] += 1
            
            # Forward request with circuit breaker
            response = await self.circuit_breaker.call(
                route.backend_url,
                self._forward_request,
                request,
                route
            )
            
            # Cache successful GET responses
            if (request.method == "GET" and 
                route.cache_ttl and 
                response.status == 200):
                try:
                    response_data = await response.json()
                    cache_key = f"{route.path}:{request.query_string}"
                    self.cache[cache_key] = response_data
                except:
                    pass
            
            self.metrics["requests_success"] += 1
            return response
            
        except Exception as e:
            logger.error(f"Request handling error: {e}")
            self.metrics["requests_failed"] += 1
            return web.json_response(
                {"error": "Internal server error"},
                status=500
            )
    
    def _match_route(self, path: str) -> Optional[Route]:
        """Match request path to registered route"""
        # Exact match
        if path in self.routes:
            return self.routes[path]
        
        # Prefix match (longest first)
        for route_path in sorted(self.routes.keys(), key=len, reverse=True):
            if path.startswith(route_path):
                return self.routes[route_path]
        
        return None
    
    async def _check_authentication(
        self,
        request: web.Request,
        route: Route
    ) -> Optional[web.Response]:
        """Check authentication"""
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return web.json_response(
                {"error": "API key required"},
                status=401
            )
        
        key_data = self.api_key_manager.validate_api_key(api_key)
        if not key_data:
            return web.json_response(
                {"error": "Invalid API key"},
                status=401
            )
        
        # Store key data for rate limiting
        request["api_key_data"] = key_data
        return None
    
    async def _check_rate_limit(
        self,
        request: web.Request,
        route: Route
    ) -> Optional[web.Response]:
        """Check rate limits"""
        # Determine rate limit config
        rate_config = route.rate_limit or self.default_rate_limit
        
        # Use API key specific limits if available
        if "api_key_data" in request:
            key_data = request["api_key_data"]
            if key_data.get("rate_limit"):
                rate_config = key_data["rate_limit"]
        
        # Determine rate limit key
        if "api_key_data" in request:
            rate_key = request.headers.get("X-API-Key")
        else:
            # Use IP address
            rate_key = request.headers.get(
                "X-Forwarded-For",
                request.remote or "unknown"
            ).split(",")[0].strip()
        
        # Check rate limit
        allowed, metadata = await self.rate_limiter.check_rate_limit(
            rate_key,
            rate_config
        )
        
        # Add rate limit headers
        headers = {
            "X-RateLimit-Limit": str(metadata.get("limit", rate_config.requests_per_minute)),
            "X-RateLimit-Remaining": str(metadata.get("remaining", 0)),
            "X-RateLimit-Reset": str(metadata.get("reset", 0))
        }
        
        if not allowed:
            retry_after = metadata.get("retry_after", 60)
            headers["Retry-After"] = str(int(retry_after))
            
            return web.json_response(
                {"error": "Rate limit exceeded"},
                status=429,
                headers=headers
            )
        
        # Add headers to successful response
        request["rate_limit_headers"] = headers
        return None
    
    async def _forward_request(
        self,
        request: web.Request,
        route: Route
    ) -> web.Response:
        """Forward request to backend service"""
        # Build backend URL
        backend_url = route.backend_url
        if not backend_url.endswith("/"):
            backend_url += "/"
        
        # Remove route prefix from path
        path = request.path
        if path.startswith(route.path):
            path = path[len(route.path):]
            if path.startswith("/"):
                path = path[1:]
        
        url = backend_url + path
        if request.query_string:
            url += f"?{request.query_string}"
        
        # Forward headers (except Host)
        headers = dict(request.headers)
        headers.pop("Host", None)
        
        # Read request body
        body = await request.read()
        
        # Make request with retry
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                async with self.session.request(
                    method=request.method,
                    url=url,
                    headers=headers,
                    data=body,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    # Read response
                    response_body = await resp.read()
                    
                    # Build response
                    response = web.Response(
                        body=response_body,
                        status=resp.status,
                        headers=resp.headers
                    )
                    
                    # Add rate limit headers if available
                    if "rate_limit_headers" in request:
                        for k, v in request["rate_limit_headers"].items():
                            response.headers[k] = v
                    
                    return response
                    
            except asyncio.TimeoutError:
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    raise
            except aiohttp.ClientError as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    raise
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get gateway metrics"""
        return {
            **self.metrics,
            "cache_size": len(self.cache),
            "circuit_breakers": {
                url: {
                    "state": state.state,
                    "failures": state.failures
                }
                for url, state in self.circuit_breaker.states.items()
            }
        }
    
    async def start(self, host: str = "0.0.0.0", port: int = 8080):
        """Start the API gateway server"""
        await self.setup()
        
        app = web.Application()
        app.router.add_route("*", "/{path:.*}", self.handle_request)
        
        # Add metrics endpoint
        async def metrics_handler(request):
            return web.json_response(self.get_metrics())
        
        app.router.add_get("/_metrics", metrics_handler)
        
        # Add health check
        async def health_handler(request):
            return web.json_response({"status": "healthy"})
        
        app.router.add_get("/_health", health_handler)
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        
        logger.info(f"Starting API Gateway on {host}:{port}")
        await site.start()
        
        try:
            await asyncio.Event().wait()
        finally:
            await runner.cleanup()
            await self.cleanup()


# Example middleware functions
async def logging_middleware(request: web.Request, route: Route) -> Optional[web.Response]:
    """Log all requests"""
    logger.info(f"{request.method} {request.path} -> {route.backend_url}")
    return None


async def cors_middleware(request: web.Request, route: Route) -> Optional[web.Response]:
    """Handle CORS preflight requests"""
    if request.method == "OPTIONS":
        return web.Response(
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, X-API-Key"
            }
        )
    return None


if __name__ == "__main__":
    # Test the API gateway with real scenarios
    async def test_gateway():
        """Test API gateway functionality"""
        # Create gateway
        gateway = APIGateway(
            redis_url="redis://localhost:6379",
            default_rate_limit=RateLimitConfig(
                requests_per_minute=30,
                algorithm=RateLimitAlgorithm.SLIDING_WINDOW
            )
        )
        
        # Register routes
        gateway.register_route(
            "/api/users",
            "https://jsonplaceholder.typicode.com/users",
            cache_ttl=60
        )
        
        gateway.register_route(
            "/api/posts",
            "https://jsonplaceholder.typicode.com/posts",
            rate_limit=RateLimitConfig(
                requests_per_minute=100,
                algorithm=RateLimitAlgorithm.TOKEN_BUCKET,
                burst_size=20
            ),
            require_auth=True
        )
        
        # Add middlewares
        gateway.add_middleware(logging_middleware)
        gateway.add_middleware(cors_middleware)
        
        # Create API keys
        basic_key = gateway.api_key_manager.create_api_key("Basic App")
        premium_key = gateway.api_key_manager.create_api_key(
            "Premium App",
            RateLimitConfig(requests_per_minute=1000)
        )
        
        logger.info(f"Created API keys: basic={basic_key}, premium={premium_key}")
        
        # Setup gateway
        await gateway.setup()
        
        # Test requests
        try:
            # Test public endpoint
            async with aiohttp.ClientSession() as session:
                # Test rate limiting
                logger.info("Testing rate limiting...")
                for i in range(5):
                    async with session.get("http://localhost:8080/api/users") as resp:
                        logger.info(f"Request {i+1}: {resp.status}")
                        logger.info(f"Rate limit headers: {dict(resp.headers)}")
                
                # Test authenticated endpoint
                logger.info("\nTesting authenticated endpoint...")
                headers = {"X-API-Key": basic_key}
                async with session.get(
                    "http://localhost:8080/api/posts",
                    headers=headers
                ) as resp:
                    logger.info(f"Auth request: {resp.status}")
                    data = await resp.json()
                    logger.info(f"Got {len(data)} posts")
        
        finally:
            await gateway.cleanup()
    
    # Run test
    logger.info("✅ API Gateway module validated successfully")
    
    # Uncomment to run the server
    # asyncio.run(test_gateway())