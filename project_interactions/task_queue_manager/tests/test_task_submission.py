"""
Module: test_task_submission.py
Purpose: Test task submission functionality for the distributed task queue manager

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/

Example Usage:
>>> pytest test_task_submission.py -v
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
import asyncio
from datetime import datetime
import uuid
from typing import Dict, Any

from task_queue_manager_interaction import (
    TaskQueueManagerInteraction, TaskStatus, Task
)


@pytest.fixture
async def manager():
    """Create task queue manager instance"""
    mgr = TaskQueueManagerInteraction(backend="memory", max_workers=3)
    yield mgr
    mgr.shutdown()


@pytest.mark.asyncio
async def test_basic_task_submission(manager):
    """Test basic task submission"""
    task_id = await manager.submit_task(
        "test_task",
        {"data": "test_payload"},
        priority=5
    )
    
    assert task_id is not None
    assert task_id in manager.tasks
    task = manager.tasks[task_id]
    assert task.name == "test_task"
    assert task.payload == {"data": "test_payload"}
    assert task.priority == 5
    assert task.status == TaskStatus.PENDING


@pytest.mark.asyncio
async def test_high_priority_task(manager):
    """Test high priority task queuing"""
    # Submit low priority tasks
    low_ids = []
    for i in range(3):
        task_id = await manager.submit_task(
            "low_priority",
            {"index": i},
            priority=1
        )
        low_ids.append(task_id)
    
    # Submit high priority task
    high_id = await manager.submit_task(
        "high_priority",
        {"urgent": True},
        priority=10
    )
    
    # Check queue order
    default_queue = manager.queues["high_priority"]
    assert high_id in default_queue
    assert default_queue[0] == high_id  # Should be first


@pytest.mark.asyncio
async def test_delayed_task_submission(manager):
    """Test delayed task submission"""
    delay_seconds = 1
    task_id = await manager.submit_task(
        "delayed_task",
        {"delay": delay_seconds},
        delay=delay_seconds
    )
    
    assert task_id is not None
    assert task_id in manager.tasks
    
    # Task should not be in queue immediately
    all_queued_tasks = []
    for queue_tasks in manager.queues.values():
        all_queued_tasks.extend(queue_tasks)
    assert task_id not in all_queued_tasks
    
    # Wait for delay
    await asyncio.sleep(delay_seconds + 0.5)
    
    # Now task should be queued
    all_queued_tasks = []
    for queue_tasks in manager.queues.values():
        all_queued_tasks.extend(queue_tasks)
    assert task_id in all_queued_tasks


@pytest.mark.asyncio
async def test_task_chaining(manager):
    """Test parent-child task relationships"""
    # Create parent task
    parent_id = await manager.submit_task(
        "parent_task",
        {"step": "initialize"}
    )
    
    # Create child tasks
    child_ids = []
    for i in range(3):
        child_id = await manager.submit_task(
            "child_task",
            {"step": f"process_{i}"},
            parent_task_id=parent_id
        )
        child_ids.append(child_id)
    
    # Verify relationships
    parent_task = manager.tasks[parent_id]
    assert len(parent_task.child_task_ids) == 3
    assert set(parent_task.child_task_ids) == set(child_ids)
    
    # Verify child tasks have parent reference
    for child_id in child_ids:
        child_task = manager.tasks[child_id]
        assert child_task.parent_task_id == parent_id


@pytest.mark.asyncio
async def test_task_deduplication(manager):
    """Test task deduplication"""
    dedupe_key = "unique-task-123"
    
    # Submit first task
    task_id1 = await manager.submit_task(
        "dedup_task",
        {"data": "first"},
        dedupe_key=dedupe_key
    )
    
    # Try to submit duplicate
    task_id2 = await manager.submit_task(
        "dedup_task",
        {"data": "second"},
        dedupe_key=dedupe_key
    )
    
    assert task_id1 is not None
    assert task_id2 is None  # Should be rejected
    assert dedupe_key in manager.dedup_cache


@pytest.mark.asyncio
async def test_task_routing_by_tags(manager):
    """Test task routing based on tags"""
    # Submit urgent task
    urgent_id = await manager.submit_task(
        "urgent_work",
        {"priority": "high"},
        tags=["urgent"]
    )
    
    # Submit batch task
    batch_id = await manager.submit_task(
        "batch_process",
        {"type": "batch"},
        tags=["batch"]
    )
    
    # Submit normal task
    normal_id = await manager.submit_task(
        "normal_work",
        {"type": "regular"}
    )
    
    # Verify routing
    assert urgent_id in manager.queues["urgent"]
    assert batch_id in manager.queues["batch"]
    assert normal_id in manager.queues["default"]


@pytest.mark.asyncio
async def test_rate_limiting(manager):
    """Test rate limiting functionality"""
    task_name = "rate_limited_task"
    submitted_count = 0
    rejected_count = 0
    
    # Try to submit many tasks quickly
    for i in range(150):  # Try to exceed limit of 100/minute
        try:
            await manager.submit_task(task_name, {"index": i})
            submitted_count += 1
        except ValueError as e:
            if "Rate limit exceeded" in str(e):
                rejected_count += 1
    
    # Should have some successful and some rejected
    assert submitted_count > 0
    assert submitted_count == 100  # Rate limit
    assert rejected_count > 0


@pytest.mark.asyncio
async def test_task_metadata(manager):
    """Test task metadata and attributes"""
    tags = ["important", "customer-facing", "v2"]
    task_id = await manager.submit_task(
        "metadata_task",
        {"customer_id": "12345"},
        priority=8,
        tags=tags
    )
    
    task = manager.tasks[task_id]
    assert task.tags == tags
    assert task.created_at is not None
    assert isinstance(task.created_at, datetime)
    assert task.retry_count == 0
    assert task.max_retries == 3


@pytest.mark.asyncio
async def test_bulk_submission(manager):
    """Test bulk task submission"""
    task_count = 50
    task_ids = []
    
    start_time = asyncio.get_event_loop().time()
    
    # Submit many tasks
    for i in range(task_count):
        task_id = await manager.submit_task(
            f"bulk_task_{i % 5}",  # Vary task names
            {"index": i, "data": f"payload_{i}"},
            priority=i % 10  # Vary priorities
        )
        task_ids.append(task_id)
    
    end_time = asyncio.get_event_loop().time()
    duration = end_time - start_time
    
    # Verify all submitted
    assert len(task_ids) == task_count
    assert all(tid in manager.tasks for tid in task_ids)
    
    # Should be reasonably fast
    assert duration < 1.0, f"Bulk submission too slow: {duration}s"
    
    # Check queue distribution
    total_queued = sum(len(queue) for queue in manager.queues.values())
    assert total_queued == task_count


# Validation
if __name__ == "__main__":
    async def validate():
        """Run validation tests"""
        print("Running task submission tests...")
        
        # Create manager
        manager = TaskQueueManagerInteraction(backend="memory")
        
        # Test 1: Basic submission
        print("\n1. Testing basic task submission...")
        task_id = await manager.submit_task(
            "validation_task",
            {"test": True}
        )
        assert task_id in manager.tasks
        print("✓ Basic submission works")
        
        # Test 2: Priority ordering
        print("\n2. Testing priority ordering...")
        ids = []
        for priority in [1, 10, 5]:
            tid = await manager.submit_task(
                "priority_test",
                {"priority": priority},
                priority=priority
            )
            ids.append(tid)
        
        # High priority should be first in queue
        queue = manager.queues["high_priority"]
        assert queue[0] == ids[1]  # Priority 10
        print("✓ Priority ordering works")
        
        # Test 3: Task chaining
        print("\n3. Testing task chaining...")
        parent = await manager.submit_task("parent", {})
        child1 = await manager.submit_task("child", {}, parent_task_id=parent)
        child2 = await manager.submit_task("child", {}, parent_task_id=parent)
        
        assert len(manager.tasks[parent].child_task_ids) == 2
        print("✓ Task chaining works")
        
        # Test 4: Deduplication
        print("\n4. Testing deduplication...")
        dup1 = await manager.submit_task("dup", {}, dedupe_key="test-dup")
        dup2 = await manager.submit_task("dup", {}, dedupe_key="test-dup")
        assert dup1 is not None and dup2 is None
        print("✓ Deduplication works")
        
        # Test 5: Tag routing
        print("\n5. Testing tag-based routing...")
        urgent = await manager.submit_task("urgent", {}, tags=["urgent"])
        batch = await manager.submit_task("batch", {}, tags=["batch"])
        
        assert urgent in manager.queues["urgent"]
        assert batch in manager.queues["batch"]
        print("✓ Tag routing works")
        
        manager.shutdown()
        print("\n✓ All validation tests passed!")
        return True
    
    # Run validation
    asyncio.run(validate())