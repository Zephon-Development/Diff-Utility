# Handoff to Implementation (Claudette)

## Context
User requested addition of command-line arguments to diff-utility and version bump to 1.2.0.

## Plan Approved
The plan in `plan_cli_args.md` has been reviewed and approved. It references CODING_STANDARDS.md appropriately.

## Implementation Tasks
1. Modify `src/diff_utility/cli.py` to add new argparse options and logic.
2. Ensure backward compatibility and correct override behavior.
3. Add tests for new functionality.
4. Bump version in pyproject.toml, VERSION.txt, README.md, RELEASE_NOTES.md.
5. Add version bump instructions to CODING_STANDARDS.md.

## Deliverables
- Updated CLI code with new arguments.
- Tests passing.
- Version updated to 1.2.0.
- Documentation updated.

## Notes
- Follow CODING_STANDARDS.md for code quality.
- Ensure type safety and testing standards.
- Output to file if specified, else stdout.