# Python Code Anti-Pattern Checklist

*Generated: 2025-06-08T07:04:42.536481*
*Source: ArjanCodes + Granger Research Synthesis*

## Overview

This checklist contains 10 Python anti-patterns identified through:
- ArjanCodes educational content analysis
- Academic research synthesis
- Community best practices
- Automated detection patterns

## Anti-Pattern Rules

### Code Style

#### AP-006: Not Using Enumerate

**Severity:** low
**Category:** code_style

**Description:** Using range(len()) to iterate with indices

**Example (Bad):**
```python
for i in range(len(items)):
```

**Example (Good):**
```python
for i, item in enumerate(items):
```

**Detection Pattern:** `for\s+\w+\s+in\s+range\s*\(\s*len\s*\(`

**Impact:**
- Performance: 20%
- Maintainability: 50%
- Security: 10%
- Reliability: 30%

---

### Data Handling

#### AP-001: Mutable Default Arguments

**Severity:** high
**Category:** data_handling

**Description:** Using mutable objects as default function arguments

**Example (Bad):**
```python
def foo(items=[]): items.append(1)
```

**Example (Good):**
```python
def foo(items=None): if items is None: items = []
```

**Detection Pattern:** `def\s+\w+\([^)]*=\s*(\[|\{)`

**Impact:**
- Performance: 80%
- Maintainability: 90%
- Security: 70%
- Reliability: 90%

---

### Design

#### AP-009: Overusing Classes

**Severity:** medium
**Category:** design

**Description:** Creating classes when functions would suffice

**Example (Bad):**
```python
class Calculator: def add(self, a, b): return a + b
```

**Example (Good):**
```python
def add(a, b): return a + b
```

**Detection Pattern:** `class\s+\w+.*:\s*def\s+\w+\(self[^)]*\)(?!.*__init__)`

**Impact:**
- Performance: 50%
- Maintainability: 70%
- Security: 30%
- Reliability: 60%

---

### Error Handling

#### AP-002: Bare Except Clauses

**Severity:** high
**Category:** error_handling

**Description:** Using except without specifying exception type

**Example (Bad):**
```python
try: risky() except: pass
```

**Example (Good):**
```python
try: risky() except SpecificError as e: handle(e)
```

**Detection Pattern:** `except\s*:`

**Impact:**
- Performance: 80%
- Maintainability: 90%
- Security: 70%
- Reliability: 90%

---

### Modernization

#### AP-008: Not Using Pathlib

**Severity:** low
**Category:** modernization

**Description:** Using os.path instead of pathlib

**Example (Bad):**
```python
os.path.join(dir, 'file')
```

**Example (Good):**
```python
Path(dir) / 'file'
```

**Detection Pattern:** `os\.path\.(join|exists|isfile)`

**Impact:**
- Performance: 20%
- Maintainability: 50%
- Security: 10%
- Reliability: 30%

---

### Performance

#### AP-005: String Concatenation in Loops

**Severity:** medium
**Category:** performance

**Description:** Building strings with + in loops

**Example (Bad):**
```python
for x in items: s += str(x)
```

**Example (Good):**
```python
''.join(str(x) for x in items)
```

**Detection Pattern:** `for.*:\s*\w+\s*\+=\s*str`

**Impact:**
- Performance: 50%
- Maintainability: 70%
- Security: 30%
- Reliability: 60%

---

### Pythonic

#### AP-010: Not Using List Comprehensions

**Severity:** low
**Category:** pythonic

**Description:** Using loops to build lists when comprehensions are clearer

**Example (Bad):**
```python
result = []; for x in items: result.append(x*2)
```

**Example (Good):**
```python
result = [x*2 for x in items]
```

**Detection Pattern:** `=\s*\[\s*\]\s*.*for.*:\s*\w+\.append`

**Impact:**
- Performance: 20%
- Maintainability: 50%
- Security: 10%
- Reliability: 30%

---

### Resource Management

#### AP-003: Not Using Context Managers

**Severity:** medium
**Category:** resource_management

**Description:** Manually opening/closing files instead of using with

**Example (Bad):**
```python
f = open('file.txt')
```

**Example (Good):**
```python
with open('file.txt') as f:
```

**Detection Pattern:** `=\s*open\s*\([^)]+\)(?!.*with)`

**Impact:**
- Performance: 50%
- Maintainability: 70%
- Security: 30%
- Reliability: 60%

---

### State Management

#### AP-004: Global State Mutation

**Severity:** high
**Category:** state_management

**Description:** Modifying global variables inside functions

**Example (Bad):**
```python
global state; state += 1
```

**Example (Good):**
```python
Pass state as parameter and return new state
```

**Detection Pattern:** `global\s+\w+`

**Impact:**
- Performance: 80%
- Maintainability: 90%
- Security: 70%
- Reliability: 90%

---

### Type Safety

#### AP-007: Type Checking with ==

**Severity:** medium
**Category:** type_safety

**Description:** Using == to check types instead of isinstance

**Example (Bad):**
```python
if type(x) == list:
```

**Example (Good):**
```python
if isinstance(x, list):
```

**Detection Pattern:** `type\s*\([^)]+\)\s*==\s*\w+`

**Impact:**
- Performance: 50%
- Maintainability: 70%
- Security: 30%
- Reliability: 60%

---

## Usage

### Automated Detection

Use the detection patterns with tools like:
- `grep -r '<pattern>' .`
- Custom linting rules
- AST-based analysis tools

### Manual Review

For patterns without automated detection:
1. Review during code reviews
2. Include in onboarding documentation
3. Add to team coding standards

### Priority

Focus on high-severity issues first:
1. **High Severity**: Fix immediately (security/reliability impact)
2. **Medium Severity**: Fix in next refactoring
3. **Low Severity**: Fix when touching the code

## Integration with Granger

This checklist is used by:
- `granger_hub`: Orchestrates anti-pattern detection
- `claude-test-reporter`: Reports violations in test results
- `world_model`: Learns from violation patterns
- `rl_commons`: Optimizes detection strategies

---

*For updates, see the [Granger Anti-Pattern Detection Pipeline](../GRANGER_PROJECTS.md)*