# Test Reporting with claude-test-reporter

## Overview

All Claude projects MUST use the  package for consistent test reporting across the ecosystem. This ensures standardized test output, beautiful HTML reports, and multi-project monitoring capabilities.

## Status

As of the latest update, **100% of projects with pyproject.toml** are using claude-test-reporter.

## Installation

Add to your project's dependencies in :



## Features

- 🚀 **Zero Dependencies** - Uses only Python standard library
- 📊 **Beautiful HTML Reports** - Sortable, searchable, exportable
- 🔍 **Pytest Integration** - Works seamlessly with pytest-json-report
- 🎨 **Customizable Themes** - Per-project branding support
- 🤖 **CI/CD Ready** - Agent-friendly report adapters
- 📈 **Multi-Project Dashboard** - Monitor all projects in one view
- 🕐 **Test History Tracking** - Trends and performance over time
- 🎲 **Flaky Test Detection** - Automatic identification of unreliable tests
- 🔄 **Agent Comparison** - Compare results between different agents

## Basic Usage

### Generate Test Report



### Integration with pytest



## Configuration

Create  in your project root:



## Multi-Project Dashboard

Monitor all projects from a single dashboard:



## CI/CD Integration

### GitHub Actions



## Test Standards Alignment

All tests must align with the standards defined in TASK_LIST_TEMPLATE_GUIDE_V2.md:

- **REAL Tests**: Must interact with live systems
- **Duration Requirements**: Tests must meet minimum duration thresholds
- **Confidence Reporting**: Self-reported confidence ≥90%
- **Honeypot Tests**: Include tests designed to fail

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure claude-test-reporter is in dependencies
2. **No Reports Generated**: Check pytest is using --json-report flag
3. **Missing Test Data**: Verify test discovery is working

### Debug Mode



## Projects Using claude-test-reporter

All 25 projects with pyproject.toml now use claude-test-reporter:
- agent_tools
- arangodb
- bubblewrap
- claude-code-mcp
- claude_comms
- claude_max_proxy
- claude-module-communicator
- claude-test-reporter
- code-index-mcp
- comms
- complexity
- docker-mcp
- fetch-page
- gitget
- llm-summarizer
- marker
- mcp-screenshot
- mcp-server-arangodb
- mcp_natrium_orchestrator
- mcp_tools
- pdf_extractor
- sparta
- student_teacher
- fine_tuning
- youtube_transcripts
