# Resource Optimization Scheduler

**GRANGER Task #32** - Level 3 Complex Task

## Overview

The Resource Optimization Scheduler orchestrates resource allocation across multiple modules to optimize performance and minimize costs. It monitors system resources (CPU, memory, GPU, network, disk I/O) and implements multiple scheduling algorithms to efficiently distribute workloads.

## Features

### Resource Monitoring
- Real-time CPU, memory, network, and disk I/O monitoring
- Historical trend analysis
- Resource usage prediction

### Scheduling Algorithms
1. **Priority-Based**: Jobs scheduled by priority (1-10 scale)
2. **Fair-Share**: Equal distribution across modules
3. **Deadline-Aware**: Prioritizes jobs with approaching deadlines
4. **Round-Robin**: Simple rotation through job queue
5. **Shortest Job First (SJF)**: Optimizes for throughput
6. **Cost-Optimized**: Prefers cheaper compute nodes

### Dynamic Resource Management
- Automatic job allocation to available nodes
- Preemptive scheduling with job migration
- Multi-node support (local + cloud)
- Resource constraints enforcement

### Job Lifecycle Management
- Submit, pause, resume, and cancel jobs
- Progress tracking
- Deadline monitoring with automatic priority boosting
- Job migration between nodes

## Quick Start

```python
from project_interactions.resource_scheduler import (
    ResourceScheduler, 
    SchedulingAlgorithm,
    ResourceRequirements
)

# Create scheduler with deadline-aware algorithm
scheduler = ResourceScheduler(SchedulingAlgorithm.DEADLINE_AWARE)

# Submit a high-priority job with deadline
job_id = scheduler.submit_job(
    module="arxiv_search",
    priority=8,
    deadline=120,  # 2 minutes
    requirements=ResourceRequirements(
        cpu_cores=2,
        memory_mb=4096,
        gpu_count=1
    ),
    estimated_duration=60.0
)

# Start scheduler
await scheduler.start()

# Monitor progress
stats = scheduler.get_scheduler_stats()
print(f"Running jobs: {stats['running_jobs']}")
print(f"CPU utilization: {stats['resource_utilization']['cpu']:.1%}")

# Stop scheduler
await scheduler.stop()
```

## Architecture

### Core Components

1. **ResourceScheduler**: Main orchestrator
2. **ResourceMonitor**: System resource tracking
3. **ResourceNode**: Compute node abstraction
4. **Job**: Schedulable work unit
5. **Scheduling Algorithms**: Pluggable scheduling strategies

### Job States
- `QUEUED`: Waiting for resources
- `RUNNING`: Actively executing
- `PAUSED`: Temporarily suspended
- `COMPLETED`: Successfully finished
- `FAILED`: Terminated with error
- `MIGRATING`: Moving between nodes

## Usage Examples

### Cost-Optimized Batch Processing
```python
scheduler = ResourceScheduler(SchedulingAlgorithm.COST_OPTIMIZED)

# Submit batch jobs
for i in range(10):
    scheduler.submit_job(
        module="batch_processor",
        requirements=ResourceRequirements(cpu_cores=1, memory_mb=1024),
        cost_per_second=0.01
    )
```

### Fair-Share Multi-Module Scheduling
```python
scheduler = ResourceScheduler(SchedulingAlgorithm.FAIR_SHARE)

# Jobs from different modules get fair access
scheduler.submit_job("module_a", priority=5)
scheduler.submit_job("module_b", priority=5)
scheduler.submit_job("module_a", priority=5)  # Won't monopolize
```

### Deadline-Critical Processing
```python
scheduler = ResourceScheduler(SchedulingAlgorithm.DEADLINE_AWARE)

# Urgent job gets priority
urgent = scheduler.submit_job("critical_task", deadline=30)  # 30 seconds
normal = scheduler.submit_job("regular_task", deadline=3600)  # 1 hour
```

## Performance Characteristics

- Handles 100+ concurrent jobs efficiently
- Sub-second scheduling decisions
- Minimal overhead (~1% CPU for monitoring)
- Scalable to multiple nodes

## Integration Points

- **SPARTA**: Schedule security scans
- **Marker**: Allocate resources for PDF processing
- **ArangoDB**: Manage indexing workloads
- **Claude Max Proxy**: Optimize LLM request routing
- **Unsloth**: Coordinate training jobs

## Testing

Run the comprehensive test suite:

```bash
python resource_scheduler_interaction.py
```

Tests include:
- Priority-based scheduling validation
- Fair-share distribution testing
- Deadline awareness verification
- Resource monitoring accuracy
- Job migration functionality
- Cost optimization effectiveness
- Performance benchmarking (100 jobs)

## Future Enhancements

1. GPU scheduling with CUDA awareness
2. Network bandwidth allocation
3. Distributed scheduler coordination
4. Machine learning-based prediction
5. Auto-scaling cloud resources
6. SLA enforcement
7. Power efficiency optimization