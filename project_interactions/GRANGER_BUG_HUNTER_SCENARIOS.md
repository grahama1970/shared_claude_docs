# GRANGER Bug Hunter Scenarios - Complete Testing Framework

## Overview

This comprehensive framework includes ALL unique scenarios from across the Granger ecosystem, designed to autonomously hunt for bugs, weaknesses, and missing functionality through real module interactions.

**Core Mission**: Find real bugs through creative, systematic testing that pushes modules beyond their comfort zones.

## Testing Philosophy

1. **Real Systems Only** - No mocks, no simulations (per TEST_VERIFICATION_TEMPLATE_GUIDE)
2. **Progressive Complexity** - Level 0-3 structure with creativity ratings
3. **Bug-First Design** - Every test designed to expose weaknesses
4. **Autonomous Execution** - Self-directing test discovery and execution
5. **Evidence-Based** - All findings must be reproducible with logs
6. **Include WIP Modules** - Test work-in-progress modules like memvid to find early bugs
7. **Multi-AI Verification** - Perplexity and Gemini must grade actual responses against expected outcomes

## AI Grading Mechanism

For each scenario, the testing framework will:
1. **Execute** the actual test and capture the response
2. **Compare** the actual response to the expected outcome
3. **Grade** using both Perplexity and Gemini to verify:
   - Does the actual response match the expected behavior?
   - Are there any deviations that indicate bugs?
   - Is the module behaving as originally designed?

Example grading prompt:
```
Scenario: [Name]
Expected Result: [What should happen]
Actual Response: [What actually happened]
Grade this response: Does it meet expectations? What bugs are indicated?
```

---

# Level 0: Single Module Tests (10 Scenarios)

## Scenario 1: SPARTA CVE Search
**Modules**: sparta
**Bug Target**: CVE data retrieval and parsing
**Expected Result**: 
- Should return structured CVE data with fields: ID, description, severity, affected systems
- Response time 1-5 seconds for typical query
- Empty results for non-existent CVEs with clear message
- Handle malformed CVE IDs gracefully

## Scenario 2: ArXiv Paper Search
**Modules**: arxiv-mcp-server
**Bug Target**: Research paper search and metadata extraction
**Expected Result**:
- Returns list of papers with title, authors, abstract, PDF URL
- Handles special characters in queries (e.g., "Müller", "∇f(x)")
- Pagination works correctly for large result sets
- Empty query returns error, not all papers

## Scenario 3: ArangoDB Storage Operations
**Modules**: arangodb
**Bug Target**: Graph database CRUD operations
**Expected Result**:
- Insert returns document ID
- Query returns matching documents or empty array
- Graph traversal respects depth limits
- Handles concurrent operations without data corruption
- Connection failures retry with exponential backoff

## Scenario 4: YouTube Transcript Download
**Modules**: youtube_transcripts
**Bug Target**: Video transcript extraction
**Expected Result**:
- Returns full transcript with timestamps
- Handles videos without transcripts gracefully
- Works with different languages
- Private/deleted videos return appropriate error
- Rate limiting prevents API bans

## Scenario 5: Marker PDF Conversion
**Modules**: marker
**Bug Target**: Document format conversion
**Expected Result**:
- Converts PDF to clean Markdown preserving structure
- Handles scanned PDFs with OCR
- Preserves tables and lists formatting
- Large files (>100MB) process without OOM
- Corrupted PDFs return error, not crash

## Scenario 6: LLM Call Routing
**Modules**: llm_call
**Bug Target**: Multi-provider LLM interface
**Expected Result**:
- Routes to correct provider based on config
- Fallback works when primary provider fails
- Token limits respected (no truncation surprises)
- Cost tracking accurate
- Handles rate limits gracefully

## Scenario 7: GitGet Repository Analysis
**Modules**: gitget
**Bug Target**: GitHub repository analysis
**Expected Result**:
- Returns repo metadata: language, size, structure
- Handles large repos without timeout
- Private repos fail with clear auth error
- Analyzes code quality metrics correctly
- Submodules handled properly

## Scenario 8: World Model State Tracking
**Modules**: world_model
**Bug Target**: System state persistence
**Expected Result**:
- State updates persist across restarts
- Concurrent updates don't cause race conditions
- State queries return consistent snapshots
- Rollback capability works
- Memory usage bounded for long sessions

## Scenario 9: RL Commons Decision Making
**Modules**: rl_commons
**Bug Target**: Reinforcement learning optimization
**Expected Result**:
- Bandit selection improves over time
- Exploration/exploitation balance maintained
- Rewards update Q-values correctly
- Handles cold start gracefully
- Performance metrics accessible

## Scenario 10: Test Reporter Generation
**Modules**: claude-test-reporter
**Bug Target**: Test report generation and formatting
**Expected Result**:
- Generates valid Markdown/HTML reports
- Includes all test results (no data loss)
- Handles test failures gracefully
- Performance metrics accurate
- Report accessible via web interface

---

# Level 1: Binary Module Interactions (10 Scenarios)

## Scenario 11: ArXiv to Marker Pipeline
**Modules**: arxiv-mcp-server, marker
**Bug Target**: PDF download and conversion pipeline
**Expected Result**:
- ArXiv provides valid PDF URL
- Marker successfully converts downloaded PDF
- Metadata preserved through pipeline
- Large papers (>50MB) handled
- Network failures retry appropriately
- Unicode in titles/content preserved

## Scenario 12: YouTube to SPARTA Pipeline
**Modules**: youtube_transcripts, sparta
**Bug Target**: Security content extraction and analysis
**Expected Result**:
- YouTube provides security-related transcript
- SPARTA identifies CVEs mentioned in transcript
- Timestamps align with CVE mentions
- False positive rate <10%
- Handles multiple CVE formats
- Cross-references work correctly

## Scenario 13: Marker to ArangoDB Pipeline
**Modules**: marker, arangodb
**Bug Target**: Document storage and indexing
**Expected Result**:
- Converted Markdown stored with structure preserved
- Full-text search works on content
- Metadata stored in separate collection
- Relationships between documents maintained
- Large documents chunked appropriately
- Deduplication prevents redundant storage

## Scenario 14: ArangoDB to Unsloth Pipeline
**Modules**: arangodb, unsloth
**Bug Target**: Training data preparation
**Expected Result**:
- Graph queries return training-ready data
- Data format matches Unsloth requirements
- Sampling maintains distribution
- Incremental updates work
- Memory efficient for large datasets
- Validation split maintained correctly

## Scenario 15: GitGet to ArangoDB Pipeline
**Modules**: gitget, arangodb
**Bug Target**: Code repository indexing
**Expected Result**:
- Repository structure preserved in graph
- File relationships mapped correctly
- Commit history accessible
- Large repos indexed incrementally
- Binary files handled appropriately
- Search queries performant

## Scenario 16: World Model RL Pipeline
**Modules**: world_model, rl_commons
**Bug Target**: Learning from system state
**Expected Result**:
- State changes trigger RL updates
- Reward signals computed correctly
- Policy improvements measurable
- Exploration decreases over time
- Multi-armed bandit convergence
- State-action pairs logged

## Scenario 17: SPARTA to ArangoDB Pipeline
**Modules**: sparta, arangodb
**Bug Target**: Security data persistence
**Expected Result**:
- CVE data stored with all fields
- Relationships between CVEs maintained
- Search by severity/date works
- Bulk inserts optimized
- Updates don't duplicate
- Audit trail maintained

## Scenario 18: LLM Call to Test Reporter Pipeline
**Modules**: llm_call, claude-test-reporter
**Bug Target**: AI-powered test analysis
**Expected Result**:
- LLM analyzes test failures correctly
- Insights included in report
- Cost tracked per analysis
- Handles timeouts gracefully
- Multiple LLM results compared
- Formatting preserved in report

## Scenario 19: Granger Hub Coordination Pipeline
**Modules**: granger_hub, rl_commons
**Bug Target**: Central orchestration optimization
**Expected Result**:
- Hub routes requests optimally
- RL improves routing over time
- Load balancing works
- Failure recovery automatic
- Metrics collected accurately
- Priority queuing respected

## Scenario 20: Unsloth to LLM Call Pipeline
**Modules**: unsloth, llm_call
**Bug Target**: Model deployment pipeline
**Expected Result**:
- Fine-tuned models callable via LLM interface
- Performance better than base model
- Memory usage acceptable
- Inference time reasonable
- Fallback to base model works
- A/B testing supported

---

# Level 2: Multi-Module Workflows (10 Scenarios)

## Scenario 21: Research to Training Workflow
**Modules**: arxiv-mcp-server, marker, arangodb, unsloth
**Bug Target**: End-to-end research pipeline
**Expected Result**:
- Papers found → converted → stored → used for training
- Quality filtering removes low-value papers
- Deduplication prevents redundant training
- Incremental training supported
- Progress tracking accurate
- Results measurably improved

## Scenario 22: Security Monitoring System
**Modules**: sparta, youtube_transcripts, llm_call, claude-test-reporter
**Bug Target**: Multi-source security intelligence
**Expected Result**:
- CVEs from SPARTA correlated with YouTube discussions
- LLM synthesizes actionable insights
- Reports generated automatically
- Real-time alerting works
- False positives minimized
- Historical analysis available

## Scenario 23: Knowledge Graph Builder
**Modules**: arxiv-mcp-server, gitget, arangodb, world_model
**Bug Target**: Multi-source knowledge integration
**Expected Result**:
- Papers linked to implementing code
- Graph relationships meaningful
- Queries traverse correctly
- Updates maintain consistency
- Visualization possible
- Export formats supported

## Scenario 24: Adaptive Learning System
**Modules**: youtube_transcripts, marker, llm_call, rl_commons
**Bug Target**: Content-based learning optimization
**Expected Result**:
- Tutorial content extracted and understood
- Key concepts identified correctly
- Learning path optimization works
- Progress tracked accurately
- Recommendations improve
- Personalization effective

## Scenario 25: Real-Time Collaboration
**Modules**: granger_hub, world_model, claude-test-reporter, arangodb
**Bug Target**: Multi-user coordination
**Expected Result**:
- Concurrent users don't conflict
- State synchronized correctly
- Changes audited properly
- Performance scales linearly
- Rollback capabilities work
- Permissions enforced

## Scenario 26: Code Enhancement Workflow
**Modules**: gitget, llm_call, marker, sparta
**Bug Target**: Automated code improvement
**Expected Result**:
- Repository analyzed for issues
- Security vulnerabilities identified
- Enhancement suggestions valid
- Documentation generated
- PR-ready output produced
- No breaking changes introduced

## Scenario 27: Document QA System
**Modules**: marker, llm_call, arangodb, claude-test-reporter
**Bug Target**: Document understanding pipeline
**Expected Result**:
- Documents parsed correctly
- Questions answered accurately
- Sources cited properly
- Multi-document QA works
- Performance acceptable
- Results reproducible

## Scenario 28: Hardware Verification QA
**Modules**: sparta, marker, llm_call, arangodb
**Bug Target**: Hardware security analysis
**Expected Result**:
- Hardware specs extracted
- Vulnerabilities identified
- Mitigations suggested
- Compliance checked
- Reports comprehensive
- Updates tracked

## Scenario 29: Scientific Paper Validation
**Modules**: arxiv-mcp-server, marker, llm_call, world_model
**Bug Target**: Research validation pipeline
**Expected Result**:
- Claims extracted correctly
- Methodology assessed
- Results verified when possible
- Citations checked
- Reproducibility scored
- Peer review assisted

## Scenario 30: Multi-Step Processing
**Modules**: youtube_transcripts, marker, sparta, arangodb
**Bug Target**: Complex pipeline reliability
**Expected Result**:
- Each step completes successfully
- Data transforms correctly
- No information lost
- Error recovery works
- Progress resumable
- Results traceable

---

# Level 3: Ecosystem-Wide Tests (11 Scenarios)

## Scenario 31: Full Research Pipeline
**Modules**: arxiv-mcp-server, youtube_transcripts, marker, llm_call, arangodb, unsloth
**Bug Target**: Complete research to model pipeline
**Expected Result**:
- Multi-source research synthesis works
- Knowledge graph built correctly
- Training improves model performance
- Insights actionable
- Process automated
- Quality maintained throughout

## Scenario 32: YouTube Research Flow
**Modules**: youtube_transcripts, arxiv-mcp-server, gitget, marker, arangodb
**Bug Target**: Video-driven research automation
**Expected Result**:
- Tutorial leads to paper discovery
- Related code repositories found
- Knowledge integrated properly
- Relationships mapped
- Search works across sources
- Updates incremental

## Scenario 33: Security Analysis Workflow
**Modules**: sparta, gitget, llm_call, marker, claude-test-reporter
**Bug Target**: Comprehensive security assessment
**Expected Result**:
- Vulnerabilities found across sources
- Risk assessment accurate
- Remediation practical
- Reports comprehensive
- Tracking effective
- Compliance verified

## Scenario 34: Autonomous Learning Loop
**Modules**: All core modules
**Bug Target**: Self-improving system
**Expected Result**:
- System identifies knowledge gaps
- Automatically seeks information
- Integrates new knowledge
- Performance improves measurably
- No degradation over time
- Explanation capability maintained

## Scenario 35: Multi-Agent Collaboration
**Modules**: granger_hub, llm_call, rl_commons, world_model, claude-test-reporter
**Bug Target**: Distributed intelligence coordination
**Expected Result**:
- Agents coordinate effectively
- No conflicts or deadlocks
- Collective intelligence emerges
- Load balanced properly
- Failures handled gracefully
- Results better than individual agents

## Scenario 36: Cross-Domain Synthesis
**Modules**: All input and processing modules
**Bug Target**: Interdisciplinary integration
**Expected Result**:
- Connections found between domains
- Novel insights generated
- Contradictions identified
- Synthesis meaningful
- Applications suggested
- Quality maintained

## Scenario 37: Real-Time Monitoring
**Modules**: All modules with granger_hub orchestration
**Bug Target**: System-wide observability
**Expected Result**:
- All modules report health
- Metrics collected properly
- Alerts triggered appropriately
- Dashboards update real-time
- Historical data available
- Anomalies detected

## Scenario 38: Adaptive Optimization
**Modules**: rl_commons, world_model, granger_hub, all processing modules
**Bug Target**: System-wide performance optimization
**Expected Result**:
- Bottlenecks identified automatically
- Resources allocated optimally
- Performance improves over time
- No oscillation or instability
- Explanations available
- Rollback possible

## Scenario 39: Knowledge Graph Enrichment
**Modules**: All data sources, arangodb, llm_call, world_model
**Bug Target**: Automated knowledge expansion
**Expected Result**:
- Graph grows meaningfully
- Quality maintained
- Relationships accurate
- Queries performant at scale
- Pruning effective
- Export/import works

## Scenario 40: Full Granger Ecosystem Test
**Modules**: Every module in system
**Bug Target**: Complete system integration
**Expected Result**:
- All modules accessible
- Data flows correctly
- No bottlenecks under load
- Graceful degradation
- Recovery automatic
- Performance acceptable

## Scenario 41: Quantum Safe Crypto Migration
**Modules**: sparta, gitget, llm_call, marker, arangodb
**Bug Target**: Quantum cryptography transition
**Expected Result**:
- Current crypto identified
- Quantum vulnerabilities found
- Migration path generated
- Code changes valid
- Documentation complete
- No security gaps introduced

---

# Level 4: UI-Driven Scenarios (1 Scenario)

## Scenario 42: Chat UI Research Test
**Modules**: chat, llm_call, arxiv-mcp-server, marker, arangodb
**Bug Target**: UI-driven research workflow
**Expected Result**:
- Natural language queries understood
- Research automated correctly
- Results presented clearly
- Interactions logged
- Context maintained
- Export functionality works

---

# Bug Hunter Unique Scenarios (25 Additional)

## Scenario 43: Module Resilience Testing
**Bug Target**: Input validation, error handling, resource limits
**Expected Result**:
- Malformed inputs rejected gracefully
- Resource exhaustion prevented
- Error messages informative but secure
- Recovery automatic
- No crashes or hangs
- Performance degraded gracefully

## Scenario 44: Performance Degradation Hunter
**Bug Target**: Memory leaks, connection pools, cache efficiency
**Expected Result**:
- Memory usage stable over time
- Connections properly pooled
- Caches effective
- No gradual slowdown
- Metrics available
- Cleanup automatic

## Scenario 45: API Contract Violation Hunter
**Bug Target**: Schema consistency, versioning, deprecation
**Expected Result**:
- Responses match documented schema
- Versioning honored
- Deprecation warnings present
- Backwards compatibility maintained
- Error formats consistent
- Documentation accurate

## Scenario 46: Message Format Mismatch Hunter
**Bug Target**: Inter-module communication formats
**Expected Result**:
- All modules speak same protocol
- Encoding consistent (UTF-8)
- Large messages handled
- Compression optional
- Encryption available
- Versioning supported

## Scenario 47: State Corruption Hunter
**Bug Target**: Concurrent access, transaction integrity
**Expected Result**:
- No race conditions
- Transactions atomic
- Rollback works
- State recoverable
- Audit trail complete
- Locks minimal

## Scenario 48: Integration Failure Pattern Hunter
**Bug Target**: Module dependency failures
**Expected Result**:
- Failures detected quickly
- Fallbacks activate
- Recovery automatic
- No cascade failures
- Alerts generated
- State consistent

## Scenario 49: Resource Contention Hunter
**Bug Target**: Deadlocks, starvation, priority inversion
**Expected Result**:
- No deadlocks possible
- Fair resource allocation
- Priority respected
- Timeouts prevent hanging
- Monitoring available
- Manual intervention possible

## Scenario 50: Error Cascade Hunter
**Bug Target**: Error propagation, retry storms
**Expected Result**:
- Errors contained
- Exponential backoff works
- Circuit breakers trip
- No retry storms
- Root cause identifiable
- Recovery coordinated

## Scenario 51: Data Loss Hunter
**Bug Target**: Persistence, replication, backup
**Expected Result**:
- No data loss on crash
- Replication lag acceptable
- Backups restorable
- Point-in-time recovery
- Integrity checks pass
- Archive accessible

## Scenario 52: Security Boundary Hunter
**Bug Target**: Authentication, authorization, audit
**Expected Result**:
- Auth required everywhere
- Permissions enforced
- Audit trail complete
- No privilege escalation
- Sessions timeout
- Secrets protected

## Scenario 53: Configuration Drift Hunter
**Bug Target**: Config synchronization, validation
**Expected Result**:
- Configs synchronized
- Validation prevents errors
- Changes tracked
- Rollback possible
- Documentation current
- Templates provided

## Scenario 54: Dependency Version Hunter
**Bug Target**: Package conflicts, security updates
**Expected Result**:
- No version conflicts
- Security updates applied
- Dependencies minimal
- Licenses compatible
- Updates tested
- Rollback possible

## Scenario 55: Network Partition Hunter
**Bug Target**: Split brain, consistency
**Expected Result**:
- Partitions detected
- Consistency maintained
- Healing automatic
- No data divergence
- Alerts generated
- Manual override available

## Scenario 56: Time Synchronization Hunter
**Bug Target**: Clock skew, ordering, timeouts
**Expected Result**:
- Clocks synchronized
- Event ordering consistent
- Timeouts appropriate
- No future timestamps
- Drift monitored
- NTP configured

## Scenario 57: Chaos Engineering Hunter
**Bug Target**: Random failures, recovery
**Expected Result**:
- Random failures tolerated
- Recovery automatic
- No data loss
- Performance acceptable
- Alerts appropriate
- Documentation helpful

## Scenario 58: Compliance Validation Hunter
**Bug Target**: GDPR, logging, retention
**Expected Result**:
- PII handled correctly
- Logs appropriately filtered
- Retention policies enforced
- Right to deletion works
- Consent tracked
- Reports available

## Scenario 59: Cross-Module Security Hunter
**Bug Target**: SSRF, injection, traversal
**Expected Result**:
- No SSRF possible
- Injection prevented
- Path traversal blocked
- Input sanitized
- Output encoded
- Headers secure

## Scenario 60: Load Distribution Hunter
**Bug Target**: Hot spots, balance, fairness
**Expected Result**:
- Load evenly distributed
- No hot spots
- Fairness maintained
- Scaling smooth
- Metrics accurate
- Rebalancing automatic

## Scenario 61: Cache Coherency Hunter
**Bug Target**: Stale data, invalidation, consistency
**Expected Result**:
- Caches consistent
- Invalidation works
- No stale reads
- Write-through reliable
- Monitoring available
- Manual flush possible

## Scenario 62: Metric Accuracy Hunter
**Bug Target**: Counter drift, sampling, aggregation
**Expected Result**:
- Metrics accurate
- No counter drift
- Sampling representative
- Aggregation correct
- Export reliable
- Dashboards current

## Scenario 63: Log Correlation Hunter
**Bug Target**: Trace IDs, context, search
**Expected Result**:
- Traces complete
- Context preserved
- Search effective
- No log loss
- Rotation works
- Archive searchable

## Scenario 64: Feature Flag Hunter
**Bug Target**: Flag consistency, rollout, rollback
**Expected Result**:
- Flags consistent
- Rollout gradual
- Rollback instant
- No flag drift
- Audit complete
- Testing easy

## Scenario 65: Deployment Safety Hunter
**Bug Target**: Rolling updates, rollback, validation
**Expected Result**:
- Zero downtime updates
- Rollback reliable
- Validation comprehensive
- No partial states
- Progress visible
- Abort possible

## Scenario 66: Documentation Accuracy Hunter
**Bug Target**: API docs, examples, tutorials
**Expected Result**:
- Docs match reality
- Examples run correctly
- Tutorials complete
- Links work
- Search effective
- Feedback incorporated

## Scenario 67: Memvid Integration Test
**Bug Target**: Memory video generation pipeline
**Expected Result**:
- Videos generated correctly
- Memory visualization accurate
- Performance acceptable
- Format compatible
- Errors handled
- Output accessible

---

## Test Execution Guidelines

### For Each Scenario:
1. **Setup**: Prepare clean environment
2. **Execute**: Run actual modules (no mocks)
3. **Capture**: Record all responses and timings
4. **Analyze**: Compare to expected results
5. **Grade**: Use Perplexity + Gemini to assess
6. **Report**: Document bugs found with evidence

### Success Criteria:
- Response matches expected result: PASS
- Minor deviations but functional: WARN  
- Major deviations or failures: FAIL
- Crashes or hangs: CRITICAL

### Bug Severity:
- **Critical**: Data loss, security breach, crashes
- **High**: Feature broken, performance severely degraded
- **Medium**: Incorrect behavior, poor UX
- **Low**: Minor issues, cosmetic problems

Remember: We're hunting for REAL bugs in REAL systems. Every test must use actual modules and verify actual behavior!