# Feedback and Additional Guidance for Gemini

## What You Did Well ✅

Your "Adaptive Threat Intelligence & Mitigation Validation" scenario shows you understand:
- The module communication patterns (MCP, HTTP, CLI)
- How to chain multiple modules together
- Proper use of schemas and API calls
- Error handling basics
- Data flow between modules

## What We Need More Of 🎯

### 1. **More Diverse Scenarios**
We need 5-10 different scenarios, not just one. Each should test different aspects:
- Performance limits
- Failure cascades
- Race conditions
- Schema evolution
- Module version conflicts

### 2. **Edge Cases and Stress Testing**
Your scenario is too "happy path". We need scenarios that break things:

```python
# Example: What happens when we overwhelm the system?
tasks = []
for i in range(1000):  # Stress test with 1000 concurrent requests
    tasks.append(comm.execute_mcp_tool_command(
        tool_name="arxiv-mcp-server",
        command="search_papers",
        args={"query": f"test_{i}", "max_results": 100}
    ))
results = await asyncio.gather(*tasks, return_exceptions=True)
# How many succeed? How many timeout? How does the system degrade?
```

### 3. **Module Interaction Conflicts**
Test what happens when modules give conflicting information:

```python
# Scenario: ArXiv says vulnerability is theoretical, SPARTA says it's actively exploited
arxiv_result = {"severity": "low", "exploitable": "theoretical"}
sparta_result = {"severity": "critical", "active_exploits": 127}
# How does the system reconcile this? Which source wins? How is the conflict logged?
```

### 4. **Cascading Failures**
Show how one module failure affects others:

```python
# Scenario: ArangoDB goes down mid-pipeline
# Step 1: Start processing 50 documents
# Step 2: After 25 documents, ArangoDB fails
# Step 3: What happens to:
#   - Documents already processed?
#   - Documents in flight?
#   - Downstream modules waiting for graph data?
#   - Recovery when ArangoDB comes back?
```

### 5. **Schema Evolution Testing**
What happens when modules update their schemas?

```python
# Old marker schema
old_response = {"text": "content", "pages": 10}

# New marker schema adds fields
new_response = {"text": "content", "pages": 10, "language": "en", "confidence": 0.95}

# How do downstream modules handle the new fields?
# What about when fields are removed or renamed?
```

## Specific Scenarios We Need

### Scenario A: Rate Limit Cascade
```markdown
When YouTube API hits its 100/day limit:
1. System switches to cached data
2. But cache is stale (>30 days)
3. Tries ArXiv as alternative source
4. ArXiv rate limits kick in (3/sec)
5. System must intelligently throttle and prioritize
```

### Scenario B: The Contradiction Resolver
```markdown
Same event reported differently:
- ArXiv paper: "Vulnerability patched in v2.1"
- YouTube video: "Exploit still works on v2.1"  
- SPARTA: "No patches available"
- System must determine truth using:
  - Timestamp analysis
  - Source credibility scoring
  - Community consensus
  - Visual evidence from screenshots
```

### Scenario C: The Infinite Loop Trap
```markdown
Module A depends on Module B
Module B depends on Module C
Module C depends on Module A
- How does the system detect circular dependencies?
- What happens with recursive knowledge graph queries?
- How are infinite loops prevented?
```

### Scenario D: The Memory Explosion
```markdown
Processing a 1000-page PDF:
- Marker needs 8GB RAM
- But system only has 6GB available
- Meanwhile, ArangoDB is consuming 3GB
- How does the system:
  - Detect memory pressure?
  - Prioritize which modules get resources?
  - Implement partial processing?
  - Clean up gracefully?
```

### Scenario E: The Time Traveler
```markdown
Historical analysis with temporal conflicts:
- User queries about an event from 2023
- But YouTube videos are from 2024 discussing it
- ArXiv papers from 2025 analyze it retrospectively
- System must maintain temporal consistency
- How are anachronisms detected and handled?
```

## Implementation Patterns to Test

### 1. **Parallel vs Sequential Processing**
```python
# Test: Which is faster and more reliable?

# Sequential
for paper in papers:
    result = await process_paper(paper)
    
# Parallel with limits
sem = asyncio.Semaphore(5)
async def process_with_limit(paper):
    async with sem:
        return await process_paper(paper)
        
# Parallel unlimited (stress test)
results = await asyncio.gather(*[process_paper(p) for p in papers])
```

### 2. **Retry Strategies**
```python
# Test different retry patterns
async def retry_with_exponential_backoff(func, max_attempts=5):
    for attempt in range(max_attempts):
        try:
            return await func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            wait_time = 2 ** attempt + random.uniform(0, 1)
            await asyncio.sleep(wait_time)

# vs Circuit Breaker pattern
# vs Retry with fallback to different module
```

### 3. **Cache Invalidation Patterns**
```python
# Test: When should caches be invalidated?
scenarios = [
    "New paper contradicts cached data",
    "Time-based expiration",
    "Size-based eviction",
    "Explicit invalidation signal",
    "Cascade invalidation (A changes, so B and C must update)"
]
```

## Metrics to Measure

For each scenario, report:

1. **Performance Metrics**
   - Latency (p50, p95, p99)
   - Throughput (requests/second)
   - Resource usage (CPU, RAM, network)
   - Queue depths

2. **Reliability Metrics**
   - Success rate
   - Retry count
   - Timeout rate
   - Error types and frequencies

3. **Data Quality Metrics**
   - Schema validation failures
   - Data consistency scores
   - Contradiction detection rate
   - Information completeness

4. **System Behavior**
   - Graceful degradation patterns
   - Recovery time
   - Cascade failure impact
   - Emergent behaviors observed

## Output Format Example

For each scenario, provide:

```markdown
# Scenario: [Name]

## Objective
What system behavior/limit are we testing?

## Setup
- Required services: [list]
- Initial data: [description]
- Configuration: [special settings]

## Implementation
```python
# Complete, runnable code
```

## Expected Behavior
- Normal case: [what should happen]
- Edge cases: [list of edge cases and expected handling]
- Failure modes: [how it should fail gracefully]

## Actual Results Template
```json
{
  "performance": {
    "latency_p95": "250ms",
    "throughput": "45 req/s",
    "resource_peak": {"cpu": "87%", "ram": "5.2GB"}
  },
  "reliability": {
    "success_rate": "94.3%",
    "common_errors": ["timeout", "rate_limit"],
    "mttr": "45 seconds"
  },
  "insights": [
    "System degrades gracefully above 40 req/s",
    "Memory pressure causes cascade at 6GB",
    "Contradiction detection improves with 3+ sources"
  ]
}
```

## Emergent Behaviors to Look For

1. **Self-Organization**: Do modules start optimizing their interactions without explicit programming?
2. **Collective Intelligence**: Does accuracy improve when modules collaborate vs work in isolation?
3. **Adaptive Behavior**: Does the system learn from failures and adjust strategies?
4. **Swarm Effects**: Do patterns emerge from many small module interactions?
5. **Feedback Loops**: Do modules create reinforcing or balancing loops?

## Creative Challenges

### The Shape-Shifter Test
Create data that changes format as it flows through modules. How well does the system adapt?

### The Telephone Game
Pass information through all 11 modules sequentially. How much is lost or distorted?

### The Democracy Test
Have multiple modules "vote" on an answer. How does consensus emerge?

### The Evolution Test
Start with simple queries and gradually make them more complex. At what point does the system break?

### The Contradiction Factory
Deliberately create contradictory data. Can the system identify and quarantine it?

## Remember

We're not just testing if modules can talk to each other. We're testing:
- How they behave under stress
- How they handle ambiguity
- How they recover from failures
- How they create emergent capabilities
- How they maintain data quality
- How they optimize performance
- How they adapt to change

Your next response should include 5-7 diverse scenarios following this guidance, each testing different aspects of the system.
