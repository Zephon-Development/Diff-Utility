# Feature Addition: Command Line Arguments for Diff-Utility

## Scope and Objectives
- **Primary Goal**: Enhance the diff-utility CLI with additional command-line arguments for better usability and flexibility.
- **Specific Changes**:
  - Add support for help options: `--help`, `/?`, `--?` (all display help).
  - Add file input options: `-file1 [filename]`, `-1 [filename]` for first file; `-file2 [filename]`, `-2 [filename]` for second file.
  - Add output option: `-output [filename]`, `-o [filename]` for output file.
  - Support positional arguments: file1, file2, output in sequence.
  - Named parameters override positional ones.
- **Version Bump**: Update version to 1.2.0 after implementation.
- **Documentation Updates**:
  - Update pyproject.toml version.
  - Update VERSION.txt.
  - Update README.md version.
  - Update RELEASE_NOTES.md with new features.
- **Standards Update**: Add version bump instructions to CODING_STANDARDS.md requiring updates to the 4 files.

## Constraints and Requirements
- **Backward Compatibility**: Existing positional arguments (file1 file2) must continue to work.
- **Override Logic**: Named switches take precedence over positional arguments.
- **Help Handling**: `/ ?` and `--?` must trigger help display, similar to `--help`.
- **Output Handling**: If `-output` or `-o` is specified, write diff to file; otherwise, print to stdout.
- **Error Handling**: Maintain existing error codes and messages.
- **Coding Standards**: Follow CODING_STANDARDS.md for code quality, type safety, testing, and documentation.

## Success Metrics
- CLI accepts and processes new arguments correctly.
- Help displays for all specified options.
- Positional and named arguments work as described, with overrides functioning.
- Output to file works when specified.
- Version bumped to 1.2.0 in all required files.
- RELEASE_NOTES.md documents the new feature.
- CODING_STANDARDS.md includes version bump checklist.
- All tests pass, including new tests for CLI arguments.
- Code quality checks (linting, formatting, type checking) pass.

## Implementation Plan
1. **Modify CLI Module** (`src/diff_utility/cli.py`):
   - Update argument parser to include new options.
   - Handle special help cases (`/?`, `--?`).
   - Implement logic for positional vs named argument precedence.
   - Add output file writing functionality.

2. **Add Tests** (`tests/unit/test_cli.py` or update existing):
   - Test new argument parsing.
   - Test help options.
   - Test override behavior.
   - Test output to file.

3. **Update Version Files**:
   - `pyproject.toml`: version = "1.2.0"
   - `VERSION.txt`: 1.2.0
   - `README.md`: Update version reference.
   - `RELEASE_NOTES.md`: Add entry for v1.2.0 with CLI enhancements.

4. **Update Standards Document** (`Documentation/CODING_STANDARDS.md`):
   - Add new section on version management with bump checklist.

5. **Validation**:
   - Run tests and quality checks.
   - Manual testing of CLI with various argument combinations.

## References
- CODING_STANDARDS.md: Sections on Type Safety, Testing, Documentation, CI/CD.
- Existing CLI code in `src/diff_utility/cli.py`.
- pyproject.toml for project configuration.