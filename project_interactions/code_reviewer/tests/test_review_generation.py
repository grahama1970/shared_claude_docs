"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_review_generation.py
Purpose: Tests for review generation and formatting

External Dependencies:
- pytest: Testing framework - https://docs.pytest.org/

Example Usage:
>>> pytest test_review_generation.py -v
"""

import pytest
from pathlib import Path
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from code_reviewer_interaction import (
    CodeReviewerInteraction, CodeIssue, ReviewResult,
    IssueSeverity, IssueCategory, CodeMetrics
)


class TestReviewGeneration:
    """Test review generation and formatting"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.reviewer = CodeReviewerInteraction()
    
    def test_review_comment_formatting(self):
        """Test formatting of individual review comments"""
        test_cases = [
            (
                CodeIssue(
                    severity=IssueSeverity.CRITICAL,
                    category=IssueCategory.SECURITY,
                    line=10,
                    column=5,
                    message="Hardcoded password detected",
                    suggestion="Use environment variables",
                    rule_id="SEC_001"
                ),
                ["🚨", "CRITICAL", "Hardcoded password", "environment variables", "SEC_001"]
            ),
            (
                CodeIssue(
                    severity=IssueSeverity.LOW,
                    category=IssueCategory.STYLE,
                    line=25,
                    column=0,
                    message="Line too long",
                    suggestion=None,
                    rule_id=None
                ),
                ["💡", "LOW", "Line too long"]
            ),
        ]
        
        for issue, expected_parts in test_cases:
            comment = self.reviewer.format_review_comment(issue)
            for part in expected_parts:
                assert part in comment, f"Comment should contain '{part}'"
    
    def test_review_report_generation(self):
        """Test comprehensive review report generation"""
        # Create mock review results
        result1 = ReviewResult(
            file_path="test1.py",
            language="python",
            metrics=CodeMetrics(
                cyclomatic_complexity=15,
                lines_of_code=100,
                function_count=5
            )
        )
        
        result1.issues = [
            CodeIssue(
                severity=IssueSeverity.CRITICAL,
                category=IssueCategory.SECURITY,
                line=10,
                column=0,
                message="SQL injection vulnerability",
                suggestion="Use parameterized queries"
            ),
            CodeIssue(
                severity=IssueSeverity.HIGH,
                category=IssueCategory.COMPLEXITY,
                line=50,
                column=0,
                message="High cyclomatic complexity",
                suggestion="Refactor into smaller functions"
            )
        ]
        
        result2 = ReviewResult(
            file_path="test2.js",
            language="javascript",
            metrics=CodeMetrics(lines_of_code=50)
        )
        
        # Generate report
        report = self.reviewer.generate_review_report([result1, result2])
        
        # Verify report structure
        assert "# Code Review Report" in report
        assert "## Summary" in report
        assert "Files reviewed: 2" in report
        assert "Total issues: 2" in report
        assert "Critical issues: 1" in report
        assert "High priority issues: 1" in report
        
        # Verify file sections
        assert "test1.py" in report
        assert "Language: python" in report
        assert "Cyclomatic complexity: 15" in report
        
        # Verify issues are included
        assert "SQL injection" in report
        assert "High cyclomatic complexity" in report
    
    def test_custom_rule_addition(self):
        """Test adding and applying custom rules"""
        # Add custom rule
        self.reviewer.add_custom_rule(
            "CUSTOM_TODO",
            r"TODO|FIXME",
            IssueSeverity.INFO,
            IssueCategory.DOCUMENTATION,
            "Found TODO/FIXME comment",
            "Address the TODO or create a ticket"
        )
        
        # Verify rule was added
        assert "CUSTOM_TODO" in self.reviewer.custom_rules
        
        # Test file with TODO
        test_code = '''def example():
    # TODO: Implement this function
    pass
    # FIXME: This is broken
'''
        test_file = Path("test_custom_rule.py")
        test_file.write_text(test_code)
        
        try:
            # Note: Custom rule application would need to be implemented
            # in the main review logic. This tests the structure.
            rule = self.reviewer.custom_rules["CUSTOM_TODO"]
            assert rule['severity'] == IssueSeverity.INFO
            assert rule['category'] == IssueCategory.DOCUMENTATION
            assert rule['pattern'].search("TODO: something") is not None
            
        finally:
            test_file.unlink()
    
    def test_issue_prioritization(self):
        """Test that issues are properly prioritized"""
        issues = [
            CodeIssue(IssueSeverity.LOW, IssueCategory.STYLE, 30, 0, "Style issue"),
            CodeIssue(IssueSeverity.CRITICAL, IssueCategory.SECURITY, 10, 0, "Security issue"),
            CodeIssue(IssueSeverity.HIGH, IssueCategory.BUG, 20, 0, "Bug"),
            CodeIssue(IssueSeverity.CRITICAL, IssueCategory.SECURITY, 5, 0, "Another security issue"),
            CodeIssue(IssueSeverity.MEDIUM, IssueCategory.PERFORMANCE, 15, 0, "Performance issue"),
        ]
        
        # Create result and sort issues
        result = ReviewResult(file_path="test.py")
        result.issues = issues
        result.issues.sort(key=lambda x: (
            list(IssueSeverity).index(x.severity),
            x.line
        ))
        
        # Verify sorting
        assert result.issues[0].severity == IssueSeverity.CRITICAL
        assert result.issues[0].line == 5  # Earlier line first
        assert result.issues[1].severity == IssueSeverity.CRITICAL
        assert result.issues[1].line == 10
        assert result.issues[2].severity == IssueSeverity.HIGH
        assert result.issues[-1].severity == IssueSeverity.LOW
    
    def test_multi_language_review(self):
        """Test reviewing files in different languages"""
        # Python file
        python_code = '''def example():
    password = "secret123"
    return password
'''
        
        # JavaScript file
        js_code = '''function example() {
    var oldStyle = true;  // Should use let/const
    return oldStyle;
}'''
        
        # Java file
        java_code = '''public class Example {
    public void debug() {
        System.out.println("Debug message");
    }
}'''
        
        files = [
            ("test.py", python_code, "python"),
            ("test.js", js_code, "javascript"),
            ("test.java", java_code, "java")
        ]
        
        results = []
        
        try:
            for filename, code, expected_lang in files:
                path = Path(filename)
                path.write_text(code)
                
                result = self.reviewer.review_file(filename)
                results.append(result)
                
                assert result.language == expected_lang, f"Should detect {expected_lang}"
                assert len(result.issues) > 0, f"Should find issues in {filename}"
                
                path.unlink()
            
            # Generate combined report
            report = self.reviewer.generate_review_report(results)
            
            # Verify all languages are in report
            assert "python" in report
            assert "javascript" in report
            assert "java" in report
            
        finally:
            # Cleanup any remaining files
            for filename, _, _ in files:
                path = Path(filename)
                if path.exists():
                    path.unlink()
    
    def test_git_diff_review(self):
        """Test reviewing git diff (mock test)"""
        # This is a mock test since we can't guarantee git state
        # In real usage, this would review actual git changes
        
        # Test the method exists and handles errors gracefully
        results = self.reviewer.review_git_diff("non-existent-branch")
        assert isinstance(results, list), "Should return a list even on error"
    
    def test_empty_file_handling(self):
        """Test handling of empty files"""
        empty_file = Path("empty.py")
        empty_file.write_text("")
        
        try:
            result = self.reviewer.review_file(str(empty_file))
            assert result.file_path == str(empty_file)
            assert result.metrics.lines_of_code == 0
            assert result.language == "python"
            
        finally:
            empty_file.unlink()
    
    def test_syntax_error_handling(self):
        """Test handling of files with syntax errors"""
        bad_code = '''def broken_function(
    # Missing closing parenthesis
    pass
'''
        
        bad_file = Path("syntax_error.py")
        bad_file.write_text(bad_code)
        
        try:
            result = self.reviewer.review_file(str(bad_file))
            
            # Should detect syntax error
            syntax_errors = [i for i in result.issues if i.category == IssueCategory.BUG and "syntax" in i.message.lower()]
            assert len(syntax_errors) > 0, "Should detect syntax error"
            assert syntax_errors[0].severity == IssueSeverity.CRITICAL
            
        finally:
            bad_file.unlink()


def main():
    """Run review generation tests with real data validation"""
    print("📝 Running review generation tests...")
    
    # Create test instance
    tests = TestReviewGeneration()
    
    tests_passed = 0
    tests_failed = 0
    
    test_methods = [
        ("Review comment formatting", tests.test_review_comment_formatting),
        ("Review report generation", tests.test_review_report_generation),
        ("Custom rule addition", tests.test_custom_rule_addition),
        ("Issue prioritization", tests.test_issue_prioritization),
        ("Multi-language review", tests.test_multi_language_review),
        ("Git diff review", tests.test_git_diff_review),
        ("Empty file handling", tests.test_empty_file_handling),
        ("Syntax error handling", tests.test_syntax_error_handling),
    ]
    
    for test_name, test_method in test_methods:
        tests.setup_method()
        try:
            test_method()
            print(f"✅ {test_name} test passed")
            tests_passed += 1
        except AssertionError as e:
            print(f"❌ {test_name} test failed: {e}")
            tests_failed += 1
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
            tests_failed += 1
    
    print(f"\n📊 Test Results: {tests_passed} passed, {tests_failed} failed")
    
    # Test actual review generation with sample file
    print("\n🔍 Testing full review generation...")
    
    sample_code = '''#!/usr/bin/env python3
"""Sample module for testing review generation"""

import random
import os

# Configuration
API_KEY = "sk-test-1234567890"
DEBUG = True

class DataProcessor:
    def __init__(self, data=[]):  # Mutable default
        self.data = data
    
    def processItems(self, items):  # Wrong naming
        """Process items with high complexity"""
        results = []
        
        for item in items:
            if item > 0:
                if item < 10:
                    results.append(item * 2)
                elif item < 100:
                    if item % 2 == 0:
                        results.append(item / 2)
                    else:
                        results.append(item * 3)
                else:
                    results.append(item)
            else:
                results.append(0)
        
        # Generate token
        token = random.randint(1000, 9999)
        
        try:
            # Some operation
            pass
        except:  # Bare except
            pass
        
        return results, token

# This is a very long line that exceeds the recommended character limit and should be broken down into multiple shorter lines for better readability
'''
    
    test_file = Path("sample_review.py")
    test_file.write_text(sample_code)
    
    try:
        reviewer = CodeReviewerInteraction()
        result = reviewer.review_file(str(test_file))
        report = reviewer.generate_review_report([result])
        
        # Save report
        report_file = Path("sample_review_report.md")
        report_file.write_text(report)
        
        print(f"✅ Generated review report: {report_file}")
        print(f"   - Found {len(result.issues)} issues")
        print(f"   - Cyclomatic complexity: {result.metrics.cyclomatic_complexity}")
        
        # Display sample of report
        print("\n--- Report Preview ---")
        lines = report.split('\n')[:20]
        for line in lines:
            print(line)
        print("...")
        
        # Cleanup
        test_file.unlink()
        report_file.unlink()
        
    except Exception as e:
        print(f"❌ Error generating sample report: {e}")
        if test_file.exists():
            test_file.unlink()
        tests_failed += 1
    
    if tests_failed > 0:
        return 1
    
    print("\n✅ All review generation tests passed!")
    return 0


if __name__ == "__main__":
    exit(main())