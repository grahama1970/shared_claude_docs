#!/usr/bin/env python3
"""
Module: deploy_granger_common.py
Description: Deploy granger_common standardized components to all Granger projects

External Dependencies:
- shutil: Built-in file operations
- pathlib: Built-in path handling
"""

import shutil
from pathlib import Path
import subprocess

def deploy_granger_common():
    """Deploy granger_common to all Granger projects."""
    
    # Source directory
    source_dir = Path("/home/graham/workspace/shared_claude_docs/granger_common")
    
    # Target projects
    projects = [
        "/home/graham/workspace/experiments/sparta",
        "/home/graham/workspace/experiments/marker", 
        "/home/graham/workspace/experiments/arangodb",
        "/home/graham/workspace/experiments/youtube_transcripts",
        "/home/graham/workspace/experiments/llm_call",
        "/home/graham/workspace/experiments/unsloth_wip",
        "/home/graham/workspace/mcp-servers/arxiv-mcp-server",
        "/home/graham/workspace/experiments/granger_hub",
        "/home/graham/workspace/experiments/claude-module-communicator",
        "/home/graham/workspace/experiments/claude-test-reporter",
        "/home/graham/workspace/experiments/rl_commons",
        "/home/graham/workspace/experiments/world_model"
    ]
    
    print("🚀 Deploying granger_common to all projects...")
    
    deployed = 0
    failed = 0
    
    for project_path in projects:
        project = Path(project_path)
        if not project.exists():
            print(f"❌ Project not found: {project_path}")
            failed += 1
            continue
            
        # Find src directory
        src_candidates = [
            project / "src",
            project / "src" / project.name,
            project
        ]
        
        target_dir = None
        for candidate in src_candidates:
            if candidate.exists() and candidate.is_dir():
                target_dir = candidate / "granger_common"
                break
        
        if target_dir is None:
            print(f"❌ Could not find src directory in: {project_path}")
            failed += 1
            continue
        
        # Copy granger_common
        try:
            if target_dir.exists():
                shutil.rmtree(target_dir)
            shutil.copytree(source_dir, target_dir)
            print(f"✅ Deployed to: {target_dir}")
            deployed += 1
        except Exception as e:
            print(f"❌ Failed to deploy to {project_path}: {e}")
            failed += 1
    
    print(f"\n📊 Deployment Summary:")
    print(f"   Successful: {deployed}")
    print(f"   Failed: {failed}")
    print(f"   Total: {len(projects)}")
    
    return deployed, failed


def create_init_files():
    """Ensure all granger_common directories have __init__.py files."""
    print("\n📝 Creating __init__.py files...")
    
    init_content = '''"""Granger Common - Standardized components for the Granger ecosystem.

This package contains:
- rate_limiter.py: Thread-safe rate limiting for external APIs
- pdf_handler.py: Smart PDF processing with memory management
- schema_manager.py: Schema versioning and migration
"""

from .rate_limiter import RateLimiter, get_rate_limiter
from .pdf_handler import SmartPDFHandler
from .schema_manager import SchemaManager, SchemaVersion

__all__ = [
    "RateLimiter",
    "get_rate_limiter", 
    "SmartPDFHandler",
    "SchemaManager",
    "SchemaVersion"
]
'''
    
    # Create init file in source
    source_init = Path("/home/graham/workspace/shared_claude_docs/granger_common/__init__.py")
    source_init.write_text(init_content)
    print(f"✅ Created: {source_init}")


if __name__ == "__main__":
    # First create init files
    create_init_files()
    
    # Then deploy
    deployed, failed = deploy_granger_common()
    
    # Exit with error if any deployments failed
    exit(0 if failed == 0 else 1)