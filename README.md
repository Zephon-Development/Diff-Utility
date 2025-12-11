# Python Template

**Version:** 0.1.0  
**Python:** 3.11+  
**License:** Internal use only

---

## Overview

This repository serves as a **standardized Python project template** for greenfield development. It enforces strict type safety, comprehensive test coverage (≥80%), and automated quality gates via CI/CD, in accordance with [`Documentation/CODING_STANDARDS.md`](Documentation/CODING_STANDARDS.md).

**Key features:**
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
cd PythonTemplate

# Create virtual environment
python -m venv .venv

# Activate virtual environment (PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies (editable mode with dev extras)
pip install --upgrade pip
pip install -e ".[dev]"
```

### 3. Verify Installation

```powershell
# Run all quality checks
black --check .
ruff check .
mypy --strict .
pytest --cov=src --cov-branch --cov-fail-under=80
python scripts/check_branch_coverage.py --threshold 75
```

All checks should pass ✅ before you begin development.

---

## Project Structure

```
PythonTemplate/
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
│   └── template/            # Main package (rename for your project)
│       ├── __init__.py
│       ├── py.typed         # PEP 561 type marker
│       └── greeter.py       # Example module
├── tests/
│   └── unit/
│       ├── template/        # Unit tests for src/template
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
pytest

# Run only unit tests
pytest -m unit

# Run with verbose output
pytest -v

# Generate HTML coverage report
pytest --cov-report=html
# Open htmlcov/index.html in browser
```

### Code Quality Checks

```powershell
# Auto-format code
black .

# Lint code
ruff check .

# Auto-fix safe lint issues
ruff check --fix .

# Type check
mypy --strict .
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

## Customizing the Template

### 1. Rename the Package

1. Rename `src/template/` to `src/<your_package>/`
2. Update `pyproject.toml`:
   ```toml
   [project]
   name = "your-project-name"
   description = "Your project description"
   ```
3. Update imports in tests to match new package name

### 2. Add Application Logic

- Place modules in `src/<your_package>/`
- Mirror directory structure in `tests/unit/<your_package>/`
- Follow patterns in `src/template/greeter.py` (type hints, docstrings)

### 3. Configure Coverage Exceptions

To exclude specific lines from coverage (use sparingly):

```python
# Add pragma comment
def debug_only() -> None:
    """This function is not covered in tests."""
    ...  # pragma: no cover
```

See `pyproject.toml` `[tool.coverage.report]` for additional exclusion patterns.

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

**Internal use only** – This template is maintained for organization projects. For questions, contact the platform engineering team or refer to the CODING_STANDARDS.md Lint Allowlist table (§3.4) for policy exceptions.

---

## References

- [CODING_STANDARDS.md](Documentation/CODING_STANDARDS.md) – Complete standards reference
- [PEP 484](https://www.python.org/dev/peps/pep-0484/) – Type hints
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)
