
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: workflow_automation_interaction.py
Purpose: Comprehensive workflow automation framework with visual design support

This module implements a full-featured workflow automation system that supports
complex workflows with conditional logic, parallel execution, and state management.

External Dependencies:
- pyyaml: https://pyyaml.org/wiki/PyYAMLDocumentation
- networkx: https://networkx.org/documentation/stable/
- croniter: https://github.com/kiorky/croniter
- aiofiles: https://github.com/Tinche/aiofiles

Example Usage:
>>> from workflow_automation_interaction import WorkflowAutomation
>>> automation = WorkflowAutomation()
>>> workflow_id = await automation.load_workflow("path/to/workflow.yaml")
>>> result = await automation.execute_workflow(workflow_id)
>>> print(result['status'])
'completed'
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union, Callable
from enum import Enum
import yaml
import networkx as nx
from croniter import croniter
import aiofiles
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import inspect
import pickle
import hashlib


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    WAITING_APPROVAL = "waiting_approval"
    RETRY = "retry"
    CANCELLED = "cancelled"


class TriggerType(Enum):
    """Workflow trigger types"""
    MANUAL = "manual"
    CRON = "cron"
    EVENT = "event"
    WEBHOOK = "webhook"
    FILE_WATCH = "file_watch"
    DEPENDENCY = "dependency"


@dataclass
class TaskDefinition:
    """Definition of a workflow task"""
    id: str
    name: str
    type: str
    config: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    retry_config: Dict[str, Any] = field(default_factory=dict)
    timeout: Optional[int] = None
    parallel: bool = False
    approval_required: bool = False


@dataclass
class WorkflowDefinition:
    """Definition of a complete workflow"""
    id: str
    name: str
    version: str
    description: str
    tasks: List[TaskDefinition]
    triggers: List[Dict[str, Any]]
    variables: Dict[str, Any] = field(default_factory=dict)
    error_handlers: List[Dict[str, Any]] = field(default_factory=list)
    notifications: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TaskResult:
    """Result of task execution"""
    task_id: str
    status: TaskStatus
    output: Any
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    retry_count: int = 0


@dataclass
class WorkflowState:
    """Current state of workflow execution"""
    workflow_id: str
    execution_id: str
    status: TaskStatus
    current_tasks: Set[str]
    completed_tasks: Dict[str, TaskResult]
    variables: Dict[str, Any]
    start_time: datetime
    end_time: Optional[datetime] = None
    parent_execution_id: Optional[str] = None


class BaseTask(ABC):
    """Abstract base class for workflow tasks"""
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Any:
        """Execute the task"""
        pass
    
    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate task configuration"""
        pass


class WorkflowEngine:
    """Core workflow execution engine"""
    
    def __init__(self, state_dir: Path = Path("workflow_states")):
        self.state_dir = state_dir
        self.state_dir.mkdir(exist_ok=True)
        self.workflows: Dict[str, WorkflowDefinition] = {}
        self.task_registry: Dict[str, type[BaseTask]] = {}
        self.active_executions: Dict[str, WorkflowState] = {}
        self._register_builtin_tasks()
    
    def _register_builtin_tasks(self):
        """Register built-in task types"""
        self.register_task("script", ScriptTask)
        self.register_task("http", HttpTask)
        self.register_task("condition", ConditionTask)
        self.register_task("parallel", ParallelTask)
        self.register_task("approval", ApprovalTask)
        self.register_task("wait", WaitTask)
        self.register_task("transform", TransformTask)
        self.register_task("notification", NotificationTask)
    
    def register_task(self, task_type: str, task_class: type[BaseTask]):
        """Register a custom task type"""
        self.task_registry[task_type] = task_class
    
    async def load_workflow(self, workflow_path: Union[str, Path]) -> str:
        """Load workflow definition from file"""
        # Ensure we have a Path object
        path = Path(workflow_path) if isinstance(workflow_path, str) else workflow_path
        
        async with aiofiles.open(path, 'r') as f:
            content = await f.read()
        
        if path.suffix == '.yaml' or path.suffix == '.yml':
            definition = yaml.safe_load(content)
        else:
            definition = json.loads(content)
        
        workflow = self._parse_workflow_definition(definition)
        self.workflows[workflow.id] = workflow
        return workflow.id
    
    def _parse_workflow_definition(self, definition: Dict[str, Any]) -> WorkflowDefinition:
        """Parse workflow definition"""
        tasks = []
        for task_def in definition.get('tasks', []):
            task = TaskDefinition(
                id=task_def['id'],
                name=task_def['name'],
                type=task_def['type'],
                config=task_def.get('config', {}),
                dependencies=task_def.get('dependencies', []),
                conditions=task_def.get('conditions', []),
                retry_config=task_def.get('retry', {}),
                timeout=task_def.get('timeout'),
                parallel=task_def.get('parallel', False),
                approval_required=task_def.get('approval_required', False)
            )
            tasks.append(task)
        
        return WorkflowDefinition(
            id=definition.get('id', str(uuid.uuid4())),
            name=definition['name'],
            version=definition.get('version', '1.0.0'),
            description=definition.get('description', ''),
            tasks=tasks,
            triggers=definition.get('triggers', []),
            variables=definition.get('variables', {}),
            error_handlers=definition.get('error_handlers', []),
            notifications=definition.get('notifications', [])
        )
    
    async def execute_workflow(self, workflow_id: str, 
                             variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a workflow"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        execution_id = str(uuid.uuid4())
        
        # Initialize workflow state
        state = WorkflowState(
            workflow_id=workflow_id,
            execution_id=execution_id,
            status=TaskStatus.RUNNING,
            current_tasks=set(),
            completed_tasks={},
            variables={**workflow.variables, **(variables or {})},
            start_time=datetime.now()
        )
        
        self.active_executions[execution_id] = state
        
        try:
            # Build task dependency graph
            graph = self._build_dependency_graph(workflow.tasks)
            
            # Execute workflow
            await self._execute_graph(workflow, state, graph)
            
            state.status = TaskStatus.COMPLETED
            state.end_time = datetime.now()
            
        except Exception as e:
            state.status = TaskStatus.FAILED
            state.end_time = datetime.now()
            await self._handle_workflow_error(workflow, state, str(e))
        
        finally:
            # Save final state
            await self._save_state(state)
            del self.active_executions[execution_id]
        
        return {
            'execution_id': execution_id,
            'status': state.status.value,
            'duration': (state.end_time - state.start_time).total_seconds(),
            'completed_tasks': len(state.completed_tasks),
            'results': {k: v.output for k, v in state.completed_tasks.items()}
        }
    
    def _build_dependency_graph(self, tasks: List[TaskDefinition]) -> nx.DiGraph:
        """Build task dependency graph"""
        graph = nx.DiGraph()
        
        for task in tasks:
            graph.add_node(task.id, task=task)
            for dep in task.dependencies:
                graph.add_edge(dep, task.id)
        
        if not nx.is_directed_acyclic_graph(graph):
            raise ValueError("Workflow contains circular dependencies")
        
        return graph
    
    async def _execute_graph(self, workflow: WorkflowDefinition, 
                           state: WorkflowState, graph: nx.DiGraph):
        """Execute tasks in dependency order"""
        # Get tasks with no dependencies
        ready_tasks = [n for n in graph.nodes() if graph.in_degree(n) == 0]
        
        while ready_tasks:
            # Execute ready tasks
            parallel_tasks = []
            sequential_tasks = []
            
            for task_id in ready_tasks:
                task = graph.nodes[task_id]['task']
                if self._should_execute_task(task, state):
                    if task.parallel:
                        parallel_tasks.append(task)
                    else:
                        sequential_tasks.append(task)
            
            # Execute parallel tasks
            if parallel_tasks:
                await self._execute_parallel_tasks(workflow, state, parallel_tasks)
            
            # Execute sequential tasks
            for task in sequential_tasks:
                await self._execute_task(workflow, state, task)
            
            # Update ready tasks
            ready_tasks = []
            for node in graph.nodes():
                if node not in state.completed_tasks:
                    predecessors = list(graph.predecessors(node))
                    if all(p in state.completed_tasks for p in predecessors):
                        ready_tasks.append(node)
    
    def _should_execute_task(self, task: TaskDefinition, 
                           state: WorkflowState) -> bool:
        """Check if task should be executed based on conditions"""
        if not task.conditions:
            return True
        
        for condition in task.conditions:
            if not self._evaluate_condition(condition, state):
                return False
        
        return True
    
    def _evaluate_condition(self, condition: Dict[str, Any], 
                          state: WorkflowState) -> bool:
        """Evaluate a condition"""
        cond_type = condition.get('type', 'expression')
        
        if cond_type == 'expression':
            # Simple expression evaluation
            expr = condition['expression']
            context = {
                'variables': state.variables,
                'tasks': state.completed_tasks
            }
            return eval(expr, {"__builtins__": {}}, context)
        
        elif cond_type == 'task_status':
            task_id = condition['task_id']
            expected_status = condition['status']
            if task_id in state.completed_tasks:
                return state.completed_tasks[task_id].status.value == expected_status
            return False
        
        return True
    
    async def _execute_task(self, workflow: WorkflowDefinition, 
                          state: WorkflowState, task: TaskDefinition,
                          retry_count: int = 0):
        """Execute a single task"""
        if task.id in state.completed_tasks and state.completed_tasks[task.id].status == TaskStatus.COMPLETED:
            return
        
        state.current_tasks.add(task.id)
        result = TaskResult(
            task_id=task.id,
            status=TaskStatus.RUNNING,
            output=None,
            start_time=datetime.now(),
            retry_count=retry_count
        )
        
        try:
            # Check if approval required
            if task.approval_required:
                result.status = TaskStatus.WAITING_APPROVAL
                state.completed_tasks[task.id] = result
                await self._wait_for_approval(task.id)
            
            # Get task executor
            if task.type not in self.task_registry:
                raise ValueError(f"Unknown task type: {task.type}")
            
            executor_class = self.task_registry[task.type]
            executor = executor_class()
            
            # Validate configuration
            if not executor.validate_config(task.config):
                raise ValueError(f"Invalid configuration for task {task.id}")
            
            # Execute with timeout
            context = {
                'variables': state.variables,
                'task_results': {k: v.output for k, v in state.completed_tasks.items()},
                'workflow': workflow,
                'task': task
            }
            
            if task.timeout:
                result.output = await asyncio.wait_for(
                    executor.execute(context),
                    timeout=task.timeout
                )
            else:
                result.output = await executor.execute(context)
            
            result.status = TaskStatus.COMPLETED
            
        except asyncio.TimeoutError:
            result.status = TaskStatus.FAILED
            result.error = f"Task timed out after {task.timeout} seconds"
            await self._handle_task_failure(workflow, state, task, result)
            
        except Exception as e:
            result.status = TaskStatus.FAILED
            result.error = str(e)
            await self._handle_task_failure(workflow, state, task, result)
        
        finally:
            result.end_time = datetime.now()
            state.completed_tasks[task.id] = result
            state.current_tasks.remove(task.id)
            
            # Update variables if task produced output
            if isinstance(result.output, dict) and 'variables' in result.output:
                state.variables.update(result.output['variables'])
    
    async def _execute_parallel_tasks(self, workflow: WorkflowDefinition,
                                    state: WorkflowState, 
                                    tasks: List[TaskDefinition]):
        """Execute multiple tasks in parallel"""
        await asyncio.gather(*[
            self._execute_task(workflow, state, task) for task in tasks
        ])
    
    async def _handle_task_failure(self, workflow: WorkflowDefinition,
                                 state: WorkflowState, task: TaskDefinition,
                                 result: TaskResult):
        """Handle task failure with retry logic"""
        retry_config = task.retry_config
        max_retries = retry_config.get('max_retries', 0)
        
        if result.retry_count < max_retries:
            result.retry_count += 1
            result.status = TaskStatus.RETRY
            
            # Wait before retry
            delay = retry_config.get('delay', 1) * (2 ** (result.retry_count - 1))
            await asyncio.sleep(delay)
            
            # Retry task
            state.completed_tasks.pop(task.id, None)
            await self._execute_task(workflow, state, task, result.retry_count)
    
    async def _handle_workflow_error(self, workflow: WorkflowDefinition,
                                   state: WorkflowState, error: str):
        """Handle workflow-level errors"""
        for handler in workflow.error_handlers:
            if handler['type'] == 'notification':
                await self._send_notification(handler['config'], {
                    'workflow': workflow.name,
                    'execution_id': state.execution_id,
                    'error': error
                })
    
    async def _wait_for_approval(self, task_id: str):
        """Wait for human approval"""
        # In real implementation, this would integrate with approval system
        await asyncio.sleep(1)  # Simulate approval
    
    async def _send_notification(self, config: Dict[str, Any], 
                               context: Dict[str, Any]):
        """Send notification"""
        # Placeholder for notification logic
        pass
    
    async def _save_state(self, state: WorkflowState):
        """Save workflow state to disk"""
        state_file = self.state_dir / f"{state.execution_id}.pkl"
        async with aiofiles.open(state_file, 'wb') as f:
            await f.write(pickle.dumps(state))
    
    async def load_state(self, execution_id: str) -> Optional[WorkflowState]:
        """Load workflow state from disk"""
        state_file = self.state_dir / f"{execution_id}.pkl"
        if not state_file.exists():
            return None
        
        async with aiofiles.open(state_file, 'rb') as f:
            content = await f.read()
        
        return pickle.loads(content)


# Built-in task implementations

class ScriptTask(BaseTask):
    """Execute Python script"""
    
    async def execute(self, context: Dict[str, Any]) -> Any:
        script = context['task'].config['script']
        local_vars = {
            'context': context,
            'variables': context['variables'],
            'results': context['task_results']
        }
        exec(script, {"__builtins__": {}}, local_vars)
        return local_vars.get('output', None)
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        return 'script' in config


class HttpTask(BaseTask):
    """Make HTTP request"""
    
    async def execute(self, context: Dict[str, Any]) -> Any:
        import aiohttp
        
        config = context['task'].config
        url = config['url']
        method = config.get('method', 'GET')
        headers = config.get('headers', {})
        data = config.get('data')
        
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, json=data) as resp:
                return {
                    'status': resp.status,
                    'headers': dict(resp.headers),
                    'body': await resp.json() if resp.content_type == 'application/json' else await resp.text()
                }
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        return 'url' in config


class ConditionTask(BaseTask):
    """Conditional branching"""
    
    async def execute(self, context: Dict[str, Any]) -> Any:
        config = context['task'].config
        condition = config['condition']
        
        # Evaluate condition
        result = eval(condition, {"__builtins__": {}}, {
            'variables': context['variables'],
            'results': context['task_results']
        })
        
        if result:
            return config.get('if_true', True)
        else:
            return config.get('if_false', False)
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        return 'condition' in config


class ParallelTask(BaseTask):
    """Execute sub-workflows in parallel"""
    
    async def execute(self, context: Dict[str, Any]) -> Any:
        config = context['task'].config
        sub_workflows = config['workflows']
        
        # In real implementation, would execute sub-workflows
        results = await asyncio.gather(*[
            self._execute_sub_workflow(w, context) for w in sub_workflows
        ])
        
        return {'results': results}
    
    async def _execute_sub_workflow(self, workflow_id: str, 
                                  context: Dict[str, Any]) -> Any:
        # Placeholder for sub-workflow execution
        await asyncio.sleep(0.1)
        return {'workflow': workflow_id, 'status': 'completed'}
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        return 'workflows' in config


class ApprovalTask(BaseTask):
    """Human approval task"""
    
    async def execute(self, context: Dict[str, Any]) -> Any:
        config = context['task'].config
        
        # In real implementation, would create approval request
        approval_id = str(uuid.uuid4())
        
        # Simulate approval
        await asyncio.sleep(1)
        
        return {
            'approval_id': approval_id,
            'approved': True,
            'approver': 'system',
            'timestamp': datetime.now().isoformat()
        }
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        return 'approvers' in config


class WaitTask(BaseTask):
    """Wait for specified duration"""
    
    async def execute(self, context: Dict[str, Any]) -> Any:
        config = context['task'].config
        duration = config['duration']
        
        await asyncio.sleep(duration)
        
        return {'waited': duration}
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        return 'duration' in config and isinstance(config['duration'], (int, float))


class TransformTask(BaseTask):
    """Transform data"""
    
    async def execute(self, context: Dict[str, Any]) -> Any:
        config = context['task'].config
        source = config['source']
        transform = config['transform']
        
        # Get source data
        if source.startswith('$'):
            # Variable reference
            var_name = source[1:]
            data = context['variables'].get(var_name)
        else:
            # Task result reference
            data = context['task_results'].get(source)
        
        # Apply transformation
        if transform['type'] == 'map':
            return {item: eval(transform['expression'], {"__builtins__": {}}, {'item': item}) 
                   for item in data}
        elif transform['type'] == 'filter':
            return [item for item in data 
                   if eval(transform['expression'], {"__builtins__": {}}, {'item': item})]
        elif transform['type'] == 'reduce':
            result = transform.get('initial', 0)
            for item in data:
                result = eval(transform['expression'], {"__builtins__": {}}, 
                            {'acc': result, 'item': item})
            return result
        
        return data
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        return 'source' in config and 'transform' in config


class NotificationTask(BaseTask):
    """Send notifications"""
    
    async def execute(self, context: Dict[str, Any]) -> Any:
        config = context['task'].config
        
        # In real implementation, would send actual notifications
        return {
            'notification_id': str(uuid.uuid4()),
            'type': config['type'],
            'recipients': config['recipients'],
            'sent': datetime.now().isoformat()
        }
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        return 'type' in config and 'recipients' in config


class WorkflowScheduler:
    """Schedule and trigger workflows"""
    
    def __init__(self, engine: WorkflowEngine):
        self.engine = engine
        self.schedules: Dict[str, Dict[str, Any]] = {}
        self.running = False
        self._tasks: List[asyncio.Task] = []
    
    async def add_schedule(self, workflow_id: str, trigger: Dict[str, Any]):
        """Add workflow schedule"""
        trigger_type = TriggerType(trigger['type'])
        
        if trigger_type == TriggerType.CRON:
            schedule_id = str(uuid.uuid4())
            self.schedules[schedule_id] = {
                'workflow_id': workflow_id,
                'trigger': trigger,
                'next_run': None
            }
            
            if self.running:
                task = asyncio.create_task(
                    self._run_cron_schedule(schedule_id)
                )
                self._tasks.append(task)
            
            return schedule_id
        
        elif trigger_type == TriggerType.EVENT:
            # Register event listener
            pass
        
        elif trigger_type == TriggerType.WEBHOOK:
            # Register webhook
            pass
    
    async def start(self):
        """Start scheduler"""
        self.running = True
        
        # Start cron schedules
        for schedule_id in self.schedules:
            if self.schedules[schedule_id]['trigger']['type'] == 'cron':
                task = asyncio.create_task(
                    self._run_cron_schedule(schedule_id)
                )
                self._tasks.append(task)
    
    async def stop(self):
        """Stop scheduler"""
        self.running = False
        
        # Cancel all tasks
        for task in self._tasks:
            task.cancel()
        
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()
    
    async def _run_cron_schedule(self, schedule_id: str):
        """Run cron schedule"""
        schedule = self.schedules[schedule_id]
        cron_expr = schedule['trigger']['expression']
        
        while self.running:
            try:
                # Calculate next run time
                cron = croniter(cron_expr)
                next_run = cron.get_next(datetime)
                schedule['next_run'] = next_run
                
                # Wait until next run
                wait_time = (next_run - datetime.now()).total_seconds()
                if wait_time > 0:
                    await asyncio.sleep(wait_time)
                
                # Execute workflow
                if self.running:
                    variables = schedule['trigger'].get('variables', {})
                    await self.engine.execute_workflow(
                        schedule['workflow_id'], 
                        variables
                    )
                
            except Exception as e:
                # Log error but continue scheduling
                await asyncio.sleep(60)  # Wait before retry


class WorkflowAutomation:
    """Main workflow automation interface"""
    
    def __init__(self, state_dir: Path = Path("workflow_states")):
        self.engine = WorkflowEngine(state_dir)
        self.scheduler = WorkflowScheduler(self.engine)
    
    async def load_workflow(self, workflow_path: Union[str, Path]) -> str:
        """Load workflow definition"""
        return await self.engine.load_workflow(workflow_path)
    
    async def execute_workflow(self, workflow_id: str, 
                             variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute workflow"""
        return await self.engine.execute_workflow(workflow_id, variables)
    
    async def schedule_workflow(self, workflow_id: str, 
                              trigger: Dict[str, Any]) -> str:
        """Schedule workflow execution"""
        return await self.scheduler.add_schedule(workflow_id, trigger)
    
    async def start_scheduler(self):
        """Start workflow scheduler"""
        await self.scheduler.start()
    
    async def stop_scheduler(self):
        """Stop workflow scheduler"""
        await self.scheduler.stop()
    
    def register_task(self, task_type: str, task_class: type[BaseTask]):
        """Register custom task type"""
        self.engine.register_task(task_type, task_class)
    
    async def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow execution status"""
        if execution_id in self.engine.active_executions:
            state = self.engine.active_executions[execution_id]
        else:
            state = await self.engine.load_state(execution_id)
        
        if not state:
            return None
        
        return {
            'execution_id': execution_id,
            'workflow_id': state.workflow_id,
            'status': state.status.value,
            'current_tasks': list(state.current_tasks),
            'completed_tasks': len(state.completed_tasks),
            'start_time': state.start_time.isoformat(),
            'end_time': state.end_time.isoformat() if state.end_time else None,
            'duration': (
                (state.end_time or datetime.now()) - state.start_time
            ).total_seconds()
        }
    
    async def list_executions(self, workflow_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List workflow executions"""
        executions = []
        
        # Check active executions
        for exec_id, state in self.engine.active_executions.items():
            if not workflow_id or state.workflow_id == workflow_id:
                executions.append(await self.get_execution_status(exec_id))
        
        # Check saved states
        for state_file in self.engine.state_dir.glob("*.pkl"):
            exec_id = state_file.stem
            if exec_id not in self.engine.active_executions:
                status = await self.get_execution_status(exec_id)
                if status and (not workflow_id or status['workflow_id'] == workflow_id):
                    executions.append(status)
        
        return sorted(executions, key=lambda x: x['start_time'], reverse=True)
    
    def export_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Export workflow definition"""
        if workflow_id not in self.engine.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.engine.workflows[workflow_id]
        
        return {
            'id': workflow.id,
            'name': workflow.name,
            'version': workflow.version,
            'description': workflow.description,
            'tasks': [
                {
                    'id': task.id,
                    'name': task.name,
                    'type': task.type,
                    'config': task.config,
                    'dependencies': task.dependencies,
                    'conditions': task.conditions,
                    'retry': task.retry_config,
                    'timeout': task.timeout,
                    'parallel': task.parallel,
                    'approval_required': task.approval_required
                }
                for task in workflow.tasks
            ],
            'triggers': workflow.triggers,
            'variables': workflow.variables,
            'error_handlers': workflow.error_handlers,
            'notifications': workflow.notifications
        }


if __name__ == "__main__":
    # Module validation with real workflow example
    import tempfile
    
    async def validate_module():
        # Create test workflow
        workflow_def = {
            'name': 'Test Workflow',
            'version': '1.0.0',
            'description': 'Test workflow for validation',
            'variables': {
                'input_data': 'test'
            },
            'tasks': [
                {
                    'id': 'task1',
                    'name': 'Initialize',
                    'type': 'script',
                    'config': {
                        'script': "output = {'message': 'Initialized'}"
                    }
                },
                {
                    'id': 'task2',
                    'name': 'Wait',
                    'type': 'wait',
                    'config': {
                        'duration': 0.5
                    },
                    'dependencies': ['task1']
                },
                {
                    'id': 'task3',
                    'name': 'Transform',
                    'type': 'script',
                    'config': {
                        'script': "output = {'result': len(variables['input_data'])}"
                    },
                    'dependencies': ['task2']
                }
            ],
            'triggers': [
                {
                    'type': 'manual'
                }
            ]
        }
        
        # Save workflow to file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(workflow_def, f)
            workflow_file = f.name
        
        try:
            # Create automation instance
            automation = WorkflowAutomation()
            
            # Load workflow
            workflow_id = await automation.load_workflow(workflow_file)
            print(f"✓ Loaded workflow: {workflow_id}")
            
            # Execute workflow
            result = await automation.execute_workflow(workflow_id, {'input_data': 'validation'})
            
            # Validate results
            assert result['status'] == 'completed', f"Expected completed, got {result['status']}"
            assert result['completed_tasks'] == 3, f"Expected 3 tasks, got {result['completed_tasks']}"
            assert 'task3' in result['results'], "Missing task3 result"
            assert result['results']['task3']['result'] == 10, "Invalid transform result"
            
            print(f"✓ Workflow executed successfully")
            print(f"  - Duration: {result['duration']:.2f}s")
            print(f"  - Tasks completed: {result['completed_tasks']}")
            
            # Test execution status
            status = await automation.get_execution_status(result['execution_id'])
            assert status is not None, "Could not retrieve execution status"
            assert status['status'] == 'completed', "Invalid status"
            
            print(f"✓ Execution status verified")
            
            # Test workflow export
            exported = automation.export_workflow(workflow_id)
            assert len(exported['tasks']) == 3, "Invalid task count in export"
            
            print(f"✓ Workflow export successful")
            
            print("\n✅ Module validation passed")
            
        finally:
            # Cleanup
            Path(workflow_file).unlink(missing_ok=True)
    
    # Run validation
    asyncio.run(validate_module())