# Granger Interaction Test Creator Guide

## Core Understanding

**Granger** is a graph-reinforced autonomous network ecosystem where specialized modules collaborate through a central hub to perform complex AI research and analysis tasks.

### Essential Architecture
```
granger_hub (orchestrator) ← → All Modules
     ↓
rl_commons (optimization)
     ↓
world_model (self-learning)
```

## Module Directory

### Input Modules (Data Sources)
```python
youtube_transcripts  # Video content extraction
arxiv-mcp-server    # Research papers (45+ search tools)
sparta              # Security documents
gitget              # GitHub repos
darpa_crawl         # Web content
```

### Processing Modules
```python
marker              # PDF/DOCX/PPTX → Markdown
llm_call            # Multi-LLM interface (Claude/Gemini/GPT)
fine_tuning         # Model fine-tuning
```

### Storage & Intelligence
```python
arangodb            # Graph database
world_model         # System state & learning
rl_commons          # Reinforcement learning
claude-test-reporter # Test verification
```

### UI Modules
```python
chat                # Chat interface
annotator           # Labeling UI
aider-daemon        # CLI assistant
```

## Creating Interaction Tests

### Pattern 1: Data Pipeline Test
**Purpose**: Test data flow from source → processing → storage

```python
# Example: Research Pipeline
async def test_research_pipeline():
    # 1. Get data from source
    papers = await arxiv.search("LLM security")
    
    # 2. Process data
    for paper in papers[:3]:
        markdown = await marker.convert_pdf(paper.pdf_url)
        
    # 3. Analyze with LLM
    analysis = await llm_call(
        f"Summarize key findings: {markdown[:2000]}"
    )
    
    # 4. Store in graph
    await arangodb.insert({
        "type": "research",
        "paper": paper.title,
        "summary": analysis
    })
    
    # Verify: Check for data format issues, missing fields, timeouts
```

### Pattern 2: Multi-Source Synthesis
**Purpose**: Combine data from multiple sources

```python
# Example: Anti-Pattern Detection
async def test_antipattern_detection():
    # 1. Get educational content
    video = await youtube_transcripts.get_transcript(
        "ArjanCodes Python antipatterns"
    )
    
    # 2. Find related research
    papers = await arxiv.search(
        f"Python code quality {video.keywords}"
    )
    
    # 3. Find example repos
    repos = await gitget.search(
        "Python linter anti-pattern"
    )
    
    # 4. Synthesize rules
    rules = await llm_call(
        prompt="Extract anti-pattern rules",
        context={
            "video": video.text,
            "papers": papers[:3],
            "tools": repos[:3]
        }
    )
    
    # 5. Apply to Granger codebases
    violations = await analyze_codebases(rules)
    
    # Verify: Integration between modules, data compatibility
```

### Pattern 3: Real-time Monitoring
**Purpose**: Test continuous data flow and alerts

```python
# Example: Security Monitoring
async def test_security_monitoring():
    # 1. Monitor security feeds
    async for cve in sparta.stream_cves():
        if cve.severity > 8:
            # 2. Find mitigations
            papers = await arxiv.search(
                f"{cve.technology} security patch"
            )
            
            # 3. Generate alert
            alert = await llm_call(
                "Create security bulletin",
                context={"cve": cve, "research": papers}
            )
            
            # 4. Store and notify
            await arangodb.insert_alert(alert)
            
    # Verify: Stream handling, error recovery, performance
```

### Pattern 4: Learning Loop
**Purpose**: Test RL optimization and world model updates

```python
# Example: Module Selection Optimization
async def test_learning_optimization():
    # 1. Define task
    task = "Find and summarize quantum computing advances"
    
    # 2. Let RL choose module sequence
    module_sequence = await rl_commons.select_modules(task)
    
    # 3. Execute sequence
    results = await granger_hub.execute_sequence(
        module_sequence, task
    )
    
    # 4. Update world model
    await world_model.record_outcome(
        task, module_sequence, results
    )
    
    # 5. RL learns from outcome
    await rl_commons.update_policy(
        results.success_score
    )
    
    # Verify: Learning improves over iterations
```

## Test Creation Formula

### 1. Pick a Real Use Case
- Research synthesis
- Code analysis  
- Document processing
- Security monitoring
- Content extraction

### 2. Select 3-5 Modules
Choose modules that should work together:
- One data source (YouTube/ArXiv/GitGet/SPARTA)
- One processor (Marker/LLM)
- One storage (ArangoDB)
- Optional: UI or orchestration module

### 3. Design the Test Flow
```python
async def test_[use_case]():
    # Step 1: Get data from source
    # Step 2: Process/transform data
    # Step 3: Analyze/synthesize
    # Step 4: Store results
    # Step 5: Verify integration
```

### 4. Add Bug Detection
Focus on finding:
- **Data mismatches**: Fields missing between modules
- **Performance issues**: Timeouts, memory leaks
- **Error handling**: What happens when a module fails?
- **Scale problems**: Large documents, many requests

## Quick Test Templates

### Template 1: Document Analysis
```python
async def test_document_analysis():
    # Get document
    doc = await [sparta/marker/youtube].get_content(source)
    
    # Process document  
    processed = await marker.extract_text(doc)
    
    # Analyze content
    insights = await llm_call("Extract key points", processed)
    
    # Store insights
    await arangodb.store(insights)
```

### Template 2: Code Understanding
```python
async def test_code_analysis():
    # Get repository
    repo = await gitget.clone(url)
    
    # Analyze code
    analysis = await llm_call("Find security issues", repo.files)
    
    # Get related research
    papers = await arxiv.search(analysis.keywords)
    
    # Generate report
    report = await create_report(analysis, papers)
```

### Template 3: Research Automation
```python
async def test_research_automation():
    # Define research question
    question = "Latest advances in topic X"
    
    # Gather sources
    papers = await arxiv.search(question)
    videos = await youtube.search(question)
    
    # Synthesize findings
    synthesis = await llm_call("Synthesize", {papers, videos})
    
    # Store knowledge
    await arangodb.create_knowledge_graph(synthesis)
```

## Success Criteria

Your test is good if it:
1. **Uses real modules** (no mocks)
2. **Tests actual integration** (data flows between modules)
3. **Could find real bugs** (not just happy path)
4. **Represents real use case** (something users would do)
5. **Checks error handling** (what if something fails?)

## Example: Complete Test

```python
async def test_granger_learning_from_youtube():
    """
    Test: Granger learns from YouTube tutorial and applies knowledge
    Modules: youtube → llm_call → gitget → arangodb → world_model
    """
    
    # 1. Extract tutorial content
    tutorial = await youtube_transcripts.get_transcript(
        "FastAPI tutorial"
    )
    
    # 2. Extract concepts
    concepts = await llm_call(
        "List key concepts taught",
        tutorial.text
    )
    
    # 3. Find example implementations
    examples = await gitget.search(
        f"FastAPI {' '.join(concepts[:3])}"
    )
    
    # 4. Create knowledge entry
    knowledge = {
        "source": tutorial.video_id,
        "concepts": concepts,
        "examples": examples,
        "timestamp": datetime.now()
    }
    
    # 5. Store in graph
    node_id = await arangodb.insert(
        collection="tutorials",
        data=knowledge
    )
    
    # 6. Update world model
    await world_model.learn({
        "event": "tutorial_processed",
        "source": "youtube",
        "concepts_extracted": len(concepts),
        "examples_found": len(examples)
    })
    
    # Verify each step succeeded
    assert tutorial.text is not None
    assert len(concepts) > 0
    assert len(examples) > 0
    assert node_id is not None
    
    # Check for integration issues
    # - Did YouTube return valid transcript?
    # - Did LLM extract meaningful concepts?
    # - Did GitGet find relevant repos?
    # - Did ArangoDB store successfully?
    # - Did world model update?
```

## Start Creating!

1. **Pick modules** from the directory above
2. **Design a workflow** that makes sense
3. **Write the test** using the patterns
4. **Focus on integration** - how modules work together
5. **Look for bugs** - what could go wrong?

Remember: The goal is to test real module interactions and find actual integration issues in the Granger ecosystem!