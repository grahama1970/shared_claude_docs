# Granger Hub Orchestration: Real Examples

## How Granger Hub Orchestrates Multi-Module Interactions

Based on the actual code in the Granger ecosystem, here's how the hub orchestrates interactions between different project modules:

### Example 1: Full Security Research Pipeline

From `test_full_granger_pipeline.py`, the hub orchestrates a complete workflow:

```python
# User makes ONE simple request:
result = pipeline.run_full_pipeline("buffer overflow")

# Behind the scenes, Granger Hub orchestrates:
```

#### Phase 1: SPARTA Module Searches for Vulnerabilities
```python
# Hub calls SPARTA
cve_result = sparta_handler.handle({
    "keyword": "buffer overflow",
    "limit": 5
})
# Returns: 5 CVEs with descriptions
```

#### Phase 2: ArXiv Module Finds Research Papers
```python
# Hub takes CVE results and calls ArXiv
# It builds a smart query from CVE descriptions
search_terms = ["buffer overflow", "memory safety", "remote exploitation"]
papers = arxiv_handler.handle({
    "query": " OR ".join(search_terms),
    "max_results": 5
})
# Returns: Research papers about these vulnerabilities
```

#### Phase 3: Marker Processes Documents (if available)
```python
# Hub downloads PDFs and sends to Marker
for paper in papers:
    pdf_content = marker_handler.handle({
        "pdf_url": paper["pdf_url"],
        "extract_tables": True
    })
```

#### Phase 4: ArangoDB Stores Everything with Relationships
```python
# Hub stores CVEs
arango_doc.handle({
    "operation": "create",
    "collection": "vulnerabilities",
    "data": cve_data
})

# Hub stores papers
arango_doc.handle({
    "operation": "create", 
    "collection": "research_papers",
    "data": paper_data
})

# Hub creates relationships
arango_graph.handle({
    "operation": "create_edge",
    "from": "vulnerabilities/CVE-2024-1234",
    "to": "research_papers/2301.12345",
    "edge_type": "addressed_by"
})
```

#### Phase 5: Memory Agent Tracks the Session
```python
# Hub logs the entire research session
arango_memory.handle({
    "operation": "create_episode",
    "agent_id": "granger_researcher",
    "content": "Researched buffer overflow vulnerabilities",
    "metadata": {
        "cves_found": 5,
        "papers_found": 3,
        "relationships_created": 8
    }
})
```

### Example 2: YouTube Research Flow

From `youtube_arxiv_gitget_research_flow.md`:

```python
# Simple API call:
result = await process_research_video("https://www.youtube.com/watch?v=ABC123")

# Granger Hub orchestrates:
```

1. **YouTube Module** extracts transcript and finds links:
   ```python
   transcript = youtube_handler.download_transcript(video_url)
   links = youtube_handler.extract_links(transcript)
   # Returns: arxiv links, github repos, timestamps
   ```

2. **ArXiv Module** fetches paper metadata for each link:
   ```python
   for arxiv_link in links["arxiv"]:
       paper_data = arxiv_handler.get_paper(arxiv_link)
   ```

3. **GitGet Module** analyzes repositories:
   ```python
   for github_link in links["github"]:
       repo_analysis = gitget_handler.analyze(github_link)
   ```

4. **ArangoDB** builds the knowledge graph:
   ```python
   # Creates nodes for videos, papers, repos
   # Creates edges: video->mentions->paper, paper->implemented_by->repo
   ```

### Example 3: Multi-Agent Collaboration

From the Level 3 tests, multiple agents work together:

```python
# Research Agent finds papers
research_agent.execute({
    "task": "find quantum computing papers",
    "modules": ["arxiv", "youtube"]
})

# Security Agent analyzes vulnerabilities  
security_agent.execute({
    "task": "analyze cryptographic weaknesses",
    "modules": ["sparta", "arxiv"]
})

# ML Agent optimizes the workflow
ml_agent.execute({
    "task": "optimize research pipeline",
    "modules": ["rl_commons", "arangodb"]
})

# All communicate through the hub
hub.broadcast({
    "event": "new_vulnerability_found",
    "data": vulnerability_data,
    "interested_agents": ["research_agent", "ml_agent"]
})
```

### Key Orchestration Patterns

1. **Sequential Pipeline**: Output of one module feeds the next
   - SPARTA → ArXiv → Marker → ArangoDB

2. **Parallel Processing**: Multiple modules work simultaneously
   - YouTube + ArXiv + GitGet all processing different aspects

3. **Conditional Branching**: Next steps depend on results
   - If CVEs found → search for papers
   - If papers have code → analyze with GitGet

4. **Event-Driven**: Modules react to hub events
   - New paper found → trigger analysis
   - Analysis complete → update knowledge graph

5. **Feedback Loops**: Results improve future runs
   - RL Commons learns from successful patterns
   - Memory agent tracks what worked

### The Magic: One Call, Complete Orchestration

The user/agent just calls:
```python
result = granger_hub.process("analyze buffer overflow vulnerabilities")
```

And Granger Hub automatically:
- Determines which modules to use
- Orchestrates the data flow
- Handles errors and retries
- Stores results in the knowledge graph
- Tracks the session for learning
- Returns a comprehensive result

This is the power of Granger's flexible hub-and-spoke architecture!