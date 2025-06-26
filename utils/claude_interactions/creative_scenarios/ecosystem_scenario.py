#!/usr/bin/env python3
"""
The Ecosystem - Symbiotic Module Relationships
Modules form an ecosystem where they produce and consume resources from each other
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, List
import random

class EcosystemScenario:
    """
    Modules act as organisms in an ecosystem, producing resources that others consume,
    creating feedback loops and emergent behaviors
    """
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.ecosystem_state = {
            "resources": {
                "knowledge": 100,
                "data": 100,
                "compute": 100,
                "insights": 0
            },
            "organisms": {},
            "cycles_completed": 0,
            "symbiotic_relationships": []
        }
    
    async def run(self, cycles: int = 3):
        """Run the ecosystem simulation"""
        print(f"\n🌳 THE ECOSYSTEM: Symbiotic Module Interactions")
        print("=" * 70)
        
        # Initialize organisms
        await self._initialize_organisms()
        
        # Run ecosystem cycles
        for cycle in range(cycles):
            print(f"\n🔄 Ecosystem Cycle {cycle + 1}")
            print("-" * 50)
            await self._run_ecosystem_cycle(cycle)
            
        # Analyze ecosystem health
        await self._analyze_ecosystem_health()
        
        self._print_ecosystem_report()
    
    async def _initialize_organisms(self):
        """Initialize modules as ecosystem organisms"""
        print("\n🌱 Initializing Ecosystem Organisms")
        
        self.ecosystem_state["organisms"] = {
            "arxiv_producer": {
                "type": "producer",
                "produces": "knowledge",
                "consumes": "compute",
                "health": 100
            },
            "youtube_decomposer": {
                "type": "decomposer",
                "produces": "data",
                "consumes": "knowledge",
                "health": 100
            },
            "marker_processor": {
                "type": "processor",
                "produces": "structured_data",
                "consumes": "data",
                "health": 100
            },
            "sparta_predator": {
                "type": "predator",
                "produces": "models",
                "consumes": "structured_data",
                "health": 100
            },
            "claude_apex": {
                "type": "apex_predator",
                "produces": "insights",
                "consumes": "models",
                "health": 100
            },
            "arangodb_environment": {
                "type": "environment",
                "maintains": "all_resources",
                "health": 100
            }
        }
        
        # Define symbiotic relationships
        self.ecosystem_state["symbiotic_relationships"] = [
            ("arxiv_producer", "youtube_decomposer", "mutualism"),
            ("marker_processor", "sparta_predator", "commensalism"),
            ("claude_apex", "arangodb_environment", "mutualism")
        ]
        
        print("  🦋 ArXiv Producer: Generates knowledge from research")
        print("  🐛 YouTube Decomposer: Breaks down knowledge into data")
        print("  🐝 Marker Processor: Transforms raw data")
        print("  🦅 Sparta Predator: Hunts patterns in data")
        print("  🦁 Claude Apex: Top of the food chain")
        print("  🌍 ArangoDB Environment: Maintains ecosystem balance")
    
    async def _run_ecosystem_cycle(self, cycle_num: int):
        """Run one ecosystem cycle"""
        
        task = self.orchestrator.create_task(
            name=f"Ecosystem Cycle {cycle_num + 1}",
            description="Organisms interact and exchange resources"
        )
        
        # Producer Phase: ArXiv generates knowledge
        if self.ecosystem_state["resources"]["compute"] > 20:
            print("\n  🌱 Producer Phase")
            self.orchestrator.add_step(
                task,
                module="arxiv-mcp-server",
                capability="search_papers",
                input_data={
                    "query": "ecosystem dynamics complex systems",
                    "max_results": 3
                },
                metadata={"organism": "arxiv_producer", "phase": "production"}
            )
            self.ecosystem_state["resources"]["compute"] -= 20
            self.ecosystem_state["resources"]["knowledge"] += 30
            print(f"    Knowledge produced: +30 (total: {self.ecosystem_state['resources']['knowledge']})")
        
        # Decomposer Phase: YouTube breaks down knowledge
        if self.ecosystem_state["resources"]["knowledge"] > 30:
            print("\n  🍄 Decomposer Phase")
            self.orchestrator.add_step(
                task,
                module="youtube_transcripts",
                capability="analyze_content",
                input_data={
                    "content": ".papers[0].abstract",
                    "extract_topics": True
                },
                metadata={"organism": "youtube_decomposer", "phase": "decomposition"}
            )
            self.ecosystem_state["resources"]["knowledge"] -= 30
            self.ecosystem_state["resources"]["data"] += 40
            print(f"    Data decomposed: +40 (total: {self.ecosystem_state['resources']['data']})")
        
        # Processor Phase: Marker processes data
        if self.ecosystem_state["resources"]["data"] > 25:
            print("\n  🐝 Processor Phase")
            self.orchestrator.add_step(
                task,
                module="marker",
                capability="extract_text",
                input_data={
                    "content": ".topics",
                    "format": "structured"
                },
                metadata={"organism": "marker_processor", "phase": "processing"}
            )
            self.ecosystem_state["resources"]["data"] -= 25
            
        # Predator Phase: Sparta hunts patterns
        print("\n  🦅 Predator Phase")
        self.orchestrator.add_step(
            task,
            module="sparta",
            capability="train_model",
            input_data={
                "dataset": ".structured_data",
                "model_type": "pattern_hunter",
                "epochs": 5
            },
            metadata={"organism": "sparta_predator", "phase": "hunting"}
        )
        
        # Apex Predator Phase: Claude generates insights
        print("\n  🦁 Apex Predator Phase")
        self.orchestrator.add_step(
            task,
            module="claude_max_proxy",
            capability="generate_insights",
            input_data={
                "model_patterns": ".patterns",
                "ecosystem_state": self.ecosystem_state,
                "insight_type": "emergent_behavior"
            },
            metadata={"organism": "claude_apex", "phase": "insight_generation"}
        )
        
        # Environment Phase: ArangoDB maintains balance
        print("\n  🌍 Environment Maintenance")
        self.orchestrator.add_step(
            task,
            module="arangodb",
            capability="update_graph",
            input_data={
                "ecosystem_snapshot": {
                    "cycle": cycle_num + 1,
                    "resources": self.ecosystem_state["resources"],
                    "organism_health": {k: v["health"] for k, v in self.ecosystem_state["organisms"].items()},
                    "insights": ".insights"
                }
            },
            metadata={"organism": "arangodb_environment", "phase": "maintenance"}
        )
        
        # Execute ecosystem cycle
        result = await self.orchestrator.execute_task(task.id)
        
        # Apply symbiotic effects
        await self._apply_symbiotic_effects(result)
        
        # Random events
        await self._random_ecosystem_event()
        
        self.ecosystem_state["cycles_completed"] += 1
        self.ecosystem_state["resources"]["insights"] += 10
        
        # Update organism health based on resource availability
        self._update_organism_health()
    
    async def _apply_symbiotic_effects(self, cycle_result: Dict[str, Any]):
        """Apply effects of symbiotic relationships"""
        print("\n  🤝 Symbiotic Effects")
        
        for org1, org2, relationship in self.ecosystem_state["symbiotic_relationships"]:
            if relationship == "mutualism":
                # Both organisms benefit
                self.ecosystem_state["organisms"][org1]["health"] += 5
                self.ecosystem_state["organisms"][org2]["health"] += 5
                print(f"    💚 {org1} ↔️ {org2}: Mutual benefit (+5 health each)")
            
            elif relationship == "commensalism":
                # One benefits, other unaffected
                self.ecosystem_state["organisms"][org2]["health"] += 3
                print(f"    💙 {org1} → {org2}: {org2} benefits (+3 health)")
    
    async def _random_ecosystem_event(self):
        """Random events that affect the ecosystem"""
        event = random.choice([
            "resource_bloom", "predator_surge", "environmental_stress", 
            "symbiosis_strengthening", "none"
        ])
        
        if event == "resource_bloom":
            print("\n  🌸 Random Event: Resource Bloom!")
            resource = random.choice(list(self.ecosystem_state["resources"].keys()))
            self.ecosystem_state["resources"][resource] += 50
            print(f"    {resource} increased by 50!")
        
        elif event == "predator_surge":
            print("\n  ⚡ Random Event: Predator Surge!")
            self.ecosystem_state["organisms"]["sparta_predator"]["health"] += 20
            self.ecosystem_state["organisms"]["marker_processor"]["health"] -= 10
        
        elif event == "environmental_stress":
            print("\n  🌪️ Random Event: Environmental Stress!")
            for org in self.ecosystem_state["organisms"].values():
                org["health"] -= 5
    
    def _update_organism_health(self):
        """Update organism health based on resources"""
        for name, org in self.ecosystem_state["organisms"].items():
            # Organisms need minimum resources to survive
            if org["type"] == "producer" and self.ecosystem_state["resources"]["compute"] < 10:
                org["health"] -= 10
            elif org["type"] == "decomposer" and self.ecosystem_state["resources"]["knowledge"] < 10:
                org["health"] -= 10
            
            # Cap health at 100
            org["health"] = min(100, max(0, org["health"]))
    
    async def _analyze_ecosystem_health(self):
        """Analyze overall ecosystem health"""
        print("\n🔬 Analyzing Ecosystem Health")
        
        task = self.orchestrator.create_task(
            name="Ecosystem Health Analysis",
            description="Comprehensive ecosystem assessment"
        )
        
        # Generate ecosystem report
        self.orchestrator.add_step(
            task,
            module="claude-test-reporter",
            capability="generate_report",
            input_data={
                "ecosystem_data": self.ecosystem_state,
                "report_type": "ecosystem_health",
                "metrics": [
                    "biodiversity", "resource_efficiency", 
                    "symbiotic_strength", "resilience"
                ]
            }
        )
        
        result = await self.orchestrator.execute_task(task.id)
        self.ecosystem_state["health_report"] = result["outputs"].get("step_1", {})
    
    def _print_ecosystem_report(self):
        """Print ecosystem summary"""
        print("\n📊 ECOSYSTEM REPORT")
        print("=" * 60)
        print(f"Cycles Completed: {self.ecosystem_state['cycles_completed']}")
        
        print("\nResource Levels:")
        for resource, amount in self.ecosystem_state["resources"].items():
            bar = "█" * (amount // 10) + "░" * (10 - amount // 10)
            print(f"  {resource:15} [{bar}] {amount}")
        
        print("\nOrganism Health:")
        for name, org in self.ecosystem_state["organisms"].items():
            health_bar = "❤️" * (org["health"] // 20) + "🖤" * (5 - org["health"] // 20)
            print(f"  {name:20} {health_bar} {org['health']}%")
        
        print("\nSymbiotic Relationships:")
        for org1, org2, rel_type in self.ecosystem_state["symbiotic_relationships"]:
            symbol = "↔️" if rel_type == "mutualism" else "→"
            print(f"  {org1} {symbol} {org2}: {rel_type}")
        
        print("\nEcosystem Insights:")
        print(f"  Total Insights Generated: {self.ecosystem_state['resources']['insights']}")
        print("  Ecosystem Status: ", end="")
        
        avg_health = sum(org["health"] for org in self.ecosystem_state["organisms"].values()) / len(self.ecosystem_state["organisms"])
        if avg_health > 80:
            print("🌟 Thriving")
        elif avg_health > 60:
            print("✅ Stable")
        elif avg_health > 40:
            print("⚠️ Stressed")
        else:
            print("❌ Collapsing")
