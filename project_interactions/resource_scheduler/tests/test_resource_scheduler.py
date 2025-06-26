"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Test suite for Resource Optimization Scheduler
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import asyncio
import pytest
import time
# REMOVED: # REMOVED: from unittest.mock import Mock, patch

from project_interactions.resource_scheduler.resource_scheduler_interaction import (
    ResourceScheduler,
    SchedulingAlgorithm,
    ResourceRequirements,
    JobStatus,
    ResourceType,
    ResourceNode,
    Job
)


class TestResourceScheduler:
    """Test cases for ResourceScheduler"""
    
    @pytest.mark.asyncio
    async def test_job_submission(self):
        """Test basic job submission"""
        scheduler = ResourceScheduler()
        
        job_id = scheduler.submit_job(
            module="test_module",
            priority=5,
            requirements=ResourceRequirements(cpu_cores=2)
        )
        
        assert job_id in scheduler.jobs
        assert scheduler.jobs[job_id].module == "test_module"
        assert scheduler.jobs[job_id].priority == 5
        assert scheduler.jobs[job_id].status == JobStatus.QUEUED
    
    @pytest.mark.asyncio
    async def test_priority_scheduling_order(self):
        """Test that jobs are scheduled in priority order"""
        scheduler = ResourceScheduler(SchedulingAlgorithm.PRIORITY_BASED)
        
        # Submit jobs with different priorities
        low = scheduler.submit_job("low", priority=2)
        high = scheduler.submit_job("high", priority=9)
        medium = scheduler.submit_job("medium", priority=5)
        
        await scheduler.start()
        await asyncio.sleep(0.5)
        
        # High priority should run first
        assert scheduler.jobs[high].status == JobStatus.RUNNING
        
        await scheduler.stop()
    
    @pytest.mark.asyncio
    async def test_resource_allocation(self):
        """Test resource allocation and deallocation"""
        scheduler = ResourceScheduler()
        node = scheduler.nodes["local"]
        initial_cpu = node.available_resources[ResourceType.CPU]
        
        job_id = scheduler.submit_job(
            "test",
            requirements=ResourceRequirements(cpu_cores=2)
        )
        
        await scheduler.start()
        await asyncio.sleep(0.5)
        
        # Check resources were allocated
        assert node.available_resources[ResourceType.CPU] == initial_cpu - 2
        assert job_id in node.running_jobs
        
        await scheduler.stop()
    
    @pytest.mark.asyncio
    async def test_job_completion(self):
        """Test job completion and resource release"""
        scheduler = ResourceScheduler()
        
        job_id = scheduler.submit_job(
            "quick_job",
            estimated_duration=1  # 1 second
        )
        
        await scheduler.start()
        await asyncio.sleep(2)  # Wait for completion
        
        job = scheduler.jobs[job_id]
        assert job.status == JobStatus.COMPLETED
        assert job.progress == 100.0
        assert job.completed_at is not None
        
        await scheduler.stop()
    
    @pytest.mark.asyncio
    async def test_deadline_priority_boost(self):
        """Test that approaching deadlines boost priority"""
        scheduler = ResourceScheduler(SchedulingAlgorithm.DEADLINE_AWARE)
        
        job_id = scheduler.submit_job(
            "deadline_job",
            priority=5,
            deadline=2  # 2 seconds
        )
        
        await scheduler.start()
        
        initial_priority = scheduler.jobs[job_id].priority
        await asyncio.sleep(1.5)  # Wait until close to deadline
        
        # Priority should be boosted
        assert scheduler.jobs[job_id].priority > initial_priority
        
        await scheduler.stop()
    
    @pytest.mark.asyncio
    async def test_fair_share_distribution(self):
        """Test fair-share scheduling distributes across modules"""
        scheduler = ResourceScheduler(SchedulingAlgorithm.FAIR_SHARE)
        
        # Submit multiple jobs from different modules
        module_a_jobs = [
            scheduler.submit_job("module_a", estimated_duration=1) 
            for _ in range(3)
        ]
        module_b_jobs = [
            scheduler.submit_job("module_b", estimated_duration=1)
        ]
        
        await scheduler.start()
        await asyncio.sleep(0.5)
        
        # Check that module_b gets resources despite fewer jobs
        module_b_running = any(
            scheduler.jobs[j].status == JobStatus.RUNNING 
            for j in module_b_jobs
        )
        
        assert module_b_running or len(scheduler.nodes) == 1
        
        await scheduler.stop()
    
    @pytest.mark.asyncio
    async def test_job_cancellation(self):
        """Test job cancellation"""
        scheduler = ResourceScheduler()
        
        job_id = scheduler.submit_job("cancel_test")
        await scheduler.start()
        await asyncio.sleep(0.5)
        
        # Cancel the job
        result = scheduler.cancel_job(job_id)
        assert result is True
        assert scheduler.jobs[job_id].status == JobStatus.FAILED
        
        await scheduler.stop()
    
    @pytest.mark.asyncio
    async def test_pause_resume(self):
        """Test job pause and resume functionality"""
        scheduler = ResourceScheduler()
        
        job_id = scheduler.submit_job(
            "pause_test",
            estimated_duration=10
        )
        
        await scheduler.start()
        await asyncio.sleep(0.5)
        
        # Pause job
        assert scheduler.pause_job(job_id) is True
        assert scheduler.jobs[job_id].status == JobStatus.PAUSED
        
        # Resume job
        assert scheduler.resume_job(job_id) is True
        assert scheduler.jobs[job_id].status == JobStatus.RUNNING
        
        await scheduler.stop()
    
    @pytest.mark.asyncio
    async def test_node_addition_removal(self):
        """Test dynamic node addition and removal"""
        scheduler = ResourceScheduler()
        
        # Add a new node
        new_node = ResourceNode(
            id="test_node",
            total_resources={
                ResourceType.CPU: 4,
                ResourceType.MEMORY: 8192,
                ResourceType.GPU: 0,
                ResourceType.NETWORK: 100,
                ResourceType.DISK_IO: 100
            },
            available_resources={
                ResourceType.CPU: 4,
                ResourceType.MEMORY: 8192,
                ResourceType.GPU: 0,
                ResourceType.NETWORK: 100,
                ResourceType.DISK_IO: 100
            }
        )
        
        scheduler.add_node(new_node)
        assert "test_node" in scheduler.nodes
        
        # Remove node
        scheduler.remove_node("test_node")
        assert "test_node" not in scheduler.nodes
    
    @pytest.mark.asyncio
    async def test_cost_optimization(self):
        """Test cost-optimized scheduling prefers cheaper nodes"""
        scheduler = ResourceScheduler(SchedulingAlgorithm.COST_OPTIMIZED)
        
        # Submit jobs that fit on local node
        jobs = [
            scheduler.submit_job(f"cost_test_{i}", 
                               requirements=ResourceRequirements(cpu_cores=0.5))
            for i in range(3)
        ]
        
        await scheduler.start()
        await asyncio.sleep(0.5)
        
        # Check jobs prefer local (cheaper) node
        local_jobs = sum(
            1 for j in jobs 
            if scheduler.jobs[j].allocated_node == "local" 
            and scheduler.jobs[j].status == JobStatus.RUNNING
        )
        
        assert local_jobs > 0
        
        await scheduler.stop()
    
    @pytest.mark.asyncio
    async def test_resource_monitoring(self):
        """Test resource monitoring functionality"""
        scheduler = ResourceScheduler()
        
        await scheduler.start()
        await asyncio.sleep(2)  # Let monitoring collect data
        
        # Check monitoring data
        assert len(scheduler.monitor.history['cpu']) > 0
        assert len(scheduler.monitor.history['memory']) > 0
        
        # Check current usage
        usage = scheduler.monitor.get_current_usage()
        assert ResourceType.CPU in usage
        assert ResourceType.MEMORY in usage
        assert usage[ResourceType.CPU] >= 0
        
        await scheduler.stop()
    
    @pytest.mark.asyncio
    async def test_scheduler_stats(self):
        """Test scheduler statistics"""
        scheduler = ResourceScheduler()
        
        # Submit some jobs
        for i in range(5):
            scheduler.submit_job(f"stats_test_{i}")
        
        await scheduler.start()
        await asyncio.sleep(0.5)
        
        stats = scheduler.get_scheduler_stats()
        
        assert stats["total_jobs"] == 5
        assert stats["queued_jobs"] >= 0
        assert stats["running_jobs"] >= 0
        assert stats["completed_jobs"] >= 0
        assert stats["queued_jobs"] + stats["running_jobs"] + stats["completed_jobs"] == 5
        assert "resource_utilization" in stats
        assert stats["algorithm"] == SchedulingAlgorithm.PRIORITY_BASED.value
        
        await scheduler.stop()
    
    @pytest.mark.asyncio
    async def test_job_start_time_prediction(self):
        """Test job start time prediction"""
        scheduler = ResourceScheduler()
        
        # Fill up resources
        for i in range(10):
            scheduler.submit_job(f"blocking_{i}", estimated_duration=10)
        
        # Submit a job that will be queued
        queued_job = scheduler.submit_job("queued", estimated_duration=5)
        
        prediction = scheduler.predict_job_start_time(queued_job)
        assert prediction is not None
        assert prediction > time.time()  # Should be in the future
    
    @pytest.mark.asyncio
    async def test_job_migration(self):
        """Test job migration between nodes"""
        scheduler = ResourceScheduler()
        
        # Submit a job
        job_id = scheduler.submit_job(
            "migration_test",
            requirements=ResourceRequirements(cpu_cores=1)
        )
        
        await scheduler.start()
        await asyncio.sleep(0.5)
        
        job = scheduler.jobs[job_id]
        original_node = job.allocated_node
        
        if original_node == "local":
            # Force migration by removing local node
            scheduler._migrate_job(job_id, "local")
            
            # Job should be migrated to cloud node
            assert job.allocated_node != original_node
            assert job.status == JobStatus.RUNNING
        
        await scheduler.stop()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])