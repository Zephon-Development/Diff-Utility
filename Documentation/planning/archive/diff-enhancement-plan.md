# Diff Enhancement Plan: Detect Line Insertions and Deletions

**Prepared by: Tracy**  
**Date:** December 11, 2025  
**Feature Branch:** feature/diff-insertions-deletions  

## Overview
The current diff utility performs line-by-line comparison, which works for exact matches but fails to detect insertions or deletions of entire lines. This causes the entire rest of the file to be flagged as different due to line number shifts. We need to implement a proper diff algorithm that identifies added, removed, and unchanged lines accurately.

## Scope and Constraints
- **Scope:** Update the diff engine in `src/diff_utility/diff.py` (with CLI glue in `src/diff_utility/cli.py`) to detect line-level insertions and deletions using a sequence matching algorithm (e.g., Myers/`difflib.SequenceMatcher`) while preserving the current diff output style.
- **Constraints:** 
  - Maintain compatibility with the existing CLI surface and output format (the `---` block structure and token-level annotations).
  - Keep performance acceptable for typical file sizes (target <1s for ~10k lines).
  - Adhere to type safety and testing standards per CODING_STANDARDS.md, including branch coverage enforcement via `scripts/check_branch_coverage.py`.
- **Out of Scope:** Changes to file-level comparisons or non-text file handling.

## Success Metrics
- Diff output correctly identifies inserted/deleted lines without flagging subsequent lines as changed.
- Unit tests achieve ≥80% coverage and ≥75% branch coverage (per `scripts/check_branch_coverage.py`), including edge cases for insertions/deletions.
- No regressions in existing functionality or CLI output format.
- Performance benchmark: Diff time < 1 second for files up to 10,000 lines.

## Implementation Approach
1. **Line-level diffing:** Use `difflib.SequenceMatcher` (Myers-based) on full line lists to produce opcodes (`equal`, `insert`, `delete`, `replace`). This provides precise line insert/delete detection and avoids cascading false positives.
2. **Integrate with existing annotator:**
  - For `equal` opcodes: skip emission.
  - For `insert`: emit a diff block with empty/placeholder original line and the inserted line, marking the entire inserted line as an addition (consistent with current `++...++` token markers).
  - For `delete`: emit a diff block with the deleted line as the original and an empty/placeholder new line, marking the entire deleted line as a removal (`--...--`).
  - For `replace`: continue to use `annotate_changes` at the token level so intra-line modifications remain highlighted.
  - Preserve the existing `---` block formatting in `diff_lines`/`diff_files` so CLI consumers are unaffected.
3. **Code updates:**
  - Refactor `diff_lines` in `src/diff_utility/diff.py` to drive output from the line-level opcodes rather than index-by-index comparison.
  - Ensure `diff_files` and CLI glue (`src/diff_utility/cli.py`) remain compatible; adjust only if parameters or behaviors change (aim to avoid breaking changes).
  - Add/confirm type annotations for any new helpers.
4. **Testing:** Extend `tests/unit` to cover insert-only, delete-only, mixed insert+delete, replace, and large-file regression scenarios. Include CLI-level snapshot/fixture tests if needed to validate formatting.
5. **Documentation:** Update `README.md` (and any CLI help text) with before/after diff examples demonstrating inserted/deleted lines and unchanged downstream lines.

## References
- CODING_STANDARDS.md: Sections 2.1 (Type Annotations), 3.1 (Testing Standards), 4.1 (Documentation).

## Risks and Mitigations
- Risk: Performance degradation for large files.
  - Mitigation: Profile and optimize; consider chunking if needed.
- Risk: Breaking changes to output format.
  - Mitigation: Maintain backward compatibility or provide migration guide.

## Next Steps
- Submit this revised plan to Clive for approval.
- Upon approval, proceed with implementation (assign Claudette for algorithm-heavy work; Georgina for integration/testing focus).