#!/usr/bin/env python3
"""
Module Discovery and Registration Service
Allows modules to register their capabilities and discover each other
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import aiohttp
from aiohttp import web

@dataclass
class ModuleCapability:
    """Represents a capability that a module provides"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    examples: List[Dict[str, Any]] = None
    constraints: Dict[str, Any] = None

@dataclass
class RegisteredModule:
    """Represents a registered module in the ecosystem"""
    name: str
    path: str
    type: str  # framework, tool, database, mcp, etc.
    version: str
    capabilities: List[ModuleCapability]
    dependencies: List[str]
    endpoints: Dict[str, str]  # API endpoints, CLI commands, etc.
    status: str = "active"
    last_seen: str = None
    metadata: Dict[str, Any] = None

class ModuleRegistry:
    """Central registry for all modules"""
    
    def __init__(self):
        self.modules: Dict[str, RegisteredModule] = {}
        self.capabilities_index: Dict[str, List[str]] = {}  # capability -> [module_names]
        self._initialize_known_modules()
    
    def _initialize_known_modules(self):
        """Pre-register known modules with their capabilities"""
        
        # Sparta - ML Framework
        self.register_module(RegisteredModule(
            name="sparta",
            path="/home/graham/workspace/experiments/sparta/",
            type="framework",
            version="1.0.0",
            capabilities=[
                ModuleCapability(
                    name="train_model",
                    description="Train ML models with various architectures",
                    input_schema={
                        "type": "object",
                        "properties": {
                            "dataset": {"type": "string"},
                            "model_type": {"type": "string", "enum": ["transformer", "cnn", "rnn"]},
                            "config": {"type": "object"}
                        }
                    },
                    output_schema={
                        "type": "object",
                        "properties": {
                            "model_path": {"type": "string"},
                            "metrics": {"type": "object"},
                            "training_history": {"type": "array"}
                        }
                    }
                ),
                ModuleCapability(
                    name="analyze_performance",
                    description="Analyze model performance and suggest improvements",
                    input_schema={"model_path": {"type": "string"}},
                    output_schema={"analysis": {"type": "object"}}
                )
            ],
            dependencies=["torch", "transformers"],
            endpoints={
                "cli": "sparta",
                "api": "http://localhost:8001",
                "slash": "/sparta"
            }
        ))
        
        # Marker - Document Processing
        self.register_module(RegisteredModule(
            name="marker",
            path="/home/graham/workspace/experiments/marker/",
            type="tool",
            version="1.0.0",
            capabilities=[
                ModuleCapability(
                    name="extract_text",
                    description="Extract text from PDFs and documents",
                    input_schema={
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string"},
                            "format": {"type": "string", "enum": ["pdf", "docx", "html"]}
                        }
                    },
                    output_schema={
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "metadata": {"type": "object"},
                            "structure": {"type": "array"}
                        }
                    }
                ),
                ModuleCapability(
                    name="segment_document",
                    description="Segment documents into logical sections",
                    input_schema={"text": {"type": "string"}},
                    output_schema={"segments": {"type": "array"}}
                )
            ],
            dependencies=["pdfplumber", "pytesseract"],
            endpoints={
                "cli": "marker",
                "api": "http://localhost:8002",
                "slash": "/marker"
            }
        ))
        
        # ArangoDB - Graph Database
        self.register_module(RegisteredModule(
            name="arangodb",
            path="/home/graham/workspace/experiments/arangodb/",
            type="database",
            version="1.0.0",
            capabilities=[
                ModuleCapability(
                    name="create_knowledge_graph",
                    description="Create knowledge graphs from structured data",
                    input_schema={
                        "nodes": {"type": "array"},
                        "edges": {"type": "array"}
                    },
                    output_schema={
                        "graph_id": {"type": "string"},
                        "stats": {"type": "object"}
                    }
                ),
                ModuleCapability(
                    name="query_graph",
                    description="Query knowledge graphs with AQL",
                    input_schema={
                        "graph_id": {"type": "string"},
                        "query": {"type": "string"}
                    },
                    output_schema={"results": {"type": "array"}}
                ),
                ModuleCapability(
                    name="visualize_graph",
                    description="Generate graph visualizations",
                    input_schema={"graph_id": {"type": "string"}},
                    output_schema={"visualization_url": {"type": "string"}}
                )
            ],
            dependencies=["pyarango", "networkx"],
            endpoints={
                "api": "http://localhost:8529",
                "slash": "/arangodb"
            }
        ))
        
        # YouTube Transcripts
        self.register_module(RegisteredModule(
            name="youtube_transcripts",
            path="/home/graham/workspace/experiments/youtube_transcripts/",
            type="tool",
            version="1.0.0",
            capabilities=[
                ModuleCapability(
                    name="extract_transcript",
                    description="Extract transcripts from YouTube videos",
                    input_schema={
                        "video_url": {"type": "string"},
                        "language": {"type": "string", "default": "en"}
                    },
                    output_schema={
                        "transcript": {"type": "string"},
                        "timestamps": {"type": "array"},
                        "metadata": {"type": "object"}
                    }
                ),
                ModuleCapability(
                    name="analyze_content",
                    description="Analyze video content and extract topics",
                    input_schema={"transcript": {"type": "string"}},
                    output_schema={
                        "topics": {"type": "array"},
                        "summary": {"type": "string"},
                        "sentiment": {"type": "object"}
                    }
                )
            ],
            dependencies=["youtube_dl", "whisper"],
            endpoints={
                "cli": "yt_transcripts",
                "slash": "/youtube"
            }
        ))
        
        # ArXiv MCP Server
        self.register_module(RegisteredModule(
            name="arxiv-mcp-server",
            path="/home/graham/workspace/mcp-servers/arxiv-mcp-server/",
            type="mcp",
            version="1.0.0",
            capabilities=[
                ModuleCapability(
                    name="search_papers",
                    description="Search academic papers on ArXiv",
                    input_schema={
                        "query": {"type": "string"},
                        "max_results": {"type": "integer", "default": 10}
                    },
                    output_schema={
                        "papers": {"type": "array"},
                        "total": {"type": "integer"}
                    }
                ),
                ModuleCapability(
                    name="get_paper_details",
                    description="Get detailed information about a paper",
                    input_schema={"paper_id": {"type": "string"}},
                    output_schema={
                        "title": {"type": "string"},
                        "abstract": {"type": "string"},
                        "authors": {"type": "array"},
                        "pdf_url": {"type": "string"}
                    }
                )
            ],
            dependencies=["arxiv"],
            endpoints={
                "mcp": "arxiv-server",
                "slash": "/arxiv"
            }
        ))
        
        # MCP Screenshot
        self.register_module(RegisteredModule(
            name="mcp-screenshot",
            path="/home/graham/workspace/experiments/mcp-screenshot/",
            type="mcp",
            version="1.0.0",
            capabilities=[
                ModuleCapability(
                    name="capture_screenshot",
                    description="Capture screenshots of applications or web pages",
                    input_schema={
                        "target": {"type": "string"},
                        "selector": {"type": "string", "optional": True}
                    },
                    output_schema={
                        "image_path": {"type": "string"},
                        "dimensions": {"type": "object"}
                    }
                ),
                ModuleCapability(
                    name="analyze_ui",
                    description="Analyze UI elements in screenshots",
                    input_schema={"image_path": {"type": "string"}},
                    output_schema={
                        "elements": {"type": "array"},
                        "layout": {"type": "object"},
                        "accessibility_issues": {"type": "array"}
                    }
                )
            ],
            dependencies=["PIL", "screenshot"],
            endpoints={
                "mcp": "screenshot-server",
                "slash": "/screenshot"
            }
        ))
        
        # Claude Test Reporter
        self.register_module(RegisteredModule(
            name="claude-test-reporter",
            path="/home/graham/workspace/experiments/claude-test-reporter/",
            type="testing",
            version="1.0.0",
            capabilities=[
                ModuleCapability(
                    name="run_tests",
                    description="Run tests and generate reports",
                    input_schema={
                        "test_path": {"type": "string"},
                        "coverage": {"type": "boolean", "default": True}
                    },
                    output_schema={
                        "passed": {"type": "integer"},
                        "failed": {"type": "integer"},
                        "coverage": {"type": "number"},
                        "report": {"type": "object"}
                    }
                ),
                ModuleCapability(
                    name="generate_test_suggestions",
                    description="Suggest tests based on code analysis",
                    input_schema={"code_path": {"type": "string"}},
                    output_schema={"suggestions": {"type": "array"}}
                )
            ],
            dependencies=["pytest", "coverage"],
            endpoints={
                "cli": "claude-test-reporter",
                "slash": "/test"
            }
        ))
    
    def register_module(self, module: RegisteredModule) -> bool:
        """Register a module with its capabilities"""
        module.last_seen = datetime.now().isoformat()
        self.modules[module.name] = module
        
        # Index capabilities for quick lookup
        for capability in module.capabilities:
            if capability.name not in self.capabilities_index:
                self.capabilities_index[capability.name] = []
            if module.name not in self.capabilities_index[capability.name]:
                self.capabilities_index[capability.name].append(module.name)
        
        return True
    
    def find_modules_by_capability(self, capability_name: str) -> List[RegisteredModule]:
        """Find all modules that provide a specific capability"""
        module_names = self.capabilities_index.get(capability_name, [])
        return [self.modules[name] for name in module_names if name in self.modules]
    
    def find_modules_by_type(self, module_type: str) -> List[RegisteredModule]:
        """Find all modules of a specific type"""
        return [m for m in self.modules.values() if m.type == module_type]
    
    def get_module(self, name: str) -> Optional[RegisteredModule]:
        """Get a specific module by name"""
        return self.modules.get(name)
    
    def get_capability_chain(self, start_capability: str, end_capability: str) -> List[List[str]]:
        """Find possible chains of modules to go from one capability to another"""
        # This is a simplified version - in reality, this would use graph algorithms
        chains = []
        
        # Find modules that provide the start capability
        start_modules = self.find_modules_by_capability(start_capability)
        
        # Find modules that provide the end capability  
        end_modules = self.find_modules_by_capability(end_capability)
        
        # For now, return direct connections
        # TODO: Implement proper graph traversal for multi-step chains
        for start in start_modules:
            for end in end_modules:
                chains.append([start.name, end.name])
        
        return chains
    
    def get_compatible_modules(self, module_name: str) -> List[str]:
        """Find modules that can work with the given module"""
        module = self.get_module(module_name)
        if not module:
            return []
        
        compatible = []
        
        # Find modules that can consume this module's outputs
        for cap in module.capabilities:
            output_schema = cap.output_schema
            
            # Check other modules' input schemas
            for other_name, other_module in self.modules.items():
                if other_name == module_name:
                    continue
                    
                for other_cap in other_module.capabilities:
                    # Simple compatibility check - can be made more sophisticated
                    if self._schemas_compatible(output_schema, other_cap.input_schema):
                        compatible.append(other_name)
                        break
        
        return list(set(compatible))
    
    def _schemas_compatible(self, output_schema: Dict, input_schema: Dict) -> bool:
        """Check if an output schema is compatible with an input schema"""
        # Simplified compatibility check
        # In reality, this would do deep schema validation
        
        if not output_schema or not input_schema:
            return False
            
        # Check if output properties match any input properties
        output_props = output_schema.get('properties', {})
        input_props = input_schema.get('properties', input_schema)
        
        for key in input_props:
            if key in output_props:
                return True
        
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Export registry as dictionary"""
        return {
            "modules": {name: asdict(module) for name, module in self.modules.items()},
            "capabilities_index": self.capabilities_index,
            "timestamp": datetime.now().isoformat()
        }

# Web API for the registry
class RegistryAPI:
    """REST API for the module registry"""
    
    def __init__(self, registry: ModuleRegistry):
        self.registry = registry
        self.app = web.Application()
        self._setup_routes()
    
    def _setup_routes(self):
        self.app.router.add_get('/modules', self.list_modules)
        self.app.router.add_get('/modules/{name}', self.get_module)
        self.app.router.add_post('/modules', self.register_module)
        self.app.router.add_get('/capabilities', self.list_capabilities)
        self.app.router.add_get('/capabilities/{name}/providers', self.get_capability_providers)
        self.app.router.add_get('/discover/{module}/compatible', self.get_compatible_modules)
        self.app.router.add_get('/chain/{start}/{end}', self.get_capability_chain)
    
    async def list_modules(self, request):
        """List all registered modules"""
        modules = [asdict(m) for m in self.registry.modules.values()]
        return web.json_response({"modules": modules})
    
    async def get_module(self, request):
        """Get details of a specific module"""
        name = request.match_info['name']
        module = self.registry.get_module(name)
        if module:
            return web.json_response(asdict(module))
        return web.json_response({"error": "Module not found"}, status=404)
    
    async def register_module(self, request):
        """Register a new module"""
        data = await request.json()
        # TODO: Validate data
        module = RegisteredModule(**data)
        self.registry.register_module(module)
        return web.json_response({"status": "registered", "module": module.name})
    
    async def list_capabilities(self, request):
        """List all available capabilities"""
        return web.json_response({"capabilities": list(self.registry.capabilities_index.keys())})
    
    async def get_capability_providers(self, request):
        """Get modules that provide a capability"""
        capability = request.match_info['name']
        modules = self.registry.find_modules_by_capability(capability)
        return web.json_response({
            "capability": capability,
            "providers": [asdict(m) for m in modules]
        })
    
    async def get_compatible_modules(self, request):
        """Get modules compatible with the given module"""
        module = request.match_info['module']
        compatible = self.registry.get_compatible_modules(module)
        return web.json_response({
            "module": module,
            "compatible": compatible
        })
    
    async def get_capability_chain(self, request):
        """Get possible chains between two capabilities"""
        start = request.match_info['start']
        end = request.match_info['end']
        chains = self.registry.get_capability_chain(start, end)
        return web.json_response({
            "start": start,
            "end": end,
            "chains": chains
        })
    
    def run(self, host='localhost', port=8888):
        """Run the registry API server"""
        web.run_app(self.app, host=host, port=port)

if __name__ == '__main__':
    # Create and populate registry
    registry = ModuleRegistry()
    
    # Start API server
    api = RegistryAPI(registry)
    print("Starting Module Registry API on http://localhost:8888")
    print("Available endpoints:")
    print("  GET  /modules                    - List all modules")
    print("  GET  /modules/{name}             - Get module details")
    print("  POST /modules                    - Register new module")
    print("  GET  /capabilities               - List all capabilities")
    print("  GET  /capabilities/{name}/providers - Get capability providers")
    print("  GET  /discover/{module}/compatible  - Find compatible modules")
    print("  GET  /chain/{start}/{end}        - Find capability chains")
    
    api.run()