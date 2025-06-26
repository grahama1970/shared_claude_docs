# Granger Ecosystem Compliance Assessment (CORRECTED)

## Important Correction

The original assessment incorrectly identified the use of `hatchling` as a compliance violation. This was wrong. The Granger ecosystem successfully uses **BOTH** `hatchling` and `setuptools` as build backends, and both work perfectly with git+https:// dependencies.

## Actual Compliance Requirements

Based on the corrected understanding of GRANGER_MODULE_STANDARDS.md:

### ✅ Build System
- **Either `hatchling` OR `setuptools` are acceptable**
- For hatchling projects, ensure `[tool.hatch.metadata] allow-direct-references = true`
- Both systems work with git+https:// dependencies

### 🔒 Locked Dependencies (CRITICAL)
These are the actual compliance requirements:
```toml
requires-python = ">=3.10.11"
dependencies = [
    "numpy==1.26.4",          # LOCKED - Do not change
    "pandas>=2.2.3,<2.3.0",   # Compatible with numpy 1.26.4
    "pyarrow>=4.0.0,<20",     # Required for mlflow compatibility
    "pillow>=10.1.0,<11.0.0", # Security constraints
]
```

### 📦 Git Dependencies
- Must use format: `"package @ git+https://github.com/user/repo.git"`
- No local file:// paths
- No missing git+ prefix

### 🚫 NO MOCKS Policy
- No mock imports or usage in tests
- Use real services only

### 📁 Project Structure
- Use 3-layer architecture: core/cli/mcp
- .env.example must start with `PYTHONPATH=./src`
- UV for package management (documentation)

## Revised Compliance Assessment

### Projects Likely Compliant (using hatchling correctly):
- claude-test-reporter
- llm_call
- arxiv-mcp-server
- annotator
- aider-daemon
- darpa_crawl
- chat

### Projects Needing Review:
1. **Dependency versions** - Check numpy, pandas, pyarrow versions
2. **Python version** - Ensure >=3.10.11
3. **Git dependency format** - Add git+ prefix where missing
4. **MCP integration** - Most projects lack this
5. **Module headers** - Documentation standards

### Actually Modified (incorrectly):
- **granger_hub** - Was changed from hatchling to setuptools unnecessarily

## Recommended Actions

1. **Revert granger_hub changes** - It was fine with hatchling
2. **Focus on actual issues:**
   - Dependency version constraints
   - Git URL formats
   - MCP integration
   - NO MOCKS policy
   - Module documentation headers

3. **Leave build systems alone** - Both hatchling and setuptools are valid

## Key Insight

The diversity of build backends (hatchling, setuptools, even pdm) in the Granger ecosystem is not a bug - it's a feature. The ecosystem is designed to be flexible and integrate different tools as long as they follow the core standards for dependencies and structure.