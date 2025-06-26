#!/usr/bin/env python3
"""
Module: test_stream_ingestion.py
Purpose: Test stream ingestion capabilities

External Dependencies:
- asyncio: https://docs.python.org/3/library/asyncio.html
- pytest: https://docs.pytest.org/

Example Usage:
>>> pytest test_stream_ingestion.py -v
"""

import asyncio
import time
from typing import List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stream_processor_interaction import (
    StreamProcessor, StreamEvent, StreamPartitioner
)


class TestStreamIngestion:
    """Test suite for stream ingestion"""
    
    async def test_basic_ingestion(self):
        """Test basic event ingestion"""
        processor = StreamProcessor(num_partitions=2)
        await processor.start()
        
        # Create test events
        events = [
            StreamEvent(
                key=f"key_{i}",
                value={"data": i},
                timestamp=int(time.time() * 1000) + i * 100,
                offset=i
            )
            for i in range(10)
        ]
        
        # Ingest events
        await processor.ingest(events)
        
        # Wait for processing
        await asyncio.sleep(0.5)
        
        # Check metrics
        metrics = processor.get_metrics()
        assert metrics["events_ingested"] == 10
        
        await processor.stop()
        return True
        
    async def test_partition_assignment(self):
        """Test automatic partition assignment"""
        processor = StreamProcessor(num_partitions=4)
        await processor.start()
        
        # Track partition distribution
        partition_counts = [0] * 4
        
        # Create events without partition assignment
        events = []
        for i in range(100):
            event = StreamEvent(
                key=f"key_{i}",
                value={"data": i},
                timestamp=int(time.time() * 1000) + i * 10,
                offset=i,
                partition=-1  # Let processor assign
            )
            events.append(event)
            
        # Ingest and check partition assignment
        await processor.ingest(events)
        
        # Count partition distribution
        for event in events:
            partition_counts[event.partition] += 1
            
        # Verify all partitions got events
        assert all(count > 0 for count in partition_counts)
        assert sum(partition_counts) == 100
        
        await processor.stop()
        return True
        
    async def test_late_event_detection(self):
        """Test late event detection based on watermarks"""
        processor = StreamProcessor()
        await processor.start()
        
        base_time = int(time.time() * 1000)
        
        # Create events with different timestamps
        events = [
            # Normal events
            StreamEvent("key1", {"data": 1}, base_time + 1000, offset=1),
            StreamEvent("key2", {"data": 2}, base_time + 2000, offset=2),
            StreamEvent("key3", {"data": 3}, base_time + 8000, offset=3),
            # Late event (timestamp before watermark)
            StreamEvent("key4", {"data": 4}, base_time + 500, offset=4),
        ]
        
        # Ingest events
        for event in events:
            await processor.ingest([event])
            await asyncio.sleep(0.1)
            
        # Check late event detection
        metrics = processor.get_metrics()
        assert metrics["late_events"] >= 1
        
        await processor.stop()
        return True
        
    async def test_high_throughput_ingestion(self):
        """Test high-throughput event ingestion"""
        processor = StreamProcessor(num_partitions=8)
        await processor.start()
        
        # Create large batch of events
        batch_size = 1000
        events = []
        base_time = int(time.time() * 1000)
        
        for i in range(batch_size):
            event = StreamEvent(
                key=f"key_{i % 100}",  # 100 unique keys
                value={"data": i, "batch": True},
                timestamp=base_time + i,
                offset=i
            )
            events.append(event)
            
        # Measure ingestion time
        start_time = time.time()
        await processor.ingest(events)
        ingestion_time = time.time() - start_time
        
        # Wait for processing
        await asyncio.sleep(1)
        
        # Verify all events ingested
        metrics = processor.get_metrics()
        assert metrics["events_ingested"] == batch_size
        
        # Check performance (should ingest 1000 events in < 1 second)
        assert ingestion_time < 1.0
        
        await processor.stop()
        return True
        
    async def test_concurrent_ingestion(self):
        """Test concurrent ingestion from multiple sources"""
        processor = StreamProcessor(num_partitions=4)
        await processor.start()
        
        # Define multiple data sources
        async def source_producer(source_id: int, count: int):
            events = []
            base_time = int(time.time() * 1000)
            
            for i in range(count):
                event = StreamEvent(
                    key=f"source_{source_id}_key_{i}",
                    value={"source": source_id, "seq": i},
                    timestamp=base_time + i * 100,
                    offset=i
                )
                events.append(event)
                
            await processor.ingest(events)
            
        # Run concurrent producers
        tasks = []
        num_sources = 5
        events_per_source = 20
        
        for source_id in range(num_sources):
            task = asyncio.create_task(
                source_producer(source_id, events_per_source)
            )
            tasks.append(task)
            
        # Wait for all producers
        await asyncio.gather(*tasks)
        await asyncio.sleep(0.5)
        
        # Verify total events
        metrics = processor.get_metrics()
        expected_total = num_sources * events_per_source
        assert metrics["events_ingested"] == expected_total
        
        await processor.stop()
        return True


async def run_all_tests():
    """Run all ingestion tests"""
    test_suite = TestStreamIngestion()
    
    tests = [
        ("Basic Ingestion", test_suite.test_basic_ingestion),
        ("Partition Assignment", test_suite.test_partition_assignment),
        ("Late Event Detection", test_suite.test_late_event_detection),
        ("High Throughput", test_suite.test_high_throughput_ingestion),
        ("Concurrent Ingestion", test_suite.test_concurrent_ingestion),
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
    print(f"Stream Ingestion Tests: {passed}/{total} passed")
    
    # Exit with appropriate code
    exit(0 if passed == total else 1)