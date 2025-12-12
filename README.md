# Diff Utility

**Version:** 1.1.1
**Python:** 3.11+  
**License:** GPL-3.0-or-later

---

## Overview

A command-line tool for comparing two text files line by line with intelligent whitespace handling. The tool ignores differences in whitespace quantity while detecting new or missing whitespace boundaries, providing clear annotations of additions and deletions.

**Key features:**
- ✅ Smart line insertion/deletion detection (no cascading false positives)
- ✅ Intelligent whitespace normalization (ignores quantity, detects boundaries)
- ✅ Supports UTF-8, cp1252 and latin-1 encoding
- ✅ Custom diff output format with `++` addition and `--` deletion markers
- ✅ Skips identical lines automatically
- ✅ Strict type checking with mypy (no `Any` types)
- ✅ Linting and formatting with Ruff + Black
- ✅ Branch coverage enforcement (≥75%)
- ✅ Reproducible dependency locking (pip-tools)
- ✅ GitHub Actions CI workflow (self-hosted runner: Grimslade)

---

## Quick Start

### 1. Prerequisites

- Python 3.11 or later
- Access to the **Grimslade** self-hosted runner (organization-level, required for CI)
- Git

### 2. Initial Setup

```powershell
# Clone the repository
git clone <repository-url>
cd Diff-Utility

# Create virtual environment
python -m venv .venv

# Activate virtual environment (PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies (editable mode with dev extras)
pip install --upgrade pip
pip install -e ".[dev]"
```

### 3. Usage

Compare two text files:

```powershell
# Basic usage
diff-utility file1.txt file2.txt

# Or using Python module
python -m diff_utility.cli file1.txt file2.txt
```

**Output Format:**

For each changed line, the tool outputs:
```
---
[file 1 line]
[file 2 line]

[changes]
```

Where `[changes]` shows file2's content with:
- `++text++` marking additions (text present in file2 but not file1)
- `--text--` marking deletions (text present in file1 but not file2)

**Example:**

file1.txt:
```
Hello World.How are you
```

file2.txt:
```
Hello World. How are you
```

Output:
```
---
File A: Hello World.How are you
File B: Hello World. How are you

Hello --World.How--++World.++++ ++How++ are you
```

**Line Insertion/Deletion Detection:**

The diff engine uses sequence matching to detect when entire lines are inserted or deleted, preventing false positives for subsequent lines.

file1.txt:
```
Line 1
Line 3
Line 4
```

file2.txt:
```
Line 1
Line 2
Line 3
Line 4
```

Output:
```
---
File A: 
File B: Line 2

+Line 2++
```

Notice that Lines 3 and 4 are **not** flagged as different - only the actual inserted line is shown. This ensures accurate diffs even for large files with scattered changes.

### 4. Whitespace Handling

The tool uses intelligent whitespace normalization:

- **Ignores quantity differences:** `"Hello   World"` vs `"Hello World"` are considered equal
- **Detects boundary changes:** `"Hello World.How"` vs `"Hello World. How"` shows the added space
- **Preserves original output:** All diff annotations show the actual content from the files
- **Normalizes for comparison only:** Tabs, spaces, and multiple whitespace characters are collapsed to single spaces when checking equality

This allows the tool to focus on meaningful content changes while being flexible about formatting.

### 5. Verify Installation

```powershell
# Run all quality checks
python -m black --check .
python -m ruff check .
python -m mypy --strict .
python -m pytest --cov=src --cov-branch --cov-fail-under=80
python scripts/check_branch_coverage.py --threshold 75
```

All checks should pass ✅ before you begin development.

---

## Project Structure

```
Diff-Utility/
├── .github/
│   ├── agents/              # AI agent configuration files
│   └── workflows/
│       └── ci.yml           # CI pipeline (lint/type/test/coverage)
├── Documentation/
│   ├── CODING_STANDARDS.md  # **Primary standards reference**
│   └── Active-Plans/        # Planning documents
├── scripts/
│   └── check_branch_coverage.py  # Branch coverage enforcement
├── src/
│   └── diff_utility/        # Main package
│       ├── __init__.py      # Public API exports
│       ├── py.typed         # PEP 561 type marker
│       ├── diff.py          # Core diff engine
│       └── cli.py           # Command-line interface
├── tests/
│   └── unit/
│       ├── diff_utility/    # Unit tests for src/diff_utility
│       └── test_check_branch_coverage.py
├── pyproject.toml           # Project metadata & tool config
├── requirements.txt         # Locked runtime dependencies
├── requirements-dev.txt     # Locked dev dependencies
└── README.md                # This file
```

---

## Development Workflow

### Running Tests

```powershell
# Run all tests with coverage
python -m pytest

# Run only unit tests
python -m pytest -m unit

# Run with verbose output
python -m pytest -v

# Generate HTML coverage report
python -m pytest --cov-report=html
# Open htmlcov/index.html in browser
```

### Code Quality Checks

```powershell
# Auto-format code
python -m black .

# Lint code
python -m ruff check .

# Auto-fix safe lint issues
python -m ruff check --fix .

# Type check
python -m mypy --strict .
```

### Updating Dependencies

When adding/removing dependencies in `pyproject.toml`:

```powershell
# Regenerate lock files
pip-compile pyproject.toml -o requirements.txt
pip-compile --extra dev pyproject.toml -o requirements-dev.txt

# Sync environment with updated locks
pip-sync requirements-dev.txt

# Re-install project in editable mode
pip install -e ".[dev]"
```

**Important:** Always commit `requirements.txt` and `requirements-dev.txt` to ensure reproducible builds (see CODING_STANDARDS.md §1.2).

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request to `main`:

1. **Format check** – Black ensures consistent code style
2. **Lint** – Ruff catches code smells and PEP violations
3. **Type check** – mypy enforces strict type safety
4. **Tests** – pytest with branch coverage reports
5. **Coverage enforcement** – Fails if overall <80% or branch <75%

**Runner Requirements:**  
The workflow uses the **Grimslade** self-hosted runner (organization-level). This runner is maintained centrally and automatically available to all repositories in the organization. External users reusing this template outside the organization must replace `runs-on: [self-hosted, Grimslade]` with a GitHub-hosted runner (e.g., `ubuntu-latest`).

---

## Standards Compliance

All code **must** adhere to [`Documentation/CODING_STANDARDS.md`](Documentation/CODING_STANDARDS.md):

- **§2 Type Safety:** All functions require explicit type annotations; `Any` is prohibited except with documented justification
- **§3 Linting:** Ruff and Black enforce consistent style; max cyclomatic complexity = 10
- **§4 Testing:** ≥80% line coverage, ≥75% branch coverage mandatory for all new code
- **§5 Documentation:** Public APIs require Google-style docstrings

Review the full standards document before contributing.

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'src'`

Ensure you installed the project in editable mode:
```powershell
pip install -e ".[dev]"
```

### CI fails with "Virtualenv not found"

The Grimslade runner caches virtual environments. If the workflow fails, check that the runner has sufficient disk space and that `pyproject.toml` hasn't been corrupted.

### Type errors in third-party libraries

If a library lacks type stubs, create a `py.typed` marker in a local stub package or add to `[tool.mypy]` `exclude` in `pyproject.toml` (document reason per §2.5).

---

## License & Support

**License:** GPL-3.0-or-later  

---

## References

- [CODING_STANDARDS.md](Documentation/CODING_STANDARDS.md) – Complete standards reference
- [PEP 484](https://www.python.org/dev/peps/pep-0484/) – Type hints
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)
