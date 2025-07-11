
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: code_translation_interaction.py
Purpose: Multi-language code translation pipeline using AST-based transformation

External Dependencies:
- ast: https://docs.python.org/3/library/ast.html
- astor: https://astor.readthedocs.io/
- loguru: https://loguru.readthedocs.io/

Example Usage:
>>> from code_translation_interaction import CodeTranslationPipeline
>>> pipeline = CodeTranslationPipeline()
>>> js_code = pipeline.translate(python_code, "python", "javascript")
'function fibonacci(n) { ... }'
"""

import ast
import re
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
from loguru import logger

# Configure logging
logger.remove()
logger.add(
    lambda msg: print(msg),
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="INFO"
)


@dataclass
class TranslationResult:
    """Result of a code translation operation"""
    success: bool
    source_language: str
    target_language: str
    source_code: str
    translated_code: str
    warnings: List[str]
    preserved_comments: List[str]
    translation_time: float


class LanguagePattern:
    """Language-specific patterns and idioms"""
    
    PYTHON_PATTERNS = {
        'list_comprehension': r'\[.*for.*in.*\]',
        'dict_comprehension': r'\{.*:.*for.*in.*\}',
        'with_statement': r'with\s+.*:',
        'decorator': r'@\w+',
        'f_string': r'f["\'].*\{.*\}.*["\']',
        'walrus': r':=',
        'type_hint': r':\s*\w+\s*=',
    }
    
    JAVASCRIPT_PATTERNS = {
        'arrow_function': r'=>',
        'template_literal': r'`.*\$\{.*\}`',
        'destructuring': r'const\s*\{.*\}\s*=',
        'spread_operator': r'\.\.\.', 
        'optional_chaining': r'\?\.', 
        'nullish_coalescing': r'\?\?',
    }
    
    GO_PATTERNS = {
        'short_declaration': r':=',
        'defer': r'defer\s+',
        'goroutine': r'go\s+',
        'channel': r'<-',
        'interface': r'interface\s*\{',
        'struct': r'struct\s*\{',
    }


class ASTTransformer:
    """Base class for AST transformations between languages"""
    
    def __init__(self):
        self.preserved_comments = []
        self.warnings = []
    
    def extract_comments(self, source_code: str, language: str) -> List[str]:
        """Extract comments from source code"""
        comments = []
        
        if language == "python":
            # Python comments
            for line in source_code.split('\n'):
                if '#' in line:
                    comment_idx = line.find('#')
                    comments.append(line[comment_idx:].strip())
            # Docstrings
            docstring_pattern = r'""".*?"""|\'\'\'.*?\'\'\''
            docstrings = re.findall(docstring_pattern, source_code, re.DOTALL)
            comments.extend(docstrings)
            
        elif language == "javascript":
            # Single line comments
            single_comments = re.findall(r'//.*$', source_code, re.MULTILINE)
            comments.extend(single_comments)
            # Multi-line comments
            multi_comments = re.findall(r'/\*.*?\*/', source_code, re.DOTALL)
            comments.extend(multi_comments)
            
        elif language == "go":
            # Similar to JavaScript
            single_comments = re.findall(r'//.*$', source_code, re.MULTILINE)
            comments.extend(single_comments)
            multi_comments = re.findall(r'/\*.*?\*/', source_code, re.DOTALL)
            comments.extend(multi_comments)
            
        return comments


class PythonToJavaScriptTransformer(ASTTransformer):
    """Transform Python AST to JavaScript code"""
    
    def __init__(self):
        super().__init__()
        self.indent_level = 0
        self.in_class = False
        
    def transform(self, node: ast.AST) -> str:
        """Transform Python AST node to JavaScript code"""
        if isinstance(node, ast.Module):
            return '\n'.join(self.transform(stmt) for stmt in node.body)
            
        elif isinstance(node, ast.FunctionDef):
            if self.in_class:
                # Skip 'self' parameter for class methods
                params = ', '.join(arg.arg for arg in node.args.args[1:])
                body = self.transform_body(node.body)
                return f"{node.name}({params}) {{\n{body}\n}}"
            else:
                params = ', '.join(arg.arg for arg in node.args.args)
                body = self.transform_body(node.body)
                return f"function {node.name}({params}) {{\n{body}\n}}"
                
        elif isinstance(node, ast.ClassDef):
            self.in_class = True
            methods = []
            constructor = None
            
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    if item.name == "__init__":
                        # Transform __init__ to constructor
                        params = ', '.join(arg.arg for arg in item.args.args[1:])  # Skip self
                        body = self.transform_body(item.body)
                        constructor = f"constructor({params}) {{\n{body}\n}}"
                    else:
                        methods.append(self.transform(item))
                        
            self.in_class = False
            
            class_body = []
            if constructor:
                class_body.append(constructor)
            class_body.extend(methods)
            
            return f"class {node.name} {{\n{chr(10).join(class_body)}\n}}"
            
        elif isinstance(node, ast.If):
            test = self.transform_expr(node.test)
            body = self.transform_body(node.body)
            if node.orelse:
                orelse = self.transform_body(node.orelse)
                return f"if ({test}) {{\n{body}\n}} else {{\n{orelse}\n}}"
            return f"if ({test}) {{\n{body}\n}}"
            
        elif isinstance(node, ast.For):
            if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name):
                if node.iter.func.id == "range":
                    # Transform range-based for loop
                    target = node.target.id
                    if len(node.iter.args) == 1:
                        end = self.transform_expr(node.iter.args[0])
                        body = self.transform_body(node.body)
                        return f"for (let {target} = 0; {target} < {end}; {target}++) {{\n{body}\n}}"
                    elif len(node.iter.args) >= 2:
                        start = self.transform_expr(node.iter.args[0])
                        end = self.transform_expr(node.iter.args[1])
                        body = self.transform_body(node.body)
                        return f"for (let {target} = {start}; {target} < {end}; {target}++) {{\n{body}\n}}"
                        
            # Transform for-in loop
            target = node.target.id if isinstance(node.target, ast.Name) else str(node.target)
            iter_expr = self.transform_expr(node.iter)
            body = self.transform_body(node.body)
            return f"for (const {target} of {iter_expr}) {{\n{body}\n}}"
            
        elif isinstance(node, ast.While):
            test = self.transform_expr(node.test)
            body = self.transform_body(node.body)
            return f"while ({test}) {{\n{body}\n}}"
            
        elif isinstance(node, ast.Return):
            if node.value:
                return f"return {self.transform_expr(node.value)};"
            return "return;"
            
        elif isinstance(node, ast.Assign):
            targets = [self.transform_expr(t) for t in node.targets]
            value = self.transform_expr(node.value)
            if len(targets) == 1:
                target = targets[0]
                # Don't use 'let' for attribute assignments (e.g., this.property)
                if '.' in target:
                    return f"{target} = {value};"
                else:
                    return f"let {target} = {value};"
            else:
                # Destructuring assignment
                return f"let [{', '.join(targets)}] = {value};"
                
        elif isinstance(node, ast.AugAssign):
            target = self.transform_expr(node.target)
            value = self.transform_expr(node.value)
            op_map = {
                ast.Add: '+=',
                ast.Sub: '-=',
                ast.Mult: '*=',
                ast.Div: '/=',
                ast.Mod: '%=',
            }
            op = op_map.get(type(node.op), '?=')
            return f"{target} {op} {value};"
                
        elif isinstance(node, ast.Expr):
            return self.transform_expr(node.value) + ";"
            
        elif isinstance(node, ast.Continue):
            return "continue;"
            
        elif isinstance(node, ast.Break):
            return "break;"
            
        elif isinstance(node, ast.Pass):
            return "// pass"
            
        else:
            self.warnings.append(f"Unsupported node type: {type(node).__name__}")
            return f"// TODO: Transform {type(node).__name__}"
            
    def transform_body(self, body: List[ast.AST]) -> str:
        """Transform a list of statements"""
        self.indent_level += 1
        result = []
        for stmt in body:
            transformed = self.transform(stmt)
            result.append("  " * self.indent_level + transformed)
        self.indent_level -= 1
        return '\n'.join(result)
        
    def transform_expr(self, node: ast.AST) -> str:
        """Transform expression nodes"""
        if isinstance(node, ast.Name):
            # Map Python built-ins to JavaScript
            name_map = {
                'True': 'true',
                'False': 'false', 
                'None': 'null',
                'len': '.length',
                'str': 'String',
                'int': 'parseInt',
                'float': 'parseFloat',
            }
            # Handle 'self' in class context
            if node.id == 'self' and self.in_class:
                return 'this'
            return name_map.get(node.id, node.id)
            
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            return str(node.value)
            
        elif isinstance(node, ast.BinOp):
            left = self.transform_expr(node.left)
            right = self.transform_expr(node.right)
            op_map = {
                ast.Add: '+',
                ast.Sub: '-',
                ast.Mult: '*',
                ast.Div: '/',
                ast.Mod: '%',
                ast.Pow: '**',
                ast.FloorDiv: '/',  # Note: JS doesn't have floor div
            }
            op = op_map.get(type(node.op), '?')
            if isinstance(node.op, ast.FloorDiv):
                return f"Math.floor({left} / {right})"
            return f"({left} {op} {right})"
            
        elif isinstance(node, ast.Compare):
            left = self.transform_expr(node.left)
            ops = []
            for op, comparator in zip(node.ops, node.comparators):
                op_map = {
                    ast.Eq: '===',
                    ast.NotEq: '!==',
                    ast.Lt: '<',
                    ast.LtE: '<=',
                    ast.Gt: '>',
                    ast.GtE: '>=',
                    ast.In: 'in',
                    ast.NotIn: 'not in',
                }
                op_str = op_map.get(type(op), '?')
                comp = self.transform_expr(comparator)
                if isinstance(op, ast.In):
                    ops.append(f"{comp}.includes({left})")
                elif isinstance(op, ast.NotIn):
                    ops.append(f"!{comp}.includes({left})")
                else:
                    ops.append(f"{left} {op_str} {comp}")
            return ' && '.join(ops)
            
        elif isinstance(node, ast.Call):
            func = self.transform_expr(node.func)
            args = [self.transform_expr(arg) for arg in node.args]
            
            # Handle Python built-in functions
            if isinstance(node.func, ast.Name):
                if node.func.id == "print":
                    return f"console.log({', '.join(args)})"
                elif node.func.id == "len":
                    return f"{args[0]}.length"
                elif node.func.id == "range":
                    # This is handled in For loop transformation
                    pass
                    
            return f"{func}({', '.join(args)})"
            
        elif isinstance(node, ast.List):
            elts = [self.transform_expr(e) for e in node.elts]
            return f"[{', '.join(elts)}]"
            
        elif isinstance(node, ast.Dict):
            pairs = []
            for k, v in zip(node.keys, node.values):
                key = self.transform_expr(k)
                value = self.transform_expr(v)
                # Remove quotes from key if it's a simple identifier
                if key.startswith('"') and key.endswith('"') and key[1:-1].isidentifier():
                    key = key[1:-1]
                pairs.append(f"{key}: {value}")
            return f"{{{', '.join(pairs)}}}"
            
        elif isinstance(node, ast.Attribute):
            value = self.transform_expr(node.value)
            # Handle method calls like self.method() -> this.method()
            return f"{value}.{node.attr}"
            
        elif isinstance(node, ast.Subscript):
            value = self.transform_expr(node.value)
            slice_val = self.transform_expr(node.slice)
            return f"{value}[{slice_val}]"
            
        elif isinstance(node, ast.UnaryOp):
            operand = self.transform_expr(node.operand)
            op_map = {
                ast.Not: '!',
                ast.USub: '-',
                ast.UAdd: '+',
            }
            op = op_map.get(type(node.op), '?')
            return f"{op}{operand}"
            
        elif isinstance(node, ast.BoolOp):
            values = [self.transform_expr(v) for v in node.values]
            op = ' && ' if isinstance(node.op, ast.And) else ' || '
            return f"({op.join(values)})"
            
        elif isinstance(node, ast.ListComp):
            # Transform list comprehension to map/filter
            target = node.generators[0].target.id
            iter_expr = self.transform_expr(node.generators[0].iter)
            elt = self.transform_expr(node.elt)
            
            result = f"{iter_expr}.map({target} => {elt})"
            
            # Handle if conditions
            for gen in node.generators:
                for if_clause in gen.ifs:
                    cond = self.transform_expr(if_clause)
                    result = f"{iter_expr}.filter({target} => {cond}).map({target} => {elt})"
                    
            return result
            
        elif isinstance(node, ast.DictComp):
            # Transform dict comprehension to Object.fromEntries
            key = self.transform_expr(node.key)
            value = self.transform_expr(node.value)
            target = node.generators[0].target.id
            iter_expr = self.transform_expr(node.generators[0].iter)
            
            return f"Object.fromEntries({iter_expr}.map({target} => [{key}, {value}]))"
            
        elif isinstance(node, ast.Tuple):
            elts = [self.transform_expr(e) for e in node.elts]
            return f"[{', '.join(elts)}]"
            
        elif isinstance(node, ast.JoinedStr):
            # Transform f-strings to template literals
            parts = []
            for value in node.values:
                if isinstance(value, ast.Constant):
                    parts.append(str(value.value))
                elif isinstance(value, ast.FormattedValue):
                    parts.append(f"${{{self.transform_expr(value.value)}}}")
            return f"`{''.join(parts)}`"
            
        elif isinstance(node, ast.IfExp):
            # Ternary operator
            test = self.transform_expr(node.test)
            body = self.transform_expr(node.body)
            orelse = self.transform_expr(node.orelse)
            return f"({test} ? {body} : {orelse})"
            
        else:
            self.warnings.append(f"Unsupported expression type: {type(node).__name__}")
            return f"/* TODO: {type(node).__name__} */"


class JavaScriptToPythonTransformer(ASTTransformer):
    """Transform JavaScript code to Python code"""
    
    def __init__(self):
        super().__init__()
        self.indent_level = 0
        
    def transform(self, js_code: str) -> str:
        """Transform JavaScript code to Python code"""
        # This is a simplified implementation
        # In a real implementation, you would use a JavaScript parser
        
        lines = []
        
        # Basic transformations
        js_code = js_code.replace('console.log', 'print')
        js_code = js_code.replace('true', 'True')
        js_code = js_code.replace('false', 'False')
        js_code = js_code.replace('null', 'None')
        js_code = js_code.replace('===', '==')
        js_code = js_code.replace('!==', '!=')
        js_code = js_code.replace('let ', '')
        js_code = js_code.replace('const ', '')
        js_code = js_code.replace('var ', '')
        
        # Transform function declarations
        js_code = re.sub(r'function\s+(\w+)\s*\((.*?)\)\s*{', r'def \1(\2):', js_code)
        
        # Transform arrow functions
        js_code = re.sub(r'(\w+)\s*=>\s*{', r'lambda \1: ', js_code)
        
        # Transform class declarations
        js_code = re.sub(r'class\s+(\w+)\s*{', r'class \1:', js_code)
        
        # Transform if statements
        js_code = re.sub(r'if\s*\((.*?)\)\s*{', r'if \1:', js_code)
        
        # Transform for loops
        js_code = re.sub(r'for\s*\(.*?(\w+)\s*=\s*(\d+);\s*\1\s*<\s*(.*?);\s*\1\+\+\)\s*{',
                         r'for \1 in range(\2, \3):', js_code)
        
        # Remove semicolons and braces
        js_code = js_code.replace(';', '')
        js_code = js_code.replace('{', '')
        js_code = js_code.replace('}', '')
        
        return js_code


class GoTransformer(ASTTransformer):
    """Transform between Python and Go"""
    
    def python_to_go(self, python_code: str) -> str:
        """Transform Python code to Go code"""
        # Parse Python AST
        tree = ast.parse(python_code)
        
        # Transform to Go
        go_code = self._transform_module_to_go(tree)
        
        # Add package declaration
        return f"package main\n\nimport \"fmt\"\n\n{go_code}"
        
    def _transform_module_to_go(self, node: ast.Module) -> str:
        """Transform Python module to Go code"""
        parts = []
        
        for stmt in node.body:
            if isinstance(stmt, ast.FunctionDef):
                parts.append(self._transform_function_to_go(stmt))
            elif isinstance(stmt, ast.Assign):
                parts.append(self._transform_assign_to_go(stmt))
                
        return '\n\n'.join(parts)
        
    def _transform_function_to_go(self, node: ast.FunctionDef) -> str:
        """Transform Python function to Go function"""
        params = []
        for arg in node.args.args:
            # Default to interface{} type
            params.append(f"{arg.arg} interface{{}}")
            
        param_str = ', '.join(params)
        body = self._transform_body_to_go(node.body)
        
        return f"func {node.name}({param_str}) interface{{}} {{\n{body}\n}}"
        
    def _transform_body_to_go(self, body: List[ast.AST]) -> str:
        """Transform function body to Go"""
        parts = []
        
        for stmt in body:
            if isinstance(stmt, ast.Return):
                if stmt.value:
                    value = self._transform_expr_to_go(stmt.value)
                    parts.append(f"\treturn {value}")
                else:
                    parts.append("\treturn nil")
            elif isinstance(stmt, ast.Assign):
                parts.append("\t" + self._transform_assign_to_go(stmt))
            elif isinstance(stmt, ast.If):
                parts.append(self._transform_if_to_go(stmt))
            elif isinstance(stmt, ast.For):
                parts.append(self._transform_for_to_go(stmt))
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                call = self._transform_expr_to_go(stmt.value)
                parts.append(f"\t{call}")
                
        return '\n'.join(parts)
        
    def _transform_assign_to_go(self, node: ast.Assign) -> str:
        """Transform assignment to Go"""
        if len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                value = self._transform_expr_to_go(node.value)
                return f"{target.id} := {value}"
        return "// TODO: Complex assignment"
        
    def _transform_if_to_go(self, node: ast.If) -> str:
        """Transform if statement to Go"""
        test = self._transform_expr_to_go(node.test)
        body = self._transform_body_to_go(node.body)
        
        result = f"\tif {test} {{\n{body}\n\t}}"
        
        if node.orelse:
            orelse = self._transform_body_to_go(node.orelse)
            result += f" else {{\n{orelse}\n\t}}"
            
        return result
        
    def _transform_for_to_go(self, node: ast.For) -> str:
        """Transform for loop to Go"""
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name):
            if node.iter.func.id == "range" and len(node.iter.args) == 1:
                # Simple range loop
                target = node.target.id
                limit = self._transform_expr_to_go(node.iter.args[0])
                body = self._transform_body_to_go(node.body)
                return f"\tfor {target} := 0; {target} < {limit}; {target}++ {{\n{body}\n\t}}"
                
        return "\t// TODO: Complex for loop"
        
    def _transform_expr_to_go(self, node: ast.AST) -> str:
        """Transform expression to Go"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            elif isinstance(node.value, bool):
                return str(node.value).lower()
            return str(node.value)
        elif isinstance(node, ast.BinOp):
            left = self._transform_expr_to_go(node.left)
            right = self._transform_expr_to_go(node.right)
            op_map = {
                ast.Add: '+',
                ast.Sub: '-',
                ast.Mult: '*',
                ast.Div: '/',
                ast.Mod: '%',
            }
            op = op_map.get(type(node.op), '?')
            return f"({left} {op} {right})"
        elif isinstance(node, ast.Compare):
            left = self._transform_expr_to_go(node.left)
            op_map = {
                ast.Eq: '==',
                ast.NotEq: '!=',
                ast.Lt: '<',
                ast.LtE: '<=',
                ast.Gt: '>',
                ast.GtE: '>=',
            }
            parts = []
            for op, comp in zip(node.ops, node.comparators):
                op_str = op_map.get(type(op), '?')
                comp_str = self._transform_expr_to_go(comp)
                parts.append(f"{left} {op_str} {comp_str}")
            return ' && '.join(parts)
        elif isinstance(node, ast.Call):
            func = self._transform_expr_to_go(node.func)
            args = [self._transform_expr_to_go(arg) for arg in node.args]
            
            # Map Python built-ins to Go
            if isinstance(node.func, ast.Name):
                if node.func.id == "print":
                    return f"fmt.Println({', '.join(args)})"
                    
            return f"{func}({', '.join(args)})"
            
        return "/* TODO */"


class CodeTranslationPipeline:
    """Main pipeline for translating code between languages"""
    
    def __init__(self):
        self.transformers = {
            ('python', 'javascript'): PythonToJavaScriptTransformer(),
            ('javascript', 'python'): JavaScriptToPythonTransformer(),
            ('python', 'go'): GoTransformer(),
        }
        
    def translate(self, source_code: str, source_lang: str, target_lang: str) -> str:
        """Translate code from source language to target language"""
        start_time = time.time()
        
        logger.info(f"Starting translation: {source_lang} → {target_lang}")
        
        # Normalize language names
        source_lang = source_lang.lower()
        target_lang = target_lang.lower()
        
        # Get appropriate transformer
        transformer_key = (source_lang, target_lang)
        if transformer_key not in self.transformers:
            raise ValueError(f"Translation from {source_lang} to {target_lang} not supported")
            
        transformer = self.transformers[transformer_key]
        
        # Extract comments
        comments = transformer.extract_comments(source_code, source_lang)
        transformer.preserved_comments = comments
        
        # Perform translation
        try:
            if source_lang == 'python' and target_lang == 'javascript':
                tree = ast.parse(source_code)
                translated_code = transformer.transform(tree)
            elif source_lang == 'javascript' and target_lang == 'python':
                translated_code = transformer.transform(source_code)
            elif source_lang == 'python' and target_lang == 'go':
                translated_code = transformer.python_to_go(source_code)
            else:
                raise ValueError(f"Translation path not implemented")
                
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return TranslationResult(
                success=False,
                source_language=source_lang,
                target_language=target_lang,
                source_code=source_code,
                translated_code="",
                warnings=[str(e)],
                preserved_comments=[],
                translation_time=time.time() - start_time
            )
            
        # Add preserved comments
        if comments and translated_code:
            comment_block = self._format_comments(comments, target_lang)
            translated_code = f"{comment_block}\n\n{translated_code}"
            
        translation_time = time.time() - start_time
        
        logger.info(f"Translation completed in {translation_time:.2f}s")
        logger.info(f"Preserved {len(comments)} comments")
        
        if transformer.warnings:
            logger.warning(f"Translation warnings: {transformer.warnings}")
            
        return TranslationResult(
            success=True,
            source_language=source_lang,
            target_language=target_lang,
            source_code=source_code,
            translated_code=translated_code,
            warnings=transformer.warnings,
            preserved_comments=comments,
            translation_time=translation_time
        )
        
    def _format_comments(self, comments: List[str], target_lang: str) -> str:
        """Format comments for target language"""
        if target_lang in ['javascript', 'go']:
            # Use // style comments
            formatted = []
            for comment in comments:
                if comment.startswith('#'):
                    formatted.append('//' + comment[1:])
                elif comment.startswith('"""') or comment.startswith("'''"):
                    # Convert docstring to multi-line comment
                    content = comment[3:-3].strip()
                    formatted.append(f"/*\n{content}\n*/")
                else:
                    formatted.append(comment)
            return '\n'.join(formatted)
        elif target_lang == 'python':
            # Use # style comments
            formatted = []
            for comment in comments:
                if comment.startswith('//'):
                    formatted.append('#' + comment[2:])
                elif comment.startswith('/*') and comment.endswith('*/'):
                    # Convert multi-line comment to docstring
                    content = comment[2:-2].strip()
                    formatted.append(f'"""\n{content}\n"""')
                else:
                    formatted.append(comment)
            return '\n'.join(formatted)
        return '\n'.join(comments)
        
    def validate_translation(self, original: str, translated: str, 
                           source_lang: str, target_lang: str) -> bool:
        """Validate that translation preserves functionality (simplified)"""
        # Check for preservation of key elements
        checks = []
        
        # Function count check
        if source_lang == 'python':
            orig_functions = len(re.findall(r'def\s+\w+', original))
            if target_lang == 'javascript':
                trans_functions = len(re.findall(r'function\s+\w+|(\w+)\s*\(.*?\)\s*{', translated))
            elif target_lang == 'go':
                trans_functions = len(re.findall(r'func\s+\w+', translated))
            else:
                trans_functions = 0
            checks.append(orig_functions == trans_functions)
            
        # Variable preservation (simplified)
        if source_lang == 'python':
            orig_vars = set(re.findall(r'(\w+)\s*=', original))
            if target_lang == 'javascript':
                trans_vars = set(re.findall(r'(?:let|const|var)?\s*(\w+)\s*=', translated))
            elif target_lang == 'go':
                trans_vars = set(re.findall(r'(\w+)\s*:=', translated))
            else:
                trans_vars = set()
            # At least 50% of variables should be preserved
            if orig_vars:
                checks.append(len(trans_vars.intersection(orig_vars)) >= len(orig_vars) * 0.5)
                
        return all(checks) if checks else True


def test_basic_translation():
    """Test basic Python to JavaScript translation - Expected: 0.5s"""
    logger.info("Testing basic Python → JavaScript translation")
    
    python_code = """
def add(a, b):
    return a + b

def multiply(x, y):
    result = x * y
    return result
    
# Test the functions
print(add(5, 3))
print(multiply(4, 6))
"""
    
    pipeline = CodeTranslationPipeline()
    result = pipeline.translate(python_code, "python", "javascript")
    
    logger.info(f"Translation successful: {result.success}")
    logger.info(f"Translation time: {result.translation_time:.3f}s")
    logger.info("Translated code:")
    print(result.translated_code)
    
    # Validate output structure
    assert "function add(" in result.translated_code
    assert "function multiply(" in result.translated_code
    assert "console.log(" in result.translated_code
    assert result.translation_time < 1.0  # Should be fast
    
    return result.success


def test_class_translation():
    """Test class translation from Python to JavaScript - Expected: 0.7s"""
    logger.info("Testing Python class → JavaScript translation")
    
    python_code = '''
class Calculator:
    """A simple calculator class"""
    
    def __init__(self, name):
        self.name = name
        self.history = []
        
    def add(self, a, b):
        result = a + b
        self.history.append(result)
        return result
        
    def get_history(self):
        return self.history
'''
    
    pipeline = CodeTranslationPipeline()
    result = pipeline.translate(python_code, "python", "javascript")
    
    logger.info(f"Translation successful: {result.success}")
    logger.info("Translated code:")
    print(result.translated_code)
    
    # Validate class structure
    assert "class Calculator" in result.translated_code
    assert "constructor(" in result.translated_code
    assert "add(a, b)" in result.translated_code
    assert "get_history()" in result.translated_code
    assert len(result.preserved_comments) > 0  # Should preserve docstring
    
    return result.success


def test_control_flow_translation():
    """Test control flow translation - Expected: 0.8s"""
    logger.info("Testing control flow translation")
    
    python_code = """
def process_numbers(numbers):
    # Process a list of numbers
    total = 0
    
    for num in numbers:
        if num > 0:
            total += num
        elif num < 0:
            print("Negative number:", num)
        else:
            continue
            
    # Check final total
    if total > 100:
        return "Large sum"
    else:
        return "Small sum"
"""
    
    pipeline = CodeTranslationPipeline()
    result = pipeline.translate(python_code, "python", "javascript")
    
    logger.info("Translated code:")
    print(result.translated_code)
    
    # Validate control structures
    assert "for (const num of numbers)" in result.translated_code
    assert "if (num > 0)" in result.translated_code
    assert "else if (num < 0)" in result.translated_code
    assert result.preserved_comments  # Comments preserved
    
    return result.success


def test_list_comprehension_translation():
    """Test list comprehension translation - Expected: 1.0s"""
    logger.info("Testing list comprehension translation")
    
    python_code = """
def process_data(data):
    # Simple list comprehension
    squares = [x * x for x in data]
    
    # Filtered comprehension
    evens = [x for x in data if x % 2 == 0]
    
    # Nested operations
    doubled_evens = [x * 2 for x in data if x % 2 == 0]
    
    return squares, evens, doubled_evens
"""
    
    pipeline = CodeTranslationPipeline()
    result = pipeline.translate(python_code, "python", "javascript")
    
    logger.info("Translated code:")
    print(result.translated_code)
    
    # Check for map/filter transformations
    assert ".map(" in result.translated_code
    assert ".filter(" in result.translated_code
    
    return result.success


def test_python_to_go_translation():
    """Test Python to Go translation - Expected: 1.2s"""
    logger.info("Testing Python → Go translation")
    
    python_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def main():
    for i in range(10):
        print(fibonacci(i))
"""
    
    pipeline = CodeTranslationPipeline()
    result = pipeline.translate(python_code, "python", "go")
    
    logger.info("Translated Go code:")
    print(result.translated_code)
    
    # Validate Go syntax
    assert "package main" in result.translated_code
    assert "import \"fmt\"" in result.translated_code
    assert "func fibonacci(" in result.translated_code
    assert "func main(" in result.translated_code
    assert "fmt.Println(" in result.translated_code
    
    return result.success


def test_idiomatic_patterns():
    """Test translation of idiomatic patterns - Expected: 1.5s"""
    logger.info("Testing idiomatic pattern translation")
    
    python_code = """
def process_dict(data):
    # Dictionary comprehension
    squared = {k: v * v for k, v in data.items()}
    
    # Using enumerate
    for i, value in enumerate(data.values()):
        print(f"Index {i}: {value}")
        
    # Multiple assignment
    a, b, c = 1, 2, 3
    
    # With statement (context manager)
    # with open('file.txt') as f:
    #     content = f.read()
    
    return squared
"""
    
    pipeline = CodeTranslationPipeline()
    result = pipeline.translate(python_code, "python", "javascript")
    
    logger.info("Translated code:")
    print(result.translated_code)
    logger.info(f"Warnings: {result.warnings}")
    
    # The translation should handle or warn about Python-specific patterns
    return result.success


def test_comment_preservation():
    """Test comment preservation across translations - Expected: 0.6s"""
    logger.info("Testing comment preservation")
    
    python_code = '''
#!/usr/bin/env python3
"""
This module demonstrates comment preservation.
It includes various comment styles.
"""

# Single line comment before function
def example_function(x, y):
    """
    Function docstring explaining purpose.
    
    Args:
        x: First parameter
        y: Second parameter
    """
    # Inline comment about calculation
    result = x + y  # End of line comment
    
    # Multi-line comment block
    # explaining the next section
    # of code in detail
    
    return result
'''
    
    pipeline = CodeTranslationPipeline()
    result = pipeline.translate(python_code, "python", "javascript")
    
    logger.info(f"Preserved {len(result.preserved_comments)} comments")
    logger.info("Translated code with comments:")
    print(result.translated_code)
    
    # Check comment preservation
    assert len(result.preserved_comments) >= 5
    assert "//" in result.translated_code or "/*" in result.translated_code
    
    return result.success


def test_error_handling():
    """Test error handling in translation - Expected: 0.3s"""
    logger.info("Testing error handling")
    
    # Invalid Python code
    invalid_code = """
def broken_function(
    # Missing closing parenthesis
    return "This won't parse"
"""
    
    pipeline = CodeTranslationPipeline()
    result = pipeline.translate(invalid_code, "python", "javascript")
    
    logger.info(f"Translation failed as expected: {not result.success}")
    logger.info(f"Error captured: {result.warnings}")
    
    # Test unsupported language pair
    try:
        pipeline.translate("code", "c++", "rust")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        logger.info(f"Correctly rejected unsupported languages: {e}")
        
    return True


def test_performance_benchmark():
    """Test translation performance on larger code - Expected: 2.0s"""
    logger.info("Testing performance on larger codebase")
    
    # Generate a larger code sample
    python_code = """
class DataProcessor:
    def __init__(self):
        self.data = []
        self.processed = False
        
    def load_data(self, items):
        self.data = items
        self.processed = False
        
    def process(self):
        results = []
        
        for item in self.data:
            if isinstance(item, int):
                if item % 2 == 0:
                    results.append(item * 2)
                else:
                    results.append(item * 3)
            elif isinstance(item, str):
                results.append(item.upper())
            else:
                results.append(str(item))
                
        self.processed = True
        return results
        
    def get_statistics(self):
        if not self.processed:
            return None
            
        total = 0
        count = 0
        
        for item in self.data:
            if isinstance(item, int):
                total += item
                count += 1
                
        return {
            'total': total,
            'count': count,
            'average': total / count if count > 0 else 0
        }
"""
    
    # Duplicate the code to make it larger
    large_code = python_code
    for i in range(5):
        large_code += f"\n\nclass DataProcessor{i}(DataProcessor):\n    pass\n"
        
    pipeline = CodeTranslationPipeline()
    start = time.time()
    result = pipeline.translate(large_code, "python", "javascript")
    duration = time.time() - start
    
    logger.info(f"Large code translation time: {duration:.3f}s")
    logger.info(f"Code size: {len(large_code)} characters")
    logger.info(f"Translation successful: {result.success}")
    
    # Performance assertion
    assert duration < 3.0, f"Translation too slow: {duration}s"
    assert result.success
    
    return True


def test_validation_accuracy():
    """Test translation validation accuracy - Expected: 1.0s"""
    logger.info("Testing translation validation")
    
    original_py = """
def calculate(x, y):
    return x + y

def process(items):
    total = 0
    for item in items:
        total += item
    return total
"""
    
    pipeline = CodeTranslationPipeline()
    result = pipeline.translate(original_py, "python", "javascript")
    
    # Test validation
    is_valid = pipeline.validate_translation(
        original_py, 
        result.translated_code,
        "python",
        "javascript"
    )
    
    logger.info(f"Translation validation: {is_valid}")
    assert is_valid, "Translation validation failed"
    
    # Test with missing function (should fail validation)
    incomplete_js = "function calculate(x, y) { return x + y; }"
    is_valid = pipeline.validate_translation(
        original_py,
        incomplete_js,
        "python", 
        "javascript"
    )
    
    logger.info(f"Incomplete translation correctly identified: {not is_valid}")
    assert not is_valid, "Should detect missing function"
    
    return True


if __name__ == "__main__":
    # Test with real data
    logger.info("=== Code Translation Pipeline Validation ===")
    
    tests = [
        ("Basic Translation", test_basic_translation, 0.5),
        ("Class Translation", test_class_translation, 0.7),
        ("Control Flow", test_control_flow_translation, 0.8),
        ("List Comprehensions", test_list_comprehension_translation, 1.0),
        ("Python to Go", test_python_to_go_translation, 1.2),
        ("Idiomatic Patterns", test_idiomatic_patterns, 1.5),
        ("Comment Preservation", test_comment_preservation, 0.6),
        ("Error Handling", test_error_handling, 0.3),
        ("Performance Benchmark", test_performance_benchmark, 2.0),
        ("Validation Accuracy", test_validation_accuracy, 1.0),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func, expected_duration in tests:
        logger.info(f"\n--- Running: {test_name} ---")
        logger.info(f"Expected duration: {expected_duration}s")
        
        try:
            start_time = time.time()
            result = test_func()
            duration = time.time() - start_time
            
            if result:
                logger.info(f"✅ PASSED in {duration:.3f}s")
                passed += 1
            else:
                logger.error(f"❌ FAILED in {duration:.3f}s")
                failed += 1
                
        except Exception as e:
            logger.error(f"❌ FAILED with exception: {e}")
            failed += 1
            
    # Summary
    total = passed + failed
    logger.info(f"\n{'='*50}")
    logger.info(f"Test Summary: {passed}/{total} passed ({failed} failed)")
    
    if failed == 0:
        logger.info("✅ All tests passed!")
    else:
        logger.error(f"❌ {failed} tests failed")
        
    # Exit with appropriate code
    exit(0 if failed == 0 else 1)