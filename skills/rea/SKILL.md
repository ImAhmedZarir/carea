---
name: rea
description: >
  Run REA-first deep reverse engineering via REA MCP tools to analyze native binaries,
  JS/Electron bundles, .NET/Java/Android/Flutter packages, UEFI/firmware, or
  PCAP/SQLite artifacts — without binary decompilation shortcuts. Full 230+ tool catalog
  coverage. Triggered by /rea or when carea Stage 1 reverse engineering is needed.
argument-hint: "<target> [goal/options]"
metadata:
  version: "1.2.0-carea"
---

# REA — Full-Power Reverse Engineering

This is the carea-bundled REA instruction layer. It routes to ALL available REA MCP
tools with no capability filtering and no pre-flight gatekeeping. Work like a
professional security researcher and binary analyst: atomic-level static inspection,
runtime observation, full provider support, pixel-perfect analysis.

## Connect and start

REA tools arrive through the `rea` MCP server registered in the host client. No
diagnostics before every job. If tools are absent, use the CLI fallback:

```bash
npx -y rea-agents@latest analyze-javascript-application /absolute/path/to/app --json
```

or for native targets:
```bash
npx -y rea-agents@latest mcp   # then call tools via stdio
```

---

## Route the target — full tool map

Pick the first tool from this complete routing table. No tool is off-limits.

### Archive / Package entry points
| Target type | First tool |
|---|---|
| Any ZIP, APK, IPA, MSIX, AppX, DMG, PyInstaller exe | `open_binary` → `inspect_artifact` |
| PyInstaller CArchive (bootloader + app layer) | `open_binary` → `inspect_artifact` (app layer, not bootloader prefix) |
| Bun `--compile` standalone | `open_binary` → `inspect_artifact` → extract modules → JavaScript tools |
| Deno `deno compile` | `open_binary` → `inspect_artifact` → extract virtual FS → JavaScript tools |
| Apple resource-only bundle (plist/IB/assets/keyed-archive) | `open_bundle_resources` → resource tools |
| Android APK — code, DEX classes, methods, refs | `inspect_android_package` → Android focused tools |
| Managed PE/CLI assembly (.NET) | `inspect_managed_artifact` → managed tools |
| Firmware image | `inspect_firmware_regions` → `extract_firmware` |
| ESP32 app/bootloader (`0xE9` magic) | `inspect_artifact` (no provider needed) |
| .NET NativeAOT PE/ELF | `open_binary` with Ghidra provider, NativeAOT workflow |

### Native binary tools (zero-engine built-in parsers)
| Target type | Tool |
|---|---|
| Go compiler/module/build metadata/static strings | `inspect_go_binary` (pass `include_string_literals: true`, page with `inspect_analysis_view` kind `go`) |
| Rust cargo-auditable dependency metadata | `inspect_rust_binary` (ELF/PE/thin Mach-O; select views with `view: {collection: "packages"}`) |
| PE Authenticode certificates | `inspect_pe_certificates` |
| PE import + delay-load tables | `inspect_pe_imports` |
| PE TLS callbacks + load configuration | `inspect_pe_load_config` |
| PE resource tree (icons, strings, manifests) | `inspect_pe_resources` |
| PE/ELF dynamic exports | `inspect_native_exports` |
| ELF/PE/Mach-O hardening flags | `inspect_binary_hardening` |
| ELF note tables (build-id, ABI-tag) | `inspect_elf_notes` |
| ELF unwind function ranges (`.eh_frame`) | `inspect_elf_unwind_ranges` |
| ELF/Mach-O pre-main initializers | `inspect_native_initializers` |
| ELF offline layout, symbols, relocs, mitigations | `inspect_binary_layout` (pwntools; no disassembler) |
| Linux ELF core dump (threads, registers, notes) | `inspect_recorded_crash` |
| Linux kernel module metadata | `inspect_kernel_module` |
| Linux kernel build config (`CONFIG_*`) | `inspect_kernel_build_config` |
| Apple `.ips` crash report | `inspect_apple_ips` |
| CPython 3.7-3.13 `.pyc` headers + bytecode identity | `inspect_python_pyc` |
| Erlang BEAM IFF container | `inspect_erlang_beam` |
| Unity IL2CPP `global-metadata.dat` | `inspect_il2cpp_metadata` (page with `inspect_analysis_view`) |
| CUDA/HIP embedded code objects | `inspect_gpu_code_objects` |
| GGUF/safetensors ML model declarations | `inspect_model_artifact` |
| Windows Shell Link `.lnk` shortcut | `inspect_windows_shortcut` |
| Native exe/lib (IDA/Ghidra/Kuna deep analysis) | `open_binary` → focused analysis tools → `binary_overview` |

### Web / JS / Electron targets
| Target type | Tool |
|---|---|
| ASAR or extracted JS/Electron tree | `analyze_javascript_application` |
| Electron fuse settings (before Inspector attach) | `inspect_electron_fuses` |
| Live Electron runtime | `list_electron_targets` → attach |
| User-owned live browser page | `list_browser_targets` → browser tools |
| Browser scenario (click, type, navigate) | `capture_browser_scenario` |
| AgentEnv bundle (web app environment) | `capture_browser_scenario` → `export_environment_bundle` |
| HAR / SAZ (Fiddler) / mitmproxy / qlog capture | `inspect_web_network_capture` (Fiddler: `format: "saz"`) |
| SPA passive capture (multi-origin) | `inspect_web_network_capture` with `allowed_origins` covering both page + API origins |
| Feature tracing / version comparison | `trace_application_feature`, `compare_application_versions` |
| JavaScript source recovery, bundle analysis | `recover_javascript_sources`, `analyze_web_bundle` |
| Web event listeners, network capture | `inspect_web_event_listeners`, `inspect_web_network_capture` |

### Mobile / Android
| Target type | Tool |
|---|---|
| APK class/method/reference search | `search_android_classes`, `inspect_android_class`, `inspect_android_method` |
| APK signing verification (v1/v2/v3/v3.1) | `inspect_apk_signature` |
| ADB live device (list, pull, screen, logcat) | `list_adb_devices`, `inspect_adb_device`, `inspect_adb_package`, `read_adb_logcat` |
| Flutter/Dart AOT | `identify_flutter_build`, `inspect_dart_aot` |

### Data / Capture formats
| Target type | Tool |
|---|---|
| SQLite database schema + rows | `inspect_sqlite_database` (Node >=24.15; `schema_scope: "database"` for full schema) |
| WebAssembly artifact | `inspect_wasm_artifact` (supply WABT via `REA_WABT_BIN_DIRECTORY`) |
| EVM bytecode | `inspect_evm_interface` (`raw` or `hex` encoding) |
| PCAP packet-field discovery | `inspect_packet_fields` → `inspect_packet_capture` (TShark 4.x, Linux prlimit) |
| PCAP DNS/SNI/protocol summaries | `inspect_pcap_capture` → kind pcap pages |
| Logic/signal recordings | `inspect_signal_decoders` → `decode_signal_recording` (sigrok-cli via `REA_SIGROK_COMMAND`) |

### Native runtime observation
| Task | Tool |
|---|---|
| Static value flow, taint, native trace | `trace_native_values` |
| Native instrumentation (Frida) | `list_frida_devices` → `start_frida_session` → `load_frida_script` → `instrument_with_frida` |
| GDB debug session | `start_gdb_session` → `gdb_console` |
| Rizin debug session | `start_rizin_debug_session` → `rizin_debug_command` |
| Cross-reference search | `xrefs`, `procedure_references`, `find_xrefs_to_name` |
| Process scenario capture | `capture_process_scenario`, `compare_process_captures` |
| Swift type analysis | `analyze_swift_types` |
| Objective-C classes/protocols | `get_objc_classes`, `get_objc_protocols` |

---

## Provider-specific rules

### IDA Pro
- Open with `open_binary` + `provider_id: "ida"` on the **original input binary**.
- **Never** pass an `.idb` or `.i64` database as the binary path.
- IDA does **not** supply `binary_overview`; go straight to `analyze_function`, pseudocode, or search.
- Modern headless profile: creates and closes a private database (no GUI save).
- Legacy attached profile: binds the already-open GUI session by SHA-256.

### Kuna
- Requires `REA_KUNA_COMMAND` env var configured.
- `provider_id: "kuna"` for procedure lists, pseudocode, assembly, `analyze_function`.
- For pseudocode/assembly, `raw_result.source` names the cached `.c`/`.asm` file and byte span. Search it directly instead of calling per-function.
- Callers/callees use a separate body-free graph; `xrefs` returns exact-address incoming sites.
- Cold first answer can come from a single-function run; assembly waits for the C export.

### Ghidra
- For large native targets, set `ghidra.startup_timeout_ms` via `update_analysis_settings` before the cold import.
- For editable analysis that must survive later agent processes, use the owned Program checkpoint workflow.
- Default timeout: 330 seconds; increase for cold imports on slow machines.

---

## Operational rules

### Summary-first + paging
- Always start with `detail: "summary"` for large targets.
- Use `inspect_analysis_view` with the returned `parent_evidence_id` for follow-up pages.
- `analyze_function` default reply is the summary; complete dossier stays retained under `parent_evidence_id`.
- For transport truncation (`resource_constraint` with `details.resource: "transport"`): call `inspect_analysis_view` with the same-session Evidence reference. Do NOT repeat the original call.

### SPA cross-origin API detection
- Default passive capture scope = page's own origin only.
- Discover API origins from absolute URLs in loaded bundles/scripts first.
- Then re-capture with `allowed_origins: [page_origin, api_origin1, ...]` — the list replaces the default scope.
- Check `completeness.excluded` before claiming an API is absent.

### Evidence workflow
- Every conclusion must distinguish: **observations** (tool returned), **inferences** (analyst reasoned), **unknowns** (not reachable).
- Cite `ev_...` Evidence IDs for every claim.
- Use `get_evidence_bundle` with `detail: "summary"` and exact filters to recover a lost `parent_evidence_id`.
- End investigation with `reset_investigation`; supply `save_path` to checkpoint.

### Multi-worker parallelism
- Independent questions (no data dependency) → assign to separate workers.
- Point each worker at existing retained Evidence IDs to avoid re-running analysis.

### Broader investigation (7 steps)
1. Turn request into checklist of questions + evidence each needs.
2. Check existing session state, bookmarks, prior Evidence; reuse matching state.
3. Start with smallest useful overview/inventory; expand only where returned evidence leaves a concrete gap.
4. Inspect packaged resources + config alongside code when they affect the question.
5. Corroborate conclusions with the evidence type they require (runtime only when static can't answer).
6. Decompose into independent questions; parallelize when possible.
7. Keep a finding ledger linking conclusions to Evidence IDs, confidence, boundaries, and unknowns.

---

## Read the relevant reference

| Topic | Reference |
|---|---|
| Native binaries, managed, archives, extraction | `references/native-and-artifacts.md` |
| ASARs, extracted JS, feature tracing, version compare | `references/javascript-applications.md` |
| Android APK, classes, methods, refs | `references/android-applications.md` |
| Native instrumentation, debugger, process capture | `references/runtime-observation.md` |
| Evidence paging, comparisons, unknowns, verification | `references/evidence-workflows.md` |
| AgentEnv bundles of web apps | `references/environments.md` |
| REA connection, recovery, plugin install | `references/connection-and-recovery.md` |

---

## Finish

Explain findings in plain language tied to Evidence. Close opened native sessions
with `close_binary`. End with `reset_investigation`; `save_path` checkpoints the
full bundle for restoration in a new process.
