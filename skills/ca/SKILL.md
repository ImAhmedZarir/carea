---
name: ca
description: >
  Run CA-first 1:1 pro-dev UI forensics, multi-viewport visual/runtime capture, clean-room
  reconstruction (without binary decompilation under --clean-room), or full 322-tool
  deep reverse engineering & game/native/Android inspection (under --deep --all-tools)
  using Craft Anything MCP tools and craft-anything-cli. Triggered by /ca or when
  carea Stage 2 observable study is needed.
argument-hint: "<target_url_or_path> [prompt/goal]"
metadata:
  version: "1.3.0-carea"
---

# Craft Anything (`/ca`) — 1:1 UI Forensics & 322-Tool Full Engine

Coordinate the **entire `craft-anything-cli` (`0.6.x`) engine** across all **17 toolsets / 322 tools** for pixel-exact 1:1 frontend architecture extraction, clean-room UI/game/app reconstruction, or unrestricted `--deep` binary, mobile, and runtime inspection — **zero pre-flight filters, zero vague guesses**.

## 0. Binary Paths & Full-Power MCP Profiles

- **Windows CLI Binary:** `C:\Users\Admin\.gemini\config\plugins\craft-anything\bin\craft-anything-0.6.0-windows-x64-portable\craft-anything-cli.exe`
- **Shortcut (`ca` / `craft-anything`):** `C:\Users\Admin\.gemini\config\node_modules\.bin\ca.cmd` *(or `craft-anything-cli` on `PATH`)*
- **MCP Profiles (`carea mcp-profile <preset>`):**
  - **Clean-Room Observable Study / Rebuild (`ca-clean-room`):** `craft-anything-cli mcp --clean-room` *(default Lean 30+ observable/build tools; blocks internal decompilation)*
  - **Full Unrestricted Power (`ca-deep-full`):** `craft-anything-cli mcp --deep --all-tools` *(exposes ALL 322 tools across all 17 toolsets: `core`, `native`, `apple`, `formats`, `managed`, `android`, `java`, `adb`, `browser`, `javascript`, `runtime`, `frida`, `application`, `database`, `projects`, `setup`, `build`)*
  - **Deep Private (`ca-deep-private`):** `craft-anything-cli mcp --deep`

> **Stage Scope Note (`/carea` vs `/ca`):** When `/ca` is invoked under `/carea <target>` Stage 2 (reverse-engineer-only mode), **stop after capture & `core_report_save`** — do NOT run `rebuild_start` or scaffold code unless the user explicitly asks to build. When `/ca` is invoked standalone to build/clone, run the complete `Study -> Build -> Check -> Refine` loop.

---

## 1. Pro-Dev 1:1 UI Forensics & Design System Extraction

Follow [`references/ui-forensics-playbook.md`](references/ui-forensics-playbook.md) on every web/app/desktop UI target so the extracted `design-system.md` or rebuild is indistinguishable at pixel level:

1. **Multi-Viewport Layout Matrix:** Always capture at **375px** (mobile), **768px** (tablet pivot), and **1440px** (desktop), verifying `320px` overflow safety and `>=44px` touch targets.
2. **State & Theme Matrix:** Capture ALL interactive & data states via `web_page_states_capture` + `web_page_watch`:
   - `default`, `:hover`, `:focus-visible`, `:active`, `[disabled]`
   - `loading` (skeleton dimensions), `empty`, `validation error`, `partial/offline`, `success`
   - Modals / drawers / command menus / popovers (`Dialog` desktop vs `Drawer` mobile swap, `DataTable` vs mobile card stack)
   - Both **dark** and **light** themes (extract exact semantic palette, hairline `1px` borders, L0->L3 elevation shadows, top inner highlights, glass blur).
3. **Token & Geometry Audit:** Extract computed font families (UI sans + `tabular-nums` mono), scale (`clamp` / step ratios), letter-spacing, leading, border radii (`--radius`), grid/container max-widths (`4px`/`8px` rhythm), transition durations, and `cubic-bezier` easing curves.
4. **DOM-to-Handler & Network Wiring:** Correlate rendered controls directly to JS event handlers (`web_listeners_list`, `web_modules_trace`, `web_page_js_analyze`, `js_runtime_code_match`) and live HTTP/WebSocket traffic (`web_site_capture` / `web_recording_show`). Even generate working local mock APIs from captured traffic via `web_standin_build` -> `web_standin_start`.

---

## 2. Verified 17-Toolset / 322-Tool Routing Catalog (`craft-anything-cli 0.6.x`)

Use ONLY exact Craft Anything tool names below (never mix REA tool names when driving `craft-anything` MCP).

### A. Core Investigation & Knowledge (`core` — 36 tools)
- **Clean-room & Deep:** `core_session_show`, `core_targets_list`, `core_target_select`, `core_target_close`, `core_investigation_show`, `core_brief_write`, `core_plan_update`, `core_hypothesis_record`, `core_hypothesis_update`, `core_finding_record`, `core_finding_edit`, `core_evidence_show`, `core_evidence_browse`, `core_evidence_export`, `core_evidence_import`, `core_unknowns_show`, `core_unknown_add`, `core_unknown_edit`, `core_unknown_verify`, `core_handoff_write`, `core_journal_read`, `core_report_save`, `core_report_write`, `core_person_ask`, `core_action_approve`, `assets_image_generate`, `assets_model_generate`, `rebuild_check`
- **Deep (`--deep`):** `core_target_open`, `core_target_triage`, `core_overview_show`, `core_archive_show`, `core_archive_extract`, `core_archives_compare`, `core_feature_find`, `native_function_study`

### B. Web, Browser & Stand-In API Server (`browser` — 22 tools)
- **Clean-room Observable:** `web_site_open`, `web_site_capture`, `web_page_states_capture`, `web_page_screenshot_take`, `web_pixels_compare`, `web_walkthrough_check`, `web_site_close`
- **Deep (`--deep`):** `web_browser_connect`, `web_pages_list`, `web_page_show`, `web_page_js_analyze`, `web_page_watch`, `web_mcp_tools_list`, `web_snapshots_compare`, `web_walkthrough_record`, `web_listeners_list`, `web_modules_trace`, `web_coverage_measure`, `web_standin_build`, `web_standin_start`, `web_standin_stop`, `web_standin_show`

### C. JavaScript & Electron (`javascript` — 11 tools, `--deep`)
`js_app_map`, `js_runtime_code_match`, `web_scripts_save`, `js_source_locate`, `js_sources_restore`, `js_electron_pages_list`, `js_electron_page_show`, `js_electron_walkthrough_record`, `js_runtimes_list`, `js_runtime_watch`, `js_electron_fuses_show`

### D. Native Programs, Disassembly & Annotation (`native` — 55 tools, `--deep`)
- **Inventory & Search:** `native_functions_list`, `native_functions_search`, `native_function_find`, `native_sections_list`, `native_strings_browse`, `native_strings_find`, `native_named_addresses_list`, `native_open_documents_list`, `native_bookmarks_show`, `native_bytes_show`, `native_bytes_find`, `native_data_show`, `native_dos_image_show`
- **Function Dissection & Graphs:** `native_function_show`, `native_function_disassemble`, `native_function_pseudocode`, `native_functions_decompile`, `native_function_instructions_list`, `native_function_address_show`, `native_function_callers_list`, `native_function_callees_list`, `native_function_references_list`, `native_xrefs_list`, `native_name_xrefs_list`, `native_instruction_show`, `native_call_site_resolve`, `native_call_graph_show`, `native_call_path_find`, `native_api_show`, `native_value_flow_show`, `native_address_show`, `native_address_offset_show`, `app_builds_line_up`, `native_source_folder_write`
- **Navigation, Naming & External Disassemblers:** `native_cursor_show`, `native_cursor_address_show`, `native_cursor_function_show`, `native_document_show`, `native_cursor_goto`, `native_cursor_forward`, `native_cursor_back`, `native_name_show`, `native_name_set`, `native_names_set`, `native_function_label`, `native_comment_read`, `native_comment_write`, `native_inline_comment_read`, `native_inline_comment_write`, `native_bookmark_add`, `native_bookmark_remove`, `native_cutter_sessions_list`, `native_cutter_command_run`, `native_objdump_run`, `native_rizin_command_run`

### E. Apple / macOS / iOS (`apple` — 14 tools, `--deep`)
`apple_macho_show`, `apple_slices_list`, `apple_signature_show`, `apple_plist_show`, `apple_objc_classes_list`, `apple_objc_protocols_list`, `apple_swift_types_list`, `apple_swift_symbols_demangle`, `apple_dispatch_show`, `apple_ui_action_trace`, `apple_nib_decode`, `apple_archive_decode`, `apple_assets_list`, `apple_dylibs_resolve`

### F. Specialized Formats, Blockchain, Games, Firmware, AI & Packets (`formats` — 36 tools)
- **WebAssembly / EVM / Solana sBPF:** `formats_wasm_module_show`, `formats_wasm_compare`, `formats_evm_interface_show`, `formats_sbpf_show`, `formats_sbpf_disassemble`
- **Game Engines (`game_*` Deep-only):** `game_archives_list`, `game_pak_list`, `game_pak_extract`, `game_iostore_list`, `game_unity_list`, `game_unity_bundle_list`, `game_unity_asset_export`, `game_unity_code_names_show`, `game_unreal_texture_export`
- **Binaries, Packers, Firmware, AI, Packets, Radio:** `native_go_binary_show`, `native_rust_binary_show`, `native_pe_resources_list`, `native_layout_show`, `native_crash_show`, `native_library_calls_list`, `native_offered_symbols_list`, `native_publisher_show`, `core_packed_files_list`, `core_packed_files_unpack`, `formats_bytecode_show`, `firmware_regions_list`, `firmware_image_extract`, `formats_ai_weights_show`, `app_folder_explain`, `web_recording_show`, `packets_capture_show`, `packets_fields_show`, `packets_inventory_show`, `engines_tshark_check`, `radio_decoders_list`, `radio_recording_decode`

### G. Android, Java, .NET & SQLite (`android` 14 + `java` 6 + `managed` 8 + `database` 1, `--deep`)
- **Android (`jadx`/`apktool`/`jeb`/Flutter):** `android_package_show`, `android_classes_find`, `android_class_show`, `android_method_show`, `android_class_users_find`, `android_resources_read`, `android_components_list`, `engines_apktool_check`, `android_flutter_identify`, `android_dart_snapshot_show`, `engines_jeb_check`, `android_jeb_open`, `android_jeb_units_browse`, `android_jeb_decompile`
- **Java (`vineflower`):** `java_archive_show`, `java_classes_find`, `java_class_show`, `java_method_show`, `java_class_users_find`, `java_vineflower_decompile`
- **.NET (`ilspycmd`):** `managed_assembly_show`, `managed_members_list`, `managed_native_calls_list`, `managed_assemblies_compare`, `managed_native_calls_verify`, `managed_reconstruction_check`, `managed_app_graph_build`, `managed_ilspy_decompile`
- **Database:** `db_sqlite_show`

### H. Live Device, Runtime, Debugger & Frida (`adb` 24 + `runtime` 14 + `frida` 9)
- **ADB (`adb`):** `engines_adb_check`, `adb_devices_find`, `adb_device_show`, `adb_apps_list`, `adb_apps_find`, `adb_app_show`, `adb_display_show`, `adb_window_show`, `adb_screenshot_take`, `adb_log_read`, `adb_running_processes_list`, `adb_folder_list`, `adb_device_features_list`, `adb_system_services_list`, `adb_setting_get`, `adb_app_download`, `adb_file_download`, `adb_file_upload`, `adb_bugreport_save`, `adb_app_install`, `adb_app_remove`, `adb_app_launch`, `adb_activity_open`, `adb_app_force_stop`
- **Runtime UI & Debuggers (`runtime`):** `native_window_capture`, `runtime_ui_read`, `runtime_walkthrough_record`, `runtime_ui_walkthrough_record`, `runtime_captures_compare`, `apple_calls_observe`, `native_gdb_session_begin`, `native_gdb_command_run`, `native_gdb_session_show`, `native_gdb_session_end`, `native_rizin_session_begin`, `native_rizin_session_command_run`, `native_rizin_session_show`, `native_rizin_session_end`
- **Frida Dynamic Hooking (`frida`):** `frida_devices_find`, `frida_targets_list`, `frida_session_begin`, `frida_script_run`, `frida_session_continue`, `frida_script_forget`, `frida_session_show`, `frida_session_end`, `frida_instrument_run`

### I. Comparison, Graph, Build & Setup (`application` 17 + `projects` 29 + `build` 6 + `setup` 20)
- **App Graph & Diff (`application`):** `app_feature_follow`, `js_function_explain`, `app_graphs_compare`, `js_exports_compare`, `app_source_import`, `js_source_bundle_compare`, `app_ledger_build`, `app_coverage_evaluate`, `android_app_graph_build`, `apple_app_graph_build`, `harmony_app_graph_build`, `app_function_versions_compare`, `core_evidence_exports_compare`, `app_changes_summarize`, `app_call_path_find`, `app_runtime_correlate`, `app_rebuild_claim_check`
- **Rebuild & Workspace (`projects` + `build`):** `rebuild_start` (supports `--build-with unity|godot|unreal|rust|web`), `rebuild_status`, `rebuild_activity_show`, `rebuild_note`, `rebuild_note_withdraw`, `rebuild_stop`, `rebuild_question_ask`, `rebuild_questions_list`, `project_*`, `build_files_list`, `build_file_read`, `build_file_write`, `build_file_edit`, `build_checklist`, `build_command_run`
- **Engines & AI (`setup`):** `engines_list`, `engines_install`, `engines_app_open`, `settings_show`, `settings_set`, `ai_models_list`, `ai_model_set`, `assets_key_*`, `plugins_*`, `setup_*`

---

## 3. Standalone Workflows & CLI Commands

### Quick CLI Power Commands
```bash
# Check all 322 tools in Clean-Room vs Deep mode
craft-anything-cli capabilities --json
craft-anything-cli --deep capabilities --json

# Instant target triage (auto-detects format + surfaces internals when --deep)
ca triage <target>
ca triage <target> --deep --json

# Export Markdown or HTML forensic report from .cany project
craft-anything-cli --project ./proj.cany report --html

# Full 4-phase rebuild (Study -> Build -> Check -> Refine)
ca rebuild <target_url_or_file> "Recreate pixel-for-pixel with responsive mobile/desktop UI"
ca rebuild <game_target> --build-with godot --generate-assets "Recreate game mechanics"
ca --deep rebuild <target> "Port with full internal reference"
```

### Done Condition (Standalone Rebuild)
- Multi-width `web_pixels_compare` passes at **375px**, **768px**, **1440px** without horizontal overflow
- `web_walkthrough_check` and `runtime_captures_compare` verify interactive state transitions
- `rebuild_check` passes with all `core_unknowns_show` entries closed or documented
- `core_report_save` / `core_report_write` cites exact `ev_...` IDs

## 4. Reference Playbooks
- Full toolsets & MCP flags: [`references/rebuild-playbook.md`](references/rebuild-playbook.md)
- Pro-dev 1:1 UI/Design System extraction: [`references/ui-forensics-playbook.md`](references/ui-forensics-playbook.md)
