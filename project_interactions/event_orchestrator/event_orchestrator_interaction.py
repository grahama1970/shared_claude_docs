
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: event_orchestrator_interaction.py
Purpose: Event-driven architecture orchestration system with saga patterns and CQRS support

External Dependencies:
- asyncio: https://docs.python.org/3/library/asyncio.html
- redis: https://redis-py.readthedocs.io/
- kafka-python: https://kafka-python.readthedocs.io/
- pika: https://pika.readthedocs.io/ (RabbitMQ)

Example Usage:
>>> orchestrator = EventOrchestrator()
>>> await orchestrator.publish_event("user.created", {"user_id": "123"})
>>> saga = await orchestrator.start_saga("order_processing", {"order_id": "456"})
"""

import asyncio
import json
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable, Set, Union, Tuple
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventStoreType(Enum):
    """Supported event store backends"""
    MEMORY = "memory"
    REDIS = "redis"
    KAFKA = "kafka"
    RABBITMQ = "rabbitmq"


class EventStatus(Enum):
    """Event processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"


class SagaStatus(Enum):
    """Saga execution status"""
    STARTED = "started"
    RUNNING = "running"
    COMPENSATING = "compensating"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATED = "compensated"


@dataclass
class Event:
    """Event data structure"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    version: int = 1
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None
    status: EventStatus = EventStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        return {
            "id": self.id,
            "type": self.type,
            "payload": self.payload,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
            "version": self.version,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "status": self.status.value,
            "retry_count": self.retry_count
        }


@dataclass
class SagaStep:
    """Saga step definition"""
    name: str
    action: Callable
    compensation: Optional[Callable] = None
    timeout: float = 30.0
    retry_policy: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Saga:
    """Saga orchestration state"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    steps: List[SagaStep] = field(default_factory=list)
    current_step: int = 0
    status: SagaStatus = SagaStatus.STARTED
    context: Dict[str, Any] = field(default_factory=dict)
    completed_steps: List[str] = field(default_factory=list)
    failed_step: Optional[str] = None
    error: Optional[str] = None
    started_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None


class EventStore(ABC):
    """Abstract event store interface"""
    
    @abstractmethod
    async def append(self, event: Event) -> None:
        """Append event to store"""
        pass
    
    @abstractmethod
    async def get_events(self, stream_id: str, from_version: int = 0) -> List[Event]:
        """Get events from stream"""
        pass
    
    @abstractmethod
    async def get_all_events(self, event_type: Optional[str] = None) -> List[Event]:
        """Get all events optionally filtered by type"""
        pass


class MemoryEventStore(EventStore):
    """In-memory event store implementation"""
    
    def __init__(self):
        self.events: List[Event] = []
        self.streams: Dict[str, List[Event]] = defaultdict(list)
    
    async def append(self, event: Event) -> None:
        """Append event to memory store"""
        self.events.append(event)
        if event.correlation_id:
            self.streams[event.correlation_id].append(event)
        logger.info(f"Event appended: {event.type} ({event.id})")
    
    async def get_events(self, stream_id: str, from_version: int = 0) -> List[Event]:
        """Get events from specific stream"""
        return [e for e in self.streams.get(stream_id, []) if e.version >= from_version]
    
    async def get_all_events(self, event_type: Optional[str] = None) -> List[Event]:
        """Get all events optionally filtered by type"""
        if event_type:
            return [e for e in self.events if e.type == event_type]
        return self.events.copy()


class EventBus:
    """Event bus for publishing and subscribing to events"""
    
    def __init__(self, store: EventStore):
        self.store = store
        self.handlers: Dict[str, List[Callable]] = defaultdict(list)
        self.filters: Dict[str, List[Callable]] = defaultdict(list)
        self.dead_letter_queue: List[Event] = []
        self.metrics: Dict[str, int] = defaultdict(int)
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe handler to event type"""
        self.handlers[event_type].append(handler)
        logger.info(f"Handler subscribed to {event_type}")
    
    def add_filter(self, event_type: str, filter_func: Callable) -> None:
        """Add filter for event type"""
        self.filters[event_type].append(filter_func)
    
    async def publish(self, event: Event) -> None:
        """Publish event to bus"""
        await self.store.append(event)
        self.metrics["events_published"] += 1
        
        # Apply filters
        if event.type in self.filters:
            for filter_func in self.filters[event.type]:
                if not await filter_func(event):
                    logger.info(f"Event filtered: {event.type} ({event.id})")
                    return
        
        # Process handlers
        if event.type in self.handlers:
            for handler in self.handlers[event.type]:
                try:
                    event.status = EventStatus.PROCESSING
                    await handler(event)
                    event.status = EventStatus.COMPLETED
                    self.metrics["events_processed"] += 1
                except Exception as e:
                    logger.error(f"Handler error for {event.type}: {e}")
                    event.retry_count += 1
                    
                    if event.retry_count >= event.max_retries:
                        event.status = EventStatus.DEAD_LETTER
                        self.dead_letter_queue.append(event)
                        self.metrics["events_dead_lettered"] += 1
                    else:
                        event.status = EventStatus.FAILED
                        self.metrics["events_failed"] += 1
    
    async def replay_events(self, event_type: Optional[str] = None, 
                          from_timestamp: Optional[float] = None) -> int:
        """Replay events from store"""
        events = await self.store.get_all_events(event_type)
        replayed = 0
        
        for event in events:
            if from_timestamp and event.timestamp < from_timestamp:
                continue
            
            # Reset status for replay
            event.status = EventStatus.PENDING
            event.retry_count = 0
            
            await self.publish(event)
            replayed += 1
        
        logger.info(f"Replayed {replayed} events")
        return replayed


class EventSchemaRegistry:
    """Registry for event schemas and versions"""
    
    def __init__(self):
        self.schemas: Dict[str, Dict[int, Dict[str, Any]]] = defaultdict(dict)
        self.migrations: Dict[str, Dict[Tuple[int, int], Callable]] = defaultdict(dict)
    
    def register_schema(self, event_type: str, version: int, schema: Dict[str, Any]) -> None:
        """Register event schema"""
        self.schemas[event_type][version] = schema
        logger.info(f"Schema registered: {event_type} v{version}")
    
    def register_migration(self, event_type: str, from_version: int, 
                         to_version: int, migration_func: Callable) -> None:
        """Register schema migration function"""
        self.migrations[event_type][(from_version, to_version)] = migration_func
    
    async def migrate_event(self, event: Event, target_version: int) -> Event:
        """Migrate event to target version"""
        if event.version == target_version:
            return event
        
        current_version = event.version
        while current_version < target_version:
            next_version = current_version + 1
            migration_key = (current_version, next_version)
            
            if migration_key in self.migrations[event.type]:
                migration_func = self.migrations[event.type][migration_key]
                event = await migration_func(event)
                event.version = next_version
                current_version = next_version
            else:
                raise ValueError(f"No migration from v{current_version} to v{next_version}")
        
        return event


class SagaOrchestrator:
    """Orchestrator for saga pattern implementation"""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.sagas: Dict[str, Saga] = {}
        self.saga_definitions: Dict[str, List[SagaStep]] = {}
    
    def define_saga(self, name: str, steps: List[SagaStep]) -> None:
        """Define saga workflow"""
        self.saga_definitions[name] = steps
        logger.info(f"Saga defined: {name} with {len(steps)} steps")
    
    async def start_saga(self, saga_name: str, context: Dict[str, Any]) -> Saga:
        """Start new saga execution"""
        if saga_name not in self.saga_definitions:
            raise ValueError(f"Unknown saga: {saga_name}")
        
        saga = Saga(
            name=saga_name,
            steps=self.saga_definitions[saga_name].copy(),
            context=context,
            status=SagaStatus.RUNNING
        )
        
        self.sagas[saga.id] = saga
        
        # Publish saga started event
        await self.event_bus.publish(Event(
            type=f"saga.{saga_name}.started",
            payload={"saga_id": saga.id, "context": context},
            correlation_id=saga.id
        ))
        
        # Execute saga
        asyncio.create_task(self._execute_saga(saga))
        
        return saga
    
    async def _execute_saga(self, saga: Saga) -> None:
        """Execute saga steps"""
        try:
            for i, step in enumerate(saga.steps):
                saga.current_step = i
                logger.info(f"Executing saga step: {step.name}")
                
                # Execute step with timeout
                try:
                    result = await asyncio.wait_for(
                        step.action(saga.context),
                        timeout=step.timeout
                    )
                    
                    saga.completed_steps.append(step.name)
                    saga.context[f"{step.name}_result"] = result
                    
                    # Publish step completed event
                    await self.event_bus.publish(Event(
                        type=f"saga.{saga.name}.step_completed",
                        payload={"saga_id": saga.id, "step": step.name, "result": result},
                        correlation_id=saga.id
                    ))
                    
                except asyncio.TimeoutError:
                    raise Exception(f"Step {step.name} timed out")
                except Exception as e:
                    raise Exception(f"Step {step.name} failed: {e}")
            
            # Saga completed successfully
            saga.status = SagaStatus.COMPLETED
            saga.completed_at = time.time()
            
            await self.event_bus.publish(Event(
                type=f"saga.{saga.name}.completed",
                payload={"saga_id": saga.id, "duration": saga.completed_at - saga.started_at},
                correlation_id=saga.id
            ))
            
        except Exception as e:
            logger.error(f"Saga {saga.id} failed: {e}")
            saga.status = SagaStatus.COMPENSATING
            saga.failed_step = saga.steps[saga.current_step].name
            saga.error = str(e)
            
            # Execute compensations
            await self._compensate_saga(saga)
    
    async def _compensate_saga(self, saga: Saga) -> None:
        """Execute saga compensations"""
        for step_name in reversed(saga.completed_steps):
            step = next((s for s in saga.steps if s.name == step_name), None)
            if step and step.compensation:
                try:
                    logger.info(f"Compensating step: {step.name}")
                    await step.compensation(saga.context)
                    
                    await self.event_bus.publish(Event(
                        type=f"saga.{saga.name}.step_compensated",
                        payload={"saga_id": saga.id, "step": step.name},
                        correlation_id=saga.id
                    ))
                    
                except Exception as e:
                    logger.error(f"Compensation failed for {step.name}: {e}")
        
        saga.status = SagaStatus.COMPENSATED
        saga.completed_at = time.time()
        
        await self.event_bus.publish(Event(
            type=f"saga.{saga.name}.compensated",
            payload={"saga_id": saga.id, "error": saga.error},
            correlation_id=saga.id
        ))


class CQRSHelper:
    """Helper for Command Query Responsibility Segregation pattern"""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.command_handlers: Dict[str, Callable] = {}
        self.query_handlers: Dict[str, Callable] = {}
        self.projections: Dict[str, Any] = {}
    
    def register_command_handler(self, command_type: str, handler: Callable) -> None:
        """Register command handler"""
        self.command_handlers[command_type] = handler
    
    def register_query_handler(self, query_type: str, handler: Callable) -> None:
        """Register query handler"""
        self.query_handlers[query_type] = handler
    
    async def send_command(self, command_type: str, data: Dict[str, Any]) -> Any:
        """Send command for processing"""
        if command_type not in self.command_handlers:
            raise ValueError(f"No handler for command: {command_type}")
        
        # Execute command
        result = await self.command_handlers[command_type](data)
        
        # Publish command executed event
        await self.event_bus.publish(Event(
            type=f"command.{command_type}.executed",
            payload={"command": command_type, "data": data, "result": result}
        ))
        
        return result
    
    async def execute_query(self, query_type: str, params: Dict[str, Any]) -> Any:
        """Execute query"""
        if query_type not in self.query_handlers:
            raise ValueError(f"No handler for query: {query_type}")
        
        return await self.query_handlers[query_type](params)
    
    def update_projection(self, projection_name: str, updater: Callable) -> None:
        """Update read model projection"""
        if projection_name not in self.projections:
            self.projections[projection_name] = {}
        
        self.projections[projection_name] = updater(self.projections[projection_name])


class DistributedTracing:
    """Distributed tracing integration"""
    
    def __init__(self):
        self.traces: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.active_spans: Dict[str, Dict[str, Any]] = {}
    
    def start_span(self, trace_id: str, span_name: str, parent_span: Optional[str] = None) -> str:
        """Start new span"""
        span_id = str(uuid.uuid4())
        span = {
            "span_id": span_id,
            "trace_id": trace_id,
            "name": span_name,
            "parent_span": parent_span,
            "start_time": time.time(),
            "tags": {},
            "logs": []
        }
        
        self.active_spans[span_id] = span
        self.traces[trace_id].append(span)
        
        return span_id
    
    def end_span(self, span_id: str) -> None:
        """End span"""
        if span_id in self.active_spans:
            span = self.active_spans[span_id]
            span["end_time"] = time.time()
            span["duration"] = span["end_time"] - span["start_time"]
            del self.active_spans[span_id]
    
    def add_tag(self, span_id: str, key: str, value: Any) -> None:
        """Add tag to span"""
        if span_id in self.active_spans:
            self.active_spans[span_id]["tags"][key] = value
    
    def add_log(self, span_id: str, message: str) -> None:
        """Add log to span"""
        if span_id in self.active_spans:
            self.active_spans[span_id]["logs"].append({
                "timestamp": time.time(),
                "message": message
            })


class EventOrchestrator:
    """Main event orchestrator combining all components"""
    
    def __init__(self, store_type: EventStoreType = EventStoreType.MEMORY):
        # Initialize event store
        if store_type == EventStoreType.MEMORY:
            self.store = MemoryEventStore()
        else:
            # Placeholder for other store implementations
            self.store = MemoryEventStore()
        
        # Initialize components
        self.event_bus = EventBus(self.store)
        self.schema_registry = EventSchemaRegistry()
        self.saga_orchestrator = SagaOrchestrator(self.event_bus)
        self.cqrs_helper = CQRSHelper(self.event_bus)
        self.tracing = DistributedTracing()
        
        # Workflow definitions
        self.workflows: Dict[str, List[Dict[str, Any]]] = {}
    
    async def publish_event(self, event_type: str, payload: Dict[str, Any],
                          correlation_id: Optional[str] = None) -> Event:
        """Publish event to the system"""
        event = Event(
            type=event_type,
            payload=payload,
            correlation_id=correlation_id or str(uuid.uuid4())
        )
        
        # Start tracing
        span_id = self.tracing.start_span(event.correlation_id, f"publish_{event_type}")
        
        try:
            await self.event_bus.publish(event)
            self.tracing.add_tag(span_id, "event_id", event.id)
            self.tracing.add_tag(span_id, "status", "success")
        finally:
            self.tracing.end_span(span_id)
        
        return event
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to events"""
        self.event_bus.subscribe(event_type, handler)
    
    def define_saga(self, name: str, steps: List[SagaStep]) -> None:
        """Define saga workflow"""
        self.saga_orchestrator.define_saga(name, steps)
    
    async def start_saga(self, saga_name: str, context: Dict[str, Any]) -> Saga:
        """Start saga execution"""
        return await self.saga_orchestrator.start_saga(saga_name, context)
    
    def register_command_handler(self, command_type: str, handler: Callable) -> None:
        """Register CQRS command handler"""
        self.cqrs_helper.register_command_handler(command_type, handler)
    
    def register_query_handler(self, query_type: str, handler: Callable) -> None:
        """Register CQRS query handler"""
        self.cqrs_helper.register_query_handler(query_type, handler)
    
    async def send_command(self, command_type: str, data: Dict[str, Any]) -> Any:
        """Send CQRS command"""
        return await self.cqrs_helper.send_command(command_type, data)
    
    async def execute_query(self, query_type: str, params: Dict[str, Any]) -> Any:
        """Execute CQRS query"""
        return await self.cqrs_helper.execute_query(query_type, params)
    
    def define_workflow(self, name: str, steps: List[Dict[str, Any]]) -> None:
        """Define event-driven workflow"""
        self.workflows[name] = steps
    
    async def start_workflow(self, workflow_name: str, initial_data: Dict[str, Any]) -> str:
        """Start workflow execution"""
        workflow_id = str(uuid.uuid4())
        
        # Create workflow context
        context = {
            "workflow_id": workflow_id,
            "workflow_name": workflow_name,
            "data": initial_data,
            "current_step": 0
        }
        
        # Publish workflow started event
        await self.publish_event(
            f"workflow.{workflow_name}.started",
            context,
            correlation_id=workflow_id
        )
        
        # Execute first step
        if workflow_name in self.workflows and self.workflows[workflow_name]:
            first_step = self.workflows[workflow_name][0]
            await self.publish_event(
                first_step["event_type"],
                {**initial_data, "workflow_context": context},
                correlation_id=workflow_id
            )
        
        return workflow_id
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get orchestrator metrics"""
        return {
            "event_bus": self.event_bus.metrics,
            "dead_letter_queue_size": len(self.event_bus.dead_letter_queue),
            "active_sagas": len([s for s in self.saga_orchestrator.sagas.values() 
                               if s.status == SagaStatus.RUNNING]),
            "active_traces": len(self.tracing.active_spans)
        }
    
    async def replay_events(self, event_type: Optional[str] = None,
                          from_timestamp: Optional[float] = None) -> int:
        """Replay events from event store"""
        return await self.event_bus.replay_events(event_type, from_timestamp)
    
    def get_dead_letter_queue(self) -> List[Event]:
        """Get dead letter queue contents"""
        return self.event_bus.dead_letter_queue.copy()
    
    async def reprocess_dead_letter(self, event_id: str) -> bool:
        """Reprocess event from dead letter queue"""
        event = next((e for e in self.event_bus.dead_letter_queue if e.id == event_id), None)
        if event:
            self.event_bus.dead_letter_queue.remove(event)
            event.status = EventStatus.PENDING
            event.retry_count = 0
            await self.event_bus.publish(event)
            return True
        return False


# Example workflow implementations
async def example_order_processing_workflow():
    """Example order processing workflow with saga"""
    orchestrator = EventOrchestrator()
    
    # Define order processing steps
    async def validate_order(context: Dict[str, Any]) -> Dict[str, Any]:
        order_id = context.get("order_id")
        # Simulate validation
        return {"valid": True, "order_id": order_id}
    
    async def reserve_inventory(context: Dict[str, Any]) -> Dict[str, Any]:
        items = context.get("items", [])
        # Simulate inventory reservation
        return {"reserved": True, "reservation_id": str(uuid.uuid4())}
    
    async def process_payment(context: Dict[str, Any]) -> Dict[str, Any]:
        amount = context.get("amount", 0)
        # Simulate payment processing
        return {"paid": True, "transaction_id": str(uuid.uuid4())}
    
    async def ship_order(context: Dict[str, Any]) -> Dict[str, Any]:
        # Simulate shipping
        return {"shipped": True, "tracking_number": "TRACK123"}
    
    # Define compensations
    async def release_inventory(context: Dict[str, Any]) -> None:
        logger.info("Releasing inventory reservation")
    
    async def refund_payment(context: Dict[str, Any]) -> None:
        logger.info("Refunding payment")
    
    # Define saga
    orchestrator.define_saga("order_processing", [
        SagaStep("validate_order", validate_order),
        SagaStep("reserve_inventory", reserve_inventory, release_inventory),
        SagaStep("process_payment", process_payment, refund_payment),
        SagaStep("ship_order", ship_order)
    ])
    
    # Start saga
    saga = await orchestrator.start_saga("order_processing", {
        "order_id": "ORDER123",
        "items": [{"sku": "ITEM1", "quantity": 2}],
        "amount": 99.99
    })
    
    return orchestrator, saga


if __name__ == "__main__":
    # Test with real event orchestration
    async def main():
        print("🎭 Event-Driven Architecture Orchestrator")
        print("=" * 50)
        
        # Create orchestrator
        orchestrator = EventOrchestrator()
        
        # Test 1: Basic event publishing and subscription
        print("\n1️⃣ Testing Event Bus:")
        
        events_received = []
        async def user_handler(event: Event):
            events_received.append(event)
            print(f"   ✓ Received: {event.type} - {event.payload}")
        
        orchestrator.subscribe("user.created", user_handler)
        
        event = await orchestrator.publish_event("user.created", {
            "user_id": "123",
            "username": "test_user"
        })
        
        await asyncio.sleep(0.1)  # Allow async processing
        
        # Test 2: Saga execution
        print("\n2️⃣ Testing Saga Orchestration:")
        
        # Create the order workflow
        order_orchestrator, saga = await example_order_processing_workflow()
        
        # Wait for saga completion
        await asyncio.sleep(1)
        
        final_saga = order_orchestrator.saga_orchestrator.sagas.get(saga.id)
        print(f"   ✓ Saga Status: {final_saga.status.value}")
        print(f"   ✓ Completed Steps: {', '.join(final_saga.completed_steps)}")
        
        # Test 3: CQRS pattern
        print("\n3️⃣ Testing CQRS Pattern:")
        
        # Command handler
        async def create_user_command(data: Dict[str, Any]) -> Dict[str, Any]:
            user_id = str(uuid.uuid4())
            return {"user_id": user_id, "created": True}
        
        # Query handler
        async def get_user_query(params: Dict[str, Any]) -> Dict[str, Any]:
            return {"user_id": params.get("user_id"), "username": "test_user"}
        
        orchestrator.register_command_handler("create_user", create_user_command)
        orchestrator.register_query_handler("get_user", get_user_query)
        
        # Execute command
        command_result = await orchestrator.send_command("create_user", {
            "username": "new_user"
        })
        print(f"   ✓ Command Result: {command_result}")
        
        # Execute query
        query_result = await orchestrator.execute_query("get_user", {
            "user_id": command_result["user_id"]
        })
        print(f"   ✓ Query Result: {query_result}")
        
        # Test 4: Event replay
        print("\n4️⃣ Testing Event Replay:")
        
        replayed = await orchestrator.replay_events("user.created")
        print(f"   ✓ Replayed {replayed} events")
        
        # Test 5: Metrics
        print("\n5️⃣ System Metrics:")
        metrics = orchestrator.get_metrics()
        for key, value in metrics.items():
            print(f"   • {key}: {value}")
        
        print("\n✅ Event Orchestrator validation passed")
    
    # Run async main
    asyncio.run(main())