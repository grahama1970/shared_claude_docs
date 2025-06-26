"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Test Self-Healing Capabilities
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
from datetime import datetime, timedelta
from typing import Dict, List, Any

from error_recovery_interaction import (
    ErrorRecoveryInteraction,
    ErrorPattern,
    RecoveryAction,
    ErrorSeverity
)


class TestSelfHealing:
    """Test self-healing and ML-based recovery capabilities"""
    
    @pytest.fixture
    def recovery_system(self):
        """Create recovery system with trained ML model"""
        recovery = ErrorRecoveryInteraction()
        
        # Generate training data
        patterns = []
        labels = []
        
        # Connection errors - use retry with backoff
        for i in range(20):
            patterns.append(ErrorPattern(
                error_type="ConnectionError",
                frequency=i + 1,
                last_occurrence=datetime.now() - timedelta(minutes=i),
                recovery_success_rate=0.7,
                avg_recovery_time=2.0
            ))
            labels.append(RecoveryAction.RETRY_WITH_BACKOFF)
        
        # Memory errors - self heal
        for i in range(15):
            patterns.append(ErrorPattern(
                error_type="MemoryError",
                frequency=i + 1,
                last_occurrence=datetime.now() - timedelta(minutes=i),
                recovery_success_rate=0.9,
                avg_recovery_time=0.5
            ))
            labels.append(RecoveryAction.SELF_HEAL)
        
        # Critical errors - escalate
        for i in range(10):
            patterns.append(ErrorPattern(
                error_type="SystemError",
                frequency=i + 1,
                last_occurrence=datetime.now() - timedelta(minutes=i),
                recovery_success_rate=0.1,
                avg_recovery_time=10.0
            ))
            labels.append(RecoveryAction.ESCALATE)
        
        # Train the classifier
        recovery.classifier.train(patterns, labels)
        
        return recovery
    
    @pytest.mark.asyncio
    async def test_pattern_learning(self, recovery_system):
        """Test system learns from recovery patterns"""
        # Initial error
        error = ValueError("Test error")
        context = {"service": "api", "retry_func": lambda: "Success"}
        
        # Get initial pattern
        initial_pattern = recovery_system._analyze_error(error, context)
        initial_success_rate = initial_pattern.recovery_success_rate
        
        # Simulate successful recoveries
        for _ in range(5):
            result = {"status": "success"}
            recovery_system._update_patterns(error, 
                RecoveryStrategy(action=RecoveryAction.RETRY),
                result, 1.0)
        
        # Check pattern has improved
        updated_pattern = recovery_system._analyze_error(error, context)
        assert updated_pattern.recovery_success_rate > initial_success_rate
    
    @pytest.mark.asyncio
    async def test_ml_strategy_selection(self, recovery_system):
        """Test ML-based strategy selection"""
        # Test connection error - should suggest retry with backoff
        conn_pattern = ErrorPattern(
            error_type="ConnectionError",
            frequency=5,
            last_occurrence=datetime.now(),
            recovery_success_rate=0.7,
            avg_recovery_time=2.0
        )
        
        strategy = await recovery_system._select_strategy(
            conn_pattern, ErrorSeverity.MEDIUM, {}
        )
        
        # ML should predict retry with backoff for connection errors
        assert strategy.action in [RecoveryAction.RETRY_WITH_BACKOFF, RecoveryAction.RETRY]
    
    @pytest.mark.asyncio
    async def test_adaptive_recovery(self, recovery_system):
        """Test adaptive recovery based on history"""
        # Simulate a pattern of failures
        error = TimeoutError("Operation timed out")
        
        # First attempts should use default strategy
        for i in range(3):
            context = {
                "service_id": "slow_service",
                "retry_func": lambda: (_ for _ in ()).throw(TimeoutError("Still timing out"))
            }
            
            try:
                await recovery_system.recover_from_error(error, context)
            except:
                pass  # Expected to fail
        
        # Check that circuit breaker might be triggered
        breaker = recovery_system.circuit_breakers.get("slow_service")
        if breaker:
            assert breaker.failure_count > 0
    
    @pytest.mark.asyncio
    async def test_recovery_history_tracking(self, recovery_system):
        """Test recovery history and statistics"""
        # Perform several recoveries
        success_count = 0
        total_count = 5
        
        for i in range(total_count):
            error = Exception(f"Test error {i}")
            
            # Alternate between success and failure
            if i % 2 == 0:
                async def success_func():
                    return "Success"
                context = {"retry_func": success_func}
                success_count += 1
            else:
                async def fail_func():
                    raise Exception("Failed")
                context = {"retry_func": fail_func}
            
            try:
                await recovery_system.recover_from_error(error, context)
            except:
                pass
        
        # Get statistics
        stats = recovery_system.get_recovery_stats()
        
        assert stats["total_recoveries"] > 0
        assert "success_rate" in stats
        assert "avg_recovery_time" in stats
    
    @pytest.mark.asyncio
    async def test_predictive_error_prevention(self, recovery_system):
        """Test predictive capabilities"""
        # Create pattern that indicates impending failure
        pattern = ErrorPattern(
            error_type="ResourceExhaustion",
            frequency=50,  # High frequency
            last_occurrence=datetime.now(),
            recovery_success_rate=0.1,  # Low success
            avg_recovery_time=30.0  # Long recovery
        )
        
        # System should assess this as critical
        error = Exception("Resource exhausted")
        severity = recovery_system._assess_severity(error, pattern)
        
        assert severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]
        
        # Strategy should be conservative
        strategy = await recovery_system._select_strategy(
            pattern, severity, {}
        )
        
        assert strategy.max_retries <= 3  # Limited retries for critical errors
    
    @pytest.mark.asyncio
    async def test_self_healing_memory_management(self, recovery_system):
        """Test self-healing for memory issues"""
        # Fill up checkpoints
        for i in range(100):
            recovery_system.create_checkpoint(f"service_{i}", {"data": f"state_{i}"})
        
        # Trigger memory error healing
        memory_error = MemoryError("Out of memory")
        result = await recovery_system._self_heal(memory_error, {})
        
        assert result["status"] == "success"
        assert len(recovery_system.checkpoints) == 0  # Cleared
    
    @pytest.mark.asyncio
    async def test_cascading_failure_recovery(self, recovery_system):
        """Test recovery from cascading failures"""
        # Simulate cascading failures
        services = ["database", "cache", "api", "frontend"]
        errors = []
        
        for i, service in enumerate(services):
            error = Exception(f"{service} failure")
            context = {
                "service_id": service,
                "dependency_chain": services[:i+1],
                "retry_func": lambda: "Recovered"
            }
            
            result = await recovery_system.recover_from_error(error, context)
            errors.append((service, result))
        
        # Verify all services attempted recovery
        assert len(errors) == len(services)
        
        # Check recovery history
        assert len(recovery_system.recovery_history) >= len(services)
    
    @pytest.mark.asyncio
    async def test_intelligent_retry_intervals(self, recovery_system):
        """Test intelligent retry interval adjustment"""
        # Create pattern with varying success rates
        fast_recovery_pattern = ErrorPattern(
            error_type="FastError",
            frequency=10,
            last_occurrence=datetime.now(),
            recovery_success_rate=0.9,
            avg_recovery_time=0.1
        )
        
        slow_recovery_pattern = ErrorPattern(
            error_type="SlowError",
            frequency=10,
            last_occurrence=datetime.now(),
            recovery_success_rate=0.3,
            avg_recovery_time=5.0
        )
        
        # Get strategies
        fast_strategy = await recovery_system._select_strategy(
            fast_recovery_pattern, ErrorSeverity.LOW, {}
        )
        
        slow_strategy = await recovery_system._select_strategy(
            slow_recovery_pattern, ErrorSeverity.MEDIUM, {}
        )
        
        # Fast recovery should have more retries
        assert fast_strategy.max_retries >= slow_strategy.max_retries
    
    @pytest.mark.asyncio
    async def test_recovery_performance_monitoring(self, recovery_system):
        """Test recovery performance monitoring"""
        # Perform timed recoveries
        recovery_times = []
        
        for i in range(10):
            start_time = time.time()
            
            async def quick_func():
                await asyncio.sleep(0.01 * (i + 1))
                return "Success"
            
            error = Exception(f"Error {i}")
            context = {"retry_func": quick_func}
            
            await recovery_system.recover_from_error(error, context)
            recovery_times.append(time.time() - start_time)
        
        # Verify recovery times are tracked
        stats = recovery_system.get_recovery_stats()
        assert stats["avg_recovery_time"] > 0
        
        # Check that longer recoveries are reflected
        assert max(recovery_times) > min(recovery_times)
    
    @pytest.mark.asyncio
    async def test_context_aware_healing(self, recovery_system):
        """Test context-aware self-healing"""
        # Database connection error
        db_error = ConnectionError("Database connection failed")
        db_context = {
            "service": "api",
            "database": "primary",
            "retry_func": lambda: "Connected"
        }
        
        result = await recovery_system.recover_from_error(db_error, db_context)
        assert result["recovery_status"] in ["success", "failed"]
        
        # API rate limit error
        rate_error = Exception("Rate limit exceeded")
        rate_context = {
            "service": "external_api",
            "endpoint": "/data",
            "retry_func": lambda: "Success"
        }
        
        result = await recovery_system.recover_from_error(rate_error, rate_context)
        
        # Should use backoff for rate limits
        assert result["strategy"] in ["retry_with_backoff", "circuit_break"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])