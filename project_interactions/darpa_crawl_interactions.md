# DARPA Crawl Module Interactions

## Overview

DARPA Crawl operates as a spoke in the Granger hub-and-spoke architecture, coordinated by claude-module-communicator. It NEVER duplicates functionality from other modules.

## Module Dependencies

### Direct Dependencies (via claude-module-communicator)

1. **granger_capability_analyzer** (from claude-module-communicator)
   - Action: `analyze_capabilities`
   - Purpose: Get verified Granger capabilities
   - Never duplicates capability analysis logic

2. **external_llm** (from claude-module-communicator)
   - Actions: `generate_proposal`, `evaluate_proposal`
   - Purpose: Use Claude for generation, Gemini for evaluation
   - Never makes direct LLM calls

3. **research_integration** (from multiple modules)
   - arxiv-mcp-server: Paper search and analysis
   - youtube_transcripts: Video evidence
   - Purpose: Gather supporting evidence

4. **rl_commons**
   - Action: `evaluate_interaction`
   - Purpose: Score and optimize module interactions
   - Learn from proposal success rates

## Communication Patterns

### 1. Opportunity Discovery Flow
```
User Request → claude-module-communicator → darpa_crawl
                                          ↓
                                    SAM.gov API / DARPA Catalog
                                          ↓
                                    Store in local DB
                                          ↓
                                    Return opportunities
```

### 2. Proposal Generation Flow
```
darpa_crawl → claude-module-communicator → granger_capability_analyzer
                                        ↓
                                  Get verified capabilities
                                        ↓
darpa_crawl → claude-module-communicator → research_integration
                                        ↓
                                  Gather evidence
                                        ↓
darpa_crawl → claude-module-communicator → external_llm (Claude)
                                        ↓
                                  Generate proposal
                                        ↓
darpa_crawl → claude-module-communicator → external_llm (Gemini)
                                        ↓
                                  Evaluate proposal
                                        ↓
darpa_crawl → claude-module-communicator → rl_commons
                                        ↓
                                  Score interaction quality
```

## Message Formats

### From DARPA Crawl to Other Modules

```python
# To granger_capability_analyzer
{
    "target": "granger_capability_analyzer",
    "action": "analyze_capabilities",
    "opportunity": {
        "title": "AI Verification System",
        "description": "...",
        "requirements": [...]
    }
}

# To external_llm for proposal generation
{
    "target": "external_llm",
    "action": "generate_proposal",
    "model": "claude-3-opus-20240229",
    "opportunity": {...},
    "capabilities": {...},
    "research": {...}
}

# To rl_commons for scoring
{
    "target": "rl_commons",
    "action": "evaluate_interaction",
    "interaction_type": "darpa_proposal_generation",
    "metrics": {
        "alignment_score": 0.85,
        "gemini_score": 87,
        "time_taken": 120,
        "modules_used": [...]
    }
}
```

### To DARPA Crawl from Other Modules

```python
# Search request
{
    "target": "darpa_crawl",
    "action": "search_opportunities",
    "keywords": ["AI", "verification"],
    "source": "all",
    "limit": 10
}

# Generate proposal request
{
    "target": "darpa_crawl",
    "action": "generate_proposal",
    "opportunity_id": "DOD-DARPA-2025-001"
}
```

## RL Optimization Points

1. **Opportunity Selection**
   - Reward: Alignment score × Gemini score
   - State: Opportunity features + Granger capabilities
   - Action: Select/Skip opportunity

2. **Research Depth**
   - Reward: Proposal score improvement per research item
   - State: Current evidence count + time spent
   - Action: Gather more / Stop researching

3. **Module Coordination**
   - Reward: Overall proposal score - time cost
   - State: Module availability + response times
   - Action: Module selection sequence

## Best Practices

1. **Never Duplicate Logic**
   - Use `granger_capability_analyzer` for ALL capability analysis
   - Use `external_llm` for ALL LLM interactions
   - Use `rl_commons` for ALL optimization decisions

2. **Always Cache Results**
   - Store opportunities in local SQLite DB
   - Cache capability analysis for 24 hours
   - Reuse research evidence across proposals

3. **Error Handling**
   - Gracefully handle module unavailability
   - Provide fallback responses
   - Log all inter-module communication

4. **Performance**
   - Batch opportunity searches
   - Parallelize research gathering
   - Use async for all module calls

## Testing Integration

```bash
# Run integration scenario
cd /home/graham/workspace/experiments/claude-module-communicator
python tests/integration_scenarios/darpa_crawl_scenario.py

# Test via CLI
claude-comm send darpa_crawl granger_capability_analyzer "analyze_capabilities"

# Monitor interactions
claude-comm list --filter darpa_crawl
```

## Future Enhancements

1. **Multi-Agent Proposal Generation**
   - Multiple Claude instances collaborating
   - Specialized agents for different sections
   - RL-optimized agent coordination

2. **Continuous Learning**
   - Track proposal success rates
   - Update scoring models
   - Improve opportunity selection

3. **Advanced Research Integration**
   - Patent database searches
   - Competitor analysis
   - Technical standard compliance
