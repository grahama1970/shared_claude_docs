# Granger Projects Registry

*Documentation verified: 2025-06-09*

## CRITICAL: GitHub URL Format for Dependencies

**⚠️ IMPORTANT:** All GitHub URLs in this registry MUST use the `git+https://` format for pyproject.toml compatibility:
- ✅ CORRECT: `git+https://github.com/grahama1970/project_name.git`
- ❌ WRONG: `file:///home/graham/workspace/...` (local file paths)
- ❌ WRONG: `https://github.com/grahama1970/project_name` (missing git+ prefix)

**Example pyproject.toml usage:**
```toml
[tool.poetry.dependencies]
runpod_ops = {git = "https://github.com/grahama1970/runpod_ops.git"}
# or
runpod_ops = "runpod_ops @ git+https://github.com/grahama1970/runpod_ops.git"
```

This document serves as the canonical registry of all projects in the Granger ecosystem. It is referenced by slash commands and automation tools.

## Project Architecture

The Granger ecosystem follows a hub-and-spokes architecture with specialized UI modules:

```
Granger Ecosystem
├── Hub (Communication & Orchestration)
├── Reinforcement Learning (Core Intelligence)
├── World Model (Self-Understanding & Prediction)
├── Test Reporting (Quality Assurance)
├── Infrastructure Services (Compute & Resources)
├── Spokes (Specialized Processing Modules)
└── User Interfaces (Human Interaction)
```

## Project Registry

### Shared Documentation
**Purpose:** Central documentation, standards, and shared resources  
**Path:** `/home/graham/workspace/shared_claude_docs/`  
**GitHub:** *Local repository only - no remote*  
**Type:** Documentation Hub  
**Status:** Active  
**Description:** AI-powered research and verification platform documentation hub. Contains integration patterns, testing frameworks, and unified documentation for the entire GRANGER ecosystem with graph-reinforced autonomous network capabilities.

### Shared Visual Assets
**Purpose:** Unified UI design system and components  
**Path:** `/home/graham/workspace/granger-ui/`  
**GitHub:** *No Git repository*  
**Type:** Design System  
**Status:** Active  
**Description:** Monorepo containing core design tokens, React web components, and terminal UI components. Provides consistent visual language across chat interfaces, annotation tools, and terminal applications.

### Hub Project Module
**Purpose:** Inter-project communication and orchestration  
**Path:** `/home/graham/workspace/experiments/granger_hub/`  
**GitHub:** `git+https://github.com/grahama1970/granger_hub.git`  
**Type:** Communication Hub  
**Status:** Active  
**Dependencies:** All spoke modules  
**Description:** Central orchestration hub for the Granger autonomous research ecosystem. Enables communication between independent modules with schema negotiation, progress tracking, ArangoDB integration, and multi-LLM access (Claude, Gemini, GPT). Includes screenshot automation and browser control capabilities.

### Reinforcement Learning Module
**Purpose:** Core intelligence and learning capabilities  
**Path:** `/home/graham/workspace/experiments/rl_commons/`  
**GitHub:** `git+https://github.com/grahama1970/rl-commons.git`  
**Type:** Intelligence Core  
**Status:** Development  
**Dependencies:** Hub, Test Reporting  
**Description:** Shared RL components for optimizing decisions across the ecosystem. Provides contextual bandits, DQN, hierarchical RL, multi-agent RL, and meta-learning capabilities for automatic algorithm selection and module coordination.

### Test Reporting Engine
**Purpose:** Comprehensive testing and quality assurance  
**Path:** `/home/graham/workspace/experiments/claude-test-reporter/`  
**GitHub:** `git+https://github.com/grahama1970/claude-test-reporter.git`  
**Type:** Quality Assurance  
**Status:** Active  
**Dependencies:** All projects (for testing)  
**Description:** Universal test reporting engine with zero dependencies. Generates beautiful HTML reports, multi-project dashboards, flaky test detection, and agent comparison capabilities for comprehensive quality assurance.

### World Model
**Purpose:** Autonomous predictive knowledge representation and self-understanding  
**Path:** `/home/graham/workspace/experiments/world_model/`  
**GitHub:** *No Git repository*  
**Type:** Intelligence Core  
**Status:** Active  
**Dependencies:** ArangoDB, RL Commons  
**Description:** Autonomous system that learns and improves through experience, tracking relationships, causal chains, and state transitions across the GRANGER ecosystem. Enables Granger to build an evolving understanding of itself and the projects it creates, working alongside ArangoDB for knowledge storage and RL Commons for learning optimization.  

## Infrastructure Services

Critical infrastructure components that provide foundational capabilities enabling AI operations across the ecosystem.

### GPU Compute Infrastructure
**Project:** runpod_ops  
**Path:** `/home/graham/workspace/experiments/runpod_ops/`  
**GitHub:** *No Git repository*  
**Purpose:** GPU compute orchestration and resource management  
**Status:** Active  
**Type:** Infrastructure Service  
**Dependents:** fine_tuning, llm_call, world_model, and any project requiring GPU compute  
**Description:** Critical GPU infrastructure layer providing intelligent compute resource management for the Granger ecosystem. Orchestrates RunPod GPU instances for both training and inference workloads with automatic GPU selection based on model requirements, multi-GPU cost optimization, real-time resource monitoring, and automatic instance lifecycle management. Features include: [Verified ✓ - 36 additional features documented]
- **Smart GPU Selection**: Automatically selects optimal GPU configurations (RTX 4090 to H100) based on model size and workload
- **Cost Optimization**: Multi-GPU cost analysis with spot instance support, saving up to 50% on training costs
- **Training Orchestration**: Manages distributed training jobs with auto-termination and checkpoint management
- **Inference Deployment**: One-command model serving with autoscaling support
- **Integration Points**: CLI commands, MCP server for Claude integration, slash commands for quick access
- **Resource Monitoring**: Real-time GPU utilization, memory tracking, and cost accumulation

**Critical Role**: Without runpod_ops, the Granger ecosystem would lack the ability to perform GPU-intensive operations like model training, fine-tuning, and high-performance inference. It serves as the bridge between Granger's intelligence layer and physical GPU compute resources.

## Spokes Project Modules

### Data Collection & Crawling
**Project:** darpa_crawl  
**Path:** `/home/graham/workspace/experiments/darpa_crawl/`  
**GitHub:** *No Git repository*  
**Purpose:** DARPA dataset collection and processing  
**Status:** Development  
**Description:** Autonomous funding acquisition module that monitors DARPA I2O opportunities, generates proposals using ArXiv/YouTube research, and optimizes selection through reinforcement learning for Granger's self-improvement reward system.

**Project:** gitget  
**Path:** `/home/graham/workspace/experiments/gitget/`  
**GitHub:** *No Git repository*  
**Purpose:** Git repository analysis and extraction  
**Status:** Active  
**Description:** CLI utility for sparse cloning, analyzing, and LLM-based documentation of GitHub repositories. Features text chunking, enhanced markdown parsing, and code analysis with tree-sitter for efficient repository processing.

### Document Processing
**Project:** sparta  
**Path:** `/home/graham/workspace/experiments/sparta/`  
**GitHub:** `git+https://github.com/grahama1970/SPARTA.git`  
**Purpose:** Advanced document analysis and processing  
**Status:** Active  
**Description:** Space cybersecurity data ingestion and enrichment pipeline. First step in transforming raw security resources into fine-tuned AI models. Downloads, enriches, and prepares cybersecurity resources for the SPARTA → Marker → ArangoDB → Unsloth pipeline.

**Project:** marker  
**Path:** `/home/graham/workspace/experiments/marker/`  
**GitHub:** `git+https://github.com/grahama1970/marker.git`  
**Purpose:** PDF extraction and document markup  
**Status:** Active  
**Description:** Advanced multi-format document processing hub supporting PDF, PowerPoint, Word, and XML with native extractors. Features table/image support, AI-powered accuracy improvements, and hierarchical content extraction.

### Data Storage & Retrieval
**Project:** arangodb  
**Path:** `/home/graham/workspace/experiments/arangodb/`  
**GitHub:** `git+https://github.com/grahama1970/arangodb.git`  
**Purpose:** Graph database operations and search  
**Status:** Active  
**Description:** Sophisticated memory and knowledge management system for AI agents. Provides persistent conversation memory, multi-algorithm search (semantic, BM25, graph-based), episode management, and advanced graph capabilities for relationship modeling.  

### Media Processing
**Project:** youtube_transcripts  
**Path:** `/home/graham/workspace/experiments/youtube_transcripts/`  
**GitHub:** `git+https://github.com/grahama1970/youtube-transcripts-search.git`  
**Purpose:** YouTube video transcript extraction and analysis  
**Status:** Active  
**Description:** Comprehensive YouTube research tool with transcript extraction, API search, and scientific metadata analysis. Features intelligent rate limiting with quota tracking, user-friendly error handling, response caching, and dual database support (SQLite/ArangoDB). Includes progressive search widening, GitHub/arXiv link extraction, and MCP server integration for Claude Code.


### Presentation & Reporting
**Project:** ppt  
**Path:** `/home/graham/workspace/experiments/ppt/`  
**GitHub:** *No Git repository*  
**Purpose:** PowerPoint automation and presentation generation  
**Status:** Active  
**Dependencies:** granger_hub, arangodb, llm_call (via hub)  
**Description:** Autonomous presentation system that monitors GRANGER ecosystem data and automatically updates PowerPoint presentations. Features natural language commands via agent interface, event-driven updates through granger_hub integration, and programmatic creation/editing of presentations. Similar to how granger-verify generates whitepapers, PPT keeps presentations current with ecosystem changes. Supports templates, charts, tables, multimedia content, and incremental updates based on data changes.

### AI Services
*Note: GPU compute for AI services is provided by runpod_ops (see Infrastructure Services section)*

**Project:** llm_call  
**Path:** `/home/graham/workspace/experiments/llm_call/`  
**GitHub:** `git+https://github.com/grahama1970/llm_call.git`  
**Purpose:** Unified multi-tier LLM orchestration and routing  
**Status:** Active  
**Description:** Universal LLM interface providing intelligent routing across Granger's multi-tiered AI infrastructure. Seamlessly integrates:
- **Claude Max/Opus**: Via Docker proxy with OAuth authentication (see [Docker Auth Guide](04_implementation/tutorials/LLM_CALL_DOCKER_AUTHENTICATION.md))
- **Claude API**: Background intelligence for complex reasoning and orchestration
- **Ollama (Local)**: Fast local inference for RL learning loops with zero latency
- **RunPod (via runpod_ops)**: 30B-70B model fine-tuning and high-performance inference
- **LiteLLM**: Access to all frontier models (GPT-4, Gemini, Claude, etc.)

Features intelligent task routing based on complexity, cost, latency, and privacy requirements. Provides persistent conversations, context-aware delegation, and 16 built-in validators. Docker deployment includes enhanced authentication helpers and shell integration for Claude Max. This unified interface ensures optimal model selection for every task while maintaining a single, consistent API across all tiers.

**Project:** fine_tuning  
**Path:** `/home/graham/workspace/experiments/fine_tuning/`  
**GitHub:** `git+https://github.com/grahama1970/fine_tuning.git`  
**Purpose:** Model fine-tuning and training pipeline  
**Status:** Active  
**Dependencies:** runpod_ops (GPU compute), ArangoDB (Q&A data)  
**Description:** Comprehensive pipeline for fine-tuning language models with LoRA adapters and student-teacher thinking enhancement. Features DAPO RL algorithm, entropy-aware training, ArangoDB Q&A generation, Claude-powered hints, and deployment to Hugging Face. Integrates with runpod_ops for GPU orchestration.

### MCP Services
**Project:** arxiv-mcp-server  
**Path:** `/home/graham/workspace/mcp-servers/arxiv-mcp-server/`  
**GitHub:** `git+https://github.com/blazickjp/arxiv-mcp-server.git`  
**Purpose:** ArXiv paper search and retrieval MCP service  
**Status:** Active  
**Description:** Research automation bot with 45+ tools for finding evidence to support or contradict hypotheses across ArXiv papers. Works as both CLI tool and MCP server with automated literature review capabilities.

**Project:** mcp-screenshot  
**Path:** `/home/graham/workspace/experiments/mcp-screenshot/`  
**GitHub:** `git+https://github.com/grahama1970/mcp-screenshot.git`  
**Purpose:** Screenshot capture and analysis MCP service  
**Status:** Development  
**Description:** AI-powered screenshot capture and image analysis tool with three-layer architecture. Features screen capture, AI-powered analysis via Gemini, expert verification, screenshot history, and BM25 text search capabilities.  

## User Interface Modules

### Annotation Interface
**Project:** annotator  
**Path:** `/home/graham/workspace/experiments/annotator/`  
**GitHub:** `git+https://github.com/grahama1970/marker-ground-truth.git`  
**Purpose:** Human annotation interface for marker training data  
**Status:** Active  
**UI Type:** Web Interface  
**Description:** Sophisticated web-based PDF annotation tool for creating high-quality ground truth data. Features active learning, multi-annotator support, reinforcement learning optimization, recipe system, and human-in-the-loop ML for continuous model improvement.

### Chat Interface
**Project:** chat  
**Path:** `/home/graham/workspace/experiments/chat/`  
**GitHub:** *Local repository only - no remote*  
**Purpose:** Conversational interface for Granger ecosystem  
**Status:** Development  
**UI Type:** Chat Interface  
**Description:** Modern, extensible chat interface serving as UX shell for integrating multiple MCP servers. Built with React, FastAPI, and Docker, providing Claude/ChatGPT-level user experience with modular MCP architecture.

### Terminal Interface
**Project:** aider-daemon  
**Path:** `/home/graham/workspace/experiments/aider-daemon/`  
**GitHub:** `git+https://github.com/grahama1970/aider-daemon.git`  
**Purpose:** Command-line interface and automation daemon  
**Status:** Active  
**UI Type:** CLI/Daemon  
**Description:** AI pair programming in terminal environment. Enables collaborative coding with LLMs to start new projects or build on existing codebases, integrating with the Granger ecosystem for enhanced development workflows.  

## Project Categories

### By Development Status
- **Active:** 17 projects (fully operational)
- **Development:** 4 projects (under active development)
- **Work in Progress:** 1 project (early stage)

### By Type
- **Core Infrastructure:** 6 projects (Hub, RL, Test, World Model, Docs, UI System)
- **Infrastructure Services:** 1 project (runpod_ops - GPU compute)
- **Processing Spokes:** 9 projects (Data, Document, Media, AI, Presentation)
- **User Interfaces:** 3 projects (Web, Chat, CLI)
- **MCP Services:** 3 projects (ArXiv, Screenshot, etc.)

### By Primary Function
- **Data Ingestion:** darpa_crawl, gitget, youtube_transcripts
- **Document Processing:** sparta, marker  
- **Knowledge Management:** arangodb, shared_claude_docs, world_model, memvid
- **AI Integration:** llm_call, fine_tuning, granger_hub
- **User Experience:** chat, annotator, aider-daemon, granger-ui
- **Research & Analysis:** arxiv-mcp-server, mcp-screenshot
- **Infrastructure:** runpod_ops (GPU compute), claude-test-reporter, rl_commons, world_model
- **Visual & Temporal Storage:** memvid
- **Presentation & Reporting:** ppt

## Usage Guidelines

### For Automation Scripts
```bash
# Read project paths programmatically
source /home/graham/workspace/shared_claude_docs/docs/GRANGER_PROJECTS.md
```

### For Slash Commands
Both `/cleanup` and `/audit` commands reference this file for:
- Project discovery and iteration
- Status tracking and reporting
- Dependency relationship mapping
- Category-based operations

### For Development
- **New Projects:** Add to appropriate category with full metadata
- **Status Changes:** Update status field when projects change phase
- **Deprecation:** Move to archived section rather than delete
- **Dependencies:** Document inter-project relationships

## Maintenance

### Update Frequency
- **Immediate:** When projects are added, moved, or significantly changed
- **Weekly:** Status updates during active development phases
- **Monthly:** Comprehensive review of all project statuses

### Validation
Projects listed here should:
- [ ] Have valid filesystem paths
- [ ] Contain proper project structure (src/, tests/, docs/)
- [ ] Include pyproject.toml or equivalent configuration
- [ ] Be accessible by automation tools

### Version Control
This file is version controlled and changes should be:
1. Reviewed before committing
2. Documented with clear commit messages
3. Synchronized across all dependent systems

## Integration Points

### Commands That Use This Registry
- `/granger-verify` - Unified verification system for all projects
- `/cleanup` - Clean single project directory
- `/cleanup-all` - Iterates through all project paths
- `/audit` - Analyze single project
- `/audit-all` - Analyzes each project and generates reports
- `/ecosystem-report` - Generate comprehensive health report
- `/ppt-create` - Create PowerPoint presentations
- `/ppt-update` - Update existing presentations
- `/ppt-monitor` - Monitor and auto-update presentations

### Automation Systems
- Build pipelines reference these paths
- Monitoring systems track these projects
- Deployment scripts use this registry
- Documentation generators read from this source

## Future Considerations

### Planned Additions
- Project health monitoring endpoints
- Automated status detection
- Dependency graph visualization
- Performance metrics tracking

### Scalability
As the ecosystem grows:
- Consider breaking into category-specific files
- Implement automated project discovery
- Add metadata for deployment and monitoring
- Include resource requirements and constraints

## GitHub Repository Status

### Projects WITH GitHub repositories (ready for pyproject.toml import):
- ✅ granger_hub: `git+https://github.com/grahama1970/granger_hub.git`
- ✅ rl_commons: `git+https://github.com/grahama1970/rl-commons.git`
- ✅ claude-test-reporter: `git+https://github.com/grahama1970/claude-test-reporter.git`
- ✅ sparta: `git+https://github.com/grahama1970/SPARTA.git`
- ✅ marker: `git+https://github.com/grahama1970/marker.git`
- ✅ arangodb: `git+https://github.com/grahama1970/arangodb.git`
- ✅ youtube_transcripts: `git+https://github.com/grahama1970/youtube-transcripts-search.git`
- ✅ memvid: `git+https://github.com/grahama1970/memvid.git`
- ✅ llm_call: `git+https://github.com/grahama1970/llm_call.git`
- ✅ fine_tuning: `git+https://github.com/grahama1970/fine_tuning.git`
- ✅ arxiv-mcp-server: `git+https://github.com/blazickjp/arxiv-mcp-server.git`
- ✅ mcp-screenshot: `git+https://github.com/grahama1970/mcp-screenshot.git`
- ✅ annotator: `git+https://github.com/grahama1970/marker-ground-truth.git`
- ✅ aider-daemon: `git+https://github.com/grahama1970/aider-daemon.git`

### Projects WITHOUT GitHub repositories (need creation):
- ❌ shared_claude_docs (local repo only - no remote)
- ❌ granger-ui (no Git repository)
- ❌ world_model (no Git repository)
- ❌ runpod_ops (no Git repository) ⚠️ **CRITICAL - needed by fine_tuning**
- ❌ darpa_crawl (no Git repository)
- ❌ gitget (no Git repository)
- ❌ ppt (no Git repository)
- ❌ chat (local repo only - no remote)

**Action Required:** The projects without GitHub repositories need to be:
1. Created on GitHub using `gh repo create`
2. Pushed to GitHub
3. Updated in this registry with their `git+https://` URLs
