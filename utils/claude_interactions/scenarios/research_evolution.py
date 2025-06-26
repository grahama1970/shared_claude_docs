#!/usr/bin/env python3
"""
Research Evolution Scenario
Demonstrates how modules collaborate to research, analyze, and evolve understanding
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path

class ResearchEvolutionScenario:
    """
    A scenario where modules collaborate to:
    1. Research a topic on ArXiv
    2. Extract and analyze papers with Marker
    3. Build a knowledge graph with ArangoDB
    4. Train models with Sparta
    5. Generate visualizations
    6. Self-improve based on results
    """
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.research_history = []
        self.knowledge_graph = nx.DiGraph()
        self.evolution_metrics = {
            "iterations": 0,
            "papers_processed": 0,
            "concepts_discovered": set(),
            "model_improvements": []
        }
    
    async def run(self, initial_query: str, iterations: int = 3):
        """Run the research evolution scenario"""
        print(f"🔬 Starting Research Evolution: '{initial_query}'")
        print("="*60)
        
        current_query = initial_query
        
        for i in range(iterations):
            print(f"\n📚 Iteration {i+1}/{iterations}")
            print("-"*40)
            
            # Phase 1: Research
            papers = await self._research_phase(current_query)
            
            # Phase 2: Extract and Analyze
            analyses = await self._analysis_phase(papers)
            
            # Phase 3: Build Knowledge Graph
            graph_update = await self._knowledge_graph_phase(analyses)
            
            # Phase 4: Train Models
            model_results = await self._training_phase(analyses)
            
            # Phase 5: Visualize Progress
            await self._visualization_phase()
            
            # Phase 6: Evolve Query
            current_query = await self._evolution_phase(analyses, model_results)
            
            self.evolution_metrics["iterations"] += 1
            
            print(f"\n✨ Evolution: New research direction: '{current_query}'")
        
        # Final summary
        await self._generate_final_report()
    
    async def _research_phase(self, query: str) -> List[Dict[str, Any]]:
        """Research papers on ArXiv"""
        print(f"  🔍 Searching for: {query}")
        
        task = self.orchestrator.create_task(
            name="Research Papers",
            description=f"Search ArXiv for: {query}"
        )
        
        self.orchestrator.add_step(
            task,
            module="arxiv-mcp-server",
            capability="search_papers",
            input_data={"query": query, "max_results": 5}
        )
        
        result = await self.orchestrator.execute_task(task.id)
        papers = result["outputs"]["step_1"]["papers"]
        
        print(f"  📄 Found {len(papers)} papers")
        self.evolution_metrics["papers_processed"] += len(papers)
        
        return papers
    
    async def _analysis_phase(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract and analyze paper content"""
        print("  📝 Analyzing papers...")
        
        analyses = []
        
        for i, paper in enumerate(papers[:3]):  # Analyze top 3 papers
            task = self.orchestrator.create_task(
                name=f"Analyze Paper {i+1}",
                description=f"Extract and analyze: {paper['title']}"
            )
            
            # Extract text
            self.orchestrator.add_step(
                task,
                module="marker",
                capability="extract_text",
                input_data={
                    "file_path": paper["pdf_url"],
                    "format": "pdf"
                }
            )
            
            # Segment document
            self.orchestrator.add_step(
                task,
                module="marker",
                capability="segment_document",
                input_data={"text": "$step_1.text"},
                depends_on=["step_1"]
            )
            
            # Analyze content (using youtube_transcripts analyzer)
            self.orchestrator.add_step(
                task,
                module="youtube_transcripts",
                capability="analyze_content",
                input_data={"transcript": "$step_1.text"},
                depends_on=["step_1"]
            )
            
            result = await self.orchestrator.execute_task(task.id)
            
            analysis = {
                "paper": paper,
                "segments": result["outputs"].get("step_2", {}).get("segments", []),
                "topics": result["outputs"].get("step_3", {}).get("topics", []),
                "summary": result["outputs"].get("step_3", {}).get("summary", "")
            }
            analyses.append(analysis)
            
            # Update concepts
            for topic in analysis["topics"]:
                self.evolution_metrics["concepts_discovered"].add(topic)
        
        print(f"  ✅ Analyzed {len(analyses)} papers")
        print(f"  💡 Total concepts discovered: {len(self.evolution_metrics['concepts_discovered'])}")
        
        return analyses
    
    async def _knowledge_graph_phase(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build and update knowledge graph"""
        print("  🕸️  Updating knowledge graph...")
        
        # Extract nodes and edges
        nodes = []
        edges = []
        
        for analysis in analyses:
            paper_node = {
                "id": analysis["paper"]["id"],
                "type": "paper",
                "title": analysis["paper"]["title"],
                "authors": analysis["paper"]["authors"]
            }
            nodes.append(paper_node)
            
            # Add concept nodes and edges
            for topic in analysis["topics"]:
                concept_node = {
                    "id": f"concept_{topic}",
                    "type": "concept",
                    "name": topic
                }
                nodes.append(concept_node)
                
                edge = {
                    "from": paper_node["id"],
                    "to": concept_node["id"],
                    "type": "contains_concept"
                }
                edges.append(edge)
                
                # Update local graph
                self.knowledge_graph.add_node(topic, type="concept")
                self.knowledge_graph.add_edge(analysis["paper"]["title"], topic)
        
        # Store in ArangoDB
        task = self.orchestrator.create_task(
            name="Update Knowledge Graph",
            description="Store research findings in graph database"
        )
        
        self.orchestrator.add_step(
            task,
            module="arangodb",
            capability="create_knowledge_graph",
            input_data={"nodes": nodes, "edges": edges}
        )
        
        result = await self.orchestrator.execute_task(task.id)
        
        print(f"  ✅ Graph updated: {len(nodes)} nodes, {len(edges)} edges")
        
        return result["outputs"]["step_1"]
    
    async def _training_phase(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train or fine-tune models based on findings"""
        print("  🤖 Training models on new knowledge...")
        
        # Prepare training data from analyses
        training_texts = []
        for analysis in analyses:
            training_texts.extend(analysis["segments"])
        
        task = self.orchestrator.create_task(
            name="Model Training",
            description="Train models on research findings"
        )
        
        self.orchestrator.add_step(
            task,
            module="sparta",
            capability="train_model",
            input_data={
                "dataset": {"texts": training_texts},
                "model_type": "transformer",
                "config": {
                    "epochs": 3,
                    "batch_size": 8,
                    "learning_rate": 1e-4
                }
            }
        )
        
        result = await self.orchestrator.execute_task(task.id)
        metrics = result["outputs"]["step_1"].get("metrics", {})
        
        self.evolution_metrics["model_improvements"].append({
            "iteration": self.evolution_metrics["iterations"],
            "metrics": metrics
        })
        
        print(f"  ✅ Model trained with performance: {metrics}")
        
        return result["outputs"]["step_1"]
    
    async def _visualization_phase(self):
        """Create visualizations of the research evolution"""
        print("  📊 Generating visualizations...")
        
        # Create knowledge graph visualization
        plt.figure(figsize=(12, 8))
        
        # Subplot 1: Knowledge Graph
        plt.subplot(2, 2, 1)
        if len(self.knowledge_graph.nodes()) > 0:
            pos = nx.spring_layout(self.knowledge_graph)
            nx.draw(self.knowledge_graph, pos, with_labels=True, node_size=500, 
                   node_color='lightblue', font_size=8, font_weight='bold')
            plt.title("Knowledge Graph Evolution")
        
        # Subplot 2: Concepts Over Time
        plt.subplot(2, 2, 2)
        iterations = list(range(1, self.evolution_metrics["iterations"] + 2))
        concepts_count = [len(self.evolution_metrics["concepts_discovered"])] * len(iterations)
        plt.plot(iterations, concepts_count, 'o-')
        plt.title("Concepts Discovered")
        plt.xlabel("Iteration")
        plt.ylabel("Total Concepts")
        
        # Subplot 3: Papers Processed
        plt.subplot(2, 2, 3)
        plt.bar(["Papers"], [self.evolution_metrics["papers_processed"]])
        plt.title("Research Volume")
        plt.ylabel("Count")
        
        # Subplot 4: Model Performance
        plt.subplot(2, 2, 4)
        if self.evolution_metrics["model_improvements"]:
            iterations = [m["iteration"] + 1 for m in self.evolution_metrics["model_improvements"]]
            accuracies = [m["metrics"].get("accuracy", 0) for m in self.evolution_metrics["model_improvements"]]
            plt.plot(iterations, accuracies, 'o-')
            plt.title("Model Performance Evolution")
            plt.xlabel("Iteration")
            plt.ylabel("Accuracy")
        
        plt.tight_layout()
        
        # Save visualization
        output_dir = Path("./visualizations")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(output_dir / f"research_evolution_{timestamp}.png")
        plt.close()
        
        print(f"  ✅ Visualizations saved to visualizations/")
    
    async def _evolution_phase(self, analyses: List[Dict[str, Any]], 
                              model_results: Dict[str, Any]) -> str:
        """Evolve the research query based on findings"""
        print("  🧬 Evolving research direction...")
        
        # Collect all discovered topics
        all_topics = set()
        for analysis in analyses:
            all_topics.update(analysis["topics"])
        
        # Find emerging topics (topics that appear frequently)
        topic_frequency = {}
        for analysis in analyses:
            for topic in analysis["topics"]:
                topic_frequency[topic] = topic_frequency.get(topic, 0) + 1
        
        # Select top emerging topics
        emerging_topics = sorted(topic_frequency.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Generate new query combining emerging topics
        if emerging_topics:
            new_topics = [topic[0] for topic in emerging_topics]
            new_query = f"{' AND '.join(new_topics)} recent advances"
        else:
            # Fallback: modify original query
            new_query = f"advanced {self.orchestrator.context.get('original_query', 'research')}"
        
        return new_query
    
    async def _generate_final_report(self):
        """Generate a comprehensive report of the research evolution"""
        print("\n" + "="*60)
        print("📈 RESEARCH EVOLUTION SUMMARY")
        print("="*60)
        
        report = {
            "total_iterations": self.evolution_metrics["iterations"],
            "papers_processed": self.evolution_metrics["papers_processed"],
            "unique_concepts": list(self.evolution_metrics["concepts_discovered"]),
            "concept_count": len(self.evolution_metrics["concepts_discovered"]),
            "knowledge_graph_size": {
                "nodes": self.knowledge_graph.number_of_nodes(),
                "edges": self.knowledge_graph.number_of_edges()
            },
            "model_improvements": self.evolution_metrics["model_improvements"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Save report
        output_dir = Path("./reports")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = output_dir / f"research_evolution_report_{timestamp}.json"
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Key Metrics:")
        print(f"  • Papers analyzed: {report['papers_processed']}")
        print(f"  • Unique concepts: {report['concept_count']}")
        print(f"  • Graph nodes: {report['knowledge_graph_size']['nodes']}")
        print(f"  • Graph edges: {report['knowledge_graph_size']['edges']}")
        
        if report['model_improvements']:
            latest_accuracy = report['model_improvements'][-1]['metrics'].get('accuracy', 0)
            print(f"  • Latest model accuracy: {latest_accuracy:.2%}")
        
        print(f"\n📁 Report saved to: {report_path}")
        
        # Show top concepts
        if report['unique_concepts']:
            print(f"\n🏆 Top Discovered Concepts:")
            for i, concept in enumerate(report['unique_concepts'][:10], 1):
                print(f"  {i}. {concept}")

# Example usage
async def main():
    """Run the research evolution scenario"""
    from orchestrator.task_orchestrator import ConversationalOrchestrator
    
    async with ConversationalOrchestrator() as orchestrator:
        scenario = ResearchEvolutionScenario(orchestrator)
        
        # Run research evolution on transformer architectures
        await scenario.run(
            initial_query="transformer architecture attention mechanisms",
            iterations=3
        )

if __name__ == "__main__":
    asyncio.run(main())