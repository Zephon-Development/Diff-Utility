# Review Summary

## Scope & Acceptance Criteria
- Restore `.github/workflows/ci.yml` so CI runs on pushes/PRs targeting `main` with cached virtualenv and tooling (black, ruff, mypy, pytest, branch coverage script)
- Ensure workflow adheres to Documentation/Reference/CODING_STANDARDS.md expectations (Python 3.11, coverage ≥80%, no degraded tooling)

## Diffs Reviewed
1. `.github/workflows/ci.yml` – reinstated `on` triggers, fixed corrupted "Activate virtualenv path" run block (added missing `else`/`fi`), removed file duplication, fixed YAML syntax (unescaped quotes in run commands)
2. Release workflow logs – inspected `release-latest.yml` run on KHAZAD-DUM; failure due to PowerShell execution policy preventing `actions/setup-python@v4` from running setup.ps1
3. Version/license updates – harmonized version to 1.0.0 across README.md, pyproject.toml, VERSION.txt; updated license to GPL-3.0-or-later in pyproject.toml/README.md, added LICENSE file

## Findings
- **Blocker**: Self-hosted runner `KHAZAD-DUM` has PowerShell execution policy set to Restricted, blocking `actions/setup-python@v4` (and potentially other actions using PowerShell scripts). Workflow step "Allow PowerShell scripts" sets policy for its process only, not affecting action subprocesses.
- **No blockers** for CI workflow: Valid YAML, complete scripts, proper caching/tooling on Grimslade (Linux runner).
- Version harmony achieved: All files now reflect 1.0.0.
- License updated to GPL-3.0-or-later: Compliant with open-source standards.

## Tests / Automation
- CI run triggered by push (f4adda5); monitor for successful execution on Grimslade (lint/type/test, coverage ≥80%, artifact uploads).
- Release workflow blocked by runner config; re-test after KHAZAD-DUM fix.

## Next Steps
1. Confirm CI run passes without syntax errors.
2. Configure KHAZAD-DUM runner: Set PowerShell execution policy to `RemoteSigned` or `Unrestricted` for the runner user/machine (e.g., `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine` as admin).
3. Re-run release workflow post-fix to validate .exe build and upload.
