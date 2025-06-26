#!/usr/bin/env python3
"""
Schema Negotiation and Adaptive Pipeline Scenario
Modules discover each other's schemas and negotiate data formats
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import jsonschema
from jsonschema import validate, ValidationError

class SchemaNegotiationScenario:
    """
    A scenario where modules:
    1. Discover each other's input/output schemas
    2. Negotiate compatible data formats
    3. Build adaptive pipelines
    4. Transform data between formats
    5. Learn from usage patterns
    """
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.schema_mappings = {}
        self.transformation_rules = {}
        self.pipeline_history = []
        self.compatibility_matrix = {}
    
    async def run(self):
        """Run the schema negotiation scenario"""
        print("🤝 Starting Schema Negotiation and Adaptive Pipeline")
        print("="*60)
        
        # Phase 1: Module Discovery
        modules = await self._discover_modules()
        
        # Phase 2: Schema Analysis
        await self._analyze_schemas(modules)
        
        # Phase 3: Build Compatibility Matrix
        self._build_compatibility_matrix(modules)
        
        # Phase 4: Demonstrate Adaptive Pipelines
        await self._demonstrate_adaptive_pipelines()
        
        # Phase 5: Schema Evolution
        await self._demonstrate_schema_evolution()
        
        # Generate report
        await self._generate_negotiation_report()
    
    async def _discover_modules(self) -> List[Dict[str, Any]]:
        """Discover available modules and their capabilities"""
        print("\n🔍 Discovering modules and capabilities...")
        
        # In a real implementation, this would query the registry
        modules = [
            {
                "name": "arxiv-mcp-server",
                "capabilities": [{
                    "name": "search_papers",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "max_results": {"type": "integer", "default": 10}
                        },
                        "required": ["query"]
                    },
                    "output_schema": {
                        "type": "object",
                        "properties": {
                            "papers": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "title": {"type": "string"},
                                        "abstract": {"type": "string"},
                                        "pdf_url": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }]
            },
            {
                "name": "marker",
                "capabilities": [{
                    "name": "extract_text",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string"},
                            "format": {"type": "string", "enum": ["pdf", "docx"]}
                        },
                        "required": ["file_path"]
                    },
                    "output_schema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "metadata": {"type": "object"}
                        }
                    }
                }]
            },
            {
                "name": "youtube_transcripts",
                "capabilities": [{
                    "name": "analyze_content",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "transcript": {"type": "string"}
                        },
                        "required": ["transcript"]
                    },
                    "output_schema": {
                        "type": "object",
                        "properties": {
                            "topics": {"type": "array", "items": {"type": "string"}},
                            "summary": {"type": "string"}
                        }
                    }
                }]
            }
        ]
        
        print(f"  ✅ Discovered {len(modules)} modules")
        for module in modules:
            print(f"     • {module['name']}: {len(module['capabilities'])} capabilities")
        
        return modules
    
    async def _analyze_schemas(self, modules: List[Dict[str, Any]]):
        """Analyze schemas for each module"""
        print("\n📋 Analyzing schemas...")
        
        for module in modules:
            module_name = module["name"]
            self.schema_mappings[module_name] = {}
            
            for capability in module["capabilities"]:
                cap_name = capability["name"]
                
                # Analyze input schema
                input_fields = self._extract_fields(capability["input_schema"])
                output_fields = self._extract_fields(capability["output_schema"])
                
                self.schema_mappings[module_name][cap_name] = {
                    "input_fields": input_fields,
                    "output_fields": output_fields,
                    "input_schema": capability["input_schema"],
                    "output_schema": capability["output_schema"]
                }
                
                print(f"\n  📌 {module_name}.{cap_name}:")
                print(f"     Input fields: {', '.join(input_fields)}")
                print(f"     Output fields: {', '.join(output_fields)}")
    
    def _extract_fields(self, schema: Dict[str, Any], prefix: str = "") -> List[str]:
        """Extract field names from a JSON schema"""
        fields = []
        
        if schema.get("type") == "object" and "properties" in schema:
            for prop_name, prop_schema in schema["properties"].items():
                field_path = f"{prefix}.{prop_name}" if prefix else prop_name
                fields.append(field_path)
                
                # Recurse for nested objects
                if prop_schema.get("type") == "object":
                    fields.extend(self._extract_fields(prop_schema, field_path))
        
        return fields
    
    def _build_compatibility_matrix(self, modules: List[Dict[str, Any]]):
        """Build compatibility matrix between modules"""
        print("\n🔗 Building compatibility matrix...")
        
        # Check which modules can connect to each other
        for source_module in modules:
            source_name = source_module["name"]
            self.compatibility_matrix[source_name] = {}
            
            for source_cap in source_module["capabilities"]:
                source_cap_name = source_cap["name"]
                compatible_targets = []
                
                # Get output schema of source
                source_output = self.schema_mappings[source_name][source_cap_name]["output_fields"]
                
                # Check compatibility with all other modules
                for target_module in modules:
                    if target_module["name"] == source_name:
                        continue
                    
                    for target_cap in target_module["capabilities"]:
                        target_cap_name = target_cap["name"]
                        target_input = self.schema_mappings[target_module["name"]][target_cap_name]["input_fields"]
                        
                        # Check if any output field matches any input field
                        compatibility_score = self._calculate_compatibility(
                            source_output, target_input,
                            source_cap["output_schema"],
                            target_cap["input_schema"]
                        )
                        
                        if compatibility_score > 0:
                            compatible_targets.append({
                                "module": target_module["name"],
                                "capability": target_cap_name,
                                "score": compatibility_score,
                                "transformations_needed": compatibility_score < 1.0
                            })
                
                self.compatibility_matrix[source_name][source_cap_name] = compatible_targets
        
        # Display compatibility matrix
        print("\n  📊 Compatibility Matrix:")
        for source, capabilities in self.compatibility_matrix.items():
            for cap, targets in capabilities.items():
                if targets:
                    print(f"\n  {source}.{cap} can connect to:")
                    for target in targets:
                        transform = " (needs transformation)" if target["transformations_needed"] else ""
                        print(f"    → {target['module']}.{target['capability']} (score: {target['score']:.2f}){transform}")
    
    def _calculate_compatibility(self, source_fields: List[str], target_fields: List[str],
                                source_schema: Dict, target_schema: Dict) -> float:
        """Calculate compatibility score between schemas"""
        # Direct field matches
        direct_matches = set(source_fields) & set(target_fields)
        if direct_matches:
            return 1.0
        
        # Check for compatible types
        compatibility_score = 0.0
        
        # Special cases
        if "text" in source_fields and "transcript" in target_fields:
            compatibility_score = 0.8  # Can rename field
        elif "pdf_url" in source_fields and "file_path" in target_fields:
            compatibility_score = 0.9  # Direct mapping
        elif "papers" in source_fields and "file_path" in target_fields:
            compatibility_score = 0.7  # Need to extract URL from array
        
        return compatibility_score
    
    async def _demonstrate_adaptive_pipelines(self):
        """Demonstrate adaptive pipeline creation"""
        print("\n\n🔄 Demonstrating Adaptive Pipelines")
        print("="*40)
        
        # Example 1: Research to Analysis Pipeline
        await self._create_adaptive_pipeline(
            "Research Paper Analysis",
            [
                ("arxiv-mcp-server", "search_papers", {"query": "transformer architectures"}),
                ("marker", "extract_text", {"$adaptive": True}),  # Will adapt input
                ("youtube_transcripts", "analyze_content", {"$adaptive": True})
            ]
        )
        
        # Example 2: Multi-source Analysis
        await self._create_adaptive_pipeline(
            "Multi-Source Knowledge Integration",
            [
                ("youtube_transcripts", "extract_transcript", {"video_url": "https://youtube.com/watch?v=example"}),
                ("youtube_transcripts", "analyze_content", {"$adaptive": True}),
                ("arangodb", "create_knowledge_graph", {"$adaptive": True})
            ]
        )
    
    async def _create_adaptive_pipeline(self, name: str, steps: List[Tuple[str, str, Dict]]):
        """Create and execute an adaptive pipeline"""
        print(f"\n📐 Creating pipeline: {name}")
        
        pipeline = {
            "name": name,
            "steps": [],
            "transformations": [],
            "execution_log": []
        }
        
        # Build pipeline with transformations
        for i, (module, capability, input_data) in enumerate(steps):
            step = {
                "step": i + 1,
                "module": module,
                "capability": capability,
                "input": input_data
            }
            
            if i > 0 and input_data.get("$adaptive"):
                # Need to adapt from previous step
                prev_module = steps[i-1][0]
                prev_capability = steps[i-1][1]
                
                # Find transformation
                transformation = self._create_transformation(
                    prev_module, prev_capability,
                    module, capability
                )
                
                if transformation:
                    step["transformation"] = transformation
                    pipeline["transformations"].append(transformation)
                    print(f"  🔄 Step {i+1}: {module}.{capability} (with transformation)")
                else:
                    print(f"  ✅ Step {i+1}: {module}.{capability} (direct connection)")
            else:
                print(f"  ✅ Step {i+1}: {module}.{capability}")
            
            pipeline["steps"].append(step)
        
        # Execute pipeline (mock)
        await self._execute_adaptive_pipeline(pipeline)
        
        self.pipeline_history.append(pipeline)
    
    def _create_transformation(self, source_module: str, source_cap: str,
                              target_module: str, target_cap: str) -> Optional[Dict]:
        """Create transformation rules between modules"""
        # Get schemas
        source_output = self.schema_mappings[source_module][source_cap]["output_schema"]
        target_input = self.schema_mappings[target_module][target_cap]["input_schema"]
        
        transformation = {
            "from": f"{source_module}.{source_cap}",
            "to": f"{target_module}.{target_cap}",
            "rules": []
        }
        
        # Define transformation rules based on known patterns
        if source_cap == "search_papers" and target_cap == "extract_text":
            transformation["rules"] = [
                {
                    "type": "extract_field",
                    "from": "papers[0].pdf_url",
                    "to": "file_path"
                },
                {
                    "type": "set_value",
                    "field": "format",
                    "value": "pdf"
                }
            ]
        elif source_cap == "extract_text" and target_cap == "analyze_content":
            transformation["rules"] = [
                {
                    "type": "rename_field",
                    "from": "text",
                    "to": "transcript"
                }
            ]
        elif source_cap == "analyze_content" and target_module == "arangodb":
            transformation["rules"] = [
                {
                    "type": "transform_array",
                    "from": "topics",
                    "to": "nodes",
                    "template": {"id": "${item}", "type": "concept", "name": "${item}"}
                },
                {
                    "type": "generate_edges",
                    "based_on": "topics",
                    "pattern": "sequential"
                }
            ]
        
        return transformation if transformation["rules"] else None
    
    async def _execute_adaptive_pipeline(self, pipeline: Dict):
        """Execute an adaptive pipeline with transformations"""
        print(f"\n▶️  Executing pipeline: {pipeline['name']}")
        
        current_data = None
        
        for step in pipeline["steps"]:
            print(f"\n  Step {step['step']}: {step['module']}.{step['capability']}")
            
            # Apply transformation if needed
            if "transformation" in step and current_data:
                print(f"    🔄 Applying transformation...")
                transformed_data = self._apply_transformation(
                    current_data, 
                    step["transformation"]
                )
                print(f"    ✅ Data transformed successfully")
                
                # Show transformation
                print(f"    📊 Transformation preview:")
                print(f"       Before: {json.dumps(current_data, indent=8)[:100]}...")
                print(f"       After: {json.dumps(transformed_data, indent=8)[:100]}...")
            else:
                transformed_data = step["input"]
            
            # Execute step (mock)
            result = await self._mock_execute_step(
                step["module"], 
                step["capability"],
                transformed_data
            )
            
            current_data = result
            
            # Log execution
            pipeline["execution_log"].append({
                "step": step["step"],
                "timestamp": datetime.now().isoformat(),
                "input": transformed_data,
                "output": result
            })
        
        print(f"\n✅ Pipeline execution complete")
        return current_data
    
    def _apply_transformation(self, data: Dict, transformation: Dict) -> Dict:
        """Apply transformation rules to data"""
        result = {}
        
        for rule in transformation["rules"]:
            if rule["type"] == "extract_field":
                # Extract nested field
                value = self._get_nested_value(data, rule["from"])
                result[rule["to"]] = value
            
            elif rule["type"] == "rename_field":
                # Simple rename
                if rule["from"] in data:
                    result[rule["to"]] = data[rule["from"]]
            
            elif rule["type"] == "set_value":
                # Set a constant value
                result[rule["field"]] = rule["value"]
            
            elif rule["type"] == "transform_array":
                # Transform array elements
                source_array = data.get(rule["from"], [])
                transformed = []
                for item in source_array:
                    transformed_item = {}
                    for key, template in rule["template"].items():
                        if "${item}" in template:
                            transformed_item[key] = template.replace("${item}", str(item))
                        else:
                            transformed_item[key] = template
                    transformed.append(transformed_item)
                result[rule["to"]] = transformed
            
            elif rule["type"] == "generate_edges":
                # Generate edges from array
                source_array = data.get(rule["based_on"], [])
                edges = []
                if rule["pattern"] == "sequential":
                    for i in range(len(source_array) - 1):
                        edges.append({
                            "from": f"concept_{source_array[i]}",
                            "to": f"concept_{source_array[i+1]}",
                            "type": "related_to"
                        })
                result["edges"] = edges
        
        return result
    
    def _get_nested_value(self, data: Dict, path: str) -> Any:
        """Get value from nested path like 'papers[0].pdf_url'"""
        parts = path.replace("]", "").split("[")
        current = data
        
        for part in parts:
            if "." in part:
                keys = part.split(".")
                for key in keys:
                    if key and isinstance(current, dict):
                        current = current.get(key)
            elif part.isdigit() and isinstance(current, list):
                index = int(part)
                if index < len(current):
                    current = current[index]
            elif isinstance(current, dict):
                current = current.get(part)
        
        return current
    
    async def _mock_execute_step(self, module: str, capability: str, 
                                input_data: Dict) -> Dict:
        """Mock execution of a module capability"""
        await asyncio.sleep(0.5)  # Simulate processing
        
        # Return mock data based on module/capability
        if module == "arxiv-mcp-server" and capability == "search_papers":
            return {
                "papers": [
                    {
                        "id": "2017.03456",
                        "title": "Attention Is All You Need",
                        "abstract": "The dominant sequence transduction models...",
                        "pdf_url": "https://arxiv.org/pdf/1706.03762.pdf"
                    }
                ]
            }
        elif module == "marker" and capability == "extract_text":
            return {
                "text": "Abstract: This paper introduces transformer architecture...",
                "metadata": {"pages": 12, "language": "en"}
            }
        elif module == "youtube_transcripts" and capability == "analyze_content":
            return {
                "topics": ["transformer", "attention", "neural networks", "NLP"],
                "summary": "This paper introduces the transformer architecture..."
            }
        else:
            return {"status": "executed", "module": module, "capability": capability}
    
    async def _demonstrate_schema_evolution(self):
        """Demonstrate how schemas can evolve based on usage"""
        print("\n\n🧬 Demonstrating Schema Evolution")
        print("="*40)
        
        # Analyze pipeline history for common transformations
        transformation_frequency = {}
        for pipeline in self.pipeline_history:
            for transformation in pipeline.get("transformations", []):
                key = f"{transformation['from']} -> {transformation['to']}"
                transformation_frequency[key] = transformation_frequency.get(key, 0) + 1
        
        print("\n📊 Transformation Usage Analysis:")
        for transform, count in transformation_frequency.items():
            print(f"  • {transform}: used {count} times")
        
        # Suggest schema improvements
        print("\n💡 Schema Evolution Suggestions:")
        
        if transformation_frequency:
            most_common = max(transformation_frequency.items(), key=lambda x: x[1])
            transform_key, usage_count = most_common
            
            print(f"\n  🔄 Most common transformation: {transform_key}")
            print(f"     Used {usage_count} times")
            print("\n  📝 Suggestion: Consider adding adapter module or updating schemas:")
            print(f"     • Option 1: Create adapter module for this transformation")
            print(f"     • Option 2: Update output schema to match common usage")
            print(f"     • Option 3: Add optional compatibility mode")
    
    async def _generate_negotiation_report(self):
        """Generate comprehensive report on schema negotiations"""
        print("\n\n" + "="*60)
        print("📊 SCHEMA NEGOTIATION SUMMARY")
        print("="*60)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "modules_analyzed": len(self.schema_mappings),
            "compatibility_pairs": sum(
                len(targets) for caps in self.compatibility_matrix.values() 
                for targets in caps.values()
            ),
            "pipelines_created": len(self.pipeline_history),
            "transformations_used": sum(
                len(p.get("transformations", [])) for p in self.pipeline_history
            ),
            "schema_mappings": self.schema_mappings,
            "compatibility_matrix": self.compatibility_matrix,
            "pipeline_history": self.pipeline_history
        }
        
        # Save report
        output_dir = Path("./reports")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = output_dir / f"schema_negotiation_report_{timestamp}.json"
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📈 Key Findings:")
        print(f"  • Modules analyzed: {report['modules_analyzed']}")
        print(f"  • Compatible connections: {report['compatibility_pairs']}")
        print(f"  • Adaptive pipelines created: {report['pipelines_created']}")
        print(f"  • Transformations applied: {report['transformations_used']}")
        
        print(f"\n🔗 Top Compatible Pairs:")
        for source, capabilities in self.compatibility_matrix.items():
            for cap, targets in capabilities.items():
                for target in targets[:2]:  # Top 2 targets
                    print(f"  • {source}.{cap} → {target['module']}.{target['capability']} (score: {target['score']:.2f})")
        
        print(f"\n📁 Full report saved to: {report_path}")

# Example usage
async def main():
    """Run the schema negotiation scenario"""
    from orchestrator.task_orchestrator import ConversationalOrchestrator
    
    async with ConversationalOrchestrator() as orchestrator:
        scenario = SchemaNegotiationScenario(orchestrator)
        await scenario.run()

if __name__ == "__main__":
    asyncio.run(main())