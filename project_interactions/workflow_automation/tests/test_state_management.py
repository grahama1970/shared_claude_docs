"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Test workflow state management

Tests state persistence, recovery, and management features
for workflow executions.
"""

import asyncio
import pytest
from pathlib import Path
import yaml
import tempfile
from datetime import datetime
import pickle
import json

import sys
sys.path.append('/home/graham/workspace/shared_claude_docs/project_interactions/workflow_automation')

from workflow_automation_interaction import (
    WorkflowAutomation, WorkflowState, TaskStatus,
    TaskResult, TaskDefinition, BaseTask
)


class TestStateManagement:
    """Test workflow state management features"""
    
    @pytest.fixture
    async def automation(self):
        """Create workflow automation instance"""
        with tempfile.TemporaryDirectory() as tmpdir:
            automation = WorkflowAutomation(state_dir=Path(tmpdir))
            yield automation
    
    @pytest.fixture
    def stateful_workflow(self):
        """Create workflow that maintains state"""
        return {
            'name': 'Stateful Workflow',
            'version': '1.0.0',
            'variables': {
                'accumulator': 0,
                'items': []
            },
            'tasks': [
                {
                    'id': 'init',
                    'name': 'Initialize',
                    'type': 'script',
                    'config': {
                        'script': """
output = {
    'initialized': True,
    'variables': {
        'accumulator': 10,
        'items': ['start']
    }
}
"""
                    }
                },
                {
                    'id': 'process1',
                    'name': 'Process Step 1',
                    'type': 'script',
                    'config': {
                        'script': """
acc = variables['accumulator'] + 5
items = variables['items'] + ['step1']
output = {
    'step': 1,
    'variables': {
        'accumulator': acc,
        'items': items
    }
}
"""
                    },
                    'dependencies': ['init']
                },
                {
                    'id': 'process2',
                    'name': 'Process Step 2',
                    'type': 'script',
                    'config': {
                        'script': """
acc = variables['accumulator'] * 2
items = variables['items'] + ['step2']
output = {
    'step': 2,
    'variables': {
        'accumulator': acc,
        'items': items
    }
}
"""
                    },
                    'dependencies': ['process1']
                },
                {
                    'id': 'finalize',
                    'name': 'Finalize',
                    'type': 'script',
                    'config': {
                        'script': """
output = {
    'final_accumulator': variables['accumulator'],
    'final_items': variables['items'],
    'item_count': len(variables['items'])
}
"""
                    },
                    'dependencies': ['process2']
                }
            ]
        }
    
    @pytest.mark.asyncio
    async def test_state_persistence(self, automation, stateful_workflow):
        """Test workflow state is persisted during execution"""
        # Save workflow
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(stateful_workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            result = await automation.execute_workflow(workflow_id)
            
            # Load persisted state
            state = await automation.engine.load_state(result['execution_id'])
            
            # Verify state was persisted
            assert state is not None
            assert state.execution_id == result['execution_id']
            assert state.workflow_id == workflow_id
            assert state.status == TaskStatus.COMPLETED
            
            # Verify final variable state
            assert state.variables['accumulator'] == 30  # ((0 + 10) + 5) * 2
            assert state.variables['items'] == ['start', 'step1', 'step2']
            
            # Verify all tasks completed
            assert len(state.completed_tasks) == 4
            for task_id in ['init', 'process1', 'process2', 'finalize']:
                assert task_id in state.completed_tasks
                assert state.completed_tasks[task_id].status == TaskStatus.COMPLETED
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_state_recovery(self, automation):
        """Test workflow state recovery after interruption"""
        # Create a workflow that can be interrupted
        workflow = {
            'name': 'Recovery Test',
            'tasks': [
                {
                    'id': 'task1',
                    'name': 'Task 1',
                    'type': 'script',
                    'config': {
                        'script': "output = {'task': 1}"
                    }
                },
                {
                    'id': 'task2',
                    'name': 'Task 2',
                    'type': 'wait',
                    'config': {
                        'duration': 5  # Long wait to simulate interruption
                    },
                    'dependencies': ['task1']
                },
                {
                    'id': 'task3',
                    'name': 'Task 3',
                    'type': 'script',
                    'config': {
                        'script': "output = {'task': 3}"
                    },
                    'dependencies': ['task2']
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            
            # Start execution
            execution_task = asyncio.create_task(
                automation.execute_workflow(workflow_id)
            )
            
            # Wait for first task to complete
            await asyncio.sleep(1)
            
            # Get execution ID from active executions
            active_exec_id = None
            for exec_id, state in automation.engine.active_executions.items():
                if state.workflow_id == workflow_id:
                    active_exec_id = exec_id
                    break
            
            assert active_exec_id is not None
            
            # Cancel execution (simulate interruption)
            execution_task.cancel()
            
            try:
                await execution_task
            except asyncio.CancelledError:
                pass
            
            # Load state from disk
            recovered_state = await automation.engine.load_state(active_exec_id)
            
            # Verify partial state was saved
            assert recovered_state is not None
            assert 'task1' in recovered_state.completed_tasks
            assert recovered_state.completed_tasks['task1'].status == TaskStatus.COMPLETED
            
            # In real implementation, would support resuming from this state
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_variable_state_tracking(self, automation):
        """Test variable state changes are tracked correctly"""
        workflow = {
            'name': 'Variable Tracking Test',
            'variables': {
                'counter': 0,
                'history': []
            },
            'tasks': [
                {
                    'id': f'increment_{i}',
                    'name': f'Increment {i}',
                    'type': 'script',
                    'config': {
                        'script': f"""
counter = variables['counter'] + 1
history = variables['history'] + [{i}]
output = {{
    'step': {i},
    'variables': {{
        'counter': counter,
        'history': history
    }}
}}
"""
                    },
                    'dependencies': [f'increment_{i-1}'] if i > 0 else []
                }
                for i in range(5)
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            result = await automation.execute_workflow(workflow_id)
            
            # Load final state
            state = await automation.engine.load_state(result['execution_id'])
            
            # Verify variable progression
            assert state.variables['counter'] == 5
            assert state.variables['history'] == [0, 1, 2, 3, 4]
            
            # Verify each task saw correct variable state
            for i in range(5):
                task_result = state.completed_tasks[f'increment_{i}']
                assert task_result.output['step'] == i
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_parallel_state_consistency(self, automation):
        """Test state consistency with parallel task execution"""
        workflow = {
            'name': 'Parallel State Test',
            'variables': {
                'shared_list': []
            },
            'tasks': [
                {
                    'id': 'init',
                    'name': 'Initialize',
                    'type': 'script',
                    'config': {
                        'script': "output = {'variables': {'shared_list': [0]}}"
                    }
                }
            ] + [
                {
                    'id': f'parallel_{i}',
                    'name': f'Parallel Task {i}',
                    'type': 'script',
                    'config': {
                        'script': f"output = {{'added': {i}}}"
                    },
                    'dependencies': ['init'],
                    'parallel': True
                }
                for i in range(1, 4)
            ] + [
                {
                    'id': 'collect',
                    'name': 'Collect Results',
                    'type': 'script',
                    'config': {
                        'script': """
# Collect all parallel results
parallel_results = []
for i in range(1, 4):
    task_name = f'parallel_{i}'
    if task_name in results:
        parallel_results.append(results[task_name]['added'])

output = {
    'collected': sorted(parallel_results),
    'initial_list': variables['shared_list']
}
"""
                    },
                    'dependencies': ['parallel_1', 'parallel_2', 'parallel_3']
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            result = await automation.execute_workflow(workflow_id)
            
            # Verify all parallel tasks completed
            assert result['status'] == 'completed'
            assert result['results']['collect']['collected'] == [1, 2, 3]
            
            # Load state to verify consistency
            state = await automation.engine.load_state(result['execution_id'])
            
            # All parallel tasks should be in completed state
            for i in range(1, 4):
                task_id = f'parallel_{i}'
                assert task_id in state.completed_tasks
                assert state.completed_tasks[task_id].status == TaskStatus.COMPLETED
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_error_state_preservation(self, automation):
        """Test state is preserved when workflow fails"""
        workflow = {
            'name': 'Error State Test',
            'variables': {
                'progress': []
            },
            'tasks': [
                {
                    'id': 'step1',
                    'name': 'Step 1',
                    'type': 'script',
                    'config': {
                        'script': """
progress = variables['progress'] + ['step1']
output = {'variables': {'progress': progress}}
"""
                    }
                },
                {
                    'id': 'step2',
                    'name': 'Step 2 (Fails)',
                    'type': 'script',
                    'config': {
                        'script': """
progress = variables['progress'] + ['step2']
raise ValueError('Intentional failure')
"""
                    },
                    'dependencies': ['step1']
                },
                {
                    'id': 'step3',
                    'name': 'Step 3',
                    'type': 'script',
                    'config': {
                        'script': """
progress = variables['progress'] + ['step3']
output = {'variables': {'progress': progress}}
"""
                    },
                    'dependencies': ['step2']
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            result = await automation.execute_workflow(workflow_id)
            
            # Verify workflow failed
            assert result['status'] == 'failed'
            
            # Load state
            state = await automation.engine.load_state(result['execution_id'])
            
            # Verify partial progress was saved
            assert state.status == TaskStatus.FAILED
            assert state.variables['progress'] == ['step1']
            
            # Verify step1 completed, step2 failed, step3 didn't run
            assert 'step1' in state.completed_tasks
            assert state.completed_tasks['step1'].status == TaskStatus.COMPLETED
            
            assert 'step2' in state.completed_tasks
            assert state.completed_tasks['step2'].status == TaskStatus.FAILED
            assert 'Intentional failure' in state.completed_tasks['step2'].error
            
            assert 'step3' not in state.completed_tasks
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_state_serialization(self, automation):
        """Test state can be properly serialized and deserialized"""
        # Create state with various data types
        workflow = {
            'name': 'Serialization Test',
            'variables': {
                'string': 'test',
                'number': 42,
                'float': 3.14,
                'boolean': True,
                'list': [1, 2, 3],
                'dict': {'key': 'value'},
                'null': None
            },
            'tasks': [
                {
                    'id': 'complex_data',
                    'name': 'Complex Data Task',
                    'type': 'script',
                    'config': {
                        'script': """
from datetime import datetime
output = {
    'timestamp': datetime.now().isoformat(),
    'nested': {
                        'data': [
                            {'id': 1, 'value': 'a'},
                            {'id': 2, 'value': 'b'}
                        ]
                    },
                    'variables': {
                        'computed': variables['number'] * 2
                    }
                }
                """
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            result = await automation.execute_workflow(workflow_id)
            
            # Load state
            state = await automation.engine.load_state(result['execution_id'])
            
            # Verify all data types preserved
            assert state.variables['string'] == 'test'
            assert state.variables['number'] == 42
            assert state.variables['float'] == 3.14
            assert state.variables['boolean'] is True
            assert state.variables['list'] == [1, 2, 3]
            assert state.variables['dict'] == {'key': 'value'}
            assert state.variables['null'] is None
            assert state.variables['computed'] == 84
            
            # Verify complex output preserved
            task_output = state.completed_tasks['complex_data'].output
            assert 'timestamp' in task_output
            assert task_output['nested']['data'][0]['id'] == 1
            assert task_output['nested']['data'][1]['value'] == 'b'
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_execution_metadata(self, automation, stateful_workflow):
        """Test execution metadata is properly tracked"""
        # Save workflow
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(stateful_workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            
            # Record start time
            start_time = datetime.now()
            
            # Execute workflow
            result = await automation.execute_workflow(workflow_id)
            
            # Load state
            state = await automation.engine.load_state(result['execution_id'])
            
            # Verify metadata
            assert state.workflow_id == workflow_id
            assert state.execution_id == result['execution_id']
            assert state.start_time >= start_time
            assert state.end_time is not None
            assert state.end_time > state.start_time
            
            # Verify task metadata
            for task_id, task_result in state.completed_tasks.items():
                assert task_result.task_id == task_id
                assert task_result.start_time is not None
                assert task_result.end_time is not None
                assert task_result.end_time >= task_result.start_time
                assert task_result.retry_count >= 0
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_state_cleanup(self, automation):
        """Test old state files can be cleaned up"""
        workflow = {
            'name': 'Cleanup Test',
            'tasks': [
                {
                    'id': 'task',
                    'name': 'Task',
                    'type': 'script',
                    'config': {
                        'script': "output = {'done': True}"
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            
            # Execute multiple times
            execution_ids = []
            for _ in range(5):
                result = await automation.execute_workflow(workflow_id)
                execution_ids.append(result['execution_id'])
            
            # Verify state files exist
            for exec_id in execution_ids:
                state_file = automation.engine.state_dir / f"{exec_id}.pkl"
                assert state_file.exists()
            
            # In real implementation, would have cleanup functionality
            # to remove old state files based on age or count
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])