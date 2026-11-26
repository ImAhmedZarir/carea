# Workflow Guide: Native / Binary Parity & AgentEnv Reconstruction

Use **Mode 3 (Deep Forensics / Reconstruction Verification / AgentEnv)** when the goal is deep understanding of a native binary, .NET assembly, APK, firmware/UEFI image, or exporting a reproducible RL AgentEnv sandbox — rather than a Clean-Room UI rebuild.

> [!WARNING]
> Only inspect binaries, devices, and services you own or are explicitly authorized to examine. Optional native providers (**IDA Pro / Hex-Rays**, **Hopper Disassembler**, **JEB**) require your own valid license ([`../../DISCLAIMER.md`](../../DISCLAIMER.md)).

---

## 1. Context-Scoped REA Profiles

Select only the families your target requires (or use `REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` on `rea >= 6.10.x`):

- **Native binary:** `REA_MCP_TOOL_FAMILIES=native,enhanced,application,session` *(add `direct` for focused procedure/assembly lookups)*
- **Managed .NET assembly:** `REA_MCP_TOOL_FAMILIES=managed,session`
- **Firmware / UEFI:** `REA_MCP_TOOL_FAMILIES=firmware,uefi,session,direct` *(omit `uefi` on `rea 6.8.x`)*
- **Web session -> AgentEnv:** `REA_MCP_TOOL_FAMILIES=browser,application,session`

Keep `REA_MCP_INPUT_SCHEMA_PROFILE=compact` and `REA_MCP_OUTPUT_SCHEMA_PROFILE=off`.

---

## 2. Path A — Native Binary Reconstruction & Parity

1. **Open & inspect summary-first:**
   - Call `open_binary` on the explicit local executable (with optional `provider_id`, e.g., Ghidra `12.2`, Hopper, IDA, or Kuna `1.1000`).
   - Use `binary_overview`, `search_procedures`, `search_strings`, or `trace_feature` to locate target subsystems.
   - Inspect procedures with `analyze_function` (default summary returns `parent_evidence_id`; page facets via `inspect_analysis_view`).
   - Follow data and call paths with `trace_native_values`, `get_call_graph`, and `trace_call_path`.
2. **Compare & verify parity:**
   - After writing your independent implementation, compile and compare behaviors cleanly:
     - **Structural / function comparison:** `match_native_functions`, `compare_functions`, `build_call_path`.
     - **Observable process parity:** `capture_process_scenario` + `compare_process_captures` *(new PTY captures require Linux/macOS; comparing retained capture files also works on Windows)*.
     - **Static-to-runtime alignment:** `correlate_static_and_runtime` (records hypotheses without asserting causality from cochange alone).
     - **Finite spec verification:** `verify_reconstruction`.
3. **Export & clean up:**
   - Export retained records with `export_evidence_bundle` and release engine resources with `close_binary`.

---

## 3. Path B — Managed .NET & Specialized Static Targets

- **.NET assemblies:** `inspect_managed_artifact` -> `inspect_managed_members` (with `--type` / type filters) -> `import_managed_reconstruction` -> `compare_managed_members` & `verify_managed_native_boundaries`.
- **Standalone / exotic formats (no disassembler required):** `inspect_go_binary`, `inspect_rust_binary`, `inspect_il2cpp_metadata`, `inspect_model_artifact`, `inspect_gpu_code_objects`, `inspect_wasm_artifact`, `inspect_evm_interface`, `inspect_python_pyc`, `inspect_erlang_beam`, `inspect_sqlite_database`, `inspect_nuget_nupkg`, `inspect_maven_gradle_metadata`, `inspect_uefi_firmware`, `extract_uefi_firmware`, `inspect_uefi_nvram`.

---

## 4. Path C — Web Capture to Runnable AgentEnv Bundle

1. Map the disposable/seeded web app with `inspect_web_page` and `capture_web_screenshot`.
2. Record an end-to-end interaction session via `capture_browser_scenario` (declaring any credentials as `{secret_id, environment_variable}` rather than raw literals), or inspect an existing HAR via `inspect_web_network_capture`.
3. Preview API surface and write-tool coverage with `inspect_analysis_view` (`api-surface`, `environment-manifest`, `environment-state`, `environment-coverage`).
4. Export the runnable sandbox with `export_environment_bundle` (or CLI `rea environment-build <capture.har> <dir>`), then test/serve with `agentenv` / `rea environment-serve` as documented in upstream `morluto/rea`.
