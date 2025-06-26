# Granger Ecosystem Dependency Conflicts Summary

## Current Status

The shared_claude_docs project cannot complete `uv sync` due to cascading dependency conflicts between various Granger ecosystem packages.

## Key Conflicts Found

### 1. NumPy Version Conflicts
- **arangodb**: requires `numpy>=2.2.2`
- **marker**: requires `numpy>=1.24.0,<2`
- **aider-chat**: requires `numpy==1.26.4`

These are fundamentally incompatible.

### 2. Package Name Mismatches
- **annotator**: Package declares itself as `active-annotator` (fixed)
- **aider-daemon**: Package declares itself as `aider-chat` (fixed)
- **rl_commons**: Should be consistent naming (pending your fix)

### 3. Repository Issues
- **fine_tuning**: Has broken submodule reference
- **arangodb**: Has unpushed pyproject.toml fix (stray quotes)

### 4. Surya-OCR Version Conflicts
- **granger-hub**: requires `surya-ocr>=0.14.5,<0.15.0`
- **marker**: requires `surya-ocr>=0.13.1,<0.14.dev0`

### 5. Other Version Conflicts
- **aiohttp**: aider-chat requires 3.11.18, we had >=3.12.6 (relaxed to fix)

## Recommended Solutions

### Option 1: Update Dependencies (Best Long-term Solution)
1. Update `marker` to support numpy 2.x and newer surya-ocr
2. Update `granger-hub` to be compatible with marker's surya-ocr version
3. Update `aider-chat` to support newer numpy versions
4. Fix `fine_tuning` submodule issue

### Option 2: Create Compatibility Layer
Create separate virtual environments for incompatible packages and use them via subprocess calls or APIs rather than direct imports.

### Option 3: Selective Installation (Quick Workaround)
Install only compatible subsets of the ecosystem:

```bash
# Group 1: Modern numpy (2.x)
# Comment out: marker, aider-chat

# Group 2: Legacy numpy (<2)  
# Comment out: arangodb
```

### Option 4: Use Docker Containers
Package each incompatible service in its own container with its required dependencies.

## Current Workaround

Currently commented out:
- `arangodb` (numpy 2.x requirement)
- `fine_tuning` (broken submodule)
- `aider-chat` (numpy version conflict)

## Action Items

1. **Immediate**: Set up GitHub authentication to push arangodb fix
2. **Short-term**: Fix package naming consistency (rl_commons)
3. **Medium-term**: Update packages to use compatible dependency versions
4. **Long-term**: Consider using dependency version ranges instead of strict pins

## Testing Approach

Once dependencies are resolved:
```bash
cd /home/graham/workspace/shared_claude_docs
uv sync
uv pip install -e .
python -c "import shared_claude_docs; print('Success!')"
```