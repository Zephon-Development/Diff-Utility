"""
Unit tests for scripts/check_branch_coverage.py.

Tests coverage enforcement logic with various coverage.json payloads.
"""

import json
import sys
from pathlib import Path

import pytest

# Import from scripts directory
scripts_dir = Path(__file__).parent.parent.parent / "scripts"
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from check_branch_coverage import check_branch_coverage  # noqa: E402


@pytest.fixture
def temp_coverage_file(tmp_path: Path) -> Path:
    """Provide temporary coverage file path."""
    return tmp_path / "coverage.json"


def test_passing_branch_coverage(temp_coverage_file: Path) -> None:
    """Test that coverage above threshold passes."""
    coverage_data = {
        "totals": {
            "num_branches": 100,
            "covered_branches": 80,
        }
    }
    temp_coverage_file.write_text(json.dumps(coverage_data))

    result = check_branch_coverage(temp_coverage_file, threshold=75.0)

    assert result == 0


def test_failing_branch_coverage(temp_coverage_file: Path) -> None:
    """Test that coverage below threshold fails."""
    coverage_data = {
        "totals": {
            "num_branches": 100,
            "covered_branches": 70,
        }
    }
    temp_coverage_file.write_text(json.dumps(coverage_data))

    result = check_branch_coverage(temp_coverage_file, threshold=75.0)

    assert result == 1


def test_exact_threshold_passes(temp_coverage_file: Path) -> None:
    """Test that coverage exactly at threshold passes."""
    coverage_data = {
        "totals": {
            "num_branches": 100,
            "covered_branches": 75,
        }
    }
    temp_coverage_file.write_text(json.dumps(coverage_data))

    result = check_branch_coverage(temp_coverage_file, threshold=75.0)

    assert result == 0


def test_zero_branches_passes(temp_coverage_file: Path) -> None:
    """Test that files with no branches pass (100% by default)."""
    coverage_data = {
        "totals": {
            "num_branches": 0,
            "covered_branches": 0,
        }
    }
    temp_coverage_file.write_text(json.dumps(coverage_data))

    result = check_branch_coverage(temp_coverage_file, threshold=75.0)

    assert result == 0


def test_missing_coverage_file(tmp_path: Path) -> None:
    """Test that missing coverage file returns error."""
    nonexistent_file = tmp_path / "does_not_exist.json"

    result = check_branch_coverage(nonexistent_file, threshold=75.0)

    assert result == 1


def test_malformed_json(temp_coverage_file: Path) -> None:
    """Test that malformed JSON returns error."""
    temp_coverage_file.write_text("{invalid json")

    result = check_branch_coverage(temp_coverage_file, threshold=75.0)

    assert result == 1


def test_missing_totals_key(temp_coverage_file: Path) -> None:
    """Test that missing totals key uses defaults (no branches = pass)."""
    coverage_data: dict[str, dict[str, object]] = {"files": {}}
    temp_coverage_file.write_text(json.dumps(coverage_data))

    result = check_branch_coverage(temp_coverage_file, threshold=75.0)

    # Should pass with 0 branches (100% coverage)
    assert result == 0


def test_missing_branch_keys(temp_coverage_file: Path) -> None:
    """Test that missing branch keys default to 0 (no branches = pass)."""
    coverage_data = {
        "totals": {
            "num_statements": 100,
            "covered_lines": 85,
        }
    }
    temp_coverage_file.write_text(json.dumps(coverage_data))

    result = check_branch_coverage(temp_coverage_file, threshold=75.0)

    # Should pass with 0 branches (100% coverage)
    assert result == 0


def test_fractional_coverage(temp_coverage_file: Path) -> None:
    """Test coverage calculation with fractional percentages."""
    coverage_data = {
        "totals": {
            "num_branches": 3,
            "covered_branches": 2,
        }
    }
    temp_coverage_file.write_text(json.dumps(coverage_data))

    # 2/3 = 66.67%, should fail against 75% threshold
    result = check_branch_coverage(temp_coverage_file, threshold=75.0)

    assert result == 1


def test_custom_threshold(temp_coverage_file: Path) -> None:
    """Test that custom threshold values are respected."""
    coverage_data = {
        "totals": {
            "num_branches": 100,
            "covered_branches": 85,
        }
    }
    temp_coverage_file.write_text(json.dumps(coverage_data))

    # Should pass 80% threshold
    result_pass = check_branch_coverage(temp_coverage_file, threshold=80.0)
    assert result_pass == 0

    # Should fail 90% threshold
    result_fail = check_branch_coverage(temp_coverage_file, threshold=90.0)
    assert result_fail == 1
