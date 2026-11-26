# `carea` Operational Modes (1–6) & Lane B Topologies

> **Default `/carea <target>` Behavior (v1.3.0):** Running `/carea <target>` executes **Reverse-Engineer-Only Master Mode** first: **Stage 1 (`/rea` 237+ tools) -> Stage 2 (`/ca` 1:1 observable UI study only, NO `rebuild_start`) -> Stage 3 (`full-breakdown.md` + `architecture.md` + `design-system.md`)**. The six modes below apply when running deep verification (`/rea`), airlock workflows, or explicit opt-in rebuilds.

---

## Mode Matrix Overview

| Mode ID | Name | Entry Point | Engines | Clean-Room? | Primary Purpose |
| --- | --- | --- | --- | --- | --- |
| `clean-room-ui` (Mode 1) | Clean-Room UI / Web Rebuild | `/ca` | CA `--clean-room` | Yes *(tool-level)* | Observable layout, styling, responsive & UI interaction rebuild |
| `two-team-process` (Mode 2) | Two-Team Clean Room Process | `/carea` | REA + Airlock + CA `--clean-room` | Process aid *(not legal)* | Internal logic/API contracts via spec/handoff airlock + dual parity |
| `deep-verification` (Mode 3) | Deep Investigation / Verification / AgentEnv | `/rea` | REA | N/A *(analysis only)* | Forensics, `verify_reconstruction`, capture diff, or AgentEnv export |
| `private-deep-rebuild` (Mode 4) | Private Deep Rebuild *(NOT clean-room)* | `/carea` | REA Deep + CA `--deep` | **NO** (`deep_private: true`) | Direct internal reconstruction/migration with full source/binary visibility |
| `game-rebuild` (Mode 5) | Game Rebuild Path *(Unity / Unreal / Godot)* | `/carea` / `/ca` | CA `--clean-room` *(or `--deep`)* | Only without `game_*` / `--deep` | Mechanics rebuild in Unity/Unreal/Godot/Rust |
| `android-mobile` (Mode 6) | Android / Mobile App Path | `/carea` | REA Android/Flutter + CA `adb` | Only across Airlock | Hybrid mobile APK/Flutter logic analysis + live `adb` screen parity |

---

## Lane B Topologies (`a` vs `b`): "Who Is Lane B?"

Because `craft-anything-cli rebuild` (`rebuild_start`) spawns its own coding agent inside Craft Anything, two distinct two-team topologies exist:

### Topology `(a)` — CA `rebuild`-Spawned Subprocess Agent (`topology: "a"`)

- **How it works:** One orchestrator runs `craft-anything-cli rebuild <target> "<request>" --clean-room` (or `rebuild_start` via MCP) pointing to `builder-workspace/`. Craft Anything spawns its configured `--backend` agent as Lane B.
- **Isolation mechanics:** Craft Anything's child process respects `--clean-room`, disabling internal target inspection tools (`core_target_open`, `native_*`, `js_*`, `android_*`, `game_*`).
- **Weaknesses:** Orchestrator shares prompt/session context, and child process inherits host disk permissions unless restricted at OS/container level.

### Topology `(b)` — Separate Fresh Agent Session Driving CA via MCP (`topology: "b"`) **[Stronger Separation]**

- **How it works:** Session 1 (Lane A / Analyst using REA MCP) closes completely after Stage 2 (`carea airlock-lint` + human review + `carea airlock-sign`). Lane B opens as an **entirely separate, fresh agent session** whose MCP config loads **only** `craft-anything-cli mcp --clean-room` (NO REA MCP server, NO `--all-tools`), with filesystem read access scoped to `airlock/` and read-write access scoped to `builder-workspace/`.
- **Isolation mechanics:** Context window, conversation memory, and prompt history start empty for Lane B; REA MCP tools do not exist in Lane B's tool catalog.
- **Residual channel notes:** See [`docs/threat-model.md`](../../../docs/threat-model.md) and run `carea isolation-check` before launching Lane B.

---

## Mode 1: Clean-Room UI / Web Rebuild (`clean-room-ui`)

- **When to use:** Target behavior is visible from rendered UI screens, responsive breakpoints, interactions, and public DOM/window states.
- **Prerequisites:** `craft-anything-cli` installed (`>= 0.6.0`). Run `carea doctor`.
- **Step list:**
  1. Delegate to `/ca` (`craft-anything-cli mcp --clean-room` without `--all-tools`; verify `clean_room: true` via `core_session_show`).
  2. Capture observable screens/states at `375px`, `768px`, and `1440px`: `web_site_open` -> `web_site_capture` -> `web_page_states_capture` -> `web_site_close` (or `native_window_capture` / `runtime_ui_read` for desktop).
  3. Record study findings (`core_brief_write`, `core_unknown_add`, `core_finding_record`).
  4. Build original code and replacement visuals (`rebuild_start`, `build_files_list`, `build_file_write`, `build_file_edit`, `build_command_run`, `assets_image_generate`).
  5. Run visual/walkthrough parity checks (`rebuild_check`, `web_pixels_compare`, `web_walkthrough_check`, `runtime_captures_compare`) and finalize (`project_build_finish`).
- **Parity method:** Axis 1 (CA Observable UI). Behavioral internals stay `unknown` unless covered by public tests.

---

## Mode 2: Two-Team Clean Room Process (`two-team-process`)

- **When to use:** Clean-room engineering separation where internal state machines, API shapes, IPC channels, validation math, or native logic inform an independent rebuild via sanitized spec/handoff.
- **Prerequisites:** Both `rea` (`>= 6.10.0` recommended) and `craft-anything-cli` (`>= 0.6.0`). Topology chosen (`topology: "b"` recommended).
- **Step list:**
  1. Run `carea init <project-dir> --mode two-team-process` and `carea isolation-check <project-dir>`.
  2. **Lane A (Analyst via REA):** Inspect target inside `analyst-evidence/` using `rea-master` / scoped presets; log unknowns (`record_unknown`); export bundle (`export_evidence_bundle`).
  3. **Airlock Gate:** Run `carea spec-draft`, edit `airlock/clean-room-spec.md` & `airlock/carea-handoff.json`, run `carea airlock-lint airlock/ --strict`, run `carea validate-handoff airlock/carea-handoff.json`, human review, then `carea airlock-sign airlock/carea-handoff.json --reviewer "<name>" --confirm-human-review`.
  4. **Lane B (Builder via CA `--clean-room`):** Launch under Topology `(b)` (or `(a)`), read only `airlock/`, build original code in `builder-workspace/`.
  5. **Stage 4 (Independent Verifier):** Compare outputs against CA visual checks and `analyst-evidence/` via REA verification, run `carea parity-report`, and pass sanitized failures back via `carea return-feedback`.
- **Parity method:** Dual-axis parity (`carea parity-report`): `passed` requires BOTH CA observable check AND REA behavioral verification complete for each obligation.

---

## Mode 3: Deep Investigation / Verification / AgentEnv (`deep-verification`)

- **When to use:** Full atomic static + dynamic reverse engineering of binaries, packages, crashes, firmware, protocols, security posture, cross-version diffs, formal verification, or AgentEnv export — with no UI rebuild.
- **Prerequisites:** `rea` installed with required native adapters (Ghidra/IDA/Kuna/Rizin/Frida/JADX/JEB/WABT/TShark/Sigrok where needed).
- **Step list:**
  1. Delegate to `/rea` with `rea-master` (`hot-cold` + raised limits) or `rea-all-families`.
  2. Run Layer 0–5 dissection (`inspect_byte_entropy`, `open_binary`, `inspect_artifact`, `analyze_javascript_application`, `analyze_function`, `trace_native_values`, `start_frida_session`, `start_gdb_session`, `capture_browser_scenario`).
  3. Record `unk_...` gaps (`record_unknown`) and run checks (`verify_reconstruction`, `compare_application_versions`, `find_changed_behavior`) or export (`export_evidence_bundle`, `export_environment_bundle`).
  4. Close active sessions (`close_binary`, `close_frida_session`, `close_gdb_session`, `close_rizin_debug_session`).
- **Parity method:** Axis 2 only (REA `verify_reconstruction`, `compare_*`). UI axis noted as `none`.

---

## Mode 4: Private Deep Rebuild (`private-deep-rebuild`)

> [!CAUTION]
> **MANDATORY NON-CLEAN-ROOM BANNER (Include verbatim at top of every Mode 4 spec, handoff summary, and verification output):**
>
> ```text
> ==============================================================================
> WARNING: PRIVATE DEEP REBUILD MODE — THIS WORKFLOW IS NOT CLEAN-ROOM
> Both REA Deep analysis and Craft Anything --deep were permitted to inspect
> source files, binaries, assets, and internals directly. Set deep_private: true.
> NEVER claim clean-room independence for artifacts produced in this mode.
> ==============================================================================
> ```

- **When to use:** Direct unrestricted internal reverse engineering + migration/reimplementation combining full REA Deep analysis AND CA `--deep --all-tools` (`deep_private: true`).
- **Prerequisites:** Both `rea` and `craft-anything-cli` (`carea mcp-profile carea-master` or `ca-deep-full`).
- **Step list:**
  1. Run `carea init <project-dir> --mode private-deep-rebuild` (sets `deep_private: true` in config & refuses clean-room stamps).
  2. Emit the loud **NOT CLEAN-ROOM** banner in specs, checklists, and handoff notes.
  3. Dissect target at instruction/runtime level with REA + CA `[native]`/`[formats]`/`[javascript]`/`[frida]`.
  4. Rebuild/port with `craft-anything-cli --deep` (`core_target_open`, `native_*`, `js_*`, `game_*`, `rebuild_start`).
  5. Verify with both CA checks (`rebuild_check`, `web_pixels_compare`, `web_walkthrough_check`) and REA checks (`verify_reconstruction`, `compare_*`), generating merged `verification/parity-checklist.md`.

---

## Mode 5: Game Rebuild Path (`game-rebuild`)

- **When to use:** Rebuilding game mechanics, physics/tick loops, rendering HUDs, or playable scenes in Unity, Unreal Engine, Godot, or Rust via Craft Anything (`--build-with <unity|unreal|godot|rust>`), optionally informed by REA (`inspect_il2cpp_metadata`, `inspect_artifact`) and CA `game_*` tools (`--deep`).
- **Note on Clean-Room vs `--deep`:** Clean-room (`--clean-room`) disables `formats/game_*` (`game_archives_list`, `game_pak_list`, `game_unity_*`, `game_unreal_texture_export`) and relies on observable frame captures + `assets_image_generate` / `assets_model_generate`. Running `game_*` extraction tools requires `--deep` (Mode 4 `deep_private: true` if building from internals).
- **Exact tools:**
  - CA Observable/Build: `rebuild_start --build-with ...`, `rebuild_check`, `native_window_capture`, `runtime_walkthrough_record`, `runtime_captures_compare`, `assets_image_generate`, `assets_model_generate`, `project_assets_allow`, `project_assets_budget`, `build_*`.
  - CA Deep-only: `game_archives_list`, `game_pak_list`, `game_iostore_list`, `game_unity_list`, `game_unity_bundle_list`, `game_unity_asset_export`, `game_unreal_texture_export`, `game_pak_extract`, `game_unity_code_names_show`.
  - REA Analyst: `inspect_artifact`, `extract_artifact`, `inspect_il2cpp_metadata`, `inspect_managed_artifact`, `inspect_binary_layout`, `open_binary`.

---

## Mode 6: Android / Mobile App Path (`android-mobile`)

- **When to use:** Full Android APK / Kotlin / Java / JNI / Flutter Dart AOT / JEB reverse engineering paired with `adb` live UI verification & rebuild.
- **Step list:**
  1. `carea init <project-dir> --mode android-mobile` + `carea isolation-check <project-dir>`.
  2. **Stage 1 REA:** `inspect_android_package`, `inspect_apk_signature`, `decode_android_resources`, `search_android_classes`, `inspect_android_class`, `inspect_android_method`, `inspect_android_jni_bindings`, `trace_android_references`, `identify_flutter_build`, `inspect_dart_aot`, `open_jeb_project`, `decompile_jeb_item`, `project_android_application_graph`, `export_evidence_bundle`.
  3. **Airlock Gate (for clean-room Mode 2) OR `deep_private: true` (for direct rebuild).**
  4. **Stage 2 CA `adb` & UI:** `engines_adb_check`, `adb_devices_find`, `adb_app_launch`, `adb_display_show`, `adb_window_show`, `adb_screenshot_take`, `adb_log_read`, `adb_app_force_stop` (plus `android_jeb_*`, `android_flutter_identify` under `--deep`).
  5. **Verification:** Compare device/UI captures (`runtime_captures_compare`) + API/logic (`verify_reconstruction`, `compare_web_captures`), merge via `carea parity-report`.
