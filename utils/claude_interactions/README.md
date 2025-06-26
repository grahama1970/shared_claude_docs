# Claude Module Interactions Framework

A comprehensive framework for testing and demonstrating inter-module communication through the granger_hub. This directory contains scenarios, scripts, and documentation showing how all registered projects can collaborate to solve complex problems.

## Vision

Create a living ecosystem where modules can:
- **Discover** each other's capabilities dynamically
- **Negotiate** data schemas and protocols
- **Collaborate** on complex multi-step tasks
- **Evolve** their interfaces based on usage patterns
- **Report** results in rich, interactive formats

## Interaction Levels

Based on the ecosystem's architectural patterns, scenarios are organized into four complexity levels:

### Level 0: Direct Module Calls
Simple, stateless operations where a single module performs its core function.

### Level 1: Sequential Pipelines
Linear data flow through multiple modules where output of one feeds into the next.

### Level 2: Parallel & Branching Workflows
Multiple execution paths with conditional routing and parallel processing.

### Level 3: Orchestrated Multi-Module Collaboration
Bi-directional communication with feedback loops, continuous learning, and dynamic adaptation.

## Core Concepts

### 1. Module Discovery Protocol
Each module registers its capabilities with the communicator, allowing dynamic discovery.

### 2. Schema Negotiation
Modules can query each other's expected input/output schemas and adapt accordingly.

### 3. Task Orchestration
Complex tasks are broken down and distributed across specialized modules.

### 4. Result Aggregation
Multiple module outputs are combined into cohesive, actionable results.

## Interaction Patterns

### Direct Communication
```
Module A → Communicator → Module B
```

### Broadcast Communication
```
Module A → Communicator → [Module B, C, D]
```

### Pipeline Communication
```
Module A → Module B → Module C → Result
```

### Collaborative Communication
```
Module A ↔ Module B
    ↓         ↓
    Module C ← →
```

## Implemented Scenarios

### Classic Scenarios (Level 1-3)

#### 1. Research Evolution (`research_evolution`) - Level 3
Modules collaborate to gather research, analyze it, build knowledge graphs, and train models based on evolving insights.
- ArXiv searches for papers based on initial query
- Marker extracts content from papers
- YouTube Transcripts finds related videos
- Sparta trains models on extracted knowledge
- ArangoDB builds evolving knowledge graph
- System refines queries based on findings

#### 2. UI Self-Improvement (`ui_improvement`) - Level 2
UI modules capture screenshots, analyze issues, generate improvements, and iteratively enhance the interface.
- MCP-Screenshot captures UI state
- Analyzes accessibility and usability issues
- Generates improvement code
- Tests changes with Claude Test Reporter
- Iterates until quality standards met

#### 3. Schema Negotiation (`schema_negotiation`) - Level 2
Modules discover each other's schemas, negotiate data formats, and build adaptive pipelines with automatic transformations.
- Discovers module capabilities and schemas
- Builds compatibility matrix
- Creates adaptive pipelines with transformations
- Tracks usage patterns for schema evolution

#### 4. Conversational Interface (`conversational`) - Level 1
Interactive mode where you can give natural language commands to orchestrate module interactions.
- Natural language understanding
- Dynamic task planning
- Multi-module orchestration
- Conversational feedback

#### 5. Grand Collaboration (`grand_collaboration`) - Level 3
The ultimate scenario where ALL modules work together through 6 phases:
- **Phase 1**: Research gathering (ArXiv, YouTube)
- **Phase 2**: Knowledge synthesis (Marker, ArangoDB)
- **Phase 3**: Model development (Sparta)
- **Phase 4**: UI development (MCP-Screenshot)
- **Phase 5**: System integration (Claude Test Reporter)
- **Phase 6**: Self-improvement loop

### Creative Scenarios (Level 2-3)

#### 6. Symphony (`symphony`) - Level 2
Modules work in parallel like musicians in an orchestra, synchronizing at key moments to create harmonious results.
- Parallel processing with synchronized checkpoints
- Multiple data streams processed simultaneously
- Harmonic convergence of results
- Rhythmic coordination patterns

#### 7. Detective (`detective`) - Level 3
Modules collaborate as specialized detectives, sharing clues on an evidence board to solve mysteries together.
- Evidence gathering from multiple sources
- Collaborative deduction and hypothesis testing
- Cross-referencing findings
- Mystery resolution through consensus

#### 8. Ecosystem (`ecosystem`) - Level 3
Modules form symbiotic relationships, producing and consuming resources from each other in a self-regulating system.
- Resource production and consumption cycles
- Dynamic equilibrium maintenance
- Adaptation to resource availability
- Emergent system behaviors

#### 9. Mirror (`mirror`) - Level 2
Each module reflects and creatively transforms the previous module's output, revealing new dimensions of understanding.
- Sequential transformation chains
- Creative reinterpretation of data
- Perspective shifting
- Layered understanding development

#### 10. Knowledge Evolution (`knowledge_evolution`) - Level 3
Iterative learning system with feedback loops that continuously improve understanding.
- Adaptive knowledge graph construction
- Feedback-driven refinement
- Concept emergence tracking
- Self-improving query generation

#### 11. Model Training Pipeline (`model_pipeline`) - Level 2
End-to-end ML workflow coordination from data gathering to deployment.
- Data collection and preprocessing
- Feature engineering
- Model training and evaluation
- Deployment and monitoring

#### 12. Competitive Collaboration (`competitive`) - Level 3
Modules compete to provide best solutions then collaborate to combine strengths.
- Parallel solution generation
- Performance-based selection
- Hybrid solution creation
- Competitive learning dynamics

### Stress Tests (Level 3)

#### 13. Avalanche (`avalanche`) - Level 3
Cascading failure scenarios with recovery mechanisms.
- Failure propagation testing
- Recovery strategy evaluation
- System resilience measurement
- Graceful degradation patterns

#### 14. Contradiction (`contradiction`) - Level 3
Handling conflicting information from multiple sources.
- Conflict detection and resolution
- Truth reconciliation strategies
- Confidence scoring
- Consensus building

#### 15. Resource Strangler (`resource_strangler`) - Level 3
Testing system behavior under resource constraints.
- Performance under load
- Resource allocation strategies
- Prioritization mechanisms
- Efficiency optimization

#### 16. Schema Shapeshifter (`schema_shapeshifter`) - Level 3
Dynamic schema changes during execution.
- Runtime adaptation
- Backward compatibility
- Schema versioning
- Migration strategies

#### 17. Security Breach (`security_breach`) - Level 3
Security and access control testing.
- Authentication flows
- Authorization boundaries
- Data isolation
- Audit trail generation

## Getting Started

```bash
# Install dependencies
./install_dependencies.sh

# Start the discovery service (in separate terminal)
./start_discovery_service.sh

# Run a specific scenario
./run_scenario.sh research_evolution
./run_scenario.sh ui_improvement
./run_scenario.sh schema_negotiation
./run_scenario.sh conversational
./run_scenario.sh grand_collaboration

# Run all scenarios
./run_scenario.sh all
```

## Directory Structure

```
claude_interactions/
├── README.md
├── install_dependencies.sh
├── start_discovery_service.sh
├── run_scenario.sh
├── run_scenario_updated.sh         # Extended scenario runner
├── discovery/                      # Module discovery service
│   ├── __init__.py
│   └── module_registry.py
├── orchestrator/                   # Task orchestration engine
│   ├── __init__.py
│   └── task_orchestrator.py
├── scenarios/                      # Classic interaction scenarios
│   ├── __init__.py
│   ├── research_evolution.py
│   ├── ui_self_improvement.py
│   ├── schema_negotiation.py
│   └── grand_collaboration.py
├── creative_scenarios/             # Novel interaction patterns
│   ├── __init__.py
│   ├── README.md
│   ├── symphony_scenario.py
│   ├── detective_scenario.py
│   ├── ecosystem_scenario.py
│   ├── mirror_scenario.py
│   ├── knowledge_evolution_scenario.py
│   ├── model_training_pipeline_scenario.py
│   ├── competitive_collaboration_scenario.py
│   ├── research_consensus_scenario.py
│   ├── research_training_pipeline_scenario.py
│   └── dynamic_explorer_scenario.py
├── stress_tests/                   # Robustness testing scenarios
│   ├── __init__.py
│   ├── avalanche_scenario.py
│   ├── contradiction_scenario.py
│   ├── resource_strangler.py
│   ├── schema_shapeshifter.py
│   └── security_breach.py
├── protocols/                      # Communication protocols (planned)
├── tests/                          # Integration tests (planned)
├── visualizations/                 # Generated graphs and charts
└── reports/                        # Scenario execution reports
```

## Registered Modules

The framework works with all registered companion projects:
- **arxiv-mcp-server**: Research paper discovery and retrieval
- **marker**: PDF/document content extraction and structuring
- **youtube_transcripts**: Video transcript extraction and analysis
- **sparta**: Scalable ML model training framework
- **arangodb**: Graph database for knowledge representation
- **mcp-screenshot**: Browser automation and UI capture
- **claude-test-reporter**: Test execution and validation
- **granger_hub**: Central communication hub

## Output

Each scenario generates:
- **JSON Reports**: Detailed execution logs in `./reports/`
- **Visualizations**: Knowledge graphs, timelines, and metrics in `./visualizations/`
- **Logs**: Module interaction traces

## Extending the Framework

To add new scenarios:
1. Create a new scenario file in `scenarios/`
2. Implement the scenario class with `async def run()`
3. Add the scenario to `run_scenario.sh`
4. Register any new modules in the discovery service

## Example Outputs

### Research Evolution Visualization
The research evolution scenario generates knowledge graphs showing concept discovery:
- Nodes represent papers and concepts
- Edges show relationships
- Graph grows with each iteration
- Model performance metrics tracked

### Symphony Coordination Pattern
The symphony scenario produces timing diagrams showing:
- Parallel execution phases
- Synchronization points
- Resource flow between modules
- Harmonic convergence moments

### Report Structure
Each scenario generates detailed JSON reports including:
```json
{
  "scenario": "research_evolution",
  "timestamp": "2025-05-30T10:15:30Z",
  "iterations": 3,
  "papers_processed": 15,
  "concepts_discovered": 42,
  "model_accuracy": 0.87,
  "execution_time_ms": 45000
}
```

## Scenario Complexity Mapping

| Scenario | Level | Modules Used | Interaction Type |
|----------|-------|--------------|------------------|
| Conversational | 1 | 1-2 | Sequential |
| UI Improvement | 2 | 3-4 | Parallel & Branching |
| Symphony | 2 | 4+ | Parallel Synchronized |
| Research Evolution | 3 | 5+ | Feedback Loops |
| Grand Collaboration | 3 | All | Full Orchestration |
| Stress Tests | 3 | Varies | Resilience Testing |

## Notes

- The discovery service must be running before executing scenarios
- Mock implementations are provided for testing without external services
- All scenarios are designed to demonstrate real-world collaboration patterns
- Reports and visualizations are timestamped for tracking evolution over time
- Creative scenarios explore novel interaction patterns beyond traditional workflows
- Stress tests ensure system resilience under adverse conditions

## Future Enhancements

1. **Protocol Library**: Formalized communication protocols in `protocols/`
2. **Integration Tests**: Comprehensive test suite in `tests/`
3. **Real-time Dashboard**: Live visualization of module interactions
4. **Performance Metrics**: Detailed benchmarking and optimization
5. **Custom Scenario Builder**: GUI for creating new interaction patterns