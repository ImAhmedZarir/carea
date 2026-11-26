---
name: rea
description: Run REA-first deep reverse engineering via external rea tools to analyze native binaries, JS/Electron bundles, .NET/Java/Android/Flutter packages, UEFI/firmware, or PCAP/SQLite artifacts, track ev_... and unk_... ledgers, verify reconstructions with verify_reconstruction, or export AgentEnv bundles. Triggered by /rea or forensic/decompilation tasks that do NOT ask for a UI rebuild loop or visual pixel diff. Skip when only observable UI rebuild is needed (use /ca) or when coordinating a two-team airlock rebuild (use /carea).
---

# `/rea` — REA-First Deep Investigation, Verification & AgentEnv

Use this entry point for targeted deep analysis using the external **REA (`rea-agents`)** engine, without starting a Craft Anything UI rebuild loop.

> Read [`../_shared/responsible-use.md`](../_shared/responsible-use.md) first: operate strictly on authorized targets and separate **Observation** (`ev_...`), **Inference**, and **Unknown** (`unk_...`) in every conclusion.

## When to Stay Here vs Delegate

- **Stay in `/rea`:** Binary/ELF/PE/Mach-O inspection, decompiler sessions, Frida/GDB/Rizin tracing, Electron/JS bundle forensics, .NET/IL2CPP/Android/Flutter analysis, offline firmware/UEFI/NuGet/Maven checks, capture comparison (`compare_web_captures`, `compare_functions`, `compare_artifacts`), formal reconstruction checks (`verify_reconstruction`), or building an `AgentEnv` sandbox (`export_environment_bundle`).
- **Delegate to `/ca`:** Only observable website/desktop UI capture, `rebuild_start` / `rebuild_check`, visual pixel diffs, or replacement asset generation are needed.
- **Delegate to `/carea`:** The task connects REA understanding to a rebuilt implementation across an Airlock (`REA -> Airlock -> CA -> Dual Parity`).

## Context Budget & Lean Startup

Never load the full 264-tool schema catalog with verbose schemas unless required. Configure REA via:

1. **Hot/cold catalog (REA `>= 6.10.0`):** `REA_MCP_TOOL_CATALOG_PROFILE=hot-cold`, `REA_MCP_INPUT_SCHEMA_PROFILE=compact`, `REA_MCP_OUTPUT_SCHEMA_PROFILE=off`. Initial session exposes 5 tools (`binary_session`, `open_binary`, `close_binary`, `get_evidence_bundle`, `discover_tools`); request needed tools with `discover_tools`.
2. **Scoped families:** Set `REA_MCP_TOOL_FAMILIES` to the exact target families documented in [`references/tool-families.md`](references/tool-families.md). Never set `REA_MCP_INPUT_SCHEMA_PROFILE=full` or `REA_MCP_OUTPUT_SCHEMA_PROFILE=full` on REA `>= 6.10.0` (rejected at startup).

## Standard Execution Loop

1. **Preflight:** Check active capabilities with `binary_session` (`inspect_analysis_settings` if timeout tuning is needed). Confirm target scope and authorization.
2. **Scoped Inspection:** Open target via `open_binary` or domain tools (`inspect_artifact`, `analyze_javascript_application`, `inspect_android_package`, `inspect_managed_artifact`, `inspect_web_page`). Prefer default summary replies and page full records with `inspect_analysis_view`.
3. **Unknown & Evidence Discipline:** Record every unverified path, encrypted container, or missing dynamic observation with `record_unknown` (`unk_...`). Preserve `ev_...` and `parent_evidence_id` references verbatim.
4. **Verification or AgentEnv Export:**
   - Behavioral verification: `build_reconstruction_obligation_ledger`, `trace_application_feature`, `evaluate_reconstruction_coverage`, `verify_reconstruction`.
   - Environment export: `capture_browser_scenario` -> `export_environment_bundle` (or `export_evidence_bundle` to archive findings).
5. **Close cleanly:** Close active handles (`close_binary`, `close_frida_session`, `close_gdb_session`, `close_rizin_session`) when done.

## References

- Target-specific `REA_MCP_TOOL_FAMILIES` presets and verified tools: [`references/tool-families.md`](references/tool-families.md)
- Evidence and `evidence_format: 2` notes: [`../_shared/evidence-handoff.md`](../_shared/evidence-handoff.md)
- Behavioral parity checks: [`../_shared/parity-verification.md`](../_shared/parity-verification.md)
- Authorization & non-circumvention rules: [`../_shared/responsible-use.md`](../_shared/responsible-use.md)
