---
name: carea
description: Autonomous reverse engineering orchestrator (/carea <target>) executing combined Stage 1 (/rea internal deep analysis) -> Stage 2 (/ca observable UI/runtime study ONLY, without building) -> Stage 3 (complete architecture.md, design-system.md, and full-breakdown.md report). Strictly analysis-first; never invokes rebuild_start or writes replacement app code unless explicitly asked to rebuild (or when running opt-in Mode 1/2/4/5 builds via carea airlock CLI gates).
---

# carea — Craft And Reverse Engineer Everything

> *"Break It Down. Build It Better."*

`carea` is an **independent, unofficial Level-1 orchestration layer** coordinating external **REA (`rea`)** and **Craft Anything (`craft-anything-cli`)**. Neither engine is vendored or bundled.

---

## HARD RULE: Analysis & Breakdown ONLY — NEVER Auto-Build an App

When invoked as `/carea <target>` (for example `/carea app.apk`, `/carea https://example.com`, `/carea tool.exe`), execute an **autonomous reverse-engineering pipeline ONLY**:

- **DO NOT** call `rebuild_start`, `rebuild_check`, `build_files_list`, `build_file_write`, `build_file_edit`, `build_command_run`, `project_build_finish`, `assets_image_generate`, or scaffold application source code.
- Even if Stage 2 delegates to Craft Anything's UI/runtime observation tools, **STOP after UI study & capture (`core_report_save`)**. Rebuilding is strictly **OPT-IN** when the user explicitly says `"rebuild"`, `"build it"`, `"clone it"`, or asks for Mode 1 / 2 / 4 / 5 implementation.

---

## 0. Mandatory 3-Stage Autonomous Pipeline (`/carea <target>`)

Auto-classify `<target>` immediately from its path, URL, or extension (see [`references/intent-router.md`](references/intent-router.md)) and run **all three stages in order without stalling on boilerplate questions**:

### Stage 1 — First `/rea` (Internal Architecture & Logic Extraction)
1. Initialize REA cleanly with lean schema budgets (`REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` or target-scoped `REA_MCP_TOOL_FAMILIES` + `compact` input + `off` output).
2. Inspect internals using REA tools suited to `<target>`:
   - Web / Electron (`https://...`, `*.asar`, JS): `analyze_javascript_application`, `inspect_web_page`, `inspect_web_network_capture`, `trace_application_feature`, `inspect_electron_fuses`, `recover_javascript_sources`, `analyze_web_bundle`, `list_electron_targets`.
   - Android (`*.apk`, `*.aab`): `inspect_android_package`, `decode_android_resources`, `search_android_classes`, `inspect_android_class`, `inspect_android_method`, `inspect_android_jni_bindings`, `identify_flutter_build`, `inspect_dart_aot`, `inspect_apk_signature`, `project_android_application_graph`.
   - Native / Managed / Firmware (`*.exe`, `*.dll`, ELF, Mach-O, `.nupkg`, `.bin`): `open_binary`, `binary_overview`, `inspect_artifact`, `analyze_function`, `inspect_managed_artifact`, `inspect_pe_imports`, `inspect_pe_certificates`, `inspect_pe_load_config`, `inspect_pe_resources`, `inspect_native_exports`, `inspect_binary_hardening`, `inspect_elf_notes`, `inspect_go_binary`, `inspect_rust_binary`, `inspect_il2cpp_metadata`, `inspect_model_artifact`, `inspect_wasm_artifact`, `inspect_evm_interface`, `inspect_sqlite_database`, `inspect_python_pyc`, `inspect_erlang_beam`, `inspect_kernel_module`, `inspect_kernel_build_config`, `inspect_apple_ips`, `inspect_recorded_crash`, `inspect_binary_layout`, `inspect_pcap_capture`, `decode_signal_recording`, `inspect_uefi_firmware`.
3. Record incomplete or unanalyzed paths with `record_unknown` (`unk_...`), preserve exact `ev_...` IDs, and close native/debugger sessions cleanly (`close_binary`).

### Stage 2 — Second `/ca` (Observable Study & Capture ONLY — NO Rebuild)
1. Connect Craft Anything (`craft-anything-cli mcp --clean-room` without `--all-tools`; check `core_session_show`). Use `--deep` ONLY when inspecting explicitly authorized internal resources (`deep_private: true`).
2. Capture observable screens, layout behavior, and user flows WITHOUT triggering code generation:
   - Websites: `web_site_open` -> `web_site_capture` (mobile & desktop widths) -> `web_page_states_capture` -> `web_site_close`.
   - Desktop runtime: `native_window_capture`, `runtime_ui_read`, `runtime_walkthrough_record`.
   - Android UI (`adb`): `adb_devices_find`, `adb_screenshot_take`, `adb_window_show`, `adb_display_show`.
3. Save clean study findings inside Craft Anything via `core_brief_write`, `core_finding_record`, `core_unknown_add`, and `core_report_save` — then **STOP Craft Anything before `rebuild_start`**.

### Stage 3 — Synthesize the Complete Reverse-Engineered Breakdown
Merge Stage 1 (REA internals) + Stage 2 (CA visual/UI study) into one organized breakdown (writing the files or presenting the complete structured sections):
1. **`full-breakdown.md`** ([`../../templates/full-breakdown.template.md`](../../templates/full-breakdown.template.md)): unified breakdown separating `[OBSERVED ev_...]`, `[CA CAPTURE]`, `[INFERRED]`, and `[UNKNOWN unk_...]`.
2. **`architecture.md`** ([`../../templates/architecture-report.template.md`](../../templates/architecture-report.template.md)): entrypoints, subsystems, module graph, state machines, API/IPC schemas, storage layout, and security boundaries.
3. **`design-system.md`** ([`../../templates/design-system.template.md`](../../templates/design-system.template.md)): screen/route inventory, responsive breakpoints, layout spacing rules, typography roles, semantic palette tokens, and interaction states.

---

## 1. Opt-In Rebuild & Clean-Room Airlock Modes (Only When Explicitly Asked)

Only switch out of Reverse-Engineer-Only mode if the user explicitly requests building software:
- **Mode 1 (`/ca` Clean-Room UI Rebuild):** Observable UI rebuild (`craft-anything-cli --clean-room`).
- **Mode 2 (Two-Team Clean Room + Airlock CLI):** Full 4-directory pipeline (`analyst-evidence/`, `airlock/`, `builder-workspace/`, `verification/`) enforcing `carea init`, `carea isolation-check`, `carea spec-draft`, `carea airlock-lint --strict`, `carea validate-handoff`, human `carea airlock-sign`, Topology B fresh Lane B session, `carea parity-report`, and `carea return-feedback`.
- **Mode 3 (`/rea` Deep Verification / AgentEnv):** Forensics, `verify_reconstruction`, or `AgentEnv` export only.
- **Mode 4 (`private-deep-rebuild`, `deep_private: true`):** Authorized direct internal rebuild (**NOT clean-room**; requires loud banner).
- **Mode 5 (`game-rebuild`) & Mode 6 (`android-mobile`) builds:** Subject to strict no-asset-copy and `game_*` Deep-only caveats in [`references/modes.md`](references/modes.md).

## References

- Auto-intake routing & CA study-only guards: [`references/intent-router.md`](references/intent-router.md)
- Opt-in Modes 1–6 & Lane B Topologies A/B: [`references/modes.md`](references/modes.md)
- Breakdown templates: [`../../templates/full-breakdown.template.md`](../../templates/full-breakdown.template.md) · [`../../templates/architecture-report.template.md`](../../templates/architecture-report.template.md) · [`../../templates/design-system.template.md`](../../templates/design-system.template.md)
- Shared protocols: [`../_shared/clean-room-protocol.md`](../_shared/clean-room-protocol.md) · [`../_shared/evidence-handoff.md`](../_shared/evidence-handoff.md) · [`../_shared/parity-verification.md`](../_shared/parity-verification.md)
