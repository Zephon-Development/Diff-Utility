# Python Coding Standards

**Version:** 2.0  
**Last Updated:** December 11, 2025  
**Applies To:** All new greenfield Python projects

---

## Overview

This document establishes rigorous coding standards for Python projects to support a disciplined CI/CD development workflow. These standards ensure consistent quality, maintainability, and reliability across the codebase.

**Guiding Principles:**
- **Type Safety First** – Leverage PEP 484 type annotations and strict type checking
- **Test-Driven Quality** – Every feature must be tested with ≥80% coverage
- **Documentation as Code** – Keep docs current with implementations
- **Automated Enforcement** – Use tooling to catch issues early

---

## 1. Python Environment Standards

## 1. Python Environment Standards

### 1.1 Python Version

**Required Version:** Python 3.11+

**Rationale:** Python 3.11 provides significant performance improvements, better error messages, and enhanced typing features including `Self` type and variadic generics.

### 1.2 Dependency Management

**Use `pyproject.toml` for all project configuration:**

```toml
[project]
name = "your-project"
version = "0.1.0"
description = "Your project description"
requires-python = ">=3.11"
dependencies = [
    "dependency>=version",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.1.0",
    "black>=23.0.0",
    "mypy>=1.7.0",
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
]
```

**Dependency locking:**
- Use `pip-tools` (`pip-compile`), `uv`, or `poetry` for reproducible builds
- Commit lock files to version control
- Update dependencies regularly and test thoroughly

### 1.3 Virtual Environments

**Always use virtual environments:**

```powershell
# Create virtual environment
python -m venv .venv

# Activate (PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -e ".[dev]"
```

---

## 2. Type Safety Standards

### 2.1 Type Annotations

**All public functions, methods, and classes must have explicit type annotations:**

```python
# ✅ GOOD: Explicit types for parameters and return
def calculate_bonus(level: int, multiplier: float) -> float:
    """Calculate bonus based on level and multiplier."""
    return level * multiplier

# ❌ BAD: Missing type annotations
def calculate_bonus(level, multiplier):
    return level * multiplier
```

### 2.2 Strict Type Checking Configuration

**Required `pyproject.toml` mypy settings:**

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_unimported = false
disallow_any_expr = false
disallow_any_decorated = false
disallow_any_explicit = false
disallow_any_generics = true
disallow_subclassing_any = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
```

### 2.3 Prohibited Patterns

❌ **NEVER use these patterns:**

```python
# ❌ BAD: Using 'Any' without justification
from typing import Any

def process_data(data: Any) -> Any:
    ...

# ❌ BAD: type: ignore without explanation
result = dangerous_operation()  # type: ignore

# ❌ BAD: Untyped function
def fetch_user(user_id):
    return database.get(user_id)
```

### 2.4 Required Patterns

✅ **DO use these patterns:**

```python
from __future__ import annotations

from typing import Protocol, TypedDict, Literal, Annotated

# ✅ GOOD: Explicit type definitions
class UserData(TypedDict):
    id: str
    name: str
    email: str
    created_at: str

# ✅ GOOD: Generic functions with type parameters
from typing import TypeVar

T = TypeVar('T')

def get_data(url: str, parser: type[T]) -> T:
    """Fetch and parse data from URL."""
    ...

# ✅ GOOD: Protocol for structural typing
class Drawable(Protocol):
    def draw(self) -> None: ...

# ✅ GOOD: Literal types for constrained values
Status = Literal['idle', 'loading', 'success', 'error']

# ✅ GOOD: Type guards for runtime checks
def is_user_data(value: object) -> TypeGuard[UserData]:
    """Check if value conforms to UserData structure."""
    return (
        isinstance(value, dict)
        and 'id' in value
        and 'name' in value
        and isinstance(value.get('id'), str)
    )
```

### 2.5 Acceptable Exceptions

**Rare cases where `Any` or `type: ignore` may be used:**

1. **Third-party library with missing stubs:**
   ```python
   # Justification: external_lib lacks type stubs
   from external_lib import process
   result: Any = process(data)  # TODO: Add type stub for external_lib
   ```

2. **Dynamic attribute access:**
   ```python
   # Justification: getattr required for dynamic config loading
   value = getattr(config, key, default)  # type: ignore[arg-type]
   ```

**Requirements for exceptions:**
- Add inline comment explaining why
- Reference issue/ticket if applicable
- Add TODO with removal plan
- Add to Lint Allowlist table (see §3.4)

---

## 3. Linting and Formatting Standards

### 3.1 Required Tools

**Linter:** Ruff (combines flake8, pyflakes, pycodestyle, pylint, and more)  
**Formatter:** Black (or Ruff formatter)  
**Import Sorter:** isort (or Ruff's isort implementation)

### 3.2 Ruff Configuration

**Required `pyproject.toml` settings:**

```toml
[tool.ruff]
target-version = "py311"
line-length = 100
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort
    "N",      # pep8-naming
    "UP",     # pyupgrade
    "ANN",    # flake8-annotations
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "DTZ",    # flake8-datetimez
    "T10",    # flake8-debugger
    "EM",     # flake8-errmsg
    "ISC",    # flake8-implicit-str-concat
    "ICN",    # flake8-import-conventions
    "PIE",    # flake8-pie
    "PT",     # flake8-pytest-style
    "Q",      # flake8-quotes
    "RSE",    # flake8-raise
    "RET",    # flake8-return
    "SIM",    # flake8-simplify
    "TID",    # flake8-tidy-imports
    "PTH",    # flake8-use-pathlib
    "PL",     # pylint
    "RUF",    # ruff-specific rules
]
ignore = [
    "ANN101",  # Missing type annotation for self
    "ANN102",  # Missing type annotation for cls
]

[tool.ruff.per-file-ignores]
"tests/**/*.py" = [
    "ANN",     # Type annotations not required in tests
    "PLR2004", # Magic value used in comparison
]

[tool.ruff.mccabe]
max-complexity = 10
```

### 3.3 Black Configuration

```toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
```

### 3.4 Lint Exception Policy

**Intrinsic Python lint exceptions are permitted only when:**
- The issue is intrinsic to Python runtime or third-party library stubs
- False positives on `typing.Protocol`, dynamic attributes, or runtime metaprogramming
- Documented workarounds for known tooling limitations

**Process for adding exceptions:**

1. **Inline exceptions** – Use for one-off cases:
   ```python
   # Justification: Protocol requires runtime_checkable for isinstance
   # Ticket: PROJ-123
   @runtime_checkable  # noqa: F811
   class MyProtocol(Protocol):
       ...
   ```

2. **File-level exceptions** – Add to `pyproject.toml`:
   ```toml
   [tool.ruff.per-file-ignores]
   "src/legacy_module.py" = ["ANN201"]  # Return types added in PROJ-456
   ```

3. **Project-wide exceptions** – Add to main `ignore` list (requires approval)

**Lint Allowlist Tracking:**

All persistent exceptions must be documented in the table below with required metadata. Review quarterly.

| Rule | Scope | Rationale | Approver | Ticket | Added | Expiry/Review |
|------|-------|-----------|----------|--------|-------|---------------|
| *Example: ANN201* | *src/legacy_module.py* | *Return types deferred pending refactor* | *Maintainer Name* | *PROJ-456* | *2025-12-11* | *2026-03-11* |

---

## 4. Testing Standards

### 4.1 Coverage Requirements

**Minimum Coverage for New Code:**
- **Overall Coverage (lines/statements):** 80%
- **Branch Coverage:** 75%

**Enforcement:** CI pipeline will fail PRs below thresholds for changed files. Overall coverage ≥80% enforced by pytest's `--cov-fail-under=80`. Branch coverage ≥75% enforced by post-test script (`scripts/check_branch_coverage.py`) that reads `coverage.json` and fails when branch percentage drops below threshold.

### 4.2 Test Framework and Tools

**Primary Framework:** pytest with pytest-cov  
**Optional:** hypothesis for property-based testing

**Required `pyproject.toml` configuration:**

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=src",
    "--cov-branch",
    "--cov-report=term-missing:skip-covered",
    "--cov-report=xml",
    "--cov-report=html",
    "--cov-report=json",
    "--cov-fail-under=80",
    "--strict-markers",
    "--tb=short",
]
markers = [
    "unit: Unit tests (fast, isolated)",
    "integration: Integration tests (may be slower)",
    "slow: Tests that take significant time",
]
```

**Coverage configuration:**

```toml
[tool.coverage.run]
branch = true
source = ["src"]
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__pycache__/*",
    "*/site-packages/*",
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
fail_under = 80.0
skip_empty = true
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if TYPE_CHECKING:",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "@abstractmethod",
    "@overload",
]

[tool.coverage.html]
directory = "htmlcov"
```

### 4.3 Test File Organization

```
project/
├── src/
│   ├── services/
│   │   ├── __init__.py
│   │   └── data_processor.py
│   └── models/
│       ├── __init__.py
│       └── user.py
└── tests/
    ├── conftest.py                 # Shared fixtures
    ├── unit/
    │   ├── services/
    │   │   └── test_data_processor.py
    │   └── models/
    │       └── test_user.py
    └── integration/
        └── test_data_pipeline.py
```

### 4.4 Test Naming Conventions

```python
import pytest
from src.services.data_processor import DataProcessor

class TestDataProcessor:
    """Unit tests for DataProcessor service."""
    
    def test_process_valid_data_returns_cleaned_result(self) -> None:
        """Test that valid data is processed and cleaned correctly."""
        processor = DataProcessor()
        result = processor.process({"key": "value"})
        assert result == {"key": "VALUE"}
    
    def test_process_invalid_data_raises_value_error(self) -> None:
        """Test that invalid data raises ValueError."""
        processor = DataProcessor()
        with pytest.raises(ValueError, match="Invalid data"):
            processor.process(None)
    
    @pytest.mark.integration
    def test_process_with_external_api_succeeds(self) -> None:
        """Test processing data from external API."""
        # Integration test implementation
        ...
```

**Pattern:** `test_[method]_[condition]_[expected_result]`

### 4.5 Required Test Categories

#### Unit Tests
- Test individual functions/methods in isolation
- Mock all external dependencies
- Fast execution (< 100ms per test)
- Mark with `@pytest.mark.unit`

```python
import pytest
from unittest.mock import Mock, patch
from src.services.api_client import APIClient

@pytest.mark.unit
def test_fetch_user_returns_parsed_data() -> None:
    """Test user fetch with mocked HTTP response."""
    client = APIClient()
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"id": "123", "name": "Alice"}
        result = client.fetch_user("123")
    
    assert result.name == "Alice"
    mock_get.assert_called_once_with("https://api.example.com/users/123")
```

#### Integration Tests
- Test interactions between modules
- Use test databases or mock APIs when possible
- Slower execution acceptable (< 5s per test)
- Mark with `@pytest.mark.integration`

```python
import pytest
from src.services.data_processor import DataProcessor
from src.repositories.user_repository import UserRepository

@pytest.mark.integration
def test_process_and_store_user_data(test_db: Database) -> None:
    """Test full pipeline from processing to storage."""
    processor = DataProcessor()
    repository = UserRepository(test_db)
    
    raw_data = {"id": "123", "name": "Alice"}
    processed = processor.process(raw_data)
    repository.save(processed)
    
    retrieved = repository.get("123")
    assert retrieved.name == "ALICE"
```

### 4.6 Fixtures and Test Utilities

**Use `conftest.py` for shared fixtures:**

```python
# tests/conftest.py
import pytest
from pathlib import Path
from typing import Generator

@pytest.fixture
def temp_data_dir(tmp_path: Path) -> Path:
    """Provide temporary directory for test data."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir

@pytest.fixture
def sample_user_data() -> dict[str, str]:
    """Provide sample user data for tests."""
    return {
        "id": "test-123",
        "name": "Test User",
        "email": "test@example.com",
    }

@pytest.fixture(autouse=True)
def reset_global_state() -> Generator[None, None, None]:
    """Reset any global state before each test."""
    yield
    # Cleanup code here
```

### 4.7 Mocking Guidelines

**Use mocks for:**
- External APIs and network calls
- File system operations
- Database connections
- Time-dependent logic

```python
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone

# ✅ GOOD: Mock external HTTP calls
@patch('requests.get')
def test_api_call(mock_get: Mock) -> None:
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": "value"}
    # Test implementation

# ✅ GOOD: Mock datetime for reproducible tests
@patch('src.utils.datetime')
def test_time_sensitive_logic(mock_datetime: Mock) -> None:
    fixed_time = datetime(2025, 12, 11, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = fixed_time
    # Test implementation

# ⚠️ AVOID: Over-mocking internal logic (test real behavior when possible)
```

### 4.8 Test Documentation

**Every test module should include:**
- Module-level docstring explaining purpose
- Fixtures documented with types and descriptions
- Complex assertions explained with comments

```python
"""
Unit tests for DataProcessor service.

Tests the processing, validation, and transformation of raw data
from external sources. Mocks all external dependencies.
"""
import pytest
from src.services.data_processor import DataProcessor

@pytest.fixture
def processor() -> DataProcessor:
    """Provide DataProcessor instance for tests."""
    return DataProcessor(timeout=5.0)

class TestDataProcessor:
    """Test suite for DataProcessor."""
    
    def test_complex_transformation(self, processor: DataProcessor) -> None:
        """
        Test multi-step data transformation.
        
        Verifies that nested data structures are flattened correctly
        while preserving key relationships. Related to PROJ-789.
        """
        # Test implementation with explanatory comments
        ...
```

---

## 5. Documentation Standards

### 5.1 Docstrings for Public APIs

**All public functions, classes, and modules must have docstrings following PEP 257:**

```python
"""Module for processing user data from external sources."""

from typing import Protocol

class DataProcessor:
    """
    Process and validate raw data from external APIs.
    
    This class handles data transformation, validation, and sanitization
    for all incoming external data sources.
    
    Attributes:
        timeout: Maximum time in seconds for processing operations.
        strict_mode: Whether to raise errors on validation failures.
    """
    
    def __init__(self, timeout: float = 10.0, strict_mode: bool = True) -> None:
        """
        Initialize DataProcessor with configuration.
        
        Args:
            timeout: Maximum processing time in seconds.
            strict_mode: If True, raise ValidationError on invalid data.
        
        Raises:
            ValueError: If timeout is negative.
        """
        if timeout < 0:
            raise ValueError("Timeout must be non-negative")
        self.timeout = timeout
        self.strict_mode = strict_mode
    
    def process(self, raw_data: dict[str, str]) -> dict[str, str]:
        """
        Process and clean raw input data.
        
        Args:
            raw_data: Dictionary containing unvalidated input data.
        
        Returns:
            Cleaned and validated data dictionary.
        
        Raises:
            ValidationError: If data fails validation in strict mode.
            TimeoutError: If processing exceeds configured timeout.
        
        Example:
            >>> processor = DataProcessor()
            >>> result = processor.process({"key": "value"})
            >>> print(result)
            {'key': 'VALUE'}
        """
        # Implementation
        ...
```

### 5.2 README Maintenance Triggers

**Update README.md when:**
- Adding new features or significant functionality
- Changing setup/installation procedures
- Modifying environment variables or configuration
- Deprecating or removing features

**Required sections:**
- Installation (including Python version requirements)
- Configuration (environment variables, config files)
- Usage examples with code snippets
- Development setup (virtual env, dependencies)
- Testing instructions
- Contributing guidelines
- License

### 5.3 Inline Comment Guidelines

**Use inline comments for:**
- Complex algorithms or business logic
- Workarounds for known issues
- Performance optimizations
- Security-sensitive code

```python
# ✅ GOOD: Explains WHY, not WHAT
# Use LRU cache to avoid repeated API calls during bulk operations
# which can hit rate limits. Cache size tuned for typical workloads.
@lru_cache(maxsize=1000)
def fetch_user_metadata(user_id: str) -> UserMetadata:
    ...

# ❌ BAD: Redundant comment
# Get the user ID
user_id = request.get("user_id")
```

### 5.4 Documentation Lifecycle

**Documentation lives in `Documentation/` hierarchy:**

1. **Active Work** → `Documentation/Active-Plans/`
   - Plans for features in development
   - Move to Records when complete

2. **Completed Work** → `Documentation/Records/`
   - Implementation summaries
   - Bug fix reports
   - Release notes

3. **Stale/Historical** → `Documentation/Archive/`
   - Superseded plans
   - Deprecated feature docs

**Maintenance Schedule:**
- Review Active-Plans monthly
- Archive completed plans within 1 week of feature ship
- Update Reference docs with each major release

### 5.5 Version Management

**Version Bump Checklist:**

When bumping the project version, the following files **must** be updated consistently:

1. **`pyproject.toml`** – Update the `version` field in the `[project]` section
2. **`VERSION.txt`** – Update the version number (single line)
3. **`README.md`** – Update the version badge/reference in the header
4. **`RELEASE_NOTES.md`** – Add a new version section with changes
5. **`src/diff_utility/__init__.py`** – Update the `__version__` variable

**Version Format:** `[MAJOR].[MINOR].[BUGFIX]`
- **MAJOR**: Breaking changes (resets MINOR and BUGFIX to 0)
- **MINOR**: New features (resets BUGFIX to 0)
- **BUGFIX**: Bug fixes (increments only)

**Version Bump Rules:**
- Bug fix: `1.2.3` → `1.2.4`
- Feature release: `1.2.45` → `1.3.0`
- Major release: `1.4.35` → `2.0.0`

**Process:**
1. Every PR must bump the version (even for bug fixes)
2. Update all five files in the same commit
3. Use commit message format: "Bump version to X.Y.Z"
4. Tag the commit with `vX.Y.Z` after merge to main
5. Update RELEASE_NOTES.md with detailed changelog before version bump

---

## 6. Error Handling and Logging Standards

### 6.1 Exception Handling

**Never use bare `except:` clauses:**

```python
# ❌ BAD: Bare except catches everything
try:
    process_data()
except:
    log.error("Something went wrong")

# ✅ GOOD: Specific exception handling
try:
    process_data()
except ValueError as e:
    log.error(f"Invalid data format: {e}")
    raise
except TimeoutError as e:
    log.warning(f"Processing timeout: {e}")
    return default_value
```

### 6.2 Exception Chaining

**Preserve exception context with `from`:**

```python
# ✅ GOOD: Chain exceptions to preserve context
try:
    result = parse_json(raw_data)
except json.JSONDecodeError as e:
    raise DataProcessingError("Failed to parse input data") from e

# ✅ GOOD: Suppress exception chain when intentional
try:
    validate_config()
except ConfigError:
    raise RuntimeError("Invalid configuration") from None
```

### 6.3 Custom Exceptions

**Define domain-specific exceptions:**

```python
class DataProcessingError(Exception):
    """Raised when data processing fails."""
    
    def __init__(self, message: str, data_id: str | None = None) -> None:
        super().__init__(message)
        self.data_id = data_id

class ValidationError(DataProcessingError):
    """Raised when data validation fails."""
    pass
```

### 6.4 Logging Standards

**Use structured logging with the `logging` module:**

```python
import logging

# Configure at application entry point
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

# ✅ GOOD: Structured logging with context
logger.info("Processing user data", extra={"user_id": user_id, "count": len(data)})

# ✅ GOOD: Appropriate log levels
logger.debug("Cache hit for key %s", cache_key)
logger.info("Started data processing pipeline")
logger.warning("Retry attempt %d failed", attempt)
logger.error("Failed to connect to database", exc_info=True)

# ❌ BAD: Using print() in production code
print(f"Processing {user_id}")  # Avoid in production
```

---

## 7. CI/CD Integration

### 7.1 Pre-Commit Requirements

**Must pass locally before committing:**

```powershell
# Format check
black --check .

# Linting
ruff check .

# Type checking
mypy --strict .

# Unit tests with coverage
pytest --cov=src --cov-branch --cov-report=term --cov-report=json --cov-fail-under=80

# Branch coverage check
python scripts/check_branch_coverage.py --threshold 75
```

### 7.2 PR Requirements Checklist

Before submitting a pull request:

- [ ] All tests pass (`pytest`)
- [ ] No type errors (`mypy --strict .`)
- [ ] No lint errors (`ruff check .`)
- [ ] Code formatted (`black --check .`)
- [ ] Code coverage meets thresholds (≥80% overall, ≥75% branches per CI enforcement)
- [ ] Public APIs have docstrings (PEP 257)
- [ ] README updated if user-facing changes
- [ ] Breaking changes documented in PR description
- [ ] Relevant `Documentation/Active-Plans/` updated or moved to Records

### 7.3 Automated Enforcement

**CI Pipeline Gates:**

1. **Format Check** – Black must pass with zero changes
2. **Lint Check** – Ruff must pass with zero errors
3. **Type Check** – mypy strict mode must pass
4. **Unit Tests** – All tests must pass, coverage ≥ 80% lines/functions/statements, ≥75% branches
5. **Build** – Package build must complete successfully

**Example CI commands:**

```powershell
# In CI pipeline (GitHub Actions, Azure Pipelines, etc.)
python -m pip install --upgrade pip
pip install -e ".[dev]"

# Run all checks
black --check .
ruff check .
mypy --strict .
pytest --cov=src --cov-branch --cov-report=term --cov-report=xml --cov-report=json --cov-fail-under=80

# Enforce branch coverage threshold
python scripts/check_branch_coverage.py --threshold 75

# Build package
python -m build
```

### 7.4 Branch Protection Rules

**`main` branch requirements:**
- At least 1 approval from code owner
- All CI checks must pass
- No force pushes
- Up-to-date with base branch

---

## 8. Code Review Standards

### 8.1 Review Checklist

**Reviewers must verify:**

- [ ] Adherence to type safety standards (no `Any` without justification, proper annotations)
- [ ] Test coverage meets minimum thresholds (≥80% overall, ≥75% branches per automated checks)
- [ ] Documentation updated appropriately (docstrings, README)
- [ ] No security vulnerabilities introduced
- [ ] Performance implications considered
- [ ] Error handling comprehensive (no bare except)
- [ ] Code follows DRY principles
- [ ] Consistent with existing patterns
- [ ] Logging appropriate (not using print())
- [ ] Lint exceptions documented in allowlist if needed

### 8.2 Review Workflow

**Process:**
1. **Plan Review (Clive)** – Architecture and approach
2. **Implementation Review (Clive)** – Code quality and standards
3. **Iteration** – Address feedback until no blockers
4. **Greenlight** – Final approval and merge

### 8.3 Feedback Guidelines

**Provide feedback that is:**
- **Specific** – Reference exact file/line numbers
- **Constructive** – Suggest alternatives
- **Prioritized** – Label severity (blocker, major, minor, nit)
- **Actionable** – Clear what needs to change

---

## 9. Best Practices by Domain

### 9.1 Data Classes and Models

```python
from dataclasses import dataclass
from datetime import datetime

# ✅ GOOD: Use dataclasses for data containers
@dataclass(frozen=True)
class UserData:
    """Immutable user data model."""
    id: str
    name: str
    email: str
    created_at: datetime
    
    def __post_init__(self) -> None:
        """Validate data after initialization."""
        if not self.email or "@" not in self.email:
            raise ValueError(f"Invalid email: {self.email}")

# ✅ GOOD: Pydantic for validation-heavy models
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    """User creation request model with validation."""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=18, le=120)
```

### 9.2 API Services and Clients

```python
from typing import Protocol
from abc import ABC, abstractmethod

# ✅ GOOD: Protocol for dependency injection
class APIClient(Protocol):
    """Protocol for API client implementations."""
    
    def fetch(self, url: str) -> dict[str, object]:
        """Fetch data from API endpoint."""
        ...

# ✅ GOOD: Single Responsibility Principle
class UserService:
    """Service for user-related operations."""
    
    def __init__(self, client: APIClient, cache_ttl: int = 300) -> None:
        if cache_ttl < 0:
            raise ValueError("Cache TTL must be non-negative")
        self._client = client
        self._cache_ttl = cache_ttl
    
    def get_user(self, user_id: str) -> UserData:
        """
        Fetch user data by ID.
        
        Args:
            user_id: Unique user identifier.
        
        Returns:
            User data object.
        
        Raises:
            UserNotFoundError: If user does not exist.
            APIError: If API request fails.
        """
        # Implementation
        ...
```

### 9.3 Async/Await Patterns

```python
import asyncio
from typing import AsyncIterator

# ✅ GOOD: Explicit async functions
async def fetch_users(user_ids: list[str]) -> list[UserData]:
    """Fetch multiple users concurrently."""
    tasks = [fetch_user(user_id) for user_id in user_ids]
    return await asyncio.gather(*tasks)

# ✅ GOOD: Async context managers
class AsyncDatabaseConnection:
    """Async database connection with context manager."""
    
    async def __aenter__(self) -> "AsyncDatabaseConnection":
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.disconnect()

# ✅ GOOD: Async generators
async def stream_data() -> AsyncIterator[DataChunk]:
    """Stream data asynchronously."""
    async with AsyncDatabaseConnection() as conn:
        async for row in conn.query("SELECT * FROM data"):
            yield DataChunk.from_row(row)
```

### 9.4 State Management

```python
from enum import Enum
from typing import TypedDict, Literal

# ✅ GOOD: Enum for finite states
class ProcessState(Enum):
    """States for data processing pipeline."""
    IDLE = "idle"
    LOADING = "loading"
    PROCESSING = "processing"
    SUCCESS = "success"
    ERROR = "error"

# ✅ GOOD: TypedDict with Literal for discriminated unions
class IdleState(TypedDict):
    status: Literal["idle"]

class LoadingState(TypedDict):
    status: Literal["loading"]
    progress: float

class SuccessState(TypedDict):
    status: Literal["success"]
    data: dict[str, object]

class ErrorState(TypedDict):
    status: Literal["error"]
    error: str

# Union type for all states
ProcessingState = IdleState | LoadingState | SuccessState | ErrorState
```

---

## 10. Enforcement

### 10.1 Agent Workflow Integration

**All agents must reference these standards:**

- **Tracy (Planner)** – Include relevant sections in plans
- **Claudette/Georgina (Implementers)** – Adhere to standards during coding
- **Clive (Reviewer)** – Verify compliance during review

### 10.2 Onboarding Requirements

**New contributors must:**
1. Read this document thoroughly
2. Complete Python typing and testing tutorial
3. Submit sample PR demonstrating standards compliance

### 10.3 Standards Evolution

**This document is versioned and maintained:**
- Propose changes via PR to `Documentation/CODING_STANDARDS.md`
- Requires approval from project maintainer
- Announce changes in team channels
- Update agent prompts to reflect changes

---

## 11. Resources

### 11.1 Internal Documentation

- `Documentation/Active-Plans/` – Current feature development plans
- `Documentation/Records/` – Implementation summaries and completed work
- `Documentation/Archive/` – Historical and superseded documentation

### 11.2 External Resources

- [Python Type Hints Documentation](https://docs.python.org/3/library/typing.html)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Code Style](https://black.readthedocs.io/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)

---

## Appendix A: Configuration Files

### pyproject.toml Complete Example

```toml
[project]
name = "your-project"
version = "0.1.0"
description = "Your project description"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.1.0",
    "black>=23.0.0",
    "mypy>=1.7.0",
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.21.0",
]

[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.ruff]
target-version = "py311"
line-length = 100
select = [
    "E", "W",  # pycodestyle
    "F",       # pyflakes
    "I",       # isort
    "N",       # pep8-naming
    "UP",      # pyupgrade
    "ANN",     # flake8-annotations
    "B",       # flake8-bugbear
    "C4",      # flake8-comprehensions
    "DTZ",     # flake8-datetimez
    "T10",     # flake8-debugger
    "EM",      # flake8-errmsg
    "ISC",     # flake8-implicit-str-concat
    "ICN",     # flake8-import-conventions
    "PIE",     # flake8-pie
    "PT",      # flake8-pytest-style
    "Q",       # flake8-quotes
    "RSE",     # flake8-raise
    "RET",     # flake8-return
    "SIM",     # flake8-simplify
    "TID",     # flake8-tidy-imports
    "PTH",     # flake8-use-pathlib
    "PL",      # pylint
    "RUF",     # ruff-specific rules
]
ignore = [
    "ANN101",  # Missing type annotation for self
    "ANN102",  # Missing type annotation for cls
]

[tool.ruff.per-file-ignores]
"tests/**/*.py" = [
    "ANN",     # Type annotations not required in tests
    "PLR2004", # Magic value used in comparison
]

[tool.ruff.mccabe]
max-complexity = 10

[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
disallow_subclassing_any = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=src",
    "--cov-branch",
    "--cov-report=term-missing:skip-covered",
    "--cov-report=xml",
    "--cov-report=html",
    "--cov-report=json",
    "--cov-fail-under=80",
    "--strict-markers",
    "--tb=short",
]
markers = [
    "unit: Unit tests (fast, isolated)",
    "integration: Integration tests (may be slower)",
    "slow: Tests that take significant time",
]

[tool.coverage.run]
branch = true
source = ["src"]
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__pycache__/*",
    "*/site-packages/*",
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
fail_under = 80.0
skip_empty = true
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if TYPE_CHECKING:",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "@abstractmethod",
    "@overload",
]

[tool.coverage.html]
directory = "htmlcov"
```

---

**Version History:**
- v2.0 (2025-12-11) – Python-specific standards for greenfield projects
- v1.0 (2025-11-30) – Initial TypeScript standards (superseded for Python projects)
