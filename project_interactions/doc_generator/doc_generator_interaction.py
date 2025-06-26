
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: doc_generator_interaction.py
Purpose: Automated Documentation Generator - Parses Python modules to generate comprehensive documentation

External Dependencies:
- ast: https://docs.python.org/3/library/ast.html
- json: https://docs.python.org/3/library/json.html
- graphviz: https://graphviz.readthedocs.io/
- markdown: https://python-markdown.github.io/

Example Usage:
>>> from doc_generator_interaction import DocumentationGenerator
>>> generator = DocumentationGenerator()
>>> docs = generator.generate_from_module('/path/to/module.py')
>>> generator.export_markdown(docs, 'output.md')
"""

import ast
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import importlib.util
import inspect
import re
from collections import defaultdict
import html

# Optional dependencies for enhanced features
try:
    import graphviz
    HAS_GRAPHVIZ = True
except ImportError:
    HAS_GRAPHVIZ = False
    print("Warning: graphviz not installed. Dependency graphs will be text-based.")

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False
    print("Warning: markdown not installed. HTML generation will use basic formatting.")


@dataclass
class FunctionInfo:
    """Information about a function or method"""
    name: str
    docstring: Optional[str]
    parameters: List[Dict[str, Any]]
    return_type: Optional[str]
    decorators: List[str]
    is_async: bool
    line_number: int
    complexity: int = 0
    
    
@dataclass 
class ClassInfo:
    """Information about a class"""
    name: str
    docstring: Optional[str]
    bases: List[str]
    methods: List[FunctionInfo]
    attributes: Dict[str, Any]
    line_number: int
    decorators: List[str]


@dataclass
class ModuleInfo:
    """Complete module information"""
    name: str
    path: str
    docstring: Optional[str]
    imports: List[str]
    classes: List[ClassInfo]
    functions: List[FunctionInfo]
    constants: Dict[str, Any]
    dependencies: Set[str]
    test_coverage: Optional[float] = None


class ASTAnalyzer(ast.NodeVisitor):
    """AST visitor for extracting module information"""
    
    def __init__(self, module_path: str):
        self.module_path = module_path
        self.imports: List[str] = []
        self.classes: List[ClassInfo] = []
        self.functions: List[FunctionInfo] = []
        self.constants: Dict[str, Any] = {}
        self.dependencies: Set[str] = set()
        self.current_class: Optional[str] = None
        
    def visit_Import(self, node: ast.Import) -> None:
        """Extract import statements"""
        for alias in node.names:
            import_name = alias.name
            self.imports.append(import_name)
            self.dependencies.add(import_name.split('.')[0])
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Extract from ... import statements"""
        if node.module:
            self.imports.append(f"from {node.module} import ...")
            self.dependencies.add(node.module.split('.')[0])
        self.generic_visit(node)
        
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Extract class information"""
        self.current_class = node.name
        
        # Extract base classes
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(ast.unparse(base))
                
        # Extract decorators
        decorators = [ast.unparse(d) for d in node.decorator_list]
        
        # Extract methods
        methods = []
        attributes = {}
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(self._extract_function_info(item))
            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                # Class attributes with type annotations
                attr_type = ast.unparse(item.annotation) if item.annotation else "Any"
                attributes[item.target.id] = attr_type
                
        class_info = ClassInfo(
            name=node.name,
            docstring=ast.get_docstring(node),
            bases=bases,
            methods=methods,
            attributes=attributes,
            line_number=node.lineno,
            decorators=decorators
        )
        
        self.classes.append(class_info)
        self.current_class = None
        self.generic_visit(node)
        
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Extract function information"""
        if self.current_class is None:  # Only top-level functions
            func_info = self._extract_function_info(node)
            self.functions.append(func_info)
        self.generic_visit(node)
        
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Extract async function information"""
        if self.current_class is None:
            func_info = self._extract_function_info(node, is_async=True)
            self.functions.append(func_info)
        self.generic_visit(node)
        
    def visit_Assign(self, node: ast.Assign) -> None:
        """Extract module-level constants"""
        if self.current_class is None:
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    try:
                        self.constants[target.id] = ast.literal_eval(node.value)
                    except:
                        self.constants[target.id] = ast.unparse(node.value)
        self.generic_visit(node)
        
    def _extract_function_info(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], 
                              is_async: bool = False) -> FunctionInfo:
        """Extract detailed function information"""
        # Extract parameters
        parameters = []
        for arg in node.args.args:
            param_info = {"name": arg.arg}
            
            # Get type annotation
            if arg.annotation:
                param_info["type"] = ast.unparse(arg.annotation)
            else:
                param_info["type"] = "Any"
                
            parameters.append(param_info)
            
        # Get return type
        return_type = None
        if node.returns:
            return_type = ast.unparse(node.returns)
            
        # Extract decorators
        decorators = [ast.unparse(d) for d in node.decorator_list]
        
        # Calculate complexity (simplified McCabe complexity)
        complexity = self._calculate_complexity(node)
        
        return FunctionInfo(
            name=node.name,
            docstring=ast.get_docstring(node),
            parameters=parameters,
            return_type=return_type,
            decorators=decorators,
            is_async=is_async or isinstance(node, ast.AsyncFunctionDef),
            line_number=node.lineno,
            complexity=complexity
        )
        
    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity


class DocumentationGenerator:
    """Main documentation generator class"""
    
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.modules: Dict[str, ModuleInfo] = {}
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        
    def generate_from_module(self, module_path: Union[str, Path]) -> ModuleInfo:
        """Generate documentation from a single module"""
        module_path = Path(module_path)
        
        if not module_path.exists():
            raise FileNotFoundError(f"Module not found: {module_path}")
            
        # Read and parse the module
        with open(module_path, 'r', encoding='utf-8') as f:
            source = f.read()
            
        tree = ast.parse(source)
        
        # Extract module information
        analyzer = ASTAnalyzer(str(module_path))
        analyzer.visit(tree)
        
        # Get module docstring
        module_docstring = ast.get_docstring(tree)
        
        # Create module info
        module_name = module_path.stem
        module_info = ModuleInfo(
            name=module_name,
            path=str(module_path),
            docstring=module_docstring,
            imports=analyzer.imports,
            classes=analyzer.classes,
            functions=analyzer.functions,
            constants=analyzer.constants,
            dependencies=analyzer.dependencies
        )
        
        self.modules[module_name] = module_info
        
        # Update dependency graph
        for dep in analyzer.dependencies:
            self.dependency_graph[module_name].add(dep)
            
        return module_info
        
    def generate_from_directory(self, directory: Union[str, Path], 
                              recursive: bool = True) -> Dict[str, ModuleInfo]:
        """Generate documentation from all Python files in a directory"""
        directory = Path(directory)
        
        if not directory.is_dir():
            raise NotADirectoryError(f"Not a directory: {directory}")
            
        pattern = "**/*.py" if recursive else "*.py"
        
        for py_file in directory.glob(pattern):
            if py_file.name.startswith('_'):
                continue  # Skip private modules
                
            try:
                self.generate_from_module(py_file)
            except Exception as e:
                print(f"Error processing {py_file}: {e}")
                
        return self.modules
        
    def generate_interaction_diagram(self, output_format: str = "text") -> str:
        """Generate module interaction diagram"""
        if output_format == "graphviz" and HAS_GRAPHVIZ:
            return self._generate_graphviz_diagram()
        else:
            return self._generate_text_diagram()
            
    def _generate_text_diagram(self) -> str:
        """Generate text-based dependency diagram"""
        lines = ["Module Dependency Graph", "=" * 50, ""]
        
        for module, deps in self.dependency_graph.items():
            if deps:
                lines.append(f"{module}:")
                for dep in sorted(deps):
                    lines.append(f"  └─> {dep}")
                lines.append("")
                
        return "\n".join(lines)
        
    def _generate_graphviz_diagram(self) -> str:
        """Generate Graphviz DOT format diagram"""
        if not HAS_GRAPHVIZ:
            return self._generate_text_diagram()
            
        dot = graphviz.Digraph(comment='Module Dependencies')
        dot.attr(rankdir='LR')
        
        # Add nodes
        for module in self.modules:
            dot.node(module, module)
            
        # Add edges
        for module, deps in self.dependency_graph.items():
            for dep in deps:
                if dep in self.modules:  # Only internal dependencies
                    dot.edge(module, dep)
                    
        return dot.source
        
    def export_markdown(self, output_path: Union[str, Path]) -> None:
        """Export documentation as Markdown"""
        output_path = Path(output_path)
        
        md_lines = [
            f"# Project Documentation",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Table of Contents",
            ""
        ]
        
        # Add TOC
        for module_name in sorted(self.modules.keys()):
            md_lines.append(f"- [{module_name}](#{module_name.lower().replace('_', '-')})")
            
        md_lines.extend(["", "## Modules", ""])
        
        # Add module documentation
        for module_name, module_info in sorted(self.modules.items()):
            md_lines.extend(self._generate_module_markdown(module_info))
            
        # Add dependency graph
        md_lines.extend([
            "",
            "## Module Dependencies",
            "",
            "```",
            self.generate_interaction_diagram(),
            "```"
        ])
        
        # Write to file
        output_path.write_text("\n".join(md_lines))
        
    def _generate_module_markdown(self, module: ModuleInfo) -> List[str]:
        """Generate Markdown for a single module"""
        lines = [
            f"### {module.name}",
            "",
            f"**Path:** `{module.path}`",
            ""
        ]
        
        if module.docstring:
            lines.extend([
                "**Description:**",
                "",
                module.docstring,
                ""
            ])
            
        # Constants
        if module.constants:
            lines.extend(["#### Constants", ""])
            for name, value in module.constants.items():
                lines.append(f"- `{name}` = `{value}`")
            lines.append("")
            
        # Functions
        if module.functions:
            lines.extend(["#### Functions", ""])
            for func in module.functions:
                lines.extend(self._generate_function_markdown(func))
                
        # Classes
        if module.classes:
            lines.extend(["#### Classes", ""])
            for cls in module.classes:
                lines.extend(self._generate_class_markdown(cls))
                
        lines.append("---")
        lines.append("")
        
        return lines
        
    def _generate_function_markdown(self, func: FunctionInfo) -> List[str]:
        """Generate Markdown for a function"""
        # Function signature
        params = ", ".join([p["name"] + ": " + p["type"] for p in func.parameters])
        return_str = f" -> {func.return_type}" if func.return_type else ""
        async_str = "async " if func.is_async else ""
        
        lines = [
            f"##### {async_str}`{func.name}({params}){return_str}`",
            ""
        ]
        
        if func.decorators:
            for dec in func.decorators:
                lines.append(f"*@{dec}*")
            lines.append("")
            
        if func.docstring:
            lines.extend([func.docstring, ""])
            
        lines.extend([
            f"- **Line:** {func.line_number}",
            f"- **Complexity:** {func.complexity}",
            ""
        ])
        
        return lines
        
    def _generate_class_markdown(self, cls: ClassInfo) -> List[str]:
        """Generate Markdown for a class"""
        bases_str = f"({', '.join(cls.bases)})" if cls.bases else ""
        
        lines = [
            f"##### `class {cls.name}{bases_str}`",
            ""
        ]
        
        if cls.decorators:
            for dec in cls.decorators:
                lines.append(f"*@{dec}*")
            lines.append("")
            
        if cls.docstring:
            lines.extend([cls.docstring, ""])
            
        if cls.attributes:
            lines.extend(["**Attributes:**", ""])
            for attr, attr_type in cls.attributes.items():
                lines.append(f"- `{attr}: {attr_type}`")
            lines.append("")
            
        if cls.methods:
            lines.extend(["**Methods:**", ""])
            for method in cls.methods:
                lines.extend(self._generate_function_markdown(method))
                
        return lines
        
    def export_html(self, output_path: Union[str, Path]) -> None:
        """Export documentation as HTML"""
        output_path = Path(output_path)
        
        # First generate markdown
        md_content_lines = []
        md_content_lines.extend([
            f"# Project Documentation",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ])
        
        for module_name, module_info in sorted(self.modules.items()):
            md_content_lines.extend(self._generate_module_markdown(module_info))
            
        md_content = "\n".join(md_content_lines)
        
        # Convert to HTML
        if HAS_MARKDOWN:
            html_body = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
        else:
            # Basic conversion without markdown library
            html_body = f"<pre>{html.escape(md_content)}</pre>"
            
        # Create full HTML document
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Project Documentation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        code {{ background: #f4f4f4; padding: 2px 4px; }}
        pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
        h1, h2, h3, h4, h5 {{ color: #333; }}
        h1 {{ border-bottom: 2px solid #333; }}
        h2 {{ border-bottom: 1px solid #666; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""
        
        output_path.write_text(html_content)
        
    def export_json(self, output_path: Union[str, Path]) -> None:
        """Export documentation as JSON"""
        output_path = Path(output_path)
        
        # Convert to serializable format
        data = {
            "generated": datetime.now().isoformat(),
            "modules": {}
        }
        
        for module_name, module_info in self.modules.items():
            module_dict = asdict(module_info)
            # Convert sets to lists for JSON serialization
            module_dict["dependencies"] = list(module_info.dependencies)
            data["modules"][module_name] = module_dict
            
        # Add dependency graph
        data["dependency_graph"] = {
            k: list(v) for k, v in self.dependency_graph.items()
        }
        
        # Write JSON
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
            
    def generate_usage_from_tests(self, test_dir: Union[str, Path]) -> Dict[str, List[str]]:
        """Extract usage examples from test files"""
        test_dir = Path(test_dir)
        usage_examples = defaultdict(list)
        
        if not test_dir.exists():
            return usage_examples
            
        for test_file in test_dir.glob("**/test_*.py"):
            try:
                with open(test_file, 'r') as f:
                    source = f.read()
                    
                tree = ast.parse(source)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                        # Extract what's being tested
                        docstring = ast.get_docstring(node)
                        if docstring:
                            # Try to extract module name from test
                            for module_name in self.modules:
                                if module_name in source:
                                    usage_examples[module_name].append(docstring)
                                    
            except Exception as e:
                print(f"Error processing test file {test_file}: {e}")
                
        return dict(usage_examples)


# Test methods with expected durations
class TestDocumentationGenerator:
    """Test suite for documentation generator"""
    
    @staticmethod
    def test_single_module_parsing(expected_duration: float = 0.5) -> Tuple[bool, str]:
        """Test parsing a single module"""
        import time
        start_time = time.time()
        
        generator = DocumentationGenerator()
        
        # Generate documentation for this module itself
        module_info = generator.generate_from_module(__file__)
        
        duration = time.time() - start_time
        
        # Validate results
        if not module_info.name == "doc_generator_interaction":
            return False, f"Module name mismatch: {module_info.name}"
            
        if not module_info.classes:
            return False, "No classes found"
            
        if not module_info.functions:
            return False, "No functions found"
            
        if duration > expected_duration:
            return False, f"Duration {duration:.2f}s exceeded expected {expected_duration}s"
            
        return True, f"Successfully parsed module in {duration:.2f}s"
        
    @staticmethod
    def test_markdown_export(expected_duration: float = 0.3) -> Tuple[bool, str]:
        """Test Markdown export functionality"""
        import time
        import tempfile
        
        start_time = time.time()
        
        generator = DocumentationGenerator()
        generator.generate_from_module(__file__)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            output_path = Path(f.name)
            
        try:
            generator.export_markdown(output_path)
            
            # Verify file was created and has content
            if not output_path.exists():
                return False, "Markdown file not created"
                
            content = output_path.read_text()
            if len(content) < 100:
                return False, f"Markdown content too short: {len(content)} chars"
                
            if "# Project Documentation" not in content:
                return False, "Missing documentation header"
                
            duration = time.time() - start_time
            if duration > expected_duration:
                return False, f"Duration {duration:.2f}s exceeded expected {expected_duration}s"
                
            return True, f"Markdown export successful in {duration:.2f}s"
            
        finally:
            output_path.unlink(missing_ok=True)
            
    @staticmethod
    def test_json_export(expected_duration: float = 0.2) -> Tuple[bool, str]:
        """Test JSON export functionality"""
        import time
        import tempfile
        
        start_time = time.time()
        
        generator = DocumentationGenerator()
        generator.generate_from_module(__file__)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_path = Path(f.name)
            
        try:
            generator.export_json(output_path)
            
            # Verify JSON structure
            with open(output_path) as f:
                data = json.load(f)
                
            if "modules" not in data:
                return False, "Missing 'modules' key in JSON"
                
            if "doc_generator_interaction" not in data["modules"]:
                return False, "Module not found in JSON output"
                
            duration = time.time() - start_time
            if duration > expected_duration:
                return False, f"Duration {duration:.2f}s exceeded expected {expected_duration}s"
                
            return True, f"JSON export successful in {duration:.2f}s"
            
        finally:
            output_path.unlink(missing_ok=True)
            
    @staticmethod
    def test_dependency_graph(expected_duration: float = 0.1) -> Tuple[bool, str]:
        """Test dependency graph generation"""
        import time
        
        start_time = time.time()
        
        generator = DocumentationGenerator()
        generator.generate_from_module(__file__)
        
        # Generate text diagram
        diagram = generator.generate_interaction_diagram("text")
        
        if not diagram:
            return False, "Empty dependency diagram"
            
        if "Module Dependency Graph" not in diagram:
            return False, "Missing diagram header"
            
        duration = time.time() - start_time
        if duration > expected_duration:
            return False, f"Duration {duration:.2f}s exceeded expected {expected_duration}s"
            
        return True, f"Dependency graph generated in {duration:.2f}s"
        
    @staticmethod
    def test_html_export(expected_duration: float = 0.4) -> Tuple[bool, str]:
        """Test HTML export functionality"""
        import time
        import tempfile
        
        start_time = time.time()
        
        generator = DocumentationGenerator()
        generator.generate_from_module(__file__)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            output_path = Path(f.name)
            
        try:
            generator.export_html(output_path)
            
            # Verify HTML structure
            content = output_path.read_text()
            
            if not content.startswith("<!DOCTYPE html>"):
                return False, "Invalid HTML document"
                
            if "<title>Project Documentation</title>" not in content:
                return False, "Missing HTML title"
                
            duration = time.time() - start_time
            if duration > expected_duration:
                return False, f"Duration {duration:.2f}s exceeded expected {expected_duration}s"
                
            return True, f"HTML export successful in {duration:.2f}s"
            
        finally:
            output_path.unlink(missing_ok=True)


def run_all_tests() -> Tuple[int, int]:
    """Run all tests and return pass/fail counts"""
    test_suite = TestDocumentationGenerator()
    tests = [
        ("Single Module Parsing", test_suite.test_single_module_parsing),
        ("Markdown Export", test_suite.test_markdown_export),
        ("JSON Export", test_suite.test_json_export),
        ("Dependency Graph", test_suite.test_dependency_graph),
        ("HTML Export", test_suite.test_html_export)
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("DOCUMENTATION GENERATOR TEST SUITE")
    print("=" * 60)
    print()
    
    for test_name, test_func in tests:
        try:
            success, message = test_func()
            if success:
                print(f"✅ {test_name}: {message}")
                passed += 1
            else:
                print(f"❌ {test_name}: {message}")
                failed += 1
        except Exception as e:
            print(f"❌ {test_name}: Exception - {str(e)}")
            failed += 1
            
    print()
    print("=" * 60)
    print(f"FINAL RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 60)
    
    return passed, failed


if __name__ == "__main__":
    # Test with real data
    print("Testing Documentation Generator with real module...")
    
    # Run all tests
    passed, failed = run_all_tests()
    
    # Example usage demonstration
    if passed > 0:
        print("\n" + "=" * 60)
        print("EXAMPLE USAGE DEMONSTRATION")
        print("=" * 60)
        
        generator = DocumentationGenerator()
        
        # Parse this module
        module_info = generator.generate_from_module(__file__)
        
        print(f"\nModule: {module_info.name}")
        print(f"Classes: {len(module_info.classes)}")
        print(f"Functions: {len(module_info.functions)}")
        print(f"Constants: {len(module_info.constants)}")
        print(f"Dependencies: {', '.join(module_info.dependencies)}")
        
        # Show sample of extracted information
        if module_info.classes:
            cls = module_info.classes[0]
            print(f"\nFirst class: {cls.name}")
            print(f"  Methods: {len(cls.methods)}")
            print(f"  Attributes: {len(cls.attributes)}")
            
        # Generate and show dependency diagram
        print("\nDependency Diagram:")
        print(generator.generate_interaction_diagram())
    
    # Exit with appropriate code
    sys.exit(1 if failed > 0 else 0)