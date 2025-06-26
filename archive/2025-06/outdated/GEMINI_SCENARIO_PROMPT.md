# Prompt for Gemini to Create More Scenarios

## Context for Gemini

You are helping create test scenarios for the Claude Module Communicator, a framework that orchestrates communication between specialized modules for space cybersecurity applications.

### Available Modules and Their Capabilities:

1. **SPARTA** - Space cybersecurity knowledge base
   - NIST controls (AC, AU, SC, SI, etc.)
   - MITRE CWE database
   - MITRE ATT&CK framework
   - STIX threat intelligence

2. **Marker** - Advanced PDF extraction
   - Tables, equations, figures, sections
   - Hierarchical document structure
   - Code block extraction
   - Metadata preservation

3. **ArangoDB** - Graph database
   - Knowledge graphs
   - Relationship modeling
   - Memory bank for conversations
   - Q&A tuple generation

4. **Chat** - Modern UX interface
   - MCP server integration
   - Real-time messaging
   - File uploads
   - Rich formatting

5. **YouTube Transcripts** - Video content extraction
   - Tutorial extraction
   - Conference talks
   - Technical demonstrations
   - Timestamp mapping

6. **LLM Call (claude_max_proxy)** - Multi-LLM interface
   - Claude, GPT-4, Gemini integration
   - Response validation
   - Multi-model consensus
   - Retry logic

7. **ArXiv** - Scientific paper access
   - Paper search and download
   - Category filtering
   - Citation extraction
   - Abstract analysis

8. **Claude Test Reporter** - Test analysis
   - Test result aggregation
   - Coverage reporting
   - Failure analysis
   - Trend tracking

9. **Unsloth** - LLM fine-tuning
   - LoRA adapter training
   - 4-bit quantization
   - Student-teacher learning
   - Grokking support

10. **Marker Ground Truth** - Human feedback
    - Annotation collection
    - Quality metrics
    - Inter-annotator agreement
    - Active learning

11. **MCP Screenshot** - Screen capture & analysis
    - Full/region screenshots
    - AI-powered descriptions
    - Visual similarity search
    - Browser automation

## Task Instructions

Create 20 new scenarios that:
1. Combine 3-7 modules per scenario
2. Address real space cybersecurity challenges
3. Show creative module integration
4. Provide practical value

## Required Format

For each scenario, provide:

### [Number]. [Scenario Name]
**Modules**: Module1 → Module2 → Module3 → Module4 → Module5
**Purpose**: [One sentence describing the goal]
**Details**:
- Step 1: [Module1 action]
- Step 2: [Module2 action]
- Step 3: [Module3 action]
- Step 4: [Module4 action]
- Step 5: [Module5 action]
**Value**: [Business/security value]

## Example Scenario

### 101. Satellite Software Supply Chain Verification
**Modules**: Marker → SPARTA → YouTube → ArangoDB → LLM Call → Test Reporter
**Purpose**: Verify software components against known vulnerabilities and best practices
**Details**:
- Step 1: Extract software manifests and dependencies with Marker
- Step 2: Check each component against SPARTA vulnerability database
- Step 3: Search YouTube for security audits of major components
- Step 4: Build supply chain graph in ArangoDB
- Step 5: Analyze risks with multiple LLMs for consensus
- Step 6: Generate comprehensive supply chain risk report
**Value**: Prevents supply chain attacks on satellite systems

## Focus Areas

Please create scenarios in these categories:
1. **Advanced Threat Detection** (4 scenarios)
2. **Compliance Automation** (3 scenarios)
3. **Secure Development** (3 scenarios)
4. **Operations Security** (3 scenarios)
5. **Emerging Technologies** (3 scenarios)
6. **Cross-Domain Integration** (4 scenarios)

## Additional Guidelines

- Each scenario should tell a story of solving a real problem
- Show how modules complement each other
- Include both technical and business perspectives
- Consider constraints of space environment
- Think about scalability and automation
- Address current trends (AI, quantum, IoT, etc.)

## Creative Suggestions

- Combine modules in unexpected ways
- Use feedback loops between modules
- Create scenarios with conditional branches
- Include human-in-the-loop elements
- Consider multi-stage workflows
- Think about real-time vs batch processing

Remember: The goal is to demonstrate the power of orchestrating multiple specialized modules to solve complex space cybersecurity challenges that would be impossible with any single tool.
