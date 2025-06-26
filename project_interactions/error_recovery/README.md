# Intelligent Error Recovery System

A Level 3 orchestration module that implements intelligent error recovery and fault tolerance with machine learning-based prediction and self-healing capabilities.

## Features

### Error Detection & Classification
- **Automatic Error Pattern Recognition**: Learns from error history
- **Severity Assessment**: Classifies errors as LOW, MEDIUM, HIGH, or CRITICAL
- **Context-Aware Analysis**: Considers service context and dependencies
- **Error Correlation**: Identifies related errors across services

### Recovery Strategies
- **Retry**: Simple retry with configurable attempts
- **Exponential Backoff**: Retry with increasing delays
- **Circuit Breaker**: Prevents cascading failures
- **Fallback Mechanisms**: Alternative execution paths
- **Checkpoint/Restore**: State recovery from saved checkpoints
- **Transaction Rollback**: Undo operations on failure
- **Self-Healing**: Automatic remediation for known issues

### Machine Learning
- **Predictive Recovery**: ML model predicts best recovery strategy
- **Pattern Learning**: Improves over time based on outcomes
- **Adaptive Strategies**: Adjusts retry intervals and thresholds
- **Anomaly Detection**: Identifies unusual error patterns

### Orchestration
- **Distributed Recovery**: Coordinates recovery across services
- **Dependency Management**: Respects service dependencies
- **Cascading Failure Prevention**: Isolates failures
- **Health Monitoring**: Continuous service health checks

## Usage

```python
from error_recovery.error_recovery_interaction import ErrorRecoveryInteraction

# Initialize recovery system
recovery = ErrorRecoveryInteraction()

# Basic error recovery
async def risky_operation():
    # Your code that might fail
    pass

try:
    result = await risky_operation()
except Exception as error:
    recovery_result = await recovery.recover_from_error(
        error,
        context={
            "service_id": "my_service",
            "retry_func": risky_operation
        }
    )
    
    if recovery_result["recovery_status"] == "success":
        print("Recovered successfully!")
```

## Recovery Strategies

### Circuit Breaker
```python
from error_recovery.error_recovery_interaction import CircuitBreaker

breaker = CircuitBreaker(failure_threshold=5, timeout=60.0)

if breaker.can_execute():
    try:
        result = await operation()
        breaker.record_success()
    except Exception:
        breaker.record_failure()
        raise
```

### Checkpointing
```python
# Create checkpoint before risky operation
recovery.create_checkpoint("process_1", current_state)

# Restore on failure
result = await recovery._restore_checkpoint("process_1")
```

### Self-Healing
The system automatically handles common errors:
- **Connection Errors**: Automatic reconnection
- **Memory Errors**: Cache clearing and cleanup
- **Rate Limits**: Exponential backoff
- **Timeouts**: Retry with adjusted timeouts

## ML-Based Prediction

The system learns from recovery patterns:
1. Tracks error frequency and recovery success rates
2. Measures average recovery times
3. Analyzes context features
4. Predicts optimal recovery strategy

## Recovery Orchestration

For distributed systems:
```python
orchestrator = RecoveryOrchestrator()

# Define dependencies
orchestrator.dependencies = {
    "api": ["database", "cache"],
    "frontend": ["api", "cdn"]
}

# Orchestrate recovery respecting dependencies
results = await orchestrator.orchestrate_recovery(
    failed_services=["frontend", "api", "database"],
    recovery_plan={
        "database": RecoveryStrategy(action=RecoveryAction.RETRY),
        "api": RecoveryStrategy(action=RecoveryAction.CIRCUIT_BREAK),
        "frontend": RecoveryStrategy(action=RecoveryAction.FALLBACK)
    }
)
```

## Statistics & Monitoring

```python
# Get recovery statistics
stats = recovery.get_recovery_stats()
print(f"Success Rate: {stats['success_rate']:.2%}")
print(f"Avg Recovery Time: {stats['avg_recovery_time']:.2f}s")
print(f"Active Circuit Breakers: {stats['active_circuit_breakers']}")
```

## Integration Examples

### With API Gateway
```python
async def api_handler(request):
    try:
        return await process_request(request)
    except Exception as error:
        result = await recovery.recover_from_error(
            error,
            context={
                "service_id": "api_gateway",
                "endpoint": request.path,
                "retry_func": lambda: process_request(request)
            }
        )
        
        if result["recovery_status"] == "success":
            return success_response()
        else:
            return error_response(result)
```

### With Database Operations
```python
async def db_operation():
    try:
        return await db.query(sql)
    except DatabaseError as error:
        # Recovery system handles reconnection, retry, and failover
        return await recovery.recover_from_error(
            error,
            context={
                "service_id": "database",
                "operation": "query",
                "retry_func": lambda: db.query(sql)
            }
        )
```

## Error Patterns

The system recognizes and learns from various error patterns:
- **Transient Errors**: Network timeouts, temporary unavailability
- **Resource Exhaustion**: Memory, CPU, connection pools
- **Configuration Errors**: Missing configs, invalid settings
- **External Service Failures**: Third-party API issues
- **Cascading Failures**: Dependencies causing chain reactions

## Best Practices

1. **Define Clear Recovery Strategies**: Configure appropriate strategies for different error types
2. **Set Reasonable Thresholds**: Balance between retry attempts and fast failure
3. **Monitor Recovery Metrics**: Track success rates and recovery times
4. **Train the ML Model**: Provide sufficient historical data for accurate predictions
5. **Test Recovery Paths**: Regularly test recovery mechanisms
6. **Document Dependencies**: Clearly define service dependencies for orchestration