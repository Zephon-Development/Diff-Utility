# Diff-Utility Project Plan

**Author:** Tracy (Planning)  
**Date:** December 11, 2025  
**Standards:** See `Documentation/CODING_STANDARDS.md` — key refs: §1 (Python 3.11+, dependency locking), §2 (strict typing, no `Any`), §3 (Ruff/Black), §4 (coverage ≥80% lines / ≥75% branches), §5 (Google-style docstrings for public APIs).

## Objective
Deliver a CLI tool "Diff Utility" that compares two text files line-by-line with custom whitespace handling, skips identical lines, and emits a custom diff format. Also rebrand all template references to Diff-Utility (code, tests, docs, metadata).

## Scope
- **Rebrand:** Rename package and all identifiers from `template/PythonTemplate` to `diff_utility/Diff-Utility`; update docs, paths, imports, metadata.
- **CLI:** Provide `diff-utility <file1> <file2>` writing to stdout only (no extra flags by default to avoid scope creep). Minimal errors/exit codes.
- **Diff Logic:**
  - Whitespace handling: ignore quantity differences (collapse consecutive internal whitespace for comparison) but detect new/missing whitespace boundaries.
  - Identical normalized lines: skip emitting.
  - Changed lines: emit block
    ```
    ---
    [file 1 line]
    [file 2 line]
    
    [changes]
    ```
    where `[changes]` is file2 line with `++...++` around additions vs file1 and `--...--` around deletions.
- **Testing:** Unit coverage for parsing, whitespace normalization, diff generation, CLI behavior; meet standards coverage thresholds.

## Constraints
- Python 3.11+ (Standards §1.1).
- No new runtime deps unless justified; prefer stdlib (`difflib`, `argparse`, `pathlib`, `re`).
- Strict typing, no `Any`; comply with mypy strict config (Standards §2.2).
- Formatting/linting via Black/Ruff (Standards §3).
- Coverage ≥80% lines, ≥75% branches enforced (Standards §4.1).
- Docs current with code; public APIs need Google-style docstrings (Standards §5).

## Success Metrics
- All template references removed/renamed to Diff-Utility/diff_utility.
- CLI produces specified format; whitespace rules honored; identical lines omitted.
- Tests cover whitespace edge cases, additions/deletions, empty files, mixed spacing; coverage thresholds met.
- CI passes (Black, Ruff, mypy, pytest, branch coverage script) on Grimslade.
- README/metadata accurately describe Diff Utility usage and behavior.

## Architecture & Design
- **Modules:**
  - `src/diff_utility/diff.py`: core functions for line loading, normalization, comparison, and change annotation.
  - `src/diff_utility/cli.py` (or `__main__.py`): argparse-based CLI entry; wires files to diff engine; handles errors/status codes.
  - `src/diff_utility/__init__.py`: exports public API (`diff_files`, `compare_lines`, etc.).
- **Whitespace Handling (resolved spec):**
  - Preserve original lines (minus trailing `\n`) for output; maintain normalized variants only for equality checks.
  - Normalization algorithm: remove trailing newline; leave leading/trailing spaces intact; collapse any run of one-or-more internal whitespace chars (space, tab, etc.) into a single space using `re.sub(r"\s+", " ", line)`.
  - Equality rule: lines are considered equal when their normalized forms match; this ignores whitespace quantity but still detects added/removed whitespace sections because token diff operates on originals.
  - Examples:
    - `"Hello   World"` vs `"Hello World"` ⇒ equal (normalized to `Hello World`).
    - `"Hello\tWorld"` vs `"Hello World"` ⇒ equal (tab collapsed).
    - `"Hello World.How"` vs `"Hello World. How"` ⇒ different (missing boundary space introduces token difference).
    - Leading/trailing spaces retained in originals so boundary insertions are visible in token diff.
- **Diff Detection and Annotation (resolved):**
  - If normalized lines match ⇒ skip.
  - Tokenization for changed lines: split originals with `re.findall(r"\s+|\S+", line)` to keep whitespace tokens explicit and in order.
  - Use `difflib.SequenceMatcher` on token lists. For opcode handling:
    - `equal`: emit tokens as-is into the `[changes]` line.
    - `insert` (tokens only in file2): wrap each inserted token with `++...++` (whitespace tokens rendered literally inside the markers, e.g., `++ ++` for a single space, `++\t++` if a tab is present).
    - `delete` (tokens only in file1): wrap with `--...--`.
    - `replace`: treat as delete of file1 tokens (with `--...--`) followed by insert of file2 tokens (with `++...++`).
  - Compose annotated line by joining annotated tokens; no additional spacing beyond token content.
  - Worked example:
    - file1: `"Hello World.How are you"`
    - file2: `"Hello World. How are you"`
    - Tokens1: `Hello` ` ` `World.How` ` ` `are` ` ` `you`
    - Tokens2: `Hello` ` ` `World.` ` ` `How` ` ` `are` ` ` `you`
    - Annotation result: `Hello --World.How-- ++World.++ ++ ++How++ are you`
- **Output Format:** Compose per-changed-line blocks with leading `---` separator; emit original file1 line, original file2 line, blank line, then annotated `[changes]` line. Overall output to stdout in file order.
- **CLI Behavior (resolved):**
  - Positional args: `file1`, `file2` (paths). No extra flags in v1. Errors reported to stderr; exit 0 on success, 2 on argument error, 1 on I/O failure.

## Resolved Decisions (per Clive feedback; proceed without ambiguity)
1. **Package name:** use Pythonic `diff_utility` (underscore) everywhere (code, imports, metadata). Repo name remains Diff-Utility.
2. **CLI options:** v1 ships with positional args only, output to stdout. No `--output`, `--ignore-case`, or context flags to avoid scope creep. Can be added later with explicit approval.
3. **Whitespace rule:** resolved spec in Architecture; leading/trailing preserved, internal runs collapsed for comparison only.
4. **Tokenization & annotation:** resolved in Architecture; regex keeps whitespace tokens; replace handled as delete+insert; whitespace insertions/deletions are visibly marked inside markers.
5. **Large files:** assume moderate text files; load into memory. No streaming support in v1. Binary files out of scope.

## Implementation Plan (sequenced)
1. **Rebrand Template**
   - Rename package dir `src/template/` → `src/diff_utility/`; adjust `__init__.py`, `py.typed` path.
   - Update imports in code/tests; rename tests folder `tests/unit/template/` → `tests/unit/diff_utility/`.
   - Update `pyproject.toml`: project `name`, `description`, entry points (if any), package include paths.
   - Update README to describe Diff Utility, commands, examples, structure.
2. **Core Logic**
   - Implement `diff.py` with:
     - `read_lines(path: Path) -> list[str]` (newline preserved handling).
     - `normalize_line(line: str) -> str` per whitespace policy.
     - `lines_equal_norm(a: str, b: str) -> bool` (uses normalization).
     - `annotate_changes(line1: str, line2: str) -> str` (word-level diff with ++/-- markers; handles whitespace tokens).
     - `diff_lines(lines1: list[str], lines2: list[str]) -> Iterable[str]` yielding formatted blocks.
     - `diff_files(path1: Path, path2: Path) -> str` (join blocks).
   - Ensure pure functions for easy testing; no `Any`; mypy-clean.
3. **CLI**
   - Implement `cli.py` (or `__main__.py` with console_script entry) using argparse.
   - Wire to `diff_files`; handle file-not-found/permission errors with user-friendly messages; unit tests for argument parsing and error codes.
4. **Testing**
   - Add unit tests under `tests/unit/diff_utility/`:
     - Normalization cases: multiple spaces vs single, tabs vs spaces, missing space between words.
     - Identical normalized lines skipped.
     - Add/delete tokens: ensure ++/-- markers correct.
     - Mixed whitespace insertions ("Hello World.How" vs "Hello World. How").
     - Empty files, single-line files, trailing newline differences.
     - CLI: successful run, missing file error, optional flags behavior.
   - Achieve ≥80% line / ≥75% branch coverage (Standards §4.1); prefer ~100% on new modules.
5. **Docs & CI Verification**
   - Update README usage examples (CLI invocation, sample output).
   - Note whitespace policy explicitly.
   - Run Black, Ruff, mypy, pytest, branch coverage script; ensure clean.

## Testing Strategy
- Unit tests only (fast, deterministic) per Standards §4.5; mark with `@pytest.mark.unit`.
- Fixtures per Standards §4.6–§4.7:
  - Use `tmp_path` to create temp input files for CLI and diff tests.
  - Consider shared helpers in `tests/conftest.py` for sample content generation.
- Cover normalization, annotation, and skip logic with table-driven cases.
- Capture stdout/stderr for CLI using `capsys`/`capfd`; assert exit codes.
- Validate coverage reports; ensure no uncovered branches in diff logic; target ~100% on new modules.

## Risks & Mitigations
- **Whitespace tokenization ambiguity:** If markers become noisy, adjust tokenization (Decision Point 4); keep implementation isolated for refactor.
- **Large files memory:** If needed, switch to streaming line diff generator; current plan acceptable for moderate files.
- **Windows newline handling:** Use text mode with universal newlines; keep `\n` stripping consistent in normalization.

## Deliverables
- Updated package/tests/docs reflecting Diff-Utility.
- Core diff engine and CLI implemented with strict typing.
- Comprehensive unit test suite meeting coverage thresholds.
- Updated README and plan archived in `Documentation/Active-Plans/`.

## Next Steps for Clive
- Confirm Decision Points 1–5 or adjust scope.
- Approve plan and assign implementation (Claudette/Georgina).
