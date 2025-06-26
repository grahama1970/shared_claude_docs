#!/usr/bin/env python3
"""
Module: test_level_3_interactions.py
Description: Level 3 interaction tests - Multi-agent collaboration

External Dependencies:
- pytest: Test framework
- interaction_framework: Granger interaction test framework

Sample Input:
>>> Multi-agent collaborative workflows with hub communication

Expected Output:
>>> Verification of Level 3 interaction patterns

Example Usage:
>>> pytest test_level_3_interactions.py -v
"""

import pytest
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
from interaction_framework import (
    InteractionRunner,
    InteractionResult,
    BaseInteraction,
    InteractionLevel,
    OptimizableInteraction
)


class Agent:
    """Represents an autonomous agent in the Granger ecosystem."""
    
    def __init__(self, name: str, specialization: str):
        self.name = name
        self.specialization = specialization
        self.knowledge_base = {}
        self.message_queue = []
    
    def receive_message(self, message: Dict[str, Any]):
        """Receive message from hub."""
        self.message_queue.append(message)
    
    def process_messages(self) -> List[Dict[str, Any]]:
        """Process queued messages and return responses."""
        responses = []
        for msg in self.message_queue:
            response = {
                "from": self.name,
                "to": msg.get("from", "hub"),
                "response_to": msg.get("id"),
                "content": f"Processed by {self.name}: {msg.get('content', '')}"
            }
            responses.append(response)
        self.message_queue.clear()
        return responses


class GrangerHub:
    """Simulates the Granger Hub for multi-agent communication."""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.message_history = []
        self.topics: Dict[str, List[str]] = {}  # topic -> [agent_names]
    
    def register_agent(self, agent: Agent):
        """Register an agent with the hub."""
        self.agents[agent.name] = agent
    
    def publish(self, message: Dict[str, Any]):
        """Publish message to relevant agents."""
        self.message_history.append(message)
        
        # Route to specific agent or broadcast
        if "to" in message:
            if message["to"] in self.agents:
                self.agents[message["to"]].receive_message(message)
        elif "topic" in message:
            # Publish to all agents subscribed to topic
            topic = message["topic"]
            for agent_name in self.topics.get(topic, []):
                self.agents[agent_name].receive_message(message)
        else:
            # Broadcast to all agents
            for agent in self.agents.values():
                agent.receive_message(message)
    
    def subscribe(self, agent_name: str, topic: str):
        """Subscribe agent to topic."""
        if topic not in self.topics:
            self.topics[topic] = []
        if agent_name not in self.topics[topic]:
            self.topics[topic].append(agent_name)


class MultiAgentCollaborationInteraction(BaseInteraction):
    """Multi-agent collaboration through hub communication."""
    
    def __init__(self):
        super().__init__(
            name="multi_agent_collaboration",
            description="Multiple agents collaborating through hub",
            level=InteractionLevel.LEVEL_3
        )
        self.hub = GrangerHub()
    
    def execute(self, **params) -> InteractionResult:
        """Execute multi-agent collaboration."""
        start_time = datetime.now()
        
        try:
            # Create specialized agents
            research_agent = Agent("researcher", "research")
            security_agent = Agent("security_analyst", "security")
            ml_agent = Agent("ml_engineer", "machine_learning")
            coordinator_agent = Agent("coordinator", "orchestration")
            
            # Register agents with hub
            for agent in [research_agent, security_agent, ml_agent, coordinator_agent]:
                self.hub.register_agent(agent)
            
            # Set up topic subscriptions
            self.hub.subscribe("researcher", "new_vulnerabilities")
            self.hub.subscribe("security_analyst", "research_findings")
            self.hub.subscribe("ml_engineer", "optimization_requests")
            self.hub.subscribe("coordinator", "all")
            
            task = params.get("task", "analyze_new_threat")
            collaboration_log = []
            
            # Step 1: Coordinator initiates task
            self.hub.publish({
                "id": "task_001",
                "from": "coordinator",
                "topic": "all",
                "content": f"New task: {task}",
                "timestamp": datetime.now().isoformat()
            })
            collaboration_log.append("Coordinator initiated task")
            
            # Step 2: Agents process and respond
            all_responses = []
            for agent_name, agent in self.hub.agents.items():
                responses = agent.process_messages()
                all_responses.extend(responses)
                for response in responses:
                    self.hub.publish(response)
            
            # Step 3: Specialized workflows based on task
            if "threat" in task or "security" in task:
                # Security-focused collaboration
                self._execute_security_collaboration(collaboration_log)
            elif "research" in task:
                # Research-focused collaboration
                self._execute_research_collaboration(collaboration_log)
            else:
                # General collaboration
                self._execute_general_collaboration(collaboration_log)
            
            # Step 4: Agents share findings
            findings = self._collect_agent_findings()
            
            # Step 5: ML agent optimizes based on collaboration
            optimization = self._call_module("rl_commons", {
                "action": "optimize_collaboration",
                "agents": list(self.hub.agents.keys()),
                "message_patterns": self.hub.message_history,
                "task_type": task
            })
            
            return InteractionResult(
                interaction_name=self.name,
                level=self.level,
                success=True,
                duration=(datetime.now() - start_time).total_seconds(),
                input_data=params,
                output_data={
                    "agents": list(self.hub.agents.keys()),
                    "messages_exchanged": len(self.hub.message_history),
                    "collaboration_log": collaboration_log,
                    "findings": findings,
                    "optimization": optimization
                }
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name=self.name,
                level=self.level,
                success=False,
                duration=(datetime.now() - start_time).total_seconds(),
                input_data=params,
                error=str(e)
            )
    
    def _execute_security_collaboration(self, log: List[str]):
        """Execute security-focused agent collaboration."""
        # Security agent leads
        self.hub.publish({
            "from": "security_analyst",
            "topic": "security_scan",
            "content": "Initiating security scan",
            "module_call": "sparta.scan"
        })
        log.append("Security agent initiated scan")
        
        # Research agent supports
        self.hub.publish({
            "from": "researcher",
            "topic": "vulnerability_research",
            "content": "Searching for known vulnerabilities",
            "module_call": "arxiv.search"
        })
        log.append("Research agent searching for vulnerabilities")
        
        # ML agent optimizes
        self.hub.publish({
            "from": "ml_engineer",
            "topic": "optimization",
            "content": "Optimizing scan parameters",
            "module_call": "rl_commons.optimize"
        })
        log.append("ML agent optimizing scan")
    
    def _execute_research_collaboration(self, log: List[str]):
        """Execute research-focused agent collaboration."""
        # Research agent leads
        self.hub.publish({
            "from": "researcher",
            "topic": "research_papers",
            "content": "Searching academic papers",
            "module_call": "arxiv.search"
        })
        log.append("Research agent searching papers")
        
        # ML agent helps with relevance
        self.hub.publish({
            "from": "ml_engineer",
            "topic": "relevance_scoring",
            "content": "Scoring paper relevance",
            "module_call": "llm_call.analyze"
        })
        log.append("ML agent scoring relevance")
    
    def _execute_general_collaboration(self, log: List[str]):
        """Execute general collaboration pattern."""
        # Coordinator orchestrates
        self.hub.publish({
            "from": "coordinator",
            "topic": "task_distribution",
            "content": "Distributing subtasks to agents"
        })
        log.append("Coordinator distributed tasks")
    
    def _collect_agent_findings(self) -> Dict[str, Any]:
        """Collect findings from all agents."""
        findings = {}
        for agent_name, agent in self.hub.agents.items():
            findings[agent_name] = {
                "knowledge": agent.knowledge_base,
                "messages_processed": len(agent.message_queue)
            }
        return findings


class HierarchicalTeamInteraction(BaseInteraction):
    """Hierarchical team structure with supervisor and worker agents."""
    
    def __init__(self):
        super().__init__(
            name="hierarchical_team",
            description="Hierarchical multi-agent team collaboration",
            level=InteractionLevel.LEVEL_3
        )
    
    def execute(self, **params) -> InteractionResult:
        """Execute hierarchical team collaboration."""
        start_time = datetime.now()
        
        try:
            # Create team hierarchy
            supervisor = Agent("supervisor", "management")
            workers = [
                Agent("worker_1", "data_processing"),
                Agent("worker_2", "analysis"),
                Agent("worker_3", "validation")
            ]
            
            hub = GrangerHub()
            hub.register_agent(supervisor)
            for worker in workers:
                hub.register_agent(worker)
            
            # Supervisor delegates tasks
            task = params.get("task", "process_dataset")
            subtasks = self._decompose_task(task)
            
            delegation_log = []
            for i, (worker, subtask) in enumerate(zip(workers, subtasks)):
                hub.publish({
                    "from": "supervisor",
                    "to": worker.name,
                    "task_id": f"subtask_{i}",
                    "content": subtask,
                    "deadline": "30_seconds"
                })
                delegation_log.append(f"Delegated {subtask} to {worker.name}")
            
            # Workers process in parallel (simulated)
            worker_results = []
            for worker in workers:
                # Worker processes messages
                responses = worker.process_messages()
                # Simulate work
                result = self._call_module("llm_call", {
                    "action": "process",
                    "worker": worker.name,
                    "task": responses[0]["content"] if responses else ""
                })
                worker_results.append(result)
                
                # Report back to supervisor
                hub.publish({
                    "from": worker.name,
                    "to": "supervisor",
                    "content": f"Completed: {result}"
                })
            
            # Supervisor aggregates results
            supervisor_responses = supervisor.process_messages()
            final_result = {
                "task": task,
                "subtasks": subtasks,
                "worker_results": worker_results,
                "delegation_log": delegation_log,
                "hierarchy": {
                    "supervisor": "supervisor",
                    "workers": [w.name for w in workers]
                }
            }
            
            return InteractionResult(
                interaction_name=self.name,
                level=self.level,
                success=True,
                duration=(datetime.now() - start_time).total_seconds(),
                input_data=params,
                output_data=final_result
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name=self.name,
                level=self.level,
                success=False,
                duration=(datetime.now() - start_time).total_seconds(),
                input_data=params,
                error=str(e)
            )
    
    def _decompose_task(self, task: str) -> List[str]:
        """Decompose task into subtasks."""
        # Simple decomposition
        return [
            f"Preprocess data for {task}",
            f"Analyze patterns in {task}",
            f"Validate results for {task}"
        ]


class SwarmIntelligenceInteraction(BaseInteraction):
    """Swarm intelligence with emergent behavior from many simple agents."""
    
    def __init__(self):
        super().__init__(
            name="swarm_intelligence",
            description="Swarm of simple agents exhibiting emergent behavior",
            level=InteractionLevel.LEVEL_3
        )
    
    def execute(self, **params) -> InteractionResult:
        """Execute swarm intelligence pattern."""
        start_time = datetime.now()
        
        try:
            # Create swarm of simple agents
            swarm_size = params.get("swarm_size", 10)
            swarm = [Agent(f"drone_{i}", "scout") for i in range(swarm_size)]
            
            hub = GrangerHub()
            for drone in swarm:
                hub.register_agent(drone)
            
            target = params.get("target", "find_optimal_solution")
            iterations = params.get("iterations", 3)
            
            swarm_log = []
            best_solution = None
            
            for iteration in range(iterations):
                # Each drone explores independently
                explorations = []
                for drone in swarm:
                    exploration = self._call_module("llm_call", {
                        "action": "explore",
                        "agent": drone.name,
                        "target": target,
                        "iteration": iteration
                    })
                    explorations.append(exploration)
                    
                    # Share findings with swarm
                    hub.publish({
                        "from": drone.name,
                        "topic": "exploration_results",
                        "content": exploration,
                        "quality": exploration.get("quality", 0)
                    })
                
                # Swarm converges on best solutions
                for drone in swarm:
                    messages = drone.process_messages()
                    # Update drone's direction based on swarm intelligence
                    best_from_swarm = max(messages, 
                                         key=lambda m: m.get("quality", 0),
                                         default=None)
                    if best_from_swarm:
                        drone.knowledge_base["best_direction"] = best_from_swarm
                
                # Track best solution
                iteration_best = max(explorations, 
                                   key=lambda e: e.get("quality", 0))
                if not best_solution or iteration_best.get("quality", 0) > best_solution.get("quality", 0):
                    best_solution = iteration_best
                
                swarm_log.append(f"Iteration {iteration}: Best quality = {iteration_best.get('quality', 0)}")
            
            return InteractionResult(
                interaction_name=self.name,
                level=self.level,
                success=True,
                duration=(datetime.now() - start_time).total_seconds(),
                input_data=params,
                output_data={
                    "swarm_size": swarm_size,
                    "iterations": iterations,
                    "best_solution": best_solution,
                    "swarm_log": swarm_log,
                    "convergence": True
                }
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name=self.name,
                level=self.level,
                success=False,
                duration=(datetime.now() - start_time).total_seconds(),
                input_data=params,
                error=str(e)
            )


class TestLevel3Interactions:
    """Test suite for Level 3 multi-agent interactions."""
    
    @pytest.fixture
    def runner(self):
        """Create interaction runner."""
        return InteractionRunner("Granger Level 3 Tests")
    
    def test_multi_agent_collaboration(self, runner):
        """Test basic multi-agent collaboration."""
        interaction = MultiAgentCollaborationInteraction()
        result = runner.run_interaction(
            interaction,
            task="analyze_security_threat"
        )
        assert result.success
        assert result.output_data["messages_exchanged"] > 0
        assert len(result.output_data["agents"]) >= 4
    
    def test_hierarchical_team(self, runner):
        """Test hierarchical team structure."""
        interaction = HierarchicalTeamInteraction()
        result = runner.run_interaction(
            interaction,
            task="process_large_dataset"
        )
        assert result.success
        assert "hierarchy" in result.output_data
        assert len(result.output_data["worker_results"]) == 3
    
    def test_swarm_intelligence(self, runner):
        """Test swarm intelligence pattern."""
        interaction = SwarmIntelligenceInteraction()
        result = runner.run_interaction(
            interaction,
            target="optimize_resource_allocation",
            swarm_size=5,
            iterations=2
        )
        assert result.success
        assert result.output_data["convergence"]
        assert "best_solution" in result.output_data
    
    def test_agent_specialization(self, runner):
        """Test that agents act according to specialization."""
        interaction = MultiAgentCollaborationInteraction()
        
        # Test security-focused task
        result1 = runner.run_interaction(
            interaction,
            task="security_audit"
        )
        
        # Test research-focused task
        result2 = runner.run_interaction(
            interaction,
            task="research_papers"
        )
        
        assert result1.success and result2.success
        # Different tasks should trigger different collaboration patterns
        assert result1.output_data["collaboration_log"] != result2.output_data["collaboration_log"]
    
    def test_hub_communication(self, runner):
        """Test hub-based communication patterns."""
        interaction = MultiAgentCollaborationInteraction()
        result = runner.run_interaction(
            interaction,
            task="coordinate_response"
        )
        
        assert result.success
        # Verify hub facilitated communication
        assert result.output_data["messages_exchanged"] >= len(result.output_data["agents"])
    
    def test_emergent_behavior(self, runner):
        """Test emergent behavior in swarm."""
        interaction = SwarmIntelligenceInteraction()
        
        # Run with different swarm sizes
        small_swarm = runner.run_interaction(
            interaction,
            swarm_size=3,
            iterations=2
        )
        
        large_swarm = runner.run_interaction(
            interaction,
            swarm_size=10,
            iterations=2
        )
        
        assert small_swarm.success and large_swarm.success
        # Larger swarm should find better solutions
        assert large_swarm.output_data["best_solution"]["quality"] >= small_swarm.output_data["best_solution"]["quality"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])