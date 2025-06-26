# Complexity Module Analysis

## Overview
Complexity is a code analysis tool that measures and reports on code complexity metrics across multiple programming languages. It helps identify areas of code that may need refactoring and provides insights into maintainability.

## Core Capabilities
- **Cyclomatic Complexity**: Measure code path complexity
- **Cognitive Complexity**: Assess mental effort to understand code
- **Lines of Code**: Various LOC metrics (total, logical, comments)
- **Halstead Metrics**: Software science measurements
- **Maintainability Index**: Overall code health score
- **Language Support**: 30+ programming languages via tree-sitter

## Technical Features
- Tree-sitter based parsing for accuracy
- Incremental analysis for large codebases
- Git integration for historical trends
- JSON/CSV/HTML report formats
- Configurable complexity thresholds
- IDE plugin support

## Integration with GRANGER
- Analyzes module code quality
- Feeds complexity data to RL for optimization
- Identifies refactoring opportunities
- Tracks technical debt over time
- Validates code improvements

## Metrics Provided
1. **Function-level**: Complexity per function/method
2. **File-level**: Aggregate file complexity
3. **Module-level**: Overall module health
4. **Trend Analysis**: Complexity over time
5. **Hotspot Detection**: Most complex areas

## Use Cases
1. **Code Quality Gates**: Enforce complexity limits
2. **Refactoring Targets**: Find complex code to simplify
3. **Technical Debt Tracking**: Monitor code health
4. **RL Training Data**: Use complexity as reward signal

## Path
`/home/graham/workspace/experiments/complexity/`

## Status
**Active** - Provides code quality metrics for GRANGER modules

## Priority
**Medium** - Important for maintaining code quality
