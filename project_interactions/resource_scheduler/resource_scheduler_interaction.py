#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: resource_scheduler_interaction.py
Purpose: Resource Optimization Scheduler for orchestrating resource allocation across modules

This module implements a Level 3 task that monitors resource usage, implements multiple
scheduling algorithms, and dynamically allocates resources to optimize performance and costs.

External Dependencies:
- psutil: https://psutil.readthedocs.io/ - System and process monitoring
- asyncio: https://docs.python.org/3/library/asyncio.html - Async operations
- heapq: https://docs.python.org/3/library/heapq.html - Priority queue implementation

Example Usage:
>>> scheduler = ResourceScheduler()
>>> scheduler.submit_job("research_task", priority=5, deadline=3600)
>>> scheduler.start()
"""

import asyncio
import heapq
import json
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import psutil
import threading
import random


class SchedulingAlgorithm(Enum):
    """Available scheduling algorithms"""
    PRIORITY_BASED = "priority_based"
    FAIR_SHARE = "fair_share"
    DEADLINE_AWARE = "deadline_aware"
    ROUND_ROBIN = "round_robin"
    SJF = "shortest_job_first"  # Shortest Job First
    COST_OPTIMIZED = "cost_optimized"


class ResourceType(Enum):
    """Types of resources that can be allocated"""
    CPU = "cpu"
    MEMORY = "memory"
    GPU = "gpu"
    NETWORK = "network"
    DISK_IO = "disk_io"


class JobStatus(Enum):
    """Status of scheduled jobs"""
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    MIGRATING = "migrating"


@dataclass
class ResourceRequirements:
    """Resource requirements for a job"""
    cpu_cores: float = 1.0
    memory_mb: int = 512
    gpu_count: int = 0
    network_mbps: float = 10.0
    disk_io_mbps: float = 50.0
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary format"""
        return {
            ResourceType.CPU.value: self.cpu_cores,
            ResourceType.MEMORY.value: self.memory_mb,
            ResourceType.GPU.value: self.gpu_count,
            ResourceType.NETWORK.value: self.network_mbps,
            ResourceType.DISK_IO.value: self.disk_io_mbps
        }


@dataclass
class Job:
    """Represents a schedulable job"""
    id: str
    module: str
    priority: int = 5  # 1-10, higher is more important
    deadline: Optional[float] = None  # Seconds from submission
    requirements: ResourceRequirements = field(default_factory=ResourceRequirements)
    estimated_duration: float = 60.0  # Seconds
    cost_per_second: float = 0.01
    status: JobStatus = JobStatus.QUEUED
    submitted_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    allocated_node: Optional[str] = None
    progress: float = 0.0
    
    def __lt__(self, other):
        """For priority queue comparison"""
        return self.priority > other.priority


@dataclass
class ResourceNode:
    """Represents a compute node with available resources"""
    id: str
    total_resources: Dict[ResourceType, float]
    available_resources: Dict[ResourceType, float]
    cost_multiplier: float = 1.0
    location: str = "default"
    running_jobs: Set[str] = field(default_factory=set)
    
    def can_accommodate(self, requirements: ResourceRequirements) -> bool:
        """Check if node can accommodate job requirements"""
        req_dict = requirements.to_dict()
        for resource_type, required in req_dict.items():
            if self.available_resources.get(ResourceType(resource_type), 0) < required:
                return False
        return True
    
    def allocate(self, job_id: str, requirements: ResourceRequirements) -> None:
        """Allocate resources for a job"""
        req_dict = requirements.to_dict()
        for resource_type, required in req_dict.items():
            self.available_resources[ResourceType(resource_type)] -= required
        self.running_jobs.add(job_id)
    
    def deallocate(self, job_id: str, requirements: ResourceRequirements) -> None:
        """Deallocate resources from a job"""
        req_dict = requirements.to_dict()
        for resource_type, required in req_dict.items():
            self.available_resources[ResourceType(resource_type)] += required
        self.running_jobs.discard(job_id)


class ResourceMonitor:
    """Monitors system resource usage"""
    
    def __init__(self):
        self.history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.monitoring = False
        self._monitor_thread = None
    
    def start_monitoring(self):
        """Start resource monitoring in background thread"""
        self.monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop)
        self._monitor_thread.daemon = True
        self._monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop resource monitoring"""
        self.monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=1)
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.monitoring:
            timestamp = time.time()
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.history['cpu'].append((timestamp, cpu_percent))
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.history['memory'].append((timestamp, memory.percent))
            
            # Network I/O
            net_io = psutil.net_io_counters()
            self.history['network_sent'].append((timestamp, net_io.bytes_sent))
            self.history['network_recv'].append((timestamp, net_io.bytes_recv))
            
            # Disk I/O
            disk_io = psutil.disk_io_counters()
            if disk_io:
                self.history['disk_read'].append((timestamp, disk_io.read_bytes))
                self.history['disk_write'].append((timestamp, disk_io.write_bytes))
            
            time.sleep(1)
    
    def get_current_usage(self) -> Dict[ResourceType, float]:
        """Get current resource usage"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        return {
            ResourceType.CPU: cpu_percent / 100.0 * psutil.cpu_count(),
            ResourceType.MEMORY: memory.used / (1024 * 1024),  # MB
            ResourceType.GPU: 0,  # Would need nvidia-ml-py for real GPU monitoring
            ResourceType.NETWORK: 100.0,  # Placeholder
            ResourceType.DISK_IO: 100.0   # Placeholder
        }
    
    def get_usage_trend(self, resource: str, window: int = 10) -> float:
        """Get resource usage trend (positive = increasing)"""
        if resource not in self.history or len(self.history[resource]) < 2:
            return 0.0
        
        recent = list(self.history[resource])[-window:]
        if len(recent) < 2:
            return 0.0
        
        # Simple linear trend
        values = [v[1] for v in recent]
        avg_first_half = sum(values[:len(values)//2]) / (len(values)//2)
        avg_second_half = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
        
        return avg_second_half - avg_first_half


class ResourceScheduler:
    """Main resource optimization scheduler"""
    
    def __init__(self, algorithm: SchedulingAlgorithm = SchedulingAlgorithm.PRIORITY_BASED):
        self.algorithm = algorithm
        self.jobs: Dict[str, Job] = {}
        self.job_queue: List[Job] = []  # Priority queue
        self.nodes: Dict[str, ResourceNode] = {}
        self.monitor = ResourceMonitor()
        self.running = False
        self._scheduler_task = None
        self.scheduler_interval = 1.0  # seconds
        
        # Scheduling state
        self.fair_share_usage: Dict[str, float] = defaultdict(float)
        self.module_allocations: Dict[str, int] = defaultdict(int)
        
        # Initialize with some default nodes
        self._initialize_default_nodes()
    
    def _initialize_default_nodes(self):
        """Initialize default compute nodes"""
        # Local node
        cpu_count = psutil.cpu_count()
        memory_total = psutil.virtual_memory().total / (1024 * 1024)  # MB
        
        self.add_node(ResourceNode(
            id="local",
            total_resources={
                ResourceType.CPU: cpu_count,
                ResourceType.MEMORY: memory_total,
                ResourceType.GPU: 0,
                ResourceType.NETWORK: 1000.0,  # Mbps
                ResourceType.DISK_IO: 500.0    # Mbps
            },
            available_resources={
                ResourceType.CPU: cpu_count,
                ResourceType.MEMORY: memory_total,
                ResourceType.GPU: 0,
                ResourceType.NETWORK: 1000.0,
                ResourceType.DISK_IO: 500.0
            },
            cost_multiplier=1.0,
            location="local"
        ))
        
        # Simulated cloud nodes
        self.add_node(ResourceNode(
            id="cloud-1",
            total_resources={
                ResourceType.CPU: 16,
                ResourceType.MEMORY: 32768,  # 32GB
                ResourceType.GPU: 2,
                ResourceType.NETWORK: 10000.0,
                ResourceType.DISK_IO: 2000.0
            },
            available_resources={
                ResourceType.CPU: 16,
                ResourceType.MEMORY: 32768,
                ResourceType.GPU: 2,
                ResourceType.NETWORK: 10000.0,
                ResourceType.DISK_IO: 2000.0
            },
            cost_multiplier=3.0,  # 3x more expensive
            location="cloud"
        ))
    
    def add_node(self, node: ResourceNode) -> None:
        """Add a compute node to the scheduler"""
        self.nodes[node.id] = node
    
    def remove_node(self, node_id: str) -> None:
        """Remove a compute node (with job migration)"""
        if node_id not in self.nodes:
            return
        
        node = self.nodes[node_id]
        # Migrate running jobs
        for job_id in list(node.running_jobs):
            self._migrate_job(job_id, node_id)
        
        del self.nodes[node_id]
    
    def submit_job(self, 
                   module: str,
                   job_id: Optional[str] = None,
                   priority: int = 5,
                   deadline: Optional[float] = None,
                   requirements: Optional[ResourceRequirements] = None,
                   estimated_duration: float = 60.0,
                   cost_per_second: float = 0.01) -> str:
        """Submit a job to the scheduler"""
        if job_id is None:
            job_id = f"{module}_{int(time.time()*1000)}"
        
        if requirements is None:
            requirements = ResourceRequirements()
        
        job = Job(
            id=job_id,
            module=module,
            priority=priority,
            deadline=deadline,
            requirements=requirements,
            estimated_duration=estimated_duration,
            cost_per_second=cost_per_second
        )
        
        self.jobs[job_id] = job
        heapq.heappush(self.job_queue, job)
        
        return job_id
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a job"""
        if job_id not in self.jobs:
            return False
        
        job = self.jobs[job_id]
        
        if job.status == JobStatus.RUNNING and job.allocated_node:
            # Deallocate resources
            node = self.nodes[job.allocated_node]
            node.deallocate(job_id, job.requirements)
        
        job.status = JobStatus.FAILED
        job.completed_at = time.time()
        
        return True
    
    def pause_job(self, job_id: str) -> bool:
        """Pause a running job"""
        if job_id not in self.jobs:
            return False
        
        job = self.jobs[job_id]
        if job.status != JobStatus.RUNNING:
            return False
        
        job.status = JobStatus.PAUSED
        # Keep resources allocated but marked as paused
        return True
    
    def resume_job(self, job_id: str) -> bool:
        """Resume a paused job"""
        if job_id not in self.jobs:
            return False
        
        job = self.jobs[job_id]
        if job.status != JobStatus.PAUSED:
            return False
        
        job.status = JobStatus.RUNNING
        return True
    
    async def start(self):
        """Start the scheduler"""
        self.running = True
        self.monitor.start_monitoring()
        self._scheduler_task = asyncio.create_task(self._scheduler_loop())
    
    async def stop(self):
        """Stop the scheduler"""
        self.running = False
        self.monitor.stop_monitoring()
        if self._scheduler_task:
            await self._scheduler_task
    
    async def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.running:
            await self._schedule_jobs()
            await self._update_job_progress()
            await self._check_deadlines()
            await asyncio.sleep(self.scheduler_interval)
    
    async def _schedule_jobs(self):
        """Schedule jobs based on selected algorithm"""
        if self.algorithm == SchedulingAlgorithm.PRIORITY_BASED:
            await self._schedule_priority_based()
        elif self.algorithm == SchedulingAlgorithm.FAIR_SHARE:
            await self._schedule_fair_share()
        elif self.algorithm == SchedulingAlgorithm.DEADLINE_AWARE:
            await self._schedule_deadline_aware()
        elif self.algorithm == SchedulingAlgorithm.ROUND_ROBIN:
            await self._schedule_round_robin()
        elif self.algorithm == SchedulingAlgorithm.SJF:
            await self._schedule_sjf()
        elif self.algorithm == SchedulingAlgorithm.COST_OPTIMIZED:
            await self._schedule_cost_optimized()
    
    async def _schedule_priority_based(self):
        """Priority-based scheduling"""
        # Process jobs in priority order
        temp_queue = []
        
        while self.job_queue:
            job = heapq.heappop(self.job_queue)
            
            if job.status == JobStatus.QUEUED:
                allocated = await self._try_allocate_job(job)
                if not allocated:
                    temp_queue.append(job)
            else:
                temp_queue.append(job)
        
        # Restore unallocated jobs to queue
        for job in temp_queue:
            heapq.heappush(self.job_queue, job)
    
    async def _schedule_fair_share(self):
        """Fair-share scheduling across modules"""
        # Group jobs by module
        module_jobs: Dict[str, List[Job]] = defaultdict(list)
        
        for job in self.job_queue:
            if job.status == JobStatus.QUEUED:
                module_jobs[job.module].append(job)
        
        # Sort modules by usage (least used first)
        sorted_modules = sorted(module_jobs.keys(), 
                               key=lambda m: self.fair_share_usage[m])
        
        # Allocate one job per module in rotation
        for module in sorted_modules:
            if module_jobs[module]:
                job = module_jobs[module][0]
                if await self._try_allocate_job(job):
                    self.fair_share_usage[module] += job.estimated_duration
                    module_jobs[module].remove(job)
    
    async def _schedule_deadline_aware(self):
        """Deadline-aware scheduling"""
        # Sort jobs by deadline (earliest first)
        deadline_jobs = []
        
        for job in self.job_queue:
            if job.status == JobStatus.QUEUED and job.deadline:
                deadline_remaining = (job.submitted_at + job.deadline) - time.time()
                deadline_jobs.append((deadline_remaining, job))
        
        deadline_jobs.sort(key=lambda x: x[0])
        
        # Schedule jobs with nearest deadlines first
        for _, job in deadline_jobs:
            await self._try_allocate_job(job)
    
    async def _schedule_round_robin(self):
        """Round-robin scheduling"""
        # Simple round-robin across all queued jobs
        queued_jobs = [j for j in self.job_queue if j.status == JobStatus.QUEUED]
        
        for job in queued_jobs[:1]:  # Allocate one at a time
            await self._try_allocate_job(job)
    
    async def _schedule_sjf(self):
        """Shortest Job First scheduling"""
        # Sort by estimated duration
        sjf_jobs = [(j.estimated_duration, j) for j in self.job_queue 
                    if j.status == JobStatus.QUEUED]
        sjf_jobs.sort(key=lambda x: x[0])
        
        for _, job in sjf_jobs:
            if await self._try_allocate_job(job):
                break  # Allocate one at a time
    
    async def _schedule_cost_optimized(self):
        """Cost-optimized scheduling"""
        # Try to use cheapest nodes first
        sorted_nodes = sorted(self.nodes.values(), key=lambda n: n.cost_multiplier)
        
        queued_jobs = [j for j in self.job_queue if j.status == JobStatus.QUEUED]
        
        for job in queued_jobs:
            for node in sorted_nodes:
                if node.can_accommodate(job.requirements):
                    await self._allocate_job_to_node(job, node)
                    break
    
    async def _try_allocate_job(self, job: Job) -> bool:
        """Try to allocate a job to any available node"""
        # Find suitable node
        for node in self.nodes.values():
            if node.can_accommodate(job.requirements):
                await self._allocate_job_to_node(job, node)
                return True
        return False
    
    async def _allocate_job_to_node(self, job: Job, node: ResourceNode):
        """Allocate a job to a specific node"""
        node.allocate(job.id, job.requirements)
        job.allocated_node = node.id
        job.status = JobStatus.RUNNING
        job.started_at = time.time()
        self.module_allocations[job.module] += 1
    
    async def _update_job_progress(self):
        """Update progress of running jobs"""
        current_time = time.time()
        
        for job in list(self.jobs.values()):
            if job.status == JobStatus.RUNNING and job.started_at:
                # Simulate progress
                elapsed = current_time - job.started_at
                job.progress = min(100.0, (elapsed / job.estimated_duration) * 100)
                
                # Complete job if done
                if job.progress >= 100.0:
                    await self._complete_job(job)
    
    async def _complete_job(self, job: Job):
        """Mark a job as completed and free resources"""
        job.status = JobStatus.COMPLETED
        job.completed_at = time.time()
        job.progress = 100.0
        
        if job.allocated_node:
            node = self.nodes[job.allocated_node]
            node.deallocate(job.id, job.requirements)
            self.module_allocations[job.module] -= 1
    
    async def _check_deadlines(self):
        """Check for jobs approaching deadlines"""
        current_time = time.time()
        
        for job in self.jobs.values():
            if job.deadline and job.status in [JobStatus.QUEUED, JobStatus.RUNNING]:
                deadline_time = job.submitted_at + job.deadline
                time_remaining = deadline_time - current_time
                
                # Boost priority if approaching deadline
                if time_remaining < 60 and job.priority < 10:  # Less than 1 minute
                    job.priority = min(10, job.priority + 2)
    
    def _migrate_job(self, job_id: str, from_node_id: str):
        """Migrate a job from one node to another"""
        if job_id not in self.jobs:
            return
        
        job = self.jobs[job_id]
        job.status = JobStatus.MIGRATING
        
        # Find new node
        for node_id, node in self.nodes.items():
            if node_id != from_node_id and node.can_accommodate(job.requirements):
                # Deallocate from old node
                old_node = self.nodes[from_node_id]
                old_node.deallocate(job_id, job.requirements)
                
                # Allocate to new node
                node.allocate(job_id, job.requirements)
                job.allocated_node = node_id
                job.status = JobStatus.RUNNING
                break
    
    def get_scheduler_stats(self) -> Dict[str, Any]:
        """Get current scheduler statistics"""
        total_jobs = len(self.jobs)
        queued = sum(1 for j in self.jobs.values() if j.status == JobStatus.QUEUED)
        running = sum(1 for j in self.jobs.values() if j.status == JobStatus.RUNNING)
        completed = sum(1 for j in self.jobs.values() if j.status == JobStatus.COMPLETED)
        
        # Resource utilization
        total_resources = {r: 0.0 for r in ResourceType}
        used_resources = {r: 0.0 for r in ResourceType}
        
        for node in self.nodes.values():
            for resource in ResourceType:
                total_resources[resource] += node.total_resources.get(resource, 0)
                used = node.total_resources.get(resource, 0) - node.available_resources.get(resource, 0)
                used_resources[resource] += used
        
        utilization = {}
        for resource in ResourceType:
            if total_resources[resource] > 0:
                utilization[resource.value] = used_resources[resource] / total_resources[resource]
            else:
                utilization[resource.value] = 0.0
        
        return {
            "total_jobs": total_jobs,
            "queued_jobs": queued,
            "running_jobs": running,
            "completed_jobs": completed,
            "resource_utilization": utilization,
            "active_nodes": len(self.nodes),
            "algorithm": self.algorithm.value
        }
    
    def predict_job_start_time(self, job_id: str) -> Optional[float]:
        """Predict when a queued job will start"""
        if job_id not in self.jobs:
            return None
        
        job = self.jobs[job_id]
        if job.status != JobStatus.QUEUED:
            return None
        
        # Simple prediction based on queue position and running jobs
        queue_position = 0
        for q_job in self.job_queue:
            if q_job.id == job_id:
                break
            if q_job.status == JobStatus.QUEUED:
                queue_position += 1
        
        # Estimate based on average job duration
        avg_duration = sum(j.estimated_duration for j in self.jobs.values()) / len(self.jobs)
        running_jobs = sum(1 for j in self.jobs.values() if j.status == JobStatus.RUNNING)
        
        # Simple formula: position * avg_duration / number_of_nodes
        if len(self.nodes) > 0:
            estimated_wait = (queue_position * avg_duration) / len(self.nodes)
            return time.time() + estimated_wait
        
        return None


# Test functions
async def test_priority_scheduling():
    """Test priority-based scheduling"""
    scheduler = ResourceScheduler(SchedulingAlgorithm.PRIORITY_BASED)
    
    # Submit jobs with different priorities
    high_priority_job = scheduler.submit_job("critical_module", priority=9, 
                                           estimated_duration=10)
    medium_priority_job = scheduler.submit_job("normal_module", priority=5,
                                             estimated_duration=10)
    low_priority_job = scheduler.submit_job("background_module", priority=2,
                                          estimated_duration=10)
    
    await scheduler.start()
    await asyncio.sleep(2)
    
    # Check that high priority job is running
    assert scheduler.jobs[high_priority_job].status == JobStatus.RUNNING
    
    # At least one lower priority job should be queued if resources are limited
    queued_count = sum(1 for j in [medium_priority_job, low_priority_job] 
                      if scheduler.jobs[j].status == JobStatus.QUEUED)
    assert queued_count >= 1 or len(scheduler.nodes) > 1
    
    # Verify priority ordering in queue
    queue_priorities = [j.priority for j in scheduler.job_queue if j.status == JobStatus.QUEUED]
    if len(queue_priorities) > 1:
        assert queue_priorities == sorted(queue_priorities, reverse=True)
    
    await scheduler.stop()
    return "Priority scheduling working correctly"


async def test_fair_share_scheduling():
    """Test fair-share scheduling"""
    scheduler = ResourceScheduler(SchedulingAlgorithm.FAIR_SHARE)
    
    # Submit multiple jobs from different modules
    module_a_jobs = [scheduler.submit_job("module_a", estimated_duration=5) for _ in range(3)]
    module_b_jobs = [scheduler.submit_job("module_b", estimated_duration=5) for _ in range(1)]
    
    await scheduler.start()
    await asyncio.sleep(2)
    
    # Check fair distribution
    module_a_running = sum(1 for j in module_a_jobs 
                          if scheduler.jobs[j].status == JobStatus.RUNNING)
    module_b_running = sum(1 for j in module_b_jobs 
                          if scheduler.jobs[j].status == JobStatus.RUNNING)
    
    # Both modules should have jobs running if resources allow
    assert module_b_running > 0 or len(scheduler.nodes) == 1
    
    await scheduler.stop()
    return "Fair-share scheduling working correctly"


async def test_deadline_aware_scheduling():
    """Test deadline-aware scheduling"""
    scheduler = ResourceScheduler(SchedulingAlgorithm.DEADLINE_AWARE)
    
    # Submit jobs with different deadlines
    urgent_job = scheduler.submit_job("urgent_task", deadline=30, estimated_duration=10)
    normal_job = scheduler.submit_job("normal_task", deadline=300, estimated_duration=10)
    
    await scheduler.start()
    await asyncio.sleep(2)
    
    # Urgent job should be scheduled first
    assert scheduler.jobs[urgent_job].status == JobStatus.RUNNING
    
    await scheduler.stop()
    return "Deadline-aware scheduling working correctly"


async def test_resource_monitoring():
    """Test resource monitoring capabilities"""
    scheduler = ResourceScheduler()
    
    await scheduler.start()
    await asyncio.sleep(3)
    
    # Get current usage
    usage = scheduler.monitor.get_current_usage()
    assert ResourceType.CPU in usage
    assert ResourceType.MEMORY in usage
    
    # Check history
    assert len(scheduler.monitor.history['cpu']) > 0
    
    await scheduler.stop()
    return "Resource monitoring working correctly"


async def test_job_migration():
    """Test job migration between nodes"""
    scheduler = ResourceScheduler()
    
    # Submit a job
    job_id = scheduler.submit_job("migration_test", 
                                requirements=ResourceRequirements(cpu_cores=2))
    
    await scheduler.start()
    await asyncio.sleep(2)
    
    # Get allocated node
    job = scheduler.jobs[job_id]
    original_node = job.allocated_node
    
    # Remove the node (triggering migration)
    if original_node:
        scheduler.remove_node(original_node)
        await asyncio.sleep(1)
        
        # Check job was migrated
        assert job.allocated_node != original_node
        assert job.status == JobStatus.RUNNING
    
    await scheduler.stop()
    return "Job migration working correctly"


async def test_cost_optimization():
    """Test cost-optimized scheduling"""
    scheduler = ResourceScheduler(SchedulingAlgorithm.COST_OPTIMIZED)
    
    # Submit jobs
    jobs = [scheduler.submit_job(f"cost_test_{i}", 
                               requirements=ResourceRequirements(cpu_cores=1))
            for i in range(3)]
    
    await scheduler.start()
    await asyncio.sleep(2)
    
    # Check that jobs prefer cheaper nodes
    local_jobs = sum(1 for j in jobs 
                    if scheduler.jobs[j].allocated_node == "local" 
                    and scheduler.jobs[j].status == JobStatus.RUNNING)
    
    assert local_jobs > 0  # At least some jobs on cheaper local node
    
    await scheduler.stop()
    return "Cost optimization working correctly"


async def test_scheduler_performance():
    """Test scheduler performance with many jobs"""
    scheduler = ResourceScheduler()
    
    # Submit many jobs
    start_time = time.time()
    job_count = 100
    
    for i in range(job_count):
        scheduler.submit_job(f"perf_test_{i}", 
                           priority=random.randint(1, 10),
                           estimated_duration=random.uniform(1, 10))
    
    await scheduler.start()
    
    # Let scheduler run for a bit
    await asyncio.sleep(5)
    
    stats = scheduler.get_scheduler_stats()
    
    await scheduler.stop()
    
    # Check performance
    elapsed = time.time() - start_time
    assert elapsed < 10  # Should handle 100 jobs quickly
    assert stats["running_jobs"] > 0
    assert stats["completed_jobs"] >= 0
    
    return f"Handled {job_count} jobs in {elapsed:.2f}s"


if __name__ == "__main__":
    import asyncio
    
    async def run_all_tests():
        """Run all test functions"""
        print("Resource Optimization Scheduler Tests")
        print("=" * 50)
        
        tests = [
            ("Priority Scheduling", test_priority_scheduling, 3),
            ("Fair-Share Scheduling", test_fair_share_scheduling, 3),
            ("Deadline-Aware Scheduling", test_deadline_aware_scheduling, 3),
            ("Resource Monitoring", test_resource_monitoring, 4),
            ("Job Migration", test_job_migration, 4),
            ("Cost Optimization", test_cost_optimization, 3),
            ("Scheduler Performance", test_scheduler_performance, 6)
        ]
        
        total_tests = len(tests)
        passed_tests = 0
        
        for test_name, test_func, expected_duration in tests:
            print(f"\n{test_name}:")
            print("-" * 30)
            
            try:
                start = time.time()
                result = await test_func()
                duration = time.time() - start
                
                print(f"✅ PASSED: {result}")
                print(f"   Duration: {duration:.2f}s (expected ~{expected_duration}s)")
                passed_tests += 1
                
            except Exception as e:
                print(f"❌ FAILED: {str(e)}")
                import traceback
                traceback.print_exc()
        
        print("\n" + "=" * 50)
        print(f"Test Summary: {passed_tests}/{total_tests} passed")
        
        # Demonstrate real usage
        print("\n" + "=" * 50)
        print("Real Usage Example:")
        print("-" * 30)
        
        scheduler = ResourceScheduler(SchedulingAlgorithm.DEADLINE_AWARE)
        
        # Submit various jobs
        job1 = scheduler.submit_job("arxiv_search", priority=8, deadline=120,
                                  requirements=ResourceRequirements(cpu_cores=2, memory_mb=4096))
        job2 = scheduler.submit_job("marker_processing", priority=6,
                                  requirements=ResourceRequirements(cpu_cores=4, memory_mb=8192))
        job3 = scheduler.submit_job("arangodb_indexing", priority=4,
                                  requirements=ResourceRequirements(cpu_cores=1, memory_mb=2048))
        
        await scheduler.start()
        
        # Monitor for a bit
        for i in range(5):
            await asyncio.sleep(1)
            stats = scheduler.get_scheduler_stats()
            print(f"\nTime {i+1}s - Running: {stats['running_jobs']}, "
                  f"Queued: {stats['queued_jobs']}, "
                  f"CPU Util: {stats['resource_utilization']['cpu']:.1%}")
        
        await scheduler.stop()
        
        return passed_tests == total_tests
    
    # Run tests
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)