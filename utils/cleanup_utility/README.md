# Project Cleanup Utility

An automated utility for cleaning up and validating multiple projects, ensuring they:
- Have proper documentation (README.md, CLAUDE.md)
- Include claude-test-reporter dependency
- Implement slash commands (for Claude projects)
- Have proper MCP implementation (for MCP servers)
- Pass all tests
- Validate README claims against implementation
- Check security and code quality

## Files

### Core Scripts
- **enhanced_cleanup.py** - Comprehensive Python cleanup utility with parallel processing
- **simple_cleanup.py** - Simpler Python cleanup utility
- **run_enhanced_cleanup.sh** - Runner for enhanced cleanup (recommended)
- **run_cleanup_simple.sh** - Runner for simple cleanup

### Configuration
- **cleanup_config.json** - Default configuration (with SSH for remote)
- **cleanup_config_localhost.json** - Localhost configuration (no SSH)

### Support Files
- **install_dependencies.sh** - Install required dependencies
- **requirements.txt** - Python dependencies
- **test_cleanup.sh** - Test the setup
- **test_enhanced_cleanup.sh** - Test enhanced cleanup functionality

### Scheduled Runs & Compliance
- **scheduled_cleanup.sh** - Safe read-only script for cron jobs
- **claude_compliance_checker.py** - Check code compliance with CLAUDE.md rules
- **SCHEDULED_RUNS_AND_COMPLIANCE.md** - Guide for automation and compliance

## Quick Start

1. Test the setup:
   ```bash
   ./test_cleanup.sh
   ```

2. Install dependencies (recommended):
   ```bash
   ./install_dependencies.sh
   ```

3. Run the enhanced cleanup:
   ```bash
   # Default run (parallel, live mode)
   ./run_enhanced_cleanup.sh
   
   # Dry run to see what would be done
   ./run_enhanced_cleanup.sh --dry-run
   
   # Verbose output
   ./run_enhanced_cleanup.sh --verbose
   
   # Sequential processing
   ./run_enhanced_cleanup.sh --sequential
   ```

4. Or run the simple cleanup:
   ```bash
   python3 simple_cleanup.py
   # or
   ./run_cleanup_simple.sh
   ```

## What it does

### Enhanced Cleanup (recommended)

The enhanced cleanup utility provides comprehensive validation:

1. **Git Safety**: Creates a safety branch before making changes
2. **Documentation Analysis**: 
   - Checks for README.md with essential sections
   - Validates CLAUDE.md for AI guidelines
   - Compares README claims against actual implementation
3. **Dependency Management**:
   - Validates claude-test-reporter in pyproject.toml
   - Checks for security vulnerabilities
   - Analyzes dependency tree and conflicts
4. **Code Structure**:
   - Validates package organization
   - Identifies misplaced files
   - Checks for proper imports
5. **Testing**:
   - Runs pytest with coverage (if not in dry-run mode)
   - Reports test statistics and failures
6. **Project-Specific Validations**:
   - Slash commands (Claude projects)
   - MCP implementation (MCP servers)
   - CLI interfaces (tool projects)
   - Inter-project communication
7. **Code Quality**:
   - Counts TODO/FIXME comments
   - Identifies large files (>500 lines)
   - Basic security checks for hardcoded secrets
8. **Reporting**: 
   - Individual JSON reports per project
   - Comprehensive markdown report with executive summary
   - Project status matrix
   - Inter-project communication matrix

### CLAUDE.md Compliance Checker (NEW)

The compliance checker analyzes code against CLAUDE.md rules WITHOUT auto-refactoring:

- Extracts rules from CLAUDE.md files
- Checks Python files for compliance
- Reports violations by severity (error/warning/info)
- Generates actionable reports for manual review
- Does NOT modify any code

### Simple Cleanup

The simple cleanup provides basic validation:
- README.md existence
- claude-test-reporter configuration
- Basic slash command checking
- MCP implementation checking
- Test execution

## Configuration

### For Localhost (Claude Code)
Edit `cleanup_config_localhost.json`:
```json
{
  "timeout_ms": 5000,
  "parallel_workers": 4,
  "projects": [
    "/path/to/project1/",
    "/path/to/project2/"
  ]
}
```

### For Remote (Claude Desktop)
Edit `cleanup_config.json` with SSH settings.

## Reports

Reports are saved in the `cleanup_reports/` directory:

### Enhanced Cleanup Reports
- `comprehensive_report_TIMESTAMP.md` - Full markdown report with analysis
- `summary_TIMESTAMP.txt` - Quick text summary
- `TIMESTAMP-PROJECT_NAME.json` - Detailed JSON per project

### Simple Cleanup Reports
- `summary_TIMESTAMP.md` - Basic markdown summary
- `TIMESTAMP-PROJECT_NAME.json` - JSON results per project

## Project-Specific Features

The enhanced cleanup recognizes project types and applies specific validations:

| Project | Type | Special Checks |
|---------|------|----------------|
| sparta | framework | PyTorch/Transformers imports, tests required |
| marker | tool | CLI interface, command validation |
| arangodb | database | Configuration files, connection setup |
| youtube_transcripts | tool | API keys, youtube_dl/whisper imports |
| claude_max_proxy | proxy | Endpoint configuration |
| arxiv-mcp-server | mcp | Full MCP validation suite |
| granger_hub | hub | Central communication and orchestration |
| claude-test-reporter | testing | Test framework validation |
| fine_tuning | experimental | WIP status, basic checks only |
| marker-ground-truth | dataset | Data structure validation |
| mcp-screenshot | mcp | MCP validation, PIL/screenshot imports |

## Advanced Usage

### Parallel vs Sequential
```bash
# Parallel processing (default, faster)
./run_enhanced_cleanup.sh

# Sequential processing (easier debugging)
./run_enhanced_cleanup.sh --sequential
```

### Dry Run Mode
```bash
# See what would be done without making changes
./run_enhanced_cleanup.sh --dry-run
```

### Custom Configuration
```bash
# Use a different config file
./run_enhanced_cleanup.sh --config my_config.json
```

### Scheduled Runs (Safe for Cron)
```bash
# Add to crontab for weekly checks (read-only)
0 7 * * 1 /path/to/scheduled_cleanup.sh

# This runs in dry-run mode and can send notifications
# See SCHEDULED_RUNS_AND_COMPLIANCE.md for details
```

### CLAUDE.md Compliance Checking
```bash
# Check a single project for CLAUDE.md compliance
python3 claude_compliance_checker.py /path/to/project

# Check all projects
for project in /home/graham/workspace/experiments/*; do
    python3 claude_compliance_checker.py "$project"
done

# Note: This ONLY reports violations, it does NOT auto-fix
```

## Scheduled Runs and Automation

### ✅ Safe for Automation
- **scheduled_cleanup.sh** - Runs in read-only mode, generates reports
- **Pre-commit hooks** - Check for issues before commits
- **CI/CD integration** - Validate PRs automatically

### ❌ NOT Safe for Automation
- **Full cleanup** - Never run with --live in cron
- **Auto-refactoring** - Don't auto-enforce CLAUDE.md rules
- **Branch creation** - Avoid automatic git operations

See `SCHEDULED_RUNS_AND_COMPLIANCE.md` for detailed automation guidelines.

## Notes

- The utility is non-destructive by default
- Changes are made in a separate git branch
- If tests fail, changes are rolled back
- Missing dependencies (toml, pytest) will limit some features but won't prevent basic operation
- The enhanced version uses multiprocessing for better performance
- Progress bars shown if tqdm is installed
