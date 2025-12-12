"""Diff Utility - A command-line tool for comparing text files with custom whitespace handling.

This package provides functionality to compare two text files line by line,
with intelligent whitespace handling that ignores quantity differences while
detecting new or missing whitespace boundaries.
"""

from __future__ import annotations

from diff_utility.diff import (
    annotate_changes,
    diff_files,
    diff_lines,
    lines_equal_norm,
    normalize_line,
    read_lines,
)

__version__ = "1.2.3"

__all__ = [
    "__version__",
    "annotate_changes",
    "diff_files",
    "diff_lines",
    "lines_equal_norm",
    "normalize_line",
    "read_lines",
]
