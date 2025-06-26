#!/usr/bin/env python3
"""
Module: test_level_2_interactions.py
Description: Level 2 interaction tests - Complex RL-optimized workflows

External Dependencies:
- pytest: Test framework
- interaction_framework: Granger interaction test framework

Sample Input:
>>> Complex multi-module workflows with RL optimization

Expected Output:
>>> Verification of Level 2 interaction patterns

Example Usage:
>>> pytest test_level_2_interactions.py -v
"""

import pytest
from typing import Dict, Any, List
from datetime import datetime
from interaction_framework import (
    InteractionRunner,
    InteractionResult,
    BaseInteraction,
    InteractionLevel,
    OptimizableInteraction
)


class ComplexWorkflowInteraction(OptimizableInteraction):
    """Complex workflow with RL optimization across multiple modules."""
    
    def __init__(self):
        super().__init__(
            name="complex_rl_workflow",
            description="Complex multi-module workflow with RL optimization",
            level=InteractionLevel.LEVEL_2
        )
    
    def get_action_space(self) -> Dict[str, Any]:
        """Define the action space for RL optimization."""
        return {
            "module_sequence": [
                ["arxiv", "marker", "arangodb"],
                ["sparta", "arxiv", "youtube", "arangodb"],
                ["youtube", "marker", "llm_call", "arangodb"],
                ["arxiv", "sparta", "marker", "arangodb"]
            ],
            "parallel_execution": [True, False],
            "batch_size": [1, 5, 10, 20],
            "retry_strategy": ["exponential", "linear", "none"],
            "cache_strategy": ["aggressive", "moderate", "minimal"]
        }
    
    def execute(self, **params) -> InteractionResult:
        """Execute complex workflow with RL optimization."""
        start_time = datetime.now()
        
        try:
            # Step 1: RL selects optimal configuration
            rl_config = self._call_module("rl_commons", {
                "action": "optimize_workflow",
                "task": params.get("task", "complex_analysis"),
                "constraints": params.get("constraints", {
                    "max_time": 300,
                    "accuracy_target": 0.95,
                    "resource_limit": "moderate"
                })
            })
            
            # Extract optimal parameters
            module_sequence = rl_config.get("module_sequence", ["arxiv", "marker", "arangodb"])
            parallel = rl_config.get("parallel_execution", False)
            batch_size = rl_config.get("batch_size", 5)
            
            # Step 2: Execute workflow based on RL decision
            results = []
            
            if parallel:
                # Simulate parallel execution
                for module in module_sequence:
                    result = self._call_module(module, {
                        "action": "process",
                        "data": params.get("input_data", {}),
                        "batch_size": batch_size
                    })
                    results.append(result)
            else:
                # Sequential execution with data passing
                current_data = params.get("input_data", {})
                for module in module_sequence:
                    result = self._call_module(module, {
                        "action": "process",
                        "input": current_data,
                        "batch_size": batch_size
                    })
                    current_data = result  # Pass output to next module
                    results.append(result)
            
            # Step 3: RL learns from execution
            reward = self._calculate_reward(results, start_time)
            self._call_module("rl_commons", {
                "action": "update_model",
                "workflow_result": results,
                "reward": reward,
                "execution_time": (datetime.now() - start_time).total_seconds()
            })
            
            return InteractionResult(
                interaction_name=self.name,
                level=self.level,
                success=True,
                duration=(datetime.now() - start_time).total_seconds(),
                input_data=params,
                output_data={
                    "rl_config": rl_config,
                    "results": results,
                    "reward": reward,
                    "optimization_applied": True
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
    
    def _calculate_reward(self, results: List[Dict], start_time: datetime) -> float:
        """Calculate reward for RL based on execution results."""
        # Simple reward calculation
        success_rate = sum(1 for r in results if r.get("success", False)) / len(results)
        time_penalty = min(1.0, (datetime.now() - start_time).total_seconds() / 300)
        return success_rate * (1 - time_penalty * 0.5)


class AdaptiveSecurityWorkflow(OptimizableInteraction):
    """Adaptive security analysis workflow that changes based on findings."""
    
    def __init__(self):
        super().__init__(
            name="adaptive_security_workflow",
            description="Security workflow that adapts based on threat level",
            level=InteractionLevel.LEVEL_2
        )
    
    def execute(self, **params) -> InteractionResult:
        """Execute adaptive security workflow."""
        start_time = datetime.now()
        
        try:
            # Initial security scan
            scan_result = self._call_module("sparta", {
                "action": "deep_scan",
                "target": params.get("target", "codebase"),
                "scan_type": "comprehensive"
            })
            
            threat_level = scan_result.get("threat_level", "low")
            workflow_path = []
            
            # Adapt workflow based on threat level
            if threat_level == "critical":
                # Critical path: immediate response
                workflow_path = ["emergency_response", "patch_search", "mitigation"]
                
                # Search for patches
                patches = self._call_module("arxiv", {
                    "action": "search",
                    "query": f"security patches {scan_result.get('vulnerabilities', [])}",
                    "urgent": True
                })
                
                # Find video tutorials
                tutorials = self._call_module("youtube", {
                    "action": "search",
                    "query": f"fix {scan_result.get('vulnerabilities', [])}",
                    "filter": "recent"
                })
                
                # Generate fix with LLM
                fix = self._call_module("llm_call", {
                    "action": "generate_fix",
                    "vulnerability": scan_result,
                    "patches": patches,
                    "model": "security_expert"
                })
                
                # Store everything
                storage = self._call_module("arangodb", {
                    "action": "store_critical",
                    "data": {
                        "scan": scan_result,
                        "patches": patches,
                        "tutorials": tutorials,
                        "fix": fix
                    },
                    "priority": "high"
                })
                
            elif threat_level == "high":
                # High threat: thorough analysis
                workflow_path = ["detailed_analysis", "research", "recommendations"]
                
                # Detailed analysis
                analysis = self._call_module("sparta", {
                    "action": "analyze_vulnerabilities",
                    "scan_data": scan_result
                })
                
                # Research solutions
                research = self._call_module("arxiv", {
                    "action": "research",
                    "topics": analysis.get("topics", [])
                })
                
                # Store findings
                storage = self._call_module("arangodb", {
                    "action": "store",
                    "data": {
                        "analysis": analysis,
                        "research": research
                    }
                })
                
            else:
                # Low threat: standard logging
                workflow_path = ["log_findings"]
                storage = self._call_module("arangodb", {
                    "action": "log",
                    "data": scan_result
                })
            
            # RL learns from this execution
            self._call_module("rl_commons", {
                "action": "learn_pattern",
                "threat_level": threat_level,
                "workflow": workflow_path,
                "success": True
            })
            
            return InteractionResult(
                interaction_name=self.name,
                level=self.level,
                success=True,
                duration=(datetime.now() - start_time).total_seconds(),
                input_data=params,
                output_data={
                    "threat_level": threat_level,
                    "workflow_path": workflow_path,
                    "adaptive_response": True
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


class ResearchPipelineOptimization(OptimizableInteraction):
    """Research pipeline that optimizes itself over time."""
    
    def __init__(self):
        super().__init__(
            name="research_pipeline_optimization",
            description="Self-optimizing research pipeline",
            level=InteractionLevel.LEVEL_2
        )
    
    def execute(self, **params) -> InteractionResult:
        """Execute self-optimizing research pipeline."""
        start_time = datetime.now()
        
        try:
            topic = params.get("topic", "quantum computing")
            
            # RL decides search strategy
            strategy = self._call_module("rl_commons", {
                "action": "select_strategy",
                "task": "research",
                "topic": topic,
                "past_performance": self.get_metrics()
            })
            
            results = {}
            
            # Execute based on strategy
            if strategy.get("start_with") == "youtube":
                # Video-first approach
                videos = self._call_module("youtube", {
                    "action": "find_lectures",
                    "topic": topic,
                    "quality": "high"
                })
                results["videos"] = videos
                
                # Extract paper references from videos
                papers = self._call_module("arxiv", {
                    "action": "search",
                    "references": videos.get("paper_mentions", [])
                })
                results["papers"] = papers
                
            else:
                # Paper-first approach
                papers = self._call_module("arxiv", {
                    "action": "search",
                    "query": topic,
                    "sort": strategy.get("sort_by", "relevance")
                })
                results["papers"] = papers
                
                # Find explanatory videos
                videos = self._call_module("youtube", {
                    "action": "find_explanations",
                    "papers": papers.get("titles", [])
                })
                results["videos"] = videos
            
            # Process documents if needed
            if strategy.get("process_pdfs", False):
                processed = self._call_module("marker", {
                    "action": "batch_process",
                    "pdfs": papers.get("pdf_links", [])
                })
                results["processed"] = processed
            
            # Store in knowledge graph
            kg_result = self._call_module("arangodb", {
                "action": "build_knowledge_graph",
                "topic": topic,
                "data": results
            })
            
            # Calculate and report metrics
            metrics = {
                "papers_found": len(results.get("papers", {}).get("items", [])),
                "videos_found": len(results.get("videos", {}).get("items", [])),
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "strategy_used": strategy
            }
            
            # RL updates based on performance
            self._call_module("rl_commons", {
                "action": "update_strategy",
                "metrics": metrics,
                "user_satisfaction": params.get("satisfaction", 0.8)
            })
            
            return InteractionResult(
                interaction_name=self.name,
                level=self.level,
                success=True,
                duration=metrics["processing_time"],
                input_data=params,
                output_data={
                    "results": results,
                    "metrics": metrics,
                    "knowledge_graph": kg_result
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


class TestLevel2Interactions:
    """Test suite for Level 2 interactions."""
    
    @pytest.fixture
    def runner(self):
        """Create interaction runner."""
        return InteractionRunner("Granger Level 2 Tests")
    
    def test_complex_workflow(self, runner):
        """Test complex RL-optimized workflow."""
        interaction = ComplexWorkflowInteraction()
        result = runner.run_interaction(
            interaction,
            task="analyze_codebase_security",
            constraints={
                "max_time": 300,
                "accuracy_target": 0.95
            }
        )
        assert result.success
        assert "rl_config" in result.output_data
        assert result.output_data["optimization_applied"]
    
    def test_adaptive_security(self, runner):
        """Test adaptive security workflow."""
        interaction = AdaptiveSecurityWorkflow()
        
        # Test with different threat levels
        for target in ["test_low_risk", "test_high_risk", "test_critical"]:
            result = runner.run_interaction(
                interaction,
                target=target
            )
            assert result.success
            assert "workflow_path" in result.output_data
            assert result.output_data["adaptive_response"]
    
    def test_research_optimization(self, runner):
        """Test self-optimizing research pipeline."""
        interaction = ResearchPipelineOptimization()
        
        # Run multiple times to test optimization
        topics = ["quantum computing", "machine learning", "cryptography"]
        for topic in topics:
            result = runner.run_interaction(
                interaction,
                topic=topic,
                satisfaction=0.9
            )
            assert result.success
            assert "metrics" in result.output_data
            assert "strategy_used" in result.output_data["metrics"]
    
    def test_workflow_adaptation(self, runner):
        """Test that workflows adapt based on context."""
        interaction = ComplexWorkflowInteraction()
        
        # First run
        result1 = runner.run_interaction(
            interaction,
            task="initial_analysis"
        )
        
        # Second run should use learned patterns
        result2 = runner.run_interaction(
            interaction,
            task="followup_analysis"
        )
        
        assert result1.success and result2.success
        # Verify RL optimization was applied
        assert result1.output_data.get("rl_config") != result2.output_data.get("rl_config")
    
    def test_constraint_handling(self, runner):
        """Test workflow optimization with constraints."""
        interaction = ComplexWorkflowInteraction()
        
        result = runner.run_interaction(
            interaction,
            task="constrained_analysis",
            constraints={
                "max_time": 60,
                "accuracy_target": 0.99,
                "resource_limit": "minimal"
            }
        )
        
        assert result.success
        assert result.duration < 60  # Respects time constraint
        assert "batch_size" in result.output_data["rl_config"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])