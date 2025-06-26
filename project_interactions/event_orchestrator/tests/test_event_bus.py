"""
Module: test_event_bus.py
Purpose: Tests for event bus functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/

Example Usage:
>>> pytest tests/test_event_bus.py -v
"""

import asyncio
import pytest
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from event_orchestrator_interaction import (
    Event, EventBus, EventStore, MemoryEventStore, EventStatus
)


class TestEventBus:
    """Test suite for EventBus functionality"""
    
    @pytest.fixture
    async def event_bus(self):
        """Create event bus fixture"""
        store = MemoryEventStore()
        return EventBus(store)
    
    @pytest.mark.asyncio
    async def test_publish_subscribe(self, event_bus):
        """Test basic publish/subscribe functionality"""
        received_events = []
        
        async def handler(event: Event):
            received_events.append(event)
        
        # Subscribe to event type
        event_bus.subscribe("test.event", handler)
        
        # Publish event
        event = Event(type="test.event", payload={"data": "test"})
        await event_bus.publish(event)
        
        # Verify event was received
        assert len(received_events) == 1
        assert received_events[0].type == "test.event"
        assert received_events[0].payload["data"] == "test"
        assert received_events[0].status == EventStatus.COMPLETED
    
    @pytest.mark.asyncio
    async def test_multiple_handlers(self, event_bus):
        """Test multiple handlers for same event type"""
        handler1_called = False
        handler2_called = False
        
        async def handler1(event: Event):
            nonlocal handler1_called
            handler1_called = True
        
        async def handler2(event: Event):
            nonlocal handler2_called
            handler2_called = True
        
        # Subscribe both handlers
        event_bus.subscribe("multi.event", handler1)
        event_bus.subscribe("multi.event", handler2)
        
        # Publish event
        await event_bus.publish(Event(type="multi.event"))
        
        # Both handlers should be called
        assert handler1_called
        assert handler2_called
    
    @pytest.mark.asyncio
    async def test_event_filtering(self, event_bus):
        """Test event filtering functionality"""
        received_events = []
        
        async def handler(event: Event):
            received_events.append(event)
        
        async def filter_func(event: Event) -> bool:
            return event.payload.get("allowed", False)
        
        # Set up subscription and filter
        event_bus.subscribe("filtered.event", handler)
        event_bus.add_filter("filtered.event", filter_func)
        
        # Publish allowed event
        await event_bus.publish(Event(
            type="filtered.event",
            payload={"allowed": True, "data": "should pass"}
        ))
        
        # Publish filtered event
        await event_bus.publish(Event(
            type="filtered.event",
            payload={"allowed": False, "data": "should not pass"}
        ))
        
        # Only allowed event should be received
        assert len(received_events) == 1
        assert received_events[0].payload["data"] == "should pass"
    
    @pytest.mark.asyncio
    async def test_dead_letter_queue(self, event_bus):
        """Test dead letter queue for failed events"""
        
        async def failing_handler(event: Event):
            raise Exception("Handler error")
        
        event_bus.subscribe("failing.event", failing_handler)
        
        # Publish event that will fail with max_retries=0
        event = Event(type="failing.event", max_retries=0)
        await event_bus.publish(event)
        
        # Event should be in dead letter queue
        assert len(event_bus.dead_letter_queue) == 1
        assert event_bus.dead_letter_queue[0].id == event.id
        assert event_bus.dead_letter_queue[0].status == EventStatus.DEAD_LETTER
    
    @pytest.mark.asyncio
    async def test_event_replay(self, event_bus):
        """Test event replay functionality"""
        replay_count = 0
        
        async def counter_handler(event: Event):
            nonlocal replay_count
            replay_count += 1
        
        event_bus.subscribe("replay.event", counter_handler)
        
        # Publish some events
        for i in range(3):
            await event_bus.publish(Event(
                type="replay.event",
                payload={"index": i}
            ))
        
        initial_count = replay_count
        
        # Replay events
        replayed = await event_bus.replay_events("replay.event")
        
        # Verify replay
        assert replayed == 3
        assert replay_count == initial_count + 3
    
    @pytest.mark.asyncio
    async def test_event_metrics(self, event_bus):
        """Test event metrics tracking"""
        
        async def success_handler(event: Event):
            pass
        
        async def failing_handler(event: Event):
            raise Exception("Test error")
        
        event_bus.subscribe("success.event", success_handler)
        event_bus.subscribe("fail.event", failing_handler)
        
        # Publish successful event
        await event_bus.publish(Event(type="success.event"))
        
        # Publish failing event
        await event_bus.publish(Event(type="fail.event", max_retries=0))
        
        # Check metrics
        metrics = event_bus.metrics
        assert metrics["events_published"] >= 2
        assert metrics["events_processed"] >= 1
        assert metrics["events_failed"] >= 1
    
    @pytest.mark.asyncio
    async def test_correlation_id_propagation(self, event_bus):
        """Test correlation ID propagation"""
        correlation_ids = []
        
        async def handler(event: Event):
            correlation_ids.append(event.correlation_id)
        
        event_bus.subscribe("correlated.event", handler)
        
        # Publish with correlation ID
        correlation_id = "test-correlation-123"
        await event_bus.publish(Event(
            type="correlated.event",
            correlation_id=correlation_id
        ))
        
        assert correlation_ids[0] == correlation_id


if __name__ == "__main__":
    # Run tests with real data
    print("🧪 Testing Event Bus Components")
    print("=" * 50)
    
    async def run_tests():
        bus = EventBus(MemoryEventStore())
        test_instance = TestEventBus()
        
        # Test 1: Basic publish/subscribe
        print("\n1️⃣ Testing publish/subscribe:")
        await test_instance.test_publish_subscribe(bus)
        print("   ✓ Basic pub/sub working")
        
        # Test 2: Multiple handlers
        print("\n2️⃣ Testing multiple handlers:")
        bus = EventBus(MemoryEventStore())  # Fresh instance
        await test_instance.test_multiple_handlers(bus)
        print("   ✓ Multiple handlers working")
        
        # Test 3: Event filtering
        print("\n3️⃣ Testing event filtering:")
        bus = EventBus(MemoryEventStore())  # Fresh instance
        await test_instance.test_event_filtering(bus)
        print("   ✓ Event filtering working")
        
        # Test 4: Dead letter queue
        print("\n4️⃣ Testing dead letter queue:")
        bus = EventBus(MemoryEventStore())  # Fresh instance
        await test_instance.test_dead_letter_queue(bus)
        print("   ✓ Dead letter queue working")
        
        # Test 5: Event replay
        print("\n5️⃣ Testing event replay:")
        bus = EventBus(MemoryEventStore())  # Fresh instance
        await test_instance.test_event_replay(bus)
        print("   ✓ Event replay working")
        
        print("\n✅ All event bus tests passed")
    
    asyncio.run(run_tests())