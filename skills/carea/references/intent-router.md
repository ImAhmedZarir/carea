# `carea` Intent Router, Full-Catalog Orchestration & MCP Budget Playbook

Configure automatic target intake for `/carea <target>` running **Stage 1 (`rea`) -> Stage 2 (`craft-anything-cli` study-only) -> Stage 3 (`full-breakdown.md` + `architecture.md` + `design-system.md`)** across every supported artifact type and MCP configuration profile.

## 1. Complete Auto-Intake Target Matrix (Stage 1 -> Stage 2 -> Stage 3)

| Target Input | Auto-Detected Kind | Stage 1: REA (`REA_MCP_TOOL_FAMILIES` & Primary Tools) | Stage 2: CA Study ONLY (NO `rebuild_start`) | Stage 3 Deliverables |
| --- | --- | --- | --- | --- |
| `*.apk`, `*.aab`, Android pkg | Mobile APK / Java / Flutter / JNI | `android,apktool,jeb,flutter,frida,adb,application,session` · `inspect_android_package`, `inspect_apk_signature`, `decode_android_resources`, `search_android_classes`, `inspect_android_method`, `inspect_android_jni_bindings`, `identify_flutter_build`, `inspect_dart_aot`, `project_android_application_graph` | `engines_adb_check`, `adb_devices_find`, `adb_screenshot_take`, `adb_window_show`, `adb_display_show`, `adb_log_read`, `core_report_save` *(or `android_*` if `deep_private`)* | `full-breakdown.md` + `architecture.md` + `design-system.md` |
| `https://...`, SPA, `*.asar`, `.jsc`, JS | Web / PWA / Electron App | `browser,electron,application,javascript-runtime,session` · `analyze_javascript_application`, `inspect_v8_code_cache`, `recover_javascript_sources`, `analyze_web_bundle`, `trace_application_feature`, `inspect_api_contract`, `inspect_web_network_capture` (`allowed_origins`), `inspect_electron_fuses`, `list_electron_targets`, `reconcile_javascript_runtime` | `web_site_open`, `web_site_capture` (375/768/1440px), `web_page_states_capture`, `web_site_close`, `core_brief_write`, `core_report_save` | `full-breakdown.md` + `architecture.md` + `design-system.md` |
| `*.exe`, `*.dll`, `*.sys`, ELF, `.so`, Mach-O, `.dylib`, `.ipa`, `.nupkg` | Native / Go / Rust / .NET / Apple | `native,enhanced,managed,artifact,application,session,frida` · `inspect_byte_entropy`, `open_binary`, `inspect_binary_hardening`, `inspect_go_binary`, `inspect_rust_binary`, `inspect_pe_imports`, `inspect_pe_load_config`, `inspect_pe_certificates`, `inspect_elf_notes`, `inspect_elf_unwind_ranges`, `inspect_native_initializers`, `inspect_managed_artifact`, `inspect_macho`, `analyze_swift_types`, `get_objc_classes`, `analyze_function`, `trace_native_values` | `native_window_capture`, `runtime_ui_read`, `core_finding_record`, `core_report_save` *(skip if CLI/headless)* | `full-breakdown.md` + `architecture.md` *(+ `design-system.md` if GUI)* |
| `*.pak`, `*.pck`, `global-metadata.dat`, Unity/Unreal/Godot | Game Engine Target | `artifact,managed,native,application,session` · `inspect_il2cpp_metadata` (+ `binary_path`), `inspect_managed_artifact`, `inspect_artifact`, `extract_artifact`, `inspect_binary_layout`, `open_binary` | `native_window_capture`, `runtime_walkthrough_record`, `runtime_captures_compare`, `core_finding_record` *(`game_*` requires `--deep`)* | `full-breakdown.md` + `architecture.md` + `design-system.md` |
| `*.bin`, `*.rom`, UEFI, ESP32, `.ko`, `vmlinux`, `.dtb` | Firmware / Kernel / Embedded | `firmware,uefi,artifact,native,session,direct` · `inspect_byte_entropy`, `inspect_firmware_regions`, `extract_firmware`, `inspect_uefi_firmware`, `inspect_uefi_nvram`, `inspect_devicetree`, `inspect_kernel_module`, `inspect_kernel_build_config` | N/A *(Stage 1 REA + Stage 3 Breakdown directly)* | `full-breakdown.md` + `architecture.md` + `ev_...` / `unk_...` |
| `*.wasm`, `.evm`, `.pyc`, `.beam`, `.sqlite`, `.gguf`, `.safetensors` | Bytecode / VM / DB / AI Artifact | `artifact,application,session` · `inspect_wasm_artifact`, `inspect_evm_interface`, `inspect_python_pyc`, `inspect_erlang_beam`, `inspect_sqlite_database`, `inspect_model_artifact` | CA `formats_wasm_module_show`, `formats_evm_interface_show`, `formats_sbpf_*`, `db_sqlite_show` when `--deep` | `full-breakdown.md` + `architecture.md` + `ev_...` |
| `*.pcap`, `*.pcapng`, `*.har`, `*.saz`, `.qlog`, `.sr` (sigrok), `.core`, `.ips` | Network / Crash / Signal Capture | `pcap,browser,artifact,native,session` · `inspect_pcap_capture`, `inspect_packet_fields`, `inspect_packet_capture`, `inspect_web_network_capture` (`format: "saz"`), `inspect_signal_decoders`, `decode_signal_recording`, `inspect_recorded_crash`, `inspect_apple_ips` | `web_recording_show`, `packets_capture_show`, `native_crash_show` when `--deep` | `full-breakdown.md` + protocol/crash appendix |

> **NO-BUILD GUARD (Default `/carea <target>`):** Never invoke `rebuild_start`, `build_file_write`, `build_file_edit`, `build_command_run`, or `project_build_finish` unless the user explicitly opted into rebuilding or Mode 1 / 2 / 4 / 5 / 6 implementation.

## 2. MCP Profile Selection (`carea mcp-profile <preset>`)

| Preset | Engine(s) | Tool Footprint | Best For |
| --- | --- | --- | --- |
| **`carea-master`** | REA (`master`) + CA (`deep-full`) | Dynamic `hot-cold` REA + ALL 322 CA tools (`--deep --all-tools`) | Unrestricted single-session reverse engineering + full engine power |
| **`rea-master`** | REA (`6.10.0+`) | `hot-cold` (5 initial + `discover_tools` -> 237+), 256M ASAR / 1G native / 2G capture limits | Atomic static/dynamic analysis across all 19 families |
| **`rea-all-families`** | REA | Explicit 19-family list (`direct` through `session`) with `compact`/`off` schemas | Older clients needing upfront tool lists without dynamic `discover_tools` |
| **`ca-deep-full`** | Craft Anything | `--deep --all-tools` (all 322 tools / 17 toolsets) | Deep CA triage, game pak inspection, native/Apple/Solana sBPF/Frida/JEB |
| **`ca-clean-room`** | Craft Anything | `--clean-room` (30 focused UI/build tools) | Default Stage 2 observable study & clean-room UI rebuilds |
| **`ca-deep-private`** | Craft Anything | `--deep` | Internal first-party migration (`deep_private: true`) |
| **`ca-restricted-web`** | Craft Anything | `--clean-room --restricted --allow-web --allow-capture` | Shared host browser study with restricted local FS |
| **`two-team-lane-a` / `two-team-lane-b`** | Separated REA / CA Clean-Room | Isolated Lane A (`hot-cold`) vs Lane B (`--clean-room` only) | Mode 2 Two-Team Clean Room builds |

## 3. Opt-In Rebuild Escalation

- **UI clone ("clone / rebuild this UI"):** Delegate to `/ca` (Mode 1 `--clean-room`).
- **Two-Team Airlock rebuild ("two-team clean-room rebuild"):** Run Mode 2 CLI gates (`carea init` -> `carea isolation-check` -> `carea spec-draft` -> `carea airlock-lint --strict` -> `carea validate-handoff` -> `carea airlock-sign` -> Topology B Lane B -> `carea parity-report`).
- **Direct internal port/rebuild ("now build it with full access"):** Run Mode 4 (`private-deep-rebuild`, `deep_private: true` with mandatory non-clean-room banner).
