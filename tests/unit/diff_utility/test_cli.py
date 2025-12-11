"""
Unit tests for diff_utility.cli module.

Tests demonstrate comprehensive coverage (≥80%) per CODING_STANDARDS.md §4.1.
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from diff_utility.cli import main, read_file_lines


class TestReadFileLines:
    """Tests for read_file_lines function."""

    def test_read_file_success(self, tmp_path: Path) -> None:
        """Test reading a file successfully."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("line1\nline2\nline3\n")

        lines = read_file_lines(file_path)
        assert lines == ["line1", "line2", "line3"]

    def test_read_empty_file(self, tmp_path: Path) -> None:
        """Test reading an empty file."""
        file_path = tmp_path / "empty.txt"
        file_path.write_text("")

        lines = read_file_lines(file_path)
        assert lines == []

    def test_read_file_no_trailing_newline(self, tmp_path: Path) -> None:
        """Test reading a file without trailing newline."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("line1\nline2")

        lines = read_file_lines(file_path)
        assert lines == ["line1", "line2"]

    def test_read_nonexistent_file_raises(self, tmp_path: Path) -> None:
        """Test reading a nonexistent file raises FileNotFoundError."""
        file_path = tmp_path / "nonexistent.txt"

        with pytest.raises(FileNotFoundError):
            read_file_lines(file_path)


class TestMain:
    """Tests for main function."""

    def test_main_no_args(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test main with no arguments shows usage."""
        with patch.object(sys, "argv", ["diff-utility"]):
            exit_code = main()

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Usage:" in captured.err

    def test_main_one_arg(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test main with one argument shows usage."""
        with patch.object(sys, "argv", ["diff-utility", "file1.txt"]):
            exit_code = main()

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Usage:" in captured.err

    def test_main_file1_not_found(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test main with nonexistent first file."""
        file2 = tmp_path / "file2.txt"
        file2.write_text("content")

        with patch.object(
            sys, "argv", ["diff-utility", str(tmp_path / "nonexistent.txt"), str(file2)]
        ):
            exit_code = main()

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "File not found" in captured.err

    def test_main_file2_not_found(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test main with nonexistent second file."""
        file1 = tmp_path / "file1.txt"
        file1.write_text("content")

        with patch.object(
            sys, "argv", ["diff-utility", str(file1), str(tmp_path / "nonexistent.txt")]
        ):
            exit_code = main()

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "File not found" in captured.err

    def test_main_identical_files(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test main with identical files."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("line1\nline2\n")
        file2.write_text("line1\nline2\n")

        with patch.object(sys, "argv", ["diff-utility", str(file1), str(file2)]):
            exit_code = main()

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "identical" in captured.out.lower()

    def test_main_different_files(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test main with different files."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("line1\n")
        file2.write_text("line2\n")

        with patch.object(sys, "argv", ["diff-utility", str(file1), str(file2)]):
            exit_code = main()

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "---" in captured.out
        assert "line1" in captured.out
        assert "line2" in captured.out

    def test_main_whitespace_difference(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test main with whitespace quantity differences (should be identical)."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("d. H\n")
        file2.write_text("d.  H\n")

        with patch.object(sys, "argv", ["diff-utility", str(file1), str(file2)]):
            exit_code = main()

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "identical" in captured.out.lower()
