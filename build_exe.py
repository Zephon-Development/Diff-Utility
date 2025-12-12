#!/usr/bin/env python3
"""Build script for creating the Diff-Utility executable."""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
from pathlib import Path


def build_exe() -> None:
    """Build the executable using PyInstaller."""
    # Ensure we're in the project root
    project_root = Path(__file__).parent

    # Print diagnostics to help debugging CI issues
    print("Python executable:", sys.executable)
    print("Python version:", sys.version)
    print("PATH:", os.environ.get("PATH"))

    # Ensure pyinstaller is installed for this python interpreter
    try:
        importlib.import_module("PyInstaller")
        print("PyInstaller already importable")
    except Exception:
        print("PyInstaller not available, installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    # Run PyInstaller
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",  # Single executable file
        "--name",
        "diff-utility",
        "--console",  # Console app (no GUI)
        "src/diff_utility/cli.py",
    ]

    print("Building executable with sys.executable -m PyInstaller...")
    result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True, check=False)

    # If `python -m PyInstaller` fails, try calling the `pyinstaller` script from PATH
    if result.returncode != 0:
        print("First build attempt failed, trying 'pyinstaller' script from PATH...")
        fallback_cmd = [
            "pyinstaller",
            "--onefile",
            "--name",
            "diff-utility",
            "--console",
            "src/diff_utility/cli.py",
        ]
        fallback = subprocess.run(
            fallback_cmd, cwd=project_root, capture_output=True, text=True, check=False
        )
        if fallback.returncode == 0:
            print("Build successful via fallback 'pyinstaller' call")
            print("Executable created at: dist/diff-utility.exe")
            return
        print("Fallback build also failed:")
        print(fallback.stderr)

    if result.returncode != 0:
        print("Build failed:")
        print(result.stderr)
        sys.exit(1)

    print("Build successful!")
    print("Executable created at: dist/diff-utility.exe")


if __name__ == "__main__":
    build_exe()
