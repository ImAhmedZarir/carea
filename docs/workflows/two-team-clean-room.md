# Workflow Guide: Two-Team Clean Room Process (Mode 2)

Use **Mode 2 (`two-team-process` -> `/carea`)** when rebuilding an application whose correctness depends on internal API contracts, validation math, or state transitions (here demonstrated on the self-owned [`examples/sample-target/`](../../examples/sample-target/README.md) `pulse-timer` app).

> **Process Aid — Not a Legal Guarantee:** Mode 2 is an engineering isolation workflow, **not legal advice and not a legal clean-room guarantee**. Use **Topology `(b)`** (two separate sessions) and human review for practical separation (`docs/threat-model.md`).

See validated example artifacts produced in this pattern:
- Sanitized spec: [`../../examples/clean-room-spec.example.md`](../../examples/clean-room-spec.example.md)
- Handoff record: [`../../examples/handoff.example.json`](../../examples/handoff.example.json)

---

## 1. Initialize Workspace & Check Isolation

```bash
carea init ./pulse-timer-rebuild --mode two-team-process --topology b --target-name pulse-timer
carea isolation-check ./pulse-timer-rebuild
```

Verify the workspace contains four separate folders (`analyst-evidence/`, `airlock/`, `builder-workspace/`, `verification/`) and apply the recommended host-agent permission deny snippet printed by `carea isolation-check` so Lane B cannot read `analyst-evidence/`.

---

## 2. Lane A — Analyst Session (REA MCP Only)

Configure Session 1 with REA only (`carea mcp-profile two-team-lane-a` or scoped `REA_MCP_TOOL_FAMILIES=browser,electron,application,javascript-runtime,session`, `compact` input, `off` output):

1. Inspect `examples/sample-target/timer.mjs`, `server.py`, and live `http://127.0.0.1:4173/api/timer/status` with REA tools (`analyze_javascript_application`, `inspect_web_page`, `capture_browser_scenario`).
2. Build an obligation ledger (`build_reconstruction_obligation_ledger`) covering clamping bounds (`[1000, 86400000]`), `warning_active <= 10000ms`, and `GET /api/timer/status`.
3. Log unverified aspects via `record_unknown`.
4. Export the session evidence bundle strictly inside `analyst-evidence/` (`export_evidence_bundle`), close active sessions, and **end Session 1**.

---

## 3. Airlock Gate (`carea spec-draft` -> `airlock-lint` -> `airlock-sign`)

1. Extract only opaque IDs and structure into a draft skeleton:
   ```bash
   carea spec-draft ./pulse-timer-rebuild/analyst-evidence/bundle.json --out ./pulse-timer-rebuild/airlock/clean-room-spec.md
   ```
2. Edit `airlock/clean-room-spec.md` with mathematical bounds, state tables, HTTP shapes, and deterministic test vectors (zero JS/Python code fences, zero `analyst-evidence/` paths).
3. Update `airlock/carea-handoff.json` and run checks:
   ```bash
   carea airlock-lint ./pulse-timer-rebuild/airlock --strict
   carea validate-handoff ./pulse-timer-rebuild/airlock/carea-handoff.json
   carea airlock-sign ./pulse-timer-rebuild/airlock/carea-handoff.json --reviewer "<your-name>" --confirm-human-review
   ```

---

## 4. Lane B — Fresh Builder Session (Topology `(b)`, CA `--clean-room` Only)

Start a brand-new Session 2 configured solely via `carea mcp-profile two-team-lane-b` (`craft-anything-cli mcp --clean-room`, no REA MCP, no `--all-tools`):

1. Verify `clean_room: true` with `core_session_show`.
2. Read **only** `airlock/clean-room-spec.md` and `obligations[]` from `airlock/carea-handoff.json`.
3. Implement cleanly inside `builder-workspace/` via `rebuild_start` or `build_files_list`, `build_file_write`, `build_file_edit`, `build_command_run`, generating original visual controls.
4. Run CA visual checks (`rebuild_check`, `web_pixels_compare`, `web_walkthrough_check`) and save CA report JSON.

---

## 5. Stage 4 — Independent Dual Parity & Sanitized Feedback

In Session 3 (or original Analyst/Verifier environment reading both `analyst-evidence/` and `builder-workspace/`):

1. Run REA verification (`verify_reconstruction`, `evaluate_reconstruction_coverage`, `compare_web_captures`, `compare_javascript_export_shapes`) against the built output and export REA results JSON.
2. Merge both axes cleanly:
   ```bash
   carea parity-report \
     --handoff ./pulse-timer-rebuild/airlock/carea-handoff.json \
     --ca-report ./pulse-timer-rebuild/verification/ca-report.json \
     --rea-report ./pulse-timer-rebuild/verification/rea-report.json \
     --out ./pulse-timer-rebuild/verification/parity-checklist.md
   ```
3. If any obligation fails, emit sanitized feedback for Lane B:
   ```bash
   carea return-feedback \
     --handoff ./pulse-timer-rebuild/airlock/carea-handoff.json \
     --ca-report ./pulse-timer-rebuild/verification/ca-report.json \
     --rea-report ./pulse-timer-rebuild/verification/rea-report.json \
     --out ./pulse-timer-rebuild/airlock/return-feedback.md
   ```
