# Contributing to `carea`

Thank you for helping improve `carea`! Because `carea` is an independent Level-1 orchestration pack over **REA** and **Craft Anything**, contributions must follow the architectural and legal boundaries below.

## Core Rules for All Pull Requests

1. **No Vendoring or Upstream Brand Assets:**
   - Never copy, mirror, fork, or check in source files, compiled binaries, fonts, icons, or logos from `morluto/rea`, `storytold/craft-anything`, or third-party targets.
   - All Python CLI helpers must use the Python 3.10+ standard library only (`pyproject.toml` dependencies must stay empty unless explicitly discussed and approved).
2. **Verify Upstream Claims First:**
   - Never invent tool names, tool families, environment variables, CLI flags, or version numbers.
   - Any new upstream claim added to docs or skills must first be verified and recorded in [`docs/upstream-facts.md`](docs/upstream-facts.md) (`VERIFIED` status). Unverified claims must stay out of `skills/**`.
3. **Preserve Legal, Credit, and Licensing Separation:**
   - Original code, schemas, and docs are licensed under [MIT](LICENSE) (`Copyright (c) 2026 Ahmed Ishtiaque Zarir`).
   - Do not modify `BRAND.md`, `docs/brand/LICENSE-brand.txt`, `NOTICE`, `THIRD_PARTY_NOTICES.md`, or `DISCLAIMER.md` in a way that weakens attribution, implies upstream endorsement, or claims legal clean-room immunity.
4. **Update Single Sources Rather Than Duplicating:**
   - Upstream compatibility bounds live only in [`compat/matrix.json`](compat/matrix.json). After editing it, run:
     ```bash
     python scripts/render-compatibility.py
     ```
   - Sync bundled package copies (`src/carea/data/`) when changing `compat/matrix.json` or `schemas/carea-handoff.schema.json`.

## Running Local Checks Before Opening a PR

```bash
python -m unittest discover -s tests -v
python scripts/render-compatibility.py --check
python scripts/check_repo.py
```

On Windows PowerShell:

```powershell
python -m unittest discover -s tests -v
python scripts\render-compatibility.py --check
python scripts\check_repo.py
```

Every PR must pass unit tests, schema validation across examples and fixtures, markdown link checks, manifest validation, and the upstream-asset-ban check.
