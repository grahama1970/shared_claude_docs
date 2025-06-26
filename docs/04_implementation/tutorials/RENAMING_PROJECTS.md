# Safe Project Rename Guide

## 🎯 Overview
This guide provides a step-by-step process to safely rename your project directory, GitHub repository, and all associated configurations with minimal risk of errors.

## 📋 Prerequisites
- GitHub CLI (`gh`) installed - Check with: `gh --version`
- Git repository with all changes committed
- UV package manager installed

## 🔧 Before You Start
Replace these placeholders throughout the guide:
- `OLD_PROJECT_NAME` - Your current project name (e.g., `claude-max-proxy`)
- `NEW_PROJECT_NAME` - Your desired project name (e.g., `llm-call`)
- `OLD_PACKAGE_NAME` - Python package name (e.g., `claude_max_proxy`)
- `NEW_PACKAGE_NAME` - New Python package name (e.g., `llm_call`)
- `YOUR_GITHUB_USERNAME` - Your GitHub username
- `YOUR_PROJECT_PATH` - Full path to project directory

## ⚠️ Pre-Rename Safety Checks

### 1. Commit All Changes
```bash
cd YOUR_PROJECT_PATH/OLD_PROJECT_NAME
git add .
git commit -m "Pre-rename commit: Save all work before renaming to NEW_PROJECT_NAME"
git push origin main
```

### 2. Create a Full Backup
```bash
cd YOUR_PROJECT_PATH/
cp -r OLD_PROJECT_NAME OLD_PROJECT_NAME-backup-$(date +%Y%m%d_%H%M%S)
```

### 3. Document Current State
```bash
# Save current environment state
cd OLD_PROJECT_NAME
uv pip freeze > ../pre-rename-dependencies.txt
find . -name "*.pyc" -delete  # Clean Python cache files
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
```

## 📁 Phase 1: Local Directory Rename

### 1. Rename the Directory
```bash
cd YOUR_PROJECT_PATH/
mv OLD_PROJECT_NAME NEW_PROJECT_NAME
cd NEW_PROJECT_NAME
```

### 2. Update pyproject.toml
```bash
# Edit pyproject.toml to update:
# - name = "NEW_PROJECT_NAME"  (instead of OLD_PROJECT_NAME)
# - Update any references to the old name
sed -i 's/OLD_PROJECT_NAME/NEW_PROJECT_NAME/g' pyproject.toml
sed -i 's/OLD_PACKAGE_NAME/NEW_PACKAGE_NAME/g' pyproject.toml
```

### 3. Update Package Directory Name (if exists)
```bash
# If you have a package directory matching the old name
if [ -d "src/OLD_PACKAGE_NAME" ]; then
    mv src/OLD_PACKAGE_NAME src/NEW_PACKAGE_NAME
fi

# Or if it's in the root
if [ -d "OLD_PACKAGE_NAME" ]; then
    mv OLD_PACKAGE_NAME NEW_PACKAGE_NAME
fi
```

### 4. Update All Python Imports
```bash
# Find and replace all imports
find . -type f -name "*.py" -exec sed -i 's/from OLD_PACKAGE_NAME/from NEW_PACKAGE_NAME/g' {} +
find . -type f -name "*.py" -exec sed -i 's/import OLD_PACKAGE_NAME/import NEW_PACKAGE_NAME/g' {} +
```

### 5. Update Configuration Files
```bash
# Update any config files that might reference the old name
for file in .env .env.example *.json *.yaml *.yml *.ini *.cfg; do
    if [ -f "$file" ]; then
        sed -i 's/OLD_PROJECT_NAME/NEW_PROJECT_NAME/g' "$file"
        sed -i 's/OLD_PACKAGE_NAME/NEW_PACKAGE_NAME/g' "$file"
    fi
done
```

## 🔄 Phase 2: Reinstall with UV

### 1. Remove Old Virtual Environment
```bash
# Deactivate if active
deactivate 2>/dev/null || true

# Remove the old .venv
rm -rf .venv

# Clear UV cache for this project
uv cache clean
```

### 2. Create Fresh Environment
```bash
# Create new virtual environment
uv venv

# Activate it
source .venv/bin/activate  # On Linux/Mac
# or
# .venv\Scripts\activate  # On Windows
```

### 3. Reinstall in Editable Mode
```bash
# Install the project with new name
uv pip install -e .

# Verify installation
python -c "import NEW_PACKAGE_NAME; print('Success!')"
```

## 🐙 Phase 3: GitHub Repository Rename

### 1. Rename Using GitHub CLI (Recommended)
```bash
# Ensure you're in the renamed directory
cd YOUR_PROJECT_PATH/NEW_PROJECT_NAME

# Check that you're authenticated
gh auth status

# Rename the repository on GitHub
gh repo rename NEW_PROJECT_NAME

# This automatically:
# - Renames the repo on GitHub
# - Updates your local git remote URL
# - Sets up redirects from the old name
```

### 2. Verify the Rename
```bash
# Confirm the remote URL was updated
git remote -v
# Should show:
# origin  git@github.com:YOUR_GITHUB_USERNAME/NEW_PROJECT_NAME.git (fetch)
# origin  git@github.com:YOUR_GITHUB_USERNAME/NEW_PROJECT_NAME.git (push)

# Open the renamed repo in browser to confirm
gh repo view --web
```

### 3. Alternative: Web Interface Method
If you prefer or if `gh` fails:
1. Go to https://github.com/YOUR_GITHUB_USERNAME/OLD_PROJECT_NAME
2. Click Settings → General
3. Under "Repository name", change to `NEW_PROJECT_NAME`
4. Click "Rename"
5. Then update local remote: `git remote set-url origin git@github.com:YOUR_GITHUB_USERNAME/NEW_PROJECT_NAME.git`

### 4. Update Git Config (if needed)
```bash
# Check for any git configs referencing the old name
git config --local --list | grep OLD_PROJECT_NAME
# Update any found with:
# git config --local <key> <new-value>
```

## 🔍 Phase 4: Search and Replace Remaining References

### 1. Find Remaining References
```bash
# Search for any remaining references
grep -r "OLD_PROJECT_NAME" . --exclude-dir=.git --exclude-dir=.venv --exclude-dir=node_modules
grep -r "OLD_PACKAGE_NAME" . --exclude-dir=.git --exclude-dir=.venv --exclude-dir=node_modules
```

### 2. Update Documentation
```bash
# Update all markdown files
find . -type f -name "*.md" -exec sed -i 's/OLD_PROJECT_NAME/NEW_PROJECT_NAME/g' {} +
find . -type f -name "*.md" -exec sed -i 's/OLD_PACKAGE_NAME/NEW_PACKAGE_NAME/g' {} +
```

### 3. Update Frontend References (if applicable)
```bash
# Update package.json if it exists
if [ -f "frontend/package.json" ]; then
    sed -i 's/OLD_PROJECT_NAME/NEW_PROJECT_NAME/g' frontend/package.json
fi

# Update any React/JS imports
find frontend -type f \( -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" \) \
    -exec sed -i 's/OLD_PROJECT_NAME/NEW_PROJECT_NAME/g' {} +
```

## ✅ Phase 5: Verification

### 1. Test Python Package
```bash
# Test that the package loads
python -c "import NEW_PACKAGE_NAME; print(NEW_PACKAGE_NAME.__name__)"

# Run tests if they exist
python -m pytest tests/ -v
```

### 2. Test Git Operations
```bash
# Test push/pull
git add .
git commit -m "Complete rename from OLD_PROJECT_NAME to NEW_PROJECT_NAME"
git push origin main
git pull
```

### 3. Check Frontend (if applicable)
```bash
cd frontend
npm install  # or pnpm install
npm run dev  # Test that it starts
```

## 🚨 Common Issues and Fixes

### Issue: GitHub CLI Authentication
```bash
# If gh commands fail with authentication error:
gh auth login
# Follow the prompts to authenticate via browser or token
```

### Issue: GitHub CLI Not Installed
```bash
# Install GitHub CLI if needed:
# Ubuntu/Debian:
sudo apt install gh
# Or download from: https://cli.github.com/
```

### Issue: UV Can't Find Package
```bash
# Make sure pyproject.toml has the correct name
# Reinstall:
uv pip uninstall OLD_PACKAGE_NAME
uv pip install -e .
```

### Issue: Git Remote Errors
```bash
# If git push fails:
git remote rm origin
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/NEW_PROJECT_NAME.git
```

### Issue: Frontend Build Errors
```bash
# Clear caches:
rm -rf frontend/node_modules frontend/.next frontend/dist
cd frontend && npm install
```

## 📝 Post-Rename Checklist

- [ ] All Python imports updated
- [ ] pyproject.toml updated
- [ ] Package directory renamed
- [ ] UV reinstall successful
- [ ] Tests passing
- [ ] Git remote updated
- [ ] GitHub repository renamed
- [ ] Documentation updated
- [ ] Frontend working (if applicable)
- [ ] CI/CD pipelines updated (if any)
- [ ] README.md updated
- [ ] Team notified of new repository URL

## 🔄 Rollback Plan

If something goes wrong:
```bash
# Restore from backup
cd YOUR_PROJECT_PATH/
rm -rf NEW_PROJECT_NAME
cp -r OLD_PROJECT_NAME-backup-* OLD_PROJECT_NAME
cd OLD_PROJECT_NAME
git remote set-url origin git@github.com:YOUR_GITHUB_USERNAME/OLD_PROJECT_NAME.git
```

## 📢 Team Communication Template

Subject: Repository Renamed: OLD_PROJECT_NAME → NEW_PROJECT_NAME

Team,

The `OLD_PROJECT_NAME` project has been renamed to `NEW_PROJECT_NAME` to better reflect its purpose.

**Action Required:**
1. Update your local clone:
   ```bash
   cd /path/to/OLD_PROJECT_NAME
   git remote set-url origin git@github.com:YOUR_GITHUB_USERNAME/NEW_PROJECT_NAME.git
   mv ../OLD_PROJECT_NAME ../NEW_PROJECT_NAME
   ```

2. Update any scripts or documentation referencing the old name

**New URLs:**
- GitHub: https://github.com/YOUR_GITHUB_USERNAME/NEW_PROJECT_NAME
- Local: `YOUR_PROJECT_PATH/NEW_PROJECT_NAME/`

Contact me if you have any issues.

---

## 🎯 Success Indicators

You'll know the rename was successful when:
1. `import NEW_PACKAGE_NAME` works in Python
2. `git push` works without errors  
3. Frontend loads without import errors
4. All tests pass
5. No references to "OLD_PROJECT_NAME" remain (except in historical docs)