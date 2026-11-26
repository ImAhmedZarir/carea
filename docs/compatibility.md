# Upstream Compatibility Matrix

<!-- GENERATED FROM compat/matrix.json via `python scripts/render-compatibility.py`. DO NOT HAND-EDIT. -->

`carea` target release **`1.2.0`** supports handoff schema versions `1.0.0`, `1.1.0` (current: `1.1.0`).
All version bounds in `carea` (`carea doctor`, `scripts/verify-upstream.sh`, and `scripts/verify-upstream.ps1`) read [`compat/matrix.json`](../compat/matrix.json) as the single source of truth.

## Engine Version Matrix

| Engine | Package / Binary | Recommended | Minimum Compatible | Runtime Requirement | Maturity & Policy |
| --- | --- | --- | --- | --- | --- |
| **[REA](https://github.com/morluto/rea)** | `rea-agents` (`rea`) | `6.10.1` | `6.8.0` | `^22.23.4 || ^24.22.1 || >=26.12.1` | MIT |
| **[Craft Anything](https://github.com/storytold/craft-anything)** | `craft-anything-cli` (`craft-anything-cli`) | `0.6.1` | `0.6.0` | Prebuilt binary or Rust toolchain | MIT OR Apache-2.0 — **early-alpha** |

## Supported Version Ranges

### REA (`rea-agents`)

| Range | Status | Behavior Notes |
| --- | --- | --- |
| `>=6.10.0, <6.11.0` | `supported` | Recommended baseline (`evidence_format: 2`, `uefi` family, `hot-cold` catalog profile, `compact`/`off` schema profiles; `full` schema profiles rejected). |
| `>=6.8.0, <6.10.0` | `limited` | Older evidence shape and tool catalog; lacks `uefi` family and `6.10.0+` schema/setup features. |

### Craft Anything (`craft-anything-cli`)

| Range | Status | Behavior Notes |
| --- | --- | --- |
| `>=0.6.0, <0.7.0` | `supported` | Verified clean-room and deep modes; 322 CLI commands in 0.6.0, 303 engine tools / 320 total documented in 0.6.1 across 17 toolsets; early alpha. |

## Observed Verification Evidence

Instead of generic "Tested with" claims, the table below records exactly what was verified vs left unverified on the build environment:

### REA

- **`6.10.1`** (`upstream-source-and-docs`):
  - Verified: 264 advertised tool schema files in scripts/verify/advertised-schemas/tools/
  - Verified: 19 TOOL_FAMILY_IDS in src/contracts/toolFamilyIds.ts
  - Verified: REA_MCP_TOOL_CATALOG_PROFILE=hot-cold (5 initial tools + discover_tools)
  - Verified: REA_MCP_INPUT_SCHEMA_PROFILE=compact and REA_MCP_OUTPUT_SCHEMA_PROFILE=off|compact (full rejected)
  - Verified: Node.js ^22.23.4 || ^24.22.1 || >=26.12.1 requirement in package.json
  - Unverified on build host: Local CLI execution (`rea --version`, `rea --help`, `rea doctor`) not run on build host because Node.js >=22 is absent.
- **`6.8.0`** (`live-mcp-server`):
  - Verified: Live `rea_rea` MCP `binary_session` tool responded in session.
  - Unverified on build host: Local CLI execution (`rea --version`) failed because host only had Deno node_compat and unbuilt plugin tree.

### Craft Anything

- **`0.6.0`** (`local-cli-and-live-mcp`):
  - Verified: `craft-anything-cli.exe --version` -> `craft-anything-cli 0.6.0`
  - Verified: `craft-anything-cli.exe doctor` -> `healthy: true`, `MCP server answered (protocol 2025-06-18, 30 tools listed)`
  - Verified: `craft-anything-cli.exe capabilities --json` -> `analysis_mode: clean-room`, `tools: 322`, 17 toolsets
  - Verified: Live `craft-anything:core_session_show` MCP call -> `clean_room: true`, `server.version: 0.6.0`
- **`0.6.1`** (`upstream-release-docs`):
  - Verified: GitHub release `v0.6.1` (`2026-11-12`)
  - Verified: `docs/tools.md`: 303 engine tools in 17 toolsets; `README.md`: 320 tools total; early alpha notice
  - Unverified on build host: Local `0.6.1` binary not installed on build host (host binary is `0.6.0`).

## Running Local Compatibility Checks

Run the upstream verification script for your OS to compare locally installed `rea` and `craft-anything-cli` binaries against `compat/matrix.json`:

```bash
# Linux / macOS / Git Bash
bash scripts/verify-upstream.sh
```

```powershell
# Windows PowerShell
pwsh -File scripts/verify-upstream.ps1
```

Or run `carea doctor` (which checks binaries, versions, and MCP config profiles directly against `compat/matrix.json`).

*Matrix updated: `2026-11-27`. Claim-by-claim evidence lives in [`docs/upstream-facts.md`](upstream-facts.md).*
