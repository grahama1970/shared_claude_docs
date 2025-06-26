# NumPy Compatibility Plan for Granger Ecosystem

## Current Situation

- **marker**: requires `numpy>=1.24.0,<2`
- **arangodb**: requires `numpy>=2.2.2`
- **aider-chat**: pins `numpy==1.26.4`

## Recommended Solution

### Option 1: Downgrade arangodb numpy requirement (Recommended)

1. Change arangodb's pyproject.toml:
   ```toml
   # From:
   "numpy>=2.2.2"
   # To:
   "numpy>=1.24.0,<2"
   ```

2. Test arangodb with numpy 1.26.4 to ensure compatibility

3. If arangodb uses numpy 2.x specific features, update the code to be compatible with numpy 1.x

### Option 2: Update marker to support numpy 2.x

This would require updating marker's dependencies and testing with numpy 2.x.

### Option 3: Use dependency groups

Create separate dependency groups that don't conflict:
- Group A: Projects compatible with numpy 1.x (marker, aider-chat)
- Group B: Projects requiring numpy 2.x (arangodb)

## Immediate Action

For now, to get everything working, I recommend Option 1:

1. Fork arangodb
2. Change numpy requirement to `"numpy>=1.24.0,<2"`
3. Test functionality
4. Push changes

## Testing Command

After making changes:
```bash
cd /home/graham/workspace/shared_claude_docs
uv sync
python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
python -c "import marker, arangodb; print('All imports successful!')"
```