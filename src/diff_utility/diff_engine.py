"""
Core diff engine for comparing text files line by line.

This module implements custom diff logic with whitespace-aware comparison
and formatted output per CODING_STANDARDS.md.
"""

import re
from dataclasses import dataclass


@dataclass
class DiffResult:
    """
    Represents the result of comparing two lines.

    Attributes:
        file1_line: Original line from file 1.
        file2_line: Corresponding line from file 2.
        changes_line: File 2 line with ++ ++ around additions and -- -- around deletions.
        is_identical: Whether the lines are considered identical.
    """

    file1_line: str
    file2_line: str
    changes_line: str
    is_identical: bool


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace for comparison purposes.

    Reduces multiple consecutive whitespace characters to single spaces,
    while preserving the presence/absence of whitespace.

    Args:
        text: The text to normalize.

    Returns:
        The text with normalized whitespace.

    Examples:
        >>> normalize_whitespace("d.  H")
        'd. H'
        >>> normalize_whitespace("d.H")
        'd.H'
    """
    # Replace multiple whitespace characters with single space
    return re.sub(r"\s+", " ", text)


def are_lines_identical(line1: str, line2: str) -> bool:
    """
    Compare two lines with whitespace-aware logic.

    Lines are considered identical if they have the same normalized whitespace.
    This means "d. H" and "d.  H" are the same, but "d.H" and "d. H" are different.

    Args:
        line1: First line to compare.
        line2: Second line to compare.

    Returns:
        True if lines are identical with normalized whitespace, False otherwise.

    Examples:
        >>> are_lines_identical("d. H", "d.  H")
        True
        >>> are_lines_identical("d.H", "d. H")
        False
    """
    return normalize_whitespace(line1) == normalize_whitespace(line2)


def tokenize_line(line: str) -> list[str]:
    """
    Tokenize a line into words and whitespace segments.

    Args:
        line: The line to tokenize.

    Returns:
        List of tokens (words and whitespace).

    Examples:
        >>> tokenize_line("hello world")
        ['hello', ' ', 'world']
        >>> tokenize_line("d.H")
        ['d.H']
    """
    # Split on whitespace while keeping the whitespace
    tokens = re.split(r"(\s+)", line)
    return [t for t in tokens if t]  # Remove empty strings


def compute_diff_changes(line1: str, line2: str) -> str:
    """
    Compute the changes line showing additions and deletions.

    The changes line is based on file2_line with markers:
    - ++ ++ surrounding additions (present in line2 but not in line1)
    - -- -- surrounding deletions (present in line1 but not in line2)

    Args:
        line1: Original line from file 1.
        line2: Modified line from file 2.

    Returns:
        Line with change markers.

    Examples:
        >>> compute_diff_changes("hello", "hello world")
        'hello ++ world ++'
        >>> compute_diff_changes("hello world", "hello")
        'hello -- world --'
    """
    # Normalize both lines for comparison
    norm1 = normalize_whitespace(line1)
    norm2 = normalize_whitespace(line2)

    # If identical after normalization, return line2 as-is
    if norm1 == norm2:
        return line2

    # Tokenize both lines
    tokens1 = tokenize_line(norm1)
    tokens2 = tokenize_line(norm2)

    # Simple token-based diff
    # This is a simplified approach: we'll mark tokens in line2 that aren't in line1 as additions
    # and tokens in line1 that aren't in line2 as deletions

    # Create sets for comparison (excluding whitespace for now)
    words1 = {t for t in tokens1 if not t.isspace()}
    words2 = {t for t in tokens2 if not t.isspace()}

    # Find additions (in line2 but not in line1) and deletions (in line1 but not in line2)
    additions = words2 - words1
    deletions = words1 - words2

    # Build the changes line
    result_parts: list[str] = []
    for token in tokens2:
        if token.isspace():
            result_parts.append(token)
        elif token in additions:
            result_parts.append(f"++ {token} ++")
        else:
            result_parts.append(token)

    # Add deletions at the end
    for deletion in deletions:
        result_parts.append(f" -- {deletion} --")

    return "".join(result_parts)


def compare_lines(line1: str, line2: str) -> DiffResult:
    """
    Compare two lines and generate a diff result.

    Args:
        line1: Line from file 1.
        line2: Line from file 2.

    Returns:
        DiffResult containing comparison information.

    Examples:
        >>> result = compare_lines("hello", "hello")
        >>> result.is_identical
        True
        >>> result = compare_lines("hello", "world")
        >>> result.is_identical
        False
    """
    is_identical = are_lines_identical(line1, line2)

    if is_identical:
        return DiffResult(
            file1_line=line1,
            file2_line=line2,
            changes_line=line2,
            is_identical=True,
        )

    changes_line = compute_diff_changes(line1, line2)

    return DiffResult(
        file1_line=line1,
        file2_line=line2,
        changes_line=changes_line,
        is_identical=False,
    )


def compare_files(file1_lines: list[str], file2_lines: list[str]) -> list[DiffResult]:
    """
    Compare two files line by line.

    Args:
        file1_lines: Lines from file 1.
        file2_lines: Lines from file 2.

    Returns:
        List of DiffResult objects for all line pairs.

    Examples:
        >>> results = compare_files(["hello"], ["hello"])
        >>> len(results)
        1
        >>> results[0].is_identical
        True
    """
    # Pad the shorter file with empty strings
    max_lines = max(len(file1_lines), len(file2_lines))
    file1_padded = file1_lines + [""] * (max_lines - len(file1_lines))
    file2_padded = file2_lines + [""] * (max_lines - len(file2_lines))

    results = []
    for line1, line2 in zip(file1_padded, file2_padded, strict=True):
        results.append(compare_lines(line1, line2))

    return results


def format_diff_output(results: list[DiffResult]) -> str:
    """
    Format diff results into the custom output format.

    Only includes changed lines (skips identical lines).

    Args:
        results: List of DiffResult objects.

    Returns:
        Formatted diff output string.

    Examples:
        >>> result = DiffResult("hello", "world", "++ world ++", False)
        >>> output = format_diff_output([result])
        >>> "---" in output
        True
    """
    output_parts = []

    for result in results:
        if not result.is_identical:
            output_parts.append("---")
            output_parts.append(result.file1_line)
            output_parts.append(result.file2_line)
            output_parts.append("")
            output_parts.append(result.changes_line)
            output_parts.append("")

    return "\n".join(output_parts)
