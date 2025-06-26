# Complete Granger Ecosystem Architecture

*Last Updated: 2025-06-02*

## Overview

The Granger ecosystem is a sophisticated hub-and-spoke architecture designed for intelligent orchestration of AI-powered document and code analysis. This document provides the complete, accurate representation of all modules and their relationships.

## Architecture Layers

```
         ┌─────────────┐                    ┌──────────────┐
         │    Chat     │                    │Marker Ground │ ← User Interface Layer
         │ (MCP Chat)  │                    │    Truth     │
         └──────┬──────┘                    └──────┬───────┘
                │                                  │
                └──────────────┬───────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │      granger_hub            │ ← HUB (Central Orchestrator)
                    └─────────────┬───────────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                │                 │                 │
         ┌──────▼──────┐   ┌──────▼──────┐   ┌────▼─────┐
         │ RL Commons  │   │Test Reporter│   │ Shared   │ ← Shared Services
         │  (Learning) │   │   Engine    │   │  Docs    │
         └─────────────┘   └─────────────┘   └──────────┘
                                  │
    ┌────────────────────────────┼────────────────────────────┐
    │                            │                            │
┌───▼───┐ ┌────────┐ ┌──────┐ ┌─▼────┐ ┌──────┐ ┌─────┐ ┌─▼────┐
│Marker │ │GitGet  │ │SPARTA│ │ArXiv │ │Aider │ │ MCP │ │DARPA │ ← Spoke Modules
└───┬───┘ └────┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ │Shot │ └──┬───┘
    │          │        │        │        │      └─────┘    │
┌───▼───┐ ┌────▼────┐ ┌─▼────┐ ┌─▼────┐ ┌─▼────┐ ┌──────┐ ┌▼──┐
│YouTube│ │ArangoDB │ │Claude│ │Unsloth│ │ ...  │ │ ...  │ │...│
│Trans. │ │(Storage)│ │ Max  │ │ Fine  │ │      │ │      │ │   │
└───────┘ └─────────┘ └──────┘ └──────┘ └──────┘ └──────┘ └───┘
```

## Module Categories and Descriptions

### 1. Central HUB

#### granger_hub
- **Path**: `/home/graham/workspace/experiments/granger_hub/`
- **Purpose**: Central orchestrator for all modules with RL-powered intelligence
- **Key Features**:
  - ✅ **ACTIVELY USES RL Commons** for intelligent routing
  - ContextualBandit for module selection
  - DQN for pipeline optimization and error handling
  - PPO for resource allocation
  - Manages inter-module communication
  - Handles workflow orchestration with learning capabilities

### 2. Shared Services

These modules provide cross-cutting functionality used by all other modules:

#### RL Commons
- **Path**: `/home/graham/workspace/experiments/rl_commons/`
- **Purpose**: Reinforcement learning algorithms for intelligent orchestration
- **Key Features**:
  - ✅ **ACTIVELY INTEGRATED** with HUB via hub_decisions.py
  - Provides ContextualBandit for module selection
  - DQN agents for pipeline optimization
  - PPO agents for resource allocation
  - Experience replay and learning from outcomes
  - Real-time decision improvement

#### Test Reporter Engine
- **Path**: `/home/graham/workspace/experiments/claude-test-reporter/`
- **Purpose**: Universal test reporting across all modules
- **Key Features**:
  - Zero dependencies
  - Markdown report generation
  - Consistent test result formatting
  - Used by all modules for test reporting

#### Shared Documentation
- **Path**: `/home/graham/workspace/shared_claude_docs/`
- **Purpose**: Central documentation and standards
- **Key Features**:
  - Architecture documentation
  - Module integration guides
  - Coding standards (CLAUDE.md)
  - Scenario planning

### 3. User Interface Modules

These provide human interaction points:

#### Chat
- **Path**: `/home/graham/workspace/experiments/chat/`
- **Purpose**: Universal MCP chat interface
- **Key Features**:
  - Web-based chat UI
  - MCP protocol support
  - Multi-module interaction
  - Primary user interface for the system

#### Marker Ground Truth
- **Path**: `/home/graham/workspace/experiments/annotator/`
- **Purpose**: Label Studio integration for training data
- **Key Features**:
  - Web UI for document annotation
  - Benchmark dataset creation
  - Quality control for Marker output
  - Human-in-the-loop validation

### 4. Spoke Modules - Document/Content Processing

#### Marker
- **Path**: `/home/graham/workspace/experiments/marker/`
- **Purpose**: Multi-format document extraction
- **Supported Formats**:
  - PDF (with advanced table/image extraction)
  - PowerPoint (PPTX) - native extraction
  - Word (DOCX) - enhanced extraction
  - XML - secure parsing
  - HTML - structure preservation
- **Key Features**:
  - Optional Claude AI enhancements
  - ArangoDB export capability
  - Unified output schema
  - MCP server implementation

#### SPARTA
- **Path**: `/home/graham/workspace/experiments/sparta/`
- **Purpose**: Space cybersecurity document processing
- **Key Features**:
  - Specialized for DARPA documents
  - Security-focused extraction
  - Integration with defense systems

#### ArXiv MCP Server
- **Path**: `/home/graham/workspace/mcp-servers/arxiv-mcp-server/`
- **Purpose**: Research paper search and retrieval
- **Key Features**:
  - 45+ MCP tools
  - Advanced search capabilities
  - Paper metadata extraction
  - Citation network analysis

#### YouTube Transcripts
- **Path**: `/home/graham/workspace/experiments/youtube_transcripts/`
- **Purpose**: Video transcript extraction and analysis
- **Key Features**:
  - 94% test coverage
  - Transcript search
  - Timeline extraction
  - Multi-language support

### 5. Spoke Modules - Code/Development

#### GitGet
- **Path**: `/home/graham/workspace/experiments/gitget/`
- **Purpose**: GitHub repository analysis
- **Key Features**:
  - Sparse cloning
  - Tree-sitter code parsing (100+ languages)
  - Code structure extraction
  - LLM-powered summarization
- **Status**: Needs Granger integration (see GITGET_GRANGER_INTEGRATION.md)

#### Aider Daemon
- **Path**: `/home/graham/workspace/experiments/aider-daemon/`
- **Purpose**: AI-powered code assistance
- **Key Features**:
  - Automated code modifications
  - Multi-file editing
  - Git integration

#### Unsloth WIP
- **Path**: `/home/graham/workspace/experiments/fine_tuning/`
- **Purpose**: LLM fine-tuning workflows
- **Key Features**:
  - LoRA adapter training
  - Student-teacher models
  - Optimization pipelines

### 6. Spoke Modules - Infrastructure

#### ArangoDB
- **Path**: `/home/graham/workspace/experiments/arangodb/`
- **Purpose**: Graph database and knowledge storage
- **Key Features**:
  - Document and graph storage
  - Vector search capabilities
  - Knowledge graph queries
  - Central storage for all modules

#### Claude Max Proxy
- **Path**: `/home/graham/workspace/experiments/llm_call/`
- **Purpose**: Unified LLM interface
- **Key Features**:
  - Multiple LLM provider support
  - Token optimization
  - Caching layer
  - Rate limiting

#### MCP Screenshot
- **Path**: `/home/graham/workspace/experiments/mcp-screenshot/`
- **Purpose**: Screen capture and analysis
- **Key Features**:
  - Browser automation
  - Visual analysis
  - Integration with other tools

#### DARPA Crawl
- **Path**: `/home/graham/workspace/experiments/darpa_crawl/`
- **Purpose**: Web crawling and data collection
- **Key Features**:
  - Targeted crawling
  - Data extraction
  - Feed into SPARTA pipeline

## Critical Integration Points

### 1. HUB ← → RL Commons ✅ IMPLEMENTED
- **Current State**: Fully integrated and operational
- **Implementation**: Multiple RL agents in hub_decisions.py
- **Impact**: Granger can learn and improve from experience

### 2. All Modules → ArangoDB
- **Current State**: Partially implemented
- **Required**: Standardized schemas for all modules
- **Impact**: Unified knowledge graph

### 3. All Modules → Test Reporter
- **Current State**: Available but underutilized
- **Required**: Consistent test reporting
- **Impact**: Better visibility into system health

## Workflow Examples

### Research Pipeline
```python
# User request through Chat UI
request = "Analyze recent papers on transformer architectures"

# HUB orchestrates:
1. ArXiv → Search for papers
2. Marker → Extract PDF content
3. GitGet → Analyze reference implementations
4. ArangoDB → Store knowledge graph
5. Test Reporter → Generate analysis report
```

### Document Analysis Pipeline
```python
# User uploads document set
request = "Extract all tables from these financial reports"

# HUB orchestrates:
1. Marker → Extract with Claude table analysis
2. Ground Truth → Human validation if needed
3. ArangoDB → Store structured data
4. Test Reporter → Quality metrics
```

### Code Understanding Pipeline
```python
# User provides repository
request = "Understand this codebase architecture"

# HUB orchestrates:
1. GitGet → Clone and analyze structure
2. Marker → Extract any docs in repo
3. Aider → Suggest improvements
4. ArangoDB → Build dependency graph
```

## Key Observations

1. **Architecture is Sound**: Hub-and-spoke design enables flexibility
2. **RL Integration COMPLETE**: HUB actively uses RL Commons for intelligent decisions
3. **Module Quality**: Individual modules are well-built
4. **Integration Active**: RL-powered module selection, pipeline optimization
5. **UI Layer**: Clear separation of user interfaces from processing

## RL Implementation Details

The HUB uses multiple RL agents for different decision types:
- **Module Selection**: ContextualBandit learns which modules work best for tasks
- **Pipeline Optimization**: DQN agent optimizes module sequences
- **Resource Allocation**: PPO agent manages CPU/memory/timeouts
- **Error Handling**: DQN agent learns recovery strategies

## Next Steps

1. **Monitor RL Performance**: Track learning metrics and improvements
2. **Complete GitGet Integration**: Follow GITGET_GRANGER_INTEGRATION.md
3. **Standardize Module Interfaces**: Ensure all modules follow BaseModule pattern
4. **Enhance Cross-Module Workflows**: Build on RL foundation
5. **Document RL Tuning**: Create guide for adjusting learning parameters

## Module Registration Format

When adding new modules, include:
- Path to repository
- Purpose (one line)
- Key features (3-5 bullets)
- Integration status
- Dependencies on other modules
- Category placement

## Maintenance Notes

This document should be updated when:
- New modules are added
- Module purposes change significantly
- Integration patterns evolve
- Architecture decisions are made
- Critical gaps are identified or resolved