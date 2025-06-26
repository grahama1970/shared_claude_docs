# Granger Module Interaction Testing Guide for Gemini

## Overview
This guide teaches how to create comprehensive interaction tests for the Granger ecosystem. The goal is to test real module capabilities, find bugs, and improve integration.

## Quick Reference

### Granger Architecture
```
Granger Ecosystem
├── Hub (granger_hub) - Central orchestration
├── RL Core (rl_commons) - Intelligence & optimization  
├── World Model - Self-understanding & prediction
├── Test Reporter - Quality assurance
└── Spokes - Specialized modules for different tasks
```

### Key Principles
1. **No Mocks** - Always use real module APIs
2. **Find Real Bugs** - Focus on actual integration issues
3. **Progressive Complexity** - Start simple (Level 0) and build up
4. **Cross-Module Testing** - Test how modules work together

## Interaction Levels

### Level 0: Single Module Tests
Test individual module capabilities in isolation.

**Example: YouTube Transcript Extraction**
```python
from youtube_transcripts import TechnicalContentMiningScenario

scenario = TechnicalContentMiningScenario()
result = scenario.search_technical_presentations("Python best practices")
assert result.success
assert len(result.output_data['videos']) > 0
```

### Level 1: Two-Module Pipelines
Test data flow between two modules.

**Example: ArXiv → Marker Pipeline**
```python
# Search papers
papers = arxiv.search("machine learning security")

# Convert first paper to markdown
pdf_url = papers[0]['pdf_url']
markdown = marker.convert_pdf_to_markdown(pdf_url)

# Verify pipeline
assert markdown is not None
assert len(markdown) > 1000
```

### Level 2: Multi-Module Orchestration
Test three or more modules working together.

**Example: Research → Analysis → Storage**
```python
# 1. Get YouTube transcript
transcript = youtube.extract_transcript(video_id)

# 2. Find related papers
papers = arxiv.search(transcript.keywords)

# 3. Store in ArangoDB
for paper in papers:
    db.collection('research').insert({
        'source_video': video_id,
        'paper': paper,
        'timestamp': datetime.now()
    })
```

### Level 3: Complex Workflows
Test complete end-to-end scenarios with many modules.

**Example: Full Anti-Pattern Analysis**
```python
# 1. Extract video content
video_data = youtube.get_arjancode_antipatterns()

# 2. Organize into rules
rules = organize_antipatterns(video_data)

# 3. Find related research
papers = arxiv.search_antipattern_research()
repos = gitget.search_linting_tools()

# 4. Synthesize with LLM
enhanced_rules = llm_call(
    prompt="Enhance these anti-pattern rules",
    context={'rules': rules, 'research': papers}
)

# 5. Analyze codebases
violations = analyze_all_granger_projects(enhanced_rules)

# 6. Generate report
report = create_antipattern_report(violations)

# 7. Store in ArangoDB
store_violations_in_graph(violations)

# 8. Get AI critique
critique = llm_call(report, provider="gemini")
```

## Creating New Interaction Tests

### 1. Choose Your Modules
Select 2-5 modules that should work together. Consider:
- Data flow (who produces, who consumes)
- Common use cases
- Integration points

### 2. Define the Scenario
Write a clear description of what the test will do:
```markdown
## Scenario: Security Vulnerability Research Pipeline
This test verifies that security data can flow from SPARTA through research
modules into our knowledge graph for analysis.

Modules: sparta → arxiv → marker → arangodb → llm_call
Expected outcome: CVE data enriched with research papers stored in graph
```

### 3. Identify Potential Bugs
Before writing the test, think about what could go wrong:
- Data format mismatches
- Missing required fields
- Timeout issues
- Memory leaks
- API rate limits
- Authentication failures

### 4. Write the Test
Structure your test to expose these potential issues:

```python
class SecurityResearchPipelineTest(BaseInteractionTest):
    def test_cve_to_research_pipeline(self):
        # Test data format compatibility
        cve_data = sparta.get_recent_cves()
        assert 'severity' in cve_data[0]  # Required field
        
        # Test timeout handling
        papers = arxiv.search(
            cve_data[0]['description'], 
            timeout=5  # Short timeout to test handling
        )
        
        # Test memory with large documents
        for paper in papers[:10]:
            markdown = marker.convert(paper['pdf_url'])
            assert len(markdown) < 10_000_000  # 10MB limit
            
        # Test graph storage
        collection = db.collection('security_research')
        for link in cve_paper_links:
            collection.insert(link)
            
        # Verify data integrity
        stored = collection.get(link['_key'])
        assert stored['cve_id'] == link['cve_id']
```

## Common Integration Patterns

### 1. Research Pipeline
```
YouTube/ArXiv → Marker → ArangoDB → LLM Analysis
```

### 2. Code Analysis Pipeline
```
GitGet → Code Parser → Vulnerability Scanner → Report
```

### 3. Document Processing Pipeline
```
SPARTA → Marker → NLP Analysis → Knowledge Graph
```

### 4. Real-time Monitoring
```
Data Source → Stream Processor → Alert System → Dashboard
```

### 5. Learning Pipeline
```
Data → Feature Extraction → RL Training → Model Deployment
```

## Module Capabilities Reference

### Data Ingestion
- **youtube_transcripts**: Video content extraction
- **arxiv-mcp-server**: Research paper search (45+ tools)
- **sparta**: Security document processing
- **gitget**: GitHub repository analysis
- **darpa_crawl**: Web crawling

### Processing
- **marker**: PDF/DOCX/PPTX → Markdown conversion
- **llm_call**: Multi-provider LLM interface
- **unsloth**: Model fine-tuning

### Storage & Intelligence
- **arangodb**: Graph database
- **world_model**: System state tracking
- **rl_commons**: Optimization algorithms

### Orchestration
- **granger_hub**: Central coordination
- **claude-test-reporter**: Test verification

## Example Test Scenarios

### 1. Documentation Generation Pipeline
```python
# GitGet → Analysis → Documentation
repo = gitget.clone_sparse("https://github.com/example/repo")
analysis = llm_call("Analyze this codebase", context=repo)
docs = generate_documentation(analysis)
```

### 2. Research Synthesis
```python
# Multiple sources → Synthesis → Knowledge Graph
papers = arxiv.search("quantum computing")
videos = youtube.search("quantum tutorials")
combined = synthesize_sources(papers, videos)
store_knowledge_graph(combined)
```

### 3. Security Monitoring
```python
# Real-time CVE → Analysis → Alert
cves = sparta.monitor_realtime()
for cve in cves:
    if cve['severity'] > 8:
        analysis = analyze_impact(cve)
        send_alert(analysis)
```

## Testing Best Practices

1. **Start Simple**: Begin with Level 0 tests, then combine
2. **Use Real Data**: No mocks - test actual integration
3. **Check Edge Cases**: Empty results, timeouts, large data
4. **Verify Both Success and Failure**: Error handling is critical
5. **Measure Performance**: Track speed and resource usage
6. **Document Bugs Found**: Create issues for each problem

## Common Bugs to Look For

### Data Issues
- Incompatible formats between modules
- Missing required fields
- Encoding problems (UTF-8, etc.)
- Size limit violations

### Integration Issues
- Module discovery failures
- Authentication problems
- Timeout cascades
- Connection pool exhaustion

### Performance Issues
- Memory leaks
- Slow queries
- Missing caching
- Inefficient data transfer

### Error Handling
- Silent failures
- Lost error context
- Unhelpful error messages
- Unhandled exceptions

## Next Steps

1. **Choose a scenario** from the examples or create your own
2. **Identify 3-5 modules** that should work together
3. **Write a test** that exercises their integration
4. **Run the test** and document any bugs found
5. **Submit findings** with reproduction steps

Remember: The goal is to make Granger more robust by finding and fixing real integration issues!