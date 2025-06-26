#!/usr/bin/env python3
"""
Migration Script for Granger MCP Prompts Standard

This script helps migrate existing Granger spoke projects to support
MCP prompts following the standard architecture.

Usage:
    python migrate_to_prompts.py /path/to/your/project
"""

import sys
import shutil
from pathlib import Path
import json


def migrate_project(project_path: Path):
    """Migrate a project to support MCP prompts"""
    
    print(f"🚀 Migrating {project_path.name} to MCP Prompts Standard...")
    
    # Detect project structure
    src_path = project_path / "src"
    if not src_path.exists():
        print("❌ No src/ directory found. Is this a valid project?")
        return False
    
    # Find project module
    project_modules = [d for d in src_path.iterdir() if d.is_dir() and not d.name.startswith('_')]
    if not project_modules:
        print("❌ No project module found in src/")
        return False
    
    project_name = project_modules[0].name
    print(f"📦 Found project module: {project_name}")
    
    # Create MCP directory
    mcp_dir = src_path / project_name / "mcp"
    if not mcp_dir.exists():
        mcp_dir.mkdir(parents=True)
        print(f"✅ Created MCP directory: {mcp_dir}")
    
    # Copy core infrastructure
    template_dir = Path(__file__).parent
    youtube_ref = Path(__file__).parent.parent.parent / "experiments/youtube_transcripts"
    
    # Copy prompts.py from YouTube Transcripts reference
    prompts_src = youtube_ref / "src/youtube_transcripts/mcp/prompts.py"
    prompts_dst = mcp_dir / "prompts.py"
    
    if prompts_src.exists():
        shutil.copy2(prompts_src, prompts_dst)
        print(f"✅ Copied core prompts infrastructure")
    else:
        print(f"⚠️  Could not find reference prompts.py at {prompts_src}")
        print("   Copy manually from YouTube Transcripts project")
    
    # Create project-specific prompts file
    project_prompts = mcp_dir / f"{project_name}_prompts.py"
    if not project_prompts.exists():
        # Copy template and customize
        template_content = (template_dir / "mcp_prompts_template.py").read_text()
        
        # Replace template placeholders
        customized = template_content.replace("template", project_name)
        customized = customized.replace("[YOUR_PROJECT_NAME]", project_name)
        customized = customized.replace("[YOUR_PROJECT_DESCRIPTION]", 
                                      f"{project_name.title()} - Part of Granger ecosystem")
        customized = customized.replace("Template project for Granger ecosystem",
                                      f"{project_name.title()} - Intelligent automation for Granger")
        
        project_prompts.write_text(customized)
        print(f"✅ Created {project_name}_prompts.py with required prompts")
    
    # Create or update MCP server
    server_file = mcp_dir / "server.py"
    if not server_file.exists():
        server_content = f'''"""
{project_name.title()} FastMCP Server

Implements MCP server with prompts for {project_name}.
"""

from fastmcp import FastMCP
from .{project_name}_prompts import register_all_prompts
from .prompts import get_prompt_registry

# Initialize server
mcp = FastMCP("{project_name}")
mcp.description = "{project_name.title()} - Part of Granger ecosystem"

# Register prompts
register_all_prompts()
prompt_registry = get_prompt_registry()

# Expose required prompts
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
    """Quick start guide"""
    return await prompt_registry.execute("{project_name}:quick-start")

# Add your existing tools here
# Example:
# @mcp.tool()
# async def your_tool(param: str) -> dict:
#     """Your tool description"""
#     return {{"result": "success"}}

def serve():
    """Start the MCP server"""
    mcp.run(transport="stdio")

if __name__ == "__main__":
    serve()
'''
        server_file.write_text(server_content)
        print(f"✅ Created FastMCP server.py")
    else:
        print(f"⚠️  server.py already exists - update manually to add prompts")
    
    # Create __init__.py files
    init_file = mcp_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text(f"# {project_name} MCP module")
        print(f"✅ Created __init__.py")
    
    # Create or update mcp.json
    mcp_json = project_path / "mcp.json"
    if mcp_json.exists():
        config = json.loads(mcp_json.read_text())
        print(f"⚠️  mcp.json exists - updating...")
    else:
        config = {
            "name": project_name,
            "version": "1.0.0",
            "description": f"{project_name.title()} with MCP prompts support"
        }
    
    # Add prompts section
    if "prompts" not in config:
        config["prompts"] = {}
    
    # Add required prompts
    config["prompts"].update({
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
    })
    
    # Update main entry point
    config["main"] = f"src/{project_name}/mcp/server.py"
    config["runtime"] = "python"
    
    # Save updated config
    mcp_json.write_text(json.dumps(config, indent=2))
    print(f"✅ Updated mcp.json with prompts configuration")
    
    # Create test file
    test_dir = project_path / "tests" / "mcp"
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_file = test_dir / "test_prompts.py"
    if not test_file.exists():
        test_content = f'''"""
Test {project_name} MCP prompts implementation
"""

import pytest
import asyncio
from {project_name}.mcp.{project_name}_prompts import register_all_prompts


class Test{project_name.title()}Prompts:
    """Test prompts implementation"""
    
    def test_required_prompts_exist(self):
        """Verify all required prompts are registered"""
        registry = register_all_prompts()
        prompts = registry.list_prompts()
        prompt_names = [p.name for p in prompts]
        
        # Check required prompts
        assert f"{project_name}:capabilities" in prompt_names
        assert f"{project_name}:help" in prompt_names
        assert f"{project_name}:quick-start" in prompt_names
    
    @pytest.mark.asyncio
    async def test_capabilities_prompt(self):
        """Test capabilities prompt execution"""
        registry = register_all_prompts()
        result = await registry.execute(f"{project_name}:capabilities")
        
        assert "{project_name}" in result.lower()
        assert "Available Prompts" in result
    
    @pytest.mark.asyncio
    async def test_help_prompt(self):
        """Test help prompt execution"""
        registry = register_all_prompts()
        
        # Test without context
        result = await registry.execute(f"{project_name}:help")
        assert "Common Tasks" in result
        
        # Test with context
        result = await registry.execute(f"{project_name}:help", context="search")
        assert "search" in result.lower()


if __name__ == "__main__":
    # Quick validation
    registry = register_all_prompts()
    print(f"✅ Registered {{len(registry.list_prompts())}} prompts")
'''
        test_file.write_text(test_content)
        print(f"✅ Created test file for prompts")
    
    # Print next steps
    print(f"\n✨ Migration complete! Next steps:\n")
    print(f"1. Review and customize {project_name}_prompts.py")
    print(f"2. Add your domain-specific prompts")
    print(f"3. Update server.py to include existing tools")
    print(f"4. Run tests: pytest tests/mcp/test_prompts.py")
    print(f"5. Test in Claude Code: /{project_name}:capabilities")
    print(f"\n📚 See GRANGER_MCP_PROMPTS_STANDARD.md for full documentation")
    
    return True


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python migrate_to_prompts.py /path/to/project")
        sys.exit(1)
    
    project_path = Path(sys.argv[1])
    if not project_path.exists():
        print(f"❌ Project path does not exist: {project_path}")
        sys.exit(1)
    
    success = migrate_project(project_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()