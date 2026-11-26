# Dual-Axis Parity Verification Guide

Stage 4 verifies the rebuilt project across **Visual/UX likeness** (Craft Anything) and **Behavioral/Structural parity** (REA) without feeding raw original code back into the Builder Lane.

---

## 1. Axis A — Visual & Interactive Parity (Craft Anything Clean Room)

Run these checks from `builder-workspace/` with `craft-anything-cli` in `--clean-room` mode:

| Check Goal | Verified Tool / Command | What It Establishes |
|---|---|---|
| **Full rebuild likeness check** | `rebuild_check` | Runs CA's built-in multi-width comparison for websites, window pictures for apps/games, build health, mechanics checks, and credits. |
| **Screenshot pixel diff** | `web_pixels_compare` | Compares original observable screenshot vs rebuilt screenshot (mobile `375px`, tablet, desktop `1440px`). |
| **Interactive web walkthrough** | `web_walkthrough_check` | Executes a scripted flow against the rebuilt site and compares UI state against expectations. |
| **Desktop / app capture diff** | `native_window_capture`, `runtime_captures_compare` | Captures rendered desktop window/UI states and compares observable runs without inspecting internal binaries. |

---

## 2. Axis B — Behavioral, API & Structural Parity (REA Verifier)

Run these checks in an **independent Verifier session** (using `analyst-evidence/` and the clean build output in `builder-workspace/`):

| Target Domain | Verified REA Tools | What It Establishes (and Limits) |
|---|---|---|
| **JS / Web / Electron Logic** | `build_reconstruction_obligation_ledger`, `evaluate_reconstruction_coverage`, `verify_reconstruction`, `compare_source_to_bundle`, `compare_javascript_export_shapes` | Evaluates declared behavioral obligations, typed `specification` inputs, export shapes, and coverage; `verify_reconstruction` proves only declared claims within the finite `specification`, not global equivalence. |
| **.NET / Managed Reconstruction** | `import_managed_reconstruction`, `compare_managed_members`, `verify_managed_native_boundaries` | Checks member signatures, native boundary declarations, and P/Invoke parity against managed evidence. |
| **Native / CLI Executables** | `capture_process_scenario`, `compare_process_captures`, `correlate_static_and_runtime`, `compare_functions`, `match_native_functions` | Compares observable terminal output, exit codes, and file effects across original vs rebuilt CLI runs (`compare_process_captures` runs on Linux/macOS PTY captures or compares retained captures on Windows). |
| **Web API / Page Captures** | `compare_web_captures`, `compare_web_screenshots` | Compares captured endpoints, DOM/accessibility states, and screenshots while preserving capture coverage limits. |
| **WASM / Package Inventories** | `compare_wasm_interfaces`, `compare_artifacts` | Checks exported/imported WASM module interfaces or package occurrence inventories. |

---

## 3. Recording Honest Results (`parity-checklist.md`)

For every obligation `obl_...` in `carea-handoff.json`, record one of four verified statuses in [`../../../templates/parity-checklist.template.md`](../../../templates/parity-checklist.template.md):

- **`passed`:** Both declared CA visual/walkthrough checks and REA behavioral/spec checks passed with complete coverage for that claim.
- **`partial`:** Observable checks pass within tested bounds, but upstream coverage or discovery is partial (state exact limitations).
- **`failed`:** Observed behavior or layout diverges; return **only** the failing test vector or visual diff description to Lane B for refinement.
- **`unknown`:** Required evidence could not be observed (e.g., missing runtime/device or unestablished indirect calls); record via `record_unknown` / `core_unknown_add`.
