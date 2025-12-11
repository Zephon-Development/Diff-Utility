"""
Command-line interface for the diff utility.

Provides a CLI for comparing text files with custom diff output.
"""

import sys
from pathlib import Path

from diff_utility.diff_engine import compare_files, format_diff_output

# Number of expected command-line arguments (excluding program name)
EXPECTED_ARGS = 2


def read_file_lines(filepath: Path) -> list[str]:
    """
    Read lines from a file.

    Args:
        filepath: Path to the file to read.

    Returns:
        List of lines from the file (with newlines stripped).

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read.
    """
    with filepath.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def main() -> int:
    """
    Main entry point for the diff utility CLI.

    Usage: diff-utility <file1> <file2>

    Returns:
        Exit code (0 for success, 1 for error).
    """
    if len(sys.argv) != EXPECTED_ARGS + 1:  # +1 for program name
        print("Usage: diff-utility <file1> <file2>", file=sys.stderr)
        return 1

    file1_path = Path(sys.argv[1])
    file2_path = Path(sys.argv[2])

    # Validate files exist
    if not file1_path.exists():
        print(f"Error: File not found: {file1_path}", file=sys.stderr)
        return 1

    if not file2_path.exists():
        print(f"Error: File not found: {file2_path}", file=sys.stderr)
        return 1

    try:
        # Read files
        file1_lines = read_file_lines(file1_path)
        file2_lines = read_file_lines(file2_path)

        # Compare files
        results = compare_files(file1_lines, file2_lines)

        # Format and output diff
        output = format_diff_output(results)

        if output:
            print(output)
        else:
            print("Files are identical.")

        return 0

    except PermissionError as e:
        print(f"Error: Permission denied: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
