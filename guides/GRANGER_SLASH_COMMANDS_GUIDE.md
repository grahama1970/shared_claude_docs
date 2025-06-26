# Granger Slash Commands Quick Start Guide

> **Central reference for all Granger ecosystem slash commands**  
> **Location**: `/home/graham/workspace/shared_claude_docs/guides/GRANGER_SLASH_COMMANDS_GUIDE.md`

---

## 🚀 **Essential Commands Overview**

### **Unified Verification System**
```bash
/granger-verify                            # Full ecosystem mock removal & testing
/granger-verify --fix                      # Remove all mocks automatically
/granger-verify --project granger_hub      # Single project verification
/granger-verify --all                      # Full ecosystem verification
/granger-verify --category "Intelligence Core"  # Category verification
/granger-verify --project arangodb --force-fix  # Force Claude to fix issues
```

### **Multi-AI Collaboration**
```bash
/granger-ai-collab               # Claude + Gemini iterative collaboration (up to 5 rounds)
```

### **Project Management**
```bash
/cleanup                          # Clean up current project
/cleanup-all                      # Clean all Granger projects
/audit                           # Audit single project
/audit-all                       # Audit all projects
```

### **Ecosystem Reporting**
```bash
/ecosystem-report                # Generate comprehensive health report
/granger-feature-sync            # Compare README vs actual features
/granger-feature-sync --implement # Auto-implement missing features
```

---

## 🔍 **Unified Verification Command: /granger-verify**

**Purpose**: Comprehensive project verification that removes ALL mocks/simulations, fixes imports, and ensures real API usage

### **Phase 1: Mock Removal (NEW)**
```bash
# Remove all mocks and simulations from entire ecosystem
/granger-verify --fix --auto

# Process projects in dependency order (Hub → Spokes)
# Automatically:
# - Removes all unittest.mock imports
# - Deletes @patch decorators
# - Replaces Mock() with real implementations
# - Converts relative imports to absolute
# - Runs Level 0 tests to find broken functionality
```

**Key Features**:
- **NO MOCKS POLICY**: All tests must use real services
- **Sequential Processing**: Hub fixed before spokes
- **Breaking Tests = Good**: Exposes real integration issues
- **Backup Creation**: .mock_backup files for all changes

### **Target Selection**
```bash
# Single project verification
/granger-verify --project granger_hub
/granger-verify --project arangodb
/granger-verify --project world_model

# Verify all projects
/granger-verify --all

# Verify by category
/granger-verify --category "Intelligence Core"
/granger-verify --category "spokes"
/granger-verify --category "User Interface"
```

### **Verification Modes**
```bash
# Full verification (default)
/granger-verify --project arangodb

# Tests only - skip cleanup and compliance
/granger-verify --project marker --tests-only

# Quick mode - reduced checks
/granger-verify --project sparta --quick

# No tests - only cleanup and compliance
/granger-verify --project llm_call --no-tests
```

### **Fix Options**
```bash
# Auto-fix common issues (default: enabled)
/granger-verify --project granger_hub --auto-fix

# Disable auto-fix
/granger-verify --project marker --no-auto-fix

# Force Claude to fix all issues
/granger-verify --project sparta --force-fix

# Set maximum fix iterations
/granger-verify --project arangodb --max-iterations 5
```

### **Output Options**
```bash
# Verbose output for debugging
/granger-verify --project granger_hub --verbose

# Quiet mode (minimal output)
/granger-verify --all --quiet

# Custom report directory
/granger-verify --all --report-dir ./my_reports/

# JSON output only
/granger-verify --project marker --json
```

### **Special Modes**
```bash
# Cron mode for scheduled runs
/granger-verify --all --cron --force-fix

# CI/CD mode with proper exit codes
/granger-verify --project $PROJECT --ci

# Parallel execution
/granger-verify --all --parallel 8
```

### **Complete Option Reference**
```bash
# Target Selection (one required)
--project PROJECT      # Single project
--all                 # All projects
--category CATEGORY   # By category

# Verification Options
--tests-only          # Skip cleanup/compliance
--no-cleanup          # Skip cleanup phase
--no-compliance       # Skip CLAUDE.md check
--no-tests           # Skip test execution
--quick              # Fast mode

# Fix Options
--auto-fix           # Auto-fix issues (default: true)
--no-auto-fix        # Disable auto-fix
--force-fix          # Generate fix directives for Claude
--max-iterations N   # Max fix attempts (default: 3)

# Output Options
--verbose, -v        # Detailed output
--quiet, -q          # Minimal output
--report-dir PATH    # Report location
--json              # JSON output only

# Special Modes
--cron              # Scheduled run mode
--ci                # CI/CD mode
--parallel N        # Parallel execution (default: 4)
```

---

## 🧹 **Project Management Commands**

### **/cleanup**

**Purpose**: Clean up current project (remove temp files, fix permissions, organize structure)

```bash
# Basic cleanup in current directory
/cleanup

# The command automatically:
# - Removes temporary files and caches
# - Fixes file permissions
# - Organizes project structure
# - Updates dependencies
# - Validates configuration
```

**Integrated into**: `/granger-verify` and `/verify-project` commands

### **/audit**

**Purpose**: Comprehensive project structure and dependency audit

```bash
# Audit current project
/audit

# Features:
# - Project structure validation
# - Dependency analysis
# - Configuration verification
# - Code quality assessment
# - Security review
```

---

## 🧪 **Testing Verification Features**

The `/granger-verify` command includes comprehensive test verification with skeptical analysis:

### **Key Testing Principles**
- ✅ **REAL Tests Only**: Must interact with live systems
- ❌ **No Mocks Allowed**: Detects and flags mock usage
- ⏱️ **Duration Thresholds**: Tests must meet minimum time requirements
- 🍯 **Honeypot Integration**: Includes designed-to-fail tests
- 📊 **Confidence Scoring**: 0-100% with supporting evidence

### **Duration Requirements**
| Operation Type | Minimum Duration | Rationale |
|----------------|------------------|-----------|
| Database Query | >0.1s | Connection overhead + query execution |
| API Call | >0.05s | Network latency + processing |
| File I/O | >0.01s | Disk access time |
| Integration Test | >0.5s | Multiple system interactions |
| Browser Automation | >1.0s | Page load + rendering |

### **Test-Focused Verification**
```bash
# Run only test verification (skip cleanup/compliance)
/granger-verify --project arangodb --tests-only

# Verify all project tests
/granger-verify --all --tests-only

# Force fix test issues
/granger-verify --project marker --tests-only --force-fix
```

---

## 📋 **CLAUDE.md Compliance**

All verification commands check compliance with `~/.claude/CLAUDE.md` standards:

### **Documentation Header Requirements**
```python
"""
Module: module_name.py
Description: Brief description of what this script file does

External Dependencies:
- package_name: https://docs.url.com
- another_package: https://docs.another.com

Sample Input:
>>> input_data = {"key": "value", "number": 42}

Expected Output:
>>> result = process_data(input_data)
>>> print(result)
{"processed": True, "value": "transformed_value", "count": 42}

Example Usage:
>>> from module_name import function
>>> result = function(input_data)
'expected output'
"""
```

### **Code Quality Checklist**
- [ ] ✓ Documentation headers in all files
- [ ] ✓ Type hints on all functions
- [ ] ✓ Documentation header contains description of the script file
- [ ] ✓ Documentation header contains all relevant third party package documentation URLs
- [ ] ✓ Documentation header contains sample input
- [ ] ✓ Documentation header contains expected output

---

## 🎯 **Project Names Reference**

### **Wave 1: Foundation Infrastructure**
```bash
granger_hub              # Central orchestration hub
arangodb                 # Knowledge storage and graph operations
claude-test-reporter     # Quality assurance and test reporting
runpod_ops               # GPU instance management and Docker deployment
```

### **Wave 2: Core Intelligence**
```bash
rl_commons              # Reinforcement learning components
world_model             # Self-understanding and autonomous learning
```

### **Wave 3: Document Processing Pipeline**
```bash
marker                  # Document extraction and processing
sparta                  # Data ingestion and enrichment
ppt                     # PowerPoint automation and generation
```

### **Wave 4: AI Services & APIs**
```bash
llm_call                # Universal LLM interface
fine_tuning             # Model training pipeline
```

### **Wave 5: Data Collection & Research**
```bash
arxiv-mcp-server        # Research paper automation
youtube_transcripts     # Video transcript analysis
gitget                  # Repository analysis and extraction
```

### **Wave 6: Specialized Processing**
```bash
darpa_crawl             # Funding opportunity monitoring
mcp-screenshot          # Screenshot and visual analysis
```

### **Wave 7: User Interfaces**
```bash
granger-ui              # Design system and components
annotator               # Human annotation interface
chat                    # Conversational interface
aider-daemon            # Terminal interface and automation
claude_bot              # Telegram bot for mobile Granger control
```

---

## 🛠️ **Project Capability Commands**

**Purpose**: Direct access to Granger project capabilities without navigating directories

### **LLM Interface: /llm-ask**
```bash
/llm-ask "What is quantum computing?" --model gpt-4
/llm-ask "Explain this code" --system "You are a Python expert"
/llm-ask "Generate unit tests" --validate code_review --json
```

### **Research Papers: /arxiv-search**
```bash
/arxiv-search "transformer architecture" --limit 10
/arxiv-search "quantum computing" --category quant-ph --analyze
/arxiv-search "LLMs improve with scale" --evidence supporting
```

### **Knowledge Base: /arangodb-search**
```bash
/arangodb-search "machine learning" --type semantic
/arangodb-search "security" --type hybrid --expand
/arangodb-search "granger" --type graph --depth 3 --visualize
```

### **Document Processing: /marker-extract**
```bash
/marker-extract document.pdf --output markdown
/marker-extract presentation.pptx --extract tables
/marker-extract --batch /path/to/docs/ --enhance
```

### **PowerPoint Automation: /ppt Commands**
```bash
# Create presentations
/ppt-create "Q1 Report" --template modern --slides 10
/ppt-create --from-doc report.md --charts --tables

# Update presentations  
/ppt-update presentation.pptx --find "2023" --replace "2024"
/ppt-update deck.pptx --add-slide --title "New Findings" --content findings.md

# Monitor and auto-update
/ppt-monitor --config ppt_monitor.json
/ppt-monitor --presentation report.pptx --collections papers,metrics --interval 300
```

### **Video Transcripts: /yt-search**
```bash
/yt-search "python tutorial" --limit 5
/yt-search "LLM training" --channel "Yannic Kilcher" --analyze
/yt-search "machine learning" --duration long --export markdown
```

### **DARPA Opportunities: /darpa-search**
```bash
/darpa-search "AI" --office I2O --analyze
/darpa-search --status open --monitor
/darpa-search "quantum" --proposal
```

### **Test Reporting: /test-report**
```bash
/test-report arangodb --format html
/test-report --dashboard --compare "claude,gemini"
/test-report marker --flaky --trends
```

### **Telegram Bot Control: /claude-bot Commands**

#### **/claude-bot-status**
```bash
# Check claude_bot Telegram bot status
/claude-bot-status
/claude-bot-status --detailed
/claude-bot-status --check-hub
```

#### **/claude-bot-send**
```bash
# Send messages via Telegram bot
/claude-bot-send "System maintenance at 2 PM"
/claude-bot-send --user 7957197311 "Personal reminder"
/claude-bot-send --broadcast "Ecosystem update complete"
```

#### **/claude-bot-execute**
```bash
# Execute commands through Telegram bot
/claude-bot-execute "/granger status"
/claude-bot-execute "/arxiv-search 'quantum computing' --limit 5"
/claude-bot-execute --async "/granger-verify --all"
```

### **Repository Analysis: GitGet Commands**

#### **/gitget-analyze**
```bash
# Analyze a repository with LLM documentation
/gitget-analyze https://github.com/psf/requests --output markdown
/gitget-analyze https://github.com/django/django --extensions py --max-tokens 50000
/gitget-analyze https://github.com/facebook/react --summary
```

#### **/gitget-clone**  
```bash
# Sparse clone repositories efficiently
/gitget-clone https://github.com/torvalds/linux --extensions c,h
/gitget-clone https://github.com/tensorflow/tensorflow --directories tensorflow/python
/gitget-clone https://github.com/kubernetes/kubernetes --depth 1
```

#### **/gitget-search**
```bash
# Search for patterns in repository code
/gitget-search https://github.com/psf/requests "try.*except" --extensions py
/gitget-search https://github.com/facebook/react "TODO|FIXME" --context 5
/gitget-search https://github.com/django/django "def.*authenticate" --json
```

#### **/gitget-mcp**
```bash
# Start GitGet MCP server for AI integration
/gitget-mcp
/gitget-mcp --cache-dir /tmp/gitget-cache
/gitget-mcp --port 8080 --max-cache-size 20
```

#### **/gitget-languages**
```bash
# List supported programming languages (100+)
/gitget-languages
/gitget-languages --format json
/gitget-languages --filter python
/gitget-languages --extensions js,ts
```

### **GPU Infrastructure: RunPod Commands**

#### **/runpod create**
```bash
# Create instance with automatic GPU optimization
/runpod create 70B --hours 4
/runpod create 13B --tokens 10000000 --spot
/runpod create 7B --gpu RTX_4090 --hours 8
```

#### **/runpod deploy**
```bash
# Deploy Docker images with dynamic model loading
/runpod deploy grahamco/runpod-sglang-base --model meta-llama/Llama-2-70b-hf
/runpod deploy grahamco/runpod-sglang-finetune --mode finetune --model meta-llama/Llama-2-13b-hf
/runpod deploy grahamco/runpod-sglang-base --mode shell --volume 200
```

#### **/runpod optimize**
```bash
# Find optimal GPU configuration (lowest total cost)
/runpod optimize 70B --tokens 10000000
/runpod optimize 13B --tokens 5000000 --max-budget 50
/runpod optimize 30B --multi-gpu --hours 48
/runpod optimize 7B --inference --tokens 1000000
```

#### **/runpod list**
```bash
# List RunPod instances
/runpod list
/runpod list --active
/runpod list --format json
```

#### **/runpod monitor**
```bash
# Monitor running instances
/runpod monitor abc123
/runpod monitor abc123 --interval 10
```

#### **/runpod terminate**
```bash
# Terminate instances
/runpod terminate abc123
/runpod terminate abc123 --force
```

---

## 📊 **Feature Synchronization: /granger-feature-sync**

**Purpose**: Compare documented features (README) vs actual implemented features, create task lists, and optionally implement missing features

### **Basic Usage**
```bash
# Analyze projects and create task lists
/granger-feature-sync

# Analyze AND automatically implement missing features
/granger-feature-sync --implement
```

### **Key Features**
- **Skeleton Detection**: Identifies projects with < 30% real implementation
- **Feature Analysis**: Compares README promises vs actual code
- **Task Generation**: Creates numbered task lists following TASK_LIST_TEMPLATE_GUIDE_V2
- **External Verification**: Generates prompts for Perplexity/Gemini verification
- **Documentation Updates**: Updates READMEs and central docs
- **Implementation Directive**: ALWAYS shows next steps when issues found

### **Implementation Directive**
When skeleton projects or missing features are detected:
1. Shows prioritized list of skeleton projects with implementation ratios
2. Provides clear implementation instructions
3. With `--implement`: Automatically generates working code
4. Without flag: Shows agent directive to begin implementation NOW

### **Output Files**
- Task lists: `{project}/docs/tasks/{number}_Tasks_List.md`
- Verification requests: `{project}/verification_request.md`
- Report: `/home/graham/workspace/shared_claude_docs/reports/feature_sync/`
- Updated docs in `docs/01_strategy/whitepaper/` and `docs/06_operations/current_state/`

---

## 🤖 **Multi-AI Collaboration: /granger-ai-collab**

**Purpose**: Orchestrate iterative AI collaboration to resolve persistent issues

### **Key Features**
- **Claude Code** attempts initial fixes
- **Google Gemini Code 2.0** provides up to 5 rounds of consultation
- **Adaptive Temperature**: Increases creativity with each round (0.3 → 0.8)
- **Agent Comparison**: Uses claude-test-reporter to track resolution progress
- **Human Guidance**: Only generated after all AI attempts exhausted

### **Usage**
```bash
# No parameters needed - fully automated workflow
/granger-ai-collab
```

### **Workflow Stages**
1. **Initial Assessment**: Identifies all issues across ecosystem
2. **Claude Force-Fix**: Generates and applies fix directives
3. **Iterative Gemini Collaboration**: Up to 5 rounds of consultation
4. **Final Report**: Human guidance only if issues remain

### **Generated Outputs**
- Initial verification: `initial_TIMESTAMP/`
- Claude fix directives: `claude_fix_TIMESTAMP/`
- Gemini fix directives: `GEMINI_FIX_R{1-5}_*.md`
- Agent comparison reports: `ai_collaboration_round_*.html`
- Resolution dashboard: `ai_collaboration_dashboard_*.html`
- Final report: `final_resolution_report_*.md`

### **Example Session**
```bash
🤖 Granger Multi-AI Collaboration Workflow v2
Claude Code → Gemini (iterative, max 5 rounds) → Human (if needed)

Step 1: Running initial verification to identify issues...
Step 2: Generating Claude force-fix directives...
Step 3: Starting multi-AI collaboration with Gemini (up to 5 rounds)...

🔄 Starting Gemini collaboration round 1/5
⏳ Round 1: Gemini fix directives generated for 3 projects.
Press Enter when ready to verify fixes...

🔄 Starting Gemini collaboration round 2/5
✅ All issues resolved in round 2!

Collaboration Statistics:
  • Total AI rounds: 2
  • Gemini consultations: 2
```

---

## 🔄 **Daily Workflow Examples**

### **Developer Workflow**
```bash
# Morning: Quick single project check
/granger-verify --project granger_hub --quick

# During development: Test verification only
/granger-verify --project granger_hub --tests-only --verbose

# Before commit: Full project verification
/granger-verify --project granger_hub

# End of day: Full ecosystem verification
/granger-verify --all

# When persistent issues arise: Multi-AI collaboration
/granger-ai-collab
```

### **Automated Cron Jobs**
```bash
# Add to crontab for 2 AM daily verification
0 2 * * * /granger-verify --all --cron --force-fix

# Quick critical projects check every 6 hours
0 */6 * * * /granger-verify --category "Communication Hub" --cron

# Single critical project monitoring
0 */2 * * * /granger-verify --project granger_hub --cron --quick
```

### **CI/CD Integration**
```bash
# Pre-deployment verification
/granger-verify --project $PROJECT --ci --tests-only

# Post-deployment health check
/granger-verify --project $PROJECT --quick

# Full regression after major changes
/granger-verify --all --no-auto-fix
```

---

## 📊 **Report Outputs**

### **Verification Report Structure**
```
granger_verification_reports/
├── summary/
│   ├── verification_summary.json          # Overall statistics
│   ├── dashboard.html                     # Visual dashboard
│   └── fix_directives/                    # Fix instructions for Claude
│       ├── FIX_REQUIRED_arangodb.md
│       ├── FIX_REQUIRED_marker.md
│       └── ECOSYSTEM_FIX_REQUIRED.md
├── projects/
│   └── [project_name]/
│       └── verification_report.json       # Detailed project results
└── logs/
    └── verification_*.log                 # Execution logs
```

### **Fix Directive System**

When using `--force-fix`, the system generates explicit instructions for Claude:

```markdown
# 🔧 AGENT FIX DIRECTIVE - IMMEDIATE ACTION REQUIRED

**Project**: arangodb
**Issues Found**: 5
**Priority**: CRITICAL

## ISSUES TO FIX

### Issue #1: Mock Usage Detected
**Files**: tests/test_api.py, tests/test_db.py
**Required Actions**:
1. Remove all @mock decorators
2. Replace with real service connections
3. Ensure minimum duration thresholds

## EXECUTION INSTRUCTIONS
1. Navigate to project
2. Apply fixes as detailed
3. Run tests to verify

**START FIXING NOW** - Do not wait for further instructions.
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Command Not Found**
```bash
# Ensure commands are executable
chmod +x /home/graham/.claude/commands/*

# Check if command exists
ls -la /home/graham/.claude/commands/granger-verify
```

#### **Project Not Found**
```bash
# For /verify-project, try full path
/verify-project /home/graham/workspace/experiments/granger_hub/

# Check available projects
ls /home/graham/workspace/experiments/
ls /home/graham/workspace/mcp-servers/
```

#### **Permission Issues**
```bash
# Fix permissions on workspace
sudo chown -R graham:graham /home/graham/workspace/

# Fix command permissions
chmod +x /home/graham/.claude/commands/*
```

#### **Service Dependencies**
```bash
# Check ArangoDB
curl -s http://localhost:8529/_api/version

# Check Redis
redis-cli ping

# Check PostgreSQL
pg_isready -h localhost
```

### **Debug Mode**
```bash
# Verbose output for debugging
/verify-project granger_hub --verbose

# Disable auto-fixing to see raw issues
/granger-verify --project marker

# Check logs
tail -f granger_daily_reports/latest/daily_verification.log
```

---

## 🎯 **Quick Reference Card**

```bash
# ESSENTIAL VERIFICATION COMMANDS
/granger-verify --fix --auto               # Remove ALL mocks & simulations
/granger-verify --project granger_hub      # Single project
/granger-verify --all                      # Full ecosystem
/granger-verify --category "spokes"        # By category
/granger-verify --project X --force-fix    # Force fixes

# AI COLLABORATION
/granger-ai-collab                         # Multi-AI resolution (up to 5 rounds)

# PROJECT CAPABILITIES
/llm-ask "question" --model gpt-4          # Query any LLM
/arxiv-search "query" --limit 10           # Search research papers
/arangodb-search "query" --type semantic   # Search knowledge base
/marker-extract file.pdf --output markdown # Extract from documents
/yt-search "query" --channel "name"        # Search YouTube transcripts
/darpa-search "AI" --status open           # Find DARPA opportunities
/test-report --dashboard                   # Generate test reports

# DEVELOPMENT COMMANDS  
/granger-verify --project X --tests-only   # Test verification only
/granger-verify --project X --quick        # Fast check
/cleanup                                   # Clean current project
/audit                                     # Audit current project

# TELEGRAM BOT COMMANDS
/claude-bot-status                         # Check bot status
/claude-bot-send "message"                 # Send via Telegram
/claude-bot-execute "/command"             # Execute slash command

# GITGET COMMANDS
/gitget-analyze <url> --output markdown    # Analyze repository
/gitget-clone <url> --extensions py,js     # Sparse clone  
/gitget-search <url> <pattern>             # Search code
/gitget-mcp                                # Start MCP server
/gitget-languages --filter <lang>          # List languages

# AUTOMATION COMMANDS
/granger-verify --all --cron --force-fix   # Nightly cron
/granger-verify --project X --ci           # CI/CD mode
/granger-verify --all --parallel 8         # Parallel execution

# MANAGEMENT COMMANDS
/cleanup-all                               # Clean all projects
/audit-all                                 # Audit all projects
/ecosystem-report                          # Health report
```

---

## 📚 **Related Documentation**

- **CLAUDE.md Standards**: `/home/graham/.claude/CLAUDE.md`
- **Task List Template**: `TASK_LIST_TEMPLATE_GUIDE_V2.md`
- **Test Verification**: `TEST_VERIFICATION_TEMPLATE_GUIDE.md`
- **Granger Projects**: `GRANGER_PROJECTS.md`
- **Command Details**: `/home/graham/.claude/commands/granger-verify-README.md`

---

## ⚠️ **Deprecated Commands**

The following commands have been consolidated into `/granger-verify`:

| Old Command | New Equivalent |
|-------------|----------------|
| `/test-verify-all` | `/granger-verify --project PROJECT --tests-only` |
| `/test-all-projects` | `/granger-verify --all --tests-only` |
| `/granger-daily-verify` | `/granger-verify --project PROJECT` |
| `/granger-verify-fix` | `/granger-verify --project PROJECT --force-fix` |
| `/verify-project` | `/granger-verify --project PROJECT --quick` |
| `/grangerverify` | `/granger-verify` |

**Note**: Deprecated commands have been moved to `~/.claude/commands/deprecated/` and will be removed on 2025-02-01.

---

## 🔄 **Updates & Maintenance**

This guide is maintained alongside the slash commands. For the latest information:

1. **Check command help**: `/granger-verify --help`
2. **Review command configs**: `/home/graham/.claude/commands/*.json`
3. **Monitor reports**: `granger_verification_reports/`
4. **Update this guide** when commands change

**Last Updated**: January 2025  
**Version**: 2.1.0  
**Maintainer**: Claude Assistant System

### **Recent Updates**
- Added GitGet slash commands for repository analysis and code search
- GitGet now supports 100+ programming languages via tree-sitter parsers
- Integrated with MCP protocol for AI assistant integration
- Respects .gitingest configuration files for project-specific settings
