# Slash Commands Guide for Claude Projects

## Overview

Slash commands are special directives that can be used in prompts to Claude to trigger specific behaviors or workflows. This guide documents all available slash commands across our projects.

## Core Slash Commands

### /task
Create a task list for systematic implementation.

**Usage:**
```
/task Create a comprehensive test suite for the marker project
```

**Output:**
- Generates a numbered task list following TASK_LIST_TEMPLATE_GUIDE_V2.md
- Each task includes clear steps and validation criteria
- Includes dependency tracking between tasks

### /test
Run tests with specific validation criteria.

**Usage:**
```
/test Run unit tests for ArangoDB connection module
```

**Features:**
- Executes tests with REAL vs FAKE validation
- Generates JSON and HTML reports
- Implements honeypot tests to detect mocking

### /validate
Validate project structure and conventions.

**Usage:**
```
/validate Check if marker project follows CLAUDE.md standards
```

**Checks:**
- Project structure compliance
- File size limits (500 lines max)
- Documentation presence
- Test coverage requirements

### /sync
Synchronize documentation or code between projects.

**Usage:**
```
/sync Update all projects with latest CLAUDE.md template
```

### /cleanup
Apply cleanup to current or specified project.

**Usage:**
```
/cleanup              # Auto-detect current project
/cleanup [path]       # Clean specific project
/clean                # Alias
```

**Features:**
- Auto-detects current project from working directory
- Organizes stray source files into proper src/ hierarchy
- Moves log files to logs/ directory
- Ensures tests/ mirrors src/ structure exactly
- Archives temporary and debug files
- **Thoroughly organizes docs/ directory with evolution management**
- **Detects and archives duplicate, outdated, or superseded documentation**
- **Maintains timestamped archive with clear reasoning**
- **Validates documentation references and cross-links**

### /cleanup-all
Apply comprehensive cleanup to entire Granger ecosystem.

**Usage:**
```
/cleanup-all          # Clean all 18 projects
/granger-cleanup      # Alias
```

**Features:**
- Processes all projects in GRANGER_PROJECTS.md
- Same cleanup operations as /cleanup but ecosystem-wide
- **Cross-project documentation consistency and deduplication**
- **Ecosystem-wide archive strategy with uniform standards**
- Generates summary report of all cleanup operations

### /audit
Analyze current or specified project for README vs implementation alignment.

**Usage:**
```
/audit                # Auto-detect current project
/audit [path]         # Audit specific project
/analyze              # Alias
```

**Features:**
- Auto-detects current project from working directory
- Analyzes codebase vs README claims
- Identifies unimplemented features and undocumented code
- Generates detailed individual project report
- Provides prioritized recommendations for alignment

### /audit-all
Analyze entire ecosystem and generate master state report.

**Usage:**
```
/audit-all            # Audit all 18 projects
/granger-audit        # Alias
```

**Features:**
- Processes all projects in GRANGER_PROJECTS.md
- Generates individual reports for each project
- Creates master ecosystem state report with health overview
- Provides ecosystem-wide recommendations and trends
- Saves reports to `/home/graham/workspace/shared_claude_docs/docs/current_state_of_granger/`

### /ecosystem-report
Generate comprehensive ecosystem documentation and strategic reports.

**Usage:**
```
/ecosystem-report     # Generate current state + whitepaper docs
/whitepaper          # Alias for strategic documentation focus
/ecosystem           # Short alias
```

**Features:**
- Performs comprehensive audit of all 18 projects (like `/audit-all`)
- Generates current state documentation with date prefixes (`MMDD_`)
- Updates whitepaper materials for strategic communication
- Creates multiple document types: health dashboards, architecture overviews, capability matrices
- Outputs to both `current_state_of_granger/` and `whitepaper/` directories
- Provides stakeholder-ready documentation with executive summaries

### /tasks
Generate task list for current or specified project.

**Usage:**
```
/tasks                # Auto-detect current project
/tasks [path]         # Generate tasks for specific project
/task-list            # Alias
/todo                 # Alias
```

**Features:**
- Auto-detects current project from working directory
- Analyzes README claims vs actual implementation
- Identifies outstanding features and missing documentation
- Generates prioritized task list following TASK_LIST_TEMPLATE_GUIDE_V2.md
- Creates file at `[project]/docs/tasks/00N_Tasks_List.md`
- Includes implementation guidelines and success criteria

### /communicate
Test inter-project communication via Granger Hub.

**Usage:**
```
/communicate Test marker to arangodb schema exchange
```

## Project-Specific Commands

### Marker Project

#### /extract
Extract content from PDFs using marker.

**Usage:**
```
/extract Process research_paper.pdf and generate schema
```

### ArangoDB Project

#### /query
Execute AQL queries on the database.

**Usage:**
```
/query FOR doc IN papers FILTER doc.year == 2024 RETURN doc
```

#### /graph
Visualize graph relationships.

**Usage:**
```
/graph Show citation network for paper arxiv:2401.12345
```

### YouTube Transcripts Project

#### /transcript
Download and process YouTube video transcript.

**Usage:**
```
/transcript https://youtube.com/watch?v=VIDEO_ID
```

## MCP-Related Commands

### /mcp-setup
Configure MCP server in Claude Desktop.

**Usage:**
```
/mcp-setup Add arxiv-mcp-server to configuration
```

### /mcp-test
Test MCP server functionality.

**Usage:**
```
/mcp-test Verify arxiv server is responding
```

## Development Commands

### /debug
Enable debug mode for detailed logging.

**Usage:**
```
/debug Enable for next operation
```

### /profile
Profile code performance.

**Usage:**
```
/profile Measure extraction time for 100-page PDF
```

### /refactor
Suggest refactoring for code improvement.

**Usage:**
```
/refactor Optimize database query in module.py
```

## Workflow Commands

### /pipeline
Execute full pipeline workflow.

**Usage:**
```
/pipeline PDF → Extract → Validate → Store → Index
```

### /batch
Process multiple items in batch.

**Usage:**
```
/batch Process all PDFs in /data/papers/ directory
```

## Best Practices

1. **Chain Commands**: Commands can be chained for complex workflows
   ```
   /extract paper.pdf && /validate schema && /communicate send to arangodb
   ```

2. **Use Flags**: Many commands support flags for options
   ```
   /test --coverage --profile --timeout=60
   ```

3. **Environment Context**: Commands respect .env configuration
   ```
   /query --database=production
   ```

4. **Error Handling**: Commands should fail gracefully
   ```
   /extract nonexistent.pdf || /debug last-error
   ```

## Custom Command Creation

To create a new slash command:

1. Define in project's CLAUDE.md
2. Implement handler in appropriate module
3. Register with command parser
4. Document usage and examples

Example:
```python
@slash_command("/mycmd")
def my_command(args):
    """Custom command implementation."""
    # Implementation
    pass
```

## Command Aliases

Common aliases for convenience:

- `/t` → `/task`
- `/v` → `/validate`
- `/d` → `/debug`
- `/q` → `/query`

## Integration with Claude

When using slash commands with Claude:

1. Be specific about context
2. Provide necessary file paths
3. Specify target projects clearly
4. Include relevant configuration

Example prompt:
```
Using the marker project at /home/graham/workspace/experiments/marker:
/task Create integration tests for PDF table extraction
/validate Ensure tests follow TASK_LIST_TEMPLATE_GUIDE_V2.md
```
