"""Command-line interface for the Diff Utility tool."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from diff_utility.diff import diff_files


def main() -> int:  # noqa: PLR0911
    """Main entry point for the diff-utility CLI.

    Returns:
        Exit code: 0 on success, 1 on I/O error, 2 on argument error.
    """
    # Convert special help cases to standard --help
    argv = sys.argv.copy()
    if len(argv) > 1 and argv[1] in ("/?", "--?"):
        argv[1] = "--help"

    parser = argparse.ArgumentParser(
        prog="diff-utility",
        description="Compare two text files with custom whitespace handling",
    )

    # Positional arguments (optional when named arguments are used)
    parser.add_argument(
        "file1",
        type=str,
        nargs="?",
        help="Path to the first file (positional)",
    )
    parser.add_argument(
        "file2",
        type=str,
        nargs="?",
        help="Path to the second file (positional)",
    )
    parser.add_argument(
        "output",
        type=str,
        nargs="?",
        help="Path to the output file (positional, optional)",
    )

    # Named arguments
    parser.add_argument(
        "-file1",
        "-1",
        dest="named_file1",
        type=str,
        help="Path to the first file (named, overrides positional)",
    )
    parser.add_argument(
        "-file2",
        "-2",
        dest="named_file2",
        type=str,
        help="Path to the second file (named, overrides positional)",
    )
    parser.add_argument(
        "-output",
        "-o",
        dest="named_output",
        type=str,
        help="Path to the output file (named, overrides positional)",
    )

    args = parser.parse_args(argv[1:])

    # Named arguments override positional ones
    final_file1 = args.named_file1 or args.file1
    final_file2 = args.named_file2 or args.file2
    final_output = args.named_output or args.output

    # Validate required arguments
    if final_file1 is None:
        print("Error: First file argument is required", file=sys.stderr)
        return 2
    if final_file2 is None:
        print("Error: Second file argument is required", file=sys.stderr)
        return 2

    try:
        path1 = Path(final_file1)
        path2 = Path(final_file2)

        if not path1.exists():
            print(f"Error: File not found: {path1}", file=sys.stderr)
            return 1

        if not path2.exists():
            print(f"Error: File not found: {path2}", file=sys.stderr)
            return 1

        result = diff_files(path1, path2)

        # Write to output file if specified, otherwise print to stdout
        if final_output:
            output_path = Path(final_output)
            output_path.write_text(result, encoding="utf-8")
        else:
            print(result)

        return 0

    except (PermissionError, OSError) as e:
        print(f"Error: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
