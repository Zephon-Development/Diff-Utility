# Implementation Handoff – Diff-Utility

**Implementer:** Claudette  
**Prepared by:** Clive  
**Date:** December 11, 2025  
**Primary Plan:** `Documentation/Active-Plans/Diff-Utility-Plan.md` (approved)

## Mission Summary
Build the Diff-Utility CLI per the approved plan: rebrand the template artifacts, implement the whitespace-aware diff engine, expose a CLI entry point, and deliver full test coverage that satisfies `Documentation/CODING_STANDARDS.md` (Python 3.11+, strict typing, ≥80% line / ≥75% branch coverage, Google-style docstrings for public APIs).

## Key Requirements
- Rename `template` package/tests/docs to `diff_utility` / Diff-Utility everywhere (pyproject, README, imports, paths, etc.).
- Implement modules described in the plan (`src/diff_utility/diff.py`, CLI entry, updated `__init__.py`).
- Enforce whitespace rules: normalized comparison per plan; token-level annotation with `++/--` markers for inserts/deletes, including whitespace tokens.
- CLI: positional args `<file1> <file2>`, stdout output only, exit codes 0/1/2, helpful error messages.
- Documentation updates: README, usage examples, whitespace policy summary.
- Testing: unit tests in `tests/unit/diff_utility/` covering normalization, annotation, skip logic, CLI behavior; use `@pytest.mark.unit`, `tmp_path`, and fixtures per plan.

## Implementation Checklist
1. **Rebranding Pass**
   - Rename directories/files and update metadata (`pyproject.toml`, README, tests, package exports).
   - Ensure `py.typed` stays aligned with new package path.
2. **Core Diff Engine**
   - Implement functions outlined in plan (reading, normalization, equality, annotation, diff composition).
   - Keep functions pure/testable; adhere to strict typing (no `Any`).
3. **CLI Module**
   - Argparse-based entry point; connect to diff engine; handle I/O/arg errors with correct exit codes and stderr messaging.
4. **Tests & Coverage**
   - Add unit tests for all logic branches; include CLI tests using temporary files and captured output.
   - Ensure pytest + coverage + `scripts/check_branch_coverage.py` meet thresholds.
5. **Docs & Final QA**
   - Update README and any other doc references to describe Diff-Utility usage and whitespace policy.
   - Run Black, Ruff, mypy, pytest, coverage script; address failures.

## Risks / Watchouts
- Whitespace/token handling is subtle; follow the exact spec/examples from the plan to avoid regressions.
- Avoid floating `type: ignore`; document any exception per Standards §2.5 if unavoidable.
- Ensure README instructions reflect renamed paths (no lingering “PythonTemplate” references).

## References
- `Documentation/Active-Plans/Diff-Utility-Plan.md`
- `Documentation/CODING_STANDARDS.md`
- Existing tests under `tests/unit/`

## Reporting
Provide progress updates via commits/PR description referencing this handoff. If clarifications arise, loop back to Clive before deviating from the plan.
