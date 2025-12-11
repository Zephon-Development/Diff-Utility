"""
Branch coverage enforcement script for CI/CD pipelines.

This script reads pytest-cov's coverage.json output and fails the build
if branch coverage falls below the configured threshold.

Usage:
    python scripts/check_branch_coverage.py --threshold 75 [--coverage-file .coverage.json]
"""

import argparse
import json
import sys
from pathlib import Path


def check_branch_coverage(coverage_file: Path, threshold: float) -> int:
    """
    Check branch coverage against threshold.

    Args:
        coverage_file: Path to coverage JSON report.
        threshold: Minimum required branch coverage percentage.

    Returns:
        Exit code: 0 if passing, 1 if failing.
    """
    if not coverage_file.exists():
        print(f"ERROR: Coverage file not found: {coverage_file}", file=sys.stderr)
        return 1

    try:
        with coverage_file.open() as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in coverage file: {e}", file=sys.stderr)
        return 1

    totals = data.get("totals", {})

    # Extract branch coverage data
    num_branches = totals.get("num_branches", 0)
    covered_branches = totals.get("covered_branches", 0)

    # Handle files with no branches
    if num_branches == 0:
        print("No branches found in coverage report (100% by default)")
        branch_pct_float = 100.0
    else:
        branch_pct_float = (covered_branches / num_branches) * 100.0

    print(f"Branch coverage: {branch_pct_float:.2f}%")
    print(f"Required threshold: {threshold:.2f}%")

    if branch_pct_float < threshold:
        print(
            f"FAILED: Branch coverage {branch_pct_float:.2f}% is below threshold {threshold:.2f}%",
            file=sys.stderr,
        )
        return 1

    print("PASSED: Branch coverage meets threshold")
    return 0


def main() -> int:
    """Parse arguments and run branch coverage check."""
    parser = argparse.ArgumentParser(
        description="Check branch coverage threshold from coverage.json"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=75.0,
        help="Minimum branch coverage percentage (default: 75.0)",
    )
    parser.add_argument(
        "--coverage-file",
        type=Path,
        default=Path("coverage.json"),
        help="Path to coverage JSON file (default: coverage.json)",
    )

    args = parser.parse_args()

    return check_branch_coverage(args.coverage_file, args.threshold)


if __name__ == "__main__":
    sys.exit(main())
