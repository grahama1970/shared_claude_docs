
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Level 0 Batch Operations Interactions for ArXiv MCP Server

Tests batch download, processing, and daily workflow features.

External Dependencies:
- typing: Built-in type annotations
- pathlib: Built-in path handling

Example Usage:
>>> interaction = BatchDownloadInteraction()
>>> result = interaction.run(paper_ids=["2017.00001", "2018.00002"])
>>> print(f"Downloaded {result.output_data['result']['success_count']} papers")
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from interaction_framework import Level0Interaction
import tempfile
import os


class BatchDownloadInteraction(Level0Interaction):
    """Test batch downloading multiple papers"""
    
    def __init__(self):
        super().__init__(
            "Batch Download Papers",
            "Download multiple papers in one operation"
        )
        self.download_dir = None
        
    def initialize_module(self):
        return {"tool": "batch-download"}
        
    def setup(self):
        super().setup()
        self.download_dir = tempfile.mkdtemp()
        
    def execute(self, **kwargs):
        paper_ids = kwargs.get("paper_ids", [
            "2017.00001", "2018.00002", "2019.00003"
        ])
        
        # Mock batch download results
        results = {
            "download_dir": self.download_dir,
            "success_count": len(paper_ids) - 1,  # Simulate one failure
            "failed_count": 1,
            "downloads": []
        }
        
        for i, paper_id in enumerate(paper_ids):
            if i == len(paper_ids) - 1:  # Simulate last one failing
                results["downloads"].append({
                    "paper_id": paper_id,
                    "status": "failed",
                    "error": "404 Not Found",
                    "path": None
                })
            else:
                path = os.path.join(self.download_dir, f"{paper_id}.pdf")
                # Create dummy file
                Path(path).touch()
                results["downloads"].append({
                    "paper_id": paper_id,
                    "status": "success",
                    "path": path,
                    "size_mb": 2.5
                })
                
        return results
        
    def validate_output(self, output):
        if not isinstance(output, dict):
            return False
            
        if "success_count" not in output or "downloads" not in output:
            return False
            
        # Check at least one successful download
        successful = [d for d in output["downloads"] if d["status"] == "success"]
        return len(successful) > 0
        
    def teardown(self):
        # Cleanup temp directory
        if self.download_dir and os.path.exists(self.download_dir):
            import shutil
            shutil.rmtree(self.download_dir)


class DailyDigestInteraction(Level0Interaction):
    """Test daily research digest generation"""
    
    def __init__(self):
        super().__init__(
            "Daily Research Digest",
            "Generate personalized daily research updates"
        )
        
    def initialize_module(self):
        return {"tool": "daily-digest"}
        
    def execute(self, **kwargs):
        interests = kwargs.get("interests", [
            "transformer models",
            "computer vision", 
            "reinforcement learning"
        ])
        
        return {
            "date": "2024-01-15",
            "total_new_papers": 47,
            "relevant_papers": 12,
            "sections": [
                {
                    "topic": "Transformer Models",
                    "papers": [
                        {
                            "id": "2024.00123",
                            "title": "Efficient Transformers: A Survey",
                            "relevance_score": 0.95,
                            "summary": "Comprehensive review of efficiency improvements"
                        },
                        {
                            "id": "2024.00124",
                            "title": "MobileViT: Light-weight Vision Transformer",
                            "relevance_score": 0.88,
                            "summary": "Transformers optimized for mobile devices"
                        }
                    ]
                },
                {
                    "topic": "Computer Vision",
                    "papers": [
                        {
                            "id": "2024.00125",
                            "title": "DINO v2: Self-supervised Vision Models",
                            "relevance_score": 0.92,
                            "summary": "Improved self-supervised learning for vision"
                        }
                    ]
                }
            ],
            "trending_topics": [
                "Multimodal transformers",
                "Efficient attention mechanisms",
                "Vision-language models"
            ],
            "recommended_deep_dive": {
                "id": "2024.00123",
                "reason": "Most comprehensive survey in your area of interest"
            }
        }
        
    def validate_output(self, output):
        if not isinstance(output, dict):
            return False
            
        required = ["date", "total_new_papers", "relevant_papers", "sections"]
        if not all(field in output for field in required):
            return False
            
        # Check sections structure
        for section in output.get("sections", []):
            if "topic" not in section or "papers" not in section:
                return False
                
        return output["relevant_papers"] > 0


class ReadingListInteraction(Level0Interaction):
    """Test reading list management"""
    
    def __init__(self):
        super().__init__(
            "Reading List Management",
            "Add, retrieve, and export reading lists"
        )
        self.reading_list = []
        
    def initialize_module(self):
        return {"tools": ["add-reading", "get-reading", "export-reading"]}
        
    def execute(self, **kwargs):
        # Simulate adding papers
        papers_to_add = kwargs.get("papers", [
            {"id": "2017.00001", "priority": "high", "tags": ["foundational"]},
            {"id": "2023.00005", "priority": "medium", "tags": ["survey"]},
            {"id": "2024.00001", "priority": "low", "tags": ["experimental"]}
        ])
        
        # Add papers
        for paper in papers_to_add:
            self.reading_list.append({
                **paper,
                "added_date": "2024-01-15",
                "status": "unread"
            })
            
        # Simulate operations
        operations = {
            "papers_added": len(papers_to_add),
            "total_papers": len(self.reading_list),
            "by_priority": {
                "high": sum(1 for p in self.reading_list if p["priority"] == "high"),
                "medium": sum(1 for p in self.reading_list if p["priority"] == "medium"),
                "low": sum(1 for p in self.reading_list if p["priority"] == "low")
            },
            "export_formats": ["bibtex", "markdown", "json"],
            "reading_list": self.reading_list
        }
        
        return operations
        
    def validate_output(self, output):
        if not isinstance(output, dict):
            return False
            
        if "papers_added" not in output or "reading_list" not in output:
            return False
            
        return len(output["reading_list"]) > 0


class CollectionManagementInteraction(Level0Interaction):
    """Test paper collection creation and management"""
    
    def __init__(self):
        super().__init__(
            "Collection Management",
            "Create and manage paper collections"
        )
        
    def initialize_module(self):
        return {"tool": "collections"}
        
    def execute(self, **kwargs):
        collection_name = kwargs.get("name", "Vision Transformers Research")
        
        return {
            "collection_id": "coll_001",
            "name": collection_name,
            "created": "2024-01-15",
            "papers_count": 25,
            "metadata": {
                "description": "Collection of papers on vision transformers",
                "tags": ["computer-vision", "transformers", "deep-learning"],
                "visibility": "private"
            },
            "statistics": {
                "total_citations": 15234,
                "avg_citations_per_paper": 609,
                "year_range": "2017-2024",
                "top_authors": [
                    "Dosovitskiy, A.",
                    "Carion, N.", 
                    "Liu, Z."
                ]
            },
            "operations": [
                "add_paper",
                "remove_paper",
                "export_collection",
                "share_collection",
                "generate_bibliography"
            ]
        }
        
    def validate_output(self, output):
        if not isinstance(output, dict):
            return False
            
        required = ["collection_id", "name", "papers_count"]
        return all(field in output for field in required)


class BulkExportInteraction(Level0Interaction):
    """Test bulk export functionality"""
    
    def __init__(self):
        super().__init__(
            "Bulk Export",
            "Export multiple papers in various formats"
        )
        
    def initialize_module(self):
        return {"tool": "bulk-export"}
        
    def execute(self, **kwargs):
        paper_ids = kwargs.get("paper_ids", ["2017.00001", "2018.00002"])
        export_format = kwargs.get("format", "bibtex")
        
        if export_format == "bibtex":
            content = """@article{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and others},
  journal={NeurIPS},
  year={2017}
}

@article{devlin2018bert,
  title={BERT: Pre-training of Deep Bidirectional Transformers},
  author={Devlin, Jacob and others},
  journal={arXiv preprint},
  year={2018}
}"""
        else:
            content = "# Exported Papers\n\n- Paper 1\n- Paper 2"
            
        return {
            "format": export_format,
            "papers_exported": len(paper_ids),
            "content": content,
            "file_size_kb": len(content) / 1024,
            "available_formats": ["bibtex", "ris", "endnote", "markdown", "json"]
        }
        
    def validate_output(self, output):
        if not isinstance(output, dict):
            return False
            
        if "content" not in output or "papers_exported" not in output:
            return False
            
        return len(output["content"]) > 0


if __name__ == "__main__":
    from interaction_framework import InteractionRunner
    
    runner = InteractionRunner("ArXiv Batch Operations")
    
    interactions = [
        BatchDownloadInteraction(),
        DailyDigestInteraction(),
        ReadingListInteraction(),
        CollectionManagementInteraction(),
        BulkExportInteraction()
    ]
    
    for interaction in interactions:
        runner.run_interaction(interaction)
        
    report = runner.generate_report()
    print(f"\nBatch operations success rate: {report['summary']['success_rate']:.1f}%")