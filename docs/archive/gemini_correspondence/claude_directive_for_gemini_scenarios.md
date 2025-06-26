# Directive for Gemini: Creating Module Interaction Scenarios

## Context
You're creating test scenarios for the **claude-module-communicator** project, which orchestrates communication between these modules:

- **arxiv-mcp-server**: Research paper search and download
- **marker**: PDF/document text extraction and processing  
- **arangodb**: Graph database for knowledge storage
- **youtube_transcripts**: Video transcript fetching and analysis
- **claude_max_proxy**: AI-powered analysis and generation
- **sparta**: ML model training framework
- **claude-test-reporter**: Test execution and reporting
- **fine_tuning**: Efficient model fine-tuning
- **marker-ground-truth**: Validation against ground truth data
- **mcp-screenshot**: Web page capture and visual analysis

## What We Need

Create scenarios that test the communicator's ability to handle **different communication patterns**, NOT stress tests or failure modes.

### Good Scenarios Focus On:

1. **Novel Communication Patterns**
   - Modules talking in circles (A→B→C→A)
   - Broadcast patterns (one to many)
   - Consensus mechanisms (many to one)
   - Relay races (sequential with handoffs)
   - Tournament brackets (elimination)

2. **Real Module Capabilities**
   ```python
   # Use actual module functions:
   self.orchestrator.add_step(
       task,
       module="arxiv-mcp-server",
       capability="search_papers",  # Real capability
       input_data={"query": "...", "max_results": 5}  # Real parameters
   )
   ```

3. **Data Transformation Flows**
   - PDF → Text → Embeddings → Graph → Insights
   - Video → Transcript → Topics → Training Data → Model
   - Screenshot → OCR → Analysis → Report

4. **Stateful Interactions**
   - Modules remember previous interactions
   - Context builds over time
   - Decisions affect future module calls

5. **Dynamic Orchestration**
   - Module selection based on results
   - Conditional workflows
   - Adaptive pipelines

### Example Patterns to Implement:

1. **The Negotiator**: Modules debate until consensus
   - Multiple modules propose solutions
   - They critique each other
   - Iterate until agreement
   - Final unified output

2. **The Teacher**: Modules learn from each other
   - Expert module teaches others
   - Students practice and get feedback
   - Knowledge transfer verification
   - Role reversal

3. **The Explorer**: Branching exploration paths
   - Start with one query
   - Each result spawns new searches
   - Explore until depth limit
   - Merge discoveries

4. **The Judge**: Multi-module jury system
   - Present evidence to multiple modules
   - Each gives verdict with reasoning
   - Majority vote decides
   - Dissenting opinions included

5. **The Translator**: Cross-domain communication
   - Module A speaks "research"
   - Module B speaks "code"
   - Translator module bridges gap
   - Verify understanding

### Implementation Template:

```python
class YourScenarioName:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.state = {}  # Track scenario state
    
    async def run(self, input_param: str = "default"):
        # Phase-based structure
        await self._phase_1_setup()
        await self._phase_2_main_pattern()  # Your unique pattern
        await self._phase_3_verification()
        self._print_results()
    
    async def _phase_2_main_pattern(self):
        task = self.orchestrator.create_task(
            name="Unique Pattern",
            description="What makes this scenario special"
        )
        
        # Use real modules with real capabilities
        self.orchestrator.add_step(
            task,
            module="actual-module-name",
            capability="real-capability",
            input_data={
                "real_param": value,
                "reference_previous": "$step_1.output"
            }
        )
```

### What NOT to Create:

❌ Stress tests (system overload, failures)
❌ Security tests (malicious inputs)
❌ Performance benchmarks (speed/latency focus)
❌ Abstract/fictional module capabilities
❌ Simple linear pipelines (A→B→C→Done)

### Key Question for Each Scenario:

**"What new communication pattern does this test that hasn't been tested before?"**

If the answer is "none" or "it just tests if things break", then it's not what we need.

## Remember:
These scenarios prove the claude-module-communicator can orchestrate complex, flexible, and creative module interactions beyond simple request-response patterns.