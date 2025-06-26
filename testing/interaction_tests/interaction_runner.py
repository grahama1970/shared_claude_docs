#!/usr/bin/env python3
"""
Simple Interaction Runner
Execute and debug specific module interaction patterns
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add module paths
sys.path.append("/home/graham/workspace/arxiv-mcp-server")
sys.path.append("/home/graham/workspace/youtube_transcripts")
sys.path.append("/home/graham/workspace/shared_claude_docs")


class InteractionRunner:
    """Run specific interaction patterns with detailed logging"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.execution_log = []
    
    def log(self, message: str, level: str = "INFO"):
        """Log execution details"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] {level}: {message}"
        self.execution_log.append(log_entry)
        if self.verbose:
            print(log_entry)
    
    async def run_interaction(self, pattern_name: str, **kwargs):
        """Run a specific interaction pattern"""
        self.log(f"Starting interaction: {pattern_name}", "START")
        
        patterns = {
            "arxiv_search": self.arxiv_search,
            "youtube_search": self.youtube_search,
            "paper_to_knowledge": self.paper_to_knowledge,
            "multi_source_research": self.multi_source_research,
            "visualization_decision": self.visualization_decision,
            "self_improvement_cycle": self.self_improvement_cycle
        }
        
        if pattern_name not in patterns:
            self.log(f"Unknown pattern: {pattern_name}", "ERROR")
            return None
        
        try:
            result = await patterns[pattern_name](**kwargs)
            self.log(f"Completed: {pattern_name}", "SUCCESS")
            return result
        except Exception as e:
            self.log(f"Failed: {pattern_name} - {str(e)}", "ERROR")
            raise
    
    # LEVEL 0: Direct Module Calls
    
    async def arxiv_search(self, query: str = "machine learning", max_results: int = 5):
        """Level 0: Direct ArXiv search"""
        self.log(f"ArXiv search: '{query}'")
        
        try:
            from arxiv_mcp_server.tools import handle_search
            
            result = await handle_search({
                "query": query,
                "max_results": max_results
            })
            
            papers = json.loads(result[0].text)["papers"]
            
            self.log(f"Found {len(papers)} papers")
            for i, paper in enumerate(papers[:3]):
                self.log(f"  {i+1}. {paper['title'][:60]}...")
            
            return papers
            
        except Exception as e:
            self.log(f"ArXiv search failed: {str(e)}", "ERROR")
            return []
    
    async def youtube_search(self, query: str = "python tutorial"):
        """Level 0: Direct YouTube search"""
        self.log(f"YouTube search: '{query}'")
        
        try:
            from youtube_transcripts.unified_search import UnifiedYouTubeSearch, UnifiedSearchConfig
            
            config = UnifiedSearchConfig()
            search = UnifiedYouTubeSearch(config)
            
            # Search local database first
            results = search.search(query=query, use_widening=True)
            
            videos = results.get("results", [])
            self.log(f"Found {len(videos)} videos in local database")
            
            for i, video in enumerate(videos[:3]):
                self.log(f"  {i+1}. {video['title'][:60]}...")
            
            return videos
            
        except Exception as e:
            self.log(f"YouTube search failed: {str(e)}", "ERROR")
            return []
    
    # LEVEL 1: Sequential Pipelines
    
    async def paper_to_knowledge(self, topic: str = "transformers"):
        """Level 1: ArXiv → Extract → Analyze"""
        self.log(f"Paper to knowledge pipeline: '{topic}'")
        
        # Step 1: Search for papers
        self.log("Step 1: Searching ArXiv...")
        papers = await self.arxiv_search(topic, max_results=3)
        
        if not papers:
            self.log("No papers found", "WARNING")
            return None
        
        # Step 2: Process first paper
        paper = papers[0]
        self.log(f"Step 2: Processing paper: {paper['title'][:60]}...")
        
        # Simulate extraction (in real implementation, use marker)
        extracted_content = {
            "title": paper["title"],
            "abstract": paper.get("summary", ""),
            "key_concepts": self._extract_concepts(paper.get("summary", ""))
        }
        self.log(f"Extracted {len(extracted_content['key_concepts'])} key concepts")
        
        # Step 3: Analyze
        self.log("Step 3: Analyzing content...")
        analysis = {
            "paper_id": paper["id"],
            "extracted": extracted_content,
            "relevance_score": 0.85,
            "implementation_ideas": [
                "Use attention mechanism",
                "Implement positional encoding",
                "Add layer normalization"
            ]
        }
        
        self.log("Pipeline completed successfully")
        return analysis
    
    # LEVEL 2: Parallel Processing
    
    async def multi_source_research(self, topic: str = "machine learning"):
        """Level 2: Parallel ArXiv + YouTube research"""
        self.log(f"Multi-source research: '{topic}'")
        
        # Create parallel tasks
        self.log("Launching parallel searches...")
        
        arxiv_task = asyncio.create_task(self.arxiv_search(topic))
        youtube_task = asyncio.create_task(self.youtube_search(topic))
        
        # Wait for both
        self.log("Waiting for results...")
        papers, videos = await asyncio.gather(arxiv_task, youtube_task)
        
        # Merge results
        self.log("Merging results...")
        merged = {
            "topic": topic,
            "sources": {
                "arxiv": {
                    "count": len(papers),
                    "titles": [p["title"] for p in papers[:3]]
                },
                "youtube": {
                    "count": len(videos),
                    "titles": [v["title"] for v in videos[:3]]
                }
            },
            "total_resources": len(papers) + len(videos)
        }
        
        self.log(f"Found {merged['total_resources']} total resources")
        return merged
    
    # LEVEL 3: Complex Orchestration
    
    async def visualization_decision(self, data_description: Dict[str, Any]):
        """Level 3: Intelligent visualization decision with feedback"""
        self.log("Visualization decision process starting...")
        
        # Phase 1: Analyze data characteristics
        self.log("Phase 1: Analyzing data characteristics...")
        data_type = data_description.get("type", "unknown")
        dimensions = data_description.get("dimensions", [])
        sparsity = data_description.get("sparsity", 0)
        
        self.log(f"  Type: {data_type}")
        self.log(f"  Dimensions: {dimensions}")
        self.log(f"  Sparsity: {sparsity:.2%}")
        
        # Phase 2: Research best practices
        self.log("Phase 2: Researching visualization best practices...")
        
        # Search for relevant papers
        query = f"{data_type} visualization techniques"
        papers = await self.arxiv_search(query, max_results=2)
        
        # Phase 3: Make decision
        self.log("Phase 3: Making visualization decision...")
        
        decision = self._make_viz_decision(data_type, dimensions, sparsity)
        
        # Phase 4: Validate decision
        self.log("Phase 4: Validating decision...")
        
        if decision["rejected_visualizations"]:
            self.log(f"  Rejected: {', '.join(decision['rejected_visualizations'])}")
        self.log(f"  Recommended: {decision['recommendation']}")
        self.log(f"  Reasoning: {decision['reasoning']}")
        
        # Phase 5: Learn from outcome
        self.log("Phase 5: Recording decision for future learning...")
        
        return decision
    
    async def self_improvement_cycle(self, target_module: str = "visualization_optimizer"):
        """Level 3: Self-improvement with research and implementation"""
        self.log(f"Self-improvement cycle for: {target_module}")
        
        # Phase 1: Analyze current state
        self.log("Phase 1: Analyzing current implementation...")
        current_metrics = {
            "accuracy": 0.75,
            "performance": "moderate",
            "issues": ["slow on large datasets", "limited chart types"]
        }
        
        # Phase 2: Research improvements
        self.log("Phase 2: Researching improvements...")
        
        # Search papers
        papers = await self.arxiv_search(f"{target_module} optimization", max_results=3)
        
        # Search tutorials
        videos = await self.youtube_search(f"{target_module} tutorial")
        
        # Phase 3: Generate improvement plan
        self.log("Phase 3: Generating improvement plan...")
        
        improvements = []
        if papers:
            improvements.append({
                "source": papers[0]["title"],
                "improvement": "Implement caching for repeated queries",
                "expected_impact": "+20% performance"
            })
        
        if videos:
            improvements.append({
                "source": videos[0]["title"],
                "improvement": "Add parallel processing",
                "expected_impact": "+50% speed on large datasets"
            })
        
        # Phase 4: Simulate implementation
        self.log("Phase 4: Implementing improvements...")
        for imp in improvements:
            self.log(f"  Implementing: {imp['improvement']}")
            await asyncio.sleep(0.5)  # Simulate work
        
        # Phase 5: Test and validate
        self.log("Phase 5: Testing improvements...")
        new_metrics = {
            "accuracy": 0.82,
            "performance": "high",
            "issues": ["none"]
        }
        
        # Phase 6: Decision
        self.log("Phase 6: Evaluating results...")
        if new_metrics["accuracy"] > current_metrics["accuracy"]:
            self.log("  ✅ Improvements successful - ready to commit")
            result = {
                "status": "success",
                "improvements": improvements,
                "metrics_before": current_metrics,
                "metrics_after": new_metrics,
                "commit_ready": True
            }
        else:
            self.log("  ❌ Improvements did not meet criteria")
            result = {
                "status": "failed",
                "reason": "No improvement in metrics"
            }
        
        return result
    
    # Helper methods
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        # Simple keyword extraction
        keywords = ["machine learning", "neural network", "transformer", 
                   "attention", "deep learning", "optimization"]
        
        found = []
        text_lower = text.lower()
        for keyword in keywords:
            if keyword in text_lower:
                found.append(keyword)
        
        return found[:5]  # Return top 5
    
    def _make_viz_decision(self, data_type: str, dimensions: List[int], 
                          sparsity: float) -> Dict[str, Any]:
        """Make visualization decision based on data characteristics"""
        
        rejected = []
        recommendation = ""
        reasoning = ""
        
        if data_type == "sparse_matrix" and sparsity > 0.9:
            rejected = ["heatmap", "3d_surface"]
            recommendation = "interactive_table"
            reasoning = "Data is too sparse (>90% empty) for heatmap visualization"
        
        elif data_type == "tabular" and len(dimensions) == 2:
            rejected = ["network_graph", "chord_diagram"]
            recommendation = "sortable_table"
            reasoning = "No relationships exist for network visualization"
        
        elif data_type == "time_series":
            rejected = ["pie_chart", "treemap"]
            recommendation = "line_chart"
            reasoning = "Time series data requires temporal visualization"
        
        else:
            recommendation = "auto_select"
            reasoning = "Using automatic visualization selection"
        
        return {
            "data_type": data_type,
            "rejected_visualizations": rejected,
            "recommendation": recommendation,
            "reasoning": reasoning,
            "confidence": 0.85
        }
    
    def save_log(self, filename: str = None):
        """Save execution log to file"""
        if not filename:
            filename = f"interaction_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as f:
            f.write("Interaction Execution Log\n")
            f.write("=" * 50 + "\n\n")
            for entry in self.execution_log:
                f.write(entry + "\n")
        
        print(f"\n📝 Log saved to: {filename}")


async def interactive_mode():
    """Interactive mode for testing interactions"""
    runner = InteractionRunner(verbose=True)
    
    print("\n🎮 Interactive Interaction Runner")
    print("=" * 50)
    print("\nAvailable interactions:")
    print("1. arxiv_search - Search ArXiv papers")
    print("2. youtube_search - Search YouTube videos")
    print("3. paper_to_knowledge - Paper analysis pipeline")
    print("4. multi_source_research - Parallel research")
    print("5. visualization_decision - Intelligent viz selection")
    print("6. self_improvement_cycle - Self-evolution demo")
    print("0. Exit")
    
    while True:
        print("\n" + "-" * 30)
        choice = input("Select interaction (0-6): ")
        
        if choice == "0":
            break
        
        elif choice == "1":
            query = input("Enter search query [machine learning]: ").strip()
            if not query:
                query = "machine learning"
            await runner.run_interaction("arxiv_search", query=query)
        
        elif choice == "2":
            query = input("Enter search query [python tutorial]: ").strip()
            if not query:
                query = "python tutorial"
            await runner.run_interaction("youtube_search", query=query)
        
        elif choice == "3":
            topic = input("Enter topic [transformers]: ").strip()
            if not topic:
                topic = "transformers"
            await runner.run_interaction("paper_to_knowledge", topic=topic)
        
        elif choice == "4":
            topic = input("Enter topic [machine learning]: ").strip()
            if not topic:
                topic = "machine learning"
            await runner.run_interaction("multi_source_research", topic=topic)
        
        elif choice == "5":
            print("\nDescribe your data:")
            data_type = input("Data type [sparse_matrix]: ").strip() or "sparse_matrix"
            dims = input("Dimensions (comma-separated) [1000,50]: ").strip() or "1000,50"
            sparsity = float(input("Sparsity (0-1) [0.95]: ").strip() or "0.95")
            
            data_desc = {
                "type": data_type,
                "dimensions": [int(d) for d in dims.split(",")],
                "sparsity": sparsity
            }
            await runner.run_interaction("visualization_decision", data_description=data_desc)
        
        elif choice == "6":
            module = input("Target module [visualization_optimizer]: ").strip()
            if not module:
                module = "visualization_optimizer"
            await runner.run_interaction("self_improvement_cycle", target_module=module)
        
        else:
            print("Invalid choice")
    
    save = input("\nSave execution log? (y/n): ")
    if save.lower() == 'y':
        runner.save_log()


async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run module interactions")
    parser.add_argument("interaction", nargs="?", 
                       help="Interaction to run (or 'interactive' for menu)")
    parser.add_argument("--query", type=str, default="machine learning",
                       help="Search query")
    parser.add_argument("--topic", type=str, default="transformers",
                       help="Research topic")
    parser.add_argument("--save-log", action="store_true",
                       help="Save execution log")
    
    args = parser.parse_args()
    
    if not args.interaction or args.interaction == "interactive":
        await interactive_mode()
    else:
        runner = InteractionRunner(verbose=True)
        
        result = await runner.run_interaction(
            args.interaction,
            query=args.query,
            topic=args.topic
        )
        
        if result:
            print("\n📊 Result:")
            print(json.dumps(result, indent=2))
        
        if args.save_log:
            runner.save_log()


if __name__ == "__main__":
    asyncio.run(main())