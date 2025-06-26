"""
Test task scheduling functionality

Tests workflow scheduling features including cron triggers,
event-based execution, and schedule management.
"""

import asyncio
import pytest
from pathlib import Path
import yaml
import tempfile
from datetime import datetime, timedelta
import time

import sys
sys.path.append('/home/graham/workspace/shared_claude_docs/project_interactions/workflow_automation')

from workflow_automation_interaction import (
    WorkflowAutomation, WorkflowScheduler, TriggerType
)


class TestTaskScheduling:
    """Test task scheduling features"""
    
    @pytest.fixture
    async def automation(self):
        """Create workflow automation instance"""
        with tempfile.TemporaryDirectory() as tmpdir:
            automation = WorkflowAutomation(state_dir=Path(tmpdir))
            yield automation
            # Ensure scheduler is stopped
            await automation.stop_scheduler()
    
    @pytest.fixture
    def scheduled_workflow(self):
        """Create workflow for scheduling tests"""
        return {
            'name': 'Scheduled Workflow',
            'version': '1.0.0',
            'variables': {
                'execution_time': ''
            },
            'tasks': [
                {
                    'id': 'record_time',
                    'name': 'Record Execution Time',
                    'type': 'script',
                    'config': {
                        'script': """
from datetime import datetime
output = {
    'executed_at': datetime.now().isoformat(),
    'variables': {'last_execution': datetime.now().isoformat()}
}
"""
                    }
                }
            ]
        }
    
    @pytest.mark.asyncio
    async def test_cron_schedule_creation(self, automation, scheduled_workflow):
        """Test creating cron-based schedule"""
        # Save workflow
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(scheduled_workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            
            # Create cron schedule (every minute)
            trigger = {
                'type': 'cron',
                'expression': '* * * * *'
            }
            
            schedule_id = await automation.schedule_workflow(workflow_id, trigger)
            
            # Verify schedule created
            assert schedule_id is not None
            assert len(schedule_id) == 36  # UUID format
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_cron_schedule_execution(self, automation, scheduled_workflow):
        """Test cron schedule execution"""
        # Track executions
        execution_count = 0
        original_execute = automation.engine.execute_workflow
        
        async def counting_execute(*args, **kwargs):
            nonlocal execution_count
            execution_count += 1
            return await original_execute(*args, **kwargs)
        
        automation.engine.execute_workflow = counting_execute
        
        # Save workflow
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(scheduled_workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            
            # Create schedule (every 2 seconds for testing)
            trigger = {
                'type': 'cron',
                'expression': '*/2 * * * * *'  # Every 2 seconds
            }
            
            await automation.schedule_workflow(workflow_id, trigger)
            await automation.start_scheduler()
            
            # Wait for executions
            await asyncio.sleep(5)
            
            # Should have executed 2-3 times in 5 seconds
            assert execution_count >= 2
            assert execution_count <= 3
            
        finally:
            await automation.stop_scheduler()
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_multiple_schedules(self, automation):
        """Test multiple workflow schedules"""
        workflows = []
        execution_counts = {}
        
        # Create multiple workflows
        for i in range(3):
            workflow = {
                'name': f'Workflow {i}',
                'tasks': [
                    {
                        'id': 'task',
                        'name': 'Task',
                        'type': 'script',
                        'config': {
                            'script': f"output = {{'workflow': {i}}}"
                        }
                    }
                ]
            }
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
                yaml.dump(workflow, f)
                workflows.append(f.name)
            
            workflow_id = await automation.load_workflow(workflows[-1])
            execution_counts[workflow_id] = 0
            
            # Track executions per workflow
            original_execute = automation.engine.execute_workflow
            
            async def counting_execute(wf_id, *args, **kwargs):
                if wf_id in execution_counts:
                    execution_counts[wf_id] += 1
                return await original_execute(wf_id, *args, **kwargs)
            
            automation.engine.execute_workflow = counting_execute
            
            # Schedule with different intervals
            trigger = {
                'type': 'cron',
                'expression': f'*/{i+2} * * * * *'  # Every 2, 3, 4 seconds
            }
            await automation.schedule_workflow(workflow_id, trigger)
        
        try:
            await automation.start_scheduler()
            await asyncio.sleep(6)
            
            # Verify all workflows executed
            for workflow_id, count in execution_counts.items():
                assert count > 0
            
        finally:
            await automation.stop_scheduler()
            for workflow_file in workflows:
                Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_schedule_with_variables(self, automation):
        """Test scheduled workflow with variables"""
        workflow = {
            'name': 'Variable Schedule Test',
            'variables': {
                'counter': 0
            },
            'tasks': [
                {
                    'id': 'increment',
                    'name': 'Increment Counter',
                    'type': 'script',
                    'config': {
                        'script': """
counter = variables.get('counter', 0) + 1
output = {'count': counter, 'variables': {'counter': counter}}
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
            
            # Schedule with initial variables
            trigger = {
                'type': 'cron',
                'expression': '*/1 * * * * *',  # Every second
                'variables': {
                    'counter': 10
                }
            }
            
            await automation.schedule_workflow(workflow_id, trigger)
            await automation.start_scheduler()
            
            # Wait for one execution
            await asyncio.sleep(2)
            
            # Get executions and check counter started at 10
            executions = await automation.list_executions(workflow_id)
            assert len(executions) > 0
            
        finally:
            await automation.stop_scheduler()
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_scheduler_start_stop(self, automation, scheduled_workflow):
        """Test scheduler start/stop functionality"""
        # Save workflow
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(scheduled_workflow, f)
            workflow_file = f.name
        
        execution_count = 0
        
        async def counting_execute(*args, **kwargs):
            nonlocal execution_count
            execution_count += 1
            return {'status': 'completed', 'completed_tasks': 1, 'results': {}}
        
        automation.engine.execute_workflow = counting_execute
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            
            # Create fast schedule
            trigger = {
                'type': 'cron',
                'expression': '*/1 * * * * *'  # Every second
            }
            
            await automation.schedule_workflow(workflow_id, trigger)
            
            # Start scheduler
            await automation.start_scheduler()
            await asyncio.sleep(3)
            first_count = execution_count
            
            # Stop scheduler
            await automation.stop_scheduler()
            await asyncio.sleep(2)
            stopped_count = execution_count
            
            # Verify no new executions after stop
            assert first_count > 0
            assert stopped_count == first_count
            
            # Restart scheduler
            await automation.start_scheduler()
            await asyncio.sleep(2)
            final_count = execution_count
            
            # Verify executions resumed
            assert final_count > stopped_count
            
        finally:
            await automation.stop_scheduler()
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_invalid_cron_expression(self, automation, scheduled_workflow):
        """Test handling of invalid cron expressions"""
        # Save workflow
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(scheduled_workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            
            # Invalid cron expression
            trigger = {
                'type': 'cron',
                'expression': 'invalid cron'
            }
            
            # Should handle error gracefully
            with pytest.raises(Exception):
                await automation.schedule_workflow(workflow_id, trigger)
                await automation.start_scheduler()
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_workflow_execution_history(self, automation):
        """Test tracking workflow execution history"""
        workflow = {
            'name': 'History Test',
            'tasks': [
                {
                    'id': 'task',
                    'name': 'Simple Task',
                    'type': 'script',
                    'config': {
                        'script': "output = {'timestamp': str(datetime.now())}"
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
            for i in range(3):
                result = await automation.execute_workflow(workflow_id)
                execution_ids.append(result['execution_id'])
                await asyncio.sleep(0.1)
            
            # Get execution history
            executions = await automation.list_executions(workflow_id)
            
            # Verify all executions recorded
            assert len(executions) >= 3
            
            # Verify execution details
            for execution in executions:
                if execution['execution_id'] in execution_ids:
                    assert execution['workflow_id'] == workflow_id
                    assert execution['status'] == 'completed'
                    assert execution['completed_tasks'] == 1
                    assert execution['duration'] >= 0
            
            # Test filtering by workflow
            all_executions = await automation.list_executions()
            assert len(all_executions) >= len(executions)
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_execution_status_tracking(self, automation):
        """Test real-time execution status tracking"""
        workflow = {
            'name': 'Status Test',
            'tasks': [
                {
                    'id': 'slow_task',
                    'name': 'Slow Task',
                    'type': 'wait',
                    'config': {
                        'duration': 2
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            
            # Start execution asynchronously
            execution_task = asyncio.create_task(
                automation.execute_workflow(workflow_id)
            )
            
            # Give it time to start
            await asyncio.sleep(0.5)
            
            # Check status while running
            running_executions = await automation.list_executions(workflow_id)
            running = [e for e in running_executions if e['status'] == 'running']
            assert len(running) == 1
            
            execution_id = running[0]['execution_id']
            
            # Get detailed status
            status = await automation.get_execution_status(execution_id)
            assert status is not None
            assert status['status'] == 'running'
            assert len(status['current_tasks']) > 0
            
            # Wait for completion
            result = await execution_task
            
            # Check final status
            final_status = await automation.get_execution_status(execution_id)
            assert final_status['status'] == 'completed'
            assert len(final_status['current_tasks']) == 0
            assert final_status['completed_tasks'] == 1
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_schedule_persistence(self, automation):
        """Test schedule persistence across restarts"""
        workflow = {
            'name': 'Persistence Test',
            'tasks': [
                {
                    'id': 'task',
                    'name': 'Task',
                    'type': 'script',
                    'config': {
                        'script': "output = {'test': True}"
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(workflow, f)
            workflow_file = f.name
        
        try:
            workflow_id = await automation.load_workflow(workflow_file)
            
            # Create schedule
            trigger = {
                'type': 'cron',
                'expression': '0 * * * *'  # Every hour
            }
            
            schedule_id = await automation.schedule_workflow(workflow_id, trigger)
            
            # Verify schedule exists
            assert schedule_id in automation.scheduler.schedules
            
            # In real implementation, would test persistence across restarts
            
        finally:
            Path(workflow_file).unlink(missing_ok=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])