"""Unit tests for the CLI module."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from diff_utility.cli import main


class TestCLI:
    """Tests for the CLI main function."""

    @pytest.mark.unit
    def test_successful_diff_output(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test successful diff operation with output to stdout."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Hello World\n", encoding="utf-8")
        file2.write_text("Hello Universe\n", encoding="utf-8")

        with patch.object(sys, "argv", ["diff-utility", str(file1), str(file2)]):
            exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "---" in captured.out
        assert "Hello World" in captured.out
        assert "Hello Universe" in captured.out

    @pytest.mark.unit
    def test_identical_files_empty_output(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that identical files produce empty output."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Same content\n", encoding="utf-8")
        file2.write_text("Same content\n", encoding="utf-8")

        with patch.object(sys, "argv", ["diff-utility", str(file1), str(file2)]):
            exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out == "\n"  # Empty output with trailing newline from print

    @pytest.mark.unit
    def test_first_file_not_found(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that missing first file returns exit code 1."""
        file1 = tmp_path / "nonexistent1.txt"
        file2 = tmp_path / "file2.txt"

        file2.write_text("content\n", encoding="utf-8")

        with patch.object(sys, "argv", ["diff-utility", str(file1), str(file2)]):
            exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error: File not found" in captured.err
        assert str(file1) in captured.err

    @pytest.mark.unit
    def test_second_file_not_found(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that missing second file returns exit code 1."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "nonexistent2.txt"

        file1.write_text("content\n", encoding="utf-8")

        with patch.object(sys, "argv", ["diff-utility", str(file1), str(file2)]):
            exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error: File not found" in captured.err
        assert str(file2) in captured.err

    @pytest.mark.unit
    def test_permission_error_handling(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that permission errors are handled gracefully."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("content\n", encoding="utf-8")
        file2.write_text("content\n", encoding="utf-8")

        def mock_open_permission_error(*args: object, **kwargs: object) -> None:
            msg = "Permission denied"
            raise PermissionError(msg)

        monkeypatch.setattr(Path, "open", mock_open_permission_error)

        with patch.object(sys, "argv", ["diff-utility", str(file1), str(file2)]):
            exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error: Permission denied" in captured.err

    @pytest.mark.unit
    def test_empty_files_no_output(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that empty files produce no diff output."""
        file1 = tmp_path / "empty1.txt"
        file2 = tmp_path / "empty2.txt"

        file1.write_text("", encoding="utf-8")
        file2.write_text("", encoding="utf-8")

        with patch.object(sys, "argv", ["diff-utility", str(file1), str(file2)]):
            exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out == "\n"  # Empty with trailing newline

    @pytest.mark.unit
    def test_multiline_diff(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test diff output with multiple changed lines."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Line 1\nLine 2\nLine 3\n", encoding="utf-8")
        file2.write_text("Line One\nLine 2\nLine Three\n", encoding="utf-8")

        with patch.object(sys, "argv", ["diff-utility", str(file1), str(file2)]):
            exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 0
        # Should have two diff blocks (line 1 and line 3 changed)
        assert captured.out.count("---") == 2
