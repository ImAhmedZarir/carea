# Upstream Fact Ledger (`docs/upstream-facts.md`)

Every external engine version, tool name, tool family, CLI flag, and environment variable referenced in `carea` is tracked below.

- **`VERIFIED`**: Confirmed directly in live local CLI/MCP execution or in pinned upstream release files (`morluto/rea` tag `rea-agents-6.10.1`, `storytold/craft-anything` local `0.6.0` binary and tag `v0.6.1`).
- **`UNVERIFIED`**: Could not be executed or observed directly in the build environment; excluded from `skills/**` prompt instructions until verified.
- **`WRONG`**: Claim found inaccurate in an earlier draft of `carea` (v0.1) and fixed in Phase 1; retained in the history log below so regressions are prevented.

---

## 1. Environment Limitations Recorded Honestly

| Claim | Where used in `carea` | Verified how | Verified version | Status |
| --- | --- | --- | --- | --- |
| `rea --version`, `rea --help`, `rea doctor` local CLI execution | `docs/compatibility.md`, `scripts/verify-upstream.*`, `carea doctor` | Attempted local run failed: host lacks global Node.js (`^22.23.4 \|\| ^24.22.1 \|\| >=26.12.1`) and bundled plugin lacks built `dist/` runtime. Verified CLI syntax via `rea-agents-6.10.1` `scripts/rea.mjs` & `docs/getting-started/cli.md` instead; local shell run remains unverified here. | `6.10.1` (docs) / `6.8.0` (unbuilt plugin) | `UNVERIFIED` *(local CLI exec; CLI docs/source verified separately)* |
| Global `ca` shell alias | Earlier v0.1 docs (`README.md`, `docs/getting-started.md`) | Local environment had `.gemini/config/node_modules/.bin/ca.cmd`, whereas standalone `craft-anything-cli` portable binary does not guarantee a `ca` symlink. Use `craft-anything-cli` for CLI calls; reserve `/ca` for the skill trigger. | `0.6.0` | `VERIFIED` *(clarified: use `craft-anything-cli`)* |
| `craft-anything-cli` `0.6.1` local binary execution | `compat/matrix.json`, `docs/compatibility.md` | GitHub release `v0.6.1` (`2026-11-12`) & docs verified remotely; local binary on build host is `0.6.0`. | `0.6.1` *(docs)* / `0.6.0` *(local)* | `VERIFIED` *(docs for `0.6.1`; local `0.6.1` exec `UNVERIFIED`)* |

---

## 2. Historical `WRONG` Claims Caught & Fixed in Phase 1

| Claim | Where it appeared (v0.1) | Finding & Correction | Verified version | Status |
| --- | --- | --- | --- | --- |
| `` `trace_spec` `` parameter/claim on `verify_reconstruction` | `skills/carea/references/parity-verification.md` (v0.1 L26) | **Does not exist**: `verify_reconstruction` accepts `specification` (`required: ["specification"]`), not `trace_spec`. Fixed to refer to `specification`. | `6.8.0` & `6.10.1` | `WRONG` *(Fixed)* |
| `` `309` engine tools `` in Craft Anything | `docs/getting-started.md` (v0.1 L60) | `v0.6.1` `docs/tools.md` documents **303 engine tools in 17 toolsets** and `v0.6.1` `README.md` documents **320 tools** total; local `craft-anything-cli 0.6.0 capabilities --json` reports **`322` total commands** across 17 toolsets. Replaced `309` with exact `0.6.1` / `0.6.0` figures. | `0.6.1` / `0.6.0` | `WRONG` *(Fixed)* |
| Unqualified wildcard tool notations (`build_*`, `project_pin_*`, `inspect_uefi_*`) in skills | `skills/carea/references/intent-router.md`, `docs/workflows/*.md` | Ambiguous shorthands can imply nonexistent tools (for instance there is no `build_files_search` in `0.6.0`/`0.6.1`). Replaced with exact verified tool names (`build_files_list`, `build_file_read`, `build_file_write`, `build_file_edit`, `build_checklist`, `build_command_run`). | `0.6.0` & `0.6.1` | `WRONG` *(Fixed)* |

---

## 3. Verified Engine Versions, Tool Counts & CLI Commands

| Claim | Where used in `carea` | Verified how | Verified version | Status |
| --- | --- | --- | --- | --- |
| `craft-anything-cli --version` -> `craft-anything-cli 0.6.0` | `compat/matrix.json`, `carea doctor`, `verify-upstream` | Executed `craft-anything-cli.exe --version` locally | `0.6.0` | `VERIFIED` |
| `craft-anything-cli doctor` | `docs/getting-started.md`, `verify-upstream`, `carea doctor` | Executed locally -> `healthy: true`, `MCP server answered (protocol 2025-06-18, 30 tools listed)` | `0.6.0` | `VERIFIED` |
| `craft-anything-cli commands` & `craft-anything-cli capabilities --json` | `docs/getting-started.md`, `intent-router`, `verify-upstream` | Executed locally -> `322` commands across 17 toolsets, `analysis_mode: "clean-room"` | `0.6.0` | `VERIFIED` |
| `craft-anything-cli mcp --clean-room` (without `--all-tools`) lists 30 tools | `docs/getting-started.md`, `carea mcp-profile` | Checked `craft-anything-cli.exe mcp --help` and `doctor` output (`30 tools listed`); `--all-tools` lists all tools | `0.6.0` | `VERIFIED` |
| `craft-anything-cli mcp --restricted --allow-web --allow-capture --allow-run --deep --clean-room --project` flags | `carea mcp-profile`, `skills/carea/references/modes.md` | Inspected `craft-anything-cli.exe mcp --help` directly | `0.6.0` | `VERIFIED` |
| `craft-anything-cli rebuild --clean-room` / `--deep` / `--build-with` / `--generate-assets` / `--project-folder` / `--existing` / `--backend` / `--rounds` / `--unattended` | `skills/ca/`, `skills/carea/references/modes.md` | Inspected `craft-anything-cli.exe rebuild --help` directly | `0.6.0` | `VERIFIED` |
| `craft-anything-cli setup --client <claude_code\|codex\|cursor> --clean-room --no-skill --dry-run` | `docs/coexistence.md` | Inspected `craft-anything-cli.exe setup --help` directly | `0.6.0` | `VERIFIED` |
| CA tool counts: `303 engine tools` (`docs/tools.md`), `320 tools` (`README.md`), `17 toolsets`, early alpha | `README.md`, `compat/matrix.json`, `docs/compatibility.md` | Checked `storytold/craft-anything` tag `v0.6.1` `README.md` & `docs/tools.md` | `0.6.1` | `VERIFIED` |
| REA Node requirement `^22.23.4 \|\| ^24.22.1 \|\| >=26.12.1` | `compat/matrix.json`, `carea doctor`, `docs/compatibility.md` | Checked `morluto/rea` tag `rea-agents-6.10.1` `package.json` | `6.10.1` | `VERIFIED` |
| REA `264` advertised MCP tool schemas | `docs/getting-started.md`, `docs/compatibility.md` | Counted JSON schema files in `rea-agents-6.10.1` `scripts/verify/advertised-schemas/tools/` (`264`) | `6.10.1` | `VERIFIED` |
| REA live MCP `binary_session` works on session server | Session runtime | Called `rea_rea:binary_session` `{}` in session (observed `6.8.0`-era backend capabilities) | `6.8.0` *(live MCP)* | `VERIFIED` |
| `npx rea-agents setup`, `rea setup --client <id> --tool-families <ids> --tool-catalog-profile <hot-cold\|full> --skill=false --dry-run` | `docs/getting-started.md`, `docs/coexistence.md` | Checked `rea-agents-6.10.1` `README.md`, `docs/getting-started/installation.md`, `docs/getting-started/client-configuration.md` | `6.10.1` | `VERIFIED` *(docs)* |
| REA CLI subcommands (`--version`, `--help`, `--mcp`, `mcp`, `doctor`, `analyze`, `compare`, `compare-bundles`, `decompile`, `environment-build`, `environment-serve`, `environment-export`, `environment-compare`, `evidence-import`, `inspect-*`) | `skills/rea/`, `docs/workflows/` | Checked `rea-agents-6.10.1` `docs/getting-started/cli.md` and `scripts/rea.mjs` | `6.10.1` | `VERIFIED` *(docs/source)* |

---

## 4. Verified Environment Variables & Tool Families (REA `6.10.1`)

| Claim | Where used in `carea` | Verified how | Verified version | Status |
| --- | --- | --- | --- | --- |
| `REA_MCP_TOOL_FAMILIES` (`direct`, `enhanced`, `native`, `artifact`, `managed`, `firmware`, `uefi`, `android`, `pcap`, `flutter`, `frida`, `apktool`, `jeb`, `adb`, `browser`, `electron`, `javascript-runtime`, `application`, `session`) | `compat/matrix.json`, `carea mcp-profile`, `skills/_shared/`, `skills/rea/` | Checked `rea-agents-6.10.1` `src/contracts/toolFamilyIds.ts` and `src/config/mcpToolFamilies.ts` | `6.10.1` | `VERIFIED` |
| `uefi` tool family added in `6.10.0` (absent in `6.8.x`) | `docs/compatibility.md`, `compat/matrix.json` | Checked `rea-agents-6.10.1` `CHANGELOG.md` and local `6.8.0` plugin schema list | `6.10.0+` | `VERIFIED` |
| `REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` advertises 5 initial tools (`binary_session`, `open_binary`, `close_binary`, `get_evidence_bundle`, `discover_tools`); `inspect_analysis_view` loads on demand | `carea mcp-profile`, `skills/rea/`, `docs/getting-started.md` | Checked `rea-agents-6.10.1` `docs/reference/mcp-contracts.md` (`### Hot/cold catalog discovery`) | `6.10.1` | `VERIFIED` *(docs)* |
| `REA_MCP_INPUT_SCHEMA_PROFILE=compact` and `REA_MCP_OUTPUT_SCHEMA_PROFILE=off \| compact`; `full` rejected in `>=6.10.0` | `carea doctor`, `carea mcp-profile`, `compat/matrix.json` | Checked `rea-agents-6.10.1` `CHANGELOG.md` (`6.10.0` notes) and `docs/getting-started/client-configuration.md` | `6.10.0+` | `VERIFIED` |
| `evidence_format: 2` required in REA `>=6.10.0` | `schemas/`, `skills/_shared/evidence-handoff.md` | Checked `rea-agents-6.10.1` `CHANGELOG.md` (`6.10.0` breaking notes) | `6.10.0+` | `VERIFIED` |

---

## 5. Verified Upstream MCP & CLI Tool Names Used in `carea`

### Craft Anything (`0.6.0` verified CLI + live MCP, `0.6.1` `docs/tools.md`)

| Tool / Group | Clean-Room (`--clean-room`) | Where used in `carea` | Verified how | Version | Status |
| --- | --- | --- | --- | --- | --- |
| `core_session_show`, `core_targets_list`, `core_target_select`, `core_target_close`, `core_evidence_show`, `core_evidence_export`, `core_evidence_import`, `core_unknowns_show`, `core_unknown_add`, `core_unknown_edit`, `core_unknown_verify`, `core_person_ask`, `core_action_approve`, `core_brief_write`, `core_finding_record`, `core_report_write`, `core_report_save` | Available (`core` toolset) | `skills/ca/`, `skills/carea/`, `skills/_shared/` | `craft-anything-cli capabilities --json` & live `craft-anything` MCP | `0.6.0` / `0.6.1` | `VERIFIED` |
| `core_target_open`, `core_archive_show`, `core_archive_extract` | **Blocked** in clean-room (Deep-only) | `skills/carea/references/modes.md` | `craft-anything-cli capabilities --json` | `0.6.0` | `VERIFIED` |
| `web_site_open`, `web_site_capture`, `web_page_states_capture`, `web_site_close`, `web_page_screenshot_take`, `web_pixels_compare`, `web_walkthrough_check` | Available (`browser` toolset) | `skills/ca/`, `skills/carea/`, `docs/workflows/` | `capabilities --json`, live MCP, `0.6.1` `docs/tools.md` | `0.6.0` / `0.6.1` | `VERIFIED` |
| `project_list`, `project_show`, `project_preview`, `project_pin_create`, `project_pin_open`, `project_pin_stop`, `project_pin_delete`, `project_assets_allow`, `project_assets_budget`, `project_build_finish` | Available (`projects` toolset) | `skills/ca/`, `modes.md` | `capabilities --json`, `0.6.1` `docs/tools.md` | `0.6.0` / `0.6.1` | `VERIFIED` |
| `rebuild_start`, `rebuild_status`, `rebuild_activity_show`, `rebuild_stop`, `rebuild_check`, `rebuild_note` | Available (`projects` / MCP) | `skills/ca/`, `modes.md`, `schemas/` | `capabilities --json`, live MCP, `0.6.1` `docs/tools.md` | `0.6.0` / `0.6.1` | `VERIFIED` |
| `build_files_list`, `build_file_read`, `build_file_write`, `build_file_edit`, `build_checklist`, `build_command_run` | Available (`build` toolset) | `skills/ca/`, `skills/carea/` | `capabilities --json` (exact 6 tools) & `0.6.1` `docs/tools.md` | `0.6.0` / `0.6.1` | `VERIFIED` |
| `native_window_capture`, `runtime_ui_read`, `runtime_walkthrough_record`, `runtime_ui_walkthrough_record`, `runtime_captures_compare` | Available (`runtime` toolset) | `modes.md`, `parity-verification.md` | `capabilities --json` & `0.6.1` `docs/tools.md` | `0.6.0` / `0.6.1` | `VERIFIED` |
| `assets_image_generate`, `assets_model_generate`, `assets_key_status` | Available (`setup`/`assets`) | `skills/ca/`, `modes.md` | `capabilities --json`, live MCP, `0.6.1` `docs/tools.md` | `0.6.0` / `0.6.1` | `VERIFIED` |
| `game_archives_list`, `game_pak_list`, `game_iostore_list`, `game_unity_list`, `game_unity_bundle_list`, `game_unity_asset_export`, `game_unreal_texture_export`, `game_pak_extract`, `game_unity_code_names_show` | **Blocked in clean-room** (**Deep-only** in `formats` toolset) | `modes.md` (Mode 5 warning) | `capabilities --json` (`reason: "This looks inside the original ... which Clean room never does."`) & `0.6.1` `docs/tools.md` | `0.6.0` / `0.6.1` | `VERIFIED` |
| `adb_devices_find`, `adb_device_show`, `adb_apps_list`, `adb_apps_find`, `adb_app_show`, `adb_app_install`, `adb_app_remove`, `adb_app_launch`, `adb_activity_open`, `adb_app_force_stop`, `adb_display_show`, `adb_window_show`, `adb_screenshot_take`, `adb_log_read`, `adb_file_download`, `adb_file_upload`, `engines_adb_check` | Available when `adb` engine is installed (Note: MCP exposes `start_adb_app` / `install_adb_package` in older/alias tables; `0.6.0` CLI & `0.6.1` docs list `adb_app_launch`, `adb_screenshot_take`, etc.) | `modes.md` (Mode 6), `intent-router` | `capabilities --json` (`adb` toolset, 24 tools) & `0.6.1` `docs/tools.md` | `0.6.0` / `0.6.1` | `VERIFIED` |

### REA (`6.10.1` schema directory + `6.8.0` live MCP)

| Tool / Group | Where used in `carea` | Verified how | Version | Status |
| --- | --- | --- | --- | --- |
| `binary_session`, `open_binary`, `close_binary`, `get_evidence_bundle`, `export_evidence_bundle`, `import_evidence_bundle`, `inspect_analysis_view`, `discover_tools` | `skills/rea/`, `skills/carea/`, `skills/_shared/` | `6.10.1` `scripts/verify/advertised-schemas/tools/` (`discover_tools` in `mcp-contracts.md`), `6.8.0` MCP | `6.10.1` (`discover_tools` `6.10.1`) | `VERIFIED` |
| `list_unknowns`, `record_unknown`, `update_unknown`, `verify_unknown_resolution` | `skills/_shared/`, `clean-room-protocol` | `6.10.1` schemas + `6.8.0` MCP | `6.10.1` / `6.8.0` | `VERIFIED` |
| `analyze_javascript_application`, `reconcile_javascript_runtime`, `trace_javascript_semantics`, `trace_application_feature`, `trace_feature`, `compare_application_versions`, `compare_javascript_export_shapes`, `build_reconstruction_obligation_ledger`, `evaluate_reconstruction_coverage`, `verify_reconstruction`, `audit_release_exposure` | `skills/rea/`, `modes.md`, `parity-verification`, `schemas/` | `6.10.1` `scripts/verify/advertised-schemas/tools/` + `6.8.0` MCP (`audit_release_exposure` verified in `6.10.1`) | `6.10.1` | `VERIFIED` |
| `inspect_web_page`, `capture_web_screenshot`, `capture_browser_scenario`, `compare_web_captures`, `compare_web_screenshots`, `inspect_web_network_capture`, `inspect_playwright_trace`, `export_environment_bundle` | `skills/rea/`, `modes.md`, `docs/workflows/` | `6.10.1` `scripts/verify/advertised-schemas/tools/` (`inspect_playwright_trace` `6.10.1`) + `6.8.0` MCP | `6.10.1` | `VERIFIED` |
| `analyze_function`, `match_native_functions`, `compare_functions`, `build_call_path`, `compare_process_captures`, `capture_process_scenario`, `compare_artifacts`, `inspect_artifact`, `extract_artifact` | `skills/rea/`, `modes.md`, `parity-verification` | `6.10.1` schemas + `6.8.0` MCP | `6.10.1` / `6.8.0` | `VERIFIED` |
| `inspect_android_package`, `search_android_classes`, `inspect_android_class`, `inspect_android_method`, `inspect_android_jni_bindings`, `decode_android_resources`, `identify_flutter_build`, `inspect_dart_aot`, `project_android_application_graph` | `modes.md` (Mode 6), `intent-router` | `6.10.1` schemas (`inspect_android_jni_bindings` `6.10.1`) + `6.8.0` MCP | `6.10.1` | `VERIFIED` |
| `inspect_uefi_firmware`, `inspect_uefi_nvram`, `extract_uefi_firmware`, `inspect_nuget_nupkg`, `inspect_maven_gradle_metadata` | `intent-router`, `docs/workflows/` | `6.10.1` `scripts/verify/advertised-schemas/tools/` (added post-`6.8.0`) | `6.10.1` | `VERIFIED` |
| `start_frida_session`, `instrument_with_frida`, `close_frida_session`, `start_gdb_session`, `close_gdb_session`, `start_rizin_debug_session`, `close_rizin_debug_session` | `skills/rea/`, `clean-room-protocol` | `6.10.1` schemas + `6.8.0` MCP | `6.10.1` / `6.8.0` | `VERIFIED` |

---

## 6. Plugin Manifest Formats (`rea-agents-6.10.1` reference)

| Claim | Where used in `carea` | Verified how | Verified version | Status |
| --- | --- | --- | --- | --- |
| `.claude-plugin/plugin.json` fields (`name`, `version`, `description`, `author`, `repository`, `license`, `keywords`, `skills`, `icon`) | `.claude-plugin/plugin.json` | Inspected `rea-agents-6.10.1` & local `6.8.0` `.claude-plugin/plugin.json` (excluding `mcpServers`, since `carea` ships no MCP server) | `6.10.1` / `6.8.0` | `VERIFIED` |
| `.codex-plugin/plugin.json` fields (`skills`, `interface.{displayName, shortDescription, longDescription, developerName, category, capabilities, defaultPrompt, composerIcon, logo}`) | `.codex-plugin/plugin.json` | Inspected `rea-agents-6.10.1` `.codex-plugin/plugin.json` | `6.10.1` | `VERIFIED` |
| `.cursor-plugin/plugin.json` fields (`name`, `version`, `description`, `author`, `repository`, `license`, `keywords`, `skills`, `logo`) | `.cursor-plugin/plugin.json` | Inspected `rea-agents-6.10.1` `.cursor-plugin/plugin.json` | `6.10.1` | `VERIFIED` |
