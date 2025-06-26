# Level 2: Moderate Everyday Scenarios

## 1. Research and Code Example
**Modules**: YouTube Transcripts → ArXiv
**Task**: "What does Ronan from Trelis Research say about Monte Carlo for improving inference? Show me code from his repo"
**Steps**:
- YouTube searches Trelis Research channel for Monte Carlo content
- Extract relevant transcript segments
- ArXiv searches for related papers he might reference
- Return quotes + code snippets + paper links
**Time**: 2-3 minutes

## 2. PDF Table to Q&A
**Modules**: MCP Screenshot → Marker → LLM Call
**Task**: "Screenshot table on page 43, create 10 Q&A pairs, verify with Marker extraction"
**Steps**:
- MCP Screenshot captures page 43 table
- Marker extracts the same table data
- LLM Call generates 10 Q&A pairs from content
- Compare screenshot vs extraction for accuracy
**Time**: 3-5 minutes

## 3. Paper Support Analysis
**Modules**: ArXiv → LLM Call
**Task**: "Get top 4 recent papers that support the claim 'LoRA improves fine-tuning efficiency'"
**Steps**:
- ArXiv searches for LoRA efficiency papers
- LLM Call analyzes abstracts for support strength
- Rank by relevance and recency
- Return summaries with confidence scores
**Time**: 2-3 minutes

## 4. Memory-Augmented Search
**Modules**: ArangoDB → ArXiv
**Task**: "Find papers related to topics we discussed last month"
**Steps**:
- ArangoDB retrieves last month's conversations
- Extract key technical terms
- ArXiv searches using those terms
- Return relevant papers
**Time**: 2-4 minutes

## 5. Video to Implementation
**Modules**: YouTube Transcripts → Marker
**Task**: "Find FastAPI tutorial and match with my API spec document"
**Steps**:
- YouTube finds FastAPI tutorials
- Extract code examples from transcripts
- Marker extracts API endpoints from your spec
- Show which tutorials cover your endpoints
**Time**: 3-5 minutes

## 6. Vulnerability Cross-Check
**Modules**: Marker → SPARTA
**Task**: "Extract code from this PDF and check for security issues"
**Steps**:
- Marker extracts code blocks
- SPARTA checks each against CWE database
- Return vulnerabilities with line numbers
**Time**: 2-4 minutes

## 7. Build Expertise Graph
**Modules**: YouTube Transcripts → ArangoDB
**Task**: "Map what experts say about transformer architectures"
**Steps**:
- YouTube extracts multiple expert videos
- Parse opinions and claims
- ArangoDB builds expert→opinion graph
- Visualize consensus/disagreements
**Time**: 5-8 minutes

## 8. Screenshot Documentation
**Modules**: MCP Screenshot → Test Reporter
**Task**: "Document this bug with screenshots and generate report"
**Steps**:
- MCP Screenshot captures bug states
- Add annotations and timestamps
- Test Reporter creates bug report
- Include reproduction steps
**Time**: 3-5 minutes

## 9. Requirements Compliance
**Modules**: Marker → SPARTA
**Task**: "Check if requirements meet NIST controls"
**Steps**:
- Marker extracts all requirements
- SPARTA maps to relevant NIST controls
- Identify gaps and compliance level
**Time**: 5-10 minutes

## 10. Learning Path Creation
**Modules**: ArXiv → YouTube Transcripts → ArangoDB
**Task**: "Create learning path for quantum computing basics"
**Steps**:
- ArXiv finds introductory papers
- YouTube finds beginner tutorials
- ArangoDB stores as learning graph
- Return ordered learning sequence
**Time**: 5-8 minutes

## 11. Code Review Assistant
**Modules**: SPARTA → LLM Call
**Task**: "Review this code for security and suggest improvements"
**Steps**:
- SPARTA checks for vulnerabilities
- LLM Call suggests fixes
- Provide before/after code
**Time**: 2-3 minutes

## 12. Research Validation
**Modules**: ArXiv → LLM Call → ArangoDB
**Task**: "Verify claims in this paper against recent research"
**Steps**:
- ArXiv finds related papers
- LLM Call compares claims
- ArangoDB stores validation results
- Return confidence assessment
**Time**: 5-10 minutes

## 13. Tutorial to Practice
**Modules**: YouTube Transcripts → Test Reporter
**Task**: "Find pytest tutorial and create test template"
**Steps**:
- YouTube finds pytest tutorials
- Extract test patterns
- Test Reporter generates template
- Include best practices
**Time**: 3-5 minutes

## 14. Multi-Source Fact Check
**Modules**: ArXiv → YouTube Transcripts → LLM Call
**Task**: "Is claim X supported by both papers and expert talks?"
**Steps**:
- ArXiv searches academic support
- YouTube finds expert opinions
- LLM Call synthesizes agreement
- Return confidence score
**Time**: 4-6 minutes

## 15. Visual Documentation
**Modules**: MCP Screenshot → Marker → Chat
**Task**: "Document UI flow with screenshots and descriptions"
**Steps**:
- MCP Screenshot captures each step
- Marker adds to document template
- Chat provides interactive review
**Time**: 5-10 minutes

## 16. Relationship Discovery
**Modules**: Marker → ArangoDB
**Task**: "Extract entities from document and map relationships"
**Steps**:
- Marker extracts named entities
- Identify relationships between them
- ArangoDB creates relationship graph
- Return visualization
**Time**: 3-5 minutes

## 17. Security Briefing
**Modules**: SPARTA → Test Reporter → Chat
**Task**: "Generate security status briefing"
**Steps**:
- SPARTA compiles recent vulnerabilities
- Test Reporter formats briefing
- Chat delivers to stakeholders
**Time**: 3-5 minutes

## 18. Code Migration Helper
**Modules**: YouTube Transcripts → LLM Call
**Task**: "How do I migrate from Vue 2 to Vue 3?"
**Steps**:
- YouTube finds migration guides
- Extract key steps and gotchas
- LLM Call creates checklist
- Prioritize by impact
**Time**: 3-5 minutes

## 19. Paper Implementation
**Modules**: ArXiv → Marker → LLM Call
**Task**: "Implement algorithm from this paper"
**Steps**:
- ArXiv downloads paper
- Marker extracts algorithm section
- LLM Call generates code
- Include paper citations
**Time**: 5-8 minutes

## 20. Knowledge Synthesis
**Modules**: ArangoDB → LLM Call → Chat
**Task**: "Summarize everything we know about topic X"
**Steps**:
- ArangoDB retrieves all related memories
- LLM Call synthesizes knowledge
- Chat presents summary
- Highlight knowledge gaps
**Time**: 3-5 minutes
