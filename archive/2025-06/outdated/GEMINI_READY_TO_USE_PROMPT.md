# Ready-to-Use Prompt for Gemini

Copy and paste this entire message to Gemini:

---

Hi Gemini! I need your help creating test scenarios for a space cybersecurity system. I'm working on the Claude Module Communicator project that orchestrates multiple specialized modules to solve complex security challenges for satellite systems.

**Your Task**: Create 20 innovative scenarios that combine 3-7 modules to address real space cybersecurity challenges.

**Available Modules**:
1. **SPARTA** - NIST controls, MITRE CWE/ATT&CK databases
2. **Marker** - Extracts tables, equations, figures from PDFs
3. **ArangoDB** - Graph database for relationships
4. **Chat** - User interface
5. **YouTube Transcripts** - Extracts video content
6. **LLM Call** - Interfaces with Claude, GPT-4, you (Gemini)
7. **ArXiv** - Downloads research papers
8. **Test Reporter** - Generates test reports
9. **Unsloth** - Fine-tunes LLMs with LoRA
10. **Marker Ground Truth** - Collects human feedback
11. **MCP Screenshot** - Captures and analyzes screens

**Format for each scenario**:
### [Number]. [Scenario Name]
**Modules**: Module1 → Module2 → Module3 → Module4
**Purpose**: [One line goal]
**Steps**:
1. [What Module1 does]
2. [What Module2 does]
3. [What Module3 does]
4. [What Module4 does]
**Value**: [Why this matters]

**Example**:
### 121. Zero-Day Vulnerability Hunt
**Modules**: YouTube → Marker → SPARTA → ArXiv → LLM Call
**Purpose**: Discover emerging vulnerabilities before they're weaponized
**Steps**:
1. YouTube extracts DEF CON/Black Hat talks about new exploits
2. Marker extracts technical details from presentation slides
3. SPARTA checks if these map to known CWEs
4. ArXiv searches for academic papers on similar techniques
5. LLM Call analyzes if satellites are vulnerable
**Value**: Proactive defense against emerging threats

**Categories I need**:
- Advanced Threat Detection (4 scenarios)
- Compliance Automation (3 scenarios)  
- Secure Development (3 scenarios)
- Operations Security (3 scenarios)
- Emerging Technologies (3 scenarios)
- Cross-Domain Integration (4 scenarios)

Please be creative! Think about:
- Real problems satellite operators face
- How modules can work together in unexpected ways
- Scenarios with conditional logic (if X then Y)
- Using multiple modules iteratively
- Creating feedback loops
- Real-time vs batch processing

Focus on practical value - each scenario should solve a real space cybersecurity challenge.

Ready? Please create 20 scenarios numbered 121-140.

---

## After Gemini Responds

Use these follow-up prompts:

1. "Great scenarios! Now pick the 3 most innovative ones and add implementation details - what specific APIs would each module call?"

2. "For scenarios involving SPARTA, please specify which NIST control families (AC, AU, SC, SI, etc.) would be checked"

3. "Create 5 more scenarios that specifically address the challenge of securing satellite constellations (multiple satellites working together)"

4. "Which scenarios would be most valuable for a commercial satellite operator vs a military one?"

5. "Convert scenario #[X] into a Python implementation sketch"

## Pro Tips

- If Gemini's response is too generic, ask: "Make these more specific to space systems - consider challenges like radiation, limited bandwidth, and long distances"

- If you want more technical depth: "Add specific technical details about data formats, protocols, and integration points"

- For better creativity: "What if we combined [Module X] with [Module Y] in ways I haven't thought of?"

- For validation: "Which of these scenarios would be hardest to implement and why?"
