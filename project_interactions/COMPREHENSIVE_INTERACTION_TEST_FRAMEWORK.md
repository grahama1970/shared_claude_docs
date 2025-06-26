# Comprehensive Interaction Test Framework for Granger Ecosystem

## Core Principle: No Module is an Island

**Every module MUST demonstrate actual working interactions with its dependencies before being marked as "tested" or "complete".**

## 1. Interaction Requirements Matrix

### Critical Interaction Paths

```
┌─────────────────────┬───────────────┬──────────────┬──────────────┬─────────────┬──────────────┐
│ Module              │ MUST Send To  │ MUST Receive │ Bidirectional│ Priority    │ Test Level   │
│                     │               │ From         │ With         │             │              │
├─────────────────────┼───────────────┼──────────────┼──────────────┼─────────────┼──────────────┤
│ Granger Hub         │ ALL modules   │ ALL modules  │ ALL modules  │ CRITICAL    │ L1, L2, L3   │
├─────────────────────┼───────────────┼──────────────┼──────────────┼─────────────┼──────────────┤
│ ArangoDB            │ RL Commons    │ Marker,      │ Hub          │ CRITICAL    │ L1, L2, L3   │
│                     │ World Model   │ SPARTA       │              │             │              │
├─────────────────────┼───────────────┼──────────────┼──────────────┼─────────────┼──────────────┤
│ ArXiv MCP           │ Marker,       │ Hub,         │ Hub          │ HIGH        │ L1, L2       │
│                     │ ArangoDB      │ YouTube      │              │             │              │
├─────────────────────┼───────────────┼──────────────┼──────────────┼─────────────┼──────────────┤
│ Marker              │ ArangoDB      │ SPARTA,      │ Hub          │ HIGH        │ L1, L2, L3   │
│                     │               │ ArXiv        │              │             │              │
├─────────────────────┼───────────────┼──────────────┼──────────────┼─────────────┼──────────────┤
│ SPARTA              │ Marker        │ Hub          │ Hub          │ HIGH        │ L1, L2, L3   │
├─────────────────────┼───────────────┼──────────────┼──────────────┼─────────────┼──────────────┤
│ YouTube             │ ArXiv,        │ Hub          │ Hub          │ MEDIUM      │ L1, L2       │
│                     │ ArangoDB      │              │              │             │              │
├─────────────────────┼───────────────┼──────────────┼──────────────┼─────────────┼──────────────┤
│ LLM Call            │ Hub           │ ALL modules  │ Hub          │ CRITICAL    │ L1, L2, L3   │
├─────────────────────┼───────────────┼──────────────┼──────────────┼─────────────┼──────────────┤
│ RL Commons          │ World Model   │ ArangoDB     │ Hub,         │ HIGH        │ L2, L3       │
│                     │               │              │ World Model  │             │              │
├─────────────────────┼───────────────┼──────────────┼──────────────┼─────────────┼──────────────┤
│ World Model         │ ArangoDB      │ RL Commons,  │ RL Commons,  │ HIGH        │ L2, L3       │
│                     │               │ Hub          │ Hub          │             │              │
├─────────────────────┼───────────────┼──────────────┼──────────────┼─────────────┼──────────────┤
│ Test Reporter       │ Hub           │ ALL modules  │ Hub          │ CRITICAL    │ L1           │
└─────────────────────┴───────────────┴──────────────┴──────────────┴─────────────┴──────────────┘
```

## 2. Minimum Viable Interactions (MVI) per Module

### Data Ingestion Modules (SPARTA, YouTube, GitGet)
```python
# MVI Checklist:
✓ Can connect to data source
✓ Can fetch/download data
✓ Can transform to standard format
✓ Can send to at least one processor
✓ Can report progress to Hub
✓ Can handle errors gracefully
```

### Processing Modules (Marker, ArXiv MCP)
```python
# MVI Checklist:
✓ Can receive data from at least one source
✓ Can process multiple data formats
✓ Can output in standard format
✓ Can send to storage (ArangoDB)
✓ Can report status to Hub
✓ Can handle malformed input
```

### Storage Module (ArangoDB)
```python
# MVI Checklist:
✓ Can receive from multiple sources
✓ Can store different data types
✓ Can serve queries from intelligence modules
✓ Can maintain relationships (graph)
✓ Can report capacity to Hub
✓ Can handle concurrent access
```

### Intelligence Modules (RL Commons, World Model)
```python
# MVI Checklist:
✓ Can query storage systems
✓ Can process retrieved data
✓ Can update internal models
✓ Can share insights with other modules
✓ Can learn from feedback
✓ Can report metrics to Hub
```

### Orchestration Module (Granger Hub)
```python
# MVI Checklist:
✓ Can discover all modules
✓ Can route messages between modules
✓ Can monitor module health
✓ Can coordinate multi-module workflows
✓ Can handle module failures
✓ Can aggregate responses
```

## 3. Standard Interaction Test Scenarios

### Level 1: Binary Interactions (Two Modules)

```python
def test_sparta_to_marker():
    """Test SPARTA can send documents to Marker"""
    # 1. SPARTA downloads a document
    sparta_output = sparta.download_document("NASA-STD-8719.13C")
    assert sparta_output.status == "success"
    assert sparta_output.format == "pdf"
    
    # 2. Marker processes SPARTA's output
    marker_output = marker.process(sparta_output.data)
    assert marker_output.status == "success"
    assert marker_output.source == "sparta"
    assert len(marker_output.extracted_text) > 100

def test_marker_to_arangodb():
    """Test Marker can store in ArangoDB"""
    # 1. Marker processes a document
    marker_output = marker.process(test_pdf)
    
    # 2. ArangoDB stores Marker's output
    storage_result = arangodb.store(marker_output)
    assert storage_result.doc_id is not None
    assert storage_result.status == "stored"
    
    # 3. Verify retrieval works
    retrieved = arangodb.get(storage_result.doc_id)
    assert retrieved.text == marker_output.extracted_text
```

### Level 2: Pipeline Interactions (Three Modules)

```python
def test_youtube_arxiv_arangodb_pipeline():
    """Test full research discovery pipeline"""
    # 1. YouTube finds research video
    video = youtube.search("quantum computing lecture")
    assert video.transcript is not None
    
    # 2. ArXiv finds related papers
    papers = arxiv.find_papers(video.extracted_topics)
    assert len(papers) > 0
    
    # 3. ArangoDB stores relationships
    graph_result = arangodb.create_knowledge_graph({
        "video": video,
        "papers": papers,
        "relationships": video.paper_references
    })
    assert graph_result.nodes_created > 2
    assert graph_result.edges_created > 1
```

### Level 3: Full Ecosystem Interactions

```python
def test_full_granger_research_flow():
    """Test complete research augmentation workflow"""
    # User query through Hub
    query = "Find quantum computing vulnerabilities"
    
    # 1. Hub orchestrates the search
    hub_response = granger_hub.process_query(query)
    
    # 2. Verify multiple modules were used
    assert "sparta" in hub_response.modules_used
    assert "arxiv" in hub_response.modules_used
    assert "marker" in hub_response.modules_used
    assert "arangodb" in hub_response.modules_used
    
    # 3. Verify integrated response
    assert len(hub_response.findings) > 0
    assert hub_response.confidence_score > 0.7
    
    # 4. Verify RL optimization occurred
    assert hub_response.rl_optimization_applied == True
```

## 4. Interaction Test Patterns

### A. Message Format Compatibility Test
```python
def test_message_format_compatibility(module_a, module_b):
    """Ensure modules speak the same language"""
    # Standard message from A
    message = module_a.create_message({
        "operation": "process",
        "data": {"test": "data"}
    })
    
    # B should understand A's message
    result = module_b.handle_message(message)
    assert result.status != "error"
    assert result.error_code != "INVALID_FORMAT"
```

### B. Error Propagation Test
```python
def test_error_propagation(module_chain):
    """Ensure errors propagate correctly through the chain"""
    # Inject error in first module
    module_chain[0].force_error = True
    
    # Run the chain
    result = run_pipeline(module_chain, test_data)
    
    # Verify error reached the end
    assert result.status == "error"
    assert result.error_source == module_chain[0].name
    assert result.error_handled_by == ["hub", "error_recovery"]
```

### C. Performance Degradation Test
```python
def test_performance_under_load(module_a, module_b):
    """Ensure modules maintain performance when integrated"""
    # Baseline performance
    solo_time = timeit(lambda: module_a.process(data), number=100)
    
    # Integrated performance
    integrated_time = timeit(
        lambda: module_b.process(module_a.process(data)), 
        number=100
    )
    
    # Should not be more than 2x slower
    assert integrated_time < solo_time * 2
```

## 5. Skeleton Detection in Interactions

### Red Flags for Fake Interactions
```python
def detect_skeleton_interaction(module_a, module_b):
    """Detect if modules pretend to interact"""
    
    red_flags = []
    
    # Test 1: Response time too fast
    start = time.time()
    result = module_b.process(module_a.output())
    duration = time.time() - start
    if duration < 0.01:  # Network calls take time
        red_flags.append("INSTANT_RESPONSE")
    
    # Test 2: Same output regardless of input
    outputs = []
    for i in range(5):
        different_input = f"test_input_{i}_{random.random()}"
        output = module_b.process(module_a.process(different_input))
        outputs.append(output)
    
    if len(set(str(o) for o in outputs)) == 1:
        red_flags.append("STATIC_OUTPUT")
    
    # Test 3: No actual network traffic
    with network_monitor():
        module_b.process(module_a.output())
        if network_bytes_transferred() == 0:
            red_flags.append("NO_NETWORK_ACTIVITY")
    
    # Test 4: Success with invalid data
    try:
        result = module_b.process("INVALID_DATA_FORMAT")
        if result.status == "success":
            red_flags.append("ACCEPTS_INVALID_INPUT")
    except:
        pass  # Should throw error
    
    return red_flags
```

## 6. Integration Test Requirements

### Update TEST_VERIFICATION_TEMPLATE_GUIDE.md

Add new section after skeleton detection:

```markdown
### 4. Interaction Verification
```bash
# Verify module has required connections
grep -r "import.*granger_hub" src/ --include="*.py"
grep -r "connect.*arangodb" src/ --include="*.py"

# Check for interaction patterns
grep -r "send_to\|receive_from\|handle_message" src/ --include="*.py"

# Verify message format compliance
find . -name "*message*.py" -o -name "*protocol*.py"

# Count actual integration points
grep -r "class.*Handler\|def handle" src/ --include="*.py" | wc -l
```

⚠️ **WARNING**: A module without interaction code is not ready for testing!
```

### Update TASK_LIST_TEMPLATE_GUIDE_V2.md

Add to implementation checklist:

```markdown
### Implementation
- [ ] **PRE-CHECK**: Verify this is not a skeleton project (>30% real implementation)
- [ ] **INTERACTION-CHECK**: Verify module can communicate with at least 2 other modules
- [ ] **MESSAGE-FORMAT**: Implements standard message format for the ecosystem
- [ ] **ERROR-HANDLING**: Can handle and propagate errors from other modules
- [ ] [Original requirements...]
```

## 7. Progressive Testing Enforcement

### Testing Progression Gates

```python
class TestProgression:
    """Enforce testing progression"""
    
    def can_proceed_to_level(self, module, target_level):
        if target_level == 1:
            return self.passed_level_0(module)
        elif target_level == 2:
            return self.passed_level_1(module)
        elif target_level == 3:
            return self.passed_level_2(module)
        elif target_level == "production":
            return self.passed_all_levels(module)
    
    def passed_level_0(self, module):
        """Module works in isolation"""
        return all([
            module.unit_tests_pass,
            module.has_documentation,
            module.skeleton_ratio > 0.3
        ])
    
    def passed_level_1(self, module):
        """Module works with one other module"""
        return all([
            self.passed_level_0(module),
            len(module.successful_interactions) >= 1,
            module.message_format_compliant
        ])
```

## 8. CI/CD Integration Strategy

```yaml
# .github/workflows/granger-integration-tests.yml
name: Granger Integration Tests

on: [push, pull_request]

jobs:
  interaction-matrix:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        module_pairs:
          - [sparta, marker]
          - [marker, arangodb]
          - [arxiv, marker]
          - [youtube, arxiv]
          - [arangodb, rl_commons]
          
    steps:
      - name: Test Module Interaction
        run: |
          python test_interaction.py ${{ matrix.module_pairs[0] }} ${{ matrix.module_pairs[1] }}
          
  pipeline-tests:
    needs: interaction-matrix
    runs-on: ubuntu-latest
    steps:
      - name: Test Research Pipeline
        run: pytest tests/level_2/test_research_pipeline.py
        
      - name: Test Security Pipeline  
        run: pytest tests/level_2/test_security_pipeline.py
        
  ecosystem-test:
    needs: pipeline-tests
    runs-on: ubuntu-latest
    steps:
      - name: Full Granger Ecosystem Test
        run: pytest tests/level_3/test_full_ecosystem.py
```

## 9. Implementation Priority

### Phase 1: Critical Path (Week 1)
1. Hub ↔ All modules (orchestration must work)
2. SPARTA → Marker → ArangoDB (main pipeline)
3. LLM Call ↔ Hub (AI services must be accessible)

### Phase 2: Intelligence Layer (Week 2)
4. ArangoDB ↔ RL Commons (learning from data)
5. RL Commons ↔ World Model (self-improvement)
6. World Model → ArangoDB (knowledge updates)

### Phase 3: Complete Coverage (Week 3)
7. All remaining Level 1 interactions
8. All Level 2 pipelines
9. Full Level 3 ecosystem tests

## 10. Interaction Health Dashboard

Create a real-time dashboard showing:
- Which modules can talk to each other ✅
- Which interactions are failing ❌
- Response times between modules ⏱️
- Message format compatibility 📋
- Error rates by interaction path 🚨

This ensures we always know the true state of our ecosystem's connectivity.

## Conclusion

No module should ever be considered "complete" without demonstrating real, working interactions with its ecosystem partners. This framework ensures we build a truly integrated system, not just a collection of isolated components.