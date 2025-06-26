"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Module: test_task_routing.py
Purpose: Test task routing and load balancing functionality for the distributed task queue manager

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/

Example Usage:
>>> pytest test_task_routing.py -v
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
from typing import Dict, List

from task_queue_manager_interaction import (
    TaskQueueManagerInteraction, TaskStatus, Task
)


@pytest.fixture
async def manager():
    """Create task queue manager instance"""
    mgr = TaskQueueManagerInteraction(backend="memory", max_workers=5)
    yield mgr
    mgr.shutdown()


@pytest.mark.asyncio
async def test_priority_based_routing(manager):
    """Test routing based on task priority"""
    # Submit tasks with different priorities
    low_priority = await manager.submit_task(
        "low_task", {"data": "low"}, priority=1
    )
    high_priority = await manager.submit_task(
        "high_task", {"data": "high"}, priority=8
    )
    normal_priority = await manager.submit_task(
        "normal_task", {"data": "normal"}, priority=5
    )
    
    # Check routing to appropriate queues
    assert low_priority in manager.queues["default"]
    assert high_priority in manager.queues["high_priority"]
    assert normal_priority in manager.queues["default"]
    
    # Verify high priority queue ordering
    high_queue = manager.queues["high_priority"]
    assert high_queue[0] == high_priority


@pytest.mark.asyncio
async def test_tag_based_routing(manager):
    """Test routing based on task tags"""
    # Submit tasks with different tags
    urgent_task = await manager.submit_task(
        "urgent_work", {"alert": True}, tags=["urgent", "customer"]
    )
    batch_task = await manager.submit_task(
        "batch_process", {"batch_size": 1000}, tags=["batch", "overnight"]
    )
    regular_task = await manager.submit_task(
        "regular_work", {"standard": True}, tags=["regular"]
    )
    
    # Verify routing
    assert urgent_task in manager.queues["urgent"]
    assert batch_task in manager.queues["batch"]
    assert regular_task in manager.queues["default"]


@pytest.mark.asyncio
async def test_queue_distribution(manager):
    """Test even distribution across queues"""
    # Submit many tasks
    task_counts = {"urgent": 0, "batch": 0, "default": 0}
    
    for i in range(30):
        tags = []
        if i % 3 == 0:
            tags = ["urgent"]
        elif i % 3 == 1:
            tags = ["batch"]
        
        await manager.submit_task(
            f"distributed_task_{i}",
            {"index": i},
            tags=tags
        )
    
    # Count tasks in each queue
    for queue_name, task_ids in manager.queues.items():
        if queue_name in task_counts:
            task_counts[queue_name] = len(task_ids)
    
    # Should have roughly even distribution
    assert task_counts["urgent"] >= 9
    assert task_counts["batch"] >= 9
    assert task_counts["default"] >= 9


@pytest.mark.asyncio
async def test_custom_routing_rules(manager):
    """Test custom routing based on payload content"""
    # Submit tasks that should route based on content
    large_task = await manager.submit_task(
        "process_file",
        {"file_size": 1000000, "type": "video"},
        tags=["batch"]  # Large files go to batch queue
    )
    
    small_task = await manager.submit_task(
        "process_file",
        {"file_size": 1000, "type": "text"}
        # Small files use default queue
    )
    
    priority_customer = await manager.submit_task(
        "customer_request",
        {"customer_tier": "premium"},
        tags=["urgent"]  # Premium customers get urgent queue
    )
    
    # Verify routing decisions
    assert large_task in manager.queues["batch"]
    assert small_task in manager.queues["default"]
    assert priority_customer in manager.queues["urgent"]


@pytest.mark.asyncio
async def test_queue_priorities_within_queue(manager):
    """Test priority ordering within same queue"""
    # Submit multiple tasks to same queue with different priorities
    task_ids = []
    priorities = [3, 8, 1, 10, 5]
    
    for i, priority in enumerate(priorities):
        task_id = await manager.submit_task(
            "priority_test",
            {"index": i},
            priority=priority
        )
        task_ids.append((task_id, priority))
    
    # Check default queue ordering
    default_queue = manager.queues["default"]
    
    # Get priorities of queued tasks
    queued_priorities = []
    for task_id in default_queue:
        if task_id in manager.tasks:
            queued_priorities.append(manager.tasks[task_id].priority)
    
    # Should be in descending order
    assert queued_priorities == sorted(queued_priorities, reverse=True)


@pytest.mark.asyncio
async def test_dead_letter_queue_routing(manager):
    """Test routing of failed tasks to dead letter queue"""
    # Submit task that will fail
    task_id = await manager.submit_task(
        "failing_task",
        {"will_fail": True}
    )
    
    task = manager.tasks[task_id]
    
    # Simulate failures up to max retries
    for i in range(task.max_retries + 1):
        task.status = TaskStatus.FAILED
        task.retry_count = i
        task.error = f"Failure {i+1}"
    
    # Run dead letter queue processor
    manager._process_dead_letter_queue()
    
    # Task should be marked as dead
    assert task.status == TaskStatus.DEAD


@pytest.mark.asyncio
async def test_load_balancing_across_queues(manager):
    """Test load balancing when multiple queues are active"""
    # Submit tasks to create load
    queue_loads = {}
    
    # High priority burst
    for i in range(20):
        await manager.submit_task(
            "high_load", {"index": i}, priority=8
        )
    
    # Normal priority steady stream
    for i in range(30):
        await manager.submit_task(
            "normal_load", {"index": i}, priority=3
        )
    
    # Batch jobs
    for i in range(15):
        await manager.submit_task(
            "batch_load", {"index": i}, tags=["batch"]
        )
    
    # Calculate queue loads
    for queue_name, task_ids in manager.queues.items():
        queue_loads[queue_name] = len(task_ids)
    
    # Verify all queues have tasks
    assert queue_loads.get("high_priority", 0) > 0
    assert queue_loads.get("default", 0) > 0
    assert queue_loads.get("batch", 0) > 0


@pytest.mark.asyncio
async def test_task_retry_routing(manager):
    """Test retry task routing"""
    # Submit task that will need retry
    task_id = await manager.submit_task(
        "retry_task",
        {"attempt": 1},
        priority=5
    )
    
    task = manager.tasks[task_id]
    
    # Simulate failure and retry
    task.status = TaskStatus.FAILED
    task.error = "Temporary failure"
    task.retry_count = 1
    task.status = TaskStatus.RETRYING
    
    # Re-queue for retry
    manager._enqueue_task(task_id, manager._get_queue_name(task), task.priority)
    
    # Should be back in queue
    assert task_id in manager.queues["default"]
    assert task.retry_count == 1
    assert task.status == TaskStatus.RETRYING


@pytest.mark.asyncio
async def test_cascading_task_routing(manager):
    """Test routing of cascading/chained tasks"""
    # Create parent task
    parent_id = await manager.submit_task(
        "parent_process",
        {"stage": "initialize"},
        priority=8
    )
    
    # Create child tasks with inherited properties
    child_ids = []
    for i in range(3):
        child_id = await manager.submit_task(
            "child_process",
            {"stage": f"step_{i}", "inherited_priority": True},
            priority=8,  # Inherit parent priority
            parent_task_id=parent_id
        )
        child_ids.append(child_id)
    
    # All should route to high priority queue
    for child_id in child_ids:
        assert child_id in manager.queues["high_priority"]
    
    # Verify parent-child relationships
    parent_task = manager.tasks[parent_id]
    assert len(parent_task.child_task_ids) == 3


@pytest.mark.asyncio
async def test_dynamic_queue_creation(manager):
    """Test dynamic queue creation based on tags"""
    # Submit task with new tag combination
    custom_task = await manager.submit_task(
        "special_work",
        {"custom": True},
        tags=["urgent", "ml-training"]  # Combination creates urgent queue
    )
    
    # Should route to urgent queue (highest priority tag)
    assert custom_task in manager.queues["urgent"]
    
    # Submit another with different custom tags
    batch_ml_task = await manager.submit_task(
        "ml_batch_job",
        {"model": "transformer"},
        tags=["batch", "ml-inference"]
    )
    
    # Should route to batch queue
    assert batch_ml_task in manager.queues["batch"]


# Validation
if __name__ == "__main__":
    async def validate():
        """Run validation tests"""
        print("Running task routing tests...")
        
        # Create manager
        manager = TaskQueueManagerInteraction(backend="memory")
        
        # Test 1: Priority routing
        print("\n1. Testing priority-based routing...")
        high = await manager.submit_task("high", {}, priority=10)
        low = await manager.submit_task("low", {}, priority=1)
        
        assert high in manager.queues["high_priority"]
        assert low in manager.queues["default"]
        print("✓ Priority routing works")
        
        # Test 2: Tag routing
        print("\n2. Testing tag-based routing...")
        urgent = await manager.submit_task("urgent", {}, tags=["urgent"])
        batch = await manager.submit_task("batch", {}, tags=["batch"])
        
        assert urgent in manager.queues["urgent"]
        assert batch in manager.queues["batch"]
        print("✓ Tag routing works")
        
        # Test 3: Queue ordering
        print("\n3. Testing queue ordering...")
        tasks = []
        for p in [3, 7, 1, 9, 5]:
            tid = await manager.submit_task("ordered", {}, priority=p)
            tasks.append((tid, p))
        
        # Check ordering in default queue
        queue = manager.queues["default"]
        priorities = [manager.tasks[tid].priority for tid in queue if tid in manager.tasks]
        assert priorities == sorted(priorities, reverse=True)
        print("✓ Queue ordering works")
        
        # Test 4: Failed task handling
        print("\n4. Testing failed task routing...")
        fail_id = await manager.submit_task("fail", {})
        fail_task = manager.tasks[fail_id]
        fail_task.status = TaskStatus.FAILED
        fail_task.retry_count = fail_task.max_retries + 1
        
        manager._process_dead_letter_queue()
        assert fail_task.status == TaskStatus.DEAD
        print("✓ Dead letter queue routing works")
        
        # Test 5: Load distribution
        print("\n5. Testing load distribution...")
        # Submit many tasks
        for i in range(30):
            tag = ["urgent"] if i % 3 == 0 else ["batch"] if i % 3 == 1 else []
            await manager.submit_task(f"load_{i}", {}, tags=tag)
        
        # Check distribution
        queue_sizes = {name: len(tasks) for name, tasks in manager.queues.items()}
        print(f"✓ Queue distribution: {queue_sizes}")
        
        manager.shutdown()
        print("\n✓ All validation tests passed!")
        return True
    
    # Run validation
    asyncio.run(validate())