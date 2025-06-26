# Pipeline Stage Testing Scenarios

## The Complete Pipeline Flow



## Stage 0: Fresh Install Testing

### Scenario 0.1: Module Heartbeat
**Test**: Each module responds to ping/version check
**Prerequisites**: None
**Command Examples**:


### Scenario 0.2: Basic I/O Test
**Test**: Each module can read input and produce output
**Prerequisites**: Sample files only
**Value**: Confirms modules are properly installed

## Stage 1: SPARTA Ingestion Testing

### Scenario 1.1: NIST Control Loading
**Modules**: SPARTA
**Prerequisites**: NIST 800-53 JSON/XML files
**Test**:


### Scenario 1.2: CWE Database Integration  
**Modules**: SPARTA
**Prerequisites**: MITRE CWE data
**Test**:


### Scenario 1.3: STIX Threat Intelligence
**Modules**: SPARTA
**Prerequisites**: STIX bundles
**Test**: Load threat actors, TTPs, relationships

## Stage 2: Marker Extraction Testing

### Scenario 2.1: Basic PDF Extraction
**Modules**: Marker
**Prerequisites**: Sample PDFs
**Test**:


### Scenario 2.2: Bulk Document Processing
**Modules**: Marker → File System
**Prerequisites**: 10+ PDFs
**Test**: Extract all, verify structured output

### Scenario 2.3: Table and Figure Extraction
**Modules**: Marker
**Prerequisites**: PDFs with complex tables
**Test**: Verify table structure preservation

## Stage 3: ArangoDB Relationship Building

### Scenario 3.1: Document to Knowledge Graph
**Modules**: Marker → ArangoDB
**Prerequisites**: Extracted documents
**Test**:


### Scenario 3.2: Q&A Tuple Generation
**Modules**: Marker → ArangoDB → LLM Call
**Prerequisites**: Extracted content + LLM access
**Test**:


### Scenario 3.3: Relationship Graph Queries
**Modules**: ArangoDB
**Prerequisites**: Populated graph
**Test**: Complex traversals work correctly

## Stage 4: Unsloth Fine-tuning Testing

### Scenario 4.1: Q&A Fine-tuning
**Modules**: ArangoDB → Unsloth
**Prerequisites**: 100+ Q&A tuples
**Test**:


### Scenario 4.2: Domain-Specific Model
**Modules**: SPARTA → ArangoDB → Unsloth
**Prerequisites**: Security-focused Q&A
**Test**: Model answers security questions better

### Scenario 4.3: LoRA Adapter Validation
**Modules**: Unsloth → LLM Call
**Prerequisites**: Fine-tuned model
**Test**: Compare base vs fine-tuned responses

## Stage 5: Full Pipeline Integration

### Scenario 5.1: Gemini #123 Implementation
**Full Pipeline Test**: AI-Powered Anomaly Detection
**Prerequisites**: ALL stages complete
**Flow**:
1. SPARTA provides normal baselines
2. Marker extracts anomaly patterns from docs
3. ArangoDB stores time-series graph
4. Unsloth fine-tunes on anomaly detection
5. System detects real anomalies

### Scenario 5.2: Knowledge Synthesis Pipeline
**Modules**: ALL
**Prerequisites**: Full pipeline operational
**Test**:


### Scenario 5.3: Compliance Automation (Gemini #126)
**Prerequisites**: Complete SPARTA + extracted policies
**Test**: Full automated compliance checking

## Progressive Test Execution Plan

### Week 1: Stage 0-1
- Install all modules
- Run heartbeat tests
- Load SPARTA data
- Verify data accessibility

### Week 2: Stage 2
- Process 50+ documents with Marker
- Verify extraction quality
- Store structured output

### Week 3: Stage 3  
- Build ArangoDB graphs
- Generate Q&A tuples
- Test graph queries

### Week 4: Stage 4
- Fine-tune first models
- Validate improvements
- Test LoRA adapters

### Week 5: Stage 5
- Run full pipeline scenarios
- Implement Gemini examples
- Stress test the system

## Critical Checkpoints

Before proceeding to next stage, verify:

**After Stage 1**:
- [ ]  returns data
- [ ]  returns data  
- [ ]  returns data

**After Stage 2**:
- [ ] Marker extracted 20+ documents
- [ ] Tables preserved with structure
- [ ] Figures extracted with captions

**After Stage 3**:
- [ ] ArangoDB has 500+ nodes
- [ ] Graph queries return connected data
- [ ] Q&A tuples generated and stored

**After Stage 4**:
- [ ] At least one model fine-tuned
- [ ] LoRA adapters saved and loadable
- [ ] Fine-tuned model shows improvement

**After Stage 5**:
- [ ] Can run Gemini scenario #123
- [ ] Knowledge synthesis produces insights
- [ ] Full pipeline completes in < 1 hour

## Debugging Tools



## Key Learning from Gemini

The Gemini scenarios assume:
1. **Rich data availability** - Thousands of documents processed
2. **Mature relationships** - Complex graph traversals work
3. **Trained models** - Specialized for each domain
4. **Historical data** - For comparison and learning

We must build up to this level systematically!
