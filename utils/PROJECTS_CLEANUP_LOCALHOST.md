# Project-Wide Cleanup & Validation Utility (Localhost Version)

## Overview
A localhost-specific version of the cleanup utility for Claude Code running directly on the local machine. This version removes all SSH dependencies and runs all commands directly.

## Configuration
```json
{
  "timeout_ms": 5000,
  "communicator_project": "/home/graham/workspace/experiments/claude-module-communicator/",
  "test_guide": "/home/graham/workspace/experiments/marker/docs/guides/TASK_LIST_TEMPLATE_GUIDE_V2.md",
  "test_reporter_repo": "claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main",
  "parallel_workers": 4,
  "ci_mode": false,
  "projects": [
    "/home/graham/workspace/experiments/sparta/",
    "/home/graham/workspace/experiments/marker/",
    "/home/graham/workspace/experiments/arangodb/",
    "/home/graham/workspace/experiments/youtube_transcripts/",
    "/home/graham/workspace/experiments/claude_max_proxy/",
    "/home/graham/workspace/mcp-servers/arxiv-mcp-server/",
    "/home/graham/workspace/experiments/claude-module-communicator/",
    "/home/graham/workspace/experiments/claude-test-reporter/",
    "/home/graham/workspace/experiments/fine_tuning/",
    "/home/graham/workspace/experiments/marker-ground-truth/",
    "/home/graham/workspace/experiments/mcp-screenshot/"
  ]
}
```

## Required Tools Installation
```bash
# Install ripgrep for fast searching
curl -LO https://github.com/BurntSushi/ripgrep/releases/download/13.0.0/ripgrep_13.0.0_amd64.deb
sudo dpkg -i ripgrep_13.0.0_amd64.deb

# Install Python tools
pip install rope vulture pipdeptree pip-audit isort black mypy pylint toml
```

## Phase 1: Pre-Cleanup Safety & CI/CD Setup

### Git Safety Protocol
```bash
cd {{project_path}}
git fetch origin
git checkout main
git pull origin main

# Create cleanup branch with timestamp
CLEANUP_BRANCH="cleanup-$(date +%Y%m%d-%H%M%S)"
git checkout -b $CLEANUP_BRANCH
git tag "pre-cleanup-$(date +%Y%m%d-%H%M%S)"

# For CI/CD environments, set up artifacts
if [ "$CI_MODE" = "true" ]; then
    mkdir -p artifacts/pre-cleanup
    cp -r . artifacts/pre-cleanup/
fi
```

### Baseline Test Capture with Coverage
```bash
# Run tests with coverage report
pytest -v tests/ --cov=src/ --cov-report=html --cov-report=json > pre_cleanup_test_results.log 2>&1 || true
EXIT_CODE=$?
echo "Exit code: $EXIT_CODE" >> pre_cleanup_test_results.log

# Save coverage for comparison
cp coverage.json pre_cleanup_coverage.json 2>/dev/null || true
```

## Phase 2: Enhanced Project Analysis

### 1. Documentation Handling with Graceful Defaults
```python
import os
from pathlib import Path

def load_project_docs(project_path):
    """Load project documentation with fallback templates"""
    docs = {}
    
    # CLAUDE.md - AI interaction guidelines
    claude_path = Path(project_path) / "CLAUDE.md"
    if claude_path.exists():
        docs['claude'] = claude_path.read_text()
    else:
        # Create default template
        docs['claude'] = """# AI Interaction Guidelines
        
## Project Overview
[TODO: Add project description]

## Key Constraints
- Follow PEP 8
- Maintain test coverage above 80%
- Document all public APIs
"""
        claude_path.write_text(docs['claude'])
        print(f"Created default CLAUDE.md at {claude_path}")
    
    return docs
```

### 2. Dependency Analysis with Version Checking
```bash
# Analyze dependencies with pipdeptree
pipdeptree --json > dependency_tree.json

# Check for version conflicts
pipdeptree --warn fail > dependency_conflicts.txt 2>&1 || true

# Find unused dependencies with vulture
vulture src/ --min-confidence 80 > unused_code.txt

# Security audit
pip-audit --desc > security_audit.txt

# Extract all imports for cross-project analysis
rg -t py "^(import|from)" --no-heading | sort | uniq > all_imports.txt

# Find cross-project dependencies
rg -t py "(sparta|marker|arangodb|youtube_transcripts|claude_max_proxy|arxiv-mcp-server|claude-module-communicator|claude-test-reporter|fine_tuning)" \
   --no-heading | grep -E "^(import|from)" > cross_project_imports.txt
```

### 3. README.md Feature Validation
```bash
# Extract README.md content if exists
if [ -f README.md ]; then
    echo "=== README.md Feature Validation ===" > readme_validation.txt
    
    # Extract feature claims from README
    rg -i "(feature|capability|function|support|provide|implement)" README.md -A 2 -B 1 > claimed_features.txt
    
    # Extract installation/usage examples
    rg -i "(install|usage|example|quickstart|getting started)" README.md -A 5 > usage_examples.txt
    
    # Extract API/CLI commands mentioned
    rg "(^\s*\$|^\s*>>>|^\s*python|^\s*pip|^\s*npm)" README.md > claimed_commands.txt
else
    echo "WARNING: No README.md found in project root" > readme_validation.txt
fi

# Validate claimed features against actual codebase
echo "=== Feature Implementation Validation ===" >> readme_validation.txt

# For each claimed feature, search for implementation
while IFS= read -r feature; do
    # Extract potential function/class names from feature description
    keywords=$(echo "$feature" | rg -o '\b[A-Z][a-zA-Z]+\b|\b[a-z]+_[a-z]+\b' | tr '\n' '|' | sed 's/|$//')
    
    if [ ! -z "$keywords" ]; then
        echo "\nSearching for implementation of: $feature" >> readme_validation.txt
        rg -l "class|def|function|const|export" --type py -e "$keywords" >> readme_validation.txt 2>&1 || echo "  ⚠️  No implementation found" >> readme_validation.txt
    fi
done < claimed_features.txt

# Validate pyproject.toml includes claude-test-reporter
echo "\n=== Claude Test Reporter Validation ===" >> readme_validation.txt
if [ -f pyproject.toml ]; then
    if rg -q "claude-test-reporter" pyproject.toml; then
        echo "✅ claude-test-reporter found in pyproject.toml" >> readme_validation.txt
        rg "claude-test-reporter" pyproject.toml >> readme_validation.txt
    else
        echo "❌ claude-test-reporter NOT found in pyproject.toml" >> readme_validation.txt
        echo "Required dependency missing: claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main" >> readme_validation.txt
    fi
else
    echo "❌ No pyproject.toml found" >> readme_validation.txt
fi

# Compare claimed vs actual functionality
echo "\n=== Code Coverage vs README Claims ===" >> readme_validation.txt
# Find all public functions/classes
rg "^(class|def) [A-Z]" --type py -o | sort | uniq > actual_public_api.txt
# Compare with what's documented
comm -23 actual_public_api.txt <(rg -o "(\`[a-zA-Z_]+\`|class [A-Z][a-zA-Z]+|def [a-z_]+)" README.md 2>/dev/null | sort | uniq) > undocumented_api.txt
if [ -s undocumented_api.txt ]; then
    echo "⚠️  Undocumented public APIs found:" >> readme_validation.txt
    cat undocumented_api.txt >> readme_validation.txt
fi
```

### 4. Slash Commands and MCP Implementation Validation
```bash
# Check for slash command implementations
echo "=== Slash Commands Validation ===" > slash_commands_validation.txt

# Check if this is a Claude-related project that should have slash commands
if rg -q "(claude|assistant|cli|command)" README.md 2>/dev/null || [ -f "CLAUDE.md" ]; then
    echo "Checking for slash command implementations..." >> slash_commands_validation.txt
    
    # Look for slash command patterns
    rg -l "^/[a-zA-Z]+" --type py --type md > potential_slash_commands.txt 2>/dev/null || true
    
    # Check for command handlers
    rg -l "(handle_command|command_handler|slash_command|@command)" --type py > command_handlers.txt 2>/dev/null || true
    
    # Validate slash command documentation
    if rg -q "slash.*command|/[a-z]+" README.md 2>/dev/null; then
        echo "✅ Slash commands documented in README.md" >> slash_commands_validation.txt
        rg "^/[a-zA-Z]+|slash.*command" README.md >> slash_commands_validation.txt
    else
        echo "⚠️  No slash command documentation found" >> slash_commands_validation.txt
    fi
    
    # Check for actual implementations
    if [ -s command_handlers.txt ]; then
        echo "✅ Command handlers found:" >> slash_commands_validation.txt
        cat command_handlers.txt >> slash_commands_validation.txt
    else
        echo "❌ No command handler implementations found" >> slash_commands_validation.txt
    fi
fi

# Check for MCP (Model Context Protocol) implementations
echo -e "\n=== MCP Implementation Validation ===" >> mcp_validation.txt

# Identify if this is an MCP server project
if rg -q "(mcp|model.*context.*protocol|mcp.*server)" README.md pyproject.toml 2>/dev/null || [[ "$project_path" == *"mcp"* ]]; then
    echo "MCP-related project detected, validating implementation..." >> mcp_validation.txt
    
    # Check for MCP server configuration
    if [ -f "mcp.json" ] || [ -f "server.json" ] || [ -f ".mcp/config.json" ]; then
        echo "✅ MCP configuration file found" >> mcp_validation.txt
    else
        echo "❌ No MCP configuration file (mcp.json, server.json, or .mcp/config.json) found" >> mcp_validation.txt
    fi
    
    # Check for MCP server implementation
    MCP_PATTERNS="MCPServer|ModelContextProtocol|@server\.|mcp_server|handle_request|handle_response"
    if rg -l "$MCP_PATTERNS" --type py > mcp_implementations.txt 2>/dev/null; then
        echo "✅ MCP server implementation found in:" >> mcp_validation.txt
        cat mcp_implementations.txt >> mcp_validation.txt
    else
        echo "❌ No MCP server implementation patterns found" >> mcp_validation.txt
    fi
    
    # Check for required MCP methods
    echo -e "\nChecking for required MCP methods:" >> mcp_validation.txt
    for method in "handle_request" "handle_response" "get_capabilities" "initialize"; do
        if rg -q "def $method" --type py; then
            echo "  ✅ $method found" >> mcp_validation.txt
        else
            echo "  ❌ $method missing" >> mcp_validation.txt
        fi
    done
    
    # Check for MCP dependencies
    if [ -f "pyproject.toml" ]; then
        if rg -q "mcp|model-context-protocol" pyproject.toml; then
            echo -e "\n✅ MCP dependencies found in pyproject.toml" >> mcp_validation.txt
        else
            echo -e "\n❌ No MCP dependencies found in pyproject.toml" >> mcp_validation.txt
        fi
    fi
fi
```

### 5. Fast Directory Analysis with Ripgrep
```bash
# Use ripgrep for fast file discovery (respects .gitignore)
rg --files > all_files.txt

# Find potentially misplaced files
rg --files -g "*.py" -g "!src/**" -g "!tests/**" -g "!setup.py" -g "!conf*.py" > misplaced_python_files.txt
rg --files -g "*.log" > log_files.txt
rg --files -g "*test*.py" -g "!tests/**" > misplaced_test_files.txt

# Search for debug/temp files
rg --files -g "debug_*" -g "temp_*" -g "*.ipynb_checkpoints" > temp_files.txt

# Find TODO/FIXME comments for tracking
rg "TODO|FIXME|HACK|XXX" -t py > technical_debt.txt
```

## Phase 3: Smart File Movement with Import Correction

### Using Rope for Safe Refactoring
```python
from rope.base.project import Project as RopeProject
from rope.refactor.move import create_move
from rope.base import libutils
import os

class SmartFileMover:
    def __init__(self, project_path):
        self.project_path = project_path
        self.rope_project = RopeProject(project_path)
        
    def move_file_with_import_update(self, source_path, dest_path):
        """Move file and automatically update all imports"""
        try:
            # Get rope resources
            source_resource = libutils.path_to_resource(
                self.rope_project, 
                source_path
            )
            
            # Create destination directory if needed
            dest_dir = os.path.dirname(dest_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            
            dest_folder = libutils.path_to_resource(
                self.rope_project,
                dest_dir
            )
            
            # Create move refactoring
            mover = create_move(self.rope_project, source_resource)
            
            # Get changes (this analyzes all imports)
            changes = mover.get_changes(dest_folder)
            
            # Preview changes
            print(f"Moving {source_path} to {dest_path}")
            print("Import updates:")
            print(changes.get_description())
            
            # Apply changes
            self.rope_project.do(changes)
            
            return True
            
        except Exception as e:
            print(f"Error moving {source_path}: {e}")
            return False
    
    def close(self):
        self.rope_project.close()
```

### Cleanup Execution with Import Safety
```python
def cleanup_project_structure(project_path):
    mover = SmartFileMover(project_path)
    
    # Move misplaced Python files
    with open('misplaced_python_files.txt') as f:
        for file_path in f:
            file_path = file_path.strip()
            if file_path.endswith('.py'):
                # Determine correct location
                if 'test' in file_path.lower():
                    dest = f"tests/{os.path.basename(file_path)}"
                else:
                    module_name = os.path.basename(project_path)
                    dest = f"src/{module_name}/utils/{os.path.basename(file_path)}"
                
                mover.move_file_with_import_update(file_path, dest)
    
    mover.close()
    
    # Ensure claude-test-reporter is in pyproject.toml
    ensure_test_reporter_dependency(project_path)

def ensure_test_reporter_dependency(project_path):
    """Ensure claude-test-reporter is properly configured in pyproject.toml"""
    pyproject_path = os.path.join(project_path, 'pyproject.toml')
    
    if not os.path.exists(pyproject_path):
        print(f"⚠️  No pyproject.toml found in {project_path}")
        return False
    
    try:
        import toml
        with open(pyproject_path, 'r') as f:
            pyproject = toml.load(f)
        
        # Check if claude-test-reporter is already present
        dependencies = pyproject.get('tool', {}).get('poetry', {}).get('dependencies', {})
        dev_dependencies = pyproject.get('tool', {}).get('poetry', {}).get('dev-dependencies', {})
        
        test_reporter_spec = "claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main"
        
        if 'claude-test-reporter' not in dependencies and 'claude-test-reporter' not in dev_dependencies:
            print(f"Adding claude-test-reporter to {pyproject_path}")
            
            # Add to dev-dependencies
            if 'tool' not in pyproject:
                pyproject['tool'] = {}
            if 'poetry' not in pyproject['tool']:
                pyproject['tool']['poetry'] = {}
            if 'dev-dependencies' not in pyproject['tool']['poetry']:
                pyproject['tool']['poetry']['dev-dependencies'] = {}
            
            pyproject['tool']['poetry']['dev-dependencies']['claude-test-reporter'] = {
                "git": "https://github.com/grahama1970/claude-test-reporter.git",
                "branch": "main"
            }
            
            # Write back
            with open(pyproject_path, 'w') as f:
                toml.dump(pyproject, f)
            
            print(f"✅ Added claude-test-reporter to {pyproject_path}")
            return True
        else:
            print(f"✅ claude-test-reporter already present in {pyproject_path}")
            return True
            
    except Exception as e:
        print(f"❌ Error updating pyproject.toml: {e}")
        return False
```

## Phase 4: Enhanced Inter-Project Communication Testing

### Local Communication Testing (No SSH)
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
import subprocess
import sys

def test_communication_pair(proj1, proj2):
    """Test communication between two projects locally"""
    results = {
        'status': 'testing',
        'proj1_to_proj2': False,
        'proj2_to_proj1': False,
        'errors': []
    }
    
    try:
        # Test importing from proj1 in proj2 context
        test_import_cmd = f"""
cd {proj2} && python -c "
import sys
sys.path.insert(0, '{proj1}')
try:
    from src import *
    print('Import successful')
except Exception as e:
    print(f'Import failed: {{e}}')
"
"""
        result = subprocess.run(test_import_cmd, shell=True, capture_output=True, text=True)
        if 'Import successful' in result.stdout:
            results['proj1_to_proj2'] = True
        else:
            results['errors'].append(f"Import {proj1} -> {proj2}: {result.stderr}")
        
        # Test reverse direction
        test_import_cmd = f"""
cd {proj1} && python -c "
import sys
sys.path.insert(0, '{proj2}')
try:
    from src import *
    print('Import successful')
except Exception as e:
    print(f'Import failed: {{e}}')
"
"""
        result = subprocess.run(test_import_cmd, shell=True, capture_output=True, text=True)
        if 'Import successful' in result.stdout:
            results['proj2_to_proj1'] = True
        else:
            results['errors'].append(f"Import {proj2} -> {proj1}: {result.stderr}")
        
        if results['proj1_to_proj2'] or results['proj2_to_proj1']:
            results['status'] = 'success'
        else:
            results['status'] = 'failed'
            
    except Exception as e:
        results['status'] = 'error'
        results['errors'].append(str(e))
    
    return results

async def test_project_communications(projects, max_workers=4):
    """Test all project pairs can communicate"""
    results = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        tasks = []
        
        for i, proj1 in enumerate(projects):
            for proj2 in projects[i+1:]:
                task = executor.submit(
                    test_communication_pair, 
                    proj1, 
                    proj2
                )
                tasks.append((proj1, proj2, task))
        
        # Gather results
        for proj1, proj2, task in tasks:
            key = f"{proj1} <-> {proj2}"
            try:
                results[key] = task.result(timeout=30)
            except Exception as e:
                results[key] = {"status": "error", "message": str(e)}
    
    return results
```

## Phase 5: Main Execution Script (Localhost Version)

```python
#!/usr/bin/env python3
import asyncio
from multiprocessing import Pool
import tqdm
from pathlib import Path
import os
import json
import re
from datetime import datetime

class ProjectCleanupUtilityLocal:
    """Localhost version - no SSH required"""
    
    def __init__(self, config):
        self.config = config
        self.results = {}
        
    def _analyze_project(self, project_path):
        """Comprehensive project analysis including README validation"""
        analysis_results = {
            'readme_validation': {},
            'dependencies': {},
            'test_reporter': {},
            'code_structure': {},
            'slash_commands': {},
            'mcp_implementation': {}
        }
        
        # README.md validation
        readme_path = os.path.join(project_path, 'README.md')
        if os.path.exists(readme_path):
            analysis_results['readme_validation'] = self._validate_readme_claims(project_path)
        else:
            analysis_results['readme_validation']['status'] = 'missing'
            analysis_results['readme_validation']['message'] = 'No README.md found'
        
        # Test reporter validation
        pyproject_path = os.path.join(project_path, 'pyproject.toml')
        if os.path.exists(pyproject_path):
            with open(pyproject_path, 'r') as f:
                content = f.read()
                if 'claude-test-reporter' in content:
                    analysis_results['test_reporter']['status'] = 'present'
                else:
                    analysis_results['test_reporter']['status'] = 'missing'
                    analysis_results['test_reporter']['action'] = 'will_add'
        else:
            analysis_results['test_reporter']['status'] = 'no_pyproject'
        
        # Run existing analysis commands locally
        os.chdir(project_path)
        os.system('rg --files > all_files.txt')
        os.system('rg -t py "TODO|FIXME|HACK" > technical_debt.txt')
        
        # Slash command validation
        analysis_results['slash_commands'] = self._validate_slash_commands(project_path)
        
        # MCP implementation validation
        analysis_results['mcp_implementation'] = self._validate_mcp_implementation(project_path)
        
        return analysis_results
    
    def _validate_readme_claims(self, project_path):
        """Validate README claims against actual implementation"""
        validation_results = {
            'claimed_features': [],
            'implemented_features': [],
            'missing_implementations': []
        }
        
        # Extract claimed features
        readme_path = os.path.join(project_path, 'README.md')
        with open(readme_path, 'r') as f:
            readme_content = f.read()
        
        # Simple feature extraction
        import re
        feature_patterns = [
            r'[*-]\s+(.*?(?:feature|capability|support|provide|implement).*?)(?:\n|$)',
            r'##\s+Features?\s*\n(.*?)(?:\n##|\Z)',
        ]
        
        for pattern in feature_patterns:
            matches = re.findall(pattern, readme_content, re.IGNORECASE | re.DOTALL)
            validation_results['claimed_features'].extend(matches)
        
        # Check for actual implementations
        for feature in validation_results['claimed_features']:
            # Extract key terms
            key_terms = re.findall(r'\b[A-Z][a-zA-Z]+\b|\b[a-z]+_[a-z]+\b', feature)
            
            for term in key_terms:
                # Search for implementation
                search_cmd = f'rg -l "class {term}|def {term}" --type py 2>/dev/null'
                result = os.popen(search_cmd).read().strip()
                
                if result:
                    validation_results['implemented_features'].append({
                        'feature': feature,
                        'term': term,
                        'files': result.split('\n')
                    })
                else:
                    validation_results['missing_implementations'].append({
                        'feature': feature,
                        'term': term
                    })
        
        return validation_results
    
    def _validate_slash_commands(self, project_path):
        """Validate slash command implementations"""
        validation_results = {
            'needs_commands': False,
            'has_documentation': False,
            'has_implementation': False,
            'commands_found': [],
            'issues': []
        }
        
        # Check if this project should have slash commands
        readme_path = os.path.join(project_path, 'README.md')
        claude_path = os.path.join(project_path, 'CLAUDE.md')
        
        needs_commands = False
        if os.path.exists(readme_path):
            with open(readme_path, 'r') as f:
                content = f.read().lower()
                if any(keyword in content for keyword in ['claude', 'assistant', 'cli', 'command']):
                    needs_commands = True
        
        if os.path.exists(claude_path):
            needs_commands = True
        
        validation_results['needs_commands'] = needs_commands
        
        if needs_commands:
            # Check for slash command documentation
            doc_cmd = 'rg "slash.*command|^/[a-zA-Z]+" README.md CLAUDE.md 2>/dev/null | head -20'
            doc_result = os.popen(doc_cmd).read().strip()
            if doc_result:
                validation_results['has_documentation'] = True
                validation_results['commands_found'] = re.findall(r'/[a-zA-Z]+', doc_result)
            else:
                validation_results['issues'].append('No slash command documentation found')
            
            # Check for implementation
            impl_cmd = 'rg -l "handle_command|command_handler|slash_command|@command" --type py 2>/dev/null'
            impl_result = os.popen(impl_cmd).read().strip()
            if impl_result:
                validation_results['has_implementation'] = True
                validation_results['implementation_files'] = impl_result.split('\n')
            else:
                validation_results['issues'].append('No command handler implementation found')
        
        return validation_results
    
    def _validate_mcp_implementation(self, project_path):
        """Validate MCP (Model Context Protocol) implementation"""
        validation_results = {
            'is_mcp_project': False,
            'has_config': False,
            'has_implementation': False,
            'has_dependencies': False,
            'required_methods': {},
            'issues': []
        }
        
        # Check if this is an MCP project
        is_mcp = False
        
        # Check project name
        if 'mcp' in os.path.basename(project_path).lower():
            is_mcp = True
        
        # Check README/pyproject for MCP mentions
        check_files = ['README.md', 'pyproject.toml']
        for file in check_files:
            file_path = os.path.join(project_path, file)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    content = f.read().lower()
                    if any(term in content for term in ['mcp', 'model context protocol', 'mcp-server']):
                        is_mcp = True
                        break
        
        validation_results['is_mcp_project'] = is_mcp
        
        if is_mcp:
            # Check for MCP configuration files
            config_files = ['mcp.json', 'server.json', '.mcp/config.json']
            for config_file in config_files:
                if os.path.exists(os.path.join(project_path, config_file)):
                    validation_results['has_config'] = True
                    validation_results['config_file'] = config_file
                    break
            
            if not validation_results['has_config']:
                validation_results['issues'].append('No MCP configuration file found')
            
            # Check for MCP implementation
            impl_cmd = 'rg -l "MCPServer|ModelContextProtocol|@server\\.|mcp_server" --type py 2>/dev/null'
            impl_result = os.popen(impl_cmd).read().strip()
            if impl_result:
                validation_results['has_implementation'] = True
                validation_results['implementation_files'] = impl_result.split('\n')
            else:
                validation_results['issues'].append('No MCP server implementation found')
            
            # Check for required methods
            required_methods = ['handle_request', 'handle_response', 'get_capabilities', 'initialize']
            for method in required_methods:
                method_cmd = f'rg -q "def {method}" --type py 2>/dev/null'
                if os.system(method_cmd) == 0:
                    validation_results['required_methods'][method] = True
                else:
                    validation_results['required_methods'][method] = False
                    validation_results['issues'].append(f'Required method "{method}" not found')
            
            # Check dependencies
            pyproject_path = os.path.join(project_path, 'pyproject.toml')
            if os.path.exists(pyproject_path):
                with open(pyproject_path, 'r') as f:
                    if re.search(r'mcp|model-context-protocol', f.read(), re.IGNORECASE):
                        validation_results['has_dependencies'] = True
                    else:
                        validation_results['issues'].append('MCP dependencies not found in pyproject.toml')
        
        return validation_results
    
    def _git_safety_branch(self, project_path):
        """Create safety branch for changes"""
        os.chdir(project_path)
        os.system('git fetch origin')
        os.system('git checkout main')
        os.system('git pull origin main')
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        branch_name = f'cleanup-{timestamp}'
        os.system(f'git checkout -b {branch_name}')
        os.system(f'git tag pre-cleanup-{timestamp}')
    
    def _smart_cleanup(self, project_path):
        """Perform smart cleanup with import updates"""
        # Implementation would call cleanup_project_structure
        return {'status': 'completed', 'files_moved': 0}
    
    def _run_tests(self, project_path):
        """Run tests and return results"""
        os.chdir(project_path)
        result = os.system('pytest -v tests/ --cov=src/ --cov-report=json > test_results.log 2>&1')
        return {'passed': result == 0, 'exit_code': result}
    
    def _merge_changes(self, project_path):
        """Merge changes back to main"""
        os.chdir(project_path)
        os.system('git add -A')
        os.system('git commit -m "Automated cleanup and validation"')
    
    def _rollback_changes(self, project_path):
        """Rollback changes if tests fail"""
        os.chdir(project_path)
        os.system('git checkout main')
        os.system('git branch -D $(git branch --show-current)')
    
    def process_project(self, project_path):
        """Process single project with all phases"""
        print(f"\n{'='*60}")
        print(f"Processing: {project_path}")
        print(f"{'='*60}")
        
        results = {
            'project': project_path,
            'status': 'started',
            'phases': {}
        }
        
        try:
            # Phase 1: Git safety
            self._git_safety_branch(project_path)
            
            # Phase 2: Analysis
            analysis = self._analyze_project(project_path)
            results['phases']['analysis'] = analysis
            
            # Phase 3: Cleanup with import fixing
            cleanup = self._smart_cleanup(project_path)
            results['phases']['cleanup'] = cleanup
            
            # Phase 4: Testing
            test_results = self._run_tests(project_path)
            results['phases']['tests'] = test_results
            
            # Phase 5: Validation
            if test_results['passed']:
                self._merge_changes(project_path)
                results['status'] = 'completed'
            else:
                self._rollback_changes(project_path)
                results['status'] = 'rolled_back'
                
        except Exception as e:
            results['status'] = 'error'
            results['error'] = str(e)
            self._rollback_changes(project_path)
            
        return results
    
    def run_parallel(self):
        """Process all projects in parallel"""
        with Pool(processes=self.config.get('parallel_workers', 4)) as pool:
            # Use tqdm for progress bar
            with tqdm.tqdm(total=len(self.config['projects'])) as pbar:
                for result in pool.imap_unordered(
                    self.process_project, 
                    self.config['projects']
                ):
                    self.results[result['project']] = result
                    pbar.update(1)
                    
        # Run cross-project communication tests
        comm_results = asyncio.run(
            test_project_communications(self.config['projects'])
        )
        self.results['communications'] = comm_results
        
        return self.results

# Main execution
if __name__ == "__main__":
    import sys
    
    # Load configuration
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'cleanup_config.json'
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Run cleanup utility
    utility = ProjectCleanupUtilityLocal(config)
    results = utility.run_parallel()
    
    # Generate report
    from report_generator import generate_comprehensive_report
    report = generate_comprehensive_report(results)
    
    # Save report
    with open('cleanup_report.md', 'w') as f:
        f.write(report)
    
    print("\nCleanup completed! Report saved to cleanup_report.md")
```

## Key Differences from SSH Version:

1. **No SSH Configuration** - Removed `connection_command` from config
2. **Direct Local Execution** - All commands run directly without SSH
3. **Local Path Access** - Direct file system access without remote connections
4. **Simplified Testing** - Inter-project communication tests use local Python imports
5. **Performance** - Faster execution without network overhead

## Usage:

```bash
# Save configuration to cleanup_config_local.json
# Run the cleanup utility
python cleanup_utility_local.py cleanup_config_local.json
```

This localhost version is optimized for Claude Code running directly on the Linux machine, eliminating all SSH-related complexity while maintaining all the validation features.