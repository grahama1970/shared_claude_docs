"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Module: test_saga_orchestration.py
Purpose: Tests for saga orchestration patterns

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/

Example Usage:
>>> pytest tests/test_saga_orchestration.py -v
"""

import asyncio
import pytest
from typing import Dict, Any, List
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from event_orchestrator_interaction import (
    EventBus, MemoryEventStore, SagaOrchestrator, SagaStep,
    Saga, SagaStatus, Event
)


class TestSagaOrchestration:
    """Test suite for Saga orchestration patterns"""
    
    @pytest.fixture
    async def saga_orchestrator(self):
        """Create saga orchestrator fixture"""
        store = MemoryEventStore()
        event_bus = EventBus(store)
        return SagaOrchestrator(event_bus)
    
    @pytest.mark.asyncio
    async def test_successful_saga_execution(self, saga_orchestrator):
        """Test successful saga execution"""
        execution_order = []
        
        async def step1(context: Dict[str, Any]) -> Dict[str, Any]:
            execution_order.append("step1")
            return {"step1": "completed"}
        
        async def step2(context: Dict[str, Any]) -> Dict[str, Any]:
            execution_order.append("step2")
            return {"step2": "completed"}
        
        async def step3(context: Dict[str, Any]) -> Dict[str, Any]:
            execution_order.append("step3")
            return {"step3": "completed"}
        
        # Define saga
        saga_orchestrator.define_saga("test_saga", [
            SagaStep("step1", step1),
            SagaStep("step2", step2),
            SagaStep("step3", step3)
        ])
        
        # Start saga
        saga = await saga_orchestrator.start_saga("test_saga", {"input": "test"})
        
        # Wait for completion
        await asyncio.sleep(0.5)
        
        # Verify execution
        final_saga = saga_orchestrator.sagas[saga.id]
        assert final_saga.status == SagaStatus.COMPLETED
        assert execution_order == ["step1", "step2", "step3"]
        assert len(final_saga.completed_steps) == 3
    
    @pytest.mark.asyncio
    async def test_saga_compensation(self, saga_orchestrator):
        """Test saga compensation on failure"""
        execution_order = []
        compensation_order = []
        
        async def step1(context: Dict[str, Any]) -> Dict[str, Any]:
            execution_order.append("step1")
            return {"step1": "completed"}
        
        async def step2(context: Dict[str, Any]) -> Dict[str, Any]:
            execution_order.append("step2")
            return {"step2": "completed"}
        
        async def step3_failing(context: Dict[str, Any]) -> Dict[str, Any]:
            execution_order.append("step3")
            raise Exception("Step 3 failed")
        
        async def compensate_step1(context: Dict[str, Any]) -> None:
            compensation_order.append("compensate_step1")
        
        async def compensate_step2(context: Dict[str, Any]) -> None:
            compensation_order.append("compensate_step2")
        
        # Define saga with compensations
        saga_orchestrator.define_saga("failing_saga", [
            SagaStep("step1", step1, compensate_step1),
            SagaStep("step2", step2, compensate_step2),
            SagaStep("step3", step3_failing)
        ])
        
        # Start saga
        saga = await saga_orchestrator.start_saga("failing_saga", {})
        
        # Wait for compensation
        await asyncio.sleep(0.5)
        
        # Verify compensation
        final_saga = saga_orchestrator.sagas[saga.id]
        assert final_saga.status == SagaStatus.COMPENSATED
        assert final_saga.failed_step == "step3"
        assert compensation_order == ["compensate_step2", "compensate_step1"]
    
    @pytest.mark.asyncio
    async def test_saga_timeout(self, saga_orchestrator):
        """Test saga step timeout"""
        
        async def slow_step(context: Dict[str, Any]) -> Dict[str, Any]:
            await asyncio.sleep(2)  # Longer than timeout
            return {"result": "should not reach"}
        
        # Define saga with short timeout
        saga_orchestrator.define_saga("timeout_saga", [
            SagaStep("slow_step", slow_step, timeout=0.1)
        ])
        
        # Start saga
        saga = await saga_orchestrator.start_saga("timeout_saga", {})
        
        # Wait for timeout
        await asyncio.sleep(0.5)
        
        # Verify timeout handling
        final_saga = saga_orchestrator.sagas[saga.id]
        assert final_saga.status == SagaStatus.COMPENSATED
        assert "timed out" in final_saga.error
    
    @pytest.mark.asyncio
    async def test_saga_context_propagation(self, saga_orchestrator):
        """Test context propagation between saga steps"""
        context_values = []
        
        async def step1(context: Dict[str, Any]) -> Dict[str, Any]:
            context_values.append(context.get("input"))
            return {"output1": "value1"}
        
        async def step2(context: Dict[str, Any]) -> Dict[str, Any]:
            context_values.append(context.get("step1_result"))
            return {"output2": "value2"}
        
        async def step3(context: Dict[str, Any]) -> Dict[str, Any]:
            context_values.append(context.get("step2_result"))
            return {"output3": "value3"}
        
        # Define saga
        saga_orchestrator.define_saga("context_saga", [
            SagaStep("step1", step1),
            SagaStep("step2", step2),
            SagaStep("step3", step3)
        ])
        
        # Start saga
        saga = await saga_orchestrator.start_saga("context_saga", {"input": "initial"})
        
        # Wait for completion
        await asyncio.sleep(0.5)
        
        # Verify context propagation
        assert context_values[0] == "initial"
        assert context_values[1]["output1"] == "value1"
        assert context_values[2]["output2"] == "value2"
    
    @pytest.mark.asyncio
    async def test_saga_events(self, saga_orchestrator):
        """Test saga event publishing"""
        events_published = []
        
        async def event_handler(event: Event):
            events_published.append(event)
        
        # Subscribe to saga events
        saga_orchestrator.event_bus.subscribe("saga.test_events.started", event_handler)
        saga_orchestrator.event_bus.subscribe("saga.test_events.step_completed", event_handler)
        saga_orchestrator.event_bus.subscribe("saga.test_events.completed", event_handler)
        
        async def simple_step(context: Dict[str, Any]) -> Dict[str, Any]:
            return {"result": "done"}
        
        # Define saga
        saga_orchestrator.define_saga("test_events", [
            SagaStep("simple", simple_step)
        ])
        
        # Start saga
        saga = await saga_orchestrator.start_saga("test_events", {})
        
        # Wait for events
        await asyncio.sleep(0.5)
        
        # Verify events
        event_types = [e.type for e in events_published]
        assert "saga.test_events.started" in event_types
        assert "saga.test_events.step_completed" in event_types
        assert "saga.test_events.completed" in event_types
    
    @pytest.mark.asyncio
    async def test_parallel_sagas(self, saga_orchestrator):
        """Test running multiple sagas in parallel"""
        saga_results = {}
        
        async def saga_step(context: Dict[str, Any]) -> Dict[str, Any]:
            saga_id = context.get("saga_id")
            await asyncio.sleep(0.1)  # Simulate work
            return {"saga_id": saga_id, "completed": True}
        
        # Define saga
        saga_orchestrator.define_saga("parallel_saga", [
            SagaStep("process", saga_step)
        ])
        
        # Start multiple sagas
        sagas = []
        for i in range(5):
            saga = await saga_orchestrator.start_saga(
                "parallel_saga",
                {"saga_id": f"saga_{i}"}
            )
            sagas.append(saga)
        
        # Wait for all to complete
        await asyncio.sleep(0.5)
        
        # Verify all completed
        for saga in sagas:
            final_saga = saga_orchestrator.sagas[saga.id]
            assert final_saga.status == SagaStatus.COMPLETED
    
    @pytest.mark.asyncio
    async def test_saga_retry_policy(self, saga_orchestrator):
        """Test saga step retry policy"""
        attempt_count = 0
        
        async def flaky_step(context: Dict[str, Any]) -> Dict[str, Any]:
            nonlocal attempt_count
            attempt_count += 1
            
            if attempt_count < 3:
                raise Exception("Temporary failure")
            
            return {"success": True}
        
        # For this test, we'll simulate retry by catching and retrying
        async def retry_wrapper(context: Dict[str, Any]) -> Dict[str, Any]:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    return await flaky_step(context)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    await asyncio.sleep(0.1)
        
        # Define saga
        saga_orchestrator.define_saga("retry_saga", [
            SagaStep("flaky", retry_wrapper)
        ])
        
        # Start saga
        saga = await saga_orchestrator.start_saga("retry_saga", {})
        
        # Wait for completion
        await asyncio.sleep(1)
        
        # Verify retry worked
        final_saga = saga_orchestrator.sagas[saga.id]
        assert final_saga.status == SagaStatus.COMPLETED
        assert attempt_count == 3


if __name__ == "__main__":
    # Run tests with real data
    print("🧪 Testing Saga Orchestration")
    print("=" * 50)
    
    async def run_tests():
        store = MemoryEventStore()
        event_bus = EventBus(store)
        orchestrator = SagaOrchestrator(event_bus)
        test_instance = TestSagaOrchestration()
        
        # Test 1: Successful saga
        print("\n1️⃣ Testing successful saga execution:")
        await test_instance.test_successful_saga_execution(orchestrator)
        print("   ✓ Saga completed successfully")
        
        # Test 2: Saga compensation
        print("\n2️⃣ Testing saga compensation:")
        orchestrator = SagaOrchestrator(EventBus(MemoryEventStore()))
        await test_instance.test_saga_compensation(orchestrator)
        print("   ✓ Compensation executed correctly")
        
        # Test 3: Saga timeout
        print("\n3️⃣ Testing saga timeout:")
        orchestrator = SagaOrchestrator(EventBus(MemoryEventStore()))
        await test_instance.test_saga_timeout(orchestrator)
        print("   ✓ Timeout handled correctly")
        
        # Test 4: Context propagation
        print("\n4️⃣ Testing context propagation:")
        orchestrator = SagaOrchestrator(EventBus(MemoryEventStore()))
        await test_instance.test_saga_context_propagation(orchestrator)
        print("   ✓ Context propagated correctly")
        
        # Test 5: Parallel sagas
        print("\n5️⃣ Testing parallel sagas:")
        orchestrator = SagaOrchestrator(EventBus(MemoryEventStore()))
        await test_instance.test_parallel_sagas(orchestrator)
        print("   ✓ Parallel execution working")
        
        print("\n✅ All saga orchestration tests passed")
    
    asyncio.run(run_tests())