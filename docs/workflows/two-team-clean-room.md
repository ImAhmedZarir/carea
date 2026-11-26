# Workflow Guide: Two-Team Clean Room Process

Use **Mode 2 (Two-Team Clean Room Process)** when recreating an application whose behavior depends on internal client/server contracts, Electron IPC channels, state machines, or algorithms that observable screenshots alone cannot reveal.

> [!IMPORTANT]
> **Process Aid — Not a Legal Guarantee:** This workflow is an engineering process aid, **not legal advice and not a legal clean-room guarantee**. Craft Anything's `--clean-room` mode is a tool-level rule rather than an OS sandbox, and **a single person or continuous agent session acting as both Analyst and Builder does not constitute a true legal clean room**. See [`../../DISCLAIMER.md`](../../DISCLAIMER.md) and [`../../skills/_shared/clean-room-protocol.md`](../../skills/_shared/clean-room-protocol.md).

See worked example files produced by this workflow:
- Sanitized spec: [`../../examples/clean-room-spec.example.md`](../../examples/clean-room-spec.example.md)
- Handoff record: [`../../examples/handoff.example.json`](../../examples/handoff.example.json)

---

## 1. Workspace Layout

Maintain four strictly separated directories:

```text
<project-root>/
├── analyst-evidence/      # Lane A only: REA exported evidence bundle
├── airlock/               # Sanitized boundary only: clean-room-spec.md + carea-handoff.json
├── builder-workspace/     # Lane B only: clean project built under CA --clean-room
└── verification/          # Stage 4 only: parity-checklist.md + comparison outputs
```

---

## 2. Lane A — Analyst (REA Deep Mode)

Configure REA with minimal families matching the target (for example, an Electron/JS app):

```bash
# Example scoped env for Electron/JS analysis (REA >= 6.10.x)
REA_MCP_TOOL_FAMILIES=browser,electron,application,javascript-runtime,session
REA_MCP_INPUT_SCHEMA_PROFILE=compact
REA_MCP_OUTPUT_SCHEMA_PROFILE=off
```

1. **Inspect without dumping:**
   - For ASAR/JS apps: call `analyze_javascript_application` with `detail: "summary"`, then page modules/routes via `inspect_analysis_view`.
   - Trace target features via `trace_application_feature` and `trace_javascript_semantics`.
   - For packaged Electron apps, inspect `inspect_electron_fuses` before attempting live inspector attachment.
   - Build an obligation inventory with `build_reconstruction_obligation_ledger` and log unobserved gaps via `record_unknown`.
2. **Export & close:**
   - Save the complete evidence bundle to `analyst-evidence/session.bundle.json` with `export_evidence_bundle`.
   - Close any active native session (`close_binary`).
3. **Draft sanitized Airlock files:**
   - Write `airlock/clean-room-spec.md` using [`../../templates/clean-room-spec.template.md`](../../templates/clean-room-spec.template.md) containing only abstract behaviors, value-free schemas, state tables, math formulas, and deterministic test vectors.
   - Write `airlock/carea-handoff.json` matching [`../../schemas/carea-handoff.schema.json`](../../schemas/carea-handoff.schema.json) with opaque `ev_...` IDs (no raw code or secrets).

---

## 3. Airlock Gate (Human / Separate Audit)

Before starting Lane B:
1. Verify `airlock/clean-room-spec.md` and `airlock/carea-handoff.json` contain **zero** source snippets, pseudocode, disassembly, CSS/DOM dumps, or copyrighted logos/text.
2. Validate `airlock/carea-handoff.json` against the JSON Schema and set `airlock.status` to `"passed"`.

---

## 4. Lane B — Builder (Craft Anything `--clean-room`)

Start a **fresh agent conversation** inside `builder-workspace/` with Craft Anything running in Clean-Room mode:

```bash
craft-anything-cli mcp --clean-room
```

1. Confirm Clean Room via `core_session_show`.
2. Read **only** `airlock/clean-room-spec.md`, the obligations/test vectors in `airlock/carea-handoff.json`, and optional observable UI captures (`web_site_capture`, `native_window_capture`).
3. Build fresh code via `rebuild_start`, `build_files_list`, `build_file_write`, `build_file_edit`, and `build_command_run`, generating original replacement assets (`assets_image_generate`) rather than reusing original media.
4. Run `rebuild_check` and `web_pixels_compare` / `web_walkthrough_check` to refine UI likeness.

---

## 5. Stage 4 — Dual Parity Verification

In a separate Verifier session (so Lane B never inspects `analyst-evidence/`):
1. Verify **Visual parity** with Craft Anything (`web_pixels_compare`, `web_walkthrough_check`, `runtime_captures_compare`).
2. Verify **Behavioral & Structural parity** with REA (`verify_reconstruction`, `evaluate_reconstruction_coverage`, `compare_javascript_export_shapes`, `compare_process_captures`) against `analyst-evidence/session.bundle.json` and the rebuilt artifact.
3. Record `passed` / `partial` / `failed` / `unknown` for each `obl_...` in `verification/parity-checklist.md` using [`../../templates/parity-checklist.template.md`](../../templates/parity-checklist.template.md). If repairs are needed, pass only failing test vectors or visual diffs back to Lane B.
