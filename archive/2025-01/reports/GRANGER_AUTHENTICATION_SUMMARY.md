# GRANGER ECOSYSTEM AUTHENTICATION ISSUES SUMMARY

## Current Status

The `uv sync` command is failing due to GitHub authentication issues with several Granger ecosystem repositories. While GitHub CLI is installed and authenticated, some repositories are still failing to authenticate.

## Affected Repositories

Based on the errors, these repositories are having authentication issues:
- `rl-commons @ git+https://github.com/grahama1970/rl-commons.git`
- `sparta @ git+https://github.com/grahama1970/sparta.git`
- `granger_hub @ git+https://github.com/grahama1970/granger_hub.git`
- `arangodb @ git+https://github.com/grahama1970/arangodb.git` (has unpushed pyproject.toml fix)

## Issues Found and Fixed

1. **arangodb**: Had malformed `pyproject.toml` with stray quotes after section headers
   - Status: Fixed locally but cannot push due to authentication
   
2. **annotator**: Package name mismatch
   - Status: Fixed - changed to `active-annotator` in pyproject.toml

## Recommended Actions

### Option 1: Fix Authentication (Recommended)
```bash
# Ensure gh is properly configured
gh auth refresh --hostname github.com

# Or use SSH for all repos
git config --global url."git@github.com:".insteadOf "https://github.com/"

# Or set up a personal access token
export GITHUB_TOKEN=your_token_here
git config --global url."https://${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"
```

### Option 2: Temporary Workaround
Comment out the problematic dependencies temporarily:
```bash
# In pyproject.toml, comment out:
# "rl_commons @ git+https://github.com/grahama1970/rl-commons.git",
# "sparta @ git+https://github.com/grahama1970/sparta.git",
# "granger_hub @ git+https://github.com/grahama1970/granger_hub.git",
# "arangodb @ git+https://github.com/grahama1970/arangodb.git",
```

Then run:
```bash
uv sync
uv pip install -e .
```

### Option 3: Clone and Install Locally
Clone the problematic repos locally and install them:
```bash
cd /home/graham/workspace/experiments
git clone https://github.com/grahama1970/rl-commons.git
git clone https://github.com/grahama1970/sparta.git
# etc...

cd /home/graham/workspace/shared_claude_docs
# Update pyproject.toml to use local paths:
# "rl_commons @ file:///home/graham/workspace/experiments/rl_commons",
```

## Next Steps

1. Fix GitHub authentication using one of the methods above
2. Push the arangodb pyproject.toml fix
3. Run `uv sync` successfully
4. Install shared_claude_docs in editable mode

## Critical Note

The arangodb repository has a critical fix that needs to be pushed to GitHub. Without this fix, no project that depends on arangodb can be installed via uv/pip.