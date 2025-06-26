#!/usr/bin/env python3
"""
Module: test_windowing.py
Purpose: Test windowing operations in stream processing

External Dependencies:
- asyncio: https://docs.python.org/3/library/asyncio.html
- pytest: https://docs.pytest.org/

Example Usage:
>>> pytest test_windowing.py -v
"""

import asyncio
import time
from typing import List, Dict, Any
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stream_processor_interaction import (
    StreamProcessor, StreamEvent, WindowSpec, StreamAggregator
)


class TestWindowing:
    """Test suite for windowing operations"""
    
    async def test_tumbling_windows(self):
        """Test tumbling window functionality"""
        processor = StreamProcessor(num_partitions=2)
        results = []
        processor.add_output_sink(lambda x: results.append(x))
        
        await processor.start()
        
        # Create window spec (1 second tumbling windows)
        window_spec = WindowSpec(size_ms=1000)
        
        # Process function to count events per window
        def count_per_window(events: List[StreamEvent]) -> Dict:
            return {
                "window_start": window_spec.get_window_start(events[0].timestamp),
                "count": len(events),
                "keys": [e.key for e in events]
            }
            
        # Start processing
        await processor.process_stream("test", count_per_window, window_spec)
        
        # Generate events across multiple windows
        base_time = int(time.time() * 1000)
        events = []
        
        # Window 1: 0-1000ms (5 events)
        for i in range(5):
            events.append(StreamEvent(
                key=f"key_{i}",
                value={"data": i},
                timestamp=base_time + i * 150,
                offset=i
            ))
            
        # Window 2: 1000-2000ms (3 events)
        for i in range(5, 8):
            events.append(StreamEvent(
                key=f"key_{i}",
                value={"data": i},
                timestamp=base_time + 1000 + (i-5) * 200,
                offset=i
            ))
            
        # Ingest events
        await processor.ingest(events)
        
        # Force watermark advance
        future_event = StreamEvent(
            key="future",
            value={},
            timestamp=base_time + 5000,
            offset=100
        )
        await processor.ingest([future_event])
        
        # Wait for processing
        await asyncio.sleep(1)
        
        # Verify window results
        window_counts = [r["count"] for r in results if "count" in r]
        assert 5 in window_counts  # First window
        assert 3 in window_counts  # Second window
        
        await processor.stop()
        return True
        
    async def test_sliding_windows(self):
        """Test sliding window functionality"""
        processor = StreamProcessor()
        results = []
        processor.add_output_sink(lambda x: results.append(x))
        
        await processor.start()
        
        # Create sliding window spec (size=1000ms, slide=500ms)
        window_spec = WindowSpec(size_ms=1000, slide_ms=500)
        
        # Process function
        def sum_in_window(events: List[StreamEvent]) -> Dict:
            total = sum(e.value["amount"] for e in events)
            return {
                "window_start": window_spec.get_window_start(events[0].timestamp),
                "sum": total,
                "event_count": len(events)
            }
            
        await processor.process_stream("sliding", sum_in_window, window_spec)
        
        # Generate events
        base_time = int(time.time() * 1000)
        events = []
        
        for i in range(10):
            events.append(StreamEvent(
                key=f"item_{i}",
                value={"amount": i * 10},
                timestamp=base_time + i * 200,  # Every 200ms
                offset=i
            ))
            
        await processor.ingest(events)
        
        # Advance watermark
        await processor.ingest([StreamEvent(
            key="advance",
            value={},
            timestamp=base_time + 5000,
            offset=100
        )])
        
        await asyncio.sleep(1)
        
        # Verify overlapping windows
        assert len(results) > 0
        sums = [r["sum"] for r in results if "sum" in r]
        assert len(sums) >= 2  # Should have multiple windows
        
        await processor.stop()
        return True
        
    async def test_window_aggregations(self):
        """Test various aggregation functions on windows"""
        processor = StreamProcessor()
        results = []
        processor.add_output_sink(lambda x: results.append(x))
        
        await processor.start()
        
        window_spec = WindowSpec(size_ms=2000)
        
        # Comprehensive aggregation function
        def aggregate_metrics(events: List[StreamEvent]) -> Dict:
            values = [e.value["metric"] for e in events]
            return {
                "window_start": window_spec.get_window_start(events[0].timestamp),
                "count": StreamAggregator.count(events),
                "sum": sum(values),
                "avg": StreamAggregator.avg(events, lambda e: e.value["metric"]),
                "min": min(values) if values else None,
                "max": max(values) if values else None,
            }
            
        await processor.process_stream("metrics", aggregate_metrics, window_spec)
        
        # Generate test data
        base_time = int(time.time() * 1000)
        events = []
        
        # Create events with varying metrics
        metrics = [10, 20, 30, 40, 50, 15, 25, 35]
        for i, metric in enumerate(metrics):
            events.append(StreamEvent(
                key=f"sensor_{i % 3}",
                value={"metric": metric},
                timestamp=base_time + i * 200,
                offset=i
            ))
            
        await processor.ingest(events)
        
        # Advance watermark
        await processor.ingest([StreamEvent(
            key="advance",
            value={},
            timestamp=base_time + 5000,
            offset=100
        )])
        
        await asyncio.sleep(1)
        
        # Verify aggregations
        for result in results:
            if "count" in result:
                assert result["count"] > 0
                assert result["sum"] > 0
                assert result["avg"] > 0
                assert result["min"] is not None
                assert result["max"] is not None
                assert result["min"] <= result["avg"] <= result["max"]
                
        await processor.stop()
        return True
        
    async def test_late_data_handling(self):
        """Test handling of late arriving data"""
        processor = StreamProcessor()
        results = []
        processor.add_output_sink(lambda x: results.append(x))
        
        await processor.start()
        
        window_spec = WindowSpec(size_ms=1000)
        
        # Count events per window
        def count_events(events: List[StreamEvent]) -> Dict:
            return {
                "window_start": window_spec.get_window_start(events[0].timestamp),
                "count": len(events),
                "late_events": sum(1 for e in events if processor.event_time.is_late(e.timestamp))
            }
            
        await processor.process_stream("late_test", count_events, window_spec)
        
        base_time = int(time.time() * 1000)
        
        # Send normal events
        normal_events = [
            StreamEvent(f"key_{i}", {"data": i}, base_time + i * 100, offset=i)
            for i in range(5)
        ]
        await processor.ingest(normal_events)
        
        # Advance watermark significantly
        await processor.ingest([StreamEvent(
            "advance", {}, base_time + 5000, offset=10
        )])
        
        # Send late event (timestamp before watermark)
        late_event = StreamEvent(
            "late_key", {"data": "late"}, base_time + 100, offset=11
        )
        await processor.ingest([late_event])
        
        await asyncio.sleep(1)
        
        # Check metrics for late events
        metrics = processor.get_metrics()
        assert metrics["late_events"] >= 1
        
        await processor.stop()
        return True
        
    async def test_window_watermark_progress(self):
        """Test watermark progression and window completion"""
        processor = StreamProcessor()
        completed_windows = []
        
        def track_windows(result):
            if "window_complete" in result:
                completed_windows.append(result)
                
        processor.add_output_sink(track_windows)
        await processor.start()
        
        window_spec = WindowSpec(size_ms=1000)
        
        # Track window completion
        def mark_complete(events: List[StreamEvent]) -> Dict:
            window_start = window_spec.get_window_start(events[0].timestamp)
            return {
                "window_complete": True,
                "window_start": window_start,
                "window_end": window_spec.get_window_end(window_start),
                "event_count": len(events)
            }
            
        await processor.process_stream("watermark_test", mark_complete, window_spec)
        
        base_time = int(time.time() * 1000)
        
        # Send events in order to advance watermark
        for i in range(20):
            event = StreamEvent(
                key=f"key_{i}",
                value={"seq": i},
                timestamp=base_time + i * 300,
                offset=i
            )
            await processor.ingest([event])
            await asyncio.sleep(0.05)
            
        # Final event to complete all windows
        await processor.ingest([StreamEvent(
            "final", {}, base_time + 10000, offset=100
        )])
        
        await asyncio.sleep(1)
        
        # Verify windows completed in order
        assert len(completed_windows) > 0
        
        # Check windows are completed in chronological order
        window_starts = [w["window_start"] for w in completed_windows]
        assert window_starts == sorted(window_starts)
        
        await processor.stop()
        return True


async def run_all_tests():
    """Run all windowing tests"""
    test_suite = TestWindowing()
    
    tests = [
        ("Tumbling Windows", test_suite.test_tumbling_windows),
        ("Sliding Windows", test_suite.test_sliding_windows),
        ("Window Aggregations", test_suite.test_window_aggregations),
        ("Late Data Handling", test_suite.test_late_data_handling),
        ("Watermark Progress", test_suite.test_window_watermark_progress),
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
    print(f"Windowing Tests: {passed}/{total} passed")
    
    # Exit with appropriate code
    exit(0 if passed == total else 1)