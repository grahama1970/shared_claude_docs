# GRANGER ECOSYSTEM CONTEXT — CLAUDE.md

> **Workspace-specific context for the Granger autonomous research ecosystem.**  
> Global coding standards are inherited from `~/.claude/CLAUDE.md`.  
> **🚨 MANDATORY: All Granger modules MUST follow [GRANGER_MODULE_STANDARDS.md](./docs/07_style_conventions/GRANGER_MODULE_STANDARDS.md)**

---

## 🔴 WORKSPACE CONTEXT

This document provides context about the **Granger Ecosystem** - a graph-reinforced autonomous network for research, verification, and fine-tuning. All projects follow the global standards plus the ecosystem-specific standards defined in [GRANGER_MODULE_STANDARDS.md](./docs/07_style_conventions/GRANGER_MODULE_STANDARDS.md).

---

## Granger Ecosystem Overview

The Granger ecosystem follows a **hub-and-spokes architecture** with specialized UI modules:

```
Granger Ecosystem
├── Hub (Communication & Orchestration)
├── Reinforcement Learning (Core Intelligence)
├── World Model (Self-Understanding & Prediction)  
├── Test Reporting (Quality Assurance)
├── Spokes (Specialized Processing Modules)
└── User Interfaces (Human Interaction)
```

### Core Pipeline Flow
```
SPARTA → Marker → ArangoDB → Unsloth
           ↓
    LLM Call (LLM access)
           ↓
    Module Communicator (orchestration)
```

---

## Project Registry

For the complete project registry, see [GRANGER_PROJECTS.md](./docs/GRANGER_PROJECTS.md).

### Key Projects by Category

#### Core Infrastructure (6 projects)
- **Hub:** `/home/graham/workspace/experiments/granger_hub/` - Inter-project communication
- **RL Commons:** `/home/graham/workspace/experiments/rl_commons/` - Intelligence and learning
- **World Model:** `/home/graham/workspace/experiments/world_model/` - Self-understanding and prediction
- **Test Reporter:** `/home/graham/workspace/experiments/claude-test-reporter/` - Quality assurance
- **Shared Docs:** `/home/graham/workspace/shared_claude_docs/` - Documentation hub
- **UI System:** `/home/graham/workspace/granger-ui/` - Design system
#### Processing Spokes (7 projects)
- **SPARTA:** `/home/graham/workspace/experiments/sparta/` - Cybersecurity data ingestion
- **Marker:** `/home/graham/workspace/experiments/marker/` - Document processing
- **ArangoDB:** `/home/graham/workspace/experiments/arangodb/` - Knowledge management
- **YouTube Transcripts:** `/home/graham/workspace/experiments/youtube_transcripts/` - Media processing
- **LLM Call:** `/home/graham/workspace/experiments/llm_call/` - LLM interface
- **Fine Tuning:** `/home/graham/workspace/experiments/fine_tuning/` - Model training
- **DARPA Crawl:** `/home/graham/workspace/experiments/darpa_crawl/` - Research funding

#### User Interfaces (3 projects)
- **Chat:** `/home/graham/workspace/experiments/chat/` - Conversational interface
- **Annotator:** `/home/graham/workspace/experiments/annotator/` - Annotation interface
- **Aider Daemon:** `/home/graham/workspace/experiments/aider-daemon/` - Terminal interface

#### MCP Services (3 projects)
- **ArXiv MCP:** `/home/graham/workspace/mcp-servers/arxiv-mcp-server/` - Research automation
- **MCP Screenshot:** `/home/graham/workspace/experiments/mcp-screenshot/` - Visual analysis
- **GitGet:** `/home/graham/workspace/experiments/gitget/` - Repository analysis

---

## Workspace-Specific Standards

### Dependency Management
All Granger projects MUST follow these locked versions:
```toml
# pyproject.toml requirements
requires-python = ">=3.10.11"
dependencies = [
    "numpy==1.26.4",          # LOCKED - Do not change
    "pandas>=2.2.3,<2.3.0",   # Compatible with numpy
    "pyarrow>=4.0.0,<20",     # mlflow constraint
    "pillow>=10.1.0,<11.0.0", # Security constraint
]
```

See [Dependency Quick Reference](./guides/DEPENDENCY_QUICK_REFERENCE.md) for troubleshooting.

### Environment Variables
All Granger projects should include these common environment variables:
```bash
# .env.example additions for Granger projects
PYTHONPATH=./src  # MUST be first line
GRANGER_HUB_URL=http://localhost:8000
ARANGODB_URL=http://localhost:8529
LLM_CALL_URL=http://localhost:8001
TEST_REPORTER_URL=http://localhost:8002

# Project-specific
MODULE_NAME=project_name
MODULE_VERSION=1.0.0
ENABLE_RL_OPTIMIZATION=true
```

### Inter-Module Communication
All Granger projects should be capable of:
- **Schema negotiation** with the Module Communicator
- **Progress reporting** via standard events
- **Health checks** on standard endpoints
- **Test result reporting** to the Test Reporter

### Documentation Requirements
In addition to global standards, Granger projects must include:
- **Integration guide** in `docs/integration/`
- **API documentation** if the project exposes APIs
- **Module communication schema** in `docs/schemas/`
---

## Reinforcement Learning Integration

### RL-Enabled Projects
Projects that use RL Commons for optimization:
- **LLM Call:** Provider selection optimization
- **Marker:** Processing pipeline optimization
- **Module Communicator:** Resource allocation and scheduling
- **Test Reporter:** Flaky test prediction
- **DARPA Crawl:** Proposal optimization

### RL Standards
```python
# All RL integrations should follow this pattern
from rl_commons import ContextualBandit, OptimizationAgent

class ModuleOptimizer:
    def __init__(self):
        self.agent = ContextualBandit(
            actions=["option_a", "option_b", "option_c"],
            context_features=["feature_1", "feature_2"],
            exploration_rate=0.1
        )
    
    def optimize_decision(self, context: dict) -> str:
        return self.agent.select_action(context)
    
    def report_outcome(self, action: str, reward: float):
        self.agent.update(action, reward)
```

---

## Testing Standards for Granger

### Cross-Module Testing
- **Integration tests** must verify communication with Module Communicator
- **End-to-end tests** should test complete pipeline flows
- **Performance tests** must include RL optimization metrics

### Test Reporting Integration
```python
# All projects should integrate with Test Reporter
from claude_test_reporter import GrangerTestReporter

def run_tests():
    reporter = GrangerTestReporter(
        module_name="project_name",
        test_suite="integration"
    )
    
    # Run tests and report results
    results = pytest.main()
    reporter.submit_results(results)
```
---

## Development Workflow

### Before Starting Work
1. Check Module Communicator for any pending coordination requests
2. Review any RL optimization suggestions for your module
3. Ensure Test Reporter has no critical failures for dependencies

### After Completing Work
1. Run full test suite and report to Test Reporter
2. Update module schema if APIs changed
3. Notify Module Communicator of completion status

---

## Ecosystem-Specific Commands

When working in the Granger workspace, these commands are available:

```bash
# Check ecosystem health
/granger:health

# Run cross-module integration tests  
/granger:integration-test

# Generate ecosystem-wide report
/granger:report

# Optimize module interactions
/granger:optimize
```

---

## Quick Navigation

### Common Paths
```bash
# Core projects
cd /home/graham/workspace/experiments/granger_hub                 # Hub
cd /home/graham/workspace/experiments/rl_commons                  # RL Core
cd /home/graham/workspace/experiments/claude-test-reporter       # Testing

# Main pipeline
cd /home/graham/workspace/experiments/sparta                     # Step 1
cd /home/graham/workspace/experiments/marker                     # Step 2  
cd /home/graham/workspace/experiments/arangodb                   # Step 3
cd /home/graham/workspace/experiments/fine_tuning               # Step 4

# Utilities
cd /home/graham/workspace/experiments/llm_call                  # LLM access
cd /home/graham/workspace/experiments/chat                      # UI
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.