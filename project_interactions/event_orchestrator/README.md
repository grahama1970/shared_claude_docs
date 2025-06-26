# Event-Driven Architecture Orchestrator

A comprehensive event-driven architecture orchestration system implementing Event Bus, Saga Pattern, CQRS, Event Sourcing, and workflow orchestration capabilities.

## Features

### 1. Event Bus Management
- Publish/Subscribe pattern with topic-based routing
- Event filtering and transformation
- Automatic retry with exponential backoff
- Dead letter queue for failed events
- Event metrics and monitoring

### 2. Event Schema Registry
- Schema versioning and evolution
- Automatic event migration between versions
- Schema validation and enforcement
- Backward compatibility support

### 3. Event Sourcing Support
- Event store abstraction with multiple backends
- Event stream management
- Event replay functionality
- Temporal queries and projections
- Snapshot support (planned)

### 4. Saga Pattern Orchestration
- Distributed transaction management
- Automatic compensation on failure
- Step-by-step execution with timeouts
- Context propagation between steps
- Parallel saga execution support

### 5. CQRS Implementation
- Command and Query separation
- Command handlers with validation
- Query handlers with caching
- Projection updates
- Read model management

### 6. Dead Letter Queue Handling
- Automatic routing of failed events
- Manual reprocessing capabilities
- Failure analysis and reporting
- Configurable retry policies

### 7. Event Store Backends
- In-memory store (implemented)
- Redis (planned)
- Kafka (planned)
- RabbitMQ (planned)

### 8. Distributed Tracing
- Span creation and management
- Tag and log support
- Trace visualization (planned)
- Performance metrics

### 9. Workflow Orchestration
- Multi-step workflow definitions
- Event-driven step execution
- Workflow state management
- Conditional branching (planned)

## Usage

### Basic Event Publishing

```python
from event_orchestrator_interaction import EventOrchestrator

# Create orchestrator
orchestrator = EventOrchestrator()

# Subscribe to events
async def user_handler(event):
    print(f"User created: {event.payload}")

orchestrator.subscribe("user.created", user_handler)

# Publish event
await orchestrator.publish_event("user.created", {
    "user_id": "123",
    "username": "john_doe"
})
```

### Saga Pattern Example

```python
# Define saga steps
async def validate_order(context):
    # Validation logic
    return {"valid": True}

async def process_payment(context):
    # Payment processing
    return {"transaction_id": "TXN123"}

async def ship_order(context):
    # Shipping logic
    return {"tracking_number": "TRACK123"}

# Define compensations
async def refund_payment(context):
    # Refund logic
    pass

# Create saga
orchestrator.define_saga("order_processing", [
    SagaStep("validate", validate_order),
    SagaStep("payment", process_payment, refund_payment),
    SagaStep("shipping", ship_order)
])

# Execute saga
saga = await orchestrator.start_saga("order_processing", {
    "order_id": "ORDER123",
    "amount": 99.99
})
```

### CQRS Pattern

```python
# Command handler
async def create_user_command(data):
    # Create user logic
    return {"user_id": "USER123", "created": True}

# Query handler
async def get_user_query(params):
    # Fetch user logic
    return {"user_id": params["user_id"], "name": "John"}

# Register handlers
orchestrator.register_command_handler("create_user", create_user_command)
orchestrator.register_query_handler("get_user", get_user_query)

# Execute
result = await orchestrator.send_command("create_user", {"name": "John"})
user = await orchestrator.execute_query("get_user", {"user_id": result["user_id"]})
```

### Event Replay

```python
# Replay all events of a specific type
replayed_count = await orchestrator.replay_events("user.created")

# Replay events from a specific timestamp
replayed_count = await orchestrator.replay_events(
    event_type="order.completed",
    from_timestamp=time.time() - 3600  # Last hour
)
```

## Testing

Run the test suite:

```bash
# Run all tests
python test_task_45.py

# Run individual test modules
python tests/test_event_bus.py
python tests/test_saga_orchestration.py
python tests/test_event_sourcing.py
```

## Architecture

The system follows a modular architecture with these key components:

1. **EventOrchestrator**: Main entry point coordinating all subsystems
2. **EventBus**: Core messaging infrastructure
3. **EventStore**: Persistence layer for events
4. **SagaOrchestrator**: Distributed transaction management
5. **CQRSHelper**: Command/Query separation implementation
6. **EventSchemaRegistry**: Schema versioning and migration
7. **DistributedTracing**: Observability and monitoring

## Future Enhancements

- Additional event store backends (Redis, Kafka, RabbitMQ)
- GraphQL API for event queries
- WebSocket support for real-time event streaming
- Event visualization dashboard
- Advanced workflow patterns (parallel, conditional)
- Event compression and archival
- Multi-tenancy support
- Security and encryption features

## License

MIT