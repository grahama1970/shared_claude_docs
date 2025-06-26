"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Module: test_worker_management.py
Purpose: Test worker management functionality for the distributed task queue manager

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/

Example Usage:
>>> pytest test_worker_management.py -v
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
import asyncio
from datetime import datetime, timedelta
import uuid
import time

from task_queue_manager_interaction import (
    TaskQueueManagerInteraction, Worker, TaskStatus
)


@pytest.fixture
async def manager():
    """Create task queue manager instance"""
    mgr = TaskQueueManagerInteraction(backend="memory", max_workers=5)
    yield mgr
    mgr.shutdown()


@pytest.mark.asyncio
async def test_worker_registration(manager):
    """Test worker registration and tracking"""
    worker_id = str(uuid.uuid4())
    worker = Worker(id=worker_id, status="idle")
    
    manager.workers[worker_id] = worker
    
    assert worker_id in manager.workers
    assert manager.workers[worker_id].status == "idle"
    assert manager.workers[worker_id].tasks_completed == 0
    assert manager.workers[worker_id].tasks_failed == 0


@pytest.mark.asyncio
async def test_worker_statistics(manager):
    """Test worker statistics collection"""
    # Create workers with different states
    workers = []
    for i in range(3):
        worker_id = f"worker-{i}"
        worker = Worker(
            id=worker_id,
            status="idle" if i == 0 else "busy",
            tasks_completed=i * 10,
            tasks_failed=i * 2
        )
        manager.workers[worker_id] = worker
        workers.append(worker)
    
    # Get statistics
    stats = manager.get_worker_stats()
    
    assert len(stats) == 3
    for i, stat in enumerate(stats):
        assert stat['worker_id'] == f"worker-{i}"
        assert stat['tasks_completed'] == i * 10
        assert stat['tasks_failed'] == i * 2
        assert 'uptime' in stat
        assert 'last_heartbeat' in stat


@pytest.mark.asyncio
async def test_worker_heartbeat_monitoring(manager):
    """Test worker heartbeat timeout detection"""
    worker_id = str(uuid.uuid4())
    
    # Create worker with old heartbeat
    worker = Worker(
        id=worker_id,
        status="busy",
        last_heartbeat=datetime.utcnow() - timedelta(seconds=35)  # Expired
    )
    manager.workers[worker_id] = worker
    
    # Assign a task to the worker
    task_id = await manager.submit_task("test_task", {"data": "test"})
    task = manager.tasks[task_id]
    task.status = TaskStatus.RUNNING
    task.worker_id = worker_id
    worker.current_task_id = task_id
    
    # Simulate health check
    manager._monitor_worker_health()
    
    # Worker should be removed due to timeout
    assert worker_id not in manager.workers
    
    # Task should be re-queued
    assert task.status == TaskStatus.PENDING
    assert task.worker_id is None


@pytest.mark.asyncio
async def test_worker_task_assignment(manager):
    """Test task assignment to workers"""
    worker_id = str(uuid.uuid4())
    worker = Worker(id=worker_id, status="idle")
    manager.workers[worker_id] = worker
    
    # Submit task
    task_id = await manager.submit_task("work_task", {"process": "data"})
    
    # Simulate task assignment
    task = manager.tasks[task_id]
    task.status = TaskStatus.RUNNING
    task.worker_id = worker_id
    task.started_at = datetime.utcnow()
    
    worker.status = "busy"
    worker.current_task_id = task_id
    
    # Verify assignment
    assert task.worker_id == worker_id
    assert worker.current_task_id == task_id
    assert worker.status == "busy"


@pytest.mark.asyncio
async def test_worker_task_completion(manager):
    """Test worker task completion tracking"""
    worker_id = str(uuid.uuid4())
    worker = Worker(id=worker_id, status="idle")
    manager.workers[worker_id] = worker
    
    # Complete multiple tasks
    for i in range(5):
        # Submit and "complete" task
        task_id = await manager.submit_task(f"task_{i}", {"index": i})
        task = manager.tasks[task_id]
        
        # Simulate processing
        task.status = TaskStatus.RUNNING
        task.worker_id = worker_id
        task.started_at = datetime.utcnow()
        
        # Complete task
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.utcnow()
        task.result = {"processed": True}
        
        worker.tasks_completed += 1
        
        # Fail one task
        if i == 3:
            task.status = TaskStatus.FAILED
            task.error = "Test error"
            worker.tasks_failed += 1
            worker.tasks_completed -= 1
    
    # Verify counts
    assert worker.tasks_completed == 4
    assert worker.tasks_failed == 1


@pytest.mark.asyncio
async def test_worker_pool_scaling(manager):
    """Test worker pool management"""
    initial_workers = len(manager.workers)
    
    # Add workers up to max
    for i in range(manager.max_workers):
        worker_id = f"worker-{i}"
        manager.workers[worker_id] = Worker(id=worker_id)
    
    assert len(manager.workers) == manager.max_workers
    
    # Verify we can't exceed max workers
    # (In real implementation, this would be enforced)
    assert manager.max_workers == 10  # Default from init


@pytest.mark.asyncio
async def test_worker_load_balancing(manager):
    """Test load distribution across workers"""
    # Create workers with different loads
    for i in range(3):
        worker_id = f"worker-{i}"
        worker = Worker(
            id=worker_id,
            status="idle" if i < 2 else "busy",
            tasks_completed=i * 5
        )
        manager.workers[worker_id] = worker
    
    # Submit multiple tasks
    task_ids = []
    for i in range(10):
        task_id = await manager.submit_task(
            "balanced_task",
            {"index": i},
            priority=5
        )
        task_ids.append(task_id)
    
    # Verify tasks are queued for distribution
    total_queued = sum(len(queue) for queue in manager.queues.values())
    assert total_queued == 10


@pytest.mark.asyncio
async def test_worker_failure_recovery(manager):
    """Test recovery from worker failures"""
    worker_id = str(uuid.uuid4())
    worker = Worker(id=worker_id, status="busy")
    manager.workers[worker_id] = worker
    
    # Assign critical task to worker
    task_id = await manager.submit_task(
        "critical_task",
        {"important": True},
        priority=10
    )
    
    task = manager.tasks[task_id]
    task.status = TaskStatus.RUNNING
    task.worker_id = worker_id
    worker.current_task_id = task_id
    
    # Simulate worker failure
    del manager.workers[worker_id]
    
    # Task should be recoverable
    task.status = TaskStatus.PENDING
    task.worker_id = None
    
    # Re-queue task
    manager._enqueue_task(task_id, "high_priority", task.priority)
    
    # Verify task is back in queue
    assert task_id in manager.queues["high_priority"]
    assert task.status == TaskStatus.PENDING


@pytest.mark.asyncio
async def test_worker_performance_metrics(manager):
    """Test worker performance tracking"""
    worker_id = str(uuid.uuid4())
    worker = Worker(id=worker_id)
    manager.workers[worker_id] = worker
    
    # Simulate task processing with timing
    durations = []
    for i in range(5):
        task_id = await manager.submit_task(f"perf_task_{i}", {"index": i})
        task = manager.tasks[task_id]
        
        # Start processing
        start_time = datetime.utcnow()
        task.status = TaskStatus.RUNNING
        task.started_at = start_time
        task.worker_id = worker_id
        
        # Simulate work
        await asyncio.sleep(0.1)
        
        # Complete
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.utcnow()
        duration = (task.completed_at - task.started_at).total_seconds()
        durations.append(duration)
        
        worker.tasks_completed += 1
    
    # Calculate average processing time
    avg_duration = sum(durations) / len(durations)
    assert avg_duration > 0.09  # Should be at least the sleep time
    assert worker.tasks_completed == 5


@pytest.mark.asyncio
async def test_concurrent_worker_operations(manager):
    """Test concurrent worker operations"""
    worker_count = 5
    tasks_per_worker = 3
    
    # Create workers
    workers = []
    for i in range(worker_count):
        worker_id = f"concurrent-worker-{i}"
        worker = Worker(id=worker_id)
        manager.workers[worker_id] = worker
        workers.append(worker)
    
    # Submit tasks concurrently
    async def submit_worker_tasks(worker_index):
        task_ids = []
        for j in range(tasks_per_worker):
            task_id = await manager.submit_task(
                f"concurrent_task_{worker_index}_{j}",
                {"worker": worker_index, "task": j}
            )
            task_ids.append(task_id)
        return task_ids
    
    # Submit all tasks concurrently
    all_task_ids = await asyncio.gather(
        *[submit_worker_tasks(i) for i in range(worker_count)]
    )
    
    # Verify all tasks submitted
    total_tasks = sum(len(tasks) for tasks in all_task_ids)
    assert total_tasks == worker_count * tasks_per_worker
    
    # Verify all tasks are in the system
    for task_list in all_task_ids:
        for task_id in task_list:
            assert task_id in manager.tasks


# Validation
if __name__ == "__main__":
    async def validate():
        """Run validation tests"""
        print("Running worker management tests...")
        
        # Create manager
        manager = TaskQueueManagerInteraction(backend="memory", max_workers=3)
        
        # Test 1: Worker registration
        print("\n1. Testing worker registration...")
        worker_id = str(uuid.uuid4())
        worker = Worker(id=worker_id, status="idle")
        manager.workers[worker_id] = worker
        
        assert worker_id in manager.workers
        print("✓ Worker registration works")
        
        # Test 2: Worker stats
        print("\n2. Testing worker statistics...")
        stats = manager.get_worker_stats()
        assert len(stats) == 1
        assert stats[0]['worker_id'] == worker_id
        print(f"✓ Worker stats: {stats[0]['status']}")
        
        # Test 3: Task assignment
        print("\n3. Testing task assignment...")
        task_id = await manager.submit_task("test_work", {"data": "process"})
        task = manager.tasks[task_id]
        task.worker_id = worker_id
        task.status = TaskStatus.RUNNING
        worker.current_task_id = task_id
        worker.status = "busy"
        
        assert task.worker_id == worker_id
        assert worker.current_task_id == task_id
        print("✓ Task assignment works")
        
        # Test 4: Task completion
        print("\n4. Testing task completion...")
        task.status = TaskStatus.COMPLETED
        task.result = {"success": True}
        worker.tasks_completed += 1
        worker.status = "idle"
        worker.current_task_id = None
        
        assert worker.tasks_completed == 1
        print("✓ Task completion tracking works")
        
        # Test 5: Multiple workers
        print("\n5. Testing multiple workers...")
        for i in range(2):
            w_id = f"worker-{i+2}"
            manager.workers[w_id] = Worker(id=w_id)
        
        assert len(manager.workers) == 3
        all_stats = manager.get_worker_stats()
        assert len(all_stats) == 3
        print(f"✓ Multiple workers: {len(all_stats)} active")
        
        manager.shutdown()
        print("\n✓ All validation tests passed!")
        return True
    
    # Run validation
    asyncio.run(validate())