#!/usr/bin/env python3
"""
Task Orchestrator for Complex Multi-Module Interactions
Coordinates tasks across multiple modules to achieve complex goals
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import aiohttp
import networkx as nx
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class TaskStep:
    """Represents a single step in a task"""
    id: str
    module: str
    capability: str
    input_data: Dict[str, Any]
    depends_on: List[str] = None
    timeout: int = 300
    retry_count: int = 3
    status: TaskStatus = TaskStatus.PENDING
    output_data: Dict[str, Any] = None
    error: str = None

@dataclass
class OrchestrationTask:
    """Represents a complete orchestration task"""
    id: str
    name: str
    description: str
    steps: List[TaskStep]
    created_at: str
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    metadata: Dict[str, Any] = None

class TaskOrchestrator:
    """Orchestrates complex tasks across multiple modules"""
    
    def __init__(self, registry_url: str = "http://localhost:8888"):
        self.registry_url = registry_url
        self.tasks: Dict[str, OrchestrationTask] = {}
        self.module_endpoints: Dict[str, str] = {}
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        await self._load_module_endpoints()
        return self
        
    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
        
    async def _load_module_endpoints(self):
        """Load module endpoints from registry"""
        async with self.session.get(f"{self.registry_url}/modules") as resp:
            data = await resp.json()
            for module in data.get("modules", []):
                # Prefer API endpoint, fallback to CLI
                if "api" in module.get("endpoints", {}):
                    self.module_endpoints[module["name"]] = module["endpoints"]["api"]
    
    def create_task(self, name: str, description: str) -> OrchestrationTask:
        """Create a new orchestration task"""
        task = OrchestrationTask(
            id=f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            name=name,
            description=description,
            steps=[],
            created_at=datetime.now().isoformat()
        )
        self.tasks[task.id] = task
        return task
    
    def add_step(self, task: OrchestrationTask, module: str, capability: str, 
                 input_data: Dict[str, Any], depends_on: List[str] = None) -> TaskStep:
        """Add a step to a task"""
        step = TaskStep(
            id=f"step_{len(task.steps) + 1}",
            module=module,
            capability=capability,
            input_data=input_data,
            depends_on=depends_on or []
        )
        task.steps.append(step)
        return step
    
    async def execute_task(self, task_id: str) -> Dict[str, Any]:
        """Execute an orchestration task"""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        task.status = TaskStatus.RUNNING
        
        # Build dependency graph
        graph = self._build_dependency_graph(task)
        
        # Execute steps in topological order
        try:
            execution_order = list(nx.topological_sort(graph))
            step_outputs = {}
            
            for step_id in execution_order:
                step = next(s for s in task.steps if s.id == step_id)
                
                # Resolve input data from previous steps
                resolved_input = await self._resolve_step_input(step, step_outputs)
                
                # Execute step
                step.status = TaskStatus.RUNNING
                try:
                    output = await self._execute_step(step, resolved_input)
                    step.output_data = output
                    step.status = TaskStatus.COMPLETED
                    step_outputs[step.id] = output
                except Exception as e:
                    step.status = TaskStatus.FAILED
                    step.error = str(e)
                    raise
            
            task.status = TaskStatus.COMPLETED
            task.result = self._aggregate_results(task, step_outputs)
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.result = {"error": str(e)}
        
        return task.result
    
    def _build_dependency_graph(self, task: OrchestrationTask) -> nx.DiGraph:
        """Build a dependency graph for the task"""
        graph = nx.DiGraph()
        
        # Add all steps as nodes
        for step in task.steps:
            graph.add_node(step.id)
        
        # Add dependency edges
        for step in task.steps:
            for dep in step.depends_on:
                graph.add_edge(dep, step.id)
        
        return graph
    
    async def _resolve_step_input(self, step: TaskStep, previous_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve input data for a step, including references to previous outputs"""
        resolved = {}
        
        for key, value in step.input_data.items():
            if isinstance(value, str) and value.startswith("$"):
                # Reference to previous step output
                ref_parts = value[1:].split(".")
                if ref_parts[0] in previous_outputs:
                    resolved[key] = self._get_nested_value(previous_outputs[ref_parts[0]], ref_parts[1:])
                else:
                    resolved[key] = value
            else:
                resolved[key] = value
        
        return resolved
    
    def _get_nested_value(self, data: Dict[str, Any], path: List[str]) -> Any:
        """Get a nested value from a dictionary using a path"""
        result = data
        for key in path:
            if isinstance(result, dict):
                result = result.get(key)
            else:
                return None
        return result
    
    async def _execute_step(self, step: TaskStep, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step"""
        endpoint = self.module_endpoints.get(step.module)
        if not endpoint:
            # Try to use claude-module-communicator as a fallback
            return await self._execute_via_communicator(step, input_data)
        
        # Direct API call
        url = f"{endpoint}/{step.capability}"
        
        for attempt in range(step.retry_count):
            try:
                async with self.session.post(
                    url, 
                    json=input_data,
                    timeout=aiohttp.ClientTimeout(total=step.timeout)
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        error_text = await resp.text()
                        if attempt < step.retry_count - 1:
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                            continue
                        raise Exception(f"API call failed: {error_text}")
            except asyncio.TimeoutError:
                if attempt < step.retry_count - 1:
                    continue
                raise
        
        raise Exception(f"Failed to execute step after {step.retry_count} attempts")
    
    async def _execute_via_communicator(self, step: TaskStep, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a step via the claude-module-communicator"""
        # This would integrate with the actual communicator
        # For now, return a mock response
        return {
            "status": "executed_via_communicator",
            "module": step.module,
            "capability": step.capability,
            "mock_output": True
        }
    
    def _aggregate_results(self, task: OrchestrationTask, step_outputs: Dict[str, Any]) -> Any:
        """Aggregate results from all steps"""
        return {
            "task_id": task.id,
            "task_name": task.name,
            "status": task.status.value,
            "steps_completed": len([s for s in task.steps if s.status == TaskStatus.COMPLETED]),
            "total_steps": len(task.steps),
            "outputs": step_outputs,
            "final_output": step_outputs.get(task.steps[-1].id) if task.steps else None
        }

class ConversationalOrchestrator(TaskOrchestrator):
    """Extended orchestrator that supports conversational interactions"""
    
    def __init__(self, registry_url: str = "http://localhost:8888"):
        super().__init__(registry_url)
        self.conversation_history: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
    
    async def converse(self, user_input: str) -> Dict[str, Any]:
        """Process conversational input and orchestrate appropriate actions"""
        # Add to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Analyze intent and required capabilities
        intent = await self._analyze_intent(user_input)
        
        # Plan task based on intent
        task_plan = await self._plan_task(intent)
        
        # Execute task
        if task_plan:
            result = await self.execute_task(task_plan.id)
            
            # Generate conversational response
            response = await self._generate_response(result, intent)
            
            self.conversation_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat(),
                "task_id": task_plan.id
            })
            
            return {
                "response": response,
                "task_id": task_plan.id,
                "result": result
            }
        else:
            response = "I understand you want to " + intent["description"] + ", but I need more information."
            self.conversation_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
            return {"response": response}
    
    async def _analyze_intent(self, user_input: str) -> Dict[str, Any]:
        """Analyze user intent from conversational input"""
        # This would use NLP in a real implementation
        # For now, use keyword matching
        
        intents = {
            "research": ["research", "paper", "arxiv", "study", "literature"],
            "analyze": ["analyze", "process", "extract", "understand"],
            "visualize": ["graph", "visualize", "show", "display", "chart"],
            "test": ["test", "validate", "check", "verify"],
            "screenshot": ["screenshot", "capture", "ui", "interface"]
        }
        
        detected_intents = []
        for intent_name, keywords in intents.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                detected_intents.append(intent_name)
        
        return {
            "primary_intent": detected_intents[0] if detected_intents else "unknown",
            "all_intents": detected_intents,
            "description": user_input,
            "entities": self._extract_entities(user_input)
        }
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text"""
        # Simplified entity extraction
        entities = {}
        
        # Extract URLs
        import re
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        if urls:
            entities["urls"] = urls
        
        # Extract file paths
        paths = re.findall(r'/[\w/.-]+', text)
        if paths:
            entities["paths"] = paths
        
        # Extract numbers
        numbers = re.findall(r'\b\d+\b', text)
        if numbers:
            entities["numbers"] = [int(n) for n in numbers]
        
        return entities
    
    async def _plan_task(self, intent: Dict[str, Any]) -> Optional[OrchestrationTask]:
        """Plan a task based on intent"""
        primary_intent = intent["primary_intent"]
        
        if primary_intent == "research":
            return await self._plan_research_task(intent)
        elif primary_intent == "analyze":
            return await self._plan_analysis_task(intent)
        elif primary_intent == "visualize":
            return await self._plan_visualization_task(intent)
        elif primary_intent == "test":
            return await self._plan_testing_task(intent)
        elif primary_intent == "screenshot":
            return await self._plan_screenshot_task(intent)
        else:
            return None
    
    async def _plan_research_task(self, intent: Dict[str, Any]) -> OrchestrationTask:
        """Plan a research task"""
        task = self.create_task(
            name="Research Pipeline",
            description=f"Research task based on: {intent['description']}"
        )
        
        # Step 1: Search papers on ArXiv
        self.add_step(
            task, 
            module="arxiv-mcp-server",
            capability="search_papers",
            input_data={
                "query": intent["description"],
                "max_results": 5
            }
        )
        
        # Step 2: Extract text from papers
        self.add_step(
            task,
            module="marker",
            capability="extract_text",
            input_data={
                "file_path": "$step_1.papers[0].pdf_url",  # Reference to previous step
                "format": "pdf"
            },
            depends_on=["step_1"]
        )
        
        # Step 3: Analyze content
        self.add_step(
            task,
            module="youtube_transcripts",  # Reusing its analyze capability
            capability="analyze_content",
            input_data={
                "transcript": "$step_2.text"
            },
            depends_on=["step_2"]
        )
        
        # Step 4: Create knowledge graph
        self.add_step(
            task,
            module="arangodb",
            capability="create_knowledge_graph",
            input_data={
                "nodes": "$step_3.topics",
                "edges": []  # Would be extracted from relationships
            },
            depends_on=["step_3"]
        )
        
        return task
    
    async def _plan_analysis_task(self, intent: Dict[str, Any]) -> OrchestrationTask:
        """Plan an analysis task"""
        task = self.create_task(
            name="Document Analysis",
            description=f"Analysis task: {intent['description']}"
        )
        
        # Add appropriate steps based on entities
        if "paths" in intent["entities"]:
            self.add_step(
                task,
                module="marker",
                capability="extract_text",
                input_data={
                    "file_path": intent["entities"]["paths"][0],
                    "format": "pdf"
                }
            )
        
        return task
    
    async def _plan_visualization_task(self, intent: Dict[str, Any]) -> OrchestrationTask:
        """Plan a visualization task"""
        task = self.create_task(
            name="Visualization Pipeline",
            description=f"Visualization: {intent['description']}"
        )
        
        # Visualization steps would go here
        return task
    
    async def _plan_testing_task(self, intent: Dict[str, Any]) -> OrchestrationTask:
        """Plan a testing task"""
        task = self.create_task(
            name="Testing Pipeline",
            description=f"Testing: {intent['description']}"
        )
        
        self.add_step(
            task,
            module="claude-test-reporter",
            capability="run_tests",
            input_data={
                "test_path": intent["entities"].get("paths", ["/tests"])[0],
                "coverage": True
            }
        )
        
        return task
    
    async def _plan_screenshot_task(self, intent: Dict[str, Any]) -> OrchestrationTask:
        """Plan a screenshot task"""
        task = self.create_task(
            name="UI Analysis Pipeline",
            description=f"Screenshot and analysis: {intent['description']}"
        )
        
        # Step 1: Capture screenshot
        self.add_step(
            task,
            module="mcp-screenshot",
            capability="capture_screenshot",
            input_data={
                "target": intent["entities"].get("urls", ["http://localhost:3000"])[0]
            }
        )
        
        # Step 2: Analyze UI
        self.add_step(
            task,
            module="mcp-screenshot",
            capability="analyze_ui",
            input_data={
                "image_path": "$step_1.image_path"
            },
            depends_on=["step_1"]
        )
        
        return task
    
    async def _generate_response(self, result: Dict[str, Any], intent: Dict[str, Any]) -> str:
        """Generate a conversational response from task results"""
        if result.get("status") == "completed":
            primary_intent = intent["primary_intent"]
            
            if primary_intent == "research":
                papers_found = len(result["outputs"].get("step_1", {}).get("papers", []))
                topics = result["outputs"].get("step_3", {}).get("topics", [])
                return f"I found {papers_found} relevant papers and identified these key topics: {', '.join(topics[:5])}. A knowledge graph has been created to visualize the relationships."
            
            elif primary_intent == "test":
                test_result = result["outputs"].get("step_1", {})
                return f"Test execution complete: {test_result.get('passed', 0)} passed, {test_result.get('failed', 0)} failed. Coverage: {test_result.get('coverage', 0):.1f}%"
            
            elif primary_intent == "screenshot":
                ui_analysis = result["outputs"].get("step_2", {})
                issues = ui_analysis.get("accessibility_issues", [])
                return f"Screenshot captured and analyzed. Found {len(ui_analysis.get('elements', []))} UI elements. {len(issues)} accessibility issues detected."
            
        return f"Task completed with status: {result.get('status')}"

# Example usage
async def main():
    """Example of using the orchestrator"""
    async with ConversationalOrchestrator() as orchestrator:
        # Example 1: Research pipeline
        response = await orchestrator.converse(
            "Research recent papers on transformer architectures and create a knowledge graph"
        )
        print("Research Response:", response["response"])
        
        # Example 2: UI Testing
        response = await orchestrator.converse(
            "Take a screenshot of http://localhost:3000 and analyze the UI for accessibility issues"
        )
        print("UI Analysis Response:", response["response"])
        
        # Example 3: Complex multi-step task
        task = orchestrator.create_task(
            name="Complete Analysis Pipeline",
            description="Extract, analyze, and visualize research data"
        )
        
        # Add custom steps
        orchestrator.add_step(
            task,
            module="arxiv-mcp-server",
            capability="search_papers",
            input_data={"query": "machine learning", "max_results": 10}
        )
        
        orchestrator.add_step(
            task,
            module="marker",
            capability="extract_text",
            input_data={"file_path": "$step_1.papers[0].pdf_url", "format": "pdf"},
            depends_on=["step_1"]
        )
        
        orchestrator.add_step(
            task,
            module="sparta",
            capability="analyze_performance",
            input_data={"model_path": "/models/latest"},
            depends_on=["step_2"]
        )
        
        result = await orchestrator.execute_task(task.id)
        print("Pipeline Result:", json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())