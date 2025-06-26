# How to Write Granger Interaction Scenarios

**Purpose**: Complete guide for creating module interaction scenarios that demonstrate real ecosystem integration  
**Focus**: Practical examples, architectural rationale, and testing patterns  
**Reference**: Based on existing scenarios in `/experiments/granger_hub/scenarios` and `/project_interactions`

---

## 📋 Table of Contents

1. [Understanding Interaction Scenarios](#understanding-interaction-scenarios)
2. [Architecture Overview](#architecture-overview)
3. [Types of Interaction Scenarios](#types-of-interaction-scenarios)
4. [Writing Your First Scenario](#writing-your-first-scenario)
5. [Advanced Patterns](#advanced-patterns)
6. [Testing Interaction Scenarios](#testing-interaction-scenarios)
7. [Common Pitfalls](#common-pitfalls)
8. [Real Examples](#real-examples)

---

## 🎯 Understanding Interaction Scenarios

### What Are Interaction Scenarios?

Interaction scenarios are concrete implementations that demonstrate how multiple Granger modules work together to accomplish real-world tasks. They are NOT:
- Unit tests for individual modules
- Mock implementations
- Isolated function demonstrations

They ARE:
- Real workflows showing data flow between modules
- Integration patterns that can be reused
- Proof that modules can communicate effectively
- Templates for building larger applications

### Why Are They Critical?

1. **Verification**: Prove modules actually work together
2. **Documentation**: Show developers how to integrate modules
3. **Testing**: Ensure changes don't break integrations
4. **Discovery**: Find missing capabilities early
5. **Architecture**: Validate the hub-and-spoke design

---

## 🏗️ Architecture Overview

### Hub-and-Spoke Model

```
                    Granger Hub
                         |
        +----------------+----------------+
        |                |                |
    Module A         Module B         Module C
        |                                 |
        +---------------------------------+
                    Can communicate via Hub
```

### Key Architectural Principles

1. **Hub Registration**: All modules register with Granger Hub
2. **Message Passing**: Standard message format for all communications
3. **Async Operations**: Non-blocking message handling
4. **Error Propagation**: Failures cascade gracefully
5. **Progress Tracking**: Hub monitors all operations

### Standard Message Format

```python
@dataclass
class Message:
    source: str          # Module sending the message
    target: str          # Module receiving the message
    operation: str       # What action to perform
    data: Dict[str, Any] # Payload
    correlation_id: str  # Track related messages
    timestamp: float     # When sent
```

---

## 📚 Types of Interaction Scenarios

### Level 1: Binary Interactions (Module A ↔ Module B)

Simple two-module interactions demonstrating basic communication:

```python
# Example: ArXiv → Marker
async def process_paper(paper_id: str):
    # ArXiv downloads paper
    paper_data = await arxiv.download_paper(paper_id)
    
    # Marker extracts content
    extracted = await marker.extract_content(paper_data)
    
    return extracted
```

### Level 2: Pipeline Interactions (A → B → C)

Sequential processing through multiple modules:

```python
# Example: YouTube → ArXiv → ArangoDB
async def research_pipeline(video_url: str):
    # Extract links from video
    links = await youtube.extract_links(video_url)
    
    # Get papers from links
    papers = await arxiv.fetch_papers(links.arxiv_links)
    
    # Store in knowledge graph
    graph_id = await arangodb.store_research(papers)
    
    return graph_id
```

### Level 3: Orchestrated Interactions (Hub Coordination)

Complex workflows with branching and parallel processing:

```python
# Example: Full research workflow
async def orchestrated_research(topic: str):
    hub = GrangerHub()
    
    # Parallel searches
    tasks = [
        hub.send_message("youtube", "search", {"query": topic}),
        hub.send_message("arxiv", "search", {"query": topic}),
        hub.send_message("gitget", "search", {"query": topic})
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Process all results through marker
    processed = []
    for result in results:
        proc = await hub.send_message("marker", "extract", result)
        processed.append(proc)
    
    # Store everything
    await hub.send_message("arangodb", "store_batch", processed)
```

### Level 4: UI-Driven Interactions

User interfaces triggering complex backend workflows:

```python
# Example: Chat UI research request
async def handle_user_research_request(user_input: str):
    # Chat UI receives request
    intent = await chat_ui.parse_intent(user_input)
    
    # Route through hub to appropriate modules
    if intent.type == "research":
        results = await hub.orchestrate_research(intent.query)
        
        # Format for display
        formatted = await chat_ui.format_results(results)
        return formatted
```

---

## ✏️ Writing Your First Scenario

### Step 1: Define the Use Case

Start with a clear, real-world use case:

```python
"""
Use Case: Security Vulnerability Research
Goal: Given a CVE ID, gather all related information from multiple sources
Modules: sparta → marker → arangodb → llm_call
"""
```

### Step 2: Create the Scenario Structure

```python
#!/usr/bin/env python3
"""
Module: security_vulnerability_research.py
Description: Research security vulnerabilities across multiple sources

External Dependencies:
- sparta: https://docs.example.com/sparta
- marker: https://docs.example.com/marker
- arangodb: https://docs.example.com/arangodb
- llm_call: https://docs.example.com/llm_call

Sample Input:
>>> request = {
>>>     "cve_id": "CVE-2024-1234",
>>>     "depth": "comprehensive"
>>> }

Expected Output:
>>> {
>>>     "cve_id": "CVE-2024-1234",
>>>     "severity": "HIGH",
>>>     "affected_systems": [...],
>>>     "mitigations": [...],
>>>     "knowledge_graph_id": "kg_12345"
>>> }
"""

import asyncio
from typing import Dict, List, Any
from dataclasses import dataclass
from loguru import logger

from granger_hub import GrangerHub, Message
from sparta import download_security_resources
from marker import extract_security_content
from arangodb import SecurityKnowledgeGraph
from llm_call import analyze_vulnerability

@dataclass
class VulnerabilityRequest:
    cve_id: str
    depth: str = "standard"  # standard, comprehensive, minimal
    include_mitigations: bool = True
```

### Step 3: Implement Module Registration

```python
class SecurityResearchScenario:
    def __init__(self):
        self.hub = GrangerHub()
        self.modules = {}
        self._register_modules()
    
    def _register_modules(self):
        """Register all required modules with the hub."""
        modules_to_register = [
            ("sparta", self._handle_sparta_message),
            ("marker", self._handle_marker_message),
            ("arangodb", self._handle_arangodb_message),
            ("llm_call", self._handle_llm_message)
        ]
        
        for module_name, handler in modules_to_register:
            self.hub.register_module(module_name, handler)
            logger.info(f"Registered {module_name} with hub")
```

### Step 4: Implement the Workflow

```python
async def research_vulnerability(self, request: VulnerabilityRequest) -> Dict[str, Any]:
    """Main workflow for vulnerability research."""
    logger.info(f"Starting research for {request.cve_id}")
    
    # Step 1: Download security resources
    logger.info("Downloading security resources...")
    sparta_msg = Message(
        source="scenario",
        target="sparta",
        operation="download_cve",
        data={"cve_id": request.cve_id}
    )
    resources = await self.hub.send_message(sparta_msg)
    
    # Step 2: Extract structured content
    logger.info("Extracting content from resources...")
    marker_tasks = []
    for resource in resources["documents"]:
        msg = Message(
            source="scenario",
            target="marker",
            operation="extract",
            data={"document": resource, "schema": "security"}
        )
        marker_tasks.append(self.hub.send_message(msg))
    
    extracted_data = await asyncio.gather(*marker_tasks)
    
    # Step 3: Store in knowledge graph
    logger.info("Building knowledge graph...")
    graph_msg = Message(
        source="scenario",
        target="arangodb",
        operation="create_vulnerability_graph",
        data={
            "cve_id": request.cve_id,
            "extracted_data": extracted_data
        }
    )
    graph_result = await self.hub.send_message(graph_msg)
    
    # Step 4: Analyze with LLM if comprehensive
    analysis = None
    if request.depth == "comprehensive":
        logger.info("Performing LLM analysis...")
        llm_msg = Message(
            source="scenario",
            target="llm_call",
            operation="analyze_vulnerability",
            data={
                "cve_id": request.cve_id,
                "graph_data": graph_result["summary"],
                "include_mitigations": request.include_mitigations
            }
        )
        analysis = await self.hub.send_message(llm_msg)
    
    # Compile results
    return {
        "cve_id": request.cve_id,
        "resources_found": len(resources["documents"]),
        "extracted_items": len(extracted_data),
        "knowledge_graph_id": graph_result["graph_id"],
        "analysis": analysis,
        "status": "complete"
    }
```

### Step 5: Add Error Handling

```python
async def research_vulnerability_safe(self, request: VulnerabilityRequest) -> Dict[str, Any]:
    """Research with comprehensive error handling."""
    try:
        return await self.research_vulnerability(request)
    except Exception as e:
        logger.error(f"Research failed for {request.cve_id}: {e}")
        
        # Notify all modules of failure
        error_msg = Message(
            source="scenario",
            target="*",  # Broadcast
            operation="error",
            data={
                "cve_id": request.cve_id,
                "error": str(e),
                "timestamp": time.time()
            }
        )
        await self.hub.broadcast_message(error_msg)
        
        return {
            "cve_id": request.cve_id,
            "status": "failed",
            "error": str(e)
        }
```

### Step 6: Add Progress Tracking

```python
async def research_with_progress(self, request: VulnerabilityRequest) -> Dict[str, Any]:
    """Research with progress updates."""
    progress_id = f"research_{request.cve_id}_{int(time.time())}"
    
    async def update_progress(stage: str, percent: int):
        await self.hub.send_message(Message(
            source="scenario",
            target="hub",
            operation="update_progress",
            data={
                "progress_id": progress_id,
                "stage": stage,
                "percent": percent
            }
        ))
    
    await update_progress("Starting", 0)
    
    # Download phase (0-25%)
    await update_progress("Downloading resources", 10)
    resources = await self._download_resources(request.cve_id)
    await update_progress("Resources downloaded", 25)
    
    # Extract phase (25-60%)
    await update_progress("Extracting content", 30)
    extracted = await self._extract_content(resources)
    await update_progress("Content extracted", 60)
    
    # Store phase (60-90%)
    await update_progress("Building knowledge graph", 70)
    graph = await self._store_graph(extracted)
    await update_progress("Graph complete", 90)
    
    # Analysis phase (90-100%)
    await update_progress("Analyzing vulnerability", 95)
    analysis = await self._analyze(graph)
    await update_progress("Complete", 100)
    
    return {
        "progress_id": progress_id,
        "result": analysis
    }
```

---

## 🚀 Advanced Patterns

### Pattern 1: Conditional Routing

```python
async def smart_document_processing(document_path: str):
    """Route document to appropriate processor based on content."""
    # Detect document type
    doc_type = await detect_document_type(document_path)
    
    if doc_type == "pdf":
        result = await hub.send_message("marker", "extract_pdf", {"path": document_path})
    elif doc_type == "video":
        result = await hub.send_message("youtube", "extract_transcript", {"path": document_path})
    elif doc_type == "code":
        result = await hub.send_message("gitget", "analyze_code", {"path": document_path})
    else:
        result = await hub.send_message("llm_call", "extract_text", {"path": document_path})
    
    return result
```

### Pattern 2: Parallel Processing with Aggregation

```python
async def comprehensive_research(topic: str):
    """Research topic across all available sources."""
    sources = ["arxiv", "youtube", "gitget", "sparta"]
    
    # Launch parallel searches
    search_tasks = []
    for source in sources:
        task = hub.send_message(source, "search", {
            "query": topic,
            "limit": 10,
            "timeout": 30
        })
        search_tasks.append(task)
    
    # Wait for all with timeout
    results = await asyncio.wait_for(
        asyncio.gather(*search_tasks, return_exceptions=True),
        timeout=35
    )
    
    # Aggregate successful results
    aggregated = {
        "topic": topic,
        "sources": {},
        "total_results": 0
    }
    
    for source, result in zip(sources, results):
        if isinstance(result, Exception):
            aggregated["sources"][source] = {"error": str(result)}
        else:
            aggregated["sources"][source] = result
            aggregated["total_results"] += len(result.get("items", []))
    
    return aggregated
```

### Pattern 3: Retry with Fallback

```python
async def reliable_llm_analysis(data: Dict[str, Any]):
    """Analyze with retries and fallbacks."""
    providers = ["claude", "gpt4", "llama", "local"]
    
    for provider in providers:
        for attempt in range(3):
            try:
                result = await hub.send_message("llm_call", "analyze", {
                    "data": data,
                    "provider": provider,
                    "timeout": 30
                })
                
                if result["confidence"] > 0.8:
                    return result
                    
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {provider}: {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
    # All providers failed - use simple analysis
    return {"provider": "fallback", "analysis": "basic", "confidence": 0.5}
```

### Pattern 4: Stateful Conversations

```python
class ResearchConversation:
    """Maintain state across multiple interactions."""
    
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.history = []
        self.context = {}
    
    async def add_query(self, query: str) -> Dict[str, Any]:
        """Process query with conversation context."""
        # Update context with previous results
        enhanced_query = {
            "query": query,
            "context": self.context,
            "history": self.history[-5:]  # Last 5 interactions
        }
        
        # Process with context awareness
        result = await hub.send_message("llm_call", "contextual_query", enhanced_query)
        
        # Update conversation state
        self.history.append({"query": query, "result": result})
        self.context.update(result.get("extracted_entities", {}))
        
        # Store conversation state
        await hub.send_message("arangodb", "update_conversation", {
            "id": self.conversation_id,
            "history": self.history,
            "context": self.context
        })
        
        return result
```

---

## 🧪 Testing Interaction Scenarios

### Test Structure

```python
import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from security_vulnerability_research import SecurityResearchScenario

class TestSecurityResearch:
    """Test security research interaction scenario."""
    
    @pytest.fixture
    async def scenario(self):
        """Create scenario with real connections."""
        scenario = SecurityResearchScenario()
        await scenario.initialize()
        yield scenario
        await scenario.cleanup()
    
    @pytest.mark.asyncio
    async def test_basic_cve_research(self, scenario):
        """Test basic CVE research flow."""
        request = VulnerabilityRequest(
            cve_id="CVE-2024-1234",
            depth="standard"
        )
        
        result = await scenario.research_vulnerability(request)
        
        # Verify all steps completed
        assert result["status"] == "complete"
        assert result["resources_found"] > 0
        assert result["knowledge_graph_id"] is not None
        
    @pytest.mark.asyncio
    async def test_module_communication(self, scenario):
        """Test that modules actually communicate."""
        # Monitor hub messages
        messages_sent = []
        
        async def capture_message(msg):
            messages_sent.append(msg)
            return {"status": "ok"}
        
        scenario.hub.send_message = capture_message
        
        await scenario.research_vulnerability(
            VulnerabilityRequest("CVE-2024-5678")
        )
        
        # Verify message flow
        assert len(messages_sent) >= 4  # sparta, marker, arangodb, llm_call
        assert any(m.target == "sparta" for m in messages_sent)
        assert any(m.target == "marker" for m in messages_sent)
        
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_real_module_integration(self, scenario):
        """Test with real module connections (no mocks)."""
        # This test requires all modules to be running
        request = VulnerabilityRequest(
            cve_id="CVE-2023-0001",  # Known test CVE
            depth="comprehensive"
        )
        
        start_time = time.time()
        result = await scenario.research_vulnerability(request)
        duration = time.time() - start_time
        
        # Real operations take time
        assert duration > 1.0  # Should take at least 1 second
        assert result["analysis"] is not None  # LLM analysis completed
        
        # Verify data actually stored
        graph_check = await scenario.hub.send_message(
            "arangodb", "get_graph", {"id": result["knowledge_graph_id"]}
        )
        assert graph_check["node_count"] > 0
```

### Interaction Test Patterns

1. **Message Flow Verification**
```python
async def test_message_ordering(scenario):
    """Ensure messages are processed in correct order."""
    message_log = []
    
    # Hook into hub to log messages
    original_send = scenario.hub.send_message
    async def logging_send(msg):
        message_log.append((msg.target, msg.operation))
        return await original_send(msg)
    
    scenario.hub.send_message = logging_send
    
    # Run scenario
    await scenario.process_document("test.pdf")
    
    # Verify order
    expected_order = [
        ("sparta", "download"),
        ("marker", "extract"),
        ("arangodb", "store")
    ]
    
    actual_order = [(target, op) for target, op in message_log]
    assert actual_order == expected_order
```

2. **Error Propagation Testing**
```python
async def test_error_propagation(scenario):
    """Test that errors propagate correctly through modules."""
    # Make marker fail
    async def failing_marker(msg):
        if msg.operation == "extract":
            raise ValueError("Extraction failed")
        return {"status": "ok"}
    
    scenario.hub.modules["marker"] = failing_marker
    
    result = await scenario.research_vulnerability(
        VulnerabilityRequest("CVE-2024-9999")
    )
    
    assert result["status"] == "failed"
    assert "Extraction failed" in result["error"]
```

3. **Performance Testing**
```python
async def test_concurrent_processing(scenario):
    """Test scenario handles concurrent requests."""
    requests = [
        VulnerabilityRequest(f"CVE-2024-{i:04d}")
        for i in range(10)
    ]
    
    start_time = time.time()
    results = await asyncio.gather(*[
        scenario.research_vulnerability(req)
        for req in requests
    ])
    duration = time.time() - start_time
    
    # Should process concurrently
    assert duration < 10  # Not 10x single request time
    assert all(r["status"] == "complete" for r in results)
```

---

## ⚠️ Common Pitfalls

### Pitfall 1: Not Using Real Connections

❌ **Wrong**:
```python
# Mocking everything
mock_hub = Mock()
mock_hub.send_message.return_value = {"status": "ok"}
```

✅ **Right**:
```python
# Use real hub with real modules
hub = GrangerHub()
await hub.connect_to_modules(["sparta", "marker", "arangodb"])
```

### Pitfall 2: Ignoring Async Patterns

❌ **Wrong**:
```python
# Blocking calls
result1 = process_module_a(data)
result2 = process_module_b(result1)
result3 = process_module_c(result2)
```

✅ **Right**:
```python
# Proper async handling
result1 = await hub.send_message("module_a", "process", data)
result2 = await hub.send_message("module_b", "process", result1)
result3 = await hub.send_message("module_c", "process", result2)
```

### Pitfall 3: No Error Handling

❌ **Wrong**:
```python
# Assuming everything works
data = await fetch_data()
processed = await process_data(data)
stored = await store_data(processed)
```

✅ **Right**:
```python
# Comprehensive error handling
try:
    data = await fetch_data()
except FetchError as e:
    logger.error(f"Fetch failed: {e}")
    return {"status": "failed", "stage": "fetch", "error": str(e)}

try:
    processed = await process_data(data)
except ProcessError as e:
    # Cleanup partial data
    await cleanup_data(data)
    return {"status": "failed", "stage": "process", "error": str(e)}
```

### Pitfall 4: Not Testing Module Dependencies

❌ **Wrong**:
```python
# Only testing the happy path
result = await scenario.run()
assert result["status"] == "success"
```

✅ **Right**:
```python
# Test with module failures
for module in ["sparta", "marker", "arangodb"]:
    scenario.disable_module(module)
    result = await scenario.run()
    assert result["status"] == "degraded"
    assert module in result["failed_modules"]
    scenario.enable_module(module)
```

---

## 📖 Real Examples

### Example 1: YouTube to Knowledge Graph Pipeline

From `/experiments/granger_hub/scenarios/research_youtube_to_knowledge_graph.py`:

```python
async def process_research_video(video_url: str) -> Dict[str, Any]:
    """Complete pipeline from YouTube video to knowledge graph."""
    
    # Extract transcript and links
    transcript_data = await youtube.download_transcript(video_url)
    links = extract_links_from_text(transcript_data["text"])
    
    # Process each link type
    arxiv_papers = []
    github_repos = []
    
    for link in links:
        if link.link_type == "arxiv":
            paper = await arxiv.get_paper(link.url)
            arxiv_papers.append(paper)
        elif link.link_type == "github":
            repo = await gitget.analyze_repo(link.url)
            github_repos.append(repo)
    
    # Build knowledge graph
    graph = KnowledgeGraphBuilder()
    graph.add_video(video_url, transcript_data)
    graph.add_papers(arxiv_papers)
    graph.add_repos(github_repos)
    
    # Store in ArangoDB
    result = await arangodb.store_graph(graph)
    
    return {
        "video_id": extract_video_id(video_url),
        "knowledge_chunks": len(graph.chunks),
        "arxiv_papers": len(arxiv_papers),
        "github_repos": len(github_repos),
        "graph_nodes": result["node_count"],
        "graph_edges": result["edge_count"]
    }
```

### Example 2: Multi-Step Document Processing

From `/project_interactions/multi_step_processing_scenario.py`:

```python
async def process_complex_document(doc_path: str) -> Dict[str, Any]:
    """Multi-step document processing with validation."""
    
    # Step 1: Initial extraction
    raw_content = await marker.extract_raw(doc_path)
    
    # Step 2: Validate extraction quality
    quality_score = await llm_call.assess_quality(raw_content)
    
    if quality_score < 0.7:
        # Re-extract with enhanced settings
        raw_content = await marker.extract_enhanced(doc_path)
    
    # Step 3: Structure content
    structured = await marker.structure_content(raw_content, schema="research")
    
    # Step 4: Enrich with external data
    enriched = structured
    for reference in structured.get("references", []):
        if "arxiv" in reference:
            paper_data = await arxiv.get_metadata(reference)
            enriched["enriched_refs"].append(paper_data)
    
    # Step 5: Store with relationships
    graph_id = await arangodb.store_document_graph(enriched)
    
    return {
        "document": doc_path,
        "quality_score": quality_score,
        "extraction_method": "enhanced" if quality_score < 0.7 else "standard",
        "references_enriched": len(enriched.get("enriched_refs", [])),
        "graph_id": graph_id
    }
```

### Example 3: Real-Time Monitoring Scenario

From `/project_interactions/performance_optimization/`:

```python
class RealTimeMonitoringScenario:
    """Monitor and optimize module performance in real-time."""
    
    async def monitor_pipeline_health(self):
        """Continuously monitor pipeline health."""
        
        while self.monitoring:
            # Collect metrics from all modules
            metrics = await asyncio.gather(*[
                self.hub.send_message(module, "get_metrics", {})
                for module in self.active_modules
            ])
            
            # Analyze performance
            bottlenecks = self.identify_bottlenecks(metrics)
            
            if bottlenecks:
                # Apply optimizations
                for module, issue in bottlenecks.items():
                    if issue == "high_latency":
                        await self.hub.send_message(module, "enable_cache", {})
                    elif issue == "memory_pressure":
                        await self.hub.send_message(module, "reduce_batch_size", {})
                    elif issue == "queue_buildup":
                        await self.scale_module(module, scale_factor=2)
            
            # Report status
            await self.hub.broadcast_message({
                "type": "health_update",
                "timestamp": time.time(),
                "metrics": metrics,
                "optimizations": bottlenecks
            })
            
            await asyncio.sleep(30)  # Check every 30 seconds
```

---

## 🎁 Scenario Templates

### Basic Binary Interaction Template

```python
#!/usr/bin/env python3
"""
Module: [module_a]_to_[module_b]_scenario.py
Description: [What this scenario demonstrates]

External Dependencies:
- [module_a]: [docs_link]
- [module_b]: [docs_link]
"""

async def process_[workflow_name](input_data: Dict[str, Any]) -> Dict[str, Any]:
    """[Describe the workflow]."""
    
    # Step 1: Process with module A
    result_a = await hub.send_message("[module_a]", "[operation]", input_data)
    
    # Step 2: Transform for module B
    transformed = transform_data(result_a)
    
    # Step 3: Process with module B
    result_b = await hub.send_message("[module_b]", "[operation]", transformed)
    
    return {
        "input": input_data,
        "module_a_result": result_a,
        "module_b_result": result_b,
        "status": "complete"
    }
```

### Pipeline Interaction Template

```python
class [Pipeline]Scenario:
    """[Description of the pipeline]."""
    
    def __init__(self):
        self.hub = GrangerHub()
        self.pipeline_modules = ["module_a", "module_b", "module_c"]
        
    async def run_pipeline(self, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the full pipeline."""
        
        current_data = initial_data
        results = {"stages": {}}
        
        for module in self.pipeline_modules:
            try:
                result = await self.hub.send_message(
                    module, 
                    "process", 
                    current_data
                )
                results["stages"][module] = result
                current_data = result  # Output becomes next input
                
            except Exception as e:
                logger.error(f"Pipeline failed at {module}: {e}")
                results["failed_at"] = module
                results["error"] = str(e)
                break
                
        results["final_output"] = current_data
        return results
```

---

## 📚 Additional Resources

- **Architecture Documentation**: [@docs/GRANGER_PROJECTS.md](/home/graham/workspace/shared_claude_docs/docs/GRANGER_PROJECTS.md)
- **Existing Scenarios**: `/home/graham/workspace/experiments/granger_hub/scenarios/`
- **Project Interactions**: `/home/graham/workspace/shared_claude_docs/project_interactions/`
- **Test Templates**: [@guides/TEST_VERIFICATION_TEMPLATE_GUIDE.md](/home/graham/workspace/shared_claude_docs/guides/TEST_VERIFICATION_TEMPLATE_GUIDE.md)
- **Task Planning**: [@guides/TASK_LIST_TEMPLATE_GUIDE_V2.md](/home/graham/workspace/shared_claude_docs/guides/TASK_LIST_TEMPLATE_GUIDE_V2.md)

---

## 🚦 Quick Checklist

Before submitting your interaction scenario:

- [ ] **Real Modules**: Uses actual module connections, not mocks
- [ ] **Hub Integration**: All modules register with Granger Hub
- [ ] **Message Format**: Uses standard Message dataclass
- [ ] **Error Handling**: Handles module failures gracefully
- [ ] **Progress Tracking**: Reports progress for long operations
- [ ] **Testing**: Includes integration tests that verify communication
- [ ] **Documentation**: Clear docstring with dependencies and examples
- [ ] **Git Workflow**: Committed and pushed to repo
- [ ] **Dependencies Updated**: All importing modules run `uv pip install -e .`
- [ ] **Verified**: Actually tested with running modules

Remember: A good interaction scenario proves that modules can work together to solve real problems!