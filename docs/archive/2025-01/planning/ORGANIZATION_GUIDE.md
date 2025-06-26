# 🗂️ Project Organization Guide

This guide explains the reorganized structure of shared_claude_docs for maximum clarity.

## 📍 Where to Find What

### Testing Code → `/testing/`
All test-related code is now organized by purpose:
```
testing/
├── interaction_tests/     # How modules work together
├── visualization_tests/   # Smart visualization selection
├── self_evolution/        # Autonomous improvement
└── integration_tests/     # Real API integration
```

### Analysis Tools → `/analysis/`
Tools for analyzing and improving projects:
```
analysis/
├── project_analysis/      # Analyze codebases
└── research_tools/        # Find improvements via research
```

### Documentation → `/docs/`
All documentation organized by type:
```
docs/
├── big_picture/          # Interaction levels & patterns
├── architecture/         # System design
├── tutorials/           # How-to guides
└── api/                 # API documentation
```

### Utilities → `/utils/`
General utilities and helpers:
```
utils/
├── cleanup_utility/      # Project maintenance
├── claude_interactions/  # Interaction scenarios
└── [other tools]        # Various helpers
```

## 🎯 Quick Navigation

### "I want to test module interactions"
→ Go to `/testing/interaction_tests/`
```bash
cd testing/interaction_tests
python3 interaction_test_framework.py
```

### "I want to test visualization decisions"
→ Go to `/testing/visualization_tests/`
```bash
cd testing/visualization_tests
python3 visualization_decision_tests.py
```

### "I want to see self-evolution in action"
→ Go to `/testing/self_evolution/`
```bash
cd testing/self_evolution
python3 demo_self_evolution.py
```

### "I want to analyze a project"
→ Go to `/analysis/project_analysis/`
```bash
cd analysis/project_analysis
python3 enhanced_big_picture_analyzer.py
```

### "I want to find research-based improvements"
→ Go to `/analysis/research_tools/`
```bash
cd analysis/research_tools
python3 research_driven_improvements.py
```

### "I want to understand interaction levels"
→ Read `/docs/big_picture/MODULE_INTERACTION_LEVELS.md`

## 🏗️ Design Principles

1. **Clear Separation**: Each directory has a single, clear purpose
2. **Easy Discovery**: Descriptive names make finding code intuitive
3. **Flat Hierarchy**: Avoid deep nesting for easy navigation
4. **Self-Documenting**: Each directory has its own README

## 📝 Key Files Moved

### From `/utils/` to `/testing/interaction_tests/`:
- `interaction_test_framework.py`
- `interaction_runner.py`
- `stress_test_interactions.py`

### From `/utils/` to `/testing/visualization_tests/`:
- `visualization_decision_tests.py`
- `arangodb_visualization_interactions.py`

### From `/utils/` to `/testing/self_evolution/`:
- `self_evolving_analyzer.py`
- `demo_self_evolution.py`

### From `/utils/` to `/analysis/`:
- `research_driven_improvements.py` → `/analysis/research_tools/`
- `big_picture_analyzer.py` → `/analysis/project_analysis/`
- `enhanced_big_picture_analyzer.py` → `/analysis/project_analysis/`

## 🚦 Development Workflow

1. **Develop** in appropriate `/testing/` subdirectory
2. **Document** in `/docs/`
3. **Analyze** using `/analysis/` tools
4. **Deploy** to production (granger_hub)

## ✅ Benefits of New Structure

- **Findability**: Easy to locate specific functionality
- **Maintainability**: Clear boundaries between concerns
- **Scalability**: Easy to add new test types or tools
- **Onboarding**: New developers/agents understand quickly
- **Modularity**: Each piece can evolve independently

---

*This organization makes the project structure clear and intuitive for both humans and AI agents.*