# Shared Claude Docs - Project Structure

This document explains the organization of the shared_claude_docs project for clear understanding by humans and agents.

## 📁 Directory Structure

```
shared_claude_docs/
│
├── docs/                      # Documentation
│   ├── api/                   # API documentation
│   ├── architecture/          # System architecture docs
│   ├── big_picture/           # Project overviews and interaction levels
│   └── tutorials/             # How-to guides
│
├── testing/                   # All testing-related code
│   ├── interaction_tests/     # Module interaction testing (Levels 0-3)
│   ├── visualization_tests/   # Visualization decision testing
│   ├── self_evolution/        # Self-evolving system tests
│   └── integration_tests/     # Full integration tests
│
├── analysis/                  # Analysis and research tools
│   ├── project_analysis/      # Project analysis utilities
│   └── research_tools/        # Research-driven improvement tools
│
├── guides/                    # Developer and setup guides
│   ├── conventions/           # Coding conventions
│   ├── setup/                 # Setup instructions
│   └── workflows/             # Workflow documentation
│
├── utils/                     # General utilities
│   ├── cleanup_utility/       # Project cleanup tools
│   ├── claude_interactions/   # Claude interaction scenarios
│   └── [other utilities]      # Various helper scripts
│
├── src/                       # Source code (Python package)
│   └── shared_claude_docs/    # Main package
│
├── templates/                 # Document templates
├── references/                # External references
└── scripts/                   # Automation scripts
```

## 🧪 Testing Organization

### `/testing/interaction_tests/`
**Purpose**: Test module interactions at different complexity levels

- `interaction_test_framework.py` - Comprehensive test suite for Levels 0-3
- `interaction_runner.py` - Interactive runner for debugging specific patterns
- `stress_test_interactions.py` - Stress testing for interaction robustness

**Usage**:
```bash
cd testing/interaction_tests
python3 interaction_test_framework.py  # Run all tests
python3 interaction_runner.py interactive  # Interactive mode
```

### `/testing/visualization_tests/`
**Purpose**: Test intelligent visualization decisions

- `visualization_decision_tests.py` - Tests for appropriate viz selection
- `arangodb_visualization_interactions.py` - Database + viz integration tests

**Usage**:
```bash
cd testing/visualization_tests
python3 visualization_decision_tests.py
```

### `/testing/self_evolution/`
**Purpose**: Test autonomous improvement capabilities

- `self_evolving_analyzer.py` - Main self-evolution system
- `demo_self_evolution.py` - Demonstration script

**Usage**:
```bash
cd testing/self_evolution
python3 self_evolving_analyzer.py marker --iterations 3
```

### `/testing/integration_tests/`
**Purpose**: Full system integration tests

- `test_real_integration.py` - Tests with real arxiv/youtube APIs

**Usage**:
```bash
cd testing/integration_tests
python3 test_real_integration.py
```

## 📊 Analysis Tools

### `/analysis/research_tools/`
**Purpose**: Research and analyze improvements

- `research_driven_improvements.py` - Find research-backed improvements

**Usage**:
```bash
cd analysis/research_tools
python3 research_driven_improvements.py
```

### `/analysis/project_analysis/`
**Purpose**: Analyze project codebases

- `big_picture_analyzer.py` - Generate project descriptions
- `enhanced_big_picture_analyzer.py` - Enhanced analysis with metrics

## 📚 Documentation

### `/docs/big_picture/`
Contains the key interaction documentation:
- `MODULE_INTERACTION_LEVELS.md` - Detailed level definitions
- `INTERACTION_EXAMPLES_VISUAL.md` - Visual examples
- `INTERACTION_PATTERNS_ANALYSIS.md` - Pattern analysis
- `INTERACTION_TESTING_GUIDE.md` - Testing guide

## 🎯 Key Concepts

### Interaction Levels
- **Level 0**: Direct module calls (single module)
- **Level 1**: Sequential pipelines (A → B → C)
- **Level 2**: Parallel & branching (multiple paths)
- **Level 3**: Orchestrated collaboration (feedback loops)

### Testing Philosophy
1. **Start Simple**: Test Level 0 first
2. **Clear Data Flow**: Show how data moves
3. **Human Readable**: Both output and code
4. **Modular**: Each test is independent

## 🚀 Quick Start

### Run All Interaction Tests
```bash
cd testing/interaction_tests
python3 interaction_test_framework.py
```

### Test Visualization Decisions
```bash
cd testing/visualization_tests
python3 visualization_decision_tests.py
```

### Try Self-Evolution
```bash
cd testing/self_evolution
python3 demo_self_evolution.py
```

## 🔧 Development Workflow

1. **Develop** interaction patterns in `testing/interaction_tests/`
2. **Test** thoroughly at each level
3. **Document** in `docs/big_picture/`
4. **Integrate** proven patterns into `granger_hub`

## 📝 Adding New Tests

### 1. Choose the Right Directory
- Module interactions → `testing/interaction_tests/`
- Visualization logic → `testing/visualization_tests/`
- Self-improvement → `testing/self_evolution/`

### 2. Follow Naming Conventions
- Test files: `test_*.py` or `*_tests.py`
- Framework files: `*_framework.py`
- Runner files: `*_runner.py`

### 3. Document Your Tests
- Add docstrings
- Update relevant guides
- Include usage examples

## 🏗️ Architecture Notes

- **shared_claude_docs**: Documentation, testing, and analysis hub
- **granger_hub**: Production orchestration (separate repo)
- **Individual modules**: arxiv-mcp-server, youtube_transcripts, etc. (separate repos)

This separation ensures:
- Clear development/production boundary
- Easy testing and iteration
- Clean integration path

---

*This structure provides clear separation of concerns and makes it easy for both humans and agents to understand and navigate the project.*