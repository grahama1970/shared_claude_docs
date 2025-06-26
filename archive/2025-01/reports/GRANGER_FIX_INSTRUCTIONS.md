# GRANGER ECOSYSTEM FIX INSTRUCTIONS

## Issue Summary
The `arangodb` repository on GitHub has a malformed `pyproject.toml` file with stray quotes after section headers like `[project.scripts]"`. This is preventing `uv sync` from working in `shared_claude_docs` and potentially other Granger projects.

## Immediate Actions Required

### 1. Set Up GitHub Authentication
Choose ONE of these options:

#### Option A: GitHub CLI (Recommended)
```bash
gh auth login
# Follow the prompts to authenticate
```

#### Option B: SSH Key
```bash
# Generate SSH key if you don't have one
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: https://github.com/settings/keys
cat ~/.ssh/id_ed25519.pub

# Update all Granger repos to use SSH
cd /home/graham/workspace/experiments/arangodb
git remote set-url origin git@github.com:grahama1970/arangodb.git
```

#### Option C: Personal Access Token
1. Create token at: https://github.com/settings/tokens
2. Select scopes: `repo` (full control)
3. Save the token securely

### 2. Fix and Push arangodb
After authentication is set up:

```bash
# Clone fresh copy
cd /tmp
git clone https://github.com/grahama1970/arangodb.git
cd arangodb

# Apply the fix
sed -i 's/\[project\.scripts\]"/[project.scripts]/' pyproject.toml
sed -i 's/\[project\.optional-dependencies\]"/[project.optional-dependencies]/' pyproject.toml
sed -i 's/\[build-system\]"/[build-system]/' pyproject.toml
sed -i 's/\[tool\.\([^]]*\)\]"/[tool.\1]/' pyproject.toml

# Verify the fix
python3 -c "import toml; toml.load(open('pyproject.toml'))"

# Commit and push
git add pyproject.toml
git commit -m "fix: remove stray quotes from pyproject.toml section headers"
git push origin main
```

### 3. Complete shared_claude_docs Setup
Once arangodb is fixed on GitHub:

```bash
cd /home/graham/workspace/shared_claude_docs
uv sync
uv pip install -e .
```

## Status of Other Projects
All other Granger projects have valid `pyproject.toml` files:
- ✅ granger_hub
- ✅ rl_commons  
- ✅ claude-test-reporter
- ✅ sparta
- ✅ marker
- ❌ arangodb (needs fix)
- ✅ youtube_transcripts
- ✅ All other projects...

## Alternative: Temporary Workaround
If you need to work immediately without fixing arangodb:

```bash
cd /home/graham/workspace/shared_claude_docs
# Comment out arangodb dependency
sed -i 's/^    "arangodb @ git/    # "arangodb @ git/' pyproject.toml
uv sync
uv pip install -e .
```

Remember to uncomment it after fixing:
```bash
sed -i 's/    # "arangodb @ git/    "arangodb @ git/' pyproject.toml
```

## Root Cause
The issue appears to be malformed TOML syntax where section headers have trailing quotes:
- `[project.scripts]"` instead of `[project.scripts]`
- `[project.optional-dependencies]"` instead of `[project.optional-dependencies]`

This may have been introduced by an automated tool or manual editing error.

## Prevention
To prevent this in the future:
1. Always validate `pyproject.toml` before committing:
   ```bash
   python3 -c "import toml; toml.load(open('pyproject.toml'))"
   ```
2. Use proper TOML editors/validators
3. Set up pre-commit hooks to validate TOML files