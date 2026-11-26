# `carea` Intent Router & Context-Budget Playbook

This playbook routes multi-engine tasks between **`rea`** and **`craft-anything-cli`** while keeping exposed MCP schemas minimal (never loading all `264` REA + `303`/`320` CA schemas simultaneously).

## 1. Context Budget Presets (`carea mcp-profile <preset>`)

Use `carea mcp-profile <preset>` to inspect verified environment and CLI flag snippets:

1. **Craft Anything (`craft-anything-cli`):**
   - Default clean-room MCP: `craft-anything-cli mcp --clean-room` *(omit `--all-tools`: exposes `30` focused tools in `0.6.0` instead of `300+`)*.
   - Restricted shared-host clean-room MCP: `craft-anything-cli mcp --clean-room --restricted --allow-web --allow-capture`.
   - Deep mode (ONLY for authorized Mode 4 Private Deep Rebuild or Deep game inspection): `craft-anything-cli mcp --deep`.
2. **REA (`rea`):**
   - Dynamic discovery (`>= 6.10.0`): `REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` *(5 initial tools: `binary_session`, `open_binary`, `close_binary`, `get_evidence_bundle`, `discover_tools`; loads analysis tools on demand)*.
   - Explicit family scope: set `REA_MCP_TOOL_FAMILIES` (`19` valid IDs in `6.10.1`, see [tool-families.md](../../rea/references/tool-families.md)).
   - Schema compaction: `REA_MCP_INPUT_SCHEMA_PROFILE=compact` and `REA_MCP_OUTPUT_SCHEMA_PROFILE=off` (or `compact`). Remember: `rea >= 6.10.0` rejects `full`.

## 2. Resolving Overlapping Tool Domains

| Shared Domain | Default Owner in `carea` | Why |
| --- | --- | --- |
| **Deep binary / APK / JS / UEFI forensics & Frida** | **REA** | Evidence-authenticated static/runtime analysis, Ghidra/Hopper/IDA/Kuna/JADX/Frida bridges, `ev_...` / `unk_...` records. |
| **Observable website capture & visual pixel diff** | **CA** | Multi-width capture (`web_site_capture`, `web_page_states_capture`) and `web_pixels_compare` / `web_walkthrough_check`. |
| **Rebuild workspace, pins, previews & asset gen** | **CA** | `rebuild_start`, `project_preview`, `project_pin_create`, `project_pin_open`, `project_pin_stop`, `build_files_list`, `build_file_read`, `build_file_write`, `build_file_edit`, `build_checklist`, `build_command_run`, `assets_image_generate`, `assets_model_generate`. |
| **Android logic vs UI** | **REA** *(logic)* + **CA** *(UI)* | REA handles APK/DEX/JNI/Flutter (`inspect_android_package`, `inspect_android_jni_bindings`, `inspect_dart_aot`); CA handles `adb_screenshot_take`, `adb_window_show`, `runtime_captures_compare`. |
| **Evidence & Unknown ledgers** | **Both (lane-scoped)** | REA owns `ev_...` and `unknown` records in Analyst/Verifier lanes; CA owns clean-room evidence/unknowns inside `builder-workspace/`. `carea` links them via `carea-handoff.json`. |

## 3. Task-to-Skill & Tool Routing Table

| Task | Entry Point / Mode | Exact Verified Engine & Tools |
| --- | --- | --- |
| **Observable Website / UI Study & Rebuild** | `/ca` (Mode 1) | CA `browser`, `projects`, `build` (`web_site_open`, `web_site_capture`, `web_page_states_capture`, `web_pixels_compare`, `rebuild_start`, `rebuild_check`, `build_files_list`, `build_file_write`, `build_file_edit`, `build_command_run`) |
| **Internal Contracts + Clean Rebuild** | `/carea` (Mode 2) | REA Analyst (`REA_MCP_TOOL_FAMILIES` / `hot-cold`) -> `carea` Airlock (`spec-draft`, `airlock-lint`, `validate-handoff`, `airlock-sign`, `isolation-check`) -> CA Builder (`--clean-room`) -> Dual Parity (`carea parity-report`) |
| **Native Binary / JS / Firmware Forensics / AgentEnv** | `/rea` (Mode 3) | REA (`open_binary`, `analyze_function`, `analyze_javascript_application`, `inspect_artifact`, `inspect_uefi_firmware`, `inspect_uefi_nvram`, `extract_uefi_firmware`, `inspect_nuget_nupkg`, `inspect_maven_gradle_metadata`, `capture_browser_scenario`, `export_environment_bundle`, `verify_reconstruction`) |
| **Private Deep Rebuild (Owned / Authorized)** | `/carea` (Mode 4) | REA deep + CA `--deep` (`deep_private: true`; loud non-clean-room banner required) |
| **Game Rebuild (Unity / Unreal / Godot)** | `/carea` (Mode 5) | CA `--clean-room` (`rebuild_start --build-with`, `assets_image_generate`, `assets_model_generate`) for clean mechanics/assets; CA `--deep` (`game_archives_list`, `game_pak_list`, `game_unity_list`, etc.) ONLY if explicitly authorized — never copy proprietary assets |
| **Android / Flutter Mobile Hybrid** | `/carea` (Mode 6) | REA (`android`, `apktool`, `jeb`, `flutter`, `frida`, `application`, `session`) for logic + CA (`adb_devices_find`, `adb_screenshot_take`, `adb_window_show`, `adb_log_read`) for UI |
