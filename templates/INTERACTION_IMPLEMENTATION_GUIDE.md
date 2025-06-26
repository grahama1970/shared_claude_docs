# Interaction Framework Implementation Guide

This guide explains how to implement the standardized interaction testing framework in each project.

## Quick Start

1. Create an `interactions/` directory in your project (or use `tests/interactions/`)
2. Copy `interaction_framework.py` from templates
3. Create interaction files for each level
4. Run interactions with the runner

## Directory Structure

```
project_name/
├── interactions/               # Or tests/interactions/
│   ├── __init__.py
│   ├── interaction_framework.py   # Copy from templates
│   ├── level_0/
│   │   ├── __init__.py
│   │   ├── basic_functionality.py
│   │   └── core_features.py
│   ├── level_1/
│   │   ├── __init__.py
│   │   └── pipeline_interactions.py
│   └── run_interactions.py
```

## Level 0 Implementation Examples

### ArXiv MCP Server Example

```python
# interactions/level_0/search_papers.py
from interaction_framework import Level0Interaction
from arxiv_mcp_server import ArxivServer  # Adjust import

class SearchPapersInteraction(Level0Interaction):
    """Test basic paper search functionality"""
    
    def __init__(self):
        super().__init__(
            "Search Papers",
            "Search ArXiv for quantum computing papers"
        )
        
    def initialize_module(self):
        return ArxivServer()
        
    def execute(self, **kwargs):
        query = kwargs.get("query", "quantum computing")
        limit = kwargs.get("limit", 10)
        return self.module.search(query, limit=limit)
        
    def validate_output(self, output):
        # Check we got results
        if not output or not isinstance(output, list):
            return False
        # Check each result has required fields
        for paper in output:
            if not all(k in paper for k in ["title", "authors", "abstract"]):
                return False
        return len(output) > 0
```

### Marker Example

```python
# interactions/level_0/pdf_conversion.py
from interaction_framework import Level0Interaction
from marker import convert_pdf
import os

class PDFConversionInteraction(Level0Interaction):
    """Test basic PDF to Markdown conversion"""
    
    def __init__(self):
        super().__init__(
            "PDF Conversion",
            "Convert a PDF to Markdown"
        )
        self.test_pdf = None
        
    def initialize_module(self):
        # Marker uses functions, not classes
        return convert_pdf
        
    def setup(self):
        super().setup()
        # Ensure we have a test PDF
        self.test_pdf = "test_data/sample.pdf"
        if not os.path.exists(self.test_pdf):
            raise FileNotFoundError(f"Test PDF not found: {self.test_pdf}")
        
    def execute(self, **kwargs):
        return self.module(
            self.test_pdf,
            extract_tables=kwargs.get("extract_tables", True),
            ai_enhancement=kwargs.get("ai_enhancement", False)
        )
        
    def validate_output(self, output):
        # Check we got markdown content
        return (
            output is not None and
            "markdown" in output and
            len(output["markdown"]) > 0
        )
```

### ArangoDB Example

```python
# interactions/level_0/memory_storage.py
from interaction_framework import Level0Interaction
from arangodb_memory import MemoryAgent

class MemoryStorageInteraction(Level0Interaction):
    """Test storing and retrieving memories"""
    
    def __init__(self):
        super().__init__(
            "Memory Storage",
            "Store and retrieve a conversation memory"
        )
        
    def initialize_module(self):
        return MemoryAgent(
            db_name="test_memories",
            collection_name="test_conversations"
        )
        
    def execute(self, **kwargs):
        # Store a memory
        memory_data = kwargs.get("memory", {
            "role": "user",
            "content": "Tell me about quantum computing",
            "metadata": {"topic": "quantum", "timestamp": "2024-01-01"}
        })
        
        stored = self.module.store_memory(memory_data)
        
        # Search for it
        results = self.module.search_memories(
            query="quantum computing",
            limit=5
        )
        
        return {
            "stored": stored,
            "found": results
        }
        
    def validate_output(self, output):
        return (
            output["stored"] is not None and
            len(output["found"]) > 0 and
            any("quantum" in str(m).lower() for m in output["found"])
        )
```

## Level 1 Implementation Examples

### ArXiv → Marker Pipeline

```python
# interactions/level_1/research_pipeline.py
from interaction_framework import Level1Interaction
from arxiv_mcp_server import ArxivServer
from marker import convert_pdf
import tempfile
import os

class ResearchPipelineInteraction(Level1Interaction):
    """Download paper from ArXiv and convert to Markdown"""
    
    def __init__(self):
        super().__init__(
            "Research Pipeline",
            "ArXiv search → download → Marker conversion"
        )
        self.temp_dir = None
        
    def initialize_modules(self):
        return ArxivServer(), convert_pdf
        
    def setup(self):
        super().setup()
        self.temp_dir = tempfile.mkdtemp()
        
    def execute_module1(self, **kwargs):
        # Search and download first paper
        query = kwargs.get("query", "attention is all you need")
        papers = self.module1.search(query, limit=1)
        
        if papers:
            paper = papers[0]
            pdf_path = os.path.join(self.temp_dir, f"{paper['id']}.pdf")
            self.module1.download_pdf(paper['id'], pdf_path)
            return {"paper": paper, "pdf_path": pdf_path}
        return None
        
    def transform_output(self, output1):
        # Pass PDF path to Marker
        return output1["pdf_path"] if output1 else None
        
    def execute_module2(self, input_data):
        if not input_data:
            return None
        return self.module2(input_data, extract_tables=True)
        
    def validate_output(self, output):
        return (
            output["module2_output"] is not None and
            "markdown" in output["module2_output"] and
            len(output["module2_output"]["markdown"]) > 100
        )
        
    def teardown(self):
        # Cleanup temp files
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
```

### Marker → ArangoDB Pipeline

```python
# interactions/level_1/document_memory_pipeline.py
from interaction_framework import Level1Interaction
from marker import convert_pdf
from arangodb_memory import MemoryAgent

class DocumentMemoryPipeline(Level1Interaction):
    """Convert PDF and store extracted content as memories"""
    
    def __init__(self):
        super().__init__(
            "Document Memory Pipeline",
            "Marker extraction → ArangoDB storage"
        )
        
    def initialize_modules(self):
        return convert_pdf, MemoryAgent(db_name="test_docs")
        
    def execute_module1(self, **kwargs):
        pdf_path = kwargs.get("pdf_path", "test_data/sample.pdf")
        return self.module1(pdf_path, ai_enhancement=True)
        
    def transform_output(self, output1):
        # Transform Marker output to memory format
        if not output1:
            return None
            
        memories = []
        
        # Store document metadata
        memories.append({
            "role": "system",
            "content": f"Document: {output1.get('title', 'Unknown')}",
            "metadata": {
                "type": "document_metadata",
                "pages": output1.get("pages", 0),
                "tables": len(output1.get("tables", []))
            }
        })
        
        # Store main content
        content = output1.get("markdown", "")
        # Split into chunks if needed
        chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
        
        for i, chunk in enumerate(chunks):
            memories.append({
                "role": "assistant",
                "content": chunk,
                "metadata": {
                    "type": "document_content",
                    "chunk": i,
                    "source": "marker_extraction"
                }
            })
            
        return memories
        
    def execute_module2(self, input_data):
        if not input_data:
            return None
            
        stored = []
        for memory in input_data:
            result = self.module2.store_memory(memory)
            stored.append(result)
            
        # Test retrieval
        search_results = self.module2.search_memories(
            query=input_data[0]["content"][:50],
            limit=5
        )
        
        return {
            "stored_count": len(stored),
            "search_results": search_results
        }
        
    def validate_output(self, output):
        result = output.get("module2_output")
        return (
            result is not None and
            result["stored_count"] > 0 and
            len(result["search_results"]) > 0
        )
```

## Running Interactions

Create a runner script:

```python
# interactions/run_interactions.py
#!/usr/bin/env python
"""Run all interactions for this project"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from interaction_framework import InteractionRunner

# Import all interactions
from level_0.search_papers import SearchPapersInteraction
from level_0.batch_operations import BatchDownloadInteraction
from level_1.research_pipeline import ResearchPipelineInteraction

def main():
    runner = InteractionRunner("ArXiv MCP Server")
    
    # Define all interactions
    interactions = [
        # Level 0
        SearchPapersInteraction(),
        BatchDownloadInteraction(),
        
        # Level 1
        ResearchPipelineInteraction(),
    ]
    
    # Run all
    report = runner.run_all(interactions)
    
    # Save report
    with open("interaction_report.json", "w") as f:
        import json
        json.dump(report, f, indent=2)
        
    # Exit with appropriate code
    failed = report["summary"]["failed"]
    sys.exit(1 if failed > 0 else 0)

if __name__ == "__main__":
    main()
```

## RL Commons Integration

For modules that can be optimized:

```python
# interactions/level_1/optimizable_pipeline.py
from interaction_framework import OptimizableInteraction, Level1Interaction
import rl_commons

class OptimizableResearchPipeline(Level1Interaction, OptimizableInteraction):
    """Research pipeline with RL optimization"""
    
    def __init__(self):
        Level1Interaction.__init__(self, 
            "Optimizable Research Pipeline",
            "ArXiv → Marker with bandit optimization"
        )
        OptimizableInteraction.__init__(self,
            self.name, self.description, self.level
        )
        
        # Optimization parameters
        self.search_limit = 10
        self.ai_enhancement = False
        self.extraction_method = "marker"
        
    def get_action_space(self):
        return {
            "search_limit": [5, 10, 20, 50],
            "ai_enhancement": [True, False],
            "extraction_method": ["marker", "pymupdf4llm"]
        }
        
    def apply_action(self, action):
        self.search_limit = action.get("search_limit", self.search_limit)
        self.ai_enhancement = action.get("ai_enhancement", self.ai_enhancement)
        self.extraction_method = action.get("extraction_method", self.extraction_method)
        
    def calculate_quality_score(self, result):
        # Custom quality metric
        if not result.success:
            return 0.0
            
        output = result.output_data.get("pipeline_result", {})
        
        # Score based on extraction quality
        score = 0.0
        if "markdown" in output:
            content_length = len(output["markdown"])
            table_count = len(output.get("tables", []))
            
            # Normalize scores
            score += min(content_length / 10000, 1.0) * 0.5
            score += min(table_count / 5, 1.0) * 0.3
            score += 0.2 if self.ai_enhancement else 0.1
            
        return score
```

## Best Practices

1. **Real Data**: Always use real test data, not mocked
2. **Timeouts**: Set reasonable timeouts for long operations
3. **Cleanup**: Always cleanup temp files/resources
4. **Validation**: Be specific about what constitutes success
5. **Error Handling**: Gracefully handle module failures
6. **Documentation**: Document expected inputs/outputs
7. **Modularity**: Keep interactions focused and simple

## Integration with CI/CD

```yaml
# .github/workflows/interactions.yml
name: Module Interactions Test

on: [push, pull_request]

jobs:
  test-interactions:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run Level 0 Interactions
        run: |
          python interactions/run_level_0.py
      - name: Run Level 1 Interactions
        run: |
          python interactions/run_level_1.py
      - name: Upload Reports
        uses: actions/upload-artifact@v2
        with:
          name: interaction-reports
          path: interaction_report.json
```