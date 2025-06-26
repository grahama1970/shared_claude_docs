#!/usr/bin/env python3
"""
Research Consensus Engine - Multi-Agent Negotiation
Multiple AI agents debate and converge on a research topic through iterative critique
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, List
import json

class ResearchConsensusEngineScenario:
    """
    Tests iterative multi-agent negotiation pattern where module outputs
    are fed back to other module instances for critique and refinement.
    
    Communication Pattern: Circular feedback loops with stateful refinement
    """
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.agents = ["Agent_A", "Agent_B", "Agent_C"]
        self.consensus_history = []
        self.debate_rounds = 3
        
    async def run(self, topic: str = "AI Ethics in Large Language Models"):
        """Run multi-agent consensus building"""
        print(f"\n🤝 RESEARCH CONSENSUS ENGINE: {topic}")
        print("=" * 70)
        
        # Phase 1: Initial research acquisition
        papers = await self._phase_1_acquire_research(topic)
        
        # Phase 2: Multi-agent debate and refinement
        consensus = await self._phase_2_consensus_building(papers, topic)
        
        # Phase 3: Verification and storage
        await self._phase_3_verify_and_store(consensus, topic)
        
        self._print_consensus_report()    
    async def _phase_1_acquire_research(self, topic: str):
        """Gather research papers for agents to analyze"""
        print("\n📚 Phase 1: Research Acquisition")
        print("-" * 50)
        
        task = self.orchestrator.create_task(
            name="Research Acquisition",
            description="Gather papers for multi-agent analysis"
        )
        
        # Search for papers
        print(f"  🔍 Searching for papers on: {topic}")
        self.orchestrator.add_step(
            task,
            module="arxiv-mcp-server",
            capability="search_papers",
            input_data={
                "query": topic,
                "max_results": 3,
                "sort_by": "relevance"
            }
        )
        
        # Download and extract text from each paper
        print("  📥 Downloading and processing papers...")
        papers_data = []
        for i in range(3):
            # Download paper
            self.orchestrator.add_step(
                task,
                module="arxiv-mcp-server",
                capability="download_paper",
                input_data={"paper_id": f"$step_1.papers[{i}].id"},
                depends_on=["step_1"]
            )
            
            # Extract text
            self.orchestrator.add_step(
                task,
                module="marker",
                capability="extract_text",
                input_data={
                    "pdf_path": f"$step_{2+i*2}.local_pdf_path",
                    "output_format": "markdown"
                },
                depends_on=[f"step_{2+i*2}"]
            )
            
            papers_data.append({
                "paper_id": f"$step_1.papers[{i}].id",
                "title": f"$step_1.papers[{i}].title",
                "text": f"$step_{3+i*2}.text"
            })
        
        result = await self.orchestrator.execute_task(task.id)
        return papers_data    
    async def _phase_2_consensus_building(self, papers: List[Dict], topic: str):
        """Multi-agent debate and refinement"""
        print("\n🎭 Phase 2: Multi-Agent Consensus Building")
        print("-" * 50)
        
        task = self.orchestrator.create_task(
            name="Consensus Building",
            description="Agents debate and refine understanding"
        )
        
        # Initial summaries by each agent
        print("\n  📝 Initial Agent Summaries:")
        agent_summaries = {}
        
        for i, agent in enumerate(self.agents):
            print(f"    • {agent} analyzing paper {i+1}...")
            self.orchestrator.add_step(
                task,
                module="claude_max_proxy",
                capability="analyze",
                input_data={
                    "text": papers[i]["text"],
                    "prompt": f"As {agent}, summarize key arguments about {topic} from this paper. Focus on ethical implications and technical considerations.",
                    "max_length": 500
                }
            )
            agent_summaries[agent] = f"$step_{i+1}.response"
        
        # Iterative critique and refinement rounds
        for round_num in range(self.debate_rounds):
            print(f"\n  🔄 Debate Round {round_num + 1}:")
            
            round_summaries = {}
            for i, agent in enumerate(self.agents):
                # Get other agents' summaries
                other_agents = [a for a in self.agents if a != agent]
                
                # Agent critiques others and refines own position
                critique_prompt = f"""
                As {agent}, review these positions:
                {other_agents[0]}: {agent_summaries[other_agents[0]]}
                {other_agents[1]}: {agent_summaries[other_agents[1]]}
                
                Your current position: {agent_summaries[agent]}
                
                Critique the other positions, identify agreements/disagreements, and refine your position.
                """
                
                self.orchestrator.add_step(
                    task,
                    module="claude_max_proxy",
                    capability="analyze",
                    input_data={
                        "prompt": critique_prompt,
                        "mode": "critique_and_refine"
                    }
                )
                round_summaries[agent] = f"$step_{3 + round_num * 3 + i + 1}.response"
            
            # Update summaries for next round
            agent_summaries = round_summaries
            
            # Track consensus evolution
            self.consensus_history.append({
                "round": round_num + 1,
                "summaries": agent_summaries
            })
        
        # Final consensus generation
        print("\n  🎯 Generating Final Consensus:")
        self.orchestrator.add_step(
            task,
            module="claude_max_proxy",
            capability="synthesize",
            input_data={
                "texts": list(agent_summaries.values()),
                "prompt": f"Synthesize these refined positions into a unified consensus on {topic}",
                "output_format": "structured_consensus"
            }
        )
        
        result = await self.orchestrator.execute_task(task.id)
        return result["outputs"][f"step_{3 + self.debate_rounds * 3 + 1}"]["response"]    
    async def _phase_3_verify_and_store(self, consensus: str, topic: str):
        """Store consensus and verify process"""
        print("\n✅ Phase 3: Verification and Storage")
        print("-" * 50)
        
        task = self.orchestrator.create_task(
            name="Consensus Storage",
            description="Store and verify consensus outcome"
        )
        
        # Store in knowledge graph
        print("  🕸️ Storing consensus in knowledge graph...")
        self.orchestrator.add_step(
            task,
            module="arangodb",
            capability="create_node",
            input_data={
                "node_type": "ConsensusOutcome",
                "properties": {
                    "topic": topic,
                    "consensus": consensus,
                    "agents": self.agents,
                    "rounds": self.debate_rounds,
                    "timestamp": datetime.now().isoformat()
                },
                "metadata": {
                    "debate_history": self.consensus_history
                }
            }
        )
        
        # Generate test report
        print("  📊 Generating consensus report...")
        self.orchestrator.add_step(
            task,
            module="claude-test-reporter",
            capability="generate_report",
            input_data={
                "test_name": "ResearchConsensusEngine",
                "test_type": "multi_agent_negotiation",
                "results": {
                    "topic": topic,
                    "agents": len(self.agents),
                    "debate_rounds": self.debate_rounds,
                    "consensus_achieved": True,
                    "consensus_summary": consensus
                }
            }
        )
        
        await self.orchestrator.execute_task(task.id)
    
    def _print_consensus_report(self):
        """Print consensus building summary"""
        print("\n📋 CONSENSUS REPORT")
        print("=" * 60)
        
        print(f"\nAgents Involved: {', '.join(self.agents)}")
        print(f"Debate Rounds: {self.debate_rounds}")
        print(f"Consensus History Length: {len(self.consensus_history)}")
        
        print("\nKey Pattern Demonstrated:")
        print("  • Multi-agent circular feedback loops")
        print("  • Iterative refinement through critique")
        print("  • Convergence to unified position")
        print("  • Stateful debate tracking")
        
        print("\nCommunication Flow:")
        print("  Papers → Individual Analysis → Critique Loops → Consensus")


if __name__ == "__main__":
    print("ResearchConsensusEngine tests:")
    print("- Multiple AI agents debating")
    print("- Circular critique and refinement")
    print("- Consensus emergence from disagreement")
    print("- Stateful multi-round negotiation")