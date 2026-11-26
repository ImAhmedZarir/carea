# Workflow Guide: Deep Investigation, Verification & AgentEnv (Mode 3)

Use **Mode 3 (`deep-verification` -> `/rea`)** when studying self-owned or authorized binaries, JS/Electron apps, managed assemblies, UEFI firmware, or building reproducible `AgentEnv` sandboxes — with **no UI rebuild**.

> This example uses our self-owned [`examples/sample-target/`](../../examples/sample-target/README.md) web/JS utility to show both behavioral verification and `AgentEnv` export cleanly.

---

## 1. Configure Focused REA Tool Profiles

Inspect lean REA profiles via `carea mcp-profile`:

- Dynamic hot-cold discovery (`rea >= 6.10.0`): `carea mcp-profile rea-hot-cold`
- Native binary: `carea mcp-profile rea-native`
- JS / Web / Electron: `carea mcp-profile rea-web`
- Firmware / UEFI (`rea >= 6.10.0`): `carea mcp-profile rea-firmware`
- Managed .NET: `carea mcp-profile rea-managed`

---

## 2. Track A — Formal Verification of a Self-Owned Reimplementation

1. Start `/rea` and open the baseline target (`examples/sample-target/timer.mjs`) using `analyze_javascript_application` (`inspect_analysis_view` for paged detail).
2. Build declared obligations via `build_reconstruction_obligation_ledger` and trace key behaviors via `trace_application_feature` and `trace_javascript_semantics`.
3. Log unverified paths via `record_unknown`.
4. Evaluate an updated or rewritten module (`builder-workspace/timer.mjs`) against the ledger using `evaluate_reconstruction_coverage`, `compare_javascript_export_shapes`, and `verify_reconstruction`.
5. Export the authenticated bundle (`export_evidence_bundle`, `evidence_format: 2`).
   - Remember: `verify_reconstruction` verifies only the declared claims inside its finite `specification` object — never global equivalence. Missing coverage leaves obligations `unknown` or `partial`.

---

## 3. Track B — Exporting a Reproducible AgentEnv Sandbox

When turning a live HTTP/UI session of an owned web app (such as `python examples/sample-target/server.py --port 4173`) into an offline agent environment:

1. Inspect observable pages with `inspect_web_page` and `capture_web_screenshot`.
2. Record user interactions and API exchanges via `capture_browser_scenario`.
3. Check whether any secrets/tokens appear cleanly redacted before export.
4. Export with `export_environment_bundle` (`rea environment-build` / `rea environment-serve` / `rea environment-compare` in upstream REA CLI).

---

## 4. Recording Mode 3 in `carea` Checklist

Because Mode 3 skips Craft Anything UI rebuilds (`ca_check_targets: ["none"]`), `carea parity-report` records UI checks as `none` / `not_applicable` and ensures single-axis runs never falsely claim dual-axis parity.
