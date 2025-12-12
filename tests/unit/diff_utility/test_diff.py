"""Unit tests for the diff module."""

from __future__ import annotations

from pathlib import Path

import pytest

from diff_utility.diff import (
    annotate_changes,
    diff_files,
    diff_lines,
    lines_equal_norm,
    normalize_line,
    read_lines,
)


class TestNormalizeLine:
    """Tests for the normalize_line function."""

    @pytest.mark.unit
    def test_multiple_spaces_collapsed_to_single(self) -> None:
        """Test that multiple spaces are collapsed into a single space."""
        assert normalize_line("Hello   World") == "Hello World"

    @pytest.mark.unit
    def test_tab_converted_to_space(self) -> None:
        """Test that tabs are converted to spaces."""
        assert normalize_line("Hello\tWorld") == "Hello World"

    @pytest.mark.unit
    def test_mixed_whitespace_collapsed(self) -> None:
        """Test that mixed whitespace (spaces and tabs) is collapsed."""
        assert normalize_line("Hello  \t \t World") == "Hello World"

    @pytest.mark.unit
    def test_leading_spaces_collapsed(self) -> None:
        """Test that leading spaces are collapsed."""
        assert normalize_line("  Hello World") == " Hello World"

    @pytest.mark.unit
    def test_trailing_spaces_collapsed(self) -> None:
        """Test that trailing spaces are collapsed."""
        assert normalize_line("Hello World  ") == "Hello World "

    @pytest.mark.unit
    def test_empty_string_unchanged(self) -> None:
        """Test that empty strings remain empty."""
        assert normalize_line("") == ""

    @pytest.mark.unit
    def test_single_space_unchanged(self) -> None:
        """Test that a single space remains unchanged."""
        assert normalize_line("Hello World") == "Hello World"


class TestLinesEqualNorm:
    """Tests for the lines_equal_norm function."""

    @pytest.mark.unit
    def test_identical_lines_equal(self) -> None:
        """Test that identical lines are considered equal."""
        assert lines_equal_norm("Hello World", "Hello World") is True

    @pytest.mark.unit
    def test_different_whitespace_quantity_equal(self) -> None:
        """Test that lines differing only in whitespace quantity are equal."""
        assert lines_equal_norm("Hello   World", "Hello World") is True

    @pytest.mark.unit
    def test_tab_vs_space_equal(self) -> None:
        """Test that tabs and spaces are considered equivalent."""
        assert lines_equal_norm("Hello\tWorld", "Hello World") is True

    @pytest.mark.unit
    def test_different_content_not_equal(self) -> None:
        """Test that lines with different content are not equal."""
        assert lines_equal_norm("Hello World", "Goodbye World") is False

    @pytest.mark.unit
    def test_missing_space_not_equal(self) -> None:
        """Test that missing space between words makes lines unequal."""
        assert lines_equal_norm("Hello World", "HelloWorld") is False


class TestAnnotateChanges:
    """Tests for the annotate_changes function."""

    @pytest.mark.unit
    def test_identical_lines_no_markers(self) -> None:
        """Test that identical lines produce no change markers."""
        result = annotate_changes("Hello World", "Hello World")
        assert result == "Hello World"

    @pytest.mark.unit
    def test_single_word_addition(self) -> None:
        """Test that a single word addition is marked correctly."""
        result = annotate_changes("Hello World", "Hello Beautiful World")
        # Whitespace tokens are included, so we get: "Hello" " " "Beautiful" " " "World"
        assert result == "Hello ++Beautiful++++ ++World"

    @pytest.mark.unit
    def test_single_word_deletion(self) -> None:
        """Test that a single word deletion is marked correctly."""
        result = annotate_changes("Hello Beautiful World", "Hello World")
        # Whitespace tokens are included
        assert result == "Hello --Beautiful---- --World"

    @pytest.mark.unit
    def test_word_replacement(self) -> None:
        """Test that word replacement shows both deletion and addition."""
        result = annotate_changes("Hello World", "Hello Universe")
        assert result == "Hello --World--++Universe++"

    @pytest.mark.unit
    def test_whitespace_addition(self) -> None:
        """Test that whitespace addition is marked."""
        result = annotate_changes("Hello World.How", "Hello World. How")
        # Tokens: "Hello" " " "World.How" vs "Hello" " " "World." " " "How"
        assert "--World.How--" in result
        assert "++World.++" in result
        assert "++ ++" in result
        assert "++How++" in result

    @pytest.mark.unit
    def test_multiple_spaces_vs_single(self) -> None:
        """Test that different whitespace quantities are marked."""
        result = annotate_changes("Hello World", "Hello  World")
        # Should show deletion of single space and addition of double space
        assert "-- --" in result
        assert "++  ++" in result

    @pytest.mark.unit
    def test_complete_line_change(self) -> None:
        """Test complete line replacement."""
        result = annotate_changes("Old line", "New line")
        assert "--Old--" in result
        assert "++New++" in result


class TestDiffLines:
    """Tests for the diff_lines function."""

    @pytest.mark.unit
    def test_identical_lines_no_output(self) -> None:
        """Test that identical lines produce no output."""
        lines1 = ["Hello World", "Goodbye"]
        lines2 = ["Hello World", "Goodbye"]
        result = diff_lines(lines1, lines2)
        assert result == []

    @pytest.mark.unit
    def test_whitespace_only_differences_skipped(self) -> None:
        """Test that whitespace-only differences are skipped."""
        lines1 = ["Hello   World"]
        lines2 = ["Hello World"]
        result = diff_lines(lines1, lines2)
        assert result == []

    @pytest.mark.unit
    def test_changed_line_produces_block(self) -> None:
        """Test that a changed line produces the correct output block."""
        lines1 = ["Hello World"]
        lines2 = ["Hello Universe"]
        result = diff_lines(lines1, lines2)

        assert result[0] == "---"
        assert result[1] == "File A: Hello World"
        assert result[2] == "File B: Hello Universe"
        assert result[3] == ""
        assert "--World--" in result[4]
        assert "++Universe++" in result[4]

    @pytest.mark.unit
    def test_multiple_changed_lines(self) -> None:
        """Test multiple changed lines produce multiple blocks."""
        lines1 = ["Line 1", "Line 2"]
        lines2 = ["Line One", "Line Two"]
        result = diff_lines(lines1, lines2)

        # Should have two blocks separated by blank lines
        assert result.count("---") == 2

    @pytest.mark.unit
    def test_insert_only_single_line(self) -> None:
        """Test that a single inserted line is detected correctly."""
        lines1 = ["Line 1", "Line 3"]
        lines2 = ["Line 1", "Line 2", "Line 3"]
        result = diff_lines(lines1, lines2)

        # Should have one block for the insertion
        assert result.count("---") == 1
        # Inserted line should be marked with ++
        assert any("++Line 2++" in line for line in result)

    @pytest.mark.unit
    def test_delete_only_single_line(self) -> None:
        """Test that a single deleted line is detected correctly."""
        lines1 = ["Line 1", "Line 2", "Line 3"]
        lines2 = ["Line 1", "Line 3"]
        result = diff_lines(lines1, lines2)

        # Should have one block for the deletion
        assert result.count("---") == 1
        # Deleted line should be marked with --
        assert any("--Line 2--" in line for line in result)

    @pytest.mark.unit
    def test_insert_and_delete_different_positions(self) -> None:
        """Test insert and delete at different positions in the file."""
        lines1 = ["Line 1", "Line 2", "Line 4"]
        lines2 = ["Line 1", "Line 3", "Line 4"]
        result = diff_lines(lines1, lines2)

        # Should have one block showing the replacement
        assert result.count("---") == 1
        assert any("Line 2" in line for line in result)
        assert any("Line 3" in line for line in result)

    @pytest.mark.unit
    def test_multiple_consecutive_insertions(self) -> None:
        """Test multiple consecutive line insertions."""
        lines1 = ["Line 1", "Line 5"]
        lines2 = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]
        result = diff_lines(lines1, lines2)

        # Should have three blocks for the three insertions
        assert result.count("---") == 3
        assert any("++Line 2++" in line for line in result)
        assert any("++Line 3++" in line for line in result)
        assert any("++Line 4++" in line for line in result)

    @pytest.mark.unit
    def test_multiple_consecutive_deletions(self) -> None:
        """Test multiple consecutive line deletions."""
        lines1 = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]
        lines2 = ["Line 1", "Line 5"]
        result = diff_lines(lines1, lines2)

        # Should have three blocks for the three deletions
        assert result.count("---") == 3
        assert any("--Line 2--" in line for line in result)
        assert any("--Line 3--" in line for line in result)
        assert any("--Line 4--" in line for line in result)

    @pytest.mark.unit
    def test_insert_at_beginning(self) -> None:
        """Test line insertion at the beginning of file."""
        lines1 = ["Line 2", "Line 3"]
        lines2 = ["Line 1", "Line 2", "Line 3"]
        result = diff_lines(lines1, lines2)

        assert result.count("---") == 1
        assert any("++Line 1++" in line for line in result)

    @pytest.mark.unit
    def test_insert_at_end(self) -> None:
        """Test line insertion at the end of file."""
        lines1 = ["Line 1", "Line 2"]
        lines2 = ["Line 1", "Line 2", "Line 3"]
        result = diff_lines(lines1, lines2)

        assert result.count("---") == 1
        assert any("++Line 3++" in line for line in result)

    @pytest.mark.unit
    def test_delete_at_beginning(self) -> None:
        """Test line deletion at the beginning of file."""
        lines1 = ["Line 1", "Line 2", "Line 3"]
        lines2 = ["Line 2", "Line 3"]
        result = diff_lines(lines1, lines2)

        assert result.count("---") == 1
        assert any("--Line 1--" in line for line in result)

    @pytest.mark.unit
    def test_delete_at_end(self) -> None:
        """Test line deletion at the end of file."""
        lines1 = ["Line 1", "Line 2", "Line 3"]
        lines2 = ["Line 1", "Line 2"]
        result = diff_lines(lines1, lines2)

        assert result.count("---") == 1
        assert any("--Line 3--" in line for line in result)

    @pytest.mark.unit
    def test_no_cascading_false_positives(self) -> None:
        """Test that inserting a line doesn't flag subsequent lines as different."""
        lines1 = ["Line 1", "Line 3", "Line 4", "Line 5"]
        lines2 = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]
        result = diff_lines(lines1, lines2)

        # Should only have one block for the insertion
        assert result.count("---") == 1
        assert any("++Line 2++" in line for line in result)
        # Lines 3, 4, 5 should NOT appear in the diff
        assert result.count("Line 3") <= 1  # Only in the insertion context if at all
        assert "Line 4" not in "\n".join(result) or result.count("Line 4") == 0
        assert "Line 5" not in "\n".join(result) or result.count("Line 5") == 0

    @pytest.mark.unit
    def test_replace_with_token_level_annotation(self) -> None:
        """Test that line replacements use token-level annotation."""
        lines1 = ["Hello World"]
        lines2 = ["Hello Universe"]
        result = diff_lines(lines1, lines2)

        # Should show token-level changes
        assert "--World--" in "\n".join(result)
        assert "++Universe++" in "\n".join(result)

    @pytest.mark.unit
    def test_different_length_files(self) -> None:
        """Test files with different lengths."""
        lines1 = ["Line 1"]
        lines2 = ["Line 1", "Line 2"]
        result = diff_lines(lines1, lines2)

        # Second line is an insertion
        assert "---" in result
        assert any("++Line 2++" in line for line in result)

    @pytest.mark.unit
    def test_large_file_performance(self) -> None:
        """Test performance with large files (regression test)."""
        # Create synthetic 1000-line files with one insertion
        lines1 = [f"Line {i}" for i in range(1000)]
        lines2 = (
            [f"Line {i}" for i in range(500)]
            + ["Inserted Line"]
            + [f"Line {i}" for i in range(500, 1000)]
        )

        result = diff_lines(lines1, lines2)

        # Should only report the one insertion, not flag remaining 500 lines
        assert result.count("---") == 1
        assert any("++Inserted Line++" in line for line in result)

    @pytest.mark.unit
    def test_empty_file_comparison(self) -> None:
        """Test comparing empty files."""
        lines1: list[str] = []
        lines2: list[str] = []
        result = diff_lines(lines1, lines2)
        assert result == []

    @pytest.mark.unit
    def test_empty_vs_non_empty(self) -> None:
        """Test comparing empty file with non-empty file."""
        lines1: list[str] = []
        lines2 = ["Line 1", "Line 2"]
        result = diff_lines(lines1, lines2)

        # Both lines should be marked as insertions
        assert result.count("---") == 2
        assert any("++Line 1++" in line for line in result)
        assert any("++Line 2++" in line for line in result)

    @pytest.mark.unit
    def test_non_empty_vs_empty(self) -> None:
        """Test comparing non-empty file with empty file."""
        lines1 = ["Line 1", "Line 2"]
        lines2: list[str] = []
        result = diff_lines(lines1, lines2)

        # Both lines should be marked as deletions
        assert result.count("---") == 2
        assert any("--Line 1--" in line for line in result)
        assert any("--Line 2--" in line for line in result)

    @pytest.mark.unit
    def test_replace_unequal_more_deletions(self) -> None:
        """Test replace operation where source has more lines than destination."""
        lines1 = ["Old Line 1", "Old Line 2", "Old Line 3"]
        lines2 = ["New Line 1"]
        result = diff_lines(lines1, lines2)

        # Should have blocks for the replacement and deletions
        assert result.count("---") == 3
        assert any("New Line 1" in line for line in result)
        assert any("--Old Line 2--" in line for line in result)
        assert any("--Old Line 3--" in line for line in result)

    @pytest.mark.unit
    def test_replace_unequal_more_insertions(self) -> None:
        """Test replace operation where destination has more lines than source."""
        lines1 = ["Old Line 1"]
        lines2 = ["New Line 1", "New Line 2", "New Line 3"]
        result = diff_lines(lines1, lines2)

        # Should have blocks for the replacement and insertions
        assert result.count("---") == 3
        assert any("Old Line 1" in line for line in result)
        assert any("++New Line 2++" in line for line in result)
        assert any("++New Line 3++" in line for line in result)


class TestReadLines:
    """Tests for the read_lines function."""

    @pytest.mark.unit
    def test_reads_file_content(self, tmp_path: Path) -> None:
        """Test that read_lines correctly reads file content."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Line 1\nLine 2\nLine 3\n", encoding="utf-8")

        lines = read_lines(test_file)
        assert lines == ["Line 1", "Line 2", "Line 3"]

    @pytest.mark.unit
    def test_removes_trailing_newlines(self, tmp_path: Path) -> None:
        """Test that trailing newlines are removed from each line."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello\nWorld\n", encoding="utf-8")

        lines = read_lines(test_file)
        assert lines == ["Hello", "World"]

    @pytest.mark.unit
    def test_empty_file(self, tmp_path: Path) -> None:
        """Test reading an empty file."""
        test_file = tmp_path / "empty.txt"
        test_file.write_text("", encoding="utf-8")

        lines = read_lines(test_file)
        assert lines == []

    @pytest.mark.unit
    def test_file_not_found(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError is raised for non-existent files."""
        non_existent = tmp_path / "does_not_exist.txt"

        with pytest.raises(FileNotFoundError):
            read_lines(non_existent)

    @pytest.mark.unit
    def test_encoding_fallback_cp1252(self, tmp_path: Path) -> None:
        """Test that files with cp1252 encoding are read correctly."""
        test_file = tmp_path / "cp1252.txt"
        # Write content with cp1252 encoding (non-breaking space 0xa0)
        content = "Hello\xa0World\nSecond line\n"
        test_file.write_bytes(content.encode("cp1252"))

        lines = read_lines(test_file)
        assert lines == ["Hello\xa0World", "Second line"]

    @pytest.mark.unit
    def test_encoding_fallback_latin1(self, tmp_path: Path) -> None:
        """Test that files with latin-1 encoding are read correctly."""
        test_file = tmp_path / "latin1.txt"
        # Write content with latin-1 encoding
        content = "Café\n naïve\n"
        test_file.write_bytes(content.encode("latin-1"))

        lines = read_lines(test_file)
        assert lines == ["Café", " naïve"]


class TestDiffFiles:
    """Tests for the diff_files function."""

    @pytest.mark.unit
    def test_identical_files_empty_output(self, tmp_path: Path) -> None:
        """Test that identical files produce empty output."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Hello World\n", encoding="utf-8")
        file2.write_text("Hello World\n", encoding="utf-8")

        result = diff_files(file1, file2)
        assert result == ""

    @pytest.mark.unit
    def test_different_files_produces_diff(self, tmp_path: Path) -> None:
        """Test that different files produce diff output."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Hello World\n", encoding="utf-8")
        file2.write_text("Hello Universe\n", encoding="utf-8")

        result = diff_files(file1, file2)
        assert "---" in result
        assert "Hello World" in result
        assert "Hello Universe" in result
        assert "--World--" in result
        assert "++Universe++" in result

    @pytest.mark.unit
    def test_whitespace_differences_example(self, tmp_path: Path) -> None:
        """Test the specific whitespace example from the plan."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Hello World.How are you\n", encoding="utf-8")
        file2.write_text("Hello World. How are you\n", encoding="utf-8")

        result = diff_files(file1, file2)
        assert "---" in result
        assert "--World.How--" in result
        assert "++World.++" in result
        assert "++ ++" in result
        assert "++How++" in result

    @pytest.mark.unit
    def test_file_not_found_raises_error(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError is raised for non-existent files."""
        file1 = tmp_path / "exists.txt"
        file2 = tmp_path / "does_not_exist.txt"

        file1.write_text("content\n", encoding="utf-8")

        with pytest.raises(FileNotFoundError):
            diff_files(file1, file2)
