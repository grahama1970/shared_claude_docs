# Workflow Automation Framework

A comprehensive workflow automation system that provides visual workflow design support, complex task orchestration, and state management capabilities.

## Features

### Core Capabilities
- **Workflow Definition Language**: Support for YAML/JSON workflow definitions
- **Task Dependencies**: Automatic dependency resolution and execution ordering
- **Conditional Branching**: Dynamic workflow paths based on conditions
- **Parallel Execution**: Run multiple tasks simultaneously
- **Error Handling**: Automatic retries with exponential backoff
- **State Persistence**: Full workflow state saved and recoverable
- **Human-in-the-Loop**: Approval tasks with wait functionality

### Advanced Features
- **Visual Designer Support**: Structured for integration with visual workflow builders
- **Pre-built Task Library**: Common tasks ready to use
- **Custom Task Plugins**: Easy extension with custom task types
- **Event-driven Triggers**: Multiple trigger types (cron, webhook, event)
- **Cron Scheduling**: Schedule workflows with cron expressions
- **Webhook Integration**: Trigger workflows via webhooks
- **Approval Workflows**: Human approval requirements
- **Workflow Versioning**: Track and manage workflow versions

## Installation

```bash
# Install dependencies
pip install pyyaml networkx croniter aiofiles
```

## Usage

### Basic Workflow Example

```python
from workflow_automation_interaction import WorkflowAutomation

# Create automation instance
automation = WorkflowAutomation()

# Load workflow from YAML file
workflow_id = await automation.load_workflow("workflow.yaml")

# Execute workflow with variables
result = await automation.execute_workflow(
    workflow_id,
    variables={'input': 'data'}
)

print(f"Status: {result['status']}")
print(f"Duration: {result['duration']}s")
```

### Workflow Definition (YAML)

```yaml
name: Data Processing Workflow
version: 1.0.0
description: Process incoming data with validation

variables:
  threshold: 100
  output_format: json

tasks:
  - id: validate
    name: Validate Input
    type: script
    config:
      script: |
        if not variables.get('input_data'):
            raise ValueError("No input data")
        output = {'valid': True, 'count': len(variables['input_data'])}

  - id: transform
    name: Transform Data
    type: transform
    dependencies: [validate]
    config:
      source: $input_data
      transform:
        type: map
        expression: "{'id': item['id'], 'value': item['value'] * 2}"

  - id: check_threshold
    name: Check Threshold
    type: condition
    dependencies: [transform]
    config:
      condition: "results['validate']['count'] > variables['threshold']"
      if_true: {needs_approval: true}
      if_false: {needs_approval: false}

  - id: approval
    name: Manager Approval
    type: approval
    dependencies: [check_threshold]
    conditions:
      - type: expression
        expression: "tasks['check_threshold'].output['needs_approval']"
    config:
      approvers: [manager@example.com]
      timeout: 3600

  - id: notify
    name: Send Notification
    type: notification
    dependencies: [transform]
    config:
      type: email
      recipients: [team@example.com]
      template: completion_notification

triggers:
  - type: cron
    expression: "0 9 * * *"  # Daily at 9 AM
  - type: webhook
    path: /workflows/data-processing
```

### Custom Task Development

```python
from workflow_automation_interaction import BaseTask

class DatabaseTask(BaseTask):
    """Custom task for database operations"""
    
    async def execute(self, context):
        config = context['task'].config
        query = config['query']
        
        # Execute database query
        result = await db.execute(query, context['variables'])
        
        return {
            'rows_affected': result.rowcount,
            'data': result.fetchall()
        }
    
    def validate_config(self, config):
        return 'query' in config

# Register custom task
automation.register_task('database', DatabaseTask)
```

### Scheduling Workflows

```python
# Schedule workflow with cron
schedule_id = await automation.schedule_workflow(
    workflow_id,
    trigger={
        'type': 'cron',
        'expression': '*/30 * * * *',  # Every 30 minutes
        'variables': {'mode': 'scheduled'}
    }
)

# Start scheduler
await automation.start_scheduler()

# Stop scheduler when done
await automation.stop_scheduler()
```

## Built-in Task Types

### Script Task
Execute Python code with access to workflow context:
```yaml
type: script
config:
  script: |
    result = variables['input'] * 2
    output = {'result': result}
```

### HTTP Task
Make HTTP requests:
```yaml
type: http
config:
  url: https://api.example.com/data
  method: POST
  headers:
    Authorization: Bearer ${API_TOKEN}
  data:
    value: ${variables.input}
```

### Condition Task
Conditional branching:
```yaml
type: condition
config:
  condition: "variables['score'] >= 80"
  if_true: {grade: 'A'}
  if_false: {grade: 'B'}
```

### Wait Task
Pause execution:
```yaml
type: wait
config:
  duration: 30  # seconds
```

### Transform Task
Data transformation:
```yaml
type: transform
config:
  source: $data_array
  transform:
    type: filter  # map, filter, or reduce
    expression: "item['active'] == True"
```

### Approval Task
Human approval:
```yaml
type: approval
config:
  approvers: [manager@example.com]
  timeout: 7200  # 2 hours
```

### Notification Task
Send notifications:
```yaml
type: notification
config:
  type: email
  recipients: [team@example.com]
  subject: Workflow Completed
```

## State Management

Workflow state is automatically persisted and can be queried:

```python
# Get execution status
status = await automation.get_execution_status(execution_id)

# List all executions
executions = await automation.list_executions()

# List executions for specific workflow
executions = await automation.list_executions(workflow_id)
```

## Error Handling

Configure retry logic for tasks:

```yaml
retry:
  max_retries: 3
  delay: 5  # Initial delay in seconds
  backoff: exponential  # or linear
```

Add error handlers at workflow level:

```yaml
error_handlers:
  - type: notification
    config:
      type: slack
      webhook: ${SLACK_WEBHOOK}
      message: "Workflow failed: ${error}"
```

## Best Practices

1. **Keep workflows modular**: Break complex workflows into smaller sub-workflows
2. **Use variables**: Parameterize workflows for reusability
3. **Add error handling**: Always configure retry and error handlers
4. **Version workflows**: Track changes with semantic versioning
5. **Test thoroughly**: Use the test suite to validate workflows
6. **Monitor executions**: Regularly check execution history and failures

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_workflow_execution.py -v

# Run verification script
python test_task_57.py
```

## Architecture

The framework consists of:

- **WorkflowEngine**: Core execution engine with dependency resolution
- **WorkflowScheduler**: Handles cron and event-based triggers
- **BaseTask**: Abstract base for all task types
- **WorkflowState**: Manages execution state and persistence
- **WorkflowAutomation**: Main interface combining all components

## Contributing

To add new task types:

1. Extend `BaseTask` class
2. Implement `execute()` and `validate_config()` methods
3. Register with `automation.register_task()`
4. Add tests for the new task type

## License

MIT License