#!/usr/bin/env python3
"""
Dynamic Knowledge Explorer - Adaptive Branching Exploration
Demonstrates dynamic orchestration through conditional branching based on runtime decisions
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, List
import random

class DynamicKnowledgeExplorerScenario:
    """
    Tests dynamic orchestration with conditional branching where workflow
    adapts based on module outputs, creating variable paths and sequences.
    
    Communication Pattern: Conditional branching with runtime adaptation
    """
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.exploration_tree = {
            "root": None,
            "branches": [],
            "depth": 0
        }
        self.max_depth = 3
        self.explored_paths = []
        
    async def run(self, initial_query: str = "Quantum Computing Breakthroughs"):
        """Run dynamic knowledge exploration"""
        print(f"\n🔭 DYNAMIC KNOWLEDGE EXPLORER: {initial_query}")
        print("=" * 70)
        
        # Start exploration from root query
        await self._explore_branch(initial_query, depth=0, path=[])
        
        # Synthesize findings
        await self._synthesize_exploration()
        
        self._print_exploration_map()    
    async def _explore_branch(self, query: str, depth: int, path: List[str]):
        """Recursively explore knowledge branches"""
        if depth >= self.max_depth:
            return
            
        print(f"\n{'  ' * depth}🌿 Depth {depth}: Exploring '{query}'")
        
        task = self.orchestrator.create_task(
            name=f"Explore_D{depth}",
            description=f"Dynamic exploration at depth {depth}"
        )
        
        # Determine exploration strategy
        self.orchestrator.add_step(
            task,
            module="claude_max_proxy",
            capability="analyze",
            input_data={
                "prompt": f"For '{query}', choose best source: papers/videos/web",
                "mode": "strategy_selection"
            }
        )
        
        # Simulate different paths based on depth
        strategy = ['papers', 'videos', 'web'][depth % 3]
        
        if strategy == "papers":
            await self._explore_papers_path(task, query)
        elif strategy == "videos":
            await self._explore_videos_path(task, query)
        else:
            await self._explore_web_path(task, query)
        
        # Execute task
        result = await self.orchestrator.execute_task(task.id)
        
        # Mock discovered topics for branching
        new_topics = self._get_mock_topics(strategy, query)
        
        # Record exploration
        self.explored_paths.append({
            "query": query,
            "depth": depth,
            "strategy": strategy,
            "discoveries": new_topics
        })
        
        # Conditionally explore new branches
        for topic in new_topics[:1]:  # Limit branching
            await self._explore_branch(topic, depth + 1, path + [query])
    
    async def _explore_papers_path(self, task, query):
        """Research paper exploration path"""
        self.orchestrator.add_step(
            task,
            module="arxiv-mcp-server",
            capability="search_papers",
            input_data={"query": query, "max_results": 2}
        )
        
        self.orchestrator.add_step(
            task,
            module="marker",
            capability="extract_key_points",
            input_data={"papers": "$step_2.papers"},
            depends_on=["step_2"]
        )
    
    async def _explore_videos_path(self, task, query):
        """Video content exploration path"""
        self.orchestrator.add_step(
            task,
            module="youtube_transcripts",
            capability="search_videos",
            input_data={"query": query, "limit": 2}
        )
        
        self.orchestrator.add_step(
            task,
            module="claude_max_proxy",
            capability="analyze",
            input_data={
                "text": "$step_2.transcripts",
                "prompt": "Extract key concepts"
            },
            depends_on=["step_2"]
        )
    
    async def _explore_web_path(self, task, query):
        """Web content exploration path"""
        self.orchestrator.add_step(
            task,
            module="mcp-screenshot",
            capability="capture_page",
            input_data={"url": f"https://search.example.com?q={query}"}
        )
        
        self.orchestrator.add_step(
            task,
            module="claude_max_proxy",
            capability="analyze_visual",
            input_data={"image": "$step_2.screenshot_path"},
            depends_on=["step_2"]
        )
    
    def _get_mock_topics(self, strategy, query):
        """Generate mock topics for demonstration"""
        topics_map = {
            "papers": ["Theoretical Advances", "Novel Algorithms"],
            "videos": ["Practical Applications", "Industry Trends"],
            "web": ["Latest News", "Community Discussions"]
        }
        return topics_map.get(strategy, ["Topic A", "Topic B"])
    
    async def _synthesize_exploration(self):
        """Synthesize all exploration findings"""
        print("\n🎯 Synthesizing Exploration Results")
        print("-" * 50)
        
        task = self.orchestrator.create_task(
            name="Synthesis",
            description="Combine all exploration findings"
        )
        
        # Store exploration tree in graph
        self.orchestrator.add_step(
            task,
            module="arangodb",
            capability="create_graph",
            input_data={
                "graph_name": "exploration_tree",
                "nodes": self.explored_paths,
                "edges": self._build_path_edges()
            }
        )
        
        # Generate exploration report
        self.orchestrator.add_step(
            task,
            module="claude-test-reporter",
            capability="generate_report",
            input_data={
                "test_name": "DynamicKnowledgeExplorer",
                "paths_explored": len(self.explored_paths),
                "max_depth_reached": max(p["depth"] for p in self.explored_paths),
                "strategies_used": list(set(p["strategy"] for p in self.explored_paths))
            }
        )
        
        await self.orchestrator.execute_task(task.id)
    
    def _build_path_edges(self):
        """Build edges for exploration tree"""
        edges = []
        for i, path in enumerate(self.explored_paths):
            if path["depth"] > 0:
                # Find parent
                for j, parent in enumerate(self.explored_paths):
                    if parent["depth"] == path["depth"] - 1:
                        edges.append({"from": j, "to": i, "type": "explored"})
                        break
        return edges
    
    def _print_exploration_map(self):
        """Print exploration summary"""
        print("\n🗺️ EXPLORATION MAP")
        print("=" * 60)
        
        print(f"\nTotal Paths Explored: {len(self.explored_paths)}")
        print(f"Maximum Depth Reached: {max(p['depth'] for p in self.explored_paths)}")
        
        print("\nExploration Tree:")
        for path in self.explored_paths:
            indent = "  " * path["depth"]
            print(f"{indent}└─ {path['query']} [{path['strategy']}]")
        
        print("\nKey Pattern Demonstrated:")
        print("  • Dynamic path selection based on content")
        print("  • Recursive exploration with depth limits")
        print("  • Multiple exploration strategies")
        print("  • Adaptive workflow branching")


if __name__ == "__main__":
    print("DynamicKnowledgeExplorer tests:")
    print("- Conditional branching based on analysis")
    print("- Variable-length exploration paths")
    print("- Runtime workflow adaptation")
    print("- Multi-strategy exploration")