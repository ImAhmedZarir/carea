---
name: rea
description: >
  Run REA-first deep reverse engineering via REA MCP tools and CLI to dissect
  native binaries, JS/Electron/V8 bundles, .NET/Java/Android/Flutter/Apple packages,
  UEFI/firmware, PCAP/signals, SQLite/WASM/EVM, and live runtimes at atomic
  instruction, data-flow, and memory level — without unverified heuristics or demo
  shortcuts. Full 230+ tool catalog coverage across all 19 tool families. Triggered
  by /rea or when carea Stage 1 internal reverse engineering is needed.
argument-hint: "<target> [goal/options]"
metadata:
  version: "1.3.0-carea"
---

# REA — Full-Power Atomic Reverse Engineering (`/rea`)

Execute exhaustive, evidence-backed static and runtime reverse engineering across every supported binary, package, runtime, capture, and protocol format using the complete `rea` MCP tool catalog and `rea` CLI — **zero pre-flight filters, zero watered-down heuristics, zero guesswork**.

## 0. Connect & Activate Full Tool Surface (MCP + CLI)

1. **Recommended Full-Power MCP Profile (`carea mcp-profile rea-master`):**
   - `REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` (initial 5 core tools + on-demand `discover_tools` across all 19 tool families without bloating schemas)
   - `REA_MCP_INPUT_SCHEMA_PROFILE=compact` and `REA_MCP_OUTPUT_SCHEMA_PROFILE=off` *(required on REA `>=6.10.0`; `full` is rejected)*
   - High-ceiling limits: `REA_ASAR_MAX_HEADER_BYTES=268435456` (256 MiB), `REA_NATIVE_MATCHING_REPRESENTATION_BYTES=1073741824` (1 GiB), `REA_CAPTURE_DECODER_OLD_GENERATION_MIB=2048` (2 GiB)
   - Or explicit full-family profile (`carea mcp-profile rea-all-families`) loading `direct,enhanced,native,artifact,managed,firmware,uefi,android,pcap,flutter,frida,apktool,jeb,adb,browser,electron,javascript-runtime,application,session`.
2. **Dynamic Tool Discovery (`>=6.10.0`):** Call `binary_session` (`{}` for availability summary; `{"detail": "complete"}` for diagnostics/paths) and `discover_tools` to unlock any needed family cleanly inside your session.
3. **Zero-MCP CLI Fallback (if MCP server is disconnected):**
   - `rea <command> <target> --json` or `npx -y rea-agents@latest analyze-javascript-application /abs/path/to/app --json`
   - Inspection flags: `--detail summary --evidence_output /abs/path/bundle.json`
   - Complete runtime config & engine health: `rea doctor --json`

---

## 1. 5-Layer Atomic Reverse-Engineering Protocol

Work top-to-bottom until every control path, struct layout, dispatch table, state machine, crypto routine, and network/IPC schema is pinned to exact offsets, addresses, and `ev_...` IDs:

### Layer 0 — Entropy, Container Peeling & Signature Verification
- **Compression / Packing / Encryption Check:** Call `inspect_byte_entropy` immediately on unknown binaries or firmware slices to isolate high-entropy packed/encrypted sections (>7.2 bits/byte) vs code/rodata vs padding.
- **Archive & Installer Peeling:** `open_binary` -> `inspect_artifact` (extract with `extract_artifact`) for ZIP, APK, IPA, MSIX, AppX, DMG, **PyInstaller CArchive** (application layer vs native bootloader), **Bun `--compile`** (embedded module graph), **Deno `deno compile`** (embedded virtual FS), **Android/iOS/Desktop installs** (`inspect_desktop_application`).
- **Firmware & Device Trees:** `inspect_firmware_regions` -> `extract_firmware` (Binwalk/Unblob), `inspect_uefi_firmware` / `inspect_uefi_nvram` / `extract_uefi_firmware`, `inspect_devicetree`, ESP32 (`0xE9` magic via `inspect_artifact`).
- **Signatures & Mitigations:** `inspect_binary_hardening` (ASLR/PIE, NX, RELRO, canary, fortify, CFG/XFG), `inspect_pe_certificates`, `inspect_apk_signature` (v1 JAR, v2, v3, v3.1 key-rotation + digest match), `inspect_signature` (Mach-O code signing & hardened runtime), `inspect_electron_fuses`.

### Layer 1 — Zero-Engine Format & Compiler Dissection (Instant, No Disassembler Required)
Run built-in binary/artifact parsers first to extract compiler provenance, symbol tables, dependencies, and hidden entrypoints:
- **PE Internals:** `inspect_pe_imports` (DLL/API/ordinal/ILT/IAT RVAs + imphash), `inspect_pe_load_config` (**TLS callbacks executing before `main`**, security cookie, SafeSEH, CFG, XFG, EH-continuation), `inspect_pe_resources`, `inspect_native_exports`, `inspect_windows_shortcut` (`.lnk` FILETIMEs, IDList, Tracker droid).
- **ELF / Mach-O Internals:** `inspect_elf_notes` (GNU build-id, ABI-tag), `inspect_elf_unwind_ranges` (`.eh_frame` FDE bounds surviving `strip`, LSDA, personality), `inspect_native_initializers` (`DT_PREINIT_ARRAY`, `DT_INIT`, `DT_INIT_ARRAY`, `DT_FINI*`, `.ctors`/`.dtors`, `__mod_init_func`, `__init_offsets`), `inspect_native_exports`, `inspect_binary_layout` (pwntools symbols/relocs/segments without loading a DB), `inspect_native_load_image`.
- **Language & Engine Metadata:**
  - **Go:** `inspect_go_binary` (`include_string_literals: true` recovers packed `(ptr, len)` non-NUL UTF-8 slices + compiler/module build settings).
  - **Rust:** `inspect_rust_binary` (`.dep-v0` / `__DATA,.dep-v0` cargo-auditable dependency graph + `/rustc/<40-hex>/` commit inference).
  - **Unity IL2CPP:** `inspect_il2cpp_metadata` (v24/27/29/31/39 types, methods, fields, properties, events, `method_indices` parameters, string literals; optional `binary_path` links to `GameAssembly`/`UnityFramework` RVAs).
  - **V8 / Node / Bytenode:** `inspect_v8_code_cache` (`.jsc` cached script metadata).
  - **Python / Erlang / WASM / EVM / AI / SQLite:** `inspect_python_pyc` (CPython 3.7–3.13 marshal + bytecode hashes), `inspect_erlang_beam` (atoms, exports, imports, lambdas, Code chunk), `inspect_wasm_artifact` (WABT WAT + imports/exports), `inspect_evm_interface` (function selectors & mutability), `inspect_model_artifact` (GGUF v2/v3 & safetensors tensors/metadata; `hash: "full"`), `inspect_sqlite_database` (`schema_scope: "database"` + WAL state + row sampling).
  - **Crashes / Kernels / GPU:** `inspect_recorded_crash` (Linux x86-64 ELF core threads & registers), `inspect_apple_ips` (`bug_type` `"309"` lossless registers & `usedImages` UUIDs), `inspect_kernel_module` (`.modinfo`, `__versions` CRCs, PKCS#7 trailer), `inspect_kernel_build_config` (`CONFIG_*` options), `inspect_gpu_code_objects` (CUDA/HIP code objects), `.NET` `inspect_managed_artifact` + `inspect_nuget_nupkg`, JVM `inspect_maven_gradle_metadata`.

### Layer 2 — Deep Disassembly, Decompilation, Data-Flow & Annotation
Open with `open_binary` (Ghidra, IDA `provider_id: "ida"`, Kuna `provider_id: "kuna"`, Rizin, Cutter, objdump) and trace to instruction/register level:
- **Program Map:** `binary_overview`, `list_segments`, `list_procedures`, `list_names`, `list_strings`, `list_documents`, `search_procedures`, `search_strings`, `search_bytes`, `read_bytes`, `address_to_file_offset`.
- **Procedure Dissection & Graph:** `procedure_info`, `procedure_address`, `procedure_pseudo_code`, `procedure_assembly`, `read_function_instructions`, `inspect_native_instruction`, `inspect_native_data_type`, `inspect_native_dispatch_metadata` (vtables/jump tables/callbacks), `inspect_native_api`, `resolve_native_call_targets`, `resolve_containing_procedure`, `analyze_function` (summary-first -> `parent_evidence_id`), `batch_decompile`, `decompile_all`.
- **Cross-References & Call Paths:** `xrefs`, `find_xrefs_to_name`, `procedure_callers`, `procedure_callees`, `procedure_references`, `get_call_graph`, `build_call_path`, `trace_call_path`, `trace_feature`, `trace_native_values` (static taint/data-flow slice).
- **Cursor, Navigation & Semantic Recovery:** `current_address`, `current_procedure`, `current_document`, `goto_address`, `next_address`, `prev_address`, `get_navigation_context`, `inspect_address_context`, `address_name`, `comment`, `inline_comment`, `list_bookmarks`.
- **Rename & Annotate Live DB:** `set_address_name`, `set_addresses_names`, `set_comment`, `set_inline_comment`, `set_bookmark`, `unset_bookmark`, `annotate_native_function` *(checkpoint editable Ghidra Program when persistence across processes is required)*.
- **Direct Low-Level Engines:** `inspect_with_objdump`, `execute_rizin_command`, `list_cutter_sessions`, `cutter_command`.
- **Apple / Swift / ObjC:** `open_bundle_resources` (or `open_binary`), `inspect_macho`, `list_architectures`, `inspect_plist`, `get_objc_classes`, `get_objc_protocols`, `analyze_swift_types`, `demangle_swift`, `decode_interface_builder`, `inspect_keyed_archive`, `inspect_asset_catalog`, `trace_dylib_resolution`, `project_apple_application_graph`, `project_harmony_application_graph`.
- **Managed (.NET) & Android (JADX / JEB / Apktool / Flutter):**
  - `.NET`: `inspect_managed_artifact` -> `inspect_managed_members` -> `inspect_managed_native_boundaries` (P/Invoke/reverse-P/Invoke) -> `project_managed_application_graph` -> `import_managed_reconstruction`.
  - Android: `inspect_android_package` -> `decode_android_resources` (`inspect_apktool_client`) -> `search_android_classes` -> `inspect_android_class` -> `inspect_android_method` (pass R8/ProGuard `mapping_path` when available) -> `trace_android_references` -> `inspect_android_jni_bindings` (links DEX native decls to `.so` ELF slots) -> `project_android_application_graph`.
  - JEB & Flutter: `inspect_jeb_client` -> `open_jeb_project` -> `list_jeb_units` -> `decompile_jeb_item`; `identify_flutter_build` -> `inspect_dart_aot`.

### Layer 3 — Live Runtime Hooking, Debugging, Network & Signal Forensics
Use when static analysis meets runtime packing, dynamic dispatch, encrypted payloads, or state machines:
- **Frida Dynamic Instrumentation (`frida`):** `list_frida_devices` / `list_frida_processes` -> `start_frida_session` (attach PID or paused spawn) -> `load_frida_script` -> `resume_frida_session` -> `instrument_with_frida` -> `frida_session_status` -> `unload_frida_script` -> `close_frida_session`.
- **GDB & Rizin Debuggers:** `start_gdb_session` -> `gdb_console` -> `gdb_session_status` -> `close_gdb_session`; `start_rizin_debug_session` -> `rizin_debug_command` -> `rizin_debug_session_status` -> `close_rizin_debug_session`. *(Close active Ghidra session before interactive debugger runs that alter memory/files, then reopen after.)*
- **Process PTY & macOS Live Observation:** `prepare_bounded_process_capture` -> `capture_process_scenario` -> `compare_process_captures`; macOS LLDB/UI: `observe_native_calls`, `observe_native_ui`, `capture_native_ui_scenario`, `trace_native_ui_action`.
- **Live Android Device (`adb`):** `inspect_adb_client` -> `list_adb_devices` -> `inspect_adb_device` -> `list_adb_packages` / `resolve_adb_packages` -> `pull_adb_package` / `pull_adb_file` / `push_adb_file` -> `inspect_adb_package` -> `start_adb_app` / `start_adb_activity` / `stop_adb_app` -> `read_adb_logcat` -> `capture_adb_screen` -> `inspect_adb_display` / `inspect_adb_window` -> `read_adb_setting` -> `list_adb_processes` / `list_adb_directory` / `list_adb_features` / `list_adb_services` -> `install_adb_package` / `uninstall_adb_package` -> `collect_adb_bugreport`.
- **Web / Browser / Electron Live Runtime:** `inspect_electron_fuses` -> `list_electron_targets` -> `inspect_electron_page` / `capture_electron_scenario`; `list_browser_targets` -> `inspect_web_page` / `observe_web_session` / `capture_browser_scenario` -> `capture_web_screenshot` -> `observe_web_execution` -> `inspect_web_event_listeners` -> `discover_webmcp_tools`; `list_javascript_runtime_targets` -> `observe_javascript_runtime` -> `reconcile_javascript_runtime`.
- **Network Captures & Signal Decoding:**
  - Web captures (HAR / Fiddler `.saz` / mitmproxy / aioquic qlog): `inspect_web_network_capture` (`format: "saz"` for Fiddler).
  - **SPA Cross-Origin API Capture Rule:** Default scope captures only page origin. Extract external API origins from loaded JS bundles first, then pass ALL origins in `allowed_origins` (`[page_origin, api_origin_1, ...]`) and inspect `completeness.excluded`.
  - Packet captures (TShark 4.x): `inspect_packet_fields` -> `inspect_packet_capture` (`match_offset`/`match_limit` or `null`); DNS/SNI/protocol summaries: `inspect_pcap_client` -> `inspect_pcap_capture`.
  - Logic/RF Signal Recordings (sigrok-cli): `inspect_signal_decoders` -> `decode_signal_recording` (`line_offset`/`line_limit`).

### Layer 4 — Web / JavaScript Bundle Deobfuscation & API Contract Recovery
- `analyze_javascript_application` (`detail: "summary"` for large trees/ASARs; select exact `source_paths` when targeted; request `view: {kind: "javascript-routes", collection: "routes"}` for route inventories).
- `recover_javascript_sources` (Wakaru deobfuscation/unbundling; pass related lazy/runtime chunks in `additional_paths`).
- `analyze_web_bundle` (`view: {kind: "web-bundle", collection: "endpoints"}`), `export_web_scripts`, `trace_web_module_imports`, `trace_web_source_location`, `trace_application_feature`, `trace_javascript_semantics`, `inspect_api_contract`, `compare_static_and_observed_endpoints`.

### Layer 5 — Cross-Build Diffing, Formal Parity Verification & AgentEnv
- **Cross-Version / Diffing:** `match_native_functions` (`left_observations`/`right_observations` via `retained-evidence` refs), `compare_functions`, `find_changed_behavior`, `compare_artifacts`, `compare_bundles`, `compare_application_versions`, `compare_source_to_bundle`, `compare_javascript_export_shapes`, `compare_managed_members`, `verify_managed_native_boundaries`, `compare_wasm_interfaces`, `compare_web_captures`, `compare_web_screenshots`, `correlate_static_and_runtime`.
- **Reconstruction Verification:** `build_reconstruction_obligation_ledger` -> `evaluate_reconstruction_coverage` -> `verify_reconstruction` -> `audit_residual_unknowns`.
- **Unknowns & Evidence Lifecycle:** `record_unknown` -> `list_unknowns` -> `update_unknown` -> `verify_unknown_resolution`; `get_evidence_bundle` (`detail: "summary"` with filters) -> `export_evidence_bundle` / `import_evidence_bundle`.
- **AgentEnv Bundle Export:** Record replayable app state/writes via `capture_browser_scenario` -> verify coverage -> `export_environment_bundle`.

---

## 2. Provider Rules & Operational Guardrails

- **IDA Pro (`provider_id: "ida"`):** Pass the **original input binary** to `open_binary` — NEVER pass an `.idb` or `.i64` database. IDA does NOT supply `binary_overview`; proceed directly to `analyze_function`, `procedure_pseudo_code`, or search tools.
- **Kuna (`REA_KUNA_COMMAND`, `provider_id: "kuna"`):** Search the cached `.c`/`.asm` file spans in `raw_result.source` directly rather than making redundant per-function RPC calls.
- **Ghidra:** Raise `ghidra.startup_timeout_ms` via `update_analysis_settings` before retrying cold imports on huge native binaries; use owned Program checkpoints when edits must persist across processes.
- **Summary-First & Transport Recovery:** Always pass `detail: "summary"` on unknown-size JS trees, layouts, artifacts, or `batch_decompile`. Use `inspect_analysis_view` with `parent_evidence_id` to page `modules`, `items`, `pseudocode`, `endpoints`, `routes`, `go`, `il2cpp`, `model-artifact`, `native-inventory`, `pcap`, `apk-signature`, `browser-scenario`. On `resource_constraint` (`details.resource: "transport"`), page the retained parent ID via `inspect_analysis_view` — never repeat the producer blindly.
- **Parallel Decomposition:** Split independent subsystems (e.g., native `.so` crypto vs DEX Java UI logic vs network endpoints) across parallel workers sharing retained `ev_...` IDs.
- **Evidence Rigor:** Separate `[OBSERVED ev_...]` from `[INFERRED]` and `[UNKNOWN unk_...]`. Never report static code inspection as runtime proof.

---

## 3. Reference Playbooks (`skills/rea/references/`)

- Native, managed, archives, zero-engine parsers, Ghidra/IDA/Kuna: [`references/native-and-artifacts.md`](references/native-and-artifacts.md)
- Tool families & preset scopes: [`references/tool-families.md`](references/tool-families.md)
- JS, Electron, ASAR, Wakaru recovery, V8 cache, routes: [`references/javascript-applications.md`](references/javascript-applications.md)
- Android APKs, DEX, R8 mapping, JNI, JEB, Flutter/Dart: [`references/android-applications.md`](references/android-applications.md)
- Frida, GDB, Rizin, PTY capture, Browser/Electron CDP, PCAP, Sigrok: [`references/runtime-observation.md`](references/runtime-observation.md)
- Evidence paging, retained refs, diffing & verification: [`references/evidence-workflows.md`](references/evidence-workflows.md)
- AgentEnv recording & desktop build environments: [`references/environments.md`](references/environments.md)
- MCP connection, hot-cold discovery, deadline recovery & CLI fallback: [`references/connection-and-recovery.md`](references/connection-and-recovery.md)

## 4. Clean Teardown

Close active binary/debugger/Frida sessions (`close_binary`, `close_frida_session`, `close_gdb_session`, `close_rizin_debug_session`), checkpoint state with `reset_investigation` (`save_path` if resuming later), and export final Evidence via `export_evidence_bundle`.
