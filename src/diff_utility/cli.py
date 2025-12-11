"""Command-line interface for the Diff Utility tool."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from diff_utility.diff import diff_files


def main() -> int:
    """Main entry point for the diff-utility CLI.

    Returns:
        Exit code: 0 on success, 1 on I/O error, 2 on argument error.
    """
    parser = argparse.ArgumentParser(
        prog="diff-utility",
        description="Compare two text files with custom whitespace handling",
    )
    parser.add_argument("file1", type=str, help="Path to the first file")
    parser.add_argument("file2", type=str, help="Path to the second file")

    args = parser.parse_args()

    try:
        path1 = Path(args.file1)
        path2 = Path(args.file2)

        if not path1.exists():
            print(f"Error: File not found: {path1}", file=sys.stderr)
            return 1

        if not path2.exists():
            print(f"Error: File not found: {path2}", file=sys.stderr)
            return 1

        result = diff_files(path1, path2)
        print(result)
        return 0

    except PermissionError as e:
        print(f"Error: Permission denied: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Error: I/O error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
