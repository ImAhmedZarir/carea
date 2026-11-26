# `carea` Intent Router, Two-Engine Breakdown & Context-Budget Playbook

This playbook configures automatic target classification for `/carea <target>`, runs **Stage 1 (`rea`) -> Stage 2 (`craft-anything-cli` study-only) -> Stage 3 (`full-breakdown.md` + `architecture.md` + `design-system.md`)**, and keeps MCP schema footprints minimal.

## 1. Stage 1 (`/rea`) -> Stage 2 (`/ca` Study-Only) Auto-Routing

| Target Input | Auto-Detected Kind | Stage 1: REA (`REA_MCP_TOOL_FAMILIES`) | Stage 2: CA Study ONLY (NO `rebuild_start`) | Stage 3 Deliverables |
| --- | --- | --- | --- | --- |
| `*.apk`, `*.aab`, Android pkg | Mobile APK / Flutter | `android,apktool,jeb,flutter,frida,adb,application,session` | `adb_devices_find`, `adb_screenshot_take`, `adb_window_show`, `adb_display_show`, `core_report_save` | `full-breakdown.md` + `architecture.md` + `design-system.md` |
| `https://...`, SPA, `*.asar` | Web / Electron App | `browser,electron,application,javascript-runtime,session` | `web_site_open`, `web_site_capture`, `web_page_states_capture`, `core_brief_write`, `core_report_save` | `full-breakdown.md` + `architecture.md` + `design-system.md` |
| `*.exe`, `*.dll`, ELF, Mach-O, `.nupkg` | Native / .NET Binary | `native,enhanced,managed,artifact,application,session` | `native_window_capture`, `runtime_ui_read`, `core_finding_record`, `core_report_save` *(skip if headless)* | `full-breakdown.md` + `architecture.md` *(+ `design-system.md` if GUI)* |
| `*.pak`, `*.pck`, Unity/Godot/Unreal | Game Target | `artifact,managed,native,session` | `native_window_capture`, `runtime_walkthrough_record`, `core_finding_record` *(no asset rip; `game_*` Deep-only)* | `full-breakdown.md` + `architecture.md` + `design-system.md` |
| `*.bin`, `*.rom`, UEFI / Firmware | Firmware / Embedded | `firmware,uefi,artifact,session,direct` | N/A *(Stage 1 REA + Stage 3 Breakdown directly)* | `full-breakdown.md` + `architecture.md` + `ev_...` / `unk_...` |

> **CRITICAL NO-BUILD GUARD:** During default `/carea <target>`, **NEVER call `rebuild_start`, `rebuild_check`, `build_file_write`, `build_file_edit`, `build_command_run`, or `project_build_finish`**. Craft Anything runs strictly for observable UI/runtime study (`core_brief_write`, `core_finding_record`, `core_report_save`).

## 2. Context Budget Presets (`carea mcp-profile <preset>`)

Never load all `264` REA + `303`/`320` CA schemas simultaneously:

1. **Stage 1 REA (`rea`):**
   - Dynamic discovery (`>= 6.10.0`): `REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` *(5 initial tools: `binary_session`, `open_binary`, `close_binary`, `get_evidence_bundle`, `discover_tools`)*.
   - Target family scoping + compaction: `REA_MCP_INPUT_SCHEMA_PROFILE=compact` and `REA_MCP_OUTPUT_SCHEMA_PROFILE=off` (`full` rejected on `>=6.10.0`).
2. **Stage 2 Craft Anything (`craft-anything-cli`):**
   - Clean-room study MCP (default): `craft-anything-cli mcp --clean-room` *(omit `--all-tools`: exposes `30` focused tools in `0.6.0`)*.
   - Restricted shared-host capture MCP: `craft-anything-cli mcp --clean-room --restricted --allow-web --allow-capture`.
   - Deep mode (only if authorized to inspect internal UI/game archives): `craft-anything-cli mcp --deep`.

## 3. Opt-In Rebuild Escalation (Explicit User Request Only)

- **UI-only rebuild requested ("clone this UI"):** Delegate to `/ca` (Mode 1).
- **Clean-room Airlock rebuild requested ("two-team clean-room rebuild"):** Run Mode 2 CLI gates (`carea init` -> `carea isolation-check` -> `carea spec-draft` -> `carea airlock-lint --strict` -> `carea validate-handoff` -> human `carea airlock-sign` -> Topology B Lane B -> `carea parity-report`).
- **Authorized direct rebuild requested ("now build/reimplement it from the breakdown"):** Run Mode 4 (`private-deep-rebuild`, `deep_private: true` with mandatory warning banner).
