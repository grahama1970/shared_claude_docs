#!/usr/bin/env python3
"""
Module: test_code_analysis.py
Purpose: Tests for code analysis functionality

External Dependencies:
- pytest: Testing framework - https://docs.pytest.org/
- ast: Python AST parsing (stdlib)

Example Usage:
>>> pytest test_code_analysis.py -v
"""

import pytest
import ast
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from code_reviewer_interaction import (
    ComplexityAnalyzer, CodeReviewerInteraction,
    CodeMetrics, IssueSeverity, IssueCategory
)


class TestComplexityAnalyzer:
    """Test complexity analysis functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = ComplexityAnalyzer()
    
    def test_cyclomatic_complexity_simple(self):
        """Test cyclomatic complexity for simple function"""
        code = """
def simple_function(x):
    return x * 2
"""
        tree = ast.parse(code)
        func_node = tree.body[0]
        complexity = self.analyzer.calculate_cyclomatic_complexity(func_node)
        assert complexity == 1, "Simple function should have complexity 1"
    
    def test_cyclomatic_complexity_with_conditions(self):
        """Test cyclomatic complexity with conditionals"""
        code = """
def conditional_function(x):
    if x > 0:
        return x
    elif x < 0:
        return -x
    else:
        return 0
"""
        tree = ast.parse(code)
        func_node = tree.body[0]
        complexity = self.analyzer.calculate_cyclomatic_complexity(func_node)
        assert complexity >= 3, "Function with if-elif-else should have complexity >= 3"
    
    def test_cyclomatic_complexity_with_loops(self):
        """Test cyclomatic complexity with loops"""
        code = """
def loop_function(items):
    result = 0
    for item in items:
        if item > 0:
            result += item
    return result
"""
        tree = ast.parse(code)
        func_node = tree.body[0]
        complexity = self.analyzer.calculate_cyclomatic_complexity(func_node)
        assert complexity >= 3, "Function with loop and condition should have complexity >= 3"
    
    def test_cognitive_complexity(self):
        """Test cognitive complexity calculation"""
        code = """
def nested_function(x, y):
    if x > 0:
        if y > 0:
            return x + y
        else:
            return x - y
    else:
        return 0
"""
        tree = ast.parse(code)
        func_node = tree.body[0]
        complexity = self.analyzer.calculate_cognitive_complexity(func_node)
        assert complexity > 2, "Nested conditions should increase cognitive complexity"
    
    def test_nesting_depth(self):
        """Test nesting depth analysis"""
        code = """
def deeply_nested():
    if True:
        while True:
            for i in range(10):
                if i > 5:
                    pass
"""
        tree = ast.parse(code)
        max_depth = self.analyzer.analyze_nesting_depth(tree)
        assert max_depth >= 4, "Should detect deep nesting"


class TestCodeAnalysis:
    """Test code analysis features"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.reviewer = CodeReviewerInteraction()
    
    def test_python_metrics_calculation(self):
        """Test Python code metrics calculation"""
        code = '''"""Module docstring"""
# This is a comment
import os

def function_one():
    """Function docstring"""
    return 42

def function_two(x, y):
    # Another comment
    if x > y:
        return x
    return y

class TestClass:
    """Class docstring"""
    def method(self):
        pass
'''
        tree = ast.parse(code)
        result = self.reviewer._calculate_python_metrics(code, tree)
        
        assert result.function_count >= 2, "Should count at least 2 functions"
        assert result.class_count == 1, "Should count 1 class"
        assert result.lines_of_code > 0, "Should have positive LOC"
        assert result.comment_ratio > 0, "Should have comments"
    
    def test_language_detection(self):
        """Test programming language detection"""
        test_cases = [
            ("test.py", "python"),
            ("test.js", "javascript"),
            ("test.java", "java"),
            ("test.go", "go"),
            ("test.ts", "typescript"),
            ("test.unknown", "unknown")
        ]
        
        for filename, expected_lang in test_cases:
            detected = self.reviewer._detect_language(filename)
            assert detected == expected_lang, f"Should detect {expected_lang} for {filename}"
    
    def test_python_style_checks(self):
        """Test Python style guideline checks"""
        # Create test file with style issues
        test_code = '''def badlyNamedFunction():
    pass

class lower_case_class:
    pass

# This is a very long line that definitely exceeds one hundred characters and should trigger a line length warning
'''
        test_file = Path("test_style.py")
        test_file.write_text(test_code)
        
        try:
            result = self.reviewer.review_file(str(test_file))
            
            # Check for naming convention issues
            naming_issues = [i for i in result.issues if "naming" in i.message.lower() or "snake_case" in i.message.lower() or "PascalCase" in i.message.lower()]
            assert len(naming_issues) >= 2, "Should detect naming convention issues"
            
            # Check for line length issues
            line_length_issues = [i for i in result.issues if "line too long" in i.message.lower()]
            assert len(line_length_issues) >= 1, "Should detect long lines"
            
        finally:
            test_file.unlink()
    
    def test_python_best_practices(self):
        """Test Python best practice checks"""
        test_code = '''def bad_function(items=[]):
    """Function with mutable default"""
    items.append(1)
    return items

def exception_handler():
    try:
        risky_operation()
    except:  # Bare except
        pass
'''
        test_file = Path("test_practices.py")
        test_file.write_text(test_code)
        
        try:
            result = self.reviewer.review_file(str(test_file))
            
            # Check for mutable default
            mutable_issues = [i for i in result.issues if "mutable" in i.message.lower()]
            assert len(mutable_issues) >= 1, "Should detect mutable default argument"
            
            # Check for bare except
            except_issues = [i for i in result.issues if "bare except" in i.message.lower()]
            assert len(except_issues) >= 1, "Should detect bare except"
            
        finally:
            test_file.unlink()
    
    def test_issue_sorting(self):
        """Test that issues are sorted by severity and line number"""
        test_code = '''
# Line 2: Low severity issue
x = 1  # TODO: fix this

# Line 5: Critical issue
password = "admin123"

# Line 8: Medium issue
def badNaming():
    pass
'''
        test_file = Path("test_sorting.py")
        test_file.write_text(test_code)
        
        try:
            result = self.reviewer.review_file(str(test_file))
            
            if len(result.issues) >= 2:
                # Check that critical issues come first
                severities = [issue.severity for issue in result.issues]
                critical_index = next((i for i, s in enumerate(severities) if s == IssueSeverity.CRITICAL), -1)
                low_index = next((i for i, s in enumerate(severities) if s == IssueSeverity.LOW), -1)
                
                if critical_index >= 0 and low_index >= 0:
                    assert critical_index < low_index, "Critical issues should come before low severity"
            
        finally:
            test_file.unlink()


def main():
    """Run tests with real data validation"""
    print("🧪 Running code analysis tests...")
    
    # Create test instances
    complexity_tests = TestComplexityAnalyzer()
    analysis_tests = TestCodeAnalysis()
    
    # Run complexity tests
    complexity_tests.setup_method()
    tests_passed = 0
    tests_failed = 0
    
    try:
        complexity_tests.test_cyclomatic_complexity_simple()
        print("✅ Cyclomatic complexity simple test passed")
        tests_passed += 1
    except AssertionError as e:
        print(f"❌ Cyclomatic complexity simple test failed: {e}")
        tests_failed += 1
    
    try:
        complexity_tests.test_cyclomatic_complexity_with_conditions()
        print("✅ Cyclomatic complexity conditions test passed")
        tests_passed += 1
    except AssertionError as e:
        print(f"❌ Cyclomatic complexity conditions test failed: {e}")
        tests_failed += 1
    
    try:
        complexity_tests.test_cognitive_complexity()
        print("✅ Cognitive complexity test passed")
        tests_passed += 1
    except AssertionError as e:
        print(f"❌ Cognitive complexity test failed: {e}")
        tests_failed += 1
    
    # Run analysis tests
    analysis_tests.setup_method()
    
    try:
        analysis_tests.test_language_detection()
        print("✅ Language detection test passed")
        tests_passed += 1
    except AssertionError as e:
        print(f"❌ Language detection test failed: {e}")
        tests_failed += 1
    
    try:
        analysis_tests.test_python_metrics_calculation()
        print("✅ Python metrics calculation test passed")
        tests_passed += 1
    except AssertionError as e:
        print(f"❌ Python metrics calculation test failed: {e}")
        tests_failed += 1
    
    print(f"\n📊 Test Results: {tests_passed} passed, {tests_failed} failed")
    
    if tests_failed > 0:
        return 1
    
    print("\n✅ All code analysis tests passed!")
    return 0


if __name__ == "__main__":
    exit(main())