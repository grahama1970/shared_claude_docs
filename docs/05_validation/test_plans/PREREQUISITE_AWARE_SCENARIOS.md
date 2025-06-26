# Prerequisite-Aware Test Scenarios

## Understanding the Testing Pipeline

Some scenarios require a fully operational pipeline:
1. **SPARTA** has ingested NIST controls, CWEs, MITRE ATT&CK
2. **Marker** has extracted documents into structured format
3. **ArangoDB** has built relationships and Q&A tuples
4. **Unsloth** has fine-tuned models with LoRA adapters

## Level 1: No Prerequisites (Can test immediately)

### 1. Basic Module Health Check
**Modules**: Each module individually
**Prerequisites**: None - just module installation
**Test**: Verify each module responds to basic queries
**Example**: 
- ArXiv: Search for "satellite security"
- YouTube: Find "SpaceX launch"
- MCP Screenshot: Capture current screen

### 2. Simple Document Processing
**Modules**: Marker
**Prerequisites**: None - just a PDF file
**Test**: Extract text from any PDF
**Value**: Tests basic Marker functionality

### 3. Memory Storage Test
**Modules**: ArangoDB
**Prerequisites**: Empty ArangoDB instance
**Test**: Store and retrieve a simple memory
**Value**: Tests basic database connectivity

## Level 2: Partial Prerequisites (Some data needed)

### 4. Security Check with Pre-loaded SPARTA
**Modules**: SPARTA → LLM Call
**Prerequisites**: SPARTA with NIST/CWE data loaded
**Test**: Check code snippet against CWE-89 (SQL Injection)
**Example from Gemini #122**: Similar pattern but simpler

### 5. Document Knowledge Extraction
**Modules**: Marker → ArangoDB
**Prerequisites**: ArangoDB running, sample PDFs
**Test**: Extract requirements and build simple graph
**Value**: Tests integration without full pipeline

### 6. Basic Fine-tuning Test
**Modules**: Unsloth
**Prerequisites**: Small dataset (can be synthetic)
**Test**: Fine-tune on 10 Q&A pairs
**Value**: Tests Unsloth without full pipeline

## Level 3: Full Pipeline Required

### 7. Vulnerability Knowledge Graph (Based on Gemini #123)
**Modules**: SPARTA → Marker → ArangoDB → Unsloth → LLM Call
**Prerequisites**: 
- SPARTA: Full CWE/NIST data ingested
- Marker: Extracted 100+ security documents
- ArangoDB: Vulnerability relationships built
- Unsloth: Fine-tuned on security Q&A
**Test**: 
1. SPARTA identifies vulnerability pattern
2. Marker extracts related docs
3. ArangoDB traverses vulnerability graph
4. Unsloth generates security recommendations
5. LLM Call validates output
**Value**: Tests complete knowledge pipeline

### 8. Compliance Automation (Like Gemini #126)
**Modules**: Marker → SPARTA → ArangoDB → Test Reporter
**Prerequisites**:
- SPARTA: NIST RMF controls loaded
- ArangoDB: Compliance graph with relationships
- Historical compliance data
**Test**: Automated compliance checking with evidence trail
**Value**: Requires full data relationships

### 9. AI-Powered Anomaly Detection (From Gemini #123)
**Modules**: ArangoDB → Unsloth → LLM Call → Test Reporter
**Prerequisites**:
- ArangoDB: Historical telemetry graph
- Unsloth: Model trained on normal vs anomalous patterns
- Q&A tuples for anomaly explanations
**Test**: Detect subtle anomalies in satellite telemetry
**Value**: Tests ML pipeline with graph data

### 10. Cross-Domain Knowledge Synthesis
**Modules**: ArXiv → Marker → ArangoDB → Unsloth → LLM Call
**Prerequisites**:
- Marker: Extracted 50+ papers
- ArangoDB: Paper relationships and citations
- Unsloth: Fine-tuned on domain Q&A
**Test**: Generate new insights from paper corpus
**Value**: Full pipeline knowledge generation

## Progressive Testing Strategy

### Phase 1: Module Installation
- Test Level 1 scenarios
- Verify basic functionality
- No data dependencies

### Phase 2: Data Loading
- Load SPARTA data
- Extract sample documents with Marker
- Build basic ArangoDB graphs
- Test Level 2 scenarios

### Phase 3: Relationship Building
- Create Q&A tuples in ArangoDB
- Build knowledge graphs
- Train initial Unsloth models
- Begin Level 3 scenarios

### Phase 4: Full Pipeline
- Complete data ingestion
- Full relationship graphs
- Fine-tuned models
- Test complex scenarios like Gemini's

## Key Insights from Gemini Response

The Gemini scenarios show patterns we should adopt:

1. **Visual Analysis**: MCP Screenshot → LLM Call (scenarios 122, 130)
2. **Knowledge Graphs**: ArangoDB central to most workflows
3. **Fine-tuned Models**: Unsloth for specialized tasks (123, 129, 135)
4. **Human Feedback**: Marker Ground Truth for validation (125, 127, 131)
5. **Multi-Model Consensus**: LLM Call with multiple models

## Testing Checkpoints

Before running Level 3 scenarios, verify:

- [ ] SPARTA has ingested NIST 800-53 controls
- [ ] SPARTA has loaded MITRE CWE database
- [ ] SPARTA has MITRE ATT&CK framework
- [ ] Marker has extracted at least 20 documents
- [ ] ArangoDB has 100+ nodes in knowledge graph
- [ ] ArangoDB has generated Q&A tuples
- [ ] Unsloth has fine-tuned at least one model
- [ ] All modules can communicate via the framework

## Scenario Complexity Matrix

| Scenario | Data Required | Modules | Prerequisites | Test Time |
|----------|--------------|---------|---------------|-----------|
| L1-Basic | None | 1 | None | < 1 min |
| L2-Integration | Some | 2-3 | Partial data | 5-10 min |
| L3-Pipeline | Full | 4-7 | Complete pipeline | 15-60 min |
| Gemini-Advanced | Full + History | 5-7 | Pipeline + Time | 30-90 min |

## Recommendation

Start with Level 1 to verify installation, then progressively load data and test higher levels. The Gemini scenarios (121-140) represent the gold standard for Level 3+ testing once the full pipeline is operational.
