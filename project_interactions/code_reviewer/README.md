# Code Reviewer - Task #36

An intelligent AI-powered code review system with multi-language support and comprehensive analysis capabilities.

## Features

### Core Capabilities
- **Multi-language support**: Python, JavaScript, TypeScript, Java, Go, C/C++, Ruby
- **Security vulnerability detection**: SQL injection, command injection, hardcoded credentials, path traversal, weak randomness, insecure deserialization
- **Code complexity analysis**: Cyclomatic complexity, cognitive complexity, nesting depth
- **Style guide compliance**: Naming conventions, line length, formatting
- **Best practice enforcement**: Mutable defaults, bare except clauses, code smells
- **Custom rule definition**: Add your own patterns and checks
- **Issue prioritization**: Critical, High, Medium, Low, Info severity levels
- **Suggested fixes**: Actionable recommendations for each issue
- **Git integration**: Review changes in pull requests
- **Comprehensive reporting**: Markdown-formatted review reports

### Level 2 (Parallel Processing) Implementation
This task demonstrates parallel processing through:
- Simultaneous analysis of multiple code aspects (security, style, complexity)
- Batch processing of multiple files
- Independent analyzers working in parallel
- Aggregated results from multiple analysis engines

## Usage

### Basic File Review
```python
from code_reviewer_interaction import CodeReviewerInteraction

reviewer = CodeReviewerInteraction()
result = reviewer.review_file("example.py")

print(f"Found {len(result.issues)} issues")
for issue in result.issues:
    print(f"{issue.severity.value}: {issue.message} (line {issue.line})")
```

### Review Git Changes
```python
# Review changes against main branch
results = reviewer.review_git_diff("main")

# Generate comprehensive report
report = reviewer.generate_review_report(results)
print(report)
```

### Add Custom Rules
```python
from code_reviewer_interaction import IssueSeverity, IssueCategory

reviewer.add_custom_rule(
    "NO_PRINT",
    r'print\s*\(',
    IssueSeverity.MEDIUM,
    IssueCategory.BEST_PRACTICE,
    "Avoid print statements in production code",
    "Use logging instead"
)
```

## Issue Categories

- **SECURITY**: Vulnerabilities and security risks
- **PERFORMANCE**: Performance bottlenecks
- **CODE_SMELL**: Poor code patterns
- **STYLE**: Style guideline violations
- **COMPLEXITY**: High complexity code
- **BEST_PRACTICE**: Best practice violations
- **BUG**: Potential bugs
- **DOCUMENTATION**: Documentation issues

## Metrics Provided

- **Cyclomatic Complexity**: Number of linearly independent paths
- **Cognitive Complexity**: How difficult code is to understand
- **Lines of Code**: Non-blank, non-comment lines
- **Comment Ratio**: Ratio of comments to code
- **Function/Class Count**: Number of functions and classes
- **Max Nesting Depth**: Maximum nesting level
- **Average Line Length**: Average characters per line

## Example Output

```markdown
# Code Review Report

Generated: 2025-06-02 08:00:00

## Summary
- Files reviewed: 3
- Total issues: 12
- Critical issues: 2
- High priority issues: 4

## Issues by File

### src/auth.py
- Language: python
- Issues: 5
- Cyclomatic complexity: 15

**Line 23**: 🚨 **CRITICAL**: Hardcoded credential detected
**Suggestion**: Use environment variables or secure vault
*Rule: SEC_HARDCODED_SECRET*

**Line 45**: ⚠️ **HIGH**: Function 'authenticate' has high cyclomatic complexity: 12
**Suggestion**: Consider breaking down the function into smaller pieces
*Rule: PY_HIGH_COMPLEXITY*
```

## Testing

Run the test suite:
```bash
# Run all tests
python test_task_36.py

# Run individual test modules
python tests/test_code_analysis.py
python tests/test_security_checks.py
python tests/test_review_generation.py
```

## Integration with CI/CD

The code reviewer can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Code Review
  run: |
    python -c "
    from code_reviewer_interaction import CodeReviewerInteraction
    reviewer = CodeReviewerInteraction()
    results = reviewer.review_git_diff('main')
    if any(i.severity.value == 'critical' for r in results for i in r.issues):
        exit(1)
    "
```

## Performance Considerations

- Files are analyzed independently for parallel processing
- Large files may take longer due to AST parsing
- Security patterns use compiled regex for efficiency
- Results are cached during review sessions

## Future Enhancements

- Machine learning-based issue detection
- Integration with more languages
- IDE plugins
- Real-time review during coding
- Team-specific rule sets
- Historical analysis tracking