#!/usr/bin/env python3
"""Local CI test script - runs the same checks as GitHub Actions CI."""

from __future__ import annotations

import subprocess
import sys


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return True if successful."""
    print(f"\n--- {description} ---")
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        print("FAILED:")
        print(result.stdout)
        print(result.stderr)
        return False
    print("PASSED")
    return True


def main() -> None:
    """Run all CI checks."""
    print("Running local CI checks...")

    checks = [
        (["python", "-m", "black", "--check", "."], "Format check (black)"),
        (["python", "-m", "ruff", "check", "."], "Lint (ruff)"),
        (["python", "-m", "mypy", "--strict", "."], "Type check (mypy)"),
        (
            [
                "python",
                "-m",
                "pytest",
                "--cov=src",
                "--cov-branch",
                "--cov-report=term-missing:skip-covered",
                "--cov-report=xml",
                "--cov-report=html",
                "--cov-report=json",
                "--cov-fail-under=80",
            ],
            "Tests with coverage",
        ),
        (
            ["python", "scripts/check_branch_coverage.py", "--threshold", "75"],
            "Enforce branch coverage",
        ),
    ]

    all_passed = True
    for cmd, desc in checks:
        if not run_command(cmd, desc):
            all_passed = False

    if all_passed:
        print("\n✅ All CI checks passed!")
        sys.exit(0)
    else:
        print("\n❌ Some CI checks failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
