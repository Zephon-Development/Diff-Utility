"""Performance tests for diff operations on large files."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from diff_utility.diff import diff_files


@pytest.mark.performance
def test_10k_line_file_performance(tmp_path: Path) -> None:
    """Test that diff on 10k-line files completes within 1 second."""
    file1 = tmp_path / "large1.txt"
    file2 = tmp_path / "large2.txt"

    # Create 10k line files with one line inserted in the middle
    lines1 = [f"Line {i:05d}\n" for i in range(10000)]
    lines2 = [*lines1[:5000], "INSERTED LINE\n", *lines1[5000:]]

    file1.write_text("".join(lines1), encoding="utf-8")
    file2.write_text("".join(lines2), encoding="utf-8")

    # Measure performance
    start_time = time.perf_counter()
    result = diff_files(file1, file2)
    elapsed = time.perf_counter() - start_time

    # Should complete in less than 1 second
    assert elapsed < 1.0, f"Diff took {elapsed:.3f}s, expected < 1.0s"

    # Should only report the one insertion
    assert result.count("---") == 1
    assert "++INSERTED LINE++" in result

    print(f"\nPerformance: 10k lines processed in {elapsed:.3f}s")


@pytest.mark.performance
def test_50k_line_file_performance(tmp_path: Path) -> None:
    """Test performance with very large 50k-line files."""
    file1 = tmp_path / "verylarge1.txt"
    file2 = tmp_path / "verylarge2.txt"

    # Create 50k line files with one deletion
    lines1 = [f"Line {i:05d}\n" for i in range(50000)]
    lines2 = lines1[:25000] + lines1[25001:]  # Delete one line

    file1.write_text("".join(lines1), encoding="utf-8")
    file2.write_text("".join(lines2), encoding="utf-8")

    # Measure performance
    start_time = time.perf_counter()
    result = diff_files(file1, file2)
    elapsed = time.perf_counter() - start_time

    # Should only report the one deletion
    assert result.count("---") == 1
    assert "--Line 25000--" in result

    print(f"\nPerformance: 50k lines processed in {elapsed:.3f}s")
