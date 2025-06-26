# Visual Module Interaction Examples

Real-world examples with visual flow diagrams for each interaction level.

## 📘 Level 0 Examples (Direct Calls)

### Example 0.1: Simple Paper Search
```mermaid
graph LR
    User[User] -->|search query| ArXiv[arxiv-mcp-server]
    ArXiv -->|paper list| User
```

**Code**:
```python
papers = arxiv.search("quantum computing", max_results=10)
```

### Example 0.2: Basic Screenshot
```mermaid
graph LR
    User[User] -->|URL| MCP[mcp-screenshot]
    MCP -->|image| User
```

**Code**:
```python
screenshot = mcp_screenshot.capture("https://example.com")
```

---

## 🔗 Level 1 Examples (Sequential Chains)

### Example 1.1: Research Paper Analysis Pipeline
```mermaid
graph LR
    User[User] -->|paper ID| A[arxiv-mcp-server]
    A -->|PDF| B[marker]
    B -->|text| C[sparta]
    C -->|insights| User
```

**Flow**:
1. Fetch PDF from ArXiv
2. Extract text with Marker
3. Analyze with Sparta
4. Return insights

**Code**:
```python
# Sequential execution
pdf = await arxiv.fetch_pdf(paper_id)
text = await marker.extract_text(pdf)
analysis = await sparta.analyze(text)
return analysis
```

### Example 1.2: Video Learning Pipeline
```mermaid
graph LR
    YT[youtube_transcripts] -->|transcript| M[marker]
    M -->|entities| A[arangodb]
    A -->|graph_id| R[Result]
```

**Flow**:
1. Get video transcript
2. Extract key entities
3. Store in knowledge graph
4. Return graph reference

---

## 🔀 Level 2 Examples (Parallel & Branching)

### Example 2.1: Multi-Source Research Aggregation
```mermaid
graph TB
    Start[User Query] --> P1[arxiv-mcp-server]
    Start --> P2[youtube_transcripts]
    
    P1 -->|papers| M1[marker]
    P2 -->|videos| A1[Analysis]
    
    M1 -->|extracted| Merge[sparta.merge]
    A1 -->|insights| Merge
    
    Merge --> DB[arangodb]
    DB --> Result[Unified Knowledge]
```

**Code**:
```python
# Parallel execution
async def multi_source_research(query):
    # Launch parallel searches
    papers_task = arxiv.search(query)
    videos_task = youtube.search(query)
    
    # Wait for both
    papers, videos = await asyncio.gather(papers_task, videos_task)
    
    # Process in parallel
    extract_task = marker.batch_extract(papers)
    analyze_task = youtube.analyze_batch(videos)
    
    extracted, analyzed = await asyncio.gather(extract_task, analyze_task)
    
    # Merge and store
    merged = await sparta.merge_knowledge(extracted, analyzed)
    graph_id = await arangodb.store(merged)
    
    return graph_id
```

### Example 2.2: Conditional Document Processing
```mermaid
graph TB
    Start[Document] --> Extract[marker.extract]
    Extract --> Type{Content Type?}
    
    Type -->|Code| Code[claude-test-reporter]
    Type -->|Docs| Docs[shared_claude_docs]
    Type -->|Data| Data[sparta]
    
    Code --> CodeResult[Test Report]
    Docs --> DocsResult[Formatted Docs]
    Data --> DataResult[Analysis]
    
    CodeResult --> Store[arangodb]
    DocsResult --> Store
    DataResult --> Store
```

---

## 🎭 Level 3 Examples (Orchestrated Systems)

### Example 3.1: Self-Improving Research System
```mermaid
graph TB
    subgraph "Discovery Phase"
        Query[Initial Query] --> Search[arxiv-mcp-server]
        Search <--> Relevance[sparta.score_relevance]
        Relevance --> Refine{Good enough?}
        Refine -->|No| Query
        Refine -->|Yes| Extract[marker.extract]
    end
    
    subgraph "Learning Phase"
        Extract <--> Validate[marker-ground-truth]
        Validate --> Learn[sparta.improve_model]
        Learn --> Extract
    end
    
    subgraph "Knowledge Building"
        Extract --> Graph[arangodb.build]
        Graph <--> Patterns[sparta.find_patterns]
        Patterns --> NewQueries[Generate New Queries]
        NewQueries --> Query
    end
    
    Graph --> Report[Final Knowledge Graph]
```

**Orchestration Logic**:
```python
class ResearchOrchestrator:
    async def run(self, initial_query):
        query = initial_query
        iterations = 0
        knowledge_graph = KnowledgeGraph()
        
        while iterations < MAX_ITERATIONS:
            # Discovery with feedback
            papers = await self.discover_relevant_papers(query)
            
            # Extraction with learning
            extracted = await self.extract_with_improvement(papers)
            
            # Knowledge building
            knowledge_graph.add(extracted)
            patterns = await knowledge_graph.find_patterns()
            
            # Generate new queries from patterns
            new_queries = await self.generate_queries(patterns)
            if not new_queries:
                break
                
            query = new_queries[0]
            iterations += 1
        
        return knowledge_graph
```

### Example 3.2: Real-time Adaptive Documentation
```mermaid
stateDiagram-v2
    [*] --> Monitoring: Git Hook
    
    Monitoring --> Analysis: Code Change Detected
    Analysis --> Impact: Analyze Changes
    
    Impact --> HighImpact: Significant
    Impact --> LowImpact: Minor
    
    HighImpact --> Regenerate: Full Doc Update
    LowImpact --> Patch: Incremental Update
    
    Regenerate --> Testing: Generate Examples
    Testing --> Validation: Test Examples
    
    Validation --> Screenshot: Update Visuals
    Screenshot --> Publish
    
    Patch --> Publish: Quick Update
    
    Publish --> Verify: Ground Truth Check
    Verify --> Learn: Feedback
    Learn --> Monitoring: Improve Detection
```

### Example 3.3: Intelligent Training Orchestra
```mermaid
graph TB
    subgraph "Exploration"
        Task[User Task] --> Papers[arxiv-mcp-server]
        Task --> Videos[youtube_transcripts]
        Papers --> Architectures[marker.extract_architectures]
        Videos --> Techniques[sparta.extract_techniques]
    end
    
    subgraph "Experimentation"
        Architectures --> Gen[sparta.generate_experiments]
        Techniques --> Gen
        Gen --> Exp1[Experiment 1]
        Gen --> Exp2[Experiment 2]
        Gen --> Exp3[Experiment 3]
        
        Exp1 --> Opt1[fine_tuning.optimize]
        Exp2 --> Opt2[fine_tuning.optimize]
        Exp3 --> Opt3[fine_tuning.optimize]
    end
    
    subgraph "Selection"
        Opt1 --> Test[claude-test-reporter]
        Opt2 --> Test
        Opt3 --> Test
        Test --> Best{Select Best}
        Best --> Ensemble[claude_max_proxy.ensemble]
    end
    
    subgraph "Deployment"
        Ensemble --> Valid[marker-ground-truth]
        Valid --> Deploy[Production]
        Deploy --> Monitor[Continuous Monitoring]
        Monitor --> Task
    end
```

---

## 🎯 Interaction Complexity Comparison

### Simple Query (Level 0)
```
Time: ~1 second
Modules: 1
Complexity: O(1)
```

### Pipeline Query (Level 1)
```
Time: ~5 seconds
Modules: 3-4
Complexity: O(n)
```

### Parallel Query (Level 2)
```
Time: ~3 seconds (parallel)
Modules: 4-6
Complexity: O(log n)
```

### Orchestrated Query (Level 3)
```
Time: Variable (adaptive)
Modules: 6-12
Complexity: O(n × iterations)
```

---

## 💡 Best Practices Illustrated

### DO: Start Simple
```mermaid
graph LR
    A[Level 0] -->|Works?| Use[Use It!]
    A -->|Need more?| B[Level 1]
    B -->|Still need more?| C[Level 2]
    C -->|Complex needs?| D[Level 3]
```

### DON'T: Over-Engineer
```mermaid
graph TB
    Simple[Simple Task] -.->|Wrong!| Complex[Level 3 System]
    Simple -->|Right!| Direct[Level 0/1]
```

### DO: Clear Error Handling
```mermaid
graph TB
    Module1 -->|Success| Module2
    Module1 -->|Error| ErrorHandler
    ErrorHandler -->|Retry| Module1
    ErrorHandler -->|Fail| UserNotification
```

---

## 🔧 Debugging Workflows

### Level 1 Debugging
```mermaid
graph LR
    Input[Check Input] --> Module1[Check Module 1]
    Module1 --> Output1[Check Output 1]
    Output1 --> Module2[Check Module 2]
    Module2 --> FinalOutput[Check Final Output]
```

### Level 3 Debugging
```mermaid
graph TB
    Logs[Check Orchestrator Logs] --> State[Verify State]
    State --> Loops[Check Feedback Loops]
    Loops --> Timing[Analyze Timing]
    Timing --> Metrics[Review Metrics]
```

---

*These visual examples demonstrate the progression from simple to complex module interactions. Use them as templates for designing your own workflows.*