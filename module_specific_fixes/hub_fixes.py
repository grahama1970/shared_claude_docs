#!/usr/bin/env python3
"""
Module: hub_fixes.py
Description: Granger Hub-specific bug fixes implementation

External Dependencies:
- granger_common: Our standardized components
"""

from pathlib import Path
import re

def apply_hub_fixes():
    """Apply all Granger Hub-specific fixes."""
    print("\n🎯 Applying Granger Hub fixes...")
    
    # 1. Fix buffer overflow with bounded queue
    bounded_queue_code = '''
from collections import deque
from threading import Lock, Event
from typing import Any, Optional
import time

class BoundedMessageQueue:
    """Thread-safe bounded message queue with backpressure."""
    
    def __init__(self, max_size: int = 10000, name: str = "default"):
        self.queue = deque(maxlen=max_size)
        self.lock = Lock()
        self.dropped_count = 0
        self.name = name
        self.not_full = Event()
        self.not_full.set()  # Initially not full
        
    def put(self, message: Any, timeout: Optional[float] = None) -> bool:
        """Add message to queue with optional timeout."""
        start_time = time.time()
        
        while True:
            with self.lock:
                if len(self.queue) < self.queue.maxlen:
                    self.queue.append(message)
                    return True
                else:
                    self.dropped_count += 1
                    
            # Wait for space if timeout allows
            if timeout is not None:
                elapsed = time.time() - start_time
                remaining = timeout - elapsed
                if remaining <= 0:
                    return False
                    
                if not self.not_full.wait(min(remaining, 0.1)):
                    continue
            else:
                return False
    
    def get(self, timeout: Optional[float] = None) -> Optional[Any]:
        """Get message from queue with optional timeout."""
        with self.lock:
            if self.queue:
                message = self.queue.popleft()
                if len(self.queue) < self.queue.maxlen:
                    self.not_full.set()
                return message
        return None
    
    def size(self) -> int:
        """Get current queue size."""
        with self.lock:
            return len(self.queue)
    
    def stats(self) -> dict:
        """Get queue statistics."""
        with self.lock:
            return {
                "name": self.name,
                "size": len(self.queue),
                "max_size": self.queue.maxlen,
                "dropped": self.dropped_count,
                "utilization": f"{(len(self.queue) / self.queue.maxlen * 100):.1f}%"
            }
'''
    
    # 2. Implement circuit breaker pattern
    circuit_breaker_code = '''
from enum import Enum
from datetime import datetime, timedelta
from threading import Lock
from typing import Callable, Any, Optional
import asyncio

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject calls
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    """Circuit breaker pattern for fault tolerance."""
    
    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self.lock = Lock()
        self.success_count = 0
        self.total_calls = 0
    
    async def call_async(self, func: Callable, *args, **kwargs) -> Any:
        """Execute async function with circuit breaker protection."""
        with self.lock:
            self.total_calls += 1
            
            if self.state == CircuitState.OPEN:
                if datetime.now() - self.last_failure_time > timedelta(seconds=self.recovery_timeout):
                    self.state = CircuitState.HALF_OPEN
                    logger.info(f"Circuit breaker {self.name} entering HALF_OPEN state")
                else:
                    raise RuntimeError(f"Circuit breaker {self.name} is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def call_sync(self, func: Callable, *args, **kwargs) -> Any:
        """Execute sync function with circuit breaker protection."""
        with self.lock:
            self.total_calls += 1
            
            if self.state == CircuitState.OPEN:
                if datetime.now() - self.last_failure_time > timedelta(seconds=self.recovery_timeout):
                    self.state = CircuitState.HALF_OPEN
                    logger.info(f"Circuit breaker {self.name} entering HALF_OPEN state")
                else:
                    raise RuntimeError(f"Circuit breaker {self.name} is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Handle successful call."""
        with self.lock:
            self.success_count += 1
            
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                logger.info(f"Circuit breaker {self.name} recovered to CLOSED state")
    
    def _on_failure(self):
        """Handle failed call."""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                logger.error(f"Circuit breaker {self.name} opened after {self.failure_count} failures")
    
    def stats(self) -> dict:
        """Get circuit breaker statistics."""
        with self.lock:
            return {
                "name": self.name,
                "state": self.state.value,
                "failure_count": self.failure_count,
                "success_count": self.success_count,
                "total_calls": self.total_calls,
                "success_rate": f"{(self.success_count / self.total_calls * 100):.1f}%" if self.total_calls > 0 else "0%"
            }
'''
    
    # 3. Add connection pooling and management
    connection_pool_code = '''
from asyncio import Queue, create_task, sleep
from typing import Dict, Optional
import aiohttp

class ConnectionPool:
    """Manage connections to spoke modules efficiently."""
    
    def __init__(self, max_connections_per_host: int = 10):
        self.max_connections_per_host = max_connections_per_host
        self.pools: Dict[str, Queue] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        
    async def get_session(self, module_url: str) -> aiohttp.ClientSession:
        """Get or create session for module."""
        if module_url not in self.pools:
            self.pools[module_url] = Queue(maxsize=self.max_connections_per_host)
            self.circuit_breakers[module_url] = CircuitBreaker(
                name=f"cb_{module_url}",
                failure_threshold=5,
                recovery_timeout=30
            )
            
            # Pre-populate pool
            for _ in range(self.max_connections_per_host):
                session = aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(limit=1),
                    timeout=aiohttp.ClientTimeout(total=30)
                )
                await self.pools[module_url].put(session)
        
        # Get session from pool
        session = await self.pools[module_url].get()
        return session
    
    async def return_session(self, module_url: str, session: aiohttp.ClientSession):
        """Return session to pool."""
        if module_url in self.pools:
            await self.pools[module_url].put(session)
    
    async def close_all(self):
        """Close all sessions in all pools."""
        for url, pool in self.pools.items():
            while not pool.empty():
                session = await pool.get()
                await session.close()
'''
    
    # 4. Add health monitoring
    health_monitoring_code = '''
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

@dataclass
class ModuleHealth:
    """Health status of a spoke module."""
    module_name: str
    url: str
    is_healthy: bool
    last_check: datetime
    response_time_ms: Optional[float] = None
    error: Optional[str] = None
    consecutive_failures: int = 0

class HealthMonitor:
    """Monitor health of all spoke modules."""
    
    def __init__(self, check_interval: int = 30):
        self.check_interval = check_interval
        self.module_health: Dict[str, ModuleHealth] = {}
        self.running = False
        
    async def start_monitoring(self, modules: Dict[str, str]):
        """Start health monitoring for modules."""
        self.running = True
        
        # Initialize health records
        for name, url in modules.items():
            self.module_health[name] = ModuleHealth(
                module_name=name,
                url=url,
                is_healthy=True,
                last_check=datetime.now()
            )
        
        # Start monitoring task
        create_task(self._monitor_loop())
    
    async def _monitor_loop(self):
        """Main monitoring loop."""
        while self.running:
            for name, health in self.module_health.items():
                create_task(self._check_module_health(name))
            
            await sleep(self.check_interval)
    
    async def _check_module_health(self, module_name: str):
        """Check health of a single module."""
        health = self.module_health[module_name]
        
        try:
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{health.url}/health", timeout=5) as response:
                    response_time = (time.time() - start_time) * 1000
                    
                    if response.status == 200:
                        health.is_healthy = True
                        health.response_time_ms = response_time
                        health.consecutive_failures = 0
                        health.error = None
                    else:
                        health.is_healthy = False
                        health.consecutive_failures += 1
                        health.error = f"HTTP {response.status}"
                        
        except Exception as e:
            health.is_healthy = False
            health.consecutive_failures += 1
            health.error = str(e)
        
        health.last_check = datetime.now()
        
        # Log if state changed
        if health.consecutive_failures == 1:
            logger.warning(f"Module {module_name} became unhealthy: {health.error}")
        elif health.consecutive_failures == 0 and not health.is_healthy:
            logger.info(f"Module {module_name} recovered")
    
    def get_health_summary(self) -> dict:
        """Get summary of all module health."""
        healthy_count = sum(1 for h in self.module_health.values() if h.is_healthy)
        total_count = len(self.module_health)
        
        return {
            "healthy_modules": healthy_count,
            "total_modules": total_count,
            "health_percentage": f"{(healthy_count / total_count * 100):.1f}%" if total_count > 0 else "0%",
            "modules": {
                name: {
                    "healthy": health.is_healthy,
                    "response_time_ms": health.response_time_ms,
                    "consecutive_failures": health.consecutive_failures,
                    "last_check": health.last_check.isoformat()
                }
                for name, health in self.module_health.items()
            }
        }
'''
    
    # 5. Add request routing with load balancing
    load_balancing_code = '''
from collections import defaultdict
import random

class RequestRouter:
    """Route requests to healthy modules with load balancing."""
    
    def __init__(self, health_monitor: HealthMonitor):
        self.health_monitor = health_monitor
        self.request_counts = defaultdict(int)
        
    def get_best_module(self, module_type: str) -> Optional[str]:
        """Get best available module for request."""
        # Get all healthy modules of this type
        healthy_modules = [
            name for name, health in self.health_monitor.module_health.items()
            if health.is_healthy and name.startswith(module_type)
        ]
        
        if not healthy_modules:
            return None
        
        # Simple round-robin with least connections
        module_loads = {
            module: self.request_counts[module] 
            for module in healthy_modules
        }
        
        # Choose module with least active requests
        best_module = min(module_loads, key=module_loads.get)
        
        # Track request
        self.request_counts[best_module] += 1
        
        return best_module
    
    def release_module(self, module_name: str):
        """Release module after request completion."""
        if module_name in self.request_counts:
            self.request_counts[module_name] = max(0, self.request_counts[module_name] - 1)
'''
    
    print("✅ Granger Hub fixes defined - ready for implementation")
    
    # Create implementation guide
    implementation_guide = '''
# Granger Hub Module Fix Implementation Guide

## 1. Bounded Message Queue (CRITICAL)
Location: src/granger_hub/core/message_queue.py
- Replace unbounded queues with BoundedMessageQueue
- Set max size to 10,000 messages per queue
- Add backpressure handling
- Monitor dropped message counts
- Log queue statistics periodically

## 2. Circuit Breaker (HIGH)
Location: src/granger_hub/core/circuit_breaker.py
- Implement for all spoke module connections
- Set failure threshold to 5
- Recovery timeout of 60 seconds
- Different breakers for different error types
- Log state transitions

## 3. Connection Pooling (HIGH)
Location: src/granger_hub/core/connection_pool.py
- Max 10 connections per spoke module
- Pre-populate connection pools
- Reuse sessions for efficiency
- Graceful shutdown handling

## 4. Health Monitoring (MEDIUM)
Location: src/granger_hub/monitoring/health.py
- Check module health every 30 seconds
- Track response times
- Count consecutive failures
- Provide health dashboard endpoint
- Alert on module failures

## 5. Load Balancing (MEDIUM)
Location: src/granger_hub/routing/load_balancer.py
- Route to healthy modules only
- Use least-connections algorithm
- Track active requests per module
- Fallback to secondary modules

## API Changes
- Add /health endpoint
- Add /stats endpoint for metrics
- Add /circuit-breakers endpoint
- WebSocket for real-time monitoring

## Configuration
```yaml
hub:
  message_queue:
    max_size: 10000
    drop_policy: "oldest"  # or "newest"
  
  circuit_breaker:
    failure_threshold: 5
    recovery_timeout: 60
    
  health_check:
    interval: 30
    timeout: 5
    
  connection_pool:
    max_per_host: 10
    idle_timeout: 300
```

## Testing
1. Buffer test: Send 20,000 messages rapidly
2. Circuit test: Simulate spoke module failures
3. Pool test: 100 concurrent connections
4. Health test: Kill/restart spoke modules
5. Load test: 1000 requests/second

## Monitoring Metrics
- Queue sizes and drop rates
- Circuit breaker states
- Connection pool usage
- Module health status
- Request latencies
- Error rates by module
'''
    
    # Save implementation guide
    guide_path = Path("/home/graham/workspace/shared_claude_docs/module_specific_fixes/hub_implementation_guide.md")
    guide_path.parent.mkdir(exist_ok=True)
    guide_path.write_text(implementation_guide)
    print(f"📝 Implementation guide saved to: {guide_path}")


if __name__ == "__main__":
    apply_hub_fixes()