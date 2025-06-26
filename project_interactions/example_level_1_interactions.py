
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Example Level 1 Interactions - Two Module Pipelines

This file provides comprehensive examples of Level 1 interactions that demonstrate
how different modules work together in pipelines.

External Dependencies:
- typing: Built-in type annotations
- pathlib: Built-in path handling

Example Usage:
>>> from example_level_1_interactions import ArxivMarkerPipeline
>>> pipeline = ArxivMarkerPipeline()
>>> result = pipeline.run(query="attention mechanisms")
>>> print(f"Converted {result.output_data['pipeline_result']['pages']} pages")
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from interaction_framework import Level1Interaction
import tempfile
import shutil
import json


class ArxivMarkerPipeline(Level1Interaction):
    """ArXiv → Marker: Search, download, and convert papers to Markdown"""
    
    def __init__(self):
        super().__init__(
            "ArXiv to Marker Pipeline",
            "Search for papers and convert to structured Markdown"
        )
        self.temp_dir = None
        
    def initialize_modules(self):
        # Mock modules for demonstration
        arxiv_module = {
            "name": "arxiv",
            "search": lambda q, limit: [
                {"id": "2017.00001", "title": f"Paper about {q}", 
                 "pdf_url": "https://arxiv.org/pdf/2017.00001.pdf"}
            ][:limit],
            "download": lambda url, path: Path(path).write_text("Mock PDF content")
        }
        
        marker_module = {
            "name": "marker",
            "convert": lambda path, **kwargs: {
                "markdown": f"# Converted from {path}\n\nMock content...",
                "metadata": {"pages": 12, "tables": 3},
                "tables": ["Table 1", "Table 2", "Table 3"] if kwargs.get("extract_tables") else []
            }
        }
        
        return arxiv_module, marker_module
        
    def setup(self):
        super().setup()
        self.temp_dir = tempfile.mkdtemp()
        
    def execute_module1(self, **kwargs):
        """Search and download paper from ArXiv"""
        query = kwargs.get("query", "transformer architecture")
        limit = kwargs.get("limit", 1)
        
        # Search for papers
        papers = self.module1["search"](query, limit)
        
        if not papers:
            return None
            
        # Download first paper
        paper = papers[0]
        pdf_path = Path(self.temp_dir) / f"{paper['id']}.pdf"
        self.module1["download"](paper["pdf_url"], pdf_path)
        
        return {
            "paper": paper,
            "pdf_path": str(pdf_path),
            "query": query
        }
        
    def transform_output(self, output1):
        """Transform ArXiv output for Marker input"""
        if not output1:
            return None
        return {
            "pdf_path": output1["pdf_path"],
            "options": {
                "extract_tables": True,
                "ai_enhancement": False,
                "preserve_formatting": True
            }
        }
        
    def execute_module2(self, input_data):
        """Convert PDF to Markdown using Marker"""
        if not input_data:
            return None
            
        result = self.module2["convert"](
            input_data["pdf_path"],
            **input_data["options"]
        )
        
        # Add source info
        result["source_pdf"] = input_data["pdf_path"]
        return result
        
    def validate_output(self, output):
        """Check pipeline succeeded"""
        if not output or "pipeline_result" not in output:
            return False
            
        result = output["pipeline_result"]
        return (
            "markdown" in result and
            len(result["markdown"]) > 0 and
            "metadata" in result
        )
        
    def teardown(self):
        """Clean up temporary files"""
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)


class MarkerArangoDBPipeline(Level1Interaction):
    """Marker → ArangoDB: Extract content and build knowledge graph"""
    
    def __init__(self):
        super().__init__(
            "Marker to ArangoDB Pipeline",
            "Convert document and store as searchable memories"
        )
        
    def initialize_modules(self):
        marker = {
            "convert": lambda path: {
                "markdown": "# Research Paper\n\n## Abstract\nThis paper presents...",
                "metadata": {
                    "title": "Important Research",
                    "authors": ["Author 1", "Author 2"],
                    "topics": ["AI", "Machine Learning"]
                },
                "sections": [
                    {"title": "Introduction", "content": "..."},
                    {"title": "Methods", "content": "..."},
                    {"title": "Results", "content": "..."}
                ]
            }
        }
        
        arangodb = {
            "memories": [],
            "store_memory": lambda m: arangodb["memories"].append(m) or {"id": len(arangodb["memories"])},
            "create_entity": lambda e: {"entity_id": f"entity_{len(arangodb['memories'])}"},
            "create_relationship": lambda r: {"rel_id": f"rel_{len(arangodb['memories'])}"},
            "search": lambda q, limit: arangodb["memories"][:limit]
        }
        
        return marker, arangodb
        
    def execute_module1(self, **kwargs):
        """Extract content from PDF"""
        pdf_path = kwargs.get("pdf_path", "test.pdf")
        return self.module1["convert"](pdf_path)
        
    def transform_output(self, output1):
        """Transform Marker output to ArangoDB memories"""
        if not output1:
            return None
            
        memories = []
        entities = []
        relationships = []
        
        # Document metadata as memory
        memories.append({
            "role": "system",
            "content": f"Document: {output1['metadata']['title']}",
            "metadata": {
                "type": "document_metadata",
                "authors": output1["metadata"].get("authors", []),
                "topics": output1["metadata"].get("topics", [])
            }
        })
        
        # Sections as memories
        for section in output1.get("sections", []):
            memories.append({
                "role": "assistant",
                "content": section["content"],
                "metadata": {
                    "type": "document_section",
                    "section_title": section["title"],
                    "document": output1["metadata"]["title"]
                }
            })
            
        # Extract entities
        for topic in output1["metadata"].get("topics", []):
            entities.append({
                "type": "topic",
                "name": topic,
                "source": "marker_extraction"
            })
            
        for author in output1["metadata"].get("authors", []):
            entities.append({
                "type": "person",
                "name": author,
                "role": "author"
            })
            
        # Create relationships
        doc_entity = {
            "type": "document",
            "name": output1["metadata"]["title"]
        }
        
        for author_entity in [e for e in entities if e["type"] == "person"]:
            relationships.append({
                "from": author_entity,
                "to": doc_entity,
                "type": "authored"
            })
            
        return {
            "memories": memories,
            "entities": entities,
            "relationships": relationships
        }
        
    def execute_module2(self, input_data):
        """Store in ArangoDB"""
        if not input_data:
            return None
            
        results = {
            "stored_memories": [],
            "created_entities": [],
            "created_relationships": []
        }
        
        # Store memories
        for memory in input_data["memories"]:
            result = self.module2["store_memory"](memory)
            results["stored_memories"].append(result)
            
        # Create entities
        for entity in input_data["entities"]:
            result = self.module2["create_entity"](entity)
            results["created_entities"].append(result)
            
        # Create relationships
        for rel in input_data["relationships"]:
            result = self.module2["create_relationship"](rel)
            results["created_relationships"].append(result)
            
        # Test search
        results["search_test"] = self.module2["search"]("research", 5)
        
        return results
        
    def validate_output(self, output):
        """Verify storage succeeded"""
        if not output or "pipeline_result" not in output:
            return False
            
        result = output["pipeline_result"]
        return (
            len(result.get("stored_memories", [])) > 0 and
            len(result.get("created_entities", [])) > 0
        )


class YouTubeSparta Pipeline(Level1Interaction):
    """YouTube → SPARTA: Analyze security content from videos"""
    
    def __init__(self):
        super().__init__(
            "YouTube to SPARTA Pipeline", 
            "Extract security insights from video transcripts"
        )
        
    def initialize_modules(self):
        youtube = {
            "get_transcript": lambda video_id: {
                "video_id": video_id,
                "title": "Cybersecurity Best Practices 2024",
                "transcript": """
                Today we're discussing critical security vulnerabilities.
                First, let's talk about SQL injection attacks.
                These attacks can compromise entire databases.
                Always sanitize user input and use prepared statements.
                Next, cross-site scripting or XSS attacks...
                """,
                "duration": 1200,
                "metadata": {
                    "channel": "SecurityExperts",
                    "views": 50000
                }
            }
        }
        
        sparta = {
            "analyze_security": lambda text: {
                "vulnerabilities_mentioned": [
                    {"type": "SQL Injection", "severity": "high", "cwe": "CWE-89"},
                    {"type": "XSS", "severity": "medium", "cwe": "CWE-79"}
                ],
                "mitigations": [
                    "Input sanitization",
                    "Prepared statements",
                    "Content Security Policy"
                ],
                "compliance_mappings": {
                    "NIST": ["AC-4", "SC-7"],
                    "ISO27001": ["A.14.2.5", "A.13.1.3"]
                },
                "risk_score": 7.5
            }
        }
        
        return youtube, sparta
        
    def execute_module1(self, **kwargs):
        """Get video transcript"""
        video_id = kwargs.get("video_id", "dQw4w9WgXcQ")
        return self.module1["get_transcript"](video_id)
        
    def transform_output(self, output1):
        """Extract text for security analysis"""
        if not output1:
            return None
        return {
            "text": output1["transcript"],
            "context": {
                "source": "youtube",
                "title": output1["title"],
                "video_id": output1["video_id"]
            }
        }
        
    def execute_module2(self, input_data):
        """Analyze security content"""
        if not input_data:
            return None
            
        analysis = self.module2["analyze_security"](input_data["text"])
        analysis["source_context"] = input_data["context"]
        return analysis
        
    def validate_output(self, output):
        """Check analysis completed"""
        if not output or "pipeline_result" not in output:
            return False
            
        result = output["pipeline_result"]
        return (
            "vulnerabilities_mentioned" in result and
            "risk_score" in result and
            result["risk_score"] >= 0
        )


class ScreenshotAnalysisPipeline(Level1Interaction):
    """Any Module → Screenshot: Capture output and analyze visually"""
    
    def __init__(self):
        super().__init__(
            "Visual Analysis Pipeline",
            "Capture module output and analyze with AI"
        )
        
    def initialize_modules(self):
        # Any module that produces visual output
        viz_module = {
            "generate_chart": lambda data: {
                "chart_url": "http://localhost:8080/chart.png",
                "chart_type": "line_graph",
                "data_points": len(data.get("values", [])),
                "title": data.get("title", "Performance Metrics")
            }
        }
        
        screenshot = {
            "capture": lambda url: {
                "screenshot_path": f"/tmp/screenshot_{url.split('/')[-1]}",
                "captured_at": "2024-01-15T10:30:00Z",
                "dimensions": {"width": 1920, "height": 1080}
            },
            "analyze": lambda path: {
                "description": "A line graph showing upward trend over time",
                "detected_elements": [
                    {"type": "chart", "confidence": 0.95},
                    {"type": "legend", "confidence": 0.88},
                    {"type": "axis_labels", "confidence": 0.92}
                ],
                "extracted_text": ["Performance Metrics", "Time", "Value"],
                "insights": [
                    "Positive growth trend observed",
                    "Peak performance at 75% mark",
                    "Consistent improvement over time"
                ]
            }
        }
        
        return viz_module, screenshot
        
    def execute_module1(self, **kwargs):
        """Generate visualization"""
        data = kwargs.get("data", {
            "title": "System Performance",
            "values": [10, 15, 25, 30, 45, 60, 75, 80]
        })
        return self.module1["generate_chart"](data)
        
    def transform_output(self, output1):
        """Get URL for screenshot"""
        if not output1:
            return None
        return {"url": output1["chart_url"]}
        
    def execute_module2(self, input_data):
        """Capture and analyze screenshot"""
        if not input_data:
            return None
            
        # Capture screenshot
        capture_result = self.module2["capture"](input_data["url"])
        
        # Analyze with AI
        analysis = self.module2["analyze"](capture_result["screenshot_path"])
        
        return {
            "capture": capture_result,
            "analysis": analysis,
            "combined_insights": {
                "visual_confirmation": True,
                "accessibility_score": 0.85,
                "recommendations": [
                    "Add alt text for screen readers",
                    "Increase contrast for better visibility"
                ]
            }
        }
        
    def validate_output(self, output):
        """Verify screenshot and analysis"""
        if not output or "pipeline_result" not in output:
            return False
            
        result = output["pipeline_result"]
        return (
            "capture" in result and
            "analysis" in result and
            len(result["analysis"].get("insights", [])) > 0
        )


class OptimizableResearchPipeline(Level1Interaction):
    """Example of RL-optimizable pipeline"""
    
    def __init__(self):
        super().__init__(
            "Optimizable Research Pipeline",
            "Research pipeline with RL optimization hooks"
        )
        # Optimization parameters
        self.search_strategy = "relevance"  # or "recent", "cited"
        self.conversion_quality = "balanced"  # or "fast", "accurate"
        self.parallel_downloads = 3
        
    def initialize_modules(self):
        return {"search": "arxiv"}, {"convert": "marker"}
        
    def get_optimization_parameters(self):
        """Parameters that can be optimized by RL"""
        return {
            "search_strategy": ["relevance", "recent", "cited"],
            "conversion_quality": ["fast", "balanced", "accurate"],
            "parallel_downloads": [1, 3, 5, 10]
        }
        
    def apply_optimization(self, params):
        """Apply RL-selected parameters"""
        self.search_strategy = params.get("search_strategy", self.search_strategy)
        self.conversion_quality = params.get("conversion_quality", self.conversion_quality)
        self.parallel_downloads = params.get("parallel_downloads", self.parallel_downloads)
        
    def execute_module1(self, **kwargs):
        """Search with optimized strategy"""
        # Use self.search_strategy to modify search
        return {"papers": ["paper1", "paper2"], "strategy": self.search_strategy}
        
    def execute_module2(self, input_data):
        """Convert with optimized quality"""
        # Use self.conversion_quality to modify conversion
        return {"markdown": "content", "quality": self.conversion_quality}
        
    def validate_output(self, output):
        return True
        
    def calculate_reward(self, result):
        """Calculate reward for RL optimization"""
        # Reward based on speed vs quality tradeoff
        speed_score = 1.0 / (result.duration + 1)
        quality_score = 0.8 if self.conversion_quality == "accurate" else 0.5
        
        return speed_score * 0.4 + quality_score * 0.6


if __name__ == "__main__":
    from interaction_framework import InteractionRunner
    
    # Test all example pipelines
    runner = InteractionRunner("Example Level 1 Pipelines")
    
    pipelines = [
        ArxivMarkerPipeline(),
        MarkerArangoDBPipeline(),
        YouTubeSpartaPipeline(),
        ScreenshotAnalysisPipeline(),
        OptimizableResearchPipeline()
    ]
    
    for pipeline in pipelines:
        result = runner.run_interaction(pipeline)
        print(f"\n{pipeline.name}: {'✅' if result.success else '❌'}")
        
    # Generate report
    report = runner.generate_report()
    
    # Example of how RL would optimize
    optimizable = OptimizableResearchPipeline()
    print(f"\nOptimization parameters: {optimizable.get_optimization_parameters()}")
    
    # Simulate RL choosing parameters
    rl_params = {
        "search_strategy": "cited",
        "conversion_quality": "accurate",
        "parallel_downloads": 5
    }
    optimizable.apply_optimization(rl_params)
    print(f"Applied optimization: {rl_params}")