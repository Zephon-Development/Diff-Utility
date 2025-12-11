# Revision Report — 2025-12-11 (Claudette)

## Context
Clive identified two blocking issues in the initial GitHub Actions workflows implementation. This document summarizes the corrective actions taken.

## Issues Identified by Clive

### Issue 1: Missing Step ID for Asset Upload
**Problem:** Both workflows referenced `${{ steps.create_release.outputs.upload_url }}` but the "Create release" step lacked `id: create_release`, causing GitHub Actions validation failure.

### Issue 2: Tag Reuse Failure on `latest-release`
**Problem:** `actions/create-release@v1` fails when attempting to create a release for an existing tag. The `latest-release` workflow would succeed once, then fail on every subsequent push to `main` with "Validation Failed: Tag already exists".

## Solution Implemented

### Approach: Migrate to `softprops/action-gh-release@v1`
Replaced the deprecated two-step process (`actions/create-release@v1` + `actions/upload-release-asset@v1`) with the modern `softprops/action-gh-release@v1` action.

**Benefits:**
- **Native tag overwriting** — the action automatically handles updating existing releases and re-uploading assets
- **Simplified workflow** — single step for release creation and asset upload
- **Active maintenance** — modern action vs deprecated GitHub actions
- **Better error handling** — clearer failure messages and retry logic

### Changes Made

#### `.github/workflows/release-latest.yml`
**Before:**
```yaml
- name: Create release
  uses: actions/create-release@v1
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    tag_name: latest-release
    ...

- name: Upload executable
  uses: actions/upload-release-asset@v1
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    upload_url: ${{ steps.create_release.outputs.upload_url }}
    ...
```

**After:**
```yaml
- name: Create or update release
  uses: softprops/action-gh-release@v1
  with:
    tag_name: latest-release
    name: Latest Release (v${{ steps.version.outputs.version }})
    body: |
      Automated latest release for Diff-Utility v${{ steps.version.outputs.version }}
      
      This release contains the latest stable executable.
    draft: false
    prerelease: false
    files: ./dist/diff-utility.exe
    fail_on_unmatched_files: true
    generate_release_notes: false
```

**Impact:** On subsequent pushes to `main`, the action will update the existing `latest-release` tag, replace the release body/name, and re-upload the `.exe` file. No manual tag deletion required.

#### `.github/workflows/release-version.yml`
**Before:**
```yaml
- name: Create release
  uses: actions/create-release@v1
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    tag_name: version-${{ inputs.version }}
    ...

- name: Upload executable
  uses: actions/upload-release-asset@v1
  ...
```

**After:**
```yaml
- name: Create version release
  uses: softprops/action-gh-release@v1
  with:
    tag_name: version-${{ inputs.version }}
    name: Version ${{ inputs.version }}
    body: |
      Release for Diff-Utility v${{ inputs.version }}
      
      This is a tagged version release containing the executable.
    draft: false
    prerelease: false
    files: ./dist/diff-utility.exe
    fail_on_unmatched_files: true
    generate_release_notes: true
```

**Impact:** Simplified to single step; added `generate_release_notes: true` for automatic changelog generation from commit messages.

## Verification Performed

### Quality Gates (All Passed)
```powershell
python -m black --check .           # ✓ All files formatted
python -m ruff check .              # ✓ All checks passed
python -m mypy --strict .           # ✓ No type errors
python -m pytest --cov=src --cov-branch --cov-fail-under=80 -q
                                     # ✓ 93.86% line coverage / 96.15% branch coverage
python scripts/check_branch_coverage.py --threshold 75
                                     # ✓ Branch coverage meets threshold
```

### Build Verification
```powershell
python build_exe.py                 # ✓ Build successful
.\dist\diff-utility.exe --help      # ✓ Executable runs correctly
```

### Commit Status
- Changes committed to `1c8bc3d` (amended previous commit)
- Total diff: 154 insertions, 1 deletion across 5 files
- All workflows use correct `softprops/action-gh-release@v1` action
- No deprecated actions remain

## Compliance with Standards

### CODING_STANDARDS.md Adherence
- **§2 Type Safety:** `build_exe.py` maintains strict typing with explicit annotations
- **§3 Linting:** All Ruff checks pass; no exceptions required
- **§4 Testing:** Coverage thresholds met (≥80% line, ≥75% branch)
- **§1.2 Dependencies:** `pyinstaller>=6.0.0` properly declared in `pyproject.toml` dev group

### Workflow Best Practices
- Quality checks run before build (fail-fast on quality issues)
- Explicit Python version pinning (`3.11`)
- Self-hosted runner correctly specified (`KHAZAD-DUM`)
- Asset upload failures will fail workflow (`fail_on_unmatched_files: true`)

## Summary

Both blocking issues resolved:
1. ✅ Asset upload now handled by single action (no missing step ID reference)
2. ✅ Tag overwriting natively supported (no manual delete/recreate logic needed)

All quality gates pass. Implementation ready for Clive's final review and green-light.
