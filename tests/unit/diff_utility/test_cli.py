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
        assert "Error: PermissionError" in captured.err

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

    @pytest.mark.unit
    def test_help_with_double_dash(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that --help displays help."""
        with (
            pytest.raises(SystemExit) as exc_info,
            patch.object(sys, "argv", ["diff-utility", "--help"]),
        ):
            main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Compare two text files" in captured.out

    @pytest.mark.unit
    def test_help_with_slash_question(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that /? displays help."""
        with (
            pytest.raises(SystemExit) as exc_info,
            patch.object(sys, "argv", ["diff-utility", "/?"]),
        ):
            main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Compare two text files" in captured.out

    @pytest.mark.unit
    def test_help_with_dash_question(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that --? displays help."""
        with (
            pytest.raises(SystemExit) as exc_info,
            patch.object(sys, "argv", ["diff-utility", "--?"]),
        ):
            main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Compare two text files" in captured.out

    @pytest.mark.unit
    def test_named_file1_argument(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test using -file1 named argument."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Hello World\n", encoding="utf-8")
        file2.write_text("Hello Universe\n", encoding="utf-8")

        with patch.object(
            sys, "argv", ["diff-utility", "-file1", str(file1), "-file2", str(file2)]
        ):
            exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "---" in captured.out

    @pytest.mark.unit
    def test_short_named_arguments(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test using -1 and -2 short named arguments."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Hello World\n", encoding="utf-8")
        file2.write_text("Hello Universe\n", encoding="utf-8")

        with patch.object(sys, "argv", ["diff-utility", "-1", str(file1), "-2", str(file2)]):
            exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "---" in captured.out

    @pytest.mark.unit
    def test_named_overrides_positional(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that named arguments override positional ones."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file3 = tmp_path / "file3.txt"

        file1.write_text("File 1\n", encoding="utf-8")
        file2.write_text("File 2\n", encoding="utf-8")
        file3.write_text("File 3\n", encoding="utf-8")

        # Positional says file1 and file2, but -file2 overrides with file3
        with patch.object(
            sys, "argv", ["diff-utility", str(file1), str(file2), "-file2", str(file3)]
        ):
            exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 0
        # Should compare file1 with file3, not file2
        assert "File 1" in captured.out
        assert "File 3" in captured.out

    @pytest.mark.unit
    def test_output_to_file_positional(self, tmp_path: Path) -> None:
        """Test writing output to file using positional argument."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        output = tmp_path / "output.txt"

        file1.write_text("Hello World\n", encoding="utf-8")
        file2.write_text("Hello Universe\n", encoding="utf-8")

        with patch.object(sys, "argv", ["diff-utility", str(file1), str(file2), str(output)]):
            exit_code = main()

        assert exit_code == 0
        assert output.exists()
        content = output.read_text(encoding="utf-8")
        assert "---" in content
        assert "Hello World" in content
        assert "Hello Universe" in content

    @pytest.mark.unit
    def test_output_to_file_named_short(self, tmp_path: Path) -> None:
        """Test writing output to file using -o named argument."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        output = tmp_path / "output.txt"

        file1.write_text("Hello World\n", encoding="utf-8")
        file2.write_text("Hello Universe\n", encoding="utf-8")

        with patch.object(sys, "argv", ["diff-utility", str(file1), str(file2), "-o", str(output)]):
            exit_code = main()

        assert exit_code == 0
        assert output.exists()
        content = output.read_text(encoding="utf-8")
        assert "---" in content

    @pytest.mark.unit
    def test_output_to_file_named_long(self, tmp_path: Path) -> None:
        """Test writing output to file using -output named argument."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        output = tmp_path / "output.txt"

        file1.write_text("Hello World\n", encoding="utf-8")
        file2.write_text("Hello Universe\n", encoding="utf-8")

        with patch.object(
            sys, "argv", ["diff-utility", str(file1), str(file2), "-output", str(output)]
        ):
            exit_code = main()

        assert exit_code == 0
        assert output.exists()
        content = output.read_text(encoding="utf-8")
        assert "---" in content

    @pytest.mark.unit
    def test_output_named_overrides_positional(self, tmp_path: Path) -> None:
        """Test that -output named argument overrides positional output."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        output1 = tmp_path / "output1.txt"
        output2 = tmp_path / "output2.txt"

        file1.write_text("Hello World\n", encoding="utf-8")
        file2.write_text("Hello Universe\n", encoding="utf-8")

        # Positional output is output1, but -output overrides with output2
        with patch.object(
            sys,
            "argv",
            ["diff-utility", str(file1), str(file2), str(output1), "-output", str(output2)],
        ):
            exit_code = main()

        assert exit_code == 0
        assert output2.exists()
        assert not output1.exists()  # Should not create the positional output file

    @pytest.mark.unit
    def test_missing_file1_error(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test error when file1 is not provided."""
        with patch.object(sys, "argv", ["diff-utility"]):
            exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 2
        assert "Error: First file argument is required" in captured.err

    @pytest.mark.unit
    def test_missing_file2_error(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test error when file2 is not provided."""
        file1 = tmp_path / "file1.txt"
        file1.write_text("content\n", encoding="utf-8")

        with patch.object(sys, "argv", ["diff-utility", str(file1)]):
            exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 2
        assert "Error: Second file argument is required" in captured.err
