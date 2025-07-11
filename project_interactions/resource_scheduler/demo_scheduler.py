#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Demonstration of Resource Optimization Scheduler capabilities
"""

import asyncio
import time
from resource_scheduler_interaction import (
    ResourceScheduler,
    SchedulingAlgorithm,
    ResourceRequirements
)


async def demo_multi_algorithm_comparison():
    """Compare different scheduling algorithms"""
    print("Resource Scheduler Algorithm Comparison")
    print("=" * 60)
    
    algorithms = [
        SchedulingAlgorithm.PRIORITY_BASED,
        SchedulingAlgorithm.FAIR_SHARE,
        SchedulingAlgorithm.DEADLINE_AWARE,
        SchedulingAlgorithm.COST_OPTIMIZED
    ]
    
    for algo in algorithms:
        print(f"\n{algo.value.upper()} Algorithm:")
        print("-" * 40)
        
        scheduler = ResourceScheduler(algo)
        
        # Submit mixed workload
        jobs = []
        
        # High priority research job
        jobs.append(scheduler.submit_job(
            "arxiv_research",
            priority=9,
            deadline=60,
            requirements=ResourceRequirements(cpu_cores=2, memory_mb=4096),
            estimated_duration=20
        ))
        
        # Medium priority processing jobs
        for i in range(2):
            jobs.append(scheduler.submit_job(
                f"marker_processing_{i}",
                priority=5,
                requirements=ResourceRequirements(cpu_cores=1, memory_mb=2048),
                estimated_duration=15
            ))
        
        # Low priority background tasks
        for i in range(2):
            jobs.append(scheduler.submit_job(
                f"arangodb_indexing_{i}",
                priority=2,
                requirements=ResourceRequirements(cpu_cores=0.5, memory_mb=1024),
                estimated_duration=30
            ))
        
        await scheduler.start()
        
        # Monitor for a few seconds
        for i in range(3):
            await asyncio.sleep(1)
            stats = scheduler.get_scheduler_stats()
            print(f"  T+{i+1}s: Running={stats['running_jobs']}, "
                  f"Queued={stats['queued_jobs']}, "
                  f"CPU={stats['resource_utilization']['cpu']:.1%}")
        
        await scheduler.stop()


async def demo_dynamic_resource_management():
    """Demonstrate dynamic resource allocation and job migration"""
    print("\n\nDynamic Resource Management Demo")
    print("=" * 60)
    
    scheduler = ResourceScheduler(SchedulingAlgorithm.PRIORITY_BASED)
    
    # Start with just local node
    print("Starting with local node only...")
    
    # Submit resource-intensive job
    big_job = scheduler.submit_job(
        "model_training",
        priority=8,
        requirements=ResourceRequirements(cpu_cores=8, memory_mb=16384, gpu_count=1),
        estimated_duration=60
    )
    
    await scheduler.start()
    await asyncio.sleep(1)
    
    stats = scheduler.get_scheduler_stats()
    print(f"Initial: Running={stats['running_jobs']}, Queued={stats['queued_jobs']}")
    
    # Job should be queued due to insufficient resources
    if scheduler.jobs[big_job].status.value == "queued":
        print("✓ Job correctly queued due to insufficient local resources")
    
    # Add cloud node dynamically
    print("\nAdding cloud node with more resources...")
    from resource_scheduler_interaction import ResourceNode, ResourceType
    
    cloud_node = ResourceNode(
        id="cloud-dynamic",
        total_resources={
            ResourceType.CPU: 16,
            ResourceType.MEMORY: 32768,
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
        cost_multiplier=3.0,
        location="cloud"
    )
    scheduler.add_node(cloud_node)
    
    # Wait for scheduler to allocate
    await asyncio.sleep(2)
    
    if scheduler.jobs[big_job].status.value == "running":
        print(f"✓ Job now running on node: {scheduler.jobs[big_job].allocated_node}")
    
    await scheduler.stop()


async def demo_real_world_pipeline():
    """Simulate a real-world GRANGER pipeline workload"""
    print("\n\nReal-World Pipeline Simulation")
    print("=" * 60)
    print("Simulating: ArXiv → Marker → ArangoDB → Unsloth pipeline")
    
    scheduler = ResourceScheduler(SchedulingAlgorithm.DEADLINE_AWARE)
    await scheduler.start()
    
    # Stage 1: ArXiv paper discovery
    print("\nStage 1: ArXiv Discovery")
    arxiv_jobs = []
    for i in range(3):
        job_id = scheduler.submit_job(
            f"arxiv_search_{i}",
            priority=7,
            deadline=30,  # Need results quickly
            requirements=ResourceRequirements(cpu_cores=1, memory_mb=1024),
            estimated_duration=5
        )
        arxiv_jobs.append(job_id)
    
    # Wait for completion
    await asyncio.sleep(6)
    
    # Stage 2: Marker PDF processing
    print("\nStage 2: Marker Processing")
    marker_jobs = []
    for i, arxiv_job in enumerate(arxiv_jobs):
        if scheduler.jobs[arxiv_job].status.value == "completed":
            job_id = scheduler.submit_job(
                f"marker_process_{i}",
                priority=8,
                requirements=ResourceRequirements(cpu_cores=2, memory_mb=4096),
                estimated_duration=10
            )
            marker_jobs.append(job_id)
    
    await asyncio.sleep(11)
    
    # Stage 3: ArangoDB storage
    print("\nStage 3: ArangoDB Storage")
    arangodb_jobs = []
    for i, marker_job in enumerate(marker_jobs):
        if marker_job and scheduler.jobs[marker_job].status.value == "completed":
            job_id = scheduler.submit_job(
                f"arangodb_store_{i}",
                priority=6,
                requirements=ResourceRequirements(cpu_cores=1, memory_mb=2048),
                estimated_duration=3
            )
            arangodb_jobs.append(job_id)
    
    await asyncio.sleep(4)
    
    # Stage 4: Unsloth training preparation
    print("\nStage 4: Unsloth Training Prep")
    if any(scheduler.jobs[j].status.value == "completed" for j in arangodb_jobs if j):
        training_job = scheduler.submit_job(
            "unsloth_training_prep",
            priority=9,
            requirements=ResourceRequirements(cpu_cores=4, memory_mb=8192, gpu_count=1),
            estimated_duration=15
        )
    
    # Final stats
    await asyncio.sleep(5)
    stats = scheduler.get_scheduler_stats()
    print(f"\nPipeline Complete:")
    print(f"  Total jobs: {stats['total_jobs']}")
    print(f"  Completed: {stats['completed_jobs']}")
    print(f"  Average CPU utilization: {stats['resource_utilization']['cpu']:.1%}")
    
    await scheduler.stop()


async def main():
    """Run all demonstrations"""
    await demo_multi_algorithm_comparison()
    await demo_dynamic_resource_management()
    await demo_real_world_pipeline()
    
    print("\n" + "=" * 60)
    print("Resource Scheduler Demo Complete!")


if __name__ == "__main__":
    asyncio.run(main())