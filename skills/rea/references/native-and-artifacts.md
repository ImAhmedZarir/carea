# Native, Managed & Archive Reverse-Engineering Playbook (`/rea`)

Deep multi-layer dissection patterns for PE, ELF, Mach-O, Go, Rust, .NET, Unity IL2CPP, PyInstaller, Bun, Deno, firmware, and native disassembler backends.

## 1. Zero-Engine Entropy, Hardening & Compiler Peeling (Run Before Decompilation)

1. **`inspect_byte_entropy`:** Always inspect entropy first on unknown executables or blobs. Uniform entropy > ~7.2 bits/byte flags packed/encrypted sections (UPX, Themida, encrypted payloads) before wasting cold decompiler imports.
2. **`inspect_binary_hardening`:** Extracts PIE/ASLR, NX, RELRO, stack-protector/fortify signals, and signature presence across PE/ELF/Mach-O slices.
3. **`inspect_pe_imports` + `inspect_pe_load_config` + `inspect_pe_certificates` + `inspect_pe_resources`:** Recover standard & delay-load imports, **TLS callbacks that execute before `main`**, SafeSEH/CFG/XFG/EH-continuation flags, PKCS#7 signers, and resource trees.
4. **`inspect_elf_notes` + `inspect_elf_unwind_ranges` + `inspect_native_initializers` + `inspect_binary_layout`:** Extract GNU build-id, `.eh_frame` FDE bounds surviving `strip`, constructors running before `main` (`DT_PREINIT_ARRAY`, `DT_INIT_ARRAY`, `.ctors`, Mach-O `__mod_init_func`, `__init_offsets`), and pwntools symbol/reloc tables.
5. **Runtime Container Unpacking:**
   - **PyInstaller:** `open_binary` -> `inspect_artifact`; focus on the embedded CArchive application layer rather than the generic bootloader prefix (`inspect_python_pyc` on extracted `.pyc`).
   - **Bun `--compile`:** `open_binary` -> `inspect_artifact` extracts embedded module graphs -> hand off extracted scripts to `analyze_javascript_application`.
   - **Deno `deno compile`:** `open_binary` -> `inspect_artifact` inspects embedded virtual FS entries, counts, and byte lengths without executing the binary.
   - **ESP32 (`0xE9` magic):** Route straight to `inspect_artifact` with no native provider needed.

## 2. Language-Specific Binary Parsers

- **Go (`inspect_go_binary`):** Recovers Go toolchain version, module path/dependencies, build flags, and `(ptr, len)` UTF-8 static string literals when `include_string_literals: true` (page via `inspect_analysis_view` kind `go` collection `string_literals`).
- **Rust (`inspect_rust_binary`):** Decodes cargo-auditable `.dep-v0` / `__DATA,.dep-v0` crate inventories + rustc `/rustc/<40-hex>/` commit clues (`detail: "summary"` or `view: {collection: "packages"}`).
- **Unity IL2CPP (`inspect_il2cpp_metadata`):** Parses `global-metadata.dat` (v24/27/29/31/39) for assemblies, types, methods, fields, properties, events, `method_indices` parameter slices, and string literals; pass matching `binary_path` (`GameAssembly.dll`/`libil2cpp.so`) to resolve native RVAs.
- **.NET (`inspect_managed_artifact` / `.NET NativeAOT`):** Managed CLI assemblies use `inspect_managed_artifact` -> `inspect_managed_members` -> `inspect_managed_native_boundaries` -> `project_managed_application_graph`. NativeAOT binaries require native Ghidra analysis via `open_binary`.
- **AI / SQLite / WASM / EVM / Erlang / Kernel / Crash:** `inspect_model_artifact` (`GGUF`/`safetensors`), `inspect_sqlite_database` (`schema_scope: "database"`), `inspect_wasm_artifact` (WABT), `inspect_evm_interface`, `inspect_erlang_beam`, `inspect_kernel_module`, `inspect_kernel_build_config`, `inspect_recorded_crash`, `inspect_apple_ips`, `inspect_gpu_code_objects`, `inspect_devicetree`, `inspect_uefi_firmware`.

## 3. Native Engine Control (Ghidra, IDA Pro, Kuna, Rizin, Cutter)

- **Ghidra (default native backend):** Open via `open_binary`. For slow/large binaries hitting startup timeout, adjust `ghidra.startup_timeout_ms` via `update_analysis_settings` before retrying. Use owned Program checkpoints if renamed symbols/comments (`set_addresses_names`, `set_comment`, `set_bookmark`) must persist across sessions.
- **IDA Pro (`provider_id: "ida"`):** Pass the **raw executable/library**, NEVER `.idb` or `.i64`. Skip `binary_overview` (unsupported on IDA) and call `analyze_function`, `procedure_pseudo_code`, `list_procedures`, or search tools directly.
- **Kuna (`REA_KUNA_COMMAND`, `provider_id: "kuna"`):** Read cached `.c` / `.asm` byte ranges referenced in `raw_result.source` directly for high-speed scanning.
- **Data-Flow & Call-Path Tracing:** Use `trace_native_values` for backward/forward register/stack/memory slices, `inspect_native_dispatch_metadata` for indirect/vtable targets, `batch_decompile` (`detail: "summary"` -> page `items`/`pseudocode`), and `build_call_path` / `get_call_graph` / `xrefs` for entry-to-sink chains.
- **Apple Native Bundles:** For non-binary resource inspection, `open_bundle_resources` -> `inspect_plist`, `decode_interface_builder`, `inspect_keyed_archive`, `inspect_asset_catalog`. For code, `open_binary` -> `inspect_macho`, `list_architectures`, `get_objc_classes`, `get_objc_protocols`, `analyze_swift_types`, `demangle_swift`, `trace_dylib_resolution`.
