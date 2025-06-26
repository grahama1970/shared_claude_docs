# GitGet Module Analysis

## Overview
GitGet is a CLI utility for sparse cloning, analyzing, and LLM-based documentation of GitHub repositories. It provides intelligent code structure analysis using tree-sitter for over 100 programming languages. As a Granger spoke module, it specializes in repository analysis while integrating seamlessly with the ecosystem.

## Core Capabilities
- **Sparse Cloning**: Efficiently clone only needed parts of repositories
- **Code Analysis**: Tree-sitter based AST parsing for 100+ languages
- **Text Chunking**: Intelligent document splitting with structure preservation
- **LLM Summarization**: AI-powered code and documentation summaries
- **Metadata Extraction**: Functions, classes, dependencies, imports
- **Configuration Support**: Respects `.gitingest` TOML files for repository-specific settings

## Technical Features
- Enhanced markdown parsing with section hierarchy
- Code block association and context preservation
- Token-aware chunking for LLM compatibility
- Multiple output formats (JSON, tree, chunks, summaries)

## Integration Status
- **MCP Server**: ✅ Fully implemented with 4 tools (clone, analyze, search, status)
- **Module Adapter**: ✅ GitGetModule class for hub integration
- **Output Renderers**: ✅ JSON, Markdown, ArangoDB formats
- **Configuration**: ✅ Supports `.gitingest` TOML files (as of 2025-01-06)
- **See**: GRANGER_INTEGRATION_SUMMARY.md for details

## Output Structure
```
repos/{repo_name}_gitget/
├── digest/
├── summary/
├── tree/
├── chunks/
└── llm_summary/
```

## Path
`/home/graham/workspace/experiments/gitget/`

## Priority
**High** - Essential for code understanding workflows