"""
Unit tests for diff_utility.diff_engine module.

Tests demonstrate comprehensive coverage (≥80%) per CODING_STANDARDS.md §4.1.
"""


from diff_utility.diff_engine import (
    DiffResult,
    are_lines_identical,
    compare_files,
    compare_lines,
    compute_diff_changes,
    format_diff_output,
    normalize_whitespace,
    tokenize_line,
)


class TestNormalizeWhitespace:
    """Tests for normalize_whitespace function."""

    def test_single_space_unchanged(self) -> None:
        """Test that single spaces are preserved."""
        result = normalize_whitespace("hello world")
        assert result == "hello world"

    def test_multiple_spaces_normalized(self) -> None:
        """Test that multiple spaces are reduced to single space."""
        result = normalize_whitespace("hello  world")
        assert result == "hello world"

    def test_tabs_normalized(self) -> None:
        """Test that tabs are normalized to single space."""
        result = normalize_whitespace("hello\tworld")
        assert result == "hello world"

    def test_mixed_whitespace_normalized(self) -> None:
        """Test that mixed whitespace is normalized."""
        result = normalize_whitespace("hello \t  world")
        assert result == "hello world"

    def test_leading_whitespace_normalized(self) -> None:
        """Test that leading whitespace is normalized."""
        result = normalize_whitespace("  hello")
        assert result == " hello"

    def test_trailing_whitespace_normalized(self) -> None:
        """Test that trailing whitespace is normalized."""
        result = normalize_whitespace("hello  ")
        assert result == "hello "


class TestAreLinesIdentical:
    """Tests for are_lines_identical function."""

    def test_identical_lines(self) -> None:
        """Test that identical lines return True."""
        assert are_lines_identical("hello", "hello") is True

    def test_different_whitespace_quantity_identical(self) -> None:
        """Test that lines with different whitespace quantities are identical."""
        assert are_lines_identical("d. H", "d.  H") is True
        assert are_lines_identical("hello  world", "hello world") is True

    def test_new_whitespace_not_identical(self) -> None:
        """Test that lines with new whitespace are not identical."""
        assert are_lines_identical("d.H", "d. H") is False

    def test_different_content_not_identical(self) -> None:
        """Test that lines with different content are not identical."""
        assert are_lines_identical("hello", "world") is False

    def test_empty_lines_identical(self) -> None:
        """Test that empty lines are identical."""
        assert are_lines_identical("", "") is True


class TestTokenizeLine:
    """Tests for tokenize_line function."""

    def test_simple_tokenization(self) -> None:
        """Test basic tokenization."""
        tokens = tokenize_line("hello world")
        assert tokens == ["hello", " ", "world"]

    def test_no_whitespace(self) -> None:
        """Test tokenization without whitespace."""
        tokens = tokenize_line("hello")
        assert tokens == ["hello"]

    def test_multiple_spaces(self) -> None:
        """Test tokenization with multiple spaces."""
        tokens = tokenize_line("hello  world")
        assert tokens == ["hello", "  ", "world"]

    def test_empty_string(self) -> None:
        """Test tokenization of empty string."""
        tokens = tokenize_line("")
        assert tokens == []


class TestComputeDiffChanges:
    """Tests for compute_diff_changes function."""

    def test_identical_lines_no_changes(self) -> None:
        """Test that identical lines return the line unchanged."""
        result = compute_diff_changes("hello", "hello")
        assert result == "hello"

    def test_addition_marked(self) -> None:
        """Test that additions are marked with ++ ++."""
        result = compute_diff_changes("hello", "hello world")
        assert "++" in result
        assert "world" in result

    def test_deletion_marked(self) -> None:
        """Test that deletions are marked with -- --."""
        result = compute_diff_changes("hello world", "hello")
        assert "--" in result
        assert "world" in result

    def test_whitespace_quantity_difference_no_changes(self) -> None:
        """Test that whitespace quantity differences don't create changes."""
        result = compute_diff_changes("d. H", "d.  H")
        assert "++" not in result
        assert "--" not in result


class TestCompareLines:
    """Tests for compare_lines function."""

    def test_identical_lines_result(self) -> None:
        """Test comparing identical lines."""
        result = compare_lines("hello", "hello")
        assert isinstance(result, DiffResult)
        assert result.is_identical is True
        assert result.file1_line == "hello"
        assert result.file2_line == "hello"

    def test_different_lines_result(self) -> None:
        """Test comparing different lines."""
        result = compare_lines("hello", "world")
        assert isinstance(result, DiffResult)
        assert result.is_identical is False
        assert result.file1_line == "hello"
        assert result.file2_line == "world"

    def test_whitespace_difference_identical(self) -> None:
        """Test that whitespace quantity differences are identical."""
        result = compare_lines("d. H", "d.  H")
        assert result.is_identical is True


class TestCompareFiles:
    """Tests for compare_files function."""

    def test_identical_files(self) -> None:
        """Test comparing identical files."""
        file1 = ["line1", "line2"]
        file2 = ["line1", "line2"]
        results = compare_files(file1, file2)
        assert len(results) == 2
        assert all(r.is_identical for r in results)

    def test_different_files(self) -> None:
        """Test comparing different files."""
        file1 = ["line1", "line2"]
        file2 = ["line1", "line3"]
        results = compare_files(file1, file2)
        assert len(results) == 2
        assert results[0].is_identical is True
        assert results[1].is_identical is False

    def test_different_length_files(self) -> None:
        """Test comparing files with different lengths."""
        file1 = ["line1"]
        file2 = ["line1", "line2"]
        results = compare_files(file1, file2)
        assert len(results) == 2
        assert results[0].is_identical is True
        assert results[1].is_identical is False

    def test_empty_files(self) -> None:
        """Test comparing empty files."""
        file1: list[str] = []
        file2: list[str] = []
        results = compare_files(file1, file2)
        assert len(results) == 0


class TestFormatDiffOutput:
    """Tests for format_diff_output function."""

    def test_no_differences_empty_output(self) -> None:
        """Test that identical lines produce empty output."""
        result = DiffResult("hello", "hello", "hello", True)
        output = format_diff_output([result])
        assert output == ""

    def test_difference_formatted(self) -> None:
        """Test that differences are formatted correctly."""
        result = DiffResult("hello", "world", "++ world ++", False)
        output = format_diff_output([result])
        assert "---" in output
        assert "hello" in output
        assert "world" in output
        assert "++" in output

    def test_multiple_differences(self) -> None:
        """Test multiple differences in output."""
        results = [
            DiffResult("line1", "line1", "line1", True),
            DiffResult("line2", "line2-modified", "line2-++ modified ++", False),
            DiffResult("line3", "line3-changed", "++ line3-changed ++", False),
        ]
        output = format_diff_output(results)
        # Should have 2 diff blocks (skip the identical line)
        assert output.count("---") == 2

    def test_output_format_structure(self) -> None:
        """Test that output follows the required format structure."""
        result = DiffResult("file1line", "file2line", "changes", False)
        output = format_diff_output([result])
        lines = output.strip().split("\n")

        # Format should be:
        # ---
        # [file 1 line]
        # [file 2 line]
        # (blank line)
        # [changes]
        # (blank line)
        assert lines[0] == "---"
        assert lines[1] == "file1line"
        assert lines[2] == "file2line"
        assert lines[3] == ""
        assert lines[4] == "changes"
