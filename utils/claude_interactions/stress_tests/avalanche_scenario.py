#!/usr/bin/env python3
"""
The Avalanche - Cascading Failure Stress Test
Tests system resilience when critical dependencies fail
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import asyncio
import json
from datetime import datetime
from typing import Dict, Any
import random

class AvalancheScenario:
    """Tests cascading failures and graceful degradation"""
    
    def __init__(self, orchestrator, failure_rate: float = 0.3):
        self.orchestrator = orchestrator
        self.failure_rate = failure_rate
        self.metrics = {
            "failures": [],
            "degradations": [],
            "recovery_attempts": 0,
            "total_latency_ms": 0
        }
    
    async def run(self):
        """Execute the avalanche scenario"""
        print("\n🏔️ AVALANCHE SCENARIO: Testing Cascading Failures")
        print("=" * 60)
        
        # Inject failure into orchestrator
        original_execute = self.orchestrator._execute_step
        self.orchestrator._execute_step = self._execute_with_failures(original_execute)
        
        try:
            # Create a complex pipeline that will experience failures
            task = self.orchestrator.create_task(
                name="Research Pipeline",
                description="Multi-stage research with potential failures"
            )
            
            # Step 1: ArXiv search (might fail)
            self.orchestrator.add_step(
                task,
                module="arxiv-mcp-server",
                capability="search_papers",
                input_data={"query": "quantum computing breakthroughs", "max_results": 5}
            )
            
            # Step 2: Download papers (depends on step 1)
            self.orchestrator.add_step(
                task,
                module="arxiv-mcp-server",
                capability="download_paper",
                input_data={"paper_id": ".papers[0].id"},
                depends_on=["step_1"]
            )
            
            # Step 3: Extract content (depends on step 2)
            self.orchestrator.add_step(
                task,
                module="marker",
                capability="extract_text",
                input_data={"file_path": ".file_path"},
                depends_on=["step_2"]
            )
            
            # Step 4: Build knowledge graph (can use partial data)
            self.orchestrator.add_step(
                task,
                module="arangodb",
                capability="build_knowledge_graph",
                input_data={
                    "nodes": [{"content": ".text", "fallback": "Limited data available"}],
                    "edges": []
                },
                depends_on=["step_3"]
            )
            
            # Execute and observe cascading effects
            start_time = datetime.now()
            result = await self.orchestrator.execute_task(task.id)
            end_time = datetime.now()
            
            self.metrics["total_latency_ms"] = (end_time - start_time).total_seconds() * 1000
            
            # Analyze results
            self._analyze_cascade_effects(result)
            
        finally:
            # Restore original execution
            self.orchestrator._execute_step = original_execute
            
        self._print_summary()
    
    def _execute_with_failures(self, original_execute):
        """Wrapper to inject failures"""
        async def wrapper(step):
            if random.random() < self.failure_rate:
                error_type = random.choice(["TimeoutError", "ConnectionError", "DataError"])
                self.metrics["failures"].append({
                    "step": step["name"],
                    "error": error_type,
                    "timestamp": datetime.now().isoformat()
                })
                raise Exception(f"{error_type}: Simulated failure in {step['module']}")
            
            # Add artificial latency
            await asyncio.sleep(random.uniform(0.5, 2.0))
            
            try:
                return await original_execute(step)
            except Exception as e:
                # Try graceful degradation
                self.metrics["degradations"].append({
                    "step": step["name"],
                    "reason": str(e)
                })
                return {"status": "degraded", "data": None, "error": str(e)}
        
        return wrapper
    
    def _analyze_cascade_effects(self, result):
        """Analyze how failures propagated"""
        print("\n📊 Cascade Analysis:")
        
        for step_id, step_result in result.get("outputs", {}).items():
            if "error" in step_result:
                print(f"  ❌ {step_id}: Failed - {step_result['error']}")
            elif step_result.get("status") == "degraded":
                print(f"  ⚠️  {step_id}: Degraded operation")
            else:
                print(f"  ✅ {step_id}: Succeeded")
    
    def _print_summary(self):
        """Print scenario summary"""
        print("\n📈 Scenario Metrics:")
        print(f"  Total Failures: {len(self.metrics['failures'])}")
        print(f"  Degraded Operations: {len(self.metrics['degradations'])}")
        print(f"  Total Latency: {self.metrics['total_latency_ms']:.0f}ms")
        print(f"  Failure Rate: {self.failure_rate * 100:.0f}%")
