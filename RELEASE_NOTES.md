# Release Notes

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