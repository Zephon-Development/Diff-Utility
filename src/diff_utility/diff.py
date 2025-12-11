"""Core diff engine for comparing text files with custom whitespace handling.

This module provides functions for reading files, normalizing whitespace,
comparing lines, and annotating differences with ++/-- markers.
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from pathlib import Path


def read_lines(path: Path) -> list[str]:
    """Read all lines from a file, preserving content but removing trailing newlines.

    Args:
        path: Path to the file to read.

    Returns:
        List of lines with trailing newlines removed.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read.
        OSError: For other I/O errors.
    """
    with path.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def normalize_line(line: str) -> str:
    """Normalize whitespace in a line for comparison purposes.

    Collapses runs of whitespace characters (space, tab, etc.) into single spaces
    while preserving leading and trailing spaces. This allows quantity-insensitive
    comparison while still detecting added/removed whitespace boundaries.

    Args:
        line: The line to normalize.

    Returns:
        Normalized line with collapsed internal whitespace.

    Examples:
        >>> normalize_line("Hello   World")
        'Hello World'
        >>> normalize_line("Hello\\tWorld")
        'Hello World'
        >>> normalize_line("  Hello World  ")
        '  Hello World  '
    """
    return re.sub(r"\s+", " ", line)


def lines_equal_norm(a: str, b: str) -> bool:
    """Check if two lines are equal after normalization.

    Args:
        a: First line to compare.
        b: Second line to compare.

    Returns:
        True if normalized lines are equal, False otherwise.
    """
    return normalize_line(a) == normalize_line(b)


def _tokenize(line: str) -> list[str]:
    """Split a line into tokens, keeping whitespace sequences as separate tokens.

    Args:
        line: The line to tokenize.

    Returns:
        List of tokens alternating between non-whitespace and whitespace sequences.

    Examples:
        >>> _tokenize("Hello World")
        ['Hello', ' ', 'World']
        >>> _tokenize("Hello  World")
        ['Hello', '  ', 'World']
    """
    return re.findall(r"\s+|\S+", line)


def annotate_changes(line1: str, line2: str) -> str:
    """Annotate differences between two lines with ++/-- markers.

    Tokenizes both lines and uses difflib.SequenceMatcher to identify additions
    and deletions. Additions from line2 are wrapped with ++...++, deletions from
    line1 are wrapped with --...--.

    Args:
        line1: Original line (file 1).
        line2: Modified line (file 2).

    Returns:
        Annotated version of line2 with markers showing changes.

    Examples:
        >>> annotate_changes("Hello World", "Hello Beautiful World")
        'Hello ++Beautiful++ World'
        >>> annotate_changes("Hello World", "Hello")
        'Hello --World--'
    """
    tokens1 = _tokenize(line1)
    tokens2 = _tokenize(line2)

    matcher = SequenceMatcher(None, tokens1, tokens2)
    result: list[str] = []

    for opcode, i1, i2, j1, j2 in matcher.get_opcodes():
        if opcode == "equal":
            # Tokens are the same, emit as-is
            result.extend(tokens2[j1:j2])
        elif opcode == "insert":
            # Tokens only in file2 (additions)
            for token in tokens2[j1:j2]:
                result.append(f"++{token}++")
        elif opcode == "delete":
            # Tokens only in file1 (deletions)
            for token in tokens1[i1:i2]:
                result.append(f"--{token}--")
        elif opcode == "replace":
            # Tokens differ: treat as delete + insert
            for token in tokens1[i1:i2]:
                result.append(f"--{token}--")
            for token in tokens2[j1:j2]:
                result.append(f"++{token}++")

    return "".join(result)


def diff_lines(lines1: list[str], lines2: list[str]) -> list[str]:
    """Generate diff output blocks for changed lines.

    Compares lines from two files and yields formatted blocks for lines that differ.
    Identical lines (after normalization) are skipped.

    Args:
        lines1: Lines from file 1.
        lines2: Lines from file 2.

    Returns:
        List of output lines representing the diff.

    Format for each changed line:
        ---
        [file 1 line]
        [file 2 line]

        [changes]
    """
    output: list[str] = []
    max_lines = max(len(lines1), len(lines2))

    for i in range(max_lines):
        line1 = lines1[i] if i < len(lines1) else ""
        line2 = lines2[i] if i < len(lines2) else ""

        # Skip if lines are equal after normalization
        if lines_equal_norm(line1, line2):
            continue

        # Emit diff block for changed line
        output.append("---")
        output.append(line1)
        output.append(line2)
        output.append("")
        output.append(annotate_changes(line1, line2))
        output.append("")

    return output


def diff_files(path1: Path, path2: Path) -> str:
    """Compare two files and generate diff output.

    Args:
        path1: Path to the first file.
        path2: Path to the second file.

    Returns:
        Formatted diff output as a string.

    Raises:
        FileNotFoundError: If either file does not exist.
        PermissionError: If either file cannot be read.
        OSError: For other I/O errors.
    """
    lines1 = read_lines(path1)
    lines2 = read_lines(path2)

    diff_output = diff_lines(lines1, lines2)
    return "\n".join(diff_output)
