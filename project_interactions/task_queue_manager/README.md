# Task Queue Manager

A distributed task queue management system for orchestrating asynchronous work across multiple workers.

## Features

### Core Capabilities
- **Multiple Queue Backends**: Support for Redis, RabbitMQ, AWS SQS, and in-memory queues
- **Priority Queue Management**: Tasks are prioritized and processed in order of importance
- **Worker Pool Management**: Dynamic worker allocation and health monitoring
- **Task Retry Logic**: Automatic retry with configurable limits and backoff
- **Dead Letter Queue**: Failed tasks are tracked and can be reprocessed
- **Task Routing**: Route tasks to specific queues based on tags or priorities
- **Load Balancing**: Distribute work evenly across available workers

### Advanced Features
- **Task Scheduling**: Schedule tasks with delays
- **Task Chaining**: Create parent-child task relationships
- **Rate Limiting**: Prevent overwhelming the system
- **Task Deduplication**: Avoid processing duplicate tasks
- **Progress Tracking**: Monitor task and workflow progress
- **Worker Auto-scaling**: Scale workers based on queue depth
- **Result Storage**: Store and retrieve task results

## Installation

```bash
# Install with Redis support
pip install redis

# Install with RabbitMQ support
pip install pika

# Install with AWS SQS support
pip install boto3
```

## Quick Start

```python
from task_queue_manager_interaction import TaskQueueManagerInteraction

# Initialize with memory backend (for testing)
manager = TaskQueueManagerInteraction(backend="memory")

# Submit a simple task
task_id = await manager.submit_task(
    "process_data",
    {"file": "data.csv", "rows": 1000},
    priority=5
)

# Get task result
result = await manager.get_result(task_id, timeout=30)
print(result)  # {'status': 'completed', 'result': {...}}
```

## Configuration

### Backend Options

#### Redis
```python
manager = TaskQueueManagerInteraction(
    backend="redis",
    redis_url="redis://localhost:6379/0"
)
```

#### RabbitMQ
```python
manager = TaskQueueManagerInteraction(
    backend="rabbitmq",
    rabbitmq_url="amqp://user:pass@localhost:5672/"
)
```

#### AWS SQS
```python
manager = TaskQueueManagerInteraction(
    backend="sqs",
    sqs_config={
        "region_name": "us-east-1",
        "aws_access_key_id": "YOUR_KEY",
        "aws_secret_access_key": "YOUR_SECRET"
    }
)
```

## Task Submission

### Basic Task
```python
task_id = await manager.submit_task(
    name="send_email",
    payload={"to": "user@example.com", "subject": "Hello"},
    priority=5  # 0-10, higher is more urgent
)
```

### Delayed Task
```python
# Schedule task to run in 60 seconds
task_id = await manager.submit_task(
    name="scheduled_backup",
    payload={"database": "production"},
    delay=60
)
```

### Task with Tags
```python
# Route to specific queue using tags
task_id = await manager.submit_task(
    name="urgent_customer_request",
    payload={"customer_id": "12345"},
    tags=["urgent", "customer-facing"]
)
```

### Task Chaining
```python
# Create parent task
parent_id = await manager.submit_task(
    name="data_import",
    payload={"source": "api"}
)

# Create child tasks
for i in range(3):
    child_id = await manager.submit_task(
        name=f"process_chunk_{i}",
        payload={"chunk": i},
        parent_task_id=parent_id
    )
```

### Task Deduplication
```python
# Prevent duplicate tasks
task_id = await manager.submit_task(
    name="daily_report",
    payload={"date": "2024-01-15"},
    dedupe_key="daily-report-2024-01-15"
)
```

## Worker Management

### Register Task Handler
```python
def process_data_handler(payload):
    # Process the data
    rows = payload.get("rows", 0)
    return {"processed": rows, "status": "success"}

manager.register_handler("process_data", process_data_handler)
```

### Monitor Workers
```python
# Get worker statistics
stats = manager.get_worker_stats()
for worker in stats:
    print(f"Worker {worker['worker_id']}: {worker['status']}")
    print(f"  Completed: {worker['tasks_completed']}")
    print(f"  Failed: {worker['tasks_failed']}")
```

## Task Monitoring

### Get Task Progress
```python
progress = manager.get_task_progress(task_id)
print(f"Status: {progress['status']}")
print(f"Progress: {progress['progress']}%")
```

### Get Queue Statistics
```python
queue_stats = manager.get_queue_stats()
for queue_name, stats in queue_stats.items():
    print(f"{queue_name}: {stats['pending']} pending tasks")
```

### Cancel Task
```python
cancelled = await manager.cancel_task(task_id)
if cancelled:
    print("Task cancelled successfully")
```

## Queue Routing

Tasks are automatically routed based on:

1. **Tags**: 
   - `urgent` → Urgent queue
   - `batch` → Batch queue
   - Others → Default queue

2. **Priority**:
   - Priority > 5 → High priority queue
   - Priority 0-5 → Default queue

3. **Custom Rules**: Can be extended for specific routing logic

## Error Handling

### Retry Configuration
```python
task = Task(
    name="risky_operation",
    payload={"data": "important"},
    max_retries=5,  # Retry up to 5 times
    retry_delay=30  # Wait 30 seconds between retries
)
```

### Dead Letter Queue
Tasks that exceed retry limits are moved to the dead letter queue for manual inspection:

```python
# Tasks with status=DEAD need manual intervention
dead_tasks = [
    task for task in manager.tasks.values() 
    if task.status == TaskStatus.DEAD
]
```

## Best Practices

1. **Use Appropriate Priorities**: Reserve high priorities (8-10) for truly urgent tasks
2. **Tag Consistently**: Use standard tags across your application
3. **Set Reasonable Timeouts**: Configure task timeouts based on expected duration
4. **Monitor Queue Depth**: Watch for queue buildup and scale workers accordingly
5. **Handle Failures Gracefully**: Implement proper error handling in task handlers
6. **Use Deduplication**: Prevent duplicate work with dedupe keys
7. **Chain Related Tasks**: Use parent-child relationships for workflows

## Performance Considerations

- **Batch Operations**: Submit related tasks together
- **Queue Selection**: Use appropriate backend for your scale
- **Worker Count**: Balance between throughput and resource usage
- **Result Storage**: Clean up old results to prevent memory growth

## Examples

See the `tests/` directory for comprehensive examples of all features.

## License

MIT