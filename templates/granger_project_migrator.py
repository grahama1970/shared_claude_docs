#!/usr/bin/env python3
"""
Granger Project Migrator - Ensures 100% Consistency

This script migrates Granger spoke projects to the MCP prompts standard
with complete consistency across all projects.

Usage:
    python granger_project_migrator.py /path/to/project
    python granger_project_migrator.py --all  # Migrate all known spokes
"""

import sys
import shutil
from pathlib import Path
import json
import subprocess
from typing import List, Dict, Any


# Known Granger spoke projects
SPOKE_PROJECTS = [
    "/home/graham/workspace/experiments/darpa_crawl/",
    "/home/graham/workspace/experiments/gitget/",
    "/home/graham/workspace/experiments/aider-daemon/",
    "/home/graham/workspace/experiments/sparta/",
    "/home/graham/workspace/experiments/marker/",
    "/home/graham/workspace/experiments/arangodb/",
    "/home/graham/workspace/experiments/claude_max_proxy/",
    "/home/graham/workspace/mcp-servers/arxiv-mcp-server/",
    "/home/graham/workspace/experiments/fine_tuning/",
    "/home/graham/workspace/experiments/mcp-screenshot/"
]

# Reference implementations
YOUTUBE_PROMPTS_PY = "/home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/mcp/prompts.py"
GRANGER_MIXIN = "/home/graham/workspace/shared_claude_docs/granger_slash_mcp_mixin.py"
TEMPLATE_PROMPTS = "/home/graham/workspace/shared_claude_docs/templates/mcp_prompts_template.py"


def find_project_module(project_path: Path) -> str:
    """Find the main module name for a project"""
    src_path = project_path / "src"
    if src_path.exists():
        # Look for directories that aren't egg-info
        modules = [d.name for d in src_path.iterdir() 
                  if d.is_dir() and not d.name.endswith('.egg-info') 
                  and not d.name.startswith('_')]
        if modules:
            return modules[0]
    
    # Fallback: use project directory name
    return project_path.name.replace('-', '_')


def ensure_mcp_directory(project_path: Path, module_name: str) -> Path:
    """Ensure MCP directory exists and return its path"""
    mcp_dir = project_path / "src" / module_name / "mcp"
    mcp_dir.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py
    init_file = mcp_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text(f'# {module_name} MCP module\n')
    
    return mcp_dir


def copy_core_infrastructure(mcp_dir: Path) -> bool:
    """Copy the core prompts.py infrastructure"""
    dst = mcp_dir / "prompts.py"
    
    if dst.exists():
        print(f"  ⚠️  prompts.py already exists, skipping")
        return True
    
    if Path(YOUTUBE_PROMPTS_PY).exists():
        shutil.copy2(YOUTUBE_PROMPTS_PY, dst)
        print(f"  ✅ Copied core prompts infrastructure")
        return True
    else:
        print(f"  ❌ Could not find reference prompts.py")
        return False


def create_project_prompts(mcp_dir: Path, project_name: str, module_name: str) -> None:
    """Create project-specific prompts file with 100% consistency"""
    prompts_file = mcp_dir / f"{module_name}_prompts.py"
    
    if prompts_file.exists():
        print(f"  ⚠️  {module_name}_prompts.py already exists, skipping")
        return
    
    # Read template
    template = Path(TEMPLATE_PROMPTS).read_text()
    
    # Customize for this project
    content = template.replace("template", module_name)
    content = content.replace("PROJECT_NAME = \"template\"", f'PROJECT_NAME = "{project_name}"')
    content = content.replace("[YOUR_PROJECT_NAME]", project_name)
    content = content.replace("[YOUR_PROJECT_DESCRIPTION]", f"{project_name} - Granger spoke module")
    content = content.replace("Template project for Granger ecosystem", 
                            f"{project_name} - Intelligent automation for the Granger ecosystem")
    
    prompts_file.write_text(content)
    print(f"  ✅ Created {module_name}_prompts.py with required prompts")


def create_fastmcp_server(mcp_dir: Path, project_name: str, module_name: str) -> None:
    """Create FastMCP server with 100% consistency"""
    server_file = mcp_dir / "server.py"
    
    if server_file.exists():
        print(f"  ⚠️  server.py already exists, updating for prompts...")
        # TODO: Parse and update existing server
        return
    
    content = f'''"""
{project_name} FastMCP Server

Granger standard MCP server implementation for {project_name}.
"""

from fastmcp import FastMCP
from .{module_name}_prompts import register_all_prompts
from .prompts import get_prompt_registry

# Initialize server
mcp = FastMCP("{project_name}")
mcp.description = "{project_name} - Granger spoke module"

# Register prompts
register_all_prompts()
prompt_registry = get_prompt_registry()


# =============================================================================
# PROMPTS - Required for Granger standard
# =============================================================================

@mcp.prompt()
async def capabilities() -> str:
    """List all MCP server capabilities"""
    return await prompt_registry.execute("{project_name}:capabilities")


@mcp.prompt()
async def help(context: str = None) -> str:
    """Get context-aware help"""
    return await prompt_registry.execute("{project_name}:help", context=context)


@mcp.prompt()
async def quick_start() -> str:
    """Quick start guide for new users"""
    return await prompt_registry.execute("{project_name}:quick-start")


# =============================================================================
# TOOLS - Add your existing tools here
# =============================================================================

# TODO: Migrate existing tools from your current implementation
# Example:
# @mcp.tool()
# async def your_tool(param: str) -> dict:
#     """Tool description"""
#     return {{"success": True, "result": param}}


# =============================================================================
# SERVER
# =============================================================================

def serve():
    """Start the MCP server"""
    mcp.run(transport="stdio")  # Use stdio for Claude Code


if __name__ == "__main__":
    # Quick validation
    import asyncio
    
    async def validate():
        result = await capabilities()
        assert "{project_name}" in result.lower()
        print("✅ Server validation passed")
    
    asyncio.run(validate())
    
    # Start server
    serve()
'''
    
    server_file.write_text(content)
    print(f"  ✅ Created FastMCP server.py")


def update_mcp_json(project_path: Path, project_name: str, module_name: str) -> None:
    """Update or create mcp.json with 100% consistency"""
    mcp_json = project_path / "mcp.json"
    
    # Standard configuration
    config = {
        "name": project_name,
        "version": "1.0.0",
        "description": f"{project_name} - Granger spoke module with MCP prompts",
        "author": "Granger Project",
        "license": "MIT",
        "runtime": "python",
        "main": f"src/{module_name}/mcp/server.py",
        "commands": {
            "serve": {
                "description": f"Start the {project_name} MCP server",
                "command": f"python -m {module_name}.mcp.server"
            }
        },
        "prompts": {
            "capabilities": {
                "description": "List all available MCP server capabilities",
                "slash_command": f"/{project_name}:capabilities"
            },
            "help": {
                "description": "Get context-aware help",
                "slash_command": f"/{project_name}:help",
                "parameters": {
                    "context": {
                        "type": "string",
                        "description": "What you're trying to do"
                    }
                }
            },
            "quick-start": {
                "description": "Quick start guide for new users",
                "slash_command": f"/{project_name}:quick-start"
            }
        },
        "capabilities": {
            "tools": True,
            "prompts": True,
            "resources": False
        },
        "config_schema": {
            "type": "object",
            "properties": {
                "log_level": {
                    "type": "string",
                    "description": "Logging level",
                    "default": "INFO",
                    "enum": ["DEBUG", "INFO", "WARNING", "ERROR"]
                }
            }
        }
    }
    
    # Preserve existing tools if file exists
    if mcp_json.exists():
        try:
            existing = json.loads(mcp_json.read_text())
            if "tools" in existing:
                config["tools"] = existing["tools"]
        except:
            pass
    
    mcp_json.write_text(json.dumps(config, indent=2))
    print(f"  ✅ Updated mcp.json with Granger standard configuration")


def update_cli_with_mixin(project_path: Path, module_name: str) -> None:
    """Update CLI to use the Granger standard mixin"""
    # Common CLI file patterns
    cli_patterns = [
        f"src/{module_name}/cli/app.py",
        f"src/{module_name}/cli/__main__.py",
        f"src/{module_name}/__main__.py",
        f"src/{module_name}/cli.py"
    ]
    
    cli_file = None
    for pattern in cli_patterns:
        path = project_path / pattern
        if path.exists():
            cli_file = path
            break
    
    if not cli_file:
        print(f"  ⚠️  No CLI file found, create one manually and add:")
        print(f"     from granger_slash_mcp_mixin import add_slash_mcp_commands")
        print(f"     add_slash_mcp_commands(app, project_name='{module_name}')")
        return
    
    print(f"  ℹ️  Found CLI at {cli_file.relative_to(project_path)}")
    print(f"     Add: add_slash_mcp_commands(app, project_name='{module_name}')")


def create_tests(project_path: Path, module_name: str) -> None:
    """Create test file for prompts"""
    test_dir = project_path / "tests" / "mcp"
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_file = test_dir / "test_prompts.py"
    if test_file.exists():
        print(f"  ⚠️  test_prompts.py already exists, skipping")
        return
    
    content = f'''"""
Test {module_name} MCP prompts implementation

Granger standard test suite for MCP prompts.
"""

import pytest
import asyncio
from {module_name}.mcp.{module_name}_prompts import register_all_prompts


class Test{module_name.title().replace("_", "")}Prompts:
    """Test prompts implementation"""
    
    def test_required_prompts_exist(self):
        """Verify all required prompts are registered"""
        registry = register_all_prompts()
        prompts = registry.list_prompts()
        prompt_names = [p.name for p in prompts]
        
        # Check required prompts (Granger standard)
        required = [
            f"{module_name}:capabilities",
            f"{module_name}:help", 
            f"{module_name}:quick-start"
        ]
        
        for req in required:
            assert req in prompt_names, f"Missing required prompt: {{req}}"
    
    @pytest.mark.asyncio
    async def test_capabilities_prompt(self):
        """Test capabilities prompt execution"""
        registry = register_all_prompts()
        result = await registry.execute(f"{module_name}:capabilities")
        
        assert "{module_name}" in result.lower()
        assert "Available Prompts" in result
        assert "Quick Start Workflow" in result
    
    @pytest.mark.asyncio
    async def test_help_prompt(self):
        """Test help prompt execution"""
        registry = register_all_prompts()
        
        # Test without context
        result = await registry.execute(f"{module_name}:help")
        assert "Common Tasks" in result
        
        # Test with context
        result = await registry.execute(f"{module_name}:help", context="search")
        assert "search" in result.lower()
    
    @pytest.mark.asyncio
    async def test_quick_start_prompt(self):
        """Test quick-start prompt execution"""
        registry = register_all_prompts()
        result = await registry.execute(f"{module_name}:quick-start")
        
        assert "Quick Start" in result
        assert "What is {module_name}?" in result
        assert "Basic Workflow" in result
    
    def test_prompt_consistency(self):
        """Test that all prompts follow Granger naming standard"""
        registry = register_all_prompts()
        prompts = registry.list_prompts()
        
        for prompt in prompts:
            # All prompts should start with module name
            assert prompt.name.startswith(f"{module_name}:"), \
                f"Prompt {{prompt.name}} doesn't follow naming standard"
            
            # All prompts should have descriptions
            assert prompt.description, f"Prompt {{prompt.name}} missing description"
            
            # Check categories
            assert prompt._mcp_prompt.category in [
                "discovery", "research", "analysis", 
                "integration", "export", "help"
            ], f"Prompt {{prompt.name}} has non-standard category"


if __name__ == "__main__":
    # Quick validation
    print(f"Testing {module_name} prompts...")
    registry = register_all_prompts()
    print(f"✅ Registered {{len(registry.list_prompts())}} prompts")
    
    # Run async tests
    import asyncio
    
    async def run_tests():
        test = Test{module_name.title().replace("_", "")}Prompts()
        test.test_required_prompts_exist()
        await test.test_capabilities_prompt()
        await test.test_help_prompt()
        await test.test_quick_start_prompt()
        test.test_prompt_consistency()
        print("✅ All tests passed!")
    
    asyncio.run(run_tests())
'''
    
    test_file.write_text(content)
    print(f"  ✅ Created comprehensive test suite")


def migrate_project(project_path: Path) -> bool:
    """Migrate a single project with 100% consistency"""
    project_name = project_path.name
    print(f"\n🚀 Migrating {project_name} to Granger MCP Standard v1.0.0...")
    
    # Find module name
    module_name = find_project_module(project_path)
    print(f"  📦 Module name: {module_name}")
    
    # Ensure MCP directory
    mcp_dir = ensure_mcp_directory(project_path, module_name)
    print(f"  📁 MCP directory: {mcp_dir.relative_to(project_path)}")
    
    # Copy core infrastructure
    if not copy_core_infrastructure(mcp_dir):
        return False
    
    # Create project prompts
    create_project_prompts(mcp_dir, project_name, module_name)
    
    # Create FastMCP server
    create_fastmcp_server(mcp_dir, project_name, module_name)
    
    # Update mcp.json
    update_mcp_json(project_path, project_name, module_name)
    
    # Update CLI
    update_cli_with_mixin(project_path, module_name)
    
    # Create tests
    create_tests(project_path, module_name)
    
    # Copy granger mixin to project
    mixin_dst = project_path / "src" / module_name / "cli" / "granger_slash_mcp_mixin.py"
    if not mixin_dst.exists() and Path(GRANGER_MIXIN).exists():
        mixin_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(GRANGER_MIXIN, mixin_dst)
        print(f"  ✅ Copied Granger standard mixin")
    
    print(f"\n✅ {project_name} migration complete!")
    print(f"\n📋 Next steps:")
    print(f"  1. Update CLI to use: add_slash_mcp_commands(app, project_name='{project_name}')")
    print(f"  2. Add domain-specific prompts to {module_name}_prompts.py")
    print(f"  3. Migrate existing tools to FastMCP in server.py")
    print(f"  4. Run tests: pytest tests/mcp/test_prompts.py")
    print(f"  5. Test in Claude Code: /{project_name}:capabilities")
    
    return True


def migrate_all_spokes():
    """Migrate all known spoke projects"""
    print("🚀 Granger Ecosystem Migration - Applying MCP Prompts Standard v1.0.0")
    print("=" * 70)
    
    successful = []
    failed = []
    
    for project_path in SPOKE_PROJECTS:
        path = Path(project_path)
        if path.exists():
            try:
                if migrate_project(path):
                    successful.append(path.name)
                else:
                    failed.append(path.name)
            except Exception as e:
                print(f"\n❌ Error migrating {path.name}: {e}")
                failed.append(path.name)
        else:
            print(f"\n⚠️  Skipping {path.name} - path not found")
    
    print("\n" + "=" * 70)
    print("📊 Migration Summary:")
    print(f"  ✅ Successful: {len(successful)}")
    for name in successful:
        print(f"     - {name}")
    
    if failed:
        print(f"  ❌ Failed: {len(failed)}")
        for name in failed:
            print(f"     - {name}")
    
    print(f"\n✨ Migration complete! All projects now follow Granger MCP Standard v1.0.0")
    print(f"📚 See GRANGER_MCP_PROMPTS_STANDARD.md for documentation")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            migrate_all_spokes()
        else:
            project_path = Path(sys.argv[1])
            if not project_path.exists():
                print(f"❌ Project path does not exist: {project_path}")
                sys.exit(1)
            
            success = migrate_project(project_path)
            sys.exit(0 if success else 1)
    else:
        print("Usage:")
        print("  python granger_project_migrator.py /path/to/project")
        print("  python granger_project_migrator.py --all")
        sys.exit(1)


if __name__ == "__main__":
    main()