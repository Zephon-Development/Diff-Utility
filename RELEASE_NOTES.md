# Release Notes

## Version 1.2.2
- Removed unnecessary PAT validation step from release-version.yml to avoid shell compatibility issues
- Workflow will fail naturally if PAT is missing, eliminating redundant checks

## Version 1.2.1
- Fixed workflow syntax errors in release-version.yml for proper CI/CD operation
- Improved secret validation logic in GitHub Actions workflows

## Version 1.2.0
- **CLI Argument Enhancements**: Added comprehensive command-line argument support
  - New help options: `--help`, `/?`, and `--?` all display help information
  - File input options: `-file1`/`-1` for first file, `-file2`/`-2` for second file
  - Output option: `-output`/`-o` to write diff results to a file
  - Positional arguments still supported with named argument override capability
  - Named parameters take precedence over positional arguments
- Improved error handling with consolidated error messages
- Added comprehensive test coverage for all new CLI features

## Version 1.1.3
- Bump version to 1.1.3 for end-to-end test
- Fixed build script to correctly invoke PyInstaller for executable generation.
- Added local CI test script for running quality checks locally.
- Improved automated tagging logic to check for existing tags instead of file changes.

## Version 1.1.1
- Added support for multiple text encodings (UTF-8, Windows-1252, Latin-1) to handle files that are not UTF-8 encoded, resolving UnicodeDecodeError issues.

## Version 1.1.0
- Enhanced diff utility to detect line insertions and deletions without cascading false positives, using SequenceMatcher for accurate line-level comparisons.
- Improved performance for large files.
- Added comprehensive unit and performance tests.