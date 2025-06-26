# GLOBAL CODING STANDARDS — CLAUDE.md

> **Reference guide for all Claude Code project development.**  
> For detailed task planning, see [TASK_PLAN_GUIDE.md](./docs/memory_bank/guides/TASK_PLAN_GUIDE.md).

---

## 🔴 AGENT INSTRUCTIONS

**IMPORTANT:**  
As an agent, you MUST read and follow ALL guidelines in this document BEFORE executing any task in a task list.  
DO NOT skip or ignore any part of these standards. These standards supersede any conflicting instructions you may have received previously.

---

## Project Structure

```
project_name/
├── docs/
│   ├── CHANGELOG.md
│   ├── memory_bank/
│   └── tasks/
├── examples/
├── pyproject.toml
├── README.md
├── src/
│   └── project_name/
├── tests/
│   ├── fixtures/
│   └── project_name/
└── uv.lock
```

- **Package Management:** Always use uv with pyproject.toml, never pip.
- **Mirror Structure:** examples/ and tests/ must mirror the structure in src/.
- **Documentation:** Keep comprehensive docs in the docs/ directory.
- **No Stray Files:** Never put stray Python, test, text, or markdown files in the project root.  
  - Python modules in `src/project_name/`
  - Tests in `tests/`
  - Documentation in `docs/`
  - Examples in `examples/`

---

## Module Requirements

- **Size:** Maximum 500 lines of code per file.
- **Documentation Header:** Every file must include:
  - Description of purpose
  - Links to third-party package documentation
  - Sample input
  - Expected output
- **Validation Function:** Every file needs a main block (`if __name__ == "__main__":`) that tests with real data.

---

## Architecture Principles

- **Function-First:** Prefer simple functions over classes.
- **Class Usage:** Only use classes when:
  - Maintaining state
  - Implementing data validation models
  - Following established design patterns
- **Async Code:** Never use `asyncio.run()` inside functions—only in main blocks.
- **Type Hints:** Use the typing library for all function parameters and return values. Prefer concrete types over Any when possible, but do not reduce readability.
- **No Conditional Imports:**  
  - Never use try/except blocks for required package imports.
  - Only use conditional imports for truly optional features (rare).

---

## Searching

- **ripgrep Preferred:** If available, ALWAYS default to ripgrep over grep.

---

## Validation & Testing

- **Real Data:** Always test with actual data, never fake inputs.
- **Expected Results:** Verify outputs against concrete expected results.
- **No Mocking:** NEVER mock core functionality; MagicMock is strictly forbidden for core tests.
- **Meaningful Assertions:** Use assertions that verify specific expected values.
- **Usage Before Tests:** ALL usage functions MUST successfully output expected results BEFORE any creation of tests.
- **Results Before Lint:** ALL usage functionality MUST produce expected results BEFORE addressing ANY linter warnings.
- **External Research:** If a usage function fails validation 3 times, use external research tools and document findings in comments.
- **No Unconditional "Tests Passed":** NEVER include unconditional "All Tests Passed" messages.

---

## Contribution Workflow

1. Fork the repository and create a feature branch.
2. Follow all coding standards in this document.
3. Ensure all usage functions work with real data before writing tests.
4. Submit a pull request with clear documentation and references.

---

## License

MIT License — see [LICENSE](LICENSE) for details.


