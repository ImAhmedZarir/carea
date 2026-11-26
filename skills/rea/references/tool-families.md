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
| **Native binary (ELF/PE/Mach-O)** | `native,enhanced,application,session` *(add `direct` or `frida` only when needed)* | `open_binary`, `analyze_function`, `inspect_analysis_view`, `match_native_functions`, `compare_functions`, `build_call_path`, `capture_process_scenario`, `compare_process_captures`, `start_frida_session` |
| **JS / Web / Electron** | `browser,electron,application,javascript-runtime,session` | `inspect_web_page`, `analyze_javascript_application`, `reconcile_javascript_runtime`, `trace_javascript_semantics`, `inspect_electron_fuses`, `inspect_playwright_trace`, `audit_release_exposure`, `build_reconstruction_obligation_ledger`, `verify_reconstruction` |
| **Android / Flutter APK** | `android,apktool,jeb,flutter,frida,adb,application,session` | `inspect_android_package`, `search_android_classes`, `inspect_android_class`, `inspect_android_method`, `inspect_android_jni_bindings`, `decode_android_resources`, `identify_flutter_build`, `inspect_dart_aot`, `project_android_application_graph` |
| **.NET / Managed** | `managed,artifact,application,session` | `inspect_managed_artifact`, `inspect_managed_members`, `inspect_managed_native_boundaries`, `compare_managed_members`, `verify_managed_native_boundaries`, `inspect_nuget_nupkg` |
| **Firmware / UEFI / Packages** | `firmware,uefi,artifact,session,direct` | `inspect_artifact`, `extract_artifact`, `inspect_firmware_regions`, `extract_firmware`, `inspect_uefi_firmware`, `inspect_uefi_nvram`, `extract_uefi_firmware`, `inspect_maven_gradle_metadata` |
| **Network Captures & AgentEnv** | `browser,artifact,pcap,application,session` | `inspect_web_network_capture`, `inspect_pcap_capture`, `capture_browser_scenario`, `compare_web_captures`, `export_environment_bundle`, `export_evidence_bundle` |

## 3. Evidence Boundaries to Report Explicitly

- `verify_reconstruction` verifies only the declared claims inside its `specification` object; missing or limited observations remain `unknown`.
- `compare_artifacts` and `compare_functions` require matching scope and complete member coverage before reporting equivalence.
- Exported AgentEnv environments replay recorded traffic and declared state handlers within captured bounds.
