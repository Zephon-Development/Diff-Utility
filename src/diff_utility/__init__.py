"""
Diff Utility - CLI tool for comparing text files line by line.

This package provides a custom diff utility with whitespace-aware comparison
and formatted output.
"""

__version__ = "0.1.0"

__all__ = [
    "DiffResult",
    "__version__",
    "compare_files",
    "compare_lines",
    "format_diff_output",
]

from diff_utility.diff_engine import (
    DiffResult,
    compare_files,
    compare_lines,
    format_diff_output,
)
