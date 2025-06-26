#!/usr/bin/env python3
"""
Module: setup_granger_projects.py
Description: Clone and set up all Granger projects from GitHub

This script:
1. Clones all Granger projects from GitHub
2. Sets up .env files in each project
3. Updates pyproject.toml with GitHub dependencies
4. Installs all dependencies

External Dependencies:
- git: For cloning repositories
- uv: For dependency management

Example Usage:
>>> python setup_granger_projects.py
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List

# Granger GitHub repositories
GRANGER_REPOS = {
    # Core Infrastructure
    "granger_hub": "https://github.com/grahamaco/granger_hub.git",
    "rl_commons": "https://github.com/grahamaco/rl_commons.git", 
    "claude-test-reporter": "https://github.com/grahamaco/claude-test-reporter.git",
    "world_model": "https://github.com/grahamaco/world_model.git",
    
    # Data Processing Spokes
    "sparta": "https://github.com/grahamaco/sparta.git",
    "marker": "https://github.com/grahamaco/marker.git",
    "arangodb": "https://github.com/grahamaco/arangodb.git",
    "youtube_transcripts": "https://github.com/grahamaco/youtube_transcripts.git",
    "unsloth_wip": "https://github.com/grahamaco/unsloth_wip.git",
    "darpa_crawl": "https://github.com/grahamaco/darpa_crawl.git",
    
    # MCP Services
    "arxiv-mcp-server": "https://github.com/grahamaco/arxiv-mcp-server.git",
    "mcp-screenshot": "https://github.com/grahamaco/mcp-screenshot.git",
    "gitget": "https://github.com/grahamaco/gitget.git",
    
    # UI Projects
    "chat": "https://github.com/grahamaco/chat.git",
    "annotator": "https://github.com/grahamaco/annotator.git",
    "aider-daemon": "https://github.com/grahamaco/aider-daemon.git",
    
    # Additional
    "llm_call": "https://github.com/grahamaco/llm_call.git",
}

# Base paths
EXPERIMENTS_DIR = Path("/home/graham/workspace/experiments")
MCP_SERVERS_DIR = Path("/home/graham/workspace/mcp-servers")
SHARED_DOCS_DIR = Path("/home/graham/workspace/shared_claude_docs")

# Common .env template
ENV_TEMPLATE = """# Project Environment Configuration
PYTHONPATH=./src

# ArangoDB Configuration
ARANGO_HOST=http://localhost:8529
ARANGO_USER=root
ARANGO_PASSWORD=openSesame
ARANGO_DATABASE=granger

# Granger Hub
GRANGER_HUB_URL=http://localhost:8000

# API Keys (from shared_claude_docs/.env)
ANTHROPIC_API_KEY={anthropic_key}
GEMINI_API_KEY={gemini_key}
OPENAI_API_KEY={openai_key}

# Module Communication
MODULE_NAME={module_name}
MODULE_VERSION=1.0.0
ENABLE_RL_OPTIMIZATION=true

# Logging
LOG_LEVEL=INFO
DEBUG=true
"""


def read_shared_env() -> Dict[str, str]:
    """Read API keys from shared_claude_docs/.env"""
    env_path = SHARED_DOCS_DIR / ".env"
    env_vars = {}
    
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
    
    return env_vars


def clone_or_update_repo(name: str, url: str, target_dir: Path):
    """Clone or update a Git repository"""
    repo_path = target_dir / name
    
    if repo_path.exists():
        print(f"   Updating {name}...")
        subprocess.run(["git", "pull"], cwd=repo_path, check=True)
    else:
        print(f"   Cloning {name}...")
        subprocess.run(["git", "clone", url, str(repo_path)], check=True)
    
    return repo_path


def create_env_file(repo_path: Path, module_name: str, shared_env: Dict[str, str]):
    """Create .env file for a project"""
    env_file = repo_path / ".env"
    
    if not env_file.exists():
        print(f"   Creating .env for {module_name}...")
        
        env_content = ENV_TEMPLATE.format(
            module_name=module_name,
            anthropic_key=shared_env.get("ANTHROPIC_API_KEY", ""),
            gemini_key=shared_env.get("GEMINI_API_KEY", ""),
            openai_key=shared_env.get("OPENAI_API_KEY", "")
        )
        
        # Add module-specific variables
        if module_name == "youtube_transcripts":
            env_content += f"\nYOUTUBE_API_KEY={shared_env.get('YOUTUBE_API_KEY', '')}\n"
        elif module_name == "marker":
            env_content += f"\nGOOGLE_APPLICATION_CREDENTIALS={shared_env.get('GOOGLE_APPLICATION_CREDENTIALS', '')}\n"
        
        env_file.write_text(env_content)
        print(f"   ✅ Created .env for {module_name}")


def update_pyproject_with_github_deps():
    """Update pyproject.toml with GitHub dependencies"""
    pyproject_path = SHARED_DOCS_DIR / "pyproject.toml"
    
    print("\nUpdating pyproject.toml with GitHub dependencies...")
    
    # Read current content
    with open(pyproject_path) as f:
        content = f.read()
    
    # Replace local file paths with GitHub URLs
    new_deps = []
    for name, url in GRANGER_REPOS.items():
        # Format: "package-name @ git+https://github.com/user/repo.git"
        github_dep = f'    "{name} @ git+{url}",\n'
        new_deps.append(github_dep)
    
    # Find dependencies section and update
    import re
    
    # Remove old local dependencies
    content = re.sub(
        r'    # Granger.*?\n.*?python-arango>=8\.0\.0",',
        '    # Granger Projects from GitHub\n' + ''.join(new_deps) + '    "python-arango>=8.0.0",',
        content,
        flags=re.DOTALL
    )
    
    # Write updated content
    with open(pyproject_path, 'w') as f:
        f.write(content)
    
    print("✅ Updated pyproject.toml")


def main():
    """Main setup function"""
    print("🚀 Setting up Granger projects from GitHub\n")
    
    # Create directories if needed
    EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)
    MCP_SERVERS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Read shared environment variables
    print("Reading shared environment variables...")
    shared_env = read_shared_env()
    
    # Clone/update repositories
    print("\nCloning/updating repositories:")
    
    for name, url in GRANGER_REPOS.items():
        # Determine target directory
        if "mcp" in name:
            target_dir = MCP_SERVERS_DIR
        else:
            target_dir = EXPERIMENTS_DIR
        
        try:
            repo_path = clone_or_update_repo(name, url, target_dir)
            create_env_file(repo_path, name, shared_env)
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to clone {name}: {e}")
        except Exception as e:
            print(f"   ❌ Error with {name}: {e}")
    
    # Update pyproject.toml
    update_pyproject_with_github_deps()
    
    # Install dependencies
    print("\nInstalling dependencies with uv...")
    os.chdir(SHARED_DOCS_DIR)
    subprocess.run(["uv", "sync"], check=True)
    
    print("\n✅ Granger projects setup complete!")
    print("\n📝 Next steps:")
    print("1. Start required services (ArangoDB, etc)")
    print("2. Run integration tests: python test_real_module_bugs.py")
    print("3. Check individual project READMEs for specific setup")


if __name__ == "__main__":
    main()