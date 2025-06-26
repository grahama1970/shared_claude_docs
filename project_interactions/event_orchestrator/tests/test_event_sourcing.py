"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Module: test_event_sourcing.py
Purpose: Tests for event sourcing and CQRS patterns

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/

Example Usage:
>>> pytest tests/test_event_sourcing.py -v
"""

import asyncio
import pytest
from typing import Dict, Any, List
import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from event_orchestrator_interaction import (
    Event, EventOrchestrator, EventSchemaRegistry, CQRSHelper,
    EventBus, MemoryEventStore, DistributedTracing
)


class TestEventSourcing:
    """Test suite for event sourcing functionality"""
    
    @pytest.fixture
    async def orchestrator(self):
        """Create orchestrator fixture"""
        return EventOrchestrator()
    
    @pytest.mark.asyncio
    async def test_event_store_append_and_retrieve(self, orchestrator):
        """Test event store operations"""
        # Create events
        events = []
        for i in range(5):
            event = await orchestrator.publish_event(
                f"test.event.{i}",
                {"index": i, "data": f"test_{i}"},
                correlation_id="stream_123"
            )
            events.append(event)
            await asyncio.sleep(0.01)  # Ensure different timestamps
        
        # Retrieve all events
        all_events = await orchestrator.store.get_all_events()
        assert len(all_events) >= 5
        
        # Retrieve by stream
        stream_events = await orchestrator.store.get_events("stream_123")
        assert len(stream_events) == 5
        assert all(e.correlation_id == "stream_123" for e in stream_events)
    
    @pytest.mark.asyncio
    async def test_event_versioning_and_migration(self, orchestrator):
        """Test event schema versioning and migration"""
        # Register schemas
        orchestrator.schema_registry.register_schema(
            "user.created",
            version=1,
            schema={"name": "string", "email": "string"}
        )
        
        orchestrator.schema_registry.register_schema(
            "user.created",
            version=2,
            schema={"name": "string", "email": "string", "phone": "string"}
        )
        
        # Register migration
        async def migrate_v1_to_v2(event: Event) -> Event:
            event.payload["phone"] = "not_provided"
            return event
        
        orchestrator.schema_registry.register_migration(
            "user.created", 1, 2, migrate_v1_to_v2
        )
        
        # Create v1 event
        v1_event = Event(
            type="user.created",
            payload={"name": "John", "email": "john@example.com"},
            version=1
        )
        
        # Migrate to v2
        v2_event = await orchestrator.schema_registry.migrate_event(v1_event, 2)
        
        assert v2_event.version == 2
        assert v2_event.payload["phone"] == "not_provided"
        assert v2_event.payload["name"] == "John"
    
    @pytest.mark.asyncio
    async def test_cqrs_command_query_separation(self, orchestrator):
        """Test CQRS pattern implementation"""
        # In-memory state for testing
        users = {}
        
        # Command handler
        async def create_user_handler(data: Dict[str, Any]) -> Dict[str, Any]:
            user_id = f"user_{len(users) + 1}"
            users[user_id] = {
                "id": user_id,
                "name": data["name"],
                "email": data["email"],
                "created_at": time.time()
            }
            return {"user_id": user_id, "success": True}
        
        # Query handler
        async def get_user_handler(params: Dict[str, Any]) -> Dict[str, Any]:
            user_id = params.get("user_id")
            return users.get(user_id, {"error": "User not found"})
        
        # Register handlers
        orchestrator.register_command_handler("create_user", create_user_handler)
        orchestrator.register_query_handler("get_user", get_user_handler)
        
        # Execute command
        command_result = await orchestrator.send_command("create_user", {
            "name": "Alice",
            "email": "alice@example.com"
        })
        
        assert command_result["success"]
        user_id = command_result["user_id"]
        
        # Execute query
        query_result = await orchestrator.execute_query("get_user", {
            "user_id": user_id
        })
        
        assert query_result["name"] == "Alice"
        assert query_result["email"] == "alice@example.com"
    
    @pytest.mark.asyncio
    async def test_event_replay_functionality(self, orchestrator):
        """Test event replay from event store"""
        replay_count = 0
        
        async def count_handler(event: Event):
            nonlocal replay_count
            replay_count += 1
        
        orchestrator.subscribe("replay.test", count_handler)
        
        # Publish events
        for i in range(10):
            await orchestrator.publish_event("replay.test", {"index": i})
        
        initial_count = replay_count
        
        # Replay all events
        replayed = await orchestrator.replay_events("replay.test")
        
        assert replayed == 10
        assert replay_count == initial_count + 10
    
    @pytest.mark.asyncio
    async def test_event_projection_updates(self, orchestrator):
        """Test projection updates for read models"""
        # Define projection updater
        def user_projection_updater(projection: Dict[str, Any]) -> Dict[str, Any]:
            if "users" not in projection:
                projection["users"] = {}
            
            # This would normally be triggered by events
            projection["users"]["user_1"] = {
                "name": "Test User",
                "email": "test@example.com"
            }
            projection["total_users"] = len(projection["users"])
            
            return projection
        
        # Update projection
        orchestrator.cqrs_helper.update_projection("user_stats", user_projection_updater)
        
        # Verify projection
        projection = orchestrator.cqrs_helper.projections.get("user_stats", {})
        assert projection["total_users"] == 1
        assert "user_1" in projection["users"]
    
    @pytest.mark.asyncio
    async def test_distributed_tracing(self, orchestrator):
        """Test distributed tracing integration"""
        trace_id = "test_trace_123"
        
        # Start spans
        root_span = orchestrator.tracing.start_span(trace_id, "root_operation")
        orchestrator.tracing.add_tag(root_span, "service", "event_orchestrator")
        
        child_span = orchestrator.tracing.start_span(
            trace_id, "child_operation", parent_span=root_span
        )
        orchestrator.tracing.add_log(child_span, "Processing event")
        
        # Simulate some work
        await asyncio.sleep(0.1)
        
        # End spans
        orchestrator.tracing.end_span(child_span)
        orchestrator.tracing.end_span(root_span)
        
        # Verify trace
        traces = orchestrator.tracing.traces[trace_id]
        assert len(traces) == 2
        
        root_trace = next(t for t in traces if t["name"] == "root_operation")
        assert root_trace["tags"]["service"] == "event_orchestrator"
        assert "duration" in root_trace
        
        child_trace = next(t for t in traces if t["name"] == "child_operation")
        assert child_trace["parent_span"] == root_span
        assert len(child_trace["logs"]) == 1
    
    @pytest.mark.asyncio
    async def test_workflow_orchestration(self, orchestrator):
        """Test workflow orchestration"""
        workflow_events = []
        
        async def workflow_handler(event: Event):
            workflow_events.append(event)
        
        # Subscribe to workflow events
        orchestrator.subscribe("workflow.order.started", workflow_handler)
        orchestrator.subscribe("order.validate", workflow_handler)
        
        # Define workflow
        orchestrator.define_workflow("order", [
            {"event_type": "order.validate", "timeout": 30},
            {"event_type": "order.payment", "timeout": 60},
            {"event_type": "order.ship", "timeout": 120}
        ])
        
        # Start workflow
        workflow_id = await orchestrator.start_workflow("order", {
            "order_id": "ORDER123",
            "amount": 99.99
        })
        
        await asyncio.sleep(0.1)
        
        # Verify workflow started
        assert len(workflow_events) >= 2
        assert any(e.type == "workflow.order.started" for e in workflow_events)
        assert any(e.type == "order.validate" for e in workflow_events)
    
    @pytest.mark.asyncio
    async def test_dead_letter_reprocessing(self, orchestrator):
        """Test dead letter queue reprocessing"""
        fail_count = 0
        
        async def failing_handler(event: Event):
            nonlocal fail_count
            fail_count += 1
            if fail_count <= 3:
                raise Exception("Temporary failure")
        
        orchestrator.subscribe("dlq.test", failing_handler)
        
        # Publish event that will fail
        event = await orchestrator.publish_event(
            "dlq.test",
            {"data": "test"},
            correlation_id="dlq_123"
        )
        
        # Let it fail and go to DLQ
        await asyncio.sleep(0.1)
        
        # Check DLQ
        dlq = orchestrator.get_dead_letter_queue()
        assert len(dlq) > 0
        
        # Reset fail count and reprocess
        fail_count = 0
        success = await orchestrator.reprocess_dead_letter(dlq[0].id)
        assert success
        
        await asyncio.sleep(0.1)
        
        # Verify reprocessed
        new_dlq = orchestrator.get_dead_letter_queue()
        assert len(new_dlq) < len(dlq)


if __name__ == "__main__":
    # Run tests with real data
    print("🧪 Testing Event Sourcing and CQRS")
    print("=" * 50)
    
    async def run_tests():
        orchestrator = EventOrchestrator()
        test_instance = TestEventSourcing()
        
        # Test 1: Event store
        print("\n1️⃣ Testing event store operations:")
        await test_instance.test_event_store_append_and_retrieve(orchestrator)
        print("   ✓ Event store working correctly")
        
        # Test 2: Event versioning
        print("\n2️⃣ Testing event versioning:")
        orchestrator = EventOrchestrator()
        await test_instance.test_event_versioning_and_migration(orchestrator)
        print("   ✓ Event migration working")
        
        # Test 3: CQRS pattern
        print("\n3️⃣ Testing CQRS pattern:")
        orchestrator = EventOrchestrator()
        await test_instance.test_cqrs_command_query_separation(orchestrator)
        print("   ✓ CQRS working correctly")
        
        # Test 4: Event replay
        print("\n4️⃣ Testing event replay:")
        orchestrator = EventOrchestrator()
        await test_instance.test_event_replay_functionality(orchestrator)
        print("   ✓ Event replay working")
        
        # Test 5: Distributed tracing
        print("\n5️⃣ Testing distributed tracing:")
        orchestrator = EventOrchestrator()
        await test_instance.test_distributed_tracing(orchestrator)
        print("   ✓ Tracing working correctly")
        
        # Test 6: Workflow orchestration
        print("\n6️⃣ Testing workflow orchestration:")
        orchestrator = EventOrchestrator()
        await test_instance.test_workflow_orchestration(orchestrator)
        print("   ✓ Workflow orchestration working")
        
        print("\n✅ All event sourcing tests passed")
    
    asyncio.run(run_tests())