# Project Interactions Testing Framework

This guide explains the standardized interaction testing framework for all projects in the ecosystem.

## Overview

The interaction testing framework ensures all modules can work together seamlessly at different levels of complexity:

- **Level 0**: Single module functionality (unit-like tests)
- **Level 1**: Two-module pipelines (integration tests)
- **Level 2**: Parallel/branching workflows (advanced integration)
- **Level 3**: Orchestrated collaboration with feedback loops (system tests)

## Directory Structure

Each project should have an `interactions/` directory (or `tests/interactions/`):

```
project_name/
├── interactions/
│   ├── __init__.py
│   ├── interaction_framework.py   # Copy from shared_claude_docs/templates/
│   ├── level_0/                   # Single module tests
│   │   ├── __init__.py
│   │   └── core_functionality.py
│   ├── level_1/                   # Two-module pipelines
│   │   ├── __init__.py
│   │   └── pipeline_interactions.py
│   ├── level_2/                   # Parallel workflows (optional)
│   └── run_interactions.py        # Main runner
```

## Implementation Status

| Project | Level 0 | Level 1 | Framework | Notes |
|---------|---------|---------|-----------|-------|
| arxiv-mcp-server | ✅ | 🔲 | ✅ | Search, evidence, batch ops |
| marker | 🔲 | 🔲 | 🔲 | PDF conversion, AI enhancement |
| arangodb | 🔲 | 🔲 | 🔲 | Memory storage, search, graphs |
| mcp-screenshot | 🔲 | 🔲 | 🔲 | Screenshot capture, analysis |
| sparta | 🔲 | 🔲 | 🔲 | Security analysis, enrichment |
| youtube_transcripts | 🔲 | 🔲 | 🔲 | Transcript fetch, search |
| granger_hub | ✅ | ✅ | ✅ | Central hub with 40+ scenarios |
| claude_max_proxy | 🔲 | 🔲 | 🔲 | LLM routing, validation |
| fine_tuning | 🔲 | 🔲 | 🔲 | Model training, optimization |
| marker-ground-truth | 🔲 | 🔲 | 🔲 | Annotation, validation |
| rl_commons | 🔲 | 🔲 | 🔲 | Bandit optimization |

## Quick Start

1. **Copy the framework to your project**:
   ```bash
   # From shared_claude_docs directory
   cp templates/interaction_framework.py /path/to/your/project/interactions/
   cp -r project_interactions/arxiv-mcp-server/* /path/to/arxiv-mcp-server/interactions/
   ```

2. **Create Level 0 interactions**:
   ```python
   from interaction_framework import Level0Interaction
   
   class YourFeatureInteraction(Level0Interaction):
       def __init__(self):
           super().__init__("Feature Name", "Feature description")
           
       def initialize_module(self):
           return YourModule()
           
       def execute(self, **kwargs):
           return self.module.your_method(**kwargs)
           
       def validate_output(self, output):
           return output is not None and output["success"]
   ```

3. **Run interactions**:
   ```bash
   python interactions/run_interactions.py
   ```

## Level 0 Examples (Single Module)

### ArXiv MCP Server
- Search papers by query
- Find supporting/contradicting evidence
- Batch download papers
- Generate daily digest

### Marker
- Convert PDF to Markdown
- Extract tables with AI
- Fast mode vs accurate mode
- Export to ArangoDB format

### ArangoDB
- Store conversation memory
- Search with multiple algorithms
- Build knowledge graphs
- Generate Q&A pairs

## Level 1 Examples (Two-Module Pipelines)

### Research Pipeline (ArXiv → Marker)
```
1. ArXiv: Search for papers on "transformers"
2. ArXiv: Download first PDF
3. Marker: Convert PDF to Markdown
4. Marker: Extract tables and figures
Result: Structured document ready for analysis
```

### Document Memory Pipeline (Marker → ArangoDB)
```
1. Marker: Extract content from PDF
2. Marker: Identify key concepts
3. ArangoDB: Store as memory chunks
4. ArangoDB: Build entity relationships
Result: Searchable knowledge graph
```

### Visual Documentation (Any → Screenshot)
```
1. Module X: Generate output/visualization
2. Screenshot: Capture the display
3. Screenshot: AI analysis of image
4. Screenshot: Store with metadata
Result: Visual documentation with AI insights
```

## Level 2 Examples (Parallel/Branching)

### Multi-Source Research
```
Parallel:
├─→ ArXiv: Search papers
│   └─→ Marker: Batch extract
└─→ YouTube: Search videos
    └─→ Transcripts: Extract
    
Merge → SPARTA: Analyze all content
     → ArangoDB: Unified graph
```

### Conditional Processing
```
Marker: Extract content
IF content_type == "code":
    → SPARTA: Security analysis
    → Test Reporter: Generate report
ELIF content_type == "research":
    → ArangoDB: Store findings
    → Unsloth: Generate Q&A
```

## RL Commons Integration

Interactions can be optimized using bandits:

```python
from interaction_framework import OptimizableInteraction
import rl_commons

class OptimizedPipeline(OptimizableInteraction):
    def get_action_space(self):
        return {
            "extraction_method": ["fast", "accurate"],
            "ai_enhancement": [True, False],
            "parallel_workers": [1, 2, 4, 8]
        }
        
    def apply_action(self, action):
        self.config.update(action)
        
    def calculate_quality_score(self, result):
        # Define what "quality" means
        speed = 1.0 / result.duration
        accuracy = result.output_data.get("accuracy", 0)
        return (speed * 0.3 + accuracy * 0.7)
```

## Best Practices

1. **Real Data Only**: Never use mocked data for core functionality
2. **Clear Success Criteria**: Define exactly what constitutes success
3. **Resource Cleanup**: Always clean up temp files, connections
4. **Timeout Handling**: Set reasonable timeouts for long operations
5. **Error Reporting**: Capture and report specific errors
6. **Incremental Development**: Start with Level 0, add levels as needed

## Common Patterns

### Pattern 1: File Processing Pipeline
```python
# Level 0: Process single file
class ProcessFileInteraction(Level0Interaction):
    def execute(self, **kwargs):
        return process_file(kwargs["file_path"])

# Level 1: Download then process
class DownloadProcessPipeline(Level1Interaction):
    def execute_module1(self, **kwargs):
        return download_file(kwargs["url"])
    def execute_module2(self, file_path):
        return process_file(file_path)
```

### Pattern 2: Search and Analyze
```python
# Level 0: Search
class SearchInteraction(Level0Interaction):
    def execute(self, **kwargs):
        return search(kwargs["query"])

# Level 1: Search then analyze
class SearchAnalyzePipeline(Level1Interaction):
    def execute_module1(self, **kwargs):
        return search(kwargs["query"])
    def execute_module2(self, results):
        return analyze(results)
```

### Pattern 3: Store and Retrieve
```python
# Level 0: Store data
class StoreInteraction(Level0Interaction):
    def execute(self, **kwargs):
        return store(kwargs["data"])

# Level 0: Retrieve data
class RetrieveInteraction(Level0Interaction):
    def execute(self, **kwargs):
        return retrieve(kwargs["query"])
```

## Testing Strategy

1. **Start with Level 0**: Ensure each module works independently
2. **Add Level 1**: Test common two-module workflows
3. **Consider Level 2**: Only if parallel/branching is common
4. **Reserve Level 3**: For complex orchestration scenarios

## CI/CD Integration

```yaml
# .github/workflows/interactions.yml
name: Module Interactions

on: [push, pull_request]

jobs:
  test-interactions:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        project: [arxiv-mcp-server, marker, arangodb]
    steps:
      - uses: actions/checkout@v2
      - name: Run ${{ matrix.project }} interactions
        run: |
          cd ${{ matrix.project }}/interactions
          python run_interactions.py
```

## Troubleshooting

### Import Errors
- Ensure `interaction_framework.py` is in the interactions directory
- Add parent directory to Python path if needed

### Module Not Found
- Check if module is installed in your environment
- Use mock objects for testing without dependencies

### Validation Failures
- Review your `validate_output()` method
- Ensure it checks for actual success, not just non-null

## Next Steps

1. Implement Level 0 for all projects
2. Identify common Level 1 pipelines
3. Create RL optimization examples
4. Build cross-project test suite

## Resources

- [Interaction Framework Source](../templates/interaction_framework.py)
- [Implementation Guide](../templates/INTERACTION_IMPLEMENTATION_GUIDE.md)
- [Module Interaction Levels](../docs/big_picture/MODULE_INTERACTION_LEVELS.md)
- [Example: ArXiv Interactions](arxiv-mcp-server/)