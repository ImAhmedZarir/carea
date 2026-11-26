# REA Tool Families & Verified Presets (`rea-agents 6.10.1`)

## 1. Verified `TOOL_FAMILY_IDS`

From `rea-agents` `6.10.1` (`src/contracts/toolFamilyIds.ts`):

`direct`, `enhanced`, `native`, `artifact`, `managed`, `firmware`, `uefi`, `android`, `pcap`, `flutter`, `frida`, `apktool`, `jeb`, `adb`, `browser`, `electron`, `javascript-runtime`, `application`, `session`

*(Note: `uefi` was added in `6.10.0`; omit `uefi` if running an older `6.8.x` server.)*

## 2. Preset Family Scopes

Always pair with `REA_MCP_INPUT_SCHEMA_PROFILE=compact` and `REA_MCP_OUTPUT_SCHEMA_PROFILE=off` (or `compact`):

| Target Type | `REA_MCP_TOOL_FAMILIES` | Key Verified Tools |
| --- | --- | --- |
| **Hot/cold dynamic discovery** | `REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` | `binary_session`, `open_binary`, `close_binary`, `get_evidence_bundle`, `discover_tools` *(loads `inspect_analysis_view` & analysis tools on demand)* |
| **Native binary (ELF/PE/Mach-O)** | `native,enhanced,application,session` *(add `direct` or `frida` only when needed)* | `open_binary`, `analyze_function`, `inspect_analysis_view`, `match_native_functions`, `compare_functions`, `build_call_path`, `inspect_binary_hardening`, `inspect_pe_imports`, `inspect_pe_certificates`, `inspect_pe_load_config`, `inspect_pe_resources`, `inspect_native_exports`, `inspect_elf_notes`, `inspect_elf_unwind_ranges`, `inspect_native_initializers`, `inspect_binary_layout`, `inspect_recorded_crash`, `inspect_go_binary`, `inspect_rust_binary` |
| **JS / Web / Electron** | `browser,electron,application,javascript-runtime,session` | `inspect_web_page`, `analyze_javascript_application`, `reconcile_javascript_runtime`, `trace_javascript_semantics`, `inspect_electron_fuses`, `list_electron_targets`, `recover_javascript_sources`, `analyze_web_bundle`, `export_web_scripts`, `trace_web_module_imports`, `build_reconstruction_obligation_ledger`, `verify_reconstruction` |
| **Android / Flutter APK** | `android,apktool,jeb,flutter,frida,adb,application,session` | `inspect_android_package`, `search_android_classes`, `inspect_android_class`, `inspect_android_method`, `inspect_android_jni_bindings`, `decode_android_resources`, `identify_flutter_build`, `inspect_dart_aot`, `inspect_apk_signature`, `project_android_application_graph` |
| **.NET / Managed** | `managed,artifact,application,session` | `inspect_managed_artifact`, `inspect_managed_members`, `inspect_managed_native_boundaries`, `compare_managed_members`, `verify_managed_native_boundaries` |
| **Firmware / UEFI / Packages** | `firmware,uefi,artifact,session,direct` | `inspect_artifact`, `extract_artifact`, `inspect_firmware_regions`, `extract_firmware`, `inspect_uefi_firmware`, `inspect_uefi_nvram`, `extract_uefi_firmware` |
| **Network Captures & AgentEnv** | `browser,artifact,pcap,application,session` | `inspect_web_network_capture`, `inspect_pcap_capture`, `inspect_packet_capture`, `inspect_packet_fields`, `capture_browser_scenario`, `compare_web_captures`, `export_environment_bundle`, `export_evidence_bundle` |
| **Signals & Logic analyzers** | `artifact,session` | `inspect_signal_decoders`, `decode_signal_recording` |
| **Data artifacts** | `artifact,session` | `inspect_sqlite_database`, `inspect_wasm_artifact`, `inspect_evm_interface`, `inspect_model_artifact`, `inspect_il2cpp_metadata`, `inspect_python_pyc`, `inspect_erlang_beam` |
| **Specialized parsers** | `artifact,session` | `inspect_kernel_module`, `inspect_kernel_build_config`, `inspect_apple_ips`, `inspect_gpu_code_objects`, `inspect_windows_shortcut`, `inspect_pe_load_config` |

## 3. Zero-Engine Built-in Parsers (no provider/disassembler needed)

These tools require only REA itself — no IDA, Ghidra, Kuna, Node, or native engine:

| Tool | What it reads |
| --- | --- |
| `inspect_go_binary` | Go compiler/module/build metadata/static strings |
| `inspect_rust_binary` | Rust cargo-auditable dependency metadata |
| `inspect_pe_certificates` | PE Authenticode certificate table |
| `inspect_pe_imports` | PE import + delay-load tables |
| `inspect_pe_load_config` | PE TLS callbacks + load config |
| `inspect_pe_resources` | PE resource tree |
| `inspect_native_exports` | PE/ELF dynamic exports |
| `inspect_binary_hardening` | ELF/PE/Mach-O hardening flags |
| `inspect_elf_notes` | ELF note tables |
| `inspect_elf_unwind_ranges` | ELF `.eh_frame` function ranges |
| `inspect_native_initializers` | ELF/Mach-O pre-main constructors |
| `inspect_binary_layout` | ELF offline layout (pwntools) |
| `inspect_recorded_crash` | Linux ELF core dump |
| `inspect_kernel_module` | Linux kernel module metadata |
| `inspect_kernel_build_config` | Kernel build config (`CONFIG_*`) |
| `inspect_apple_ips` | Apple `.ips` crash report |
| `inspect_python_pyc` | CPython 3.7-3.13 `.pyc` headers |
| `inspect_erlang_beam` | Erlang BEAM IFF container |
| `inspect_il2cpp_metadata` | Unity IL2CPP global-metadata.dat |
| `inspect_model_artifact` | GGUF/safetensors ML model |
| `inspect_windows_shortcut` | Windows `.lnk` shortcut |
| `inspect_wasm_artifact` | WebAssembly (needs WABT) |
| `inspect_evm_interface` | EVM bytecode |
| `inspect_sqlite_database` | SQLite schema + rows (Node >=24.15) |
| `inspect_gpu_code_objects` | CUDA/HIP code objects |

## 4. Evidence Boundaries to Report Explicitly

- `verify_reconstruction` verifies only the declared claims inside its `specification` object; missing or limited observations remain `unknown`.
- `compare_artifacts` and `compare_functions` require matching scope and complete member coverage before reporting equivalence.
- Exported AgentEnv environments replay recorded traffic and declared state handlers within captured bounds.
- `inspect_binary_layout` uses caller-supplied pwntools without opening a disassembler; raw locations and inference/coverage limits apply.
- Zero-engine parsers report observed absence (missing section/table) separately from proof of absence.
