# Example Questions for Google Gemini

## Context
After reading the GEMINI_MODULE_BRIEFING.md, here are specific questions that will help generate robust test scenarios for the module communication system.

## Scenario Generation Questions

### 1. Conflict Resolution Scenarios
"Create a test scenario where:
- ArXiv papers claim one thing about a security vulnerability
- SPARTA threat intelligence contradicts it
- YouTube experts have a third opinion
- The system must reconcile these differences using claude_max_proxy
Include specific JSON payloads and expected error handling."

### 2. Cascade Failure Testing
"Design a scenario that tests cascading failures:
- Start with YouTube API quota exhaustion
- Leading to fallback on cached data
- But ArangoDB is under heavy load
- And marker service is processing large documents
How should the system gracefully degrade?"

### 3. Real-Time Pipeline Optimization
"Create a scenario for processing a major security incident:
- 50 new ArXiv papers published simultaneously
- 100 YouTube videos released about it
- SPARTA receives 500 threat indicators
- System must process, correlate, and alert within 15 minutes
What optimizations and parallelization strategies would work?"

### 4. Data Validation Chains
"Design a validation pipeline that:
- Uses marker-ground-truth to establish baseline accuracy
- Processes 100 documents through marker with different configurations
- Compares outputs using claude_max_proxy
- Stores results in ArangoDB
- Generates accuracy reports with claude-test-reporter
Include schemas for each transformation step."

### 5. Visual Intelligence Correlation
"Create a scenario where:
- mcp-screenshot captures 5 different security dashboards
- Each shows different metrics about the same incident
- System must extract data from images
- Correlate with textual reports from SPARTA
- Build a unified view in ArangoDB
How would you handle OCR errors and visual inconsistencies?"

### 6. Emergent Behavior Discovery
"Design experiments to discover emergent behaviors:
- What happens when modules start referencing each other's outputs?
- Can the system learn new patterns without explicit programming?
- How do feedback loops form between modules?
- What unexpected capabilities arise from combinations?"

### 7. Performance Boundary Testing
"Create stress tests that explore:
- Maximum concurrent operations each module can handle
- Memory usage patterns under load
- Network bandwidth optimization
- Queue management strategies
- Graceful degradation patterns
Include specific metrics and monitoring approaches."

### 8. Security Vulnerability Scenarios
"Design security-focused tests:
- Malicious input attempting SQL injection through search queries
- Large file uploads trying to exhaust memory
- Circular reference attacks in graph database
- API key exposure risks
- Man-in-the-middle attack simulations
How should each module defend itself?"

### 9. Multi-Language Challenge
"Create a scenario processing:
- Chinese ArXiv papers
- Spanish YouTube videos
- Arabic SPARTA threat reports
- Japanese technical documentation
How does the system handle translation, transliteration, and cultural context?"

### 10. Time-Sensitive Coordination
"Design a scenario requiring precise timing:
- Monitor for a specific event across all sources
- Trigger immediate capture with mcp-screenshot when detected
- Process and analyze within 60 seconds
- Generate alerts before market close
- Handle timezone differences
What synchronization mechanisms are needed?"

## Implementation Detail Questions

### For Each Scenario, Provide:

1. **Setup Requirements**
   - Which services must be running
   - Required API keys and quotas
   - Initial data seeding
   - Performance baselines

2. **Execution Steps**
   ```python
   # Specific code showing module interactions
   # Error handling patterns
   # Timeout configurations
   # Retry strategies
   ```

3. **Validation Criteria**
   - Success metrics
   - Acceptable error rates
   - Performance thresholds
   - Data integrity checks

4. **Failure Modes**
   - Expected failures
   - Recovery procedures
   - Rollback strategies
   - Alert mechanisms

5. **Edge Cases**
   - Boundary conditions
   - Null/empty data handling
   - Malformed inputs
   - Resource exhaustion

## Advanced Integration Questions

### 1. Schema Evolution
"How should the system handle schema changes in modules over time? Design a test for backward compatibility when marker adds new fields to its output that arangodb doesn't expect."

### 2. Module Discovery
"Create a scenario where modules can discover each other's capabilities dynamically. How would arxiv-mcp-server learn that marker has new PDF processing features?"

### 3. Distributed Transactions
"Design a test for distributed transaction patterns: If processing fails at step 3 of 5, how do we rollback changes in modules 1 and 2?"

### 4. Caching Strategies
"Create scenarios testing different caching patterns:
- When should results be cached vs. recomputed?
- How do modules invalidate each other's caches?
- What's the optimal cache size for each module?"

### 5. Module Versioning
"Design tests for handling multiple versions:
- Running marker v1 and v2 simultaneously
- Gradual migration strategies
- Feature flag testing
- A/B testing module improvements"

## Creative Combination Challenges

### 1. The Knowledge Loop
"Create a self-improving system where:
- System analyzes its own test reports
- Identifies weak points
- Searches for solutions in ArXiv
- Implements improvements
- Tests itself again"

### 2. The Translation Pipeline
"YouTube video → Transcript → Translation → Document → Graph → Visualization → Screenshot → Analysis → Report
Test data fidelity through each transformation."

### 3. The Controversy Detector
"Build a system that:
- Identifies controversial topics across sources
- Maps different viewpoints
- Tracks opinion evolution over time
- Predicts consensus formation
- Generates balanced reports"

### 4. The Research Assistant
"Simulate a complete research workflow:
- Question formulation
- Literature search
- Video tutorial discovery
- Experiment design
- Result validation
- Paper writing assistance"

### 5. The Security Analyst
"24/7 monitoring system that:
- Watches multiple threat feeds
- Correlates indicators
- Predicts attack vectors
- Generates defensive strategies
- Tests its own predictions"

## Output Format Request

For each scenario Gemini creates, request:

1. **Scenario Name and Objective**
2. **Modules Involved** (with specific capabilities used)
3. **Data Flow Diagram**
4. **Implementation Code** (Python with async/await)
5. **Test Assertions**
6. **Performance Expectations**
7. **Failure Recovery Plans**
8. **Success Metrics**
9. **Lessons Learned** (what this tests about the system)
10. **Variations** (how to make it harder/easier)

These questions should inspire Gemini to create comprehensive, challenging, and creative test scenarios that will truly validate the robustness and flexibility of the module communication system.
