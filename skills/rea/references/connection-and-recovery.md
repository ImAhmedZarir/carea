# REA Connection, Engine Discovery & Deadline Recovery

Fast diagnostics and recovery when MCP tools, external providers, or large-target deadlines block analysis.

## 1. Engine & Provider Readiness

- Run `rea doctor --json` (or `binary_session` with `{"detail": "complete"}`) when a specific provider (`ghidra`, `ida`, `kuna`, `jadx`, `jeb`, `frida`, `rizin`, `gdb`, `wabt`, `tshark`, `sigrok`, `desktop_build`) reports unavailable.
- **Hot-Cold Schema Efficiency (`>=6.10.0`):** Use `REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` + `REA_MCP_INPUT_SCHEMA_PROFILE=compact` + `REA_MCP_OUTPUT_SCHEMA_PROFILE=off` (`full` output/input profiles are rejected on `6.10.0+`). Call `discover_tools` to materialize specific tool families on demand.
- **Missing Global CLI Fallback:** Replace `rea` with `npx -y rea-agents@latest <command> ... --json` using absolute target paths.

## 2. Client Timeout vs Server/Provider Timeout

- **Host MCP Client Timed Out (`timed out awaiting tools/call`):** Work may still exist in the REA ledger or partial evidence store. Check `binary_session` and `get_evidence_bundle` (`detail: "summary"`) instead of immediately re-running the identical call. Adjust client tool timeout (e.g. `tool_timeout_sec`) when analyzing huge inputs.
- **REA Returned `provider_timeout`:** Read `remediation.action` and reuse `error.details.partial_observation` via `inspect_analysis_view`. Adjust exact server tunables via `update_analysis_settings` only where recommended:
  - JS/ASAR: `analysis_timeout_ms`, `max_heap_mb`, `asar.max_header_bytes` (`REA_ASAR_MAX_HEADER_BYTES`)
  - Ghidra: `ghidra.startup_timeout_ms`
  - JADX: `jadx.operation_timeout_ms` (`REA_JADX_OPERATION_TIMEOUT_MS`), `REA_JADX_HEAP_MIB`
  - Native diffing: `native.matching_representation_bytes` (`REA_NATIVE_MATCHING_REPRESENTATION_BYTES`)
  - Captures: `REA_CAPTURE_DECODER_OLD_GENERATION_MIB`
- **Transport Oversize (`resource_constraint` -> `transport`):** Never repeat the producer blindly; fetch slices of the returned `parent_evidence_id` with `inspect_analysis_view` or stream via `export_evidence_bundle`.

## 3. Session & Cleanup Recovery

- If `cleanup_incomplete` occurs, call the named cleanup owner (`close_binary`, `close_frida_session`, `close_gdb_session`, `close_rizin_debug_session`) directly before starting conflicting operations.
- Checkpoint long investigations before closing/restarting with `reset_investigation` + `save_path`, then reload via `import_evidence_bundle`.
