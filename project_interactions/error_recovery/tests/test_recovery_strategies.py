"""
Test Recovery Strategy Execution
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
import asyncio
import time
from typing import Dict, Any

from error_recovery_interaction import (
    RecoveryStrategy,
    RecoveryAction,
    CircuitBreaker,
    RecoveryOrchestrator,
    ErrorRecoveryInteraction
)


class TestRecoveryStrategies:
    """Test various recovery strategies"""
    
    @pytest.fixture
    def retry_strategy(self):
        """Create retry strategy"""
        return RecoveryStrategy(
            action=RecoveryAction.RETRY,
            max_retries=3,
            timeout=10.0
        )
    
    @pytest.fixture
    def backoff_strategy(self):
        """Create backoff strategy"""
        return RecoveryStrategy(
            action=RecoveryAction.RETRY_WITH_BACKOFF,
            max_retries=3,
            backoff_base=2.0
        )
    
    @pytest.fixture
    def circuit_breaker(self):
        """Create circuit breaker"""
        return CircuitBreaker(failure_threshold=3, timeout=5.0)
    
    @pytest.mark.asyncio
    async def test_simple_retry_strategy(self, retry_strategy):
        """Test simple retry strategy"""
        attempt_count = 0
        
        async def flaky_function():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError("Temporary failure")
            return "Success"
        
        result = await retry_strategy.execute(flaky_function)
        assert result == "Success"
        assert attempt_count == 3
    
    @pytest.mark.asyncio
    async def test_retry_exhaustion(self, retry_strategy):
        """Test retry exhaustion"""
        async def always_fails():
            raise RuntimeError("Permanent failure")
        
        with pytest.raises(RuntimeError):
            await retry_strategy.execute(always_fails)
    
    @pytest.mark.asyncio
    async def test_exponential_backoff(self, backoff_strategy):
        """Test exponential backoff timing"""
        call_times = []
        
        async def track_timing():
            call_times.append(time.time())
            if len(call_times) < 3:
                raise ConnectionError("Connection failed")
            return "Connected"
        
        start_time = time.time()
        result = await backoff_strategy.execute(track_timing)
        
        assert result == "Connected"
        assert len(call_times) == 3
        
        # Check backoff intervals (approximately)
        intervals = [call_times[i+1] - call_times[i] for i in range(len(call_times)-1)]
        assert intervals[0] < 1.5  # First retry ~1s
        assert 1.5 < intervals[1] < 3  # Second retry ~2s
    
    @pytest.mark.asyncio
    async def test_fallback_strategy(self):
        """Test fallback strategy"""
        async def primary_handler():
            raise Exception("Primary failed")
        
        async def fallback_handler(*args, **kwargs):
            return "Fallback result"
        
        strategy = RecoveryStrategy(
            action=RecoveryAction.FALLBACK,
            fallback_handler=fallback_handler
        )
        
        result = await strategy.execute(primary_handler)
        assert result == "Fallback result"
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_states(self, circuit_breaker):
        """Test circuit breaker state transitions"""
        # Initial state - closed
        assert circuit_breaker.state == "closed"
        assert circuit_breaker.can_execute()
        
        # Record failures to open circuit
        for _ in range(3):
            circuit_breaker.record_failure()
        
        assert circuit_breaker.state == "open"
        assert not circuit_breaker.can_execute()
        
        # Wait for timeout
        await asyncio.sleep(0.1)
        circuit_breaker.timeout = 0.05  # Speed up test
        
        # Should transition to half-open
        assert circuit_breaker.can_execute()
        assert circuit_breaker.state == "half-open"
        
        # Success closes circuit
        circuit_breaker.record_success()
        assert circuit_breaker.state == "closed"
    
    @pytest.mark.asyncio
    async def test_recovery_orchestration(self):
        """Test recovery orchestration across services"""
        orchestrator = RecoveryOrchestrator()
        
        # Define service dependencies
        orchestrator.dependencies = {
            "api": ["database", "cache"],
            "worker": ["database"],
            "cache": [],
            "database": []
        }
        
        # Define health checks
        async def db_health():
            return True
        
        async def cache_health():
            return True
        
        orchestrator.health_checks = {
            "database": db_health,
            "cache": cache_health
        }
        
        # Create recovery plan
        recovery_plan = {
            "database": RecoveryStrategy(action=RecoveryAction.RETRY),
            "cache": RecoveryStrategy(action=RecoveryAction.RETRY),
            "api": RecoveryStrategy(action=RecoveryAction.RETRY)
        }
        
        # Orchestrate recovery
        failed_services = ["api", "database", "cache"]
        results = await orchestrator.orchestrate_recovery(failed_services, recovery_plan)
        
        # Verify recovery order (dependencies first)
        assert "database" in results
        assert "cache" in results
        assert "api" in results
    
    @pytest.mark.asyncio
    async def test_checkpoint_restore(self):
        """Test checkpoint and restore functionality"""
        recovery = ErrorRecoveryInteraction()
        
        # Create checkpoint
        state_data = {"user_id": 123, "progress": 50}
        recovery.create_checkpoint("process_1", state_data)
        
        # Restore checkpoint
        result = await recovery._restore_checkpoint("process_1")
        
        assert result["status"] == "success"
        assert result["restored_state"]["state"] == state_data
        
        # Test missing checkpoint
        result = await recovery._restore_checkpoint("nonexistent")
        assert result["status"] == "failed"
    
    @pytest.mark.asyncio
    async def test_self_healing_capabilities(self):
        """Test self-healing mechanisms"""
        recovery = ErrorRecoveryInteraction()
        
        # Test connection error healing
        connection_error = ConnectionError("Connection lost")
        result = await recovery._self_heal(connection_error, {"service": "api"})
        assert result["status"] == "success"
        assert result["action"] == "reconnected"
        
        # Test memory error healing
        memory_error = MemoryError("Out of memory")
        recovery.checkpoints = {"test": "data"}  # Add some data
        result = await recovery._self_heal(memory_error, {})
        assert result["status"] == "success"
        assert result["action"] == "memory_cleared"
        assert len(recovery.checkpoints) == 0
        
        # Test unhandled error
        unknown_error = Exception("Unknown error")
        result = await recovery._self_heal(unknown_error, {})
        assert result["status"] == "failed"
    
    @pytest.mark.asyncio
    async def test_transaction_rollback(self):
        """Test transaction rollback"""
        recovery = ErrorRecoveryInteraction()
        
        # Test with transaction ID
        result = await recovery._rollback_transaction({
            "transaction_id": "txn_123"
        })
        assert result["status"] == "success"
        assert result["transaction_id"] == "txn_123"
        
        # Test without transaction ID
        result = await recovery._rollback_transaction({})
        assert result["status"] == "failed"
        assert "No transaction" in result["error"]
    
    @pytest.mark.asyncio
    async def test_recovery_with_timeout(self):
        """Test recovery with timeout"""
        async def slow_function():
            await asyncio.sleep(5)
            return "Success"
        
        strategy = RecoveryStrategy(
            action=RecoveryAction.RETRY,
            timeout=1.0
        )
        
        # This should timeout
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(
                strategy.execute(slow_function),
                timeout=2.0
            )
    
    @pytest.mark.asyncio
    async def test_concurrent_recovery_strategies(self):
        """Test concurrent execution of multiple strategies"""
        recovery = ErrorRecoveryInteraction()
        
        async def create_error_and_recover(error_msg: str, service_id: str):
            error = Exception(error_msg)
            context = {
                "service_id": service_id,
                "retry_func": lambda: "Recovered"
            }
            return await recovery.recover_from_error(error, context)
        
        # Execute multiple recoveries concurrently
        tasks = [
            create_error_and_recover("Error 1", "service_1"),
            create_error_and_recover("Error 2", "service_2"),
            create_error_and_recover("Error 3", "service_3")
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Verify all recoveries
        assert len(results) == 3
        for result in results:
            assert "recovery_status" in result
            assert "strategy" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])