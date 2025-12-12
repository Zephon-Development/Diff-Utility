# Review Summary: Release Workflow Revamp & CLI Versioning

**Reviewer:** Clive  
**Date:** 2025-12-12  
**Branch Under Review:** `feature/release-revamp`

## Scope & Acceptance Criteria
- Hardening both release workflows so they run entirely under PowerShell on the KHAZAD-DUM Windows runner
- Ensuring every merge to `main` updates the `latest-release` tag+artifact, while tagged releases (`vX.Y.Z`) publish a permanent release _and_ refresh `latest-release`
- Surfacing the package version via `diff-utility -v/--version` plus corresponding documentation/tests
- Maintaining CODING_STANDARDS.md expectations (strict typing, linting, pytest coverage ≥80%, branch coverage ≥75%)

## Diffs & Tests Reviewed
- `.github/workflows/release-latest.yml`
- `.github/workflows/release-version.yml`
- `src/diff_utility/cli.py`
- `tests/unit/diff_utility/test_cli.py`
- `README.md`, `RELEASE_NOTES.md`, `pyproject.toml`, `VERSION.txt`, `src/diff_utility/__init__.py`
- Coverage artifact `coverage.json`

**Tests executed during review:**
- `python -m pytest --cov=src --cov-branch` → 88 passed, 2 warnings (custom `performance` marker), total coverage **96.21%**, branch coverage ≥94%

## Findings
1. **Blocker – Conflicting release metadata flags** (`.github/workflows/release-version.yml` lines 90-98)
   - The new "Update latest-release" step sets `generate_release_notes` twice—first `false`, then `true`—and also repeats `fail_on_unmatched_files`. YAML keeps the last value, so `latest-release` will now _generate release notes_, contradicting the stated intent of copying the pre-built body from the tagged release. This will spam auto-generated notes every time a tag is pushed and makes the workflow harder to reason about. Please drop the duplicate keys and keep `generate_release_notes: false` for the latest-release update.

## Next Steps / Requests for Claudette
- Clean up the duplicated keys in `.github/workflows/release-version.yml` so the latest-release job inherits the intended settings (no release notes, single `fail_on_unmatched_files`).
- After adjusting, re-run the standard lint/type/test suite to keep coverage data in sync and update this branch.

Once the workflow file is corrected, I can re-review quickly to green-light the merge.

## Re-Review (2025-12-12 PM)
- **Scope recap:** Confirmed PowerShell-only release workflows, dual latest/version release behavior, CLI version flag UX/tests, and adherence to CODING_STANDARDS (strict typing, linting, ≥80% coverage w/ ≥75% branch coverage).
- **Diff spot-check:** `.github/workflows/release-version.yml` now has single `fail_on_unmatched_files` + `generate_release_notes: false` entry for the latest-release step; no other regressions observed.
- **Tests observed:** `black .`, `ruff check .`, `mypy --strict .`, `pytest --cov=src --cov-branch --cov-fail-under=80 -q`, `python scripts/check_branch_coverage.py --threshold 75` → all passed, overall coverage 96.21%, branch coverage 94.64%.
- **Finding status:** Previous blocker resolved; no new issues detected.
- **Next steps:** Green-light to merge `feature/release-revamp` once CI completes.
