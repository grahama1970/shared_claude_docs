#!/usr/bin/env python3
"""
Enhanced Big Picture Analyzer
Analyzes all registered projects with advanced metrics including:
- Security vulnerability scanning
- Code complexity analysis
- Dependency mapping
- Documentation quality metrics
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import re
import ast
import importlib.util

# Import the base analyzer
from big_picture_analyzer import ProjectAnalyzer

class EnhancedProjectAnalyzer(ProjectAnalyzer):
    """Enhanced analyzer with security, complexity, and quality metrics"""
    
    def __init__(self, output_dir: Path):
        super().__init__(output_dir)
        
        # Add enhanced analysis template sections
        self.enhanced_template = """# {project_name}

## Overview
{overview}

## Core Capabilities
{capabilities}

## Technical Architecture
{architecture}

## Security Analysis
{security_analysis}

## Code Quality Metrics
{code_metrics}

## Dependency Analysis
{dependency_analysis}

## Documentation Quality
{doc_quality}

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

## Git/Version Control Metrics
{git_metrics}

## Overall Health Score
{health_score}

## Notes
{notes}

## Claude Instance Interactions
{claude_interactions}

---
*Generated: {timestamp}*
"""

    async def analyze_project(self, project: Dict[str, str]):
        """Enhanced project analysis"""
        print(f"\n📂 Analyzing {project['name']}...")
        
        project_path = Path(project['path'])
        if not project_path.exists():
            print(f"  ⚠️  Project not found: {project_path}")
            return
        
        # Run base analysis first
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
        
        # Add enhanced analyses
        print("  🔒 Running security analysis...")
        analysis["security_analysis"] = await self._analyze_security(project_path)
        
        print("  📊 Calculating code metrics...")
        analysis["code_metrics"] = await self._analyze_code_metrics(project_path)
        
        print("  🔗 Analyzing dependencies...")
        analysis["dependency_analysis"] = await self._analyze_dependencies_enhanced(project_path)
        
        print("  📚 Evaluating documentation quality...")
        analysis["doc_quality"] = await self._analyze_documentation_quality(project_path)
        
        print("  📈 Gathering Git metrics...")
        analysis["git_metrics"] = await self._analyze_git_metrics(project_path)
        
        print("  🏥 Calculating health score...")
        analysis["health_score"] = await self._calculate_health_score(analysis)
        
        print("  🤖 Generating Claude interactions...")
        analysis["claude_interactions"] = await self._generate_claude_interactions(project_path, project['name'])
        
        # Generate output
        output_content = self.enhanced_template.format(**analysis)
        output_file = self.output_dir / f"{project['order']}_Describe_{project['name']}.md"
        
        with open(output_file, 'w') as f:
            f.write(output_content)
        
        print(f"  ✅ Enhanced analysis saved to: {output_file.name}")

    async def _analyze_security(self, project_path: Path) -> str:
        """Perform security analysis using multiple tools"""
        security_report = []
        
        # Check if it's a Python project
        if not list(project_path.rglob("*.py")):
            return "Not a Python project - security analysis skipped"
        
        # 1. Run pip-audit for dependency vulnerabilities
        security_report.append("### Dependency Vulnerabilities (pip-audit)")
        req_files = list(project_path.glob("requirements*.txt"))
        if req_files:
            for req_file in req_files:
                try:
                    result = subprocess.run(
                        ["pip-audit", "-r", str(req_file), "--format", "json"],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if result.returncode == 0 and result.stdout:
                        vulns = json.loads(result.stdout)
                        if vulns:
                            security_report.append(f"\n**Found {len(vulns)} vulnerabilities in {req_file.name}:**")
                            for vuln in vulns[:5]:  # Show first 5
                                security_report.append(f"- {vuln.get('name', 'Unknown')}: {vuln.get('description', 'No description')}")
                        else:
                            security_report.append(f"✅ No vulnerabilities found in {req_file.name}")
                except Exception as e:
                    security_report.append(f"⚠️  pip-audit not available or failed: {str(e)}")
        else:
            security_report.append("⚠️  No requirements.txt found")
        
        # 2. Run bandit for code security issues
        security_report.append("\n### Code Security Issues (bandit)")
        try:
            result = subprocess.run(
                ["bandit", "-r", str(project_path), "-f", "json", "-ll"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.stdout:
                bandit_results = json.loads(result.stdout)
                issues = bandit_results.get("results", [])
                if issues:
                    security_report.append(f"\n**Found {len(issues)} security issues:**")
                    # Group by severity
                    by_severity = {}
                    for issue in issues:
                        sev = issue.get("issue_severity", "UNKNOWN")
                        if sev not in by_severity:
                            by_severity[sev] = []
                        by_severity[sev].append(issue)
                    
                    for severity, items in sorted(by_severity.items(), reverse=True):
                        security_report.append(f"\n**{severity} ({len(items)} issues)**")
                        for issue in items[:3]:  # Show first 3 of each severity
                            security_report.append(f"- {issue.get('issue_text', 'Unknown issue')} in {Path(issue.get('filename', '')).name}:{issue.get('line_number', '?')}")
                else:
                    security_report.append("✅ No security issues found")
        except Exception as e:
            security_report.append(f"⚠️  bandit not available or failed: {str(e)}")
        
        # 3. Check for hardcoded secrets
        security_report.append("\n### Hardcoded Secrets Check")
        secret_patterns = {
            "API Key": r'api[_-]?key\s*=\s*["\'][\w-]{20,}["\']',
            "AWS Key": r'aws[_-]?access[_-]?key[_-]?id\s*=\s*["\'][A-Z0-9]{20}["\']',
            "Private Key": r'-----BEGIN\s+(?:RSA|DSA|EC|OPENSSH)\s+PRIVATE\s+KEY-----',
            "Password": r'password\s*=\s*["\'][^"\']{8,}["\']'
        }
        
        found_secrets = []
        py_files = list(project_path.rglob("*.py"))[:20]  # Check first 20 files
        for py_file in py_files:
            try:
                content = py_file.read_text()
                for secret_type, pattern in secret_patterns.items():
                    if re.search(pattern, content, re.IGNORECASE):
                        found_secrets.append(f"- Potential {secret_type} in {py_file.name}")
            except:
                pass
        
        if found_secrets:
            security_report.append(f"⚠️  Found {len(found_secrets)} potential secrets:")
            security_report.extend(found_secrets[:5])
        else:
            security_report.append("✅ No hardcoded secrets detected")
        
        return '\n'.join(security_report)

    async def _analyze_code_metrics(self, project_path: Path) -> str:
        """Calculate code complexity metrics"""
        metrics_report = []
        
        # Try to use radon for complexity metrics
        try:
            # Cyclomatic Complexity
            result = subprocess.run(
                ["radon", "cc", str(project_path), "-s", "-j"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout:
                cc_data = json.loads(result.stdout)
                
                # Calculate statistics
                total_complexity = 0
                total_functions = 0
                complex_functions = []
                
                for file_path, items in cc_data.items():
                    for item in items:
                        if item['type'] in ['method', 'function']:
                            total_functions += 1
                            complexity = item['complexity']
                            total_complexity += complexity
                            if complexity > 10:  # Complex functions
                                complex_functions.append({
                                    'name': item['name'],
                                    'file': Path(file_path).name,
                                    'complexity': complexity
                                })
                
                metrics_report.append("### Cyclomatic Complexity")
                if total_functions > 0:
                    avg_complexity = total_complexity / total_functions
                    metrics_report.append(f"- Average complexity: {avg_complexity:.2f}")
                    metrics_report.append(f"- Total functions analyzed: {total_functions}")
                    
                    if complex_functions:
                        metrics_report.append(f"\n**Most complex functions ({len(complex_functions)} with CC > 10):**")
                        for func in sorted(complex_functions, key=lambda x: x['complexity'], reverse=True)[:5]:
                            metrics_report.append(f"- {func['name']} in {func['file']}: CC = {func['complexity']}")
                else:
                    metrics_report.append("- No functions found to analyze")
            
            # Maintainability Index
            result = subprocess.run(
                ["radon", "mi", str(project_path), "-s", "-j"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout:
                mi_data = json.loads(result.stdout)
                
                metrics_report.append("\n### Maintainability Index")
                mi_scores = []
                low_mi_files = []
                
                for file_path, score in mi_data.items():
                    mi_scores.append(score['mi'])
                    if score['mi'] < 65:  # Hard to maintain
                        low_mi_files.append({
                            'file': Path(file_path).name,
                            'score': score['mi'],
                            'rank': score['rank']
                        })
                
                if mi_scores:
                    avg_mi = sum(mi_scores) / len(mi_scores)
                    metrics_report.append(f"- Average MI: {avg_mi:.1f} ({self._get_mi_rating(avg_mi)})")
                    metrics_report.append(f"- Files analyzed: {len(mi_scores)}")
                    
                    if low_mi_files:
                        metrics_report.append(f"\n**Files needing refactoring ({len(low_mi_files)} with MI < 65):**")
                        for file in sorted(low_mi_files, key=lambda x: x['score'])[:5]:
                            metrics_report.append(f"- {file['file']}: MI = {file['score']:.1f} (Rank: {file['rank']})")
            
            # Raw metrics
            result = subprocess.run(
                ["radon", "raw", str(project_path), "-s", "-j"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout:
                raw_data = json.loads(result.stdout)
                
                total_loc = 0
                total_sloc = 0
                total_comments = 0
                
                for file_path, metrics in raw_data.items():
                    total_loc += metrics['loc']
                    total_sloc += metrics['sloc']
                    total_comments += metrics['comments']
                
                metrics_report.append("\n### Code Volume Metrics")
                metrics_report.append(f"- Total Lines of Code (LOC): {total_loc:,}")
                metrics_report.append(f"- Source Lines of Code (SLOC): {total_sloc:,}")
                metrics_report.append(f"- Comment Lines: {total_comments:,}")
                if total_sloc > 0:
                    comment_ratio = (total_comments / total_sloc) * 100
                    metrics_report.append(f"- Comment Ratio: {comment_ratio:.1f}%")
                
        except Exception as e:
            metrics_report.append(f"⚠️  radon not available: {str(e)}")
            metrics_report.append("\nInstall with: pip install radon")
        
        # Fallback: Basic metrics using AST
        if not metrics_report or "not available" in '\n'.join(metrics_report):
            metrics_report.append("\n### Basic Code Metrics (Fallback)")
            
            classes = 0
            functions = 0
            total_lines = 0
            
            py_files = list(project_path.rglob("*.py"))
            for py_file in py_files:
                try:
                    content = py_file.read_text()
                    total_lines += len(content.splitlines())
                    
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            classes += 1
                        elif isinstance(node, ast.FunctionDef):
                            functions += 1
                except:
                    pass
            
            metrics_report.append(f"- Total Python files: {len(py_files)}")
            metrics_report.append(f"- Total lines: {total_lines:,}")
            metrics_report.append(f"- Total classes: {classes}")
            metrics_report.append(f"- Total functions: {functions}")
        
        return '\n'.join(metrics_report)

    def _get_mi_rating(self, mi_score: float) -> str:
        """Get maintainability rating based on MI score"""
        if mi_score >= 85:
            return "Highly Maintainable ✅"
        elif mi_score >= 65:
            return "Moderately Maintainable ⚠️"
        else:
            return "Hard to Maintain ❌"

    async def _analyze_dependencies_enhanced(self, project_path: Path) -> str:
        """Enhanced dependency analysis with vulnerability checking"""
        dep_report = []
        
        # Check for Python dependencies
        req_files = list(project_path.glob("requirements*.txt"))
        if req_files:
            dep_report.append("### Python Dependencies Analysis")
            
            for req_file in req_files:
                try:
                    content = req_file.read_text()
                    deps = [line.strip() for line in content.splitlines() 
                           if line.strip() and not line.startswith('#')]
                    
                    dep_report.append(f"\n**{req_file.name} ({len(deps)} dependencies)**")
                    
                    # Categorize dependencies
                    categories = {
                        "Web Frameworks": ["flask", "django", "fastapi", "aiohttp"],
                        "ML/AI": ["torch", "tensorflow", "scikit-learn", "numpy", "pandas"],
                        "Testing": ["pytest", "unittest", "nose", "tox"],
                        "Documentation": ["sphinx", "mkdocs", "pdoc"],
                        "Security": ["cryptography", "pyjwt", "bcrypt"],
                        "Database": ["sqlalchemy", "pymongo", "redis", "psycopg"],
                        "CLI": ["click", "typer", "argparse"],
                        "Async": ["asyncio", "aiofiles", "httpx"]
                    }
                    
                    categorized = {}
                    for dep in deps:
                        dep_name = dep.split('==')[0].split('>=')[0].split('<')[0].lower()
                        for category, keywords in categories.items():
                            if any(keyword in dep_name for keyword in keywords):
                                if category not in categorized:
                                    categorized[category] = []
                                categorized[category].append(dep)
                                break
                    
                    if categorized:
                        for category, items in sorted(categorized.items()):
                            dep_report.append(f"\n{category}:")
                            for item in items:
                                dep_report.append(f"  - {item}")
                    
                    # Check for outdated dependencies
                    try:
                        result = subprocess.run(
                            ["pip", "list", "--outdated", "--format", "json"],
                            capture_output=True,
                            text=True,
                            cwd=project_path,
                            timeout=30
                        )
                        
                        if result.returncode == 0 and result.stdout:
                            outdated = json.loads(result.stdout)
                            project_deps = {d.split('==')[0].lower() for d in deps if '==' in d}
                            
                            outdated_project_deps = [
                                pkg for pkg in outdated 
                                if pkg['name'].lower() in project_deps
                            ]
                            
                            if outdated_project_deps:
                                dep_report.append(f"\n**⚠️  Outdated Dependencies ({len(outdated_project_deps)}):**")
                                for pkg in outdated_project_deps[:5]:
                                    dep_report.append(f"- {pkg['name']}: {pkg['version']} → {pkg['latest_version']}")
                    except:
                        pass
                    
                except Exception as e:
                    dep_report.append(f"Error reading {req_file.name}: {str(e)}")
        
        # Check for package.json (Node.js)
        package_json = project_path / "package.json"
        if package_json.exists():
            dep_report.append("\n### Node.js Dependencies")
            try:
                data = json.loads(package_json.read_text())
                deps = data.get('dependencies', {})
                dev_deps = data.get('devDependencies', {})
                
                dep_report.append(f"- Production dependencies: {len(deps)}")
                dep_report.append(f"- Development dependencies: {len(dev_deps)}")
            except:
                dep_report.append("- Error reading package.json")
        
        # Dependency tree visualization (simplified)
        dep_report.append("\n### Dependency Relationships")
        dep_report.append("```mermaid")
        dep_report.append("graph TD")
        dep_report.append(f"    {project_path.name}[{project_path.name}]")
        
        # Add first level deps
        if req_files:
            for req_file in req_files[:1]:  # Just show first requirements file
                try:
                    content = req_file.read_text()
                    deps = [line.strip().split('==')[0].split('>=')[0] 
                           for line in content.splitlines() 
                           if line.strip() and not line.startswith('#')][:5]  # Show first 5
                    
                    for i, dep in enumerate(deps):
                        dep_report.append(f"    {project_path.name} --> {dep}")
                except:
                    pass
        
        dep_report.append("```")
        
        return '\n'.join(dep_report) if dep_report else "No dependency analysis available"

    async def _analyze_documentation_quality(self, project_path: Path) -> str:
        """Analyze documentation quality and coverage"""
        doc_report = []
        
        # Check README
        doc_report.append("### README Analysis")
        readme_files = ["README.md", "README.rst", "README.txt", "readme.md"]
        readme_found = False
        
        for readme_name in readme_files:
            readme_path = project_path / readme_name
            if readme_path.exists():
                readme_found = True
                content = readme_path.read_text()
                
                # Check for essential sections
                sections = {
                    "Installation": ["install", "setup", "getting started"],
                    "Usage": ["usage", "example", "how to use"],
                    "API Documentation": ["api", "reference", "methods"],
                    "Contributing": ["contribut", "development", "pull request"],
                    "License": ["license", "copyright"],
                    "Requirements": ["requirement", "dependencies", "prerequisite"],
                    "Testing": ["test", "pytest", "unittest"],
                    "Badges": ["![", "shield", "badge"]
                }
                
                found_sections = []
                missing_sections = []
                
                content_lower = content.lower()
                for section, keywords in sections.items():
                    if any(keyword in content_lower for keyword in keywords):
                        found_sections.append(section)
                    else:
                        missing_sections.append(section)
                
                doc_report.append(f"✅ README found: {readme_name}")
                doc_report.append(f"- Length: {len(content)} characters")
                doc_report.append(f"- Sections present: {', '.join(found_sections)}")
                if missing_sections:
                    doc_report.append(f"- Missing sections: {', '.join(missing_sections)}")
                
                # Calculate completeness score
                completeness = (len(found_sections) / len(sections)) * 100
                doc_report.append(f"- Completeness score: {completeness:.0f}%")
                break
        
        if not readme_found:
            doc_report.append("❌ No README file found")
        
        # Check docstring coverage
        doc_report.append("\n### Docstring Coverage")
        
        total_functions = 0
        documented_functions = 0
        total_classes = 0
        documented_classes = 0
        
        py_files = list(project_path.rglob("*.py"))[:20]  # Sample first 20 files
        for py_file in py_files:
            try:
                content = py_file.read_text()
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        total_functions += 1
                        if ast.get_docstring(node):
                            documented_functions += 1
                    elif isinstance(node, ast.ClassDef):
                        total_classes += 1
                        if ast.get_docstring(node):
                            documented_classes += 1
            except:
                pass
        
        if total_functions > 0:
            func_coverage = (documented_functions / total_functions) * 100
            doc_report.append(f"- Function docstring coverage: {func_coverage:.0f}% ({documented_functions}/{total_functions})")
        
        if total_classes > 0:
            class_coverage = (documented_classes / total_classes) * 100
            doc_report.append(f"- Class docstring coverage: {class_coverage:.0f}% ({documented_classes}/{total_classes})")
        
        # Check for additional documentation
        doc_report.append("\n### Additional Documentation")
        
        doc_dirs = ["docs", "doc", "documentation"]
        for doc_dir in doc_dirs:
            doc_path = project_path / doc_dir
            if doc_path.exists() and doc_path.is_dir():
                doc_files = list(doc_path.rglob("*.md")) + list(doc_path.rglob("*.rst"))
                if doc_files:
                    doc_report.append(f"✅ Documentation directory found: {doc_dir}/")
                    doc_report.append(f"  - Contains {len(doc_files)} documentation files")
                    # Show first few files
                    for doc_file in doc_files[:3]:
                        doc_report.append(f"  - {doc_file.relative_to(project_path)}")
                break
        
        # Check for inline code examples
        example_dirs = ["examples", "example", "demos", "samples"]
        for example_dir in example_dirs:
            example_path = project_path / example_dir
            if example_path.exists() and example_path.is_dir():
                example_files = list(example_path.rglob("*.py"))
                if example_files:
                    doc_report.append(f"\n✅ Examples directory found: {example_dir}/")
                    doc_report.append(f"  - Contains {len(example_files)} example scripts")
                break
        
        return '\n'.join(doc_report)

    async def _analyze_git_metrics(self, project_path: Path) -> str:
        """Analyze git repository metrics"""
        git_report = []
        
        git_dir = project_path / ".git"
        if not git_dir.exists():
            return "Not a git repository"
        
        try:
            # Get commit count
            result = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                commit_count = result.stdout.strip()
                git_report.append(f"### Repository Statistics")
                git_report.append(f"- Total commits: {commit_count}")
            
            # Get contributors
            result = subprocess.run(
                ["git", "shortlog", "-sn", "HEAD"],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                contributors = result.stdout.strip().splitlines()
                git_report.append(f"- Contributors: {len(contributors)}")
                if contributors:
                    git_report.append("\n**Top contributors:**")
                    for contributor in contributors[:3]:
                        git_report.append(f"  {contributor}")
            
            # Get last commit date
            result = subprocess.run(
                ["git", "log", "-1", "--format=%cd", "--date=relative"],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                last_commit = result.stdout.strip()
                git_report.append(f"\n- Last commit: {last_commit}")
            
            # Get file count
            result = subprocess.run(
                ["git", "ls-files"],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                file_count = len(result.stdout.strip().splitlines())
                git_report.append(f"- Files tracked: {file_count}")
            
            # Get branch info
            result = subprocess.run(
                ["git", "branch", "-r"],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                branches = [b.strip() for b in result.stdout.strip().splitlines()]
                git_report.append(f"- Remote branches: {len(branches)}")
            
            # Code churn (files changed in last 30 days)
            result = subprocess.run(
                ["git", "log", "--since=30.days", "--name-only", "--pretty=format:"],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                changed_files = set(f for f in result.stdout.strip().splitlines() if f)
                git_report.append(f"\n### Recent Activity (last 30 days)")
                git_report.append(f"- Files changed: {len(changed_files)}")
                
                # Most changed files
                result = subprocess.run(
                    ["git", "log", "--since=30.days", "--name-only", "--pretty=format:", "--", "*.py"],
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    file_changes = {}
                    for f in result.stdout.strip().splitlines():
                        if f:
                            file_changes[f] = file_changes.get(f, 0) + 1
                    
                    if file_changes:
                        git_report.append("\n**Most frequently changed Python files:**")
                        for f, count in sorted(file_changes.items(), key=lambda x: x[1], reverse=True)[:5]:
                            git_report.append(f"  - {f}: {count} changes")
            
        except Exception as e:
            git_report.append(f"Error analyzing git metrics: {str(e)}")
        
        return '\n'.join(git_report)

    async def _calculate_health_score(self, analysis: Dict[str, Any]) -> str:
        """Calculate overall project health score"""
        health_report = []
        scores = {}
        
        # Security score (0-100)
        security_text = analysis.get('security_analysis', '')
        if 'No vulnerabilities found' in security_text and 'No security issues found' in security_text:
            scores['security'] = 100
        elif 'vulnerabilities' in security_text or 'security issues' in security_text:
            # Count issues
            vuln_count = len(re.findall(r'Found \d+ vulnerabilities', security_text))
            issue_count = len(re.findall(r'Found \d+ security issues', security_text))
            scores['security'] = max(0, 100 - (vuln_count * 20) - (issue_count * 10))
        else:
            scores['security'] = 50  # Unknown
        
        # Code quality score (0-100)
        metrics_text = analysis.get('code_metrics', '')
        if 'Average complexity:' in metrics_text:
            match = re.search(r'Average complexity: ([\d.]+)', metrics_text)
            if match:
                avg_complexity = float(match.group(1))
                # Score based on complexity (lower is better)
                scores['code_quality'] = max(0, 100 - (avg_complexity * 5))
        else:
            scores['code_quality'] = 50
        
        # Maintainability score
        if 'Average MI:' in metrics_text:
            match = re.search(r'Average MI: ([\d.]+)', metrics_text)
            if match:
                mi_score = float(match.group(1))
                scores['maintainability'] = min(100, mi_score)
        else:
            scores['maintainability'] = 50
        
        # Documentation score (0-100)
        doc_text = analysis.get('doc_quality', '')
        doc_score = 0
        if 'README found' in doc_text:
            doc_score += 30
        if 'Completeness score:' in doc_text:
            match = re.search(r'Completeness score: (\d+)%', doc_text)
            if match:
                doc_score += int(match.group(1)) * 0.4
        if 'Documentation directory found' in doc_text:
            doc_score += 20
        if 'Examples directory found' in doc_text:
            doc_score += 10
        scores['documentation'] = min(100, doc_score)
        
        # Test coverage (check if tests exist)
        if (Path(analysis.get('project_path', '')) / 'tests').exists():
            scores['testing'] = 70  # Base score for having tests
        else:
            scores['testing'] = 0
        
        # Activity score (based on git metrics)
        git_text = analysis.get('git_metrics', '')
        if 'Last commit:' in git_text:
            if any(time in git_text for time in ['hours ago', 'days ago', 'week ago']):
                scores['activity'] = 100
            elif 'month' in git_text:
                scores['activity'] = 70
            else:
                scores['activity'] = 40
        else:
            scores['activity'] = 0
        
        # Calculate overall health score
        weights = {
            'security': 0.25,
            'code_quality': 0.20,
            'maintainability': 0.20,
            'documentation': 0.15,
            'testing': 0.15,
            'activity': 0.05
        }
        
        overall_score = sum(scores.get(metric, 0) * weight for metric, weight in weights.items())
        
        # Generate report
        health_report.append(f"### Overall Health Score: {overall_score:.0f}/100 {self._get_health_emoji(overall_score)}")
        health_report.append("\n**Component Scores:**")
        
        for metric, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            emoji = self._get_health_emoji(score)
            weight_pct = weights.get(metric, 0) * 100
            health_report.append(f"- {metric.replace('_', ' ').title()}: {score:.0f}/100 {emoji} (weight: {weight_pct:.0f}%)")
        
        # Recommendations
        health_report.append("\n**Health Recommendations:**")
        
        if scores.get('security', 0) < 80:
            health_report.append("- 🔒 **Priority**: Address security vulnerabilities immediately")
        
        if scores.get('code_quality', 0) < 70:
            health_report.append("- 📊 Refactor complex functions to reduce cyclomatic complexity")
        
        if scores.get('documentation', 0) < 60:
            health_report.append("- 📚 Improve documentation coverage and README completeness")
        
        if scores.get('testing', 0) < 50:
            health_report.append("- 🧪 Add comprehensive test suite with >80% coverage")
        
        if scores.get('activity', 0) < 50:
            health_report.append("- 📈 Project appears inactive - consider archiving or updating")
        
        return '\n'.join(health_report)

    def _get_health_emoji(self, score: float) -> str:
        """Get emoji based on health score"""
        if score >= 90:
            return "🟢"
        elif score >= 70:
            return "🟡"
        elif score >= 50:
            return "🟠"
        else:
            return "🔴"

    async def _generate_claude_interactions(self, project_path: Path, project_name: str) -> str:
        """Generate creative Claude instance interactions for testing module collaboration"""
        from datetime import datetime
        import random
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        interactions = []
        
        # Project-specific creative interaction scenarios
        # Enhanced with Gemini's stress-testing scenarios
        interaction_templates = {
            "arxiv-mcp-server": [
                {
                    "scenario": "Research Paper Analysis Pipeline",
                    "description": "Search for papers on quantum computing, extract with Marker, analyze with Sparta",
                    "interactions": [
                        "1. Use arxiv-mcp-server to search for 'quantum error correction 2024'",
                        "2. Pass the top 3 paper PDFs to marker for extraction",
                        "3. Send extracted text to youtube_transcripts to find related video content",
                        "4. Use sparta to train a model on the combined knowledge",
                        "5. Store the knowledge graph in arangodb",
                        "6. Generate a visual report with mcp-screenshot"
                    ]
                },
                {
                    "scenario": "Academic Trend Analysis",
                    "description": "Track emerging research trends across multiple domains",
                    "interactions": [
                        "1. Query arxiv-mcp-server for papers in 5 different AI subfields",
                        "2. Use marker to extract abstracts and conclusions",
                        "3. Apply sparta for topic modeling and trend detection",
                        "4. Visualize trend connections in arangodb graph",
                        "5. Test the trend prediction model with claude-test-reporter"
                    ]
                }
            ],
            "marker": [
                {
                    "scenario": "Multi-Format Document Intelligence",
                    "description": "Process diverse document types and create unified knowledge base",
                    "interactions": [
                        "1. Use marker to extract content from PDF research papers",
                        "2. Process the same topics from youtube_transcripts",
                        "3. Compare and merge findings using sparta's NLP capabilities",
                        "4. Validate extraction accuracy with marker-ground-truth",
                        "5. Create a searchable index in arangodb"
                    ]
                },
                {
                    "scenario": "Automated Documentation Generation",
                    "description": "Extract code and generate documentation across projects",
                    "interactions": [
                        "1. Use marker to parse existing PDF documentation",
                        "2. Extract code examples and validate with claude-test-reporter",
                        "3. Generate improved docs using claude-module-communicator",
                        "4. Screenshot the generated docs with mcp-screenshot",
                        "5. Store versioned docs in shared_claude_docs"
                    ]
                },
                {
                    "scenario": "Document Integrity Stress Test",
                    "description": "Test marker's handling of corrupted and edge-case documents",
                    "interactions": [
                        "1. Test marker.check_document_integrity() with corrupted PDFs",
                        "2. Process very large PDFs (>1000 pages) to test memory limits",
                        "3. Extract from multi-language documents to test unicode handling",
                        "4. Handle password-protected PDFs to test error propagation",
                        "5. Validate all error messages with claude-test-reporter"
                    ]
                }
            ],
            "youtube_transcripts": [
                {
                    "scenario": "Educational Content Synthesis",
                    "description": "Create comprehensive learning materials from video content",
                    "interactions": [
                        "1. Extract transcripts from ML tutorial playlists",
                        "2. Cross-reference concepts with arxiv papers via arxiv-mcp-server",
                        "3. Use marker to extract diagrams from paper PDFs",
                        "4. Train a Q&A model with sparta on the combined content",
                        "5. Test the model's accuracy with claude-test-reporter"
                    ]
                },
                {
                    "scenario": "Real-time Knowledge Updates",
                    "description": "Monitor YouTube for breaking AI news and research",
                    "interactions": [
                        "1. Monitor specific YouTube channels for new AI content",
                        "2. Extract and analyze transcripts in real-time",
                        "3. Cross-reference claims with arxiv-mcp-server papers",
                        "4. Update knowledge graph in arangodb",
                        "5. Generate daily briefings with mcp-screenshot"
                    ]
                }
            ],
            "sparta": [
                {
                    "scenario": "Distributed Model Training Orchestra",
                    "description": "Coordinate training across multiple data sources",
                    "interactions": [
                        "1. Gather training data from marker-processed documents",
                        "2. Augment with youtube_transcripts educational content",
                        "3. Use sparta to orchestrate distributed training",
                        "4. Optimize with unsloth_wip techniques",
                        "5. Monitor training progress via claude-test-reporter",
                        "6. Visualize results with mcp-screenshot"
                    ]
                },
                {
                    "scenario": "AutoML Pipeline",
                    "description": "Automated model selection and hyperparameter tuning",
                    "interactions": [
                        "1. Define problem using natural language via claude-module-communicator",
                        "2. Sparta analyzes data characteristics",
                        "3. Automatically selects models and tunes hyperparameters",
                        "4. Validates results with claude-test-reporter",
                        "5. Stores experiment history in arangodb"
                    ]
                }
            ],
            "arangodb": [
                {
                    "scenario": "Knowledge Graph Evolution",
                    "description": "Build and evolve a comprehensive knowledge graph",
                    "interactions": [
                        "1. Ingest entities from arxiv papers via marker",
                        "2. Add relationships from youtube_transcripts analysis",
                        "3. Use sparta to predict missing links",
                        "4. Visualize graph evolution with mcp-screenshot",
                        "5. Query graph via claude-module-communicator natural language"
                    ]
                },
                {
                    "scenario": "Semantic Search Engine",
                    "description": "Build a multi-modal semantic search system",
                    "interactions": [
                        "1. Index paper content from marker extractions",
                        "2. Add video transcripts from youtube_transcripts",
                        "3. Create embeddings with sparta models",
                        "4. Store in arangodb with vector indices",
                        "5. Test search accuracy with claude-test-reporter"
                    ]
                }
            ],
            "mcp-screenshot": [
                {
                    "scenario": "Visual Testing Automation",
                    "description": "Automated UI testing with visual regression detection",
                    "interactions": [
                        "1. Capture baseline screenshots of all project UIs",
                        "2. Use sparta to detect visual anomalies",
                        "3. Generate test reports with claude-test-reporter",
                        "4. Store visual history in arangodb",
                        "5. Create visual diff reports via claude-module-communicator"
                    ]
                },
                {
                    "scenario": "Documentation Screenshot Pipeline",
                    "description": "Auto-generate visual documentation",
                    "interactions": [
                        "1. Screenshot all project interfaces with mcp-screenshot",
                        "2. Use sparta for OCR and element detection",
                        "3. Generate captions using youtube_transcripts style",
                        "4. Create interactive docs in shared_claude_docs",
                        "5. Validate screenshots with marker-ground-truth"
                    ]
                }
            ],
            "claude-module-communicator": [
                {
                    "scenario": "Natural Language Orchestration",
                    "description": "Control entire ecosystem with conversational commands",
                    "interactions": [
                        "1. User: 'Find recent papers on transformers and create a summary'",
                        "2. Communicator routes to arxiv-mcp-server for search",
                        "3. Automatically sends PDFs to marker for extraction",
                        "4. Uses sparta to generate summaries",
                        "5. Stores in arangodb and returns formatted response"
                    ]
                },
                {
                    "scenario": "Adaptive Workflow Creation",
                    "description": "Dynamically create workflows based on task requirements",
                    "interactions": [
                        "1. Analyze user request with NLP",
                        "2. Determine required modules and sequence",
                        "3. Negotiate data formats between modules",
                        "4. Execute workflow with error handling",
                        "5. Learn from execution for future optimization"
                    ]
                }
            ],
            "claude-test-reporter": [
                {
                    "scenario": "Cross-Project Test Orchestration",
                    "description": "Coordinate testing across all modules",
                    "interactions": [
                        "1. Trigger test suites across all projects",
                        "2. Collect and normalize test results",
                        "3. Use sparta to identify test patterns and flaky tests",
                        "4. Generate visual test reports with mcp-screenshot",
                        "5. Store test history in arangodb for trend analysis"
                    ]
                },
                {
                    "scenario": "Intelligent Test Generation",
                    "description": "Generate tests based on code analysis",
                    "interactions": [
                        "1. Analyze code changes across projects",
                        "2. Use sparta to predict high-risk areas",
                        "3. Generate targeted test cases",
                        "4. Execute and validate with existing test suites",
                        "5. Report coverage gaps via claude-module-communicator"
                    ]
                }
            ],
            "unsloth_wip": [
                {
                    "scenario": "LLM Fine-tuning Pipeline",
                    "description": "Optimize LLMs for specific domains",
                    "interactions": [
                        "1. Gather domain data from arxiv papers via marker",
                        "2. Augment with youtube_transcripts educational content",
                        "3. Use unsloth_wip for efficient fine-tuning",
                        "4. Validate with claude-test-reporter benchmarks",
                        "5. Deploy via claude_max_proxy for inference"
                    ]
                },
                {
                    "scenario": "Model Compression Orchestra",
                    "description": "Compress models while maintaining performance",
                    "interactions": [
                        "1. Load pre-trained models from sparta",
                        "2. Apply unsloth_wip quantization techniques",
                        "3. Test compressed models with claude-test-reporter",
                        "4. Compare performance metrics in arangodb",
                        "5. Generate optimization reports"
                    ]
                }
            ],
            "marker-ground-truth": [
                {
                    "scenario": "Extraction Accuracy Evolution",
                    "description": "Continuously improve extraction accuracy",
                    "interactions": [
                        "1. Compare marker extractions with ground truth",
                        "2. Use sparta to identify error patterns",
                        "3. Generate corrected training data",
                        "4. Retrain marker models",
                        "5. Track accuracy improvements in arangodb"
                    ]
                },
                {
                    "scenario": "Multi-Modal Validation",
                    "description": "Validate extractions across different media types",
                    "interactions": [
                        "1. Extract same content from PDFs and videos",
                        "2. Compare marker and youtube_transcripts outputs",
                        "3. Use ground truth to identify best extraction method",
                        "4. Create unified extraction pipeline",
                        "5. Report accuracy via claude-test-reporter"
                    ]
                }
            ],
            "claude_max_proxy": [
                {
                    "scenario": "Intelligent Request Routing",
                    "description": "Optimize API usage across multiple Claude instances",
                    "interactions": [
                        "1. Monitor request patterns from all modules",
                        "2. Use sparta to predict request volumes",
                        "3. Dynamically route to optimal Claude instances",
                        "4. Cache common responses in arangodb",
                        "5. Report cost savings via claude-module-communicator"
                    ]
                },
                {
                    "scenario": "Collaborative AI Ensemble",
                    "description": "Coordinate multiple AI models for complex tasks",
                    "interactions": [
                        "1. Receive complex query via claude-module-communicator",
                        "2. Decompose into sub-tasks for different models",
                        "3. Route through claude_max_proxy for parallel processing",
                        "4. Aggregate responses using sparta",
                        "5. Return unified answer with confidence scores"
                    ]
                }
            ],
            "shared_claude_docs": [
                {
                    "scenario": "Living Documentation System",
                    "description": "Auto-update documentation based on code changes",
                    "interactions": [
                        "1. Monitor all projects for code changes",
                        "2. Use marker to extract docstrings and comments",
                        "3. Generate updated docs with claude-module-communicator",
                        "4. Validate examples with claude-test-reporter",
                        "5. Screenshot and publish via mcp-screenshot"
                    ]
                },
                {
                    "scenario": "Cross-Project Knowledge Transfer",
                    "description": "Share learnings and patterns across projects",
                    "interactions": [
                        "1. Analyze patterns in all project codebases",
                        "2. Identify common solutions and anti-patterns",
                        "3. Generate best practices documentation",
                        "4. Create project-specific implementation guides",
                        "5. Track adoption via git metrics"
                    ]
                }
            ]
        }
        
        # Get scenarios for this project
        project_scenarios = interaction_templates.get(project_name, [])
        
        if not project_scenarios:
            # Generate generic scenarios for unknown projects
            project_scenarios = [{
                "scenario": "Generic Integration Test",
                "description": f"Test {project_name} integration with other modules",
                "interactions": [
                    f"1. Initialize {project_name} with test configuration",
                    "2. Send test data through claude-module-communicator",
                    "3. Verify output format and correctness",
                    "4. Test error handling and edge cases",
                    "5. Generate test report with claude-test-reporter"
                ]
            }]
        
        # Select a random scenario (different each run)
        scenario = random.choice(project_scenarios)
        
        # Generate the interaction script
        interactions.append(f"### Test Scenario: {scenario['scenario']}")
        interactions.append(f"\n**Description**: {scenario['description']}")
        interactions.append(f"\n**Generated**: {timestamp}")
        interactions.append("\n**Interaction Steps**:")
        
        for step in scenario['interactions']:
            interactions.append(f"{step}")
        
        # Generate test file
        test_dir = self.output_dir / "claude_interaction_tests"
        test_dir.mkdir(exist_ok=True)
        
        test_filename = f"{project_name}_interaction_{timestamp}.py"
        test_file = test_dir / test_filename
        
        # Generate Python test script
        test_content = f'''#!/usr/bin/env python3
"""
Claude Instance Interaction Test for {project_name}
Scenario: {scenario['scenario']}
Generated: {timestamp}
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime

class {project_name.replace('-', '_').replace('_', '').title()}InteractionTest:
    """Test {scenario['scenario']}"""
    
    def __init__(self):
        self.project_name = "{project_name}"
        self.scenario = "{scenario['scenario']}"
        self.start_time = datetime.now()
        self.results = []
    
    async def run_test(self):
        """Execute the interaction scenario"""
        print(f"🧪 Running interaction test: {{self.scenario}}")
        print("=" * 60)
        
        # Test steps
'''
        
        for i, step in enumerate(scenario['interactions'], 1):
            test_content += f'''
        # Step {i}: {step}
        print(f"\\n📍 Step {i}: {step}")
        result = await self.execute_step_{i}()
        self.results.append({{
            "step": {i},
            "description": "{step}",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }})
'''
        
        test_content += '''
        
        # Generate report
        self.generate_report()
        
        return self.results
'''
        
        # Add step implementations
        for i in range(1, len(scenario['interactions']) + 1):
            test_content += f'''
    
    async def execute_step_{i}(self):
        """Execute step {i} of the scenario"""
        # TODO: Implement actual interaction with modules
        await asyncio.sleep(0.5)  # Simulate work
        
        # Mock result for now
        return {{
            "status": "success",
            "data": f"Step {i} completed successfully",
            "module": "{project_name}"
        }}
'''
        
        test_content += '''
    
    def generate_report(self):
        """Generate test execution report"""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        report = {
            "project": self.project_name,
            "scenario": self.scenario,
            "duration": duration,
            "results": self.results,
            "summary": {
                "total_steps": len(self.results),
                "successful": sum(1 for r in self.results if r["result"]["status"] == "success"),
                "failed": sum(1 for r in self.results if r["result"]["status"] == "failed")
            }
        }
        
        # Save report
        report_file = Path(f"./reports/{self.project_name}_interaction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\\n📊 Report saved to: {report_file}")
        
        # Print summary
        print(f"\\n✨ Test Summary:")
        print(f"  - Total steps: {report['summary']['total_steps']}")
        print(f"  - Successful: {report['summary']['successful']}")
        print(f"  - Failed: {report['summary']['failed']}")
        print(f"  - Duration: {duration:.2f} seconds")


async def main():
    """Run the interaction test"""
    test = {project_name.replace('-', '_').replace('_', '').title()}InteractionTest()
    await test.run_test()


if __name__ == "__main__":
    asyncio.run(main())
'''
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        # Make executable
        test_file.chmod(0o755)
        
        interactions.append(f"\n**Generated Test Script**: `{test_file.relative_to(self.output_dir)}`")
        
        # Add execution instructions
        interactions.append("\n### Running the Interaction Test")
        interactions.append("```bash")
        interactions.append(f"cd {self.output_dir}")
        interactions.append(f"python3 {test_file.relative_to(self.output_dir)}")
        interactions.append("```")
        
        # Add inter-module collaboration notes
        interactions.append("\n### Inter-Module Collaboration")
        
        # Define module relationships
        collaborations = {
            "arxiv-mcp-server": ["marker", "sparta", "arangodb"],
            "marker": ["arxiv-mcp-server", "sparta", "marker-ground-truth"],
            "youtube_transcripts": ["sparta", "arangodb", "marker"],
            "sparta": ["all modules for ML training"],
            "arangodb": ["all modules for data storage"],
            "mcp-screenshot": ["claude-test-reporter", "shared_claude_docs"],
            "claude-module-communicator": ["all modules as central hub"],
            "claude-test-reporter": ["all modules for testing"],
            "unsloth_wip": ["sparta", "claude_max_proxy"],
            "marker-ground-truth": ["marker", "claude-test-reporter"],
            "claude_max_proxy": ["all Claude-facing modules"],
            "shared_claude_docs": ["all modules for documentation"]
        }
        
        if project_name in collaborations:
            interactions.append(f"\n**Primary Collaborators**:")
            for collab in collaborations[project_name]:
                interactions.append(f"- {collab}")
        
        # Add creative integration ideas
        interactions.append("\n### Creative Integration Ideas")
        
        creative_ideas = [
            f"- Use {project_name} to trigger a cascade of module interactions",
            f"- Create a feedback loop where {project_name} learns from other modules",
            f"- Implement a pub/sub system where {project_name} broadcasts events",
            f"- Build a module mesh where {project_name} can discover and use new capabilities",
            f"- Design a scenario where {project_name} coordinates a complex multi-module workflow"
        ]
        
        # Select 3 random ideas
        selected_ideas = random.sample(creative_ideas, min(3, len(creative_ideas)))
        interactions.extend(selected_ideas)
        
        return '\n'.join(interactions)

    async def create_master_index(self):
        """Create enhanced master index with health scores"""
        index_content = """# Big Picture: All Registered Projects (Enhanced Analysis)

This directory contains comprehensive enhanced analyses of all registered projects in the ecosystem,
including security scanning, code metrics, and health scores.

## Project Index

| Order | Project | Health | Security | Code Quality | Docs | Status |
|-------|---------|--------|----------|--------------|------|--------|
"""
        
        for project in self.projects:
            output_file = self.output_dir / f"{project['order']}_Describe_{project['name']}.md"
            status = "✅" if output_file.exists() else "❌"
            
            # Extract scores from file if it exists
            health = "?"
            security = "?"
            quality = "?"
            docs = "?"
            
            if output_file.exists():
                content = output_file.read_text()
                
                # Extract overall health score
                health_match = re.search(r'Overall Health Score: (\d+)/100', content)
                if health_match:
                    score = int(health_match.group(1))
                    health = f"{score} {self._get_health_emoji(score)}"
                
                # Extract other metrics
                if 'No vulnerabilities found' in content and 'No security issues found' in content:
                    security = "✅"
                elif 'vulnerabilities' in content or 'security issues' in content:
                    security = "⚠️"
                
                # Code quality
                mi_match = re.search(r'Average MI: ([\d.]+)', content)
                if mi_match:
                    mi = float(mi_match.group(1))
                    quality = "✅" if mi >= 65 else "⚠️"
                
                # Documentation
                doc_match = re.search(r'Completeness score: (\d+)%', content)
                if doc_match:
                    doc_score = int(doc_match.group(1))
                    docs = "✅" if doc_score >= 70 else "⚠️"
            
            index_content += f"| {project['order']} | [{project['name']}](./{project['order']}_Describe_{project['name']}.md) | {health} | {security} | {quality} | {docs} | {status} |\n"
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        index_content += f"""

## Legend

- **Health**: Overall project health score (0-100)
  - 🟢 90-100: Excellent
  - 🟡 70-89: Good
  - 🟠 50-69: Needs Improvement
  - 🔴 0-49: Critical Issues

- **Security**: ✅ Secure | ⚠️ Issues Found
- **Code Quality**: ✅ Good | ⚠️ Needs Refactoring
- **Docs**: ✅ Well Documented | ⚠️ Needs Documentation

## Enhanced Analysis Features

This enhanced analysis includes:

1. **Security Scanning**
   - Dependency vulnerability scanning (pip-audit)
   - Code security analysis (bandit)
   - Hardcoded secrets detection

2. **Code Quality Metrics**
   - Cyclomatic Complexity
   - Maintainability Index
   - Lines of Code metrics
   - Comment ratios

3. **Documentation Quality**
   - README completeness scoring
   - Docstring coverage analysis
   - Example code detection

4. **Git/Version Control Metrics**
   - Commit history analysis
   - Contributor statistics
   - Recent activity tracking

5. **Health Scoring**
   - Comprehensive health score calculation
   - Component-wise scoring
   - Actionable recommendations

## Next Steps

1. Address security vulnerabilities in projects with ⚠️ security status
2. Refactor code in projects with low maintainability scores
3. Improve documentation for projects with ⚠️ docs status
4. Run regular scans to track improvement over time

## Running the Analysis

To run this enhanced analysis:

```bash
cd /home/graham/workspace/shared_claude_docs
python3 utils/enhanced_big_picture_analyzer.py
```

To install required tools:
```bash
pip install radon bandit pip-audit safety
```

---
*Generated: {timestamp}*
"""
        
        index_file = self.output_dir / "000_INDEX_ENHANCED.md"
        with open(index_file, 'w') as f:
            f.write(index_content)
        
        print(f"\n📚 Enhanced master index created: {index_file.name}")


async def main():
    """Main execution"""
    output_dir = Path("/home/graham/workspace/shared_claude_docs/docs/big_picture")
    
    print("🚀 Enhanced Big Picture Analyzer")
    print("=" * 50)
    print("\nThis enhanced version includes:")
    print("- Security vulnerability scanning")
    print("- Code complexity metrics")
    print("- Documentation quality analysis")
    print("- Git metrics and activity tracking")
    print("- Overall health scoring")
    print("\nNote: Some features require additional tools:")
    print("  pip install radon bandit pip-audit safety")
    print("")
    
    analyzer = EnhancedProjectAnalyzer(output_dir)
    await analyzer.analyze_all_projects()


if __name__ == "__main__":
    asyncio.run(main())