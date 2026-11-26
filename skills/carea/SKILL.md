---
name: carea
description: >
  Autonomous master reverse engineering orchestrator (/carea <target>) executing
  combined Stage 1 (/rea atomic 237-tool deep internal analysis) -> Stage 2 (/ca
  1:1 pro-dev UI & runtime study ONLY, without building) -> Stage 3 (complete
  full-breakdown.md, architecture.md, and design-system.md). Strictly analysis-first;
  never invokes rebuild_start or writes replacement app code unless explicitly asked to
  rebuild (or when running opt-in Mode 1/2/4/5/6 builds and clean-room airlock CLI gates).
---

# carea — Craft And Reverse Engineer Everything

> *"Break It Down. Build It Better."*

`carea` is an **independent, unofficial Level-1 master orchestration layer** unifying **REA (`rea-agents`, 237+ tools across 19 families)** and **Craft Anything (`craft-anything-cli`, 322 tools across 17 toolsets)** across **both MCP servers and CLI**.

---

## HARD RULE: Default `/carea <target>` = Reverse-Engineer-Only (NO Auto-Build)

When invoked as `/carea <target>` (e.g. `/carea app.apk`, `/carea https://example.com`, `/carea binary.exe`), run an **autonomous, full-depth reverse engineering pipeline ONLY**:

- **DO NOT** call `rebuild_start`, `build_files_list`, `build_file_write`, `build_file_edit`, `build_command_run`, `project_build_finish`, `assets_image_generate`, or generate replacement source trees.
- Stage 2 delegates to Craft Anything strictly for **observable UI, visual tokens, responsive layout, runtime state, and pixel capture (`core_report_save`)**. Code generation/rebuilding is strictly **OPT-IN** when the user explicitly requests `"rebuild"`, `"clone"`, `"build it"`, or runs Mode 1 / 2 / 4 / 5 / 6 builds.

---

## 0. Mandatory 3-Stage Autonomous Master Pipeline (`/carea <target>`)

Auto-classify `<target>` immediately from its path, URL, magic bytes, or extension ([`references/intent-router.md`](references/intent-router.md)) and execute **all 3 stages end-to-end without stalling**:

### Stage 1 — `/rea` Atomic & Nucleus-Level Internal Extraction
1. **Activate REA Full Catalog:** Prefer `carea mcp-profile rea-master` (`hot-cold` + `compact`/`off` + `discover_tools` + raised ASAR/matching/decoder ceilings) or target-scoped `REA_MCP_TOOL_FAMILIES` (all 19 families supported). Use `npx -y rea-agents@latest` CLI fallback if MCP tools are absent.
2. **Execute Multi-Layer Dissection (Layer 0 -> Layer 5 in [`../rea/SKILL.md`](../rea/SKILL.md)):**
   - **Web / SPA / Electron (`https://...`, `*.asar`, `.jsc`, JS):** `analyze_javascript_application` (`detail: "summary"`), `inspect_v8_code_cache`, `recover_javascript_sources`, `analyze_web_bundle`, `trace_web_module_imports`, `trace_application_feature`, `inspect_api_contract`, `inspect_web_network_capture` *(multi-origin `allowed_origins` for SPAs & `.saz` Fiddler traces)*, `inspect_electron_fuses`, `list_electron_targets`, `reconcile_javascript_runtime`.
   - **Android / Java / Flutter (`*.apk`, `*.aab`, `.jar`):** `inspect_android_package`, `inspect_apk_signature`, `decode_android_resources`, `search_android_classes`, `inspect_android_class`, `inspect_android_method`, `trace_android_references`, `inspect_android_jni_bindings`, `identify_flutter_build`, `inspect_dart_aot`, `open_jeb_project`/`decompile_jeb_item`, `project_android_application_graph`.
   - **Native ELF / PE / Mach-O / Go / Rust / IL2CPP / Firmware / Blockchain / Captures:** `inspect_byte_entropy`, `open_binary`, `inspect_artifact`, `inspect_binary_hardening`, `inspect_go_binary`, `inspect_rust_binary`, `inspect_pe_imports`, `inspect_pe_load_config`, `inspect_pe_certificates`, `inspect_pe_resources`, `inspect_elf_notes`, `inspect_elf_unwind_ranges`, `inspect_native_initializers`, `inspect_il2cpp_metadata`, `inspect_python_pyc`, `inspect_erlang_beam`, `inspect_wasm_artifact`, `inspect_evm_interface`, `inspect_sqlite_database`, `inspect_model_artifact`, `inspect_kernel_module`, `inspect_kernel_build_config`, `inspect_recorded_crash`, `inspect_apple_ips`, `inspect_uefi_firmware`, `inspect_pcap_capture`, `decode_signal_recording`, `analyze_function`, `trace_native_values`, `batch_decompile`, `get_call_graph`, plus runtime `start_frida_session` / `start_gdb_session` / `start_rizin_debug_session` when static analysis hits dynamic behavior.
3. Log gaps explicitly with `record_unknown` (`unk_...`), preserve exact `ev_...` Evidence IDs, export raw evidence if persisting (`export_evidence_bundle`), and close active sessions (`close_binary`, `close_frida_session`, `close_gdb_session`, `close_rizin_debug_session`).

### Stage 2 — `/ca` Pro-Dev 1:1 Observable & UI Study (NO `rebuild_start`)
1. Connect Craft Anything (`ca-clean-room` for observable surface study, or `ca-deep-full` `--deep --all-tools` when internal UI bundles/game archives/native views are needed under `deep_private: true`; check `core_session_show`).
2. Extract **1:1 UI/Product Forensics** ([`../ca/references/ui-forensics-playbook.md`](../ca/references/ui-forensics-playbook.md)):
   - **Websites:** `web_site_open` -> `web_site_capture` across **375px, 768px, and 1440px** -> `web_page_states_capture` (hover, focus, active, loading, empty, error, dark/light themes) -> `web_site_close`.
   - **Desktop Runtime:** `native_window_capture`, `runtime_ui_read`, `runtime_walkthrough_record`.
   - **Android Live UI (`adb`):** `engines_adb_check`, `adb_devices_find`, `adb_screenshot_take`, `adb_window_show`, `adb_display_show`, `adb_log_read`.
   - **Correlate tokens, spacing, typography, states, and API wiring** inside Craft Anything (`core_brief_write`, `core_finding_record`, `core_unknown_add`, `core_report_save`) — then **STOP before `rebuild_start`**.

### Stage 3 — Synthesize the Complete Engineering Breakdown
Deliver complete, production-detail documentation grounded strictly in `[OBSERVED ev_...]`, `[CA CAPTURE]`, `[INFERRED]`, and `[UNKNOWN unk_...]`:
1. **`full-breakdown.md`** ([`../../templates/full-breakdown.template.md`](../../templates/full-breakdown.template.md))
2. **`architecture.md`** ([`../../templates/architecture-report.template.md`](../../templates/architecture-report.template.md))
3. **`design-system.md`** ([`../../templates/design-system.template.md`](../../templates/design-system.template.md))

---

## 1. Full MCP & CLI Integration (`carea mcp-profile`)

Use both **Skills** (`/carea`, `/rea`, `/ca`) AND **MCP profiles** via `carea mcp-profile <preset>` (`--apply <config.json> --yes`):
- **`carea-master`** — Combined dual-server profile: REA (`hot-cold` + raised ASAR/matching/capture limits) + Craft Anything (`--deep --all-tools` unlocking all 322 tools).
- **`rea-master`** / **`rea-all-families`** — Full REA power across all 19 tool families.
- **`ca-deep-full`** / **`ca-deep-private`** / **`ca-clean-room`** — Full 322-tool Deep CA vs lean Clean-Room CA.
- **`two-team-lane-a`** / **`two-team-lane-b`** — Isolated Lane A vs Lane B sessions for Mode 2 Airlock builds.

---

## 2. Opt-In Rebuild & Clean-Room Airlock Modes (When Explicitly Requested)

- **Mode 1 (`/ca` Clean-Room UI Rebuild):** Observable UI rebuild (`craft-anything-cli --clean-room`).
- **Mode 2 (Two-Team Clean Room + Airlock CLI):** 4-directory pipeline (`analyst-evidence/`, `airlock/`, `builder-workspace/`, `verification/`) enforced by `carea init`, `carea isolation-check`, `carea spec-draft`, `carea airlock-lint --strict`, `carea validate-handoff`, human `carea airlock-sign`, Topology B fresh Lane B session, `carea parity-report`, and `carea return-feedback`.
- **Mode 3 (`/rea` Deep Investigation / AgentEnv):** Forensics, `verify_reconstruction`, or `AgentEnv` export only.
- **Mode 4 (`private-deep-rebuild`, `deep_private: true`):** Direct REA Deep + CA `--deep` reconstruction (prints loud **NOT CLEAN-ROOM** banner; airlock checks paths/secrets only).
- **Mode 5 (`game-rebuild`) & Mode 6 (`android-mobile`):** Game engine (`unity`/`unreal`/`godot`/`rust`) & hybrid APK/Flutter + ADB rebuilds in [`references/modes.md`](references/modes.md).

## References

- Auto-intake routing & MCP budget playbook: [`references/intent-router.md`](references/intent-router.md)
- Modes 1–6 & Lane B Topologies A/B: [`references/modes.md`](references/modes.md)
- Templates: [`../../templates/full-breakdown.template.md`](../../templates/full-breakdown.template.md) · [`../../templates/architecture-report.template.md`](../../templates/architecture-report.template.md) · [`../../templates/design-system.template.md`](../../templates/design-system.template.md)
- Shared protocols: [`../_shared/clean-room-protocol.md`](../_shared/clean-room-protocol.md) · [`../_shared/evidence-handoff.md`](../_shared/evidence-handoff.md) · [`../_shared/parity-verification.md`](../_shared/parity-verification.md)
