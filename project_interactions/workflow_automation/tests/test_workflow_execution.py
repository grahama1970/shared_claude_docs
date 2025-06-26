"""
Test workflow execution functionality

Tests the core workflow execution engine including task execution,
dependency management, and error handling.
"""

import asyncio
import pytest
from pathlib import Path
import yaml
import tempfile
from datetime import datetime

import sys
sys.path.append('/home/graham/workspace/shared_claude_docs/project_interactions/workflow_automation')

from workflow_automation_interaction import (
    WorkflowAutomation, WorkflowEngine, TaskStatus,
    TaskDefinition, BaseTask, ScriptTask
)


class TestWorkflowExecution:
    """Test workflow execution features"""
    
    @pytest.fixture
    async def automation(self):
        """Create workflow automation instance"""
        with tempfile.TemporaryDirectory() as tmpdir:
            automation = WorkflowAutomation(state_dir=Path(tmpdir))
            yield automation
    
    @pytest.fixture
    def simple_workflow(self):
        """Create simple test workflow"""
        return {
            'name': 'Simple Test Workflow',
            'version': '1.0.0',
            'description': 'Basic workflow for testing',
            'tasks': [
                {
                    'id': 'start',
                    'name': 'Start Task',
                    'type': 'script',
                    'config': {
                        'script': "output = {'status': 'started', 'time': str(datetime.now())}"
                    }
                },
                {
                    'id': 'process',
                    'name': 'Process Task',
                    'type': 'script',
                    'config': {
                        'script': "output = {'processed': True, 'count': 42}"
                    },
                    'dependencies': ['start']
                },
                {
                    'id': 'complete',
                    'name': 'Complete Task',
                    'type': 'script',
                    'config': {
                        'script': "output = {'final': 'done'}"
                    },
                    'dependencies': ['process']
                }
            ]
        }
    
    @pytest.fixture
    def complex_workflow(self):
        """Create complex workflow with branching and parallel tasks"""
        return {
            'name': 'Complex Test Workflow',
            'version': '1.0.0',
            'variables': {
                'threshold': 50,
                'mode': 'test'
            },
            'tasks': [
                {
                    'id': 'init',
                    'name': 'Initialize',
                    'type': 'script',
                    'config': {
                        'script': "output = {'value': 75}"
                    }
                },
                {
                    'id': 'check',
                    'name': 'Check Threshold',
                    'type': 'condition',
                    'config': {
                        'condition': "results['init']['value'] > variables['threshold']",
                        'if_true': {'branch': 'high'},
                        'if_false': {'branch': 'low'}
                    },
                    'dependencies': ['init']
                },
                {
                    'id': 'high_path',
                    'name': 'High Value Path',
                    'type': 'script',
                    'config': {
                        'script': "output = {'path': 'high', 'result': results['init']['value'] * 2}"
                    },
                    'dependencies': ['check'],
                    'conditions': [
                        {
                            'type': 'expression',
                            'expression': "tasks['check'].output['branch'] == 'high'"
                        }
                    ]
                },
                {
                    'id': 'low_path',
                    'name': 'Low Value Path',
                    'type': 'script',
                    'config': {
                        'script': "output = {'path': 'low', 'result': results['init']['value'] / 2}"
                    },
                    'dependencies': ['check'],
                    'conditions': [
                        {
                            'type': 'expression',
                            'expression': "tasks['check'].output['branch'] == 'low'"
                        }
                    ]
                },
                {
                    'id': 'parallel1',
                    'name': 'Parallel Task 1',
                    'type': 'wait',
                    'config': {
                        'duration': 0.1
                    },
                    'dependencies': ['check'],
                    'parallel': True
                },
                {
                    'id': 'parallel2',
                    'name': 'Parallel Task 2',
                    'type': 'wait',
                    'config': {
                        'duration': 0.1
                    },
                    'dependencies': ['check'],
                    'parallel': True
                }
            ]
        }
    
    @pytest.mark.asyncio
    async def test_simple_workflow_execution(self, automation, simple_workflow):
        """Test execution of simple sequential workflow"""
        # Save workflow
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(simple_workflow, f)
            workflow_file = f.name
        
        try:
            # Load and execute
            workflow_id = await automation.load_workflow(workflow_file)
            result = await automation.execute_workflow(workflow_id)
            
            # Verify execution
            assert result['status'] == 'completed'
            assert result['completed_tasks'] == 3
            assert 'start' in result['results']
            assert 'process' in result['results']
            assert 'complete' in result['results']
            
            # Check task outputs
            assert result['results']['process']['processed'] is True
            assert result['results']['process']['count'] == 42
            assert result['results']['complete']['final'] == 'done'
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_workflow_with_dependencies(self, automation, simple_workflow):
        """Test workflow dependency execution order"""
        # Track execution order
        execution_order = []
        
        class OrderTrackingTask(ScriptTask):
            async def execute(self, context):
                task_id = context['task'].id
                execution_order.append(task_id)
                return await super().execute(context)
        
        # Register custom task
        automation.register_task('script', OrderTrackingTask)
        
        # Save and execute workflow
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(simple_workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            await automation.execute_workflow(workflow_id)
            
            # Verify execution order
            assert execution_order == ['start', 'process', 'complete']
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_conditional_workflow_execution(self, automation, complex_workflow):
        """Test workflow with conditional branching"""
        # Save workflow
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(complex_workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            result = await automation.execute_workflow(workflow_id)
            
            # Verify high path was taken (value=75 > threshold=50)
            assert 'high_path' in result['results']
            assert result['results']['high_path']['path'] == 'high'
            assert result['results']['high_path']['result'] == 150  # 75 * 2
            
            # Verify low path was skipped
            assert 'low_path' not in result['results']
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_parallel_task_execution(self, automation, complex_workflow):
        """Test parallel task execution"""
        # Save workflow
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(complex_workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            
            # Track execution timing
            start_time = datetime.now()
            result = await automation.execute_workflow(workflow_id)
            duration = (datetime.now() - start_time).total_seconds()
            
            # Verify both parallel tasks completed
            assert 'parallel1' in result['results']
            assert 'parallel2' in result['results']
            
            # Verify they ran in parallel (total time < sum of individual times)
            # Each wait task is 0.1s, if sequential would be 0.2s minimum
            assert duration < 0.2
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_workflow_with_variables(self, automation):
        """Test workflow variable handling"""
        workflow = {
            'name': 'Variable Test',
            'variables': {
                'base_value': 10,
                'multiplier': 3
            },
            'tasks': [
                {
                    'id': 'calculate',
                    'name': 'Calculate',
                    'type': 'script',
                    'config': {
                        'script': """
result = variables['base_value'] * variables['multiplier']
output = {'result': result, 'variables': {'calculated': result}}
"""
                    }
                },
                {
                    'id': 'verify',
                    'name': 'Verify',
                    'type': 'script',
                    'config': {
                        'script': "output = {'verified': variables['calculated'] == 30}"
                    },
                    'dependencies': ['calculate']
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            
            # Execute with override variables
            result = await automation.execute_workflow(workflow_id, {'multiplier': 5})
            
            # Verify calculations with overridden variable
            assert result['results']['calculate']['result'] == 50  # 10 * 5
            assert result['results']['verify']['verified'] is False  # Expected 30, got 50
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_workflow_error_handling(self, automation):
        """Test workflow error handling"""
        workflow = {
            'name': 'Error Test',
            'tasks': [
                {
                    'id': 'failing_task',
                    'name': 'Failing Task',
                    'type': 'script',
                    'config': {
                        'script': "raise ValueError('Test error')"
                    }
                },
                {
                    'id': 'dependent_task',
                    'name': 'Dependent Task',
                    'type': 'script',
                    'config': {
                        'script': "output = {'should_not_run': True}"
                    },
                    'dependencies': ['failing_task']
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
            
            # Verify failing task recorded
            assert 'failing_task' in result['results']
            
            # Verify dependent task didn't run
            assert 'dependent_task' not in result['results']
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_workflow_retry_logic(self, automation):
        """Test task retry functionality"""
        retry_count = 0
        
        class RetryTestTask(BaseTask):
            async def execute(self, context):
                nonlocal retry_count
                retry_count += 1
                if retry_count < 3:
                    raise ValueError(f"Attempt {retry_count} failed")
                return {'success': True, 'attempts': retry_count}
            
            def validate_config(self, config):
                return True
        
        automation.register_task('retry_test', RetryTestTask)
        
        workflow = {
            'name': 'Retry Test',
            'tasks': [
                {
                    'id': 'retry_task',
                    'name': 'Retry Task',
                    'type': 'retry_test',
                    'config': {},
                    'retry': {
                        'max_retries': 3,
                        'delay': 0.1
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
            
            # Verify task succeeded after retries
            assert result['status'] == 'completed'
            assert result['results']['retry_task']['success'] is True
            assert result['results']['retry_task']['attempts'] == 3
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_workflow_timeout(self, automation):
        """Test task timeout handling"""
        workflow = {
            'name': 'Timeout Test',
            'tasks': [
                {
                    'id': 'slow_task',
                    'name': 'Slow Task',
                    'type': 'wait',
                    'config': {
                        'duration': 2  # 2 second wait
                    },
                    'timeout': 1  # 1 second timeout
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            result = await automation.execute_workflow(workflow_id)
            
            # Verify workflow failed due to timeout
            assert result['status'] == 'failed'
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_custom_task_registration(self, automation):
        """Test custom task type registration"""
        class CustomTask(BaseTask):
            async def execute(self, context):
                config = context['task'].config
                return {
                    'custom': True,
                    'input': config.get('input', ''),
                    'upper': config.get('input', '').upper()
                }
            
            def validate_config(self, config):
                return 'input' in config
        
        # Register custom task
        automation.register_task('custom', CustomTask)
        
        workflow = {
            'name': 'Custom Task Test',
            'tasks': [
                {
                    'id': 'custom_task',
                    'name': 'Custom Task',
                    'type': 'custom',
                    'config': {
                        'input': 'hello world'
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
            
            # Verify custom task executed
            assert result['status'] == 'completed'
            assert result['results']['custom_task']['custom'] is True
            assert result['results']['custom_task']['input'] == 'hello world'
            assert result['results']['custom_task']['upper'] == 'HELLO WORLD'
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])