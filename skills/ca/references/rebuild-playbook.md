# Craft Anything 17-Toolset & Mode Playbook (`0.6.x` — 322 Tools)

Verified against `craft-anything-cli 0.6.0` (`322` tools / CLI subcommands across `17` toolsets) and upstream `v0.6.1`.

## 1. MCP Startup Profiles (`carea mcp-profile`)

| Preset | Command | Tools Exposed | Mode |
| --- | --- | --- | --- |
| **`ca-clean-room`** | `craft-anything-cli mcp --clean-room` | ~90 observable UI, runtime, capture, `adb`, `projects`, `setup`, `build` tools | Clean-Room (default) |
| **`ca-restricted-web`** | `craft-anything-cli mcp --clean-room --restricted --allow-web --allow-capture` | Restricted browser/capture subset | Clean-Room on shared hosts |
| **`ca-deep-private`** | `craft-anything-cli mcp --deep` | Standard Deep surface (`core_target_open`, archives, web deep) | Deep Mode |
| **`ca-deep-full`** | `craft-anything-cli mcp --deep --all-tools` | **ALL 322 tools across ALL 17 toolsets** (`native_*`, `formats`/`game_*`, `frida_*`, `android_*`, `managed_*`, `java_*`, `database`, `javascript`, `apple`, `application`, etc.) | Unrestricted Full Power |

## 2. Clean-Room Available vs Deep-Only Toolset Breakdown (`0.6.0`)

| Toolset | Count | Clean-Room (`--clean-room`) | Deep (`--deep --all-tools`) Key Additions |
| --- | --- | --- | --- |
| **`core`** | 36 | 28 (`core_session_show`, `core_brief_write`, `core_finding_record`, `core_report_save`, `assets_*`, `rebuild_check`) | +8: `core_target_open`, `core_target_triage`, `core_overview_show`, `core_archive_show`, `core_archive_extract`, `core_archives_compare`, `core_feature_find`, `native_function_study` |
| **`native`** | 55 | 0 | All 55 disassembly, pseudocode, xref, call-graph, value-flow, cursor, naming, Cutter, Rizin, objdump tools |
| **`apple`** | 14 | 0 | All 14 `apple_macho_show`, `apple_objc_*`, `apple_swift_*`, `apple_nib_decode`, `apple_assets_list`, `apple_dylibs_resolve` |
| **`formats`** | 36 | 1 (`engines_tshark_check`) | +35: `formats_sbpf_*` (Solana eBPF), `formats_wasm_*`, `formats_evm_interface_show`, `game_*` (9 tools: Unity/Unreal/Pak), `native_go/rust_binary_show`, `formats_ai_weights_show`, `firmware_*`, `packets_*`, `radio_*` |
| **`managed`** | 8 | 0 | All 8 `.NET` inspection + `managed_ilspy_decompile` |
| **`android`** | 14 | 2 (`engines_apktool_check`, `engines_jeb_check`) | +12: `android_package_show`, `android_classes_find`, `android_method_show`, `android_resources_read`, `android_flutter_identify`, `android_dart_snapshot_show`, `android_jeb_*` |
| **`java`** | 6 | 0 | All 6 `java_archive_show`, `java_classes_find`, `java_method_show`, `java_vineflower_decompile` |
| **`adb`** | 24 | Observable phone UI (`engines_adb_check` + `adb_*` when ADB active) | Full device pull/push/install/logcat/bugreport/shell inspection |
| **`browser`** | 22 | 7 observable (`web_site_open/capture/close`, `web_page_states_capture`, `web_page_screenshot_take`, `web_pixels_compare`, `web_walkthrough_check`) | +15: `web_browser_connect`, `web_page_js_analyze`, `web_page_watch`, `web_listeners_list`, `web_modules_trace`, `web_coverage_measure`, `web_standin_build/start/stop/show`, `web_snapshots_compare` |
| **`javascript`** | 11 | 0 | All 11: `js_app_map`, `js_runtime_code_match`, `js_source_locate`, `js_sources_restore`, `web_scripts_save`, `js_electron_*` |
| **`runtime`** | 14 | 5 observable (`native_window_capture`, `runtime_ui_read`, `runtime_walkthrough_record`, `runtime_ui_walkthrough_record`, `runtime_captures_compare`) | +9: `native_gdb_session_*`, `native_rizin_session_*`, `apple_calls_observe` |
| **`frida`** | 9 | 0 | All 9: `frida_devices_find`, `frida_targets_list`, `frida_session_*`, `frida_script_*`, `frida_instrument_run` |
| **`application`** | 17 | 0 | All 17: `app_feature_follow`, `app_graphs_compare`, `js_source_bundle_compare`, `app_ledger_build`, `app_rebuild_claim_check`, mobile/Apple/Harmony graph builders |
| **`database`** | 1 | 0 | `db_sqlite_show` |
| **`projects`** | 29 | 28 (`project_*`, `rebuild_start`, `rebuild_status`, `project_build_finish`, etc.) | +`project_plan_fold` |
| **`setup`** | 20 | All 20 (`engines_list/install`, `ai_models_*`, `assets_key_*`, `settings_*`, `plugins_*`) | Same |
| **`build`** | 6 | All 6 (`build_files_list/read/write/edit`, `build_checklist`, `build_command_run`) | Same |

## 3. Standalone CLI Flags Worth Knowing

- `ca --deep ...` vs `ca --clean-room ...` overrides Settings per invocation.
- `ca --allow-run ...` allows tools that execute targets or connect to devices without interactive prompt stalling.
- `ca --project ./my.cany ...` persists findings, journal, and Evidence across CLI invocations.
- `ca rebuild <target> "<goal>" --build-with <web|unity|unreal|godot|rust> --rounds <N> --project-folder <dir> --generate-assets` drives autonomous multi-round builds.
- `ca --project ./my.cany report --html` exports a standalone shareable forensic HTML report.
