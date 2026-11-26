# Dual-Axis Parity Verification Guide

`carea` separates verification into two measurable axes and merges them with `carea parity-report` into `verification/parity-checklist.md`.

## Axis 1 — Observable / Visual & Runtime Parity (Craft Anything)

Run from `builder-workspace/` with Craft Anything (`--clean-room` for Modes 1, 2, 5, 6; `--deep` only if explicitly running authorized Mode 4):

| Check | Verified CA Tool | What It Measures |
| --- | --- | --- |
| **Multi-width rebuild likeness** | `rebuild_check` | Compares running build against captured reference across desktop/mobile viewports or app windows. |
| **Screenshot pixel diff** | `web_pixels_compare` | Pixel comparison between reference capture and rebuilt screen captures. |
| **Interactive web flow** | `web_walkthrough_check` | Executes scripted UI interaction steps against rebuilt site and verifies state transitions. |
| **Desktop window / UI tree** | `native_window_capture`, `runtime_ui_read`, `runtime_captures_compare`, `runtime_walkthrough_record` | Compares rendered desktop windows and accessible runtime UI states. |
| **Android observable UI** | `adb_screenshot_take`, `adb_window_show`, `adb_display_show`, `adb_log_read` | Captures observable Android screen layouts and logs (when `adb` is configured). |

## Axis 2 — Behavioral & Structural Parity (REA)

Run in the Verification / Analyst environment over rebuilt outputs + `analyst-evidence/` bundles:

| Domain | Verified REA Tools | What It Verifies |
| --- | --- | --- |
| **JS / Web / Electron obligations** | `build_reconstruction_obligation_ledger`, `evaluate_reconstruction_coverage`, `verify_reconstruction`, `compare_source_to_bundle`, `compare_javascript_export_shapes`, `trace_application_feature`, `trace_javascript_semantics` | Evaluates declared behavioral obligations, typed `specification` inputs, export shapes, and coverage. `verify_reconstruction` proves only declared claims within the finite `specification` — never global equivalence. |
| **Live web API / captures** | `compare_web_captures`, `compare_web_screenshots`, `inspect_web_network_capture` | Compares HTTP endpoints, response shapes, DOM structures, and screenshots. |
| **Native binary parity** | `match_native_functions`, `compare_functions`, `build_call_path`, `compare_process_captures`, `capture_process_scenario`, `trace_feature` | Compares function/call-path structures and observable syscall/process captures (`capture_process_scenario` + `compare_process_captures`). |
| **Packaged artifact / managed diff** | `compare_artifacts`, `compare_bundles`, `compare_managed_members`, `verify_managed_native_boundaries`, `find_changed_behavior` | Compares containers, .NET member/P-Invoke surfaces, or version deltas. |

## Merging Results & Verdict Rules

Generate the combined parity table using:

```bash
carea parity-report --handoff airlock/carea-handoff.json --ca-report <ca-results.json> --rea-report <rea-results.json> --out verification/parity-checklist.md
```

Every obligation `obl_...` receives one strict verdict:

- **`passed`**: **Both** required axes (Axis 1 observable CA check and Axis 2 behavioral REA check, or the sole required axis in single-engine Mode 1 / Mode 3) executed and passed with complete scope and zero unresolved blockers.
- **`partial`**: Checks pass within tested bounds, or one axis passed while the second axis has partial coverage, limited adapters, or `limitations` notes.
- **`failed`**: Rebuilt UI layout, pixel diff, API contract, or runtime behavior fails verification. Generate sanitized Lane-B remediation via `carea return-feedback`.
- **`unknown`**: Blocked by unverified/missing engine adapters, encryption/obfuscation, or unexecuted runtime verification (`unk_...` preserved).
