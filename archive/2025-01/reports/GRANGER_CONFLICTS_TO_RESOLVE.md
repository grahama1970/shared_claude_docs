# Granger Ecosystem Conflicts to Resolve

## Current Blockers

### 1. NumPy Version Conflict
- **arangodb**: requires `numpy>=2.2.2`
- **marker**: requires `numpy>=1.24.0,<2`
- **Solution**: Update arangodb to support numpy<2 or update marker to support numpy>=2

### 2. Surya-OCR Version Conflict
- **granger-hub**: requires `surya-ocr>=0.14.5,<0.15.0`
- **marker**: requires `surya-ocr>=0.13.1,<0.14.dev0`
- **Solution**: Update marker to use surya-ocr 0.14.x or update granger-hub to be flexible

### 3. Broken Submodule
- **fine_tuning**: Has broken submodule reference `repos/runpod_llm_ops`
- **Solution**: Remove the submodule reference from .gitmodules

## Packages Currently Disabled

1. **arangodb** - numpy conflict
2. **fine_tuning** - broken submodule
3. **aider-chat** - not needed (UI package)
4. **active-annotator** - not needed (UI package)

## Action Plan

### Immediate (to get most things working):
1. Keep arangodb commented out until numpy issue is resolved
2. Keep fine_tuning commented out until submodule is fixed
3. Choose between granger-hub and marker (can't have both currently)

### Short-term fixes needed:
1. Fork arangodb and change numpy requirement to `<2`
2. Fork marker and update surya-ocr to `>=0.14.5,<0.15.0`
3. Fix fine_tuning submodule issue

### Long-term:
1. Coordinate version requirements across all Granger projects
2. Use version ranges instead of strict pins where possible
3. Set up CI/CD to catch these conflicts early

## Current Working Set

With the following commented out, the rest should work:
- arangodb (numpy conflict)
- fine_tuning (submodule issue)
- Either marker OR granger-hub (surya-ocr conflict)

## Commands to Test

```bash
# Clear cache and sync
uv cache clean
uv sync

# Test imports
python -c "import sparta, youtube_transcripts, claude_test_reporter"
python -c "import rl_commons, arxiv_mcp_server, mcp_screenshot"
```