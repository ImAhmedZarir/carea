# `carea` Intent Router & Context-Budget Playbook

This playbook routes tasks to the right upstream engine while preventing the 500+ tool context flood that occurs when full REA and Craft Anything MCP catalogs are exposed together.

---

## 1. Context-Budget Profiles (Start Small)

1. **Craft Anything (`craft-anything-cli mcp`):**
   - **Never** pass `--all-tools` unless explicitly doing Deep-mode desktop/workbench inspection. Without `--all-tools`, Craft Anything exposes only `core` (Essentials) plus enabled toolsets.
   - Pass `--clean-room` for Builder Lane runs so internal inspection tools remain refused (`available: false`).
   - Use CLI subcommands (`craft-anything-cli capabilities`, `rebuild`, `report`, `doctor`) for single-shot operations outside persistent MCP sessions.
2. **REA (`rea`):**
   - Prefer `REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` (REA `>= 6.10.x`: advertises 5 core tools initially and loads tools on demand via `discover_tools`) **or** scope `REA_MCP_TOOL_FAMILIES` to the workflow's domain families + `session` + `application`.
   - Always use `REA_MCP_INPUT_SCHEMA_PROFILE=compact` and `REA_MCP_OUTPUT_SCHEMA_PROFILE=off` (or `compact`). Remember: `rea >= 6.10.0` rejects `full` schema profiles at startup.
   - Always prefer `detail: "summary"` plus `inspect_analysis_view` when inspecting large binaries, JS graphs, ELF layouts, IL2CPP, Rust/Go, or artifact inventories.
   - For one-off static checks on uncommon formats (`.pyc`, `.beam`, `.nupkg`, SQLite, UEFI, etc.), invoke the REA CLI directly (`rea <command> --json`) instead of widening the MCP server's loaded families.

---

## 2. Ownership Rules for Overlapping Capabilities

Both engines cover areas such as Ghidra, JADX, Apktool, adb, Frida, browser capture, and evidence ledgers. To avoid duplicate tool schemas and conflicting sessions:

| Shared Domain | Default Owner in `carea` | Why |
|---|---|---|
| **Deep static decompilation & CFG** | **REA** | Supports multiple native backends (Hopper, Ghidra `12.2`, IDA Pro, Kuna `1.1000`, Rizin, Cutter, objdump) and retained dossier paging. |
| **Live runtime tracing & debugging** | **REA** | Dedicated Frida, GDB/pwndbg, Rizin debug, LLDB call observation, PTY process scenarios, and static/runtime correlation. |
| **JavaScript / Electron forensics** | **REA** | Semantic tracing, route/IPC recovery, source-to-bundle checks, and `recover_javascript_sources`. |
| **Observable website capture & visual pixel diff** | **CA** | Multi-width capture (`web_site_capture`, `web_page_states_capture`), `web_pixels_compare`, `web_walkthrough_check`, and `rebuild_check`. |
| **Rebuild workspace, pins, previews & asset gen** | **CA** | `rebuild_start`, `project_preview`, `project_pin_create`, `project_pin_open`, `project_pin_stop`, `build_files_list`, `build_file_write`, `build_file_edit`, `build_command_run`, `assets_image_generate`, `assets_model_generate`. |
| **Evidence & Unknown ledgers** | **Both (lane-scoped)** | REA owns `ev_...` and `unknown` records in Analyst/Verification lanes; CA owns `core_evidence_*`, `core_unknown_*`, and `core_finding_*` in Clean-Room Builder lane, bridged by `carea-handoff.json`. |

---

## 3. Phase-Based Routing Table

| Task Type | Engine | Verified Tool Group / Family / CLI | Mode / Notes |
|---|---|---|---|
| **Observable Website / UI Study & Rebuild** | **CA** | Toolsets `browser`, `projects`, `build` (`web_site_open`, `web_site_capture`, `web_page_states_capture`, `web_page_screenshot_take`, `rebuild_start`, `build_files_list`, `build_file_write`, `build_file_edit`, `build_command_run`, or CLI `craft-anything-cli rebuild <url>`) | Clean-Room default (`--clean-room`). Reads zero HTML/JS source. |
| **Visual & Responsive Pixel Parity** | **CA** | Toolsets `browser`, `core`, `runtime` (`web_pixels_compare`, `web_walkthrough_check`, `rebuild_check`, `native_window_capture`, `runtime_captures_compare`) | Clean-Room. Compares screenshots, walkthroughs, and layout metrics. |
| **Original Replacement Images & 3D Assets** | **CA** | Toolsets `core`, `setup` (`assets_image_generate`, `assets_model_generate`, `assets_key_status`, `project_assets_budget`, `project_assets_allow`) | Clean-Room safe replacement assets (requires user's `fal.ai` key). |
| **Deep Native Decompilation & Value Tracing** | **REA** | Families `native`, `enhanced`, `session`, `application` (`open_binary`, `binary_overview`, `analyze_function`, `procedure_pseudo_code`, `procedure_assembly`, `get_call_graph`, `trace_feature`, `trace_call_path`, `trace_native_values`, `batch_decompile`, `decompile_all`, `close_binary`) | Analyst / Deep Lane. Add `direct` only when needed. |
| **Live Instrumentation & Process Capture** | **REA** | Families `frida`, `native`, `javascript-runtime`, `session` (`list_frida_devices`, `start_frida_session`, `load_frida_script`, `instrument_with_frida`, `start_gdb_session`, `start_rizin_debug_session`, `capture_process_scenario`, `observe_native_calls`) | Analyst / Deep Lane. Executes or attaches to targets; explicit authorization required. |
| **Electron / JS Bundle Forensics** | **REA** | Families `browser`, `electron`, `application`, `javascript-runtime`, `session` (`analyze_javascript_application`, `list_electron_targets`, `inspect_electron_fuses`, `trace_application_feature`, `trace_javascript_semantics`, `recover_javascript_sources`) | Analyst / Deep Lane. CLI fallback: `rea analyze-javascript-application <path> --json`. |
| **Specialized Static Formats (No Disassembler)** | **REA** | Families `artifact`, `managed`, `firmware`, `uefi`, `session` (`inspect_go_binary`, `inspect_rust_binary`, `inspect_il2cpp_metadata`, `inspect_model_artifact`, `inspect_gpu_code_objects`, `inspect_evm_interface`, `inspect_wasm_artifact`, `inspect_python_pyc`, `inspect_erlang_beam`, `inspect_sqlite_database`, `inspect_pe_imports`, `inspect_pe_certificates`, `inspect_pe_load_config`, `inspect_elf_notes`, `inspect_apple_ips`, `inspect_kernel_module`, `inspect_managed_artifact`, `inspect_nuget_nupkg`, `inspect_maven_gradle_metadata`, `audit_release_exposure`, `inspect_firmware_regions`, `inspect_uefi_firmware`, `extract_uefi_firmware`, `inspect_uefi_nvram`) | Analyst / Deep Lane. Omit `uefi` on `rea 6.8.x`. Prefer one-shot CLI for single files. |
| **Android APK, Flutter & Device Inspection** | **REA** *(code)* / **CA** *(UI)* | REA families `android`, `apktool`, `jeb`, `flutter`, `adb`, `session` (`inspect_android_package`, `inspect_android_jni_bindings`, `inspect_apk_signature`, `decode_android_resources`, `identify_flutter_build`, `inspect_dart_aot`, `open_jeb_project`, `list_adb_devices`, `pull_adb_package`) · CA `adb` (`adb_screenshot_take`, `adb_display_show`) | REA handles DEX/JADX/JEB/JNI/Flutter analysis; CA handles clean visual UI observation. |
| **Saved Network, PCAP & Signal Captures** | **REA** | Families `browser`, `artifact`, `pcap`, `session` (`inspect_web_network_capture` for HAR/SAZ/mitmproxy/qlog, `inspect_pcap_capture`, `inspect_packet_capture`, `decode_signal_recording`, `inspect_playwright_trace`) | Read-only over saved captures. |
| **Behavioral / Structural Parity & Ledgers** | **REA** | Families `application`, `enhanced`, `managed`, `session` (`build_reconstruction_obligation_ledger`, `evaluate_reconstruction_coverage`, `verify_reconstruction`, `compare_source_to_bundle`, `compare_application_versions`, `compare_javascript_export_shapes`, `compare_functions`, `match_native_functions`, `compare_artifacts`, `compare_process_captures`, `correlate_static_and_runtime`) | Verification Gate. Maps `ev_...` evidence to explicit pass/partial/unknown claims. |
| **AgentEnv / RL Environment Export** | **REA** | Families `application`, `browser` (`capture_browser_scenario`, `inspect_analysis_view` with `api-surface` / `environment-manifest` / `environment-state` / `environment-coverage`, `export_environment_bundle`, CLI `rea environment-build`) | Optional RL/eval export (`agentenv` + Docker needed to run exported bundles). |
| **Desktop App / Game UI Rebuild Loop** | **CA** | Toolsets `runtime`, `projects`, `build`, `core` (`native_window_capture`, `runtime_ui_read`, `runtime_walkthrough_record`, `runtime_captures_compare`, `rebuild_start`, `rebuild_check`, `project_play`) | Builder Lane. Note: CA's `game_*` asset extraction tools are Deep-only and blocked in Clean Room. |
