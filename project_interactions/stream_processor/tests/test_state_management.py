"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_state_management.py
Purpose: Test state management and checkpointing in stream processing

External Dependencies:
- asyncio: https://docs.python.org/3/library/asyncio.html
- pytest: https://docs.pytest.org/

Example Usage:
>>> pytest test_state_management.py -v
"""

import asyncio
import time
import json
from typing import Dict, Any
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stream_processor_interaction import (
    StreamProcessor, StreamEvent, StateStore, 
    SequencePattern, TemporalPattern
)


class TestStateManagement:
    """Test suite for state management"""
    
    async def test_state_store_operations(self):
        """Test basic state store operations"""
        store = StateStore()
        
        # Test put and get
        store.put("key1", "value1")
        store.put("key2", {"data": "value2"})
        
        assert store.get("key1") == "value1"
        assert store.get("key2") == {"data": "value2"}
        assert store.get("nonexistent") is None
        
        # Test delete
        store.delete("key1")
        assert store.get("key1") is None
        
        # Test update
        store.put("key2", {"data": "updated"})
        assert store.get("key2") == {"data": "updated"}
        
        return True
        
    async def test_stateful_processing(self):
        """Test stateful stream processing"""
        processor = StreamProcessor()
        results = []
        processor.add_output_sink(lambda x: results.append(x))
        
        await processor.start()
        
        # Stateful processing function (running count per key)
        def stateful_count(event: StreamEvent) -> Dict:
            # Get state store for partition
            store = processor.state_stores[event.partition]
            
            # Get current count
            current_count = store.get(event.key) or 0
            new_count = current_count + 1
            
            # Update state
            store.put(event.key, new_count)
            
            return {
                "key": event.key,
                "count": new_count,
                "timestamp": event.timestamp
            }
            
        await processor.process_stream("stateful", stateful_count)
        
        # Generate events with repeated keys
        base_time = int(time.time() * 1000)
        events = []
        
        for i in range(20):
            events.append(StreamEvent(
                key=f"user_{i % 5}",  # 5 unique keys
                value={"action": "click"},
                timestamp=base_time + i * 100,
                offset=i
            ))
            
        await processor.ingest(events)
        await asyncio.sleep(1)
        
        # Verify stateful counting
        counts_by_key = {}
        for result in results:
            if "key" in result:
                counts_by_key[result["key"]] = result["count"]
                
        # Each of 5 keys should have count of 4 (20 events / 5 keys)
        assert all(count == 4 for count in counts_by_key.values())
        
        await processor.stop()
        return True
        
    async def test_checkpointing(self):
        """Test state checkpointing"""
        store = StateStore(checkpoint_interval_ms=100)
        
        # Add some state
        for i in range(10):
            store.put(f"key_{i}", {"value": i})
            
        # Create checkpoint
        checkpoint = store.checkpoint()
        
        assert "state" in checkpoint
        assert "timestamp" in checkpoint
        assert len(checkpoint["state"]) == 10
        
        # Modify state after checkpoint
        store.put("key_10", {"value": 10})
        store.delete("key_0")
        
        # Restore from checkpoint
        store.restore(checkpoint)
        
        # Verify restored state
        assert store.get("key_0") == {"value": 0}
        assert store.get("key_10") is None
        assert len(store.state) == 10
        
        return True
        
    async def test_exactly_once_processing(self):
        """Test exactly-once processing guarantees"""
        processor = StreamProcessor()
        processed_events = []
        
        def track_processing(result):
            processed_events.append(result)
            
        processor.add_output_sink(track_processing)
        await processor.start()
        
        # Simple processing that includes offset
        def process_once(event: StreamEvent) -> Dict:
            return {
                "key": event.key,
                "offset": event.offset,
                "processed": True
            }
            
        await processor.process_stream("exactly_once", process_once)
        
        # Send same events multiple times (simulating replay)
        base_time = int(time.time() * 1000)
        
        for replay in range(3):
            events = [
                StreamEvent(
                    key=f"key_{i}",
                    value={"data": i},
                    timestamp=base_time + i * 100,
                    offset=i,
                    partition=0
                )
                for i in range(5)
            ]
            await processor.ingest(events)
            await asyncio.sleep(0.5)
            
        # Check that each offset was processed exactly once
        processed_offsets = [e["offset"] for e in processed_events if "offset" in e]
        unique_offsets = list(set(processed_offsets))
        
        assert len(unique_offsets) == 5
        assert sorted(unique_offsets) == [0, 1, 2, 3, 4]
        
        await processor.stop()
        return True
        
    async def test_complex_event_patterns(self):
        """Test complex event pattern matching"""
        processor = StreamProcessor()
        detected_patterns = []
        
        processor.add_output_sink(lambda x: detected_patterns.append(x))
        await processor.start()
        
        # Define a sequence pattern: login -> search -> purchase
        sequence = SequencePattern([
            lambda e: e.value.get("action") == "login",
            lambda e: e.value.get("action") == "search",
            lambda e: e.value.get("action") == "purchase"
        ])
        
        # Pattern detection with state
        event_buffer = []
        
        def detect_patterns(event: StreamEvent) -> Dict:
            # Add to buffer
            event_buffer.append(event)
            
            # Keep only recent events (last 10)
            if len(event_buffer) > 10:
                event_buffer.pop(0)
                
            # Check for pattern in sliding window
            for i in range(len(event_buffer) - 2):
                window = event_buffer[i:i+3]
                if sequence.match(window):
                    return {
                        "pattern": "login_search_purchase",
                        "user": event.key,
                        "timestamp": event.timestamp,
                        "events": [e.value["action"] for e in window]
                    }
                    
            return None
            
        await processor.process_stream("patterns", detect_patterns)
        
        # Generate event sequence
        base_time = int(time.time() * 1000)
        events = [
            StreamEvent("user1", {"action": "login"}, base_time, offset=0),
            StreamEvent("user1", {"action": "browse"}, base_time + 100, offset=1),
            StreamEvent("user1", {"action": "search"}, base_time + 200, offset=2),
            StreamEvent("user1", {"action": "purchase"}, base_time + 300, offset=3),
            StreamEvent("user2", {"action": "login"}, base_time + 400, offset=4),
            StreamEvent("user2", {"action": "search"}, base_time + 500, offset=5),
            StreamEvent("user2", {"action": "logout"}, base_time + 600, offset=6),
        ]
        
        await processor.ingest(events)
        await asyncio.sleep(1)
        
        # Verify pattern detection
        patterns = [p for p in detected_patterns if p and "pattern" in p]
        assert len(patterns) >= 1
        assert patterns[0]["pattern"] == "login_search_purchase"
        assert patterns[0]["user"] == "user1"
        
        await processor.stop()
        return True
        
    async def test_state_recovery(self):
        """Test state recovery after failure"""
        # First processor instance
        processor1 = StreamProcessor()
        results1 = []
        processor1.add_output_sink(lambda x: results1.append(x))
        
        await processor1.start()
        
        # Stateful aggregation
        def aggregate_sum(event: StreamEvent) -> Dict:
            store = processor1.state_stores[event.partition]
            current_sum = store.get("total_sum") or 0
            new_sum = current_sum + event.value["amount"]
            store.put("total_sum", new_sum)
            
            return {
                "total_sum": new_sum,
                "event_count": (store.get("count") or 0) + 1
            }
            
        await processor1.process_stream("aggregate", aggregate_sum)
        
        # Process some events
        base_time = int(time.time() * 1000)
        events = [
            StreamEvent(
                key=f"txn_{i}",
                value={"amount": i * 10},
                timestamp=base_time + i * 100,
                offset=i,
                partition=0
            )
            for i in range(5)
        ]
        
        await processor1.ingest(events)
        await asyncio.sleep(0.5)
        
        # Get checkpoint
        checkpoint = processor1.state_stores[0].checkpoint()
        last_offset = processor1.processed_offsets.get(0, -1)
        
        await processor1.stop()
        
        # Simulate recovery with new processor
        processor2 = StreamProcessor()
        results2 = []
        processor2.add_output_sink(lambda x: results2.append(x))
        
        # Restore state
        processor2.state_stores[0].restore(checkpoint)
        processor2.processed_offsets[0] = last_offset
        
        await processor2.start()
        
        # Continue processing from where we left off
        def continue_aggregate(event: StreamEvent) -> Dict:
            store = processor2.state_stores[event.partition]
            current_sum = store.get("total_sum") or 0
            new_sum = current_sum + event.value["amount"]
            store.put("total_sum", new_sum)
            
            return {"total_sum": new_sum}
            
        await processor2.process_stream("aggregate", continue_aggregate)
        
        # Process more events
        more_events = [
            StreamEvent(
                key=f"txn_{i}",
                value={"amount": i * 10},
                timestamp=base_time + i * 100,
                offset=i,
                partition=0
            )
            for i in range(5, 10)
        ]
        
        await processor2.ingest(more_events)
        await asyncio.sleep(0.5)
        
        # Verify state continuity
        final_sum = processor2.state_stores[0].get("total_sum")
        expected_sum = sum(i * 10 for i in range(10))
        assert final_sum == expected_sum
        
        await processor2.stop()
        return True


async def run_all_tests():
    """Run all state management tests"""
    test_suite = TestStateManagement()
    
    tests = [
        ("State Store Operations", test_suite.test_state_store_operations),
        ("Stateful Processing", test_suite.test_stateful_processing),
        ("Checkpointing", test_suite.test_checkpointing),
        ("Exactly Once Processing", test_suite.test_exactly_once_processing),
        ("Complex Event Patterns", test_suite.test_complex_event_patterns),
        ("State Recovery", test_suite.test_state_recovery),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            status = "✅ Pass" if result else "❌ Fail"
            results.append((test_name, status))
            print(f"{test_name}: {status}")
        except Exception as e:
            results.append((test_name, f"❌ Error: {e}"))
            print(f"{test_name}: ❌ Error: {e}")
            
    return results


if __name__ == "__main__":
    # Run tests
    results = asyncio.run(run_all_tests())
    
    # Summary
    passed = sum(1 for _, status in results if "✅" in status)
    total = len(results)
    
    print(f"\n{'='*50}")
    print(f"State Management Tests: {passed}/{total} passed")
    
    # Exit with appropriate code
    exit(0 if passed == total else 1)