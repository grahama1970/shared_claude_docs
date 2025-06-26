#!/usr/bin/env python3
"""
Big Picture Analyzer
Analyzes all registered projects to create unified descriptions of their capabilities,
usage, and potential improvements.
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import subprocess
import re

class ProjectAnalyzer:
    """Analyzes individual projects and generates comprehensive documentation"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Registered projects in order
        self.projects = [
            {
                "path": "/home/graham/workspace/shared_claude_docs/",
                "name": "shared_claude_docs",
                "order": "000"
            },
            {
                "path": "/home/graham/workspace/experiments/sparta/",
                "name": "sparta",
                "order": "001"
            },
            {
                "path": "/home/graham/workspace/experiments/marker/",
                "name": "marker",
                "order": "002"
            },
            {
                "path": "/home/graham/workspace/experiments/arangodb/",
                "name": "arangodb",
                "order": "003"
            },
            {
                "path": "/home/graham/workspace/experiments/youtube_transcripts/",
                "name": "youtube_transcripts",
                "order": "004"
            },
            {
                "path": "/home/graham/workspace/experiments/claude_max_proxy/",
                "name": "claude_max_proxy",
                "order": "005"
            },
            {
                "path": "/home/graham/workspace/mcp-servers/arxiv-mcp-server/",
                "name": "arxiv-mcp-server",
                "order": "006"
            },
            {
                "path": "/home/graham/workspace/experiments/claude-module-communicator/",
                "name": "claude-module-communicator",
                "order": "007"
            },
            {
                "path": "/home/graham/workspace/experiments/claude-test-reporter/",
                "name": "claude-test-reporter",
                "order": "008"
            },
            {
                "path": "/home/graham/workspace/experiments/fine_tuning/",
                "name": "unsloth_wip",
                "order": "009"
            },
            {
                "path": "/home/graham/workspace/experiments/marker-ground-truth/",
                "name": "marker-ground-truth",
                "order": "010"
            },
            {
                "path": "/home/graham/workspace/experiments/mcp-screenshot/",
                "name": "mcp-screenshot",
                "order": "011"
            }
        ]
        
        self.analysis_template = """# {project_name}

## Overview
{overview}

## Core Capabilities
{capabilities}

## Technical Architecture
{architecture}

## Installation & Setup
{installation}

## Usage Examples
{usage_examples}

## API/Interface Documentation
{api_docs}

## Integration Points
{integration}

## Dependencies
{dependencies}

## Current Limitations
{limitations}

## Potential Improvements
{improvements}

## Error Analysis
{errors}

## Missing Features
{missing_features}

## Related Projects
{related_projects}

## Notes
{notes}

---
*Generated: {timestamp}*
"""

    async def analyze_all_projects(self):
        """Analyze all registered projects"""
        print("🔍 Starting Big Picture Analysis")
        print("=" * 60)
        
        for project in self.projects:
            await self.analyze_project(project)
        
        # Create master index
        await self.create_master_index()
        
        print("\n✅ Analysis complete!")
        print(f"📁 Results saved to: {self.output_dir}")

    async def analyze_project(self, project: Dict[str, str]):
        """Analyze a single project"""
        print(f"\n📂 Analyzing {project['name']}...")
        
        project_path = Path(project['path'])
        if not project_path.exists():
            print(f"  ⚠️  Project not found: {project_path}")
            return
        
        # Gather project information
        analysis = {
            "project_name": project['name'].replace('_', ' ').title(),
            "overview": await self._get_overview(project_path),
            "capabilities": await self._analyze_capabilities(project_path),
            "architecture": await self._analyze_architecture(project_path),
            "installation": await self._get_installation_info(project_path),
            "usage_examples": await self._get_usage_examples(project_path),
            "api_docs": await self._analyze_api(project_path),
            "integration": await self._analyze_integration_points(project_path),
            "dependencies": await self._analyze_dependencies(project_path),
            "limitations": await self._analyze_limitations(project_path),
            "improvements": await self._suggest_improvements(project_path, project['name']),
            "errors": await self._analyze_errors(project_path),
            "missing_features": await self._identify_missing_features(project_path, project['name']),
            "related_projects": self._get_related_projects(project['name']),
            "notes": await self._get_additional_notes(project_path),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Generate output
        output_content = self.analysis_template.format(**analysis)
        output_file = self.output_dir / f"{project['order']}_Describe_{project['name']}.md"
        
        with open(output_file, 'w') as f:
            f.write(output_content)
        
        print(f"  ✅ Analysis saved to: {output_file.name}")

    async def _get_overview(self, project_path: Path) -> str:
        """Extract project overview from README"""
        readme_files = ["README.md", "readme.md", "README.rst", "README.txt"]
        
        for readme in readme_files:
            readme_path = project_path / readme
            if readme_path.exists():
                content = readme_path.read_text()
                # Extract first paragraph or description
                lines = content.split('\n')
                overview_lines = []
                started = False
                
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        started = True
                        overview_lines.append(line)
                    elif started and not line.strip():
                        break
                
                if overview_lines:
                    return ' '.join(overview_lines)
        
        return "No overview found. This project requires documentation."

    async def _analyze_capabilities(self, project_path: Path) -> str:
        """Analyze project capabilities"""
        capabilities = []
        
        # Check for specific patterns in code
        py_files = list(project_path.rglob("*.py"))
        
        # Analyze main modules
        for py_file in py_files[:10]:  # Limit to avoid too much processing
            try:
                content = py_file.read_text()
                
                # Look for class definitions
                classes = re.findall(r'class\s+(\w+)', content)
                # Look for main functions
                functions = re.findall(r'def\s+(\w+)\s*\(', content)
                
                if classes or functions:
                    capabilities.append(f"- **{py_file.name}**: Contains {len(classes)} classes and {len(functions)} functions")
            except:
                pass
        
        # Check for CLI tools
        if (project_path / "cli.py").exists() or (project_path / "__main__.py").exists():
            capabilities.append("- Command-line interface available")
        
        # Check for API endpoints
        if any(f.name in ["app.py", "server.py", "api.py"] for f in py_files):
            capabilities.append("- Web API/Server capabilities")
        
        # Check for specific frameworks
        if (project_path / "requirements.txt").exists():
            reqs = (project_path / "requirements.txt").read_text()
            if "fastapi" in reqs or "flask" in reqs:
                capabilities.append("- Web framework integration")
            if "pytorch" in reqs or "tensorflow" in reqs:
                capabilities.append("- Machine learning capabilities")
            if "playwright" in reqs or "selenium" in reqs:
                capabilities.append("- Web automation capabilities")
        
        return '\n'.join(capabilities) if capabilities else "- Core functionality to be determined through code analysis"

    async def _analyze_architecture(self, project_path: Path) -> str:
        """Analyze project architecture"""
        architecture = []
        
        # Analyze directory structure
        dirs = [d for d in project_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        if dirs:
            architecture.append("### Directory Structure")
            for d in sorted(dirs):
                py_files = list(d.glob("*.py"))
                if py_files:
                    architecture.append(f"- `{d.name}/`: {len(py_files)} Python files")
        
        # Look for patterns
        if (project_path / "src").exists():
            architecture.append("\n### Source Organization")
            architecture.append("- Follows standard src/ layout")
        
        if (project_path / "tests").exists():
            architecture.append("- Test suite included")
        
        if (project_path / "docs").exists():
            architecture.append("- Documentation directory present")
        
        # Check for configuration files
        config_files = ["config.py", "settings.py", ".env.example", "config.json"]
        found_configs = [f for f in config_files if (project_path / f).exists()]
        if found_configs:
            architecture.append("\n### Configuration")
            architecture.append(f"- Configuration files: {', '.join(found_configs)}")
        
        return '\n'.join(architecture) if architecture else "Standard Python project structure"

    async def _get_installation_info(self, project_path: Path) -> str:
        """Extract installation information"""
        installation = []
        
        # Check for standard installation files
        if (project_path / "setup.py").exists():
            installation.append("```bash\npip install -e .\n```")
        elif (project_path / "pyproject.toml").exists():
            installation.append("```bash\npip install -e .\n```")
        elif (project_path / "requirements.txt").exists():
            installation.append("```bash\npip install -r requirements.txt\n```")
        
        # Check README for installation section
        readme_path = project_path / "README.md"
        if readme_path.exists():
            content = readme_path.read_text().lower()
            if "installation" in content or "install" in content:
                installation.append("\nSee README.md for detailed installation instructions")
        
        # Check for Docker
        if (project_path / "Dockerfile").exists():
            installation.append("\n### Docker Installation")
            installation.append("```bash\ndocker build -t " + project_path.name + " .\n```")
        
        return '\n'.join(installation) if installation else "Installation instructions not found"

    async def _get_usage_examples(self, project_path: Path) -> str:
        """Extract usage examples"""
        examples = []
        
        # Check for examples directory
        examples_dir = project_path / "examples"
        if examples_dir.exists():
            example_files = list(examples_dir.glob("*.py"))
            if example_files:
                examples.append("### Example Scripts")
                for f in example_files[:5]:
                    examples.append(f"- `{f.name}`")
        
        # Check README for usage section
        readme_path = project_path / "README.md"
        if readme_path.exists():
            content = readme_path.read_text()
            # Look for code blocks after "Usage" or "Example"
            if "## Usage" in content or "## Example" in content:
                examples.append("\n### From README")
                examples.append("See README.md for usage examples")
        
        # Check for main entry point
        if (project_path / "__main__.py").exists():
            examples.append("\n### Command Line")
            examples.append(f"```bash\npython -m {project_path.name}\n```")
        
        return '\n'.join(examples) if examples else "Usage examples to be added"

    async def _analyze_api(self, project_path: Path) -> str:
        """Analyze API structure"""
        api_info = []
        
        # Check for API files
        api_files = list(project_path.rglob("*api*.py"))
        if api_files:
            api_info.append("### API Endpoints")
            for f in api_files[:5]:
                api_info.append(f"- `{f.relative_to(project_path)}`")
        
        # Check for OpenAPI/Swagger
        if (project_path / "openapi.json").exists() or (project_path / "swagger.json").exists():
            api_info.append("\n### API Documentation")
            api_info.append("- OpenAPI/Swagger specification available")
        
        # Check for GraphQL
        if any("graphql" in f.name.lower() for f in project_path.rglob("*.py")):
            api_info.append("- GraphQL API detected")
        
        return '\n'.join(api_info) if api_info else "No API documentation found"

    async def _analyze_integration_points(self, project_path: Path) -> str:
        """Analyze how this project integrates with others"""
        integrations = []
        
        project_name = project_path.name
        
        # Check for known integrations
        integration_map = {
            "shared_claude_docs": ["All projects", "Documentation synchronization", "CLAUDE.md management"],
            "claude-module-communicator": ["All other modules", "Central communication hub"],
            "arxiv-mcp-server": ["marker", "sparta", "claude-module-communicator"],
            "marker": ["arxiv-mcp-server", "marker-ground-truth", "sparta"],
            "youtube_transcripts": ["sparta", "arangodb", "claude-module-communicator"],
            "sparta": ["marker", "youtube_transcripts", "arangodb"],
            "arangodb": ["All data-producing modules", "Knowledge graph storage"],
            "mcp-screenshot": ["claude-test-reporter", "UI analysis tools"],
            "claude-test-reporter": ["All modules with tests", "CI/CD pipelines"],
            "unsloth_wip": ["sparta", "Model training pipelines"],
            "marker-ground-truth": ["marker", "Validation systems"],
            "claude_max_proxy": ["All Claude-interfacing modules", "API management"]
        }
        
        if project_name in integration_map:
            integrations.append("### Direct Integrations")
            for integration in integration_map[project_name]:
                integrations.append(f"- {integration}")
        
        # Check imports for cross-references
        py_files = list(project_path.rglob("*.py"))[:10]
        for py_file in py_files:
            try:
                content = py_file.read_text()
                for other_project in ["arxiv", "marker", "youtube", "sparta", "arangodb", "mcp", "claude"]:
                    if other_project in content and other_project != project_name:
                        integrations.append(f"- References {other_project} in {py_file.name}")
                        break
            except:
                pass
        
        return '\n'.join(integrations) if integrations else "- Standalone module (integration points to be identified)"

    async def _analyze_dependencies(self, project_path: Path) -> str:
        """Analyze project dependencies"""
        deps = []
        
        # Check requirements.txt
        req_file = project_path / "requirements.txt"
        if req_file.exists():
            requirements = req_file.read_text().strip().split('\n')
            deps.append("### Python Dependencies")
            for req in requirements[:10]:  # Show first 10
                if req and not req.startswith('#'):
                    deps.append(f"- {req}")
            if len(requirements) > 10:
                deps.append(f"- ... and {len(requirements) - 10} more")
        
        # Check package.json for Node dependencies
        package_json = project_path / "package.json"
        if package_json.exists():
            deps.append("\n### Node.js Dependencies")
            deps.append("- See package.json")
        
        # Check for system dependencies in README
        readme_path = project_path / "README.md"
        if readme_path.exists():
            content = readme_path.read_text().lower()
            if "dependencies" in content or "requirements" in content:
                deps.append("\n### Additional Requirements")
                deps.append("- See README.md for system dependencies")
        
        return '\n'.join(deps) if deps else "No explicit dependencies found"

    async def _analyze_limitations(self, project_path: Path) -> str:
        """Analyze current limitations"""
        limitations = []
        
        # Check for TODO/FIXME in code
        py_files = list(project_path.rglob("*.py"))[:20]
        todos = []
        fixmes = []
        
        for py_file in py_files:
            try:
                content = py_file.read_text()
                todos.extend(re.findall(r'#\s*TODO:?\s*(.+)', content))
                fixmes.extend(re.findall(r'#\s*FIXME:?\s*(.+)', content))
            except:
                pass
        
        if todos:
            limitations.append(f"### Known TODOs ({len(todos)} found)")
            for todo in todos[:3]:
                limitations.append(f"- {todo.strip()}")
        
        if fixmes:
            limitations.append(f"\n### Known Issues ({len(fixmes)} found)")
            for fixme in fixmes[:3]:
                limitations.append(f"- {fixme.strip()}")
        
        # Check for common limitations
        if not (project_path / "tests").exists():
            limitations.append("\n### Testing")
            limitations.append("- No test suite found")
        
        if not (project_path / "docs").exists() and not (project_path / "README.md").exists():
            limitations.append("\n### Documentation")
            limitations.append("- Limited documentation available")
        
        return '\n'.join(limitations) if limitations else "No significant limitations identified"

    async def _suggest_improvements(self, project_path: Path, project_name: str) -> str:
        """Suggest improvements based on analysis"""
        improvements = []
        
        # Check for missing standard files
        missing_files = []
        standard_files = {
            "README.md": "documentation",
            ".gitignore": "Git configuration",
            "requirements.txt": "dependency management",
            "setup.py": "package installation",
            "tests/": "test suite",
            ".env.example": "environment configuration example"
        }
        
        for file, purpose in standard_files.items():
            if not (project_path / file).exists():
                missing_files.append(f"- Add {file} for {purpose}")
        
        if missing_files:
            improvements.append("### Missing Standard Files")
            improvements.extend(missing_files)
        
        # Suggest based on project type
        suggestions_map = {
            "shared_claude_docs": [
                "- Add automated documentation generation from code",
                "- Implement documentation versioning",
                "- Add interactive documentation browser",
                "- Create documentation quality metrics"
            ],
            "arxiv-mcp-server": [
                "- Add rate limiting for API calls",
                "- Implement caching for frequent queries",
                "- Add batch processing capabilities"
            ],
            "marker": [
                "- Improve PDF parsing accuracy",
                "- Add support for more document formats",
                "- Implement parallel processing"
            ],
            "youtube_transcripts": [
                "- Add subtitle language detection",
                "- Implement transcript caching",
                "- Add timestamp alignment features"
            ],
            "sparta": [
                "- Add distributed training support",
                "- Implement model versioning",
                "- Add experiment tracking"
            ],
            "arangodb": [
                "- Add graph visualization exports",
                "- Implement backup/restore utilities",
                "- Add query optimization tools"
            ],
            "mcp-screenshot": [
                "- Add mobile viewport support",
                "- Implement visual regression testing",
                "- Add accessibility analysis"
            ],
            "claude-module-communicator": [
                "- Add message queuing for reliability",
                "- Implement module health checks",
                "- Add performance monitoring"
            ]
        }
        
        if project_name in suggestions_map:
            improvements.append("\n### Feature Enhancements")
            improvements.extend(suggestions_map[project_name])
        
        # General improvements
        improvements.append("\n### General Improvements")
        improvements.append("- Add comprehensive logging")
        improvements.append("- Implement error recovery mechanisms")
        improvements.append("- Add performance benchmarks")
        
        return '\n'.join(improvements)

    async def _analyze_errors(self, project_path: Path) -> str:
        """Analyze potential errors in implementation"""
        errors = []
        
        # Check for common Python issues
        py_files = list(project_path.rglob("*.py"))[:20]
        
        error_patterns = {
            r'except\s*:': "Bare except clause (catches all exceptions)",
            r'print\s*\(': "Using print instead of logging",
            r'api_key\s*=\s*["\']': "Hardcoded API key",
            r'password\s*=\s*["\']': "Hardcoded password",
            r'TODO|FIXME|XXX|HACK': "Unresolved technical debt"
        }
        
        found_issues = {}
        for py_file in py_files:
            try:
                content = py_file.read_text()
                for pattern, description in error_patterns.items():
                    if re.search(pattern, content, re.IGNORECASE):
                        if description not in found_issues:
                            found_issues[description] = []
                        found_issues[description].append(py_file.name)
            except:
                pass
        
        if found_issues:
            errors.append("### Potential Issues Found")
            for issue, files in found_issues.items():
                errors.append(f"\n**{issue}**")
                for f in files[:3]:
                    errors.append(f"- Found in {f}")
                if len(files) > 3:
                    errors.append(f"- ... and {len(files) - 3} more files")
        
        # Check for missing error handling
        if not any("try" in open(f).read() for f in py_files[:5] if f.exists()):
            errors.append("\n### Error Handling")
            errors.append("- Limited error handling detected")
        
        return '\n'.join(errors) if errors else "No significant errors detected in implementation"

    async def _identify_missing_features(self, project_path: Path, project_name: str) -> str:
        """Identify missing features using domain knowledge"""
        missing = []
        
        # Project-specific missing features
        missing_features_map = {
            "shared_claude_docs": [
                "- Auto-sync documentation to all projects",
                "- Documentation search and indexing",
                "- Project dependency visualization",
                "- Automated API documentation extraction",
                "- Cross-project documentation linking"
            ],
            "arxiv-mcp-server": [
                "- Full-text search within papers",
                "- Citation graph analysis",
                "- Author collaboration networks",
                "- Paper recommendation system"
            ],
            "marker": [
                "- Table extraction to structured data",
                "- Mathematical formula recognition",
                "- Multi-column layout handling",
                "- Image caption extraction"
            ],
            "youtube_transcripts": [
                "- Speaker diarization",
                "- Sentiment analysis",
                "- Key moment detection",
                "- Multi-language support"
            ],
            "sparta": [
                "- AutoML capabilities",
                "- Model interpretability tools",
                "- Federated learning support",
                "- Neural architecture search"
            ],
            "arangodb": [
                "- GraphQL API",
                "- Real-time subscriptions",
                "- Graph algorithms library",
                "- Visual query builder"
            ],
            "mcp-screenshot": [
                "- Video recording",
                "- Network traffic capture",
                "- Performance metrics",
                "- Cross-browser testing"
            ],
            "claude-module-communicator": [
                "- WebSocket support",
                "- Module marketplace",
                "- Visual workflow designer",
                "- Module versioning"
            ],
            "claude-test-reporter": [
                "- Test coverage trends",
                "- Flaky test detection",
                "- Performance regression detection",
                "- Test prioritization"
            ],
            "unsloth_wip": [
                "- Custom optimization strategies",
                "- Memory profiling tools",
                "- Distributed training orchestration",
                "- Model compression techniques"
            ],
            "marker-ground-truth": [
                "- Automated annotation tools",
                "- Inter-annotator agreement metrics",
                "- Active learning integration",
                "- Version control for datasets"
            ],
            "claude_max_proxy": [
                "- Request queuing and prioritization",
                "- Cost optimization strategies",
                "- Multi-model load balancing",
                "- Usage analytics dashboard"
            ]
        }
        
        if project_name in missing_features_map:
            missing.append("### Domain-Specific Features")
            missing.extend(missing_features_map[project_name])
        
        # Check for common missing features
        missing.append("\n### Common Features")
        
        if not (project_path / "Dockerfile").exists():
            missing.append("- Docker containerization")
        
        if not (project_path / ".github" / "workflows").exists():
            missing.append("- GitHub Actions CI/CD")
        
        if not any(f.name.endswith("_test.py") or f.name.startswith("test_") 
                  for f in project_path.rglob("*.py")):
            missing.append("- Automated test suite")
        
        if not (project_path / "docs").exists():
            missing.append("- Comprehensive documentation")
        
        # Suggest using ask-perplexity for research
        missing.append("\n### Research Needed")
        missing.append("- Use `ask-perplexity` to research:")
        missing.append(f"  - Latest best practices for {project_name}")
        missing.append(f"  - Competing solutions to {project_name}")
        missing.append(f"  - Performance optimization techniques for {project_name}")
        
        return '\n'.join(missing)

    def _get_related_projects(self, project_name: str) -> str:
        """Get related projects from the ecosystem"""
        related = []
        
        # Define relationships
        relationships = {
            "shared_claude_docs": ["All projects - Central documentation hub"],
            "arxiv-mcp-server": ["marker", "sparta", "claude-module-communicator"],
            "marker": ["arxiv-mcp-server", "marker-ground-truth", "sparta"],
            "youtube_transcripts": ["sparta", "arangodb"],
            "sparta": ["marker", "youtube_transcripts", "unsloth_wip", "arangodb"],
            "arangodb": ["sparta", "youtube_transcripts", "claude-module-communicator"],
            "mcp-screenshot": ["claude-test-reporter"],
            "claude-module-communicator": ["All projects in the ecosystem"],
            "claude-test-reporter": ["mcp-screenshot", "All projects with tests"],
            "unsloth_wip": ["sparta"],
            "marker-ground-truth": ["marker"],
            "claude_max_proxy": ["claude-module-communicator"]
        }
        
        if project_name in relationships:
            related.append("### Direct Dependencies")
            for rel in relationships[project_name]:
                related.append(f"- {rel}")
        
        # Add ecosystem context
        related.append("\n### Ecosystem Role")
        ecosystem_roles = {
            "shared_claude_docs": "Central documentation and coordination hub for all projects",
            "arxiv-mcp-server": "Research paper discovery and retrieval",
            "marker": "Document parsing and content extraction",
            "youtube_transcripts": "Video content analysis and transcription",
            "sparta": "Scalable machine learning training",
            "arangodb": "Knowledge graph storage and querying",
            "mcp-screenshot": "Web automation and visual testing",
            "claude-module-communicator": "Inter-module communication hub",
            "claude-test-reporter": "Test execution and reporting",
            "unsloth_wip": "LLM optimization and fine-tuning",
            "marker-ground-truth": "Document parsing validation",
            "claude_max_proxy": "Claude API management and optimization"
        }
        
        if project_name in ecosystem_roles:
            related.append(f"- {ecosystem_roles[project_name]}")
        
        return '\n'.join(related)

    async def _get_additional_notes(self, project_path: Path) -> str:
        """Get additional notes about the project"""
        notes = []
        
        # Check for interesting files
        interesting_files = {
            "CHANGELOG.md": "Version history available",
            "CONTRIBUTING.md": "Contribution guidelines present",
            "LICENSE": "License information available",
            "CODE_OF_CONDUCT.md": "Community guidelines defined",
            ".env.example": "Environment configuration template provided"
        }
        
        found_files = []
        for file, description in interesting_files.items():
            if (project_path / file).exists():
                found_files.append(f"- {description} ({file})")
        
        if found_files:
            notes.append("### Project Metadata")
            notes.extend(found_files)
        
        # Check last modification
        try:
            git_dir = project_path / ".git"
            if git_dir.exists():
                # Get last commit date
                result = subprocess.run(
                    ["git", "log", "-1", "--format=%cd", "--date=short"],
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    notes.append(f"\n### Activity")
                    notes.append(f"- Last commit: {result.stdout.strip()}")
        except:
            pass
        
        # Add development status
        notes.append("\n### Development Status")
        if (project_path / "setup.py").exists() or (project_path / "pyproject.toml").exists():
            notes.append("- Packaged for distribution")
        else:
            notes.append("- Development/experimental stage")
        
        return '\n'.join(notes) if notes else "No additional notes"

    async def create_master_index(self):
        """Create a master index of all projects"""
        index_content = """# Big Picture: All Registered Projects

This directory contains comprehensive analyses of all registered projects in the ecosystem.

## Project Index

| Order | Project | Description | Status |
|-------|---------|-------------|--------|
"""
        
        for project in self.projects:
            output_file = self.output_dir / f"{project['order']}_Describe_{project['name']}.md"
            status = "✅ Analyzed" if output_file.exists() else "❌ Missing"
            
            # Get brief description
            description = "Pending analysis"
            if output_file.exists():
                content = output_file.read_text()
                # Extract overview section
                if "## Overview" in content:
                    overview_start = content.find("## Overview") + len("## Overview")
                    overview_end = content.find("\n##", overview_start)
                    if overview_end == -1:
                        overview_end = overview_start + 200
                    description = content[overview_start:overview_end].strip().split('\n')[0][:80] + "..."
            
            index_content += f"| {project['order']} | [{project['name']}](./{project['order']}_Describe_{project['name']}.md) | {description} | {status} |\n"
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        index_content += f"""
## Ecosystem Overview

The registered projects form a comprehensive ecosystem for:

0. **Documentation & Coordination**
   - shared_claude_docs: Central documentation hub and project coordination

1. **Research & Content Extraction**
   - arxiv-mcp-server: Academic paper discovery
   - marker: Document parsing and extraction
   - youtube_transcripts: Video content analysis

2. **Machine Learning & AI**
   - sparta: Scalable training framework
   - unsloth_wip: LLM optimization
   - marker-ground-truth: Validation datasets

3. **Data Management**
   - arangodb: Graph database for knowledge representation
   - claude_max_proxy: API management and optimization

4. **Testing & Automation**
   - mcp-screenshot: Browser automation
   - claude-test-reporter: Test execution and reporting

5. **Integration & Communication**
   - claude-module-communicator: Central hub for all modules

## Analysis Methodology

Each project analysis includes:
- Core capabilities and architecture
- Installation and usage instructions
- Integration points with other projects
- Current limitations and potential improvements
- Missing features and error analysis

## Next Steps

1. Review individual project analyses
2. Identify integration opportunities
3. Prioritize improvements based on ecosystem needs
4. Use ask-perplexity for deeper research on specific topics

---
*Generated: {timestamp}*
"""
        
        index_file = self.output_dir / "000_INDEX.md"
        with open(index_file, 'w') as f:
            f.write(index_content)
        
        print(f"\n📚 Master index created: {index_file.name}")


async def main():
    """Main execution"""
    output_dir = Path("/home/graham/workspace/shared_claude_docs/docs/big_picture")
    
    analyzer = ProjectAnalyzer(output_dir)
    await analyzer.analyze_all_projects()


if __name__ == "__main__":
    asyncio.run(main())