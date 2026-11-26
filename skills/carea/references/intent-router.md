# `carea` Intent Router, Auto-Target Intake & Context-Budget Playbook

This playbook automatically classifies any `/carea <target>` input, routes between **`rea`** and **`craft-anything-cli`**, generates full architecture & design blueprints (`architecture.md` + `design-system.md`), and keeps exposed MCP schemas minimal.

## 1. Automatic Target Classification (`/carea <target>`)

| Target Input | Auto-Detected Kind | Default REA Families (`REA_MCP_TOOL_FAMILIES`) | Craft Anything Role | Required Blueprint Outputs |
| --- | --- | --- | --- | --- |
| `*.apk`, `*.aab`, Android pkg | Mobile APK / Flutter | `android,apktool,jeb,flutter,frida,adb,application,session` | `adb_screenshot_take`, `adb_window_show`, rebuild UI | `architecture.md` + `design-system.md` + mobile/web rebuild |
| `https://...`, SPA, `*.asar` | Web / Electron App | `browser,electron,application,javascript-runtime,session` | `web_site_open`, `web_site_capture`, `web_pixels_compare`, `rebuild_start` | `architecture.md` + `design-system.md` + rebuilt web app |
| `*.exe`, `*.dll`, ELF, Mach-O, `.nupkg` | Native / .NET Binary | `native,enhanced,managed,artifact,application,session` | `native_window_capture`, `rebuild_start` (if GUI/port) | `architecture.md` (+ `design-system.md` if GUI) + parity ledger |
| `*.pak`, `*.pck`, Unity/Godot/Unreal | Game Engine Project | `artifact,managed,native,session` | `rebuild_start --build-with <engine>`, `assets_image_generate` *(note `game_*` Deep-only)* | `architecture.md` + `design-system.md` + original replacement assets |
| `*.bin`, `*.rom`, UEFI / Firmware | Firmware / Embedded | `firmware,uefi,artifact,session,direct` | N/A (REA verification/AgentEnv) | `architecture.md` + `ev_...` / `unk_...` ledger |

## 2. Context Budget Presets (`carea mcp-profile <preset>`)

Never load all `264` REA + `303`/`320` CA schemas at once:

1. **Craft Anything (`craft-anything-cli`):**
   - Default clean-room MCP: `craft-anything-cli mcp --clean-room` *(omit `--all-tools`: advertises `30` focused tools in `0.6.0`)*.
   - Restricted shared-host clean-room MCP: `craft-anything-cli mcp --clean-room --restricted --allow-web --allow-capture`.
   - Deep mode (Default Track A owned/authorized study, Mode 4 Private Deep Rebuild, or Mode 5 `game_*`): `craft-anything-cli mcp --deep`.
2. **REA (`rea`):**
   - Dynamic discovery (`>= 6.10.0`): `REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` *(5 initial tools: `binary_session`, `open_binary`, `close_binary`, `get_evidence_bundle`, `discover_tools`)*.
   - Scoped families + compaction: `REA_MCP_INPUT_SCHEMA_PROFILE=compact` and `REA_MCP_OUTPUT_SCHEMA_PROFILE=off` (`full` rejected on `>=6.10.0`).

## 3. Resolving Overlapping Tool Domains

| Shared Domain | Default Owner in `carea` | Why |
| --- | --- | --- |
| **Deep binary / APK / JS / UEFI forensics & Frida** | **REA** | Evidence-authenticated static/runtime analysis, Ghidra/Hopper/IDA/Kuna/JADX/Frida bridges, `ev_...` / `unk_...` records. |
| **Observable website capture & visual pixel diff** | **CA** | Multi-width capture (`web_site_capture`, `web_page_states_capture`) and `web_pixels_compare` / `web_walkthrough_check`. |
| **Rebuild workspace, pins, previews & asset gen** | **CA** | `rebuild_start`, `project_preview`, `project_pin_create`, `build_files_list`, `build_file_read`, `build_file_write`, `build_file_edit`, `build_checklist`, `build_command_run`, `assets_image_generate`, `assets_model_generate`. |
| **Android logic vs UI** | **REA** *(logic)* + **CA** *(UI)* | REA handles APK/DEX/JNI/Flutter (`inspect_android_package`, `inspect_android_jni_bindings`, `inspect_dart_aot`); CA handles `adb_screenshot_take`, `adb_window_show`, `runtime_captures_compare`. |
| **Architecture & Design Synthesis** | **`carea` (`templates/`)** | Combines REA internal findings (`ev_...`, `unk_...`) and CA UI captures into `architecture.md` + `design-system.md` before or during rebuild. |

## 4. Track Decision Summary

- **Auto-Direct (`deep_private: true` unless UI-only):** Triggered automatically on `/carea <target>` for authorized reverse-engineering + full design/architecture + rebuild without clean-room gating. Always mark non-clean-room status explicitly.
- **Two-Team Airlock (`clean-room` / `two-team`):** Triggered when isolation/clean-room is requested (`Mode 2`), enforcing `carea init`, `carea isolation-check`, `carea spec-draft`, `carea airlock-lint`, human `carea airlock-sign`, Topology B fresh Lane B session, and dual `carea parity-report`.
- **Single-Engine Shortcuts:** `/ca` (`Mode 1` observable UI only) or `/rea` (`Mode 3` investigation/`AgentEnv` without rebuild).
