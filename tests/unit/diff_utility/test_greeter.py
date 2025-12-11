"""
Unit tests for diff_utility.greeter module.

Tests demonstrate comprehensive coverage (≥80%) per CODING_STANDARDS.md §4.1.
"""

import pytest

from diff_utility.greeter import greeter


def test_greeter_informal_default() -> None:
    """Test informal greeting with default parameters."""
    result = greeter("World")
    assert result == "Hello, World!"


def test_greeter_informal_explicit() -> None:
    """Test informal greeting with explicit formal=False."""
    result = greeter("Alice", formal=False)
    assert result == "Hello, Alice!"


def test_greeter_formal() -> None:
    """Test formal greeting style."""
    result = greeter("Dr. Smith", formal=True)
    assert result == "Good day, Dr. Smith."


def test_greeter_strips_whitespace() -> None:
    """Test that leading/trailing whitespace is stripped from name."""
    result = greeter("  Bob  ")
    assert result == "Hello, Bob!"


def test_greeter_strips_whitespace_formal() -> None:
    """Test whitespace stripping in formal mode."""
    result = greeter("  Professor Jones  ", formal=True)
    assert result == "Good day, Professor Jones."


def test_greeter_empty_string_raises() -> None:
    """Test that empty string raises ValueError."""
    with pytest.raises(ValueError, match="Name cannot be empty or whitespace"):
        greeter("")


def test_greeter_whitespace_only_raises() -> None:
    """Test that whitespace-only string raises ValueError."""
    with pytest.raises(ValueError, match="Name cannot be empty or whitespace"):
        greeter("   ")


def test_greeter_tab_whitespace_raises() -> None:
    """Test that tab/newline whitespace raises ValueError."""
    with pytest.raises(ValueError, match="Name cannot be empty or whitespace"):
        greeter("\t\n")
