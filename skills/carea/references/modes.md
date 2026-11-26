# `carea` Operational Modes (1–6) & Lane B Topologies

This guide defines all six operational modes spanning **Craft Anything (`craft-anything-cli`)** and **REA (`rea`)**, plus the two isolation topologies for Lane B when running Two-Team workflows.

---

## Mode Matrix Overview

| Mode ID | Name | Entry Point | Engines | Clean-Room? | Primary Purpose |
| --- | --- | --- | --- | --- | --- |
| `clean-room-ui` (Mode 1) | Clean-Room UI / Web Rebuild | `/ca` | CA `--clean-room` | Yes *(tool-level)* | Observable layout, styling, responsive & UI interaction rebuild |
| `two-team-process` (Mode 2) | Two-Team Clean Room Process | `/carea` | REA + Airlock + CA `--clean-room` | Process aid *(not legal)* | Internal logic/API contracts via spec/handoff airlock + dual parity |
| `deep-verification` (Mode 3) | Deep Investigation / Verification / AgentEnv | `/rea` | REA | N/A *(analysis only)* | Forensics, `verify_reconstruction`, capture diff, or AgentEnv export |
| `private-deep-rebuild` (Mode 4) | Private Deep Rebuild *(NOT clean-room)* | `/carea` | REA Deep + CA `--deep` | **NO** (`deep_private: true`) | Authorized reconstruction/migration with direct internal visibility |
| `game-rebuild` (Mode 5) | Game Rebuild Path *(Unity / Unreal / Godot)* | `/carea` / `/ca` | CA `--clean-room` *(optional CA `--deep`)* | Only without `game_*` / `--deep` | Mechanics rebuild in Unity/Unreal/Godot with original generated assets |
| `android-mobile` (Mode 6) | Android / Mobile App Path | `/carea` | REA Android/Flutter + CA `adb` | Only across Airlock | Hybrid mobile APK/Flutter logic analysis + live `adb` screen parity |

---

## Lane B Topologies (`a` vs `b`): "Who Is Lane B?"

Because `craft-anything-cli rebuild` (`rebuild_start`) spawns its own coding agent inside Craft Anything, two distinct two-team topologies exist:

### Topology `(a)` — CA `rebuild`-Spawned Subprocess Agent (`topology: "a"`)

- **How it works:** One orchestrator (or analyst handoff operator) runs `craft-anything-cli rebuild <target> "<request>" --clean-room` (or `rebuild_start` via MCP) pointing to `builder-workspace/`. Craft Anything spawns its configured `--backend` agent as Lane B.
- **Isolation guarantees:** Craft Anything's child process respects `--clean-room`, disabling internal target inspection tools (`core_target_open`, `native_*`, `js_*`, `android_*`, `game_*`).
- **Weaknesses:**
  - The same parent session or terminal supplies both `<request>` and workspace access; prompt phrasing or `--continue-in` context originates with the orchestrator.
  - If `--backend` runs with unconstrained filesystem/shell access on the host, the child coding agent shares user disk permissions (`analyst-evidence/` is only protected if host permissions or container mounts block it).

### Topology `(b)` — Separate Fresh Agent Session Driving CA via MCP (`topology: "b"`) **[Stronger Separation]**

- **How it works:** Session 1 (Lane A / Analyst using REA MCP) closes completely after Stage 2 (`carea airlock-lint` + human review + `carea airlock-sign`). Lane B opens as an **entirely separate, fresh agent session** whose MCP config loads **only** `craft-anything-cli mcp --clean-room` (NO REA MCP server, NO `--all-tools`), with filesystem read access scoped to `airlock/` and read-write access scoped to `builder-workspace/`.
- **Isolation guarantees:** Context window, conversation memory, and prompt history start empty for Lane B; REA MCP tools do not exist in Lane B's tool catalog.
- **Weaknesses (Residual Risk):** `--clean-room` is still not an OS sandbox; shell access, shared OS temp/logs, clipboard, or misconfigured workspace permissions (`carea isolation-check` checks symlinks and parent/child overlap) remain residual channels summarized in [`DISCLAIMER.md`](../../../DISCLAIMER.md).

> **Which gives stronger separation?** **Topology `(b)` gives strictly stronger separation** than Topology `(a)` because Lane B's conversation context, prompt history, and MCP tool table are isolated from Session 1 and REA. Still, neither topology is a legal clean-room guarantee (`DISCLAIMER.md`).

---

## Mode 1: Clean-Room UI / Web Rebuild (`clean-room-ui`)

- **When to use:** Target behavior is fully visible from rendered UI screens, responsive breakpoints, interactions, and public DOM/window states. Internal APIs, proprietary obfuscated logic, or binaries are not needed.
- **Prerequisites:**
  - **Authorization gate:** Own or hold permission for the target UI/website.
  - `craft-anything-cli` installed (`>= 0.6.0`). Run `carea doctor`.
- **Step list:**
  1. Delegate to `/ca` (`craft-anything-cli mcp --clean-room` without `--all-tools`; verify `clean_room: true` via `core_session_show`).
  2. Capture observable screens/states: `web_site_open` -> `web_site_capture` -> `web_page_states_capture` -> `web_site_close` (or `native_window_capture` / `runtime_ui_read` for desktop).
  3. Record clean brief (`core_brief_write`, `core_unknown_add`).
  4. Build original code and replacement visuals (`rebuild_start`, `build_files_list`, `build_file_write`, `build_file_edit`, `build_command_run`, `assets_image_generate`).
  5. Run visual/walkthrough parity checks and finalize (`project_build_finish`).
- **Lane / workspace layout:** Single builder workspace (`builder-workspace/` or CA project folder `--project-folder`). No `analyst-evidence/` directory required.
- **Exact verified tools:** `core_session_show`, `core_brief_write`, `core_unknown_add`, `core_finding_record`, `web_site_open`, `web_site_capture`, `web_page_states_capture`, `web_site_close`, `web_page_screenshot_take`, `native_window_capture`, `runtime_ui_read`, `rebuild_start`, `rebuild_check`, `web_pixels_compare`, `web_walkthrough_check`, `runtime_captures_compare`, `build_files_list`, `build_file_read`, `build_file_write`, `build_file_edit`, `build_checklist`, `build_command_run`, `assets_image_generate`, `project_build_finish`.
- **Outputs:** Rebuilt application in `builder-workspace/`, CA project captures/diffs, and optional `parity-checklist.md` (marked observable UI scope only).
- **Parity method:** Axis 1 (CA Observable UI: `rebuild_check`, `web_pixels_compare`, `web_walkthrough_check`, `runtime_captures_compare`). Behavioral internals are explicitly marked `unknown` or out of scope unless public observable tests exist.
- **Known limits:** Cannot verify hidden algorithms, offline persistence internals, or unrendered error branches; `--clean-room` is a tool-level rule, not an OS sandbox.

---

## Mode 2: Two-Team Clean Room Process (`two-team-process`)

- **When to use:** Rebuilding software cleanly when internal state machines, API shapes, IPC channels, validation math, or native logic cannot be inferred from screenshots alone.
- **Prerequisites:**
  - **Authorization gate:** Authorized target only. Explicitly note Mode 2 is an **engineering process aid — NOT legal advice or a legal clean room**.
  - Both `rea` (`>= 6.10.0` recommended) and `craft-anything-cli` (`>= 0.6.0`) installed.
  - Topology chosen (`topology: "b"` recommended).
- **Step list:**
  1. Run `carea init <project-dir> --mode two-team-process` and `carea isolation-check <project-dir>`.
  2. **Lane A (Analyst via REA):** Inspect target inside `analyst-evidence/` using lean REA presets; log unknowns (`record_unknown`); export bundle (`export_evidence_bundle`).
  3. **Airlock Gate:** Run `carea spec-draft`, edit `airlock/clean-room-spec.md` & `airlock/carea-handoff.json`, run `carea airlock-lint airlock/`, run `carea validate-handoff airlock/carea-handoff.json`, human review, then `carea airlock-sign airlock/carea-handoff.json --reviewer "<name>"`.
  4. **Lane B (Builder via CA `--clean-room`):** Launch under Topology `(b)` (or `(a)`), read only `airlock/`, build original code in `builder-workspace/`.
  5. **Stage 4 (Independent Verifier):** Compare outputs against CA visual checks and `analyst-evidence/` via REA verification, run `carea parity-report`, and pass sanitized failures back via `carea return-feedback`.
- **Lane / workspace layout:** Strict 4-directory split (`analyst-evidence/`, `airlock/`, `builder-workspace/`, `verification/`).
- **Exact verified tools:**
  - CLI/gates: `carea init`, `carea isolation-check`, `carea spec-draft`, `carea airlock-lint`, `carea airlock-sign`, `carea validate-handoff`, `carea parity-report`, `carea return-feedback`.
  - REA Analyst/Verifier: `binary_session`, `open_binary`, `discover_tools`, `inspect_analysis_view`, `analyze_javascript_application`, `analyze_function`, `inspect_artifact`, `build_reconstruction_obligation_ledger`, `record_unknown`, `export_evidence_bundle`, `evaluate_reconstruction_coverage`, `verify_reconstruction`, `compare_web_captures`, `compare_functions`, `compare_artifacts`, `close_binary`.
  - CA Builder/Verifier: `core_session_show`, `rebuild_start`, `rebuild_check`, `web_pixels_compare`, `web_walkthrough_check`, `build_files_list`, `build_file_read`, `build_file_write`, `build_file_edit`, `build_checklist`, `build_command_run`, `assets_image_generate`.
- **Outputs:** `airlock/clean-room-spec.md`, `airlock/carea-handoff.json` (`airlock.audit` populated), fresh project in `builder-workspace/`, `verification/parity-checklist.md`.
- **Parity method:** Dual-axis parity (`carea parity-report`): `passed` requires BOTH CA observable check AND REA behavioral verification complete for each obligation.
- **Known limits:** Heuristic `airlock-lint` cannot guarantee zero leakage; Topology `(a)` shares initiator context; `verify_reconstruction` covers only finite declared obligations.

---

## Mode 3: Deep Investigation / Verification / AgentEnv (`deep-verification`)

- **When to use:** Studying binaries, packages, crashes, firmware, protocols, security posture, comparing releases, running formal behavioral verification, or exporting an `AgentEnv` sandbox — with **no UI rebuild**.
- **Prerequisites:**
  - **Authorization gate:** Authorized target only. Never attempt DRM/auth/anti-cheat bypass.
  - `rea` installed with required native adapters (Ghidra/Hopper/IDA/Kuna/Frida/JADX where needed).
- **Step list:**
  1. Delegate to `/rea` with `REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` or target-specific `REA_MCP_TOOL_FAMILIES`.
  2. Inspect artifacts/functions/bundles (`open_binary`, `inspect_artifact`, `analyze_javascript_application`, `analyze_function`, `capture_browser_scenario`).
  3. Record `unk_...` gaps (`record_unknown`) and run checks (`verify_reconstruction`, `compare_application_versions`, `audit_release_exposure`) or export (`export_evidence_bundle`, `export_environment_bundle`).
  4. Close active sessions (`close_binary`, `close_frida_session`).
- **Lane / workspace layout:** Single `analyst-evidence/` directory (plus optional `verification/` report). Zero `builder-workspace/`.
- **Exact verified tools:** `binary_session`, `open_binary`, `close_binary`, `get_evidence_bundle`, `export_evidence_bundle`, `export_environment_bundle`, `inspect_analysis_view`, `discover_tools`, `analyze_function`, `analyze_javascript_application`, `inspect_artifact`, `extract_artifact`, `inspect_uefi_firmware`, `inspect_uefi_nvram`, `extract_uefi_firmware`, `inspect_nuget_nupkg`, `inspect_maven_gradle_metadata`, `capture_browser_scenario`, `compare_web_captures`, `compare_artifacts`, `compare_functions`, `build_reconstruction_obligation_ledger`, `verify_reconstruction`, `audit_release_exposure`, `record_unknown`.
- **Outputs:** Exported `evidence.json` bundle (`evidence_format: 2`), `AgentEnv` bundle directory, or `parity-checklist.md` (marked REA verification scope only).
- **Parity method:** Axis 2 only (REA `verify_reconstruction`, `compare_*`). UI axis explicitly noted as not applicable (`none`).
- **Known limits:** Host missing Node `>=22` cannot run local `rea` CLI; native/dynamic findings depend on installed external adapters and test inputs.

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

- **When to use:** Migrating, refactoring, modernizing, or rebuilding **first-party / owned / explicitly licensed codebases and internal software** where clean-room independence is unnecessary and direct source/binary inspection speeds up exact migration.
- **Prerequisites:**
  - **Authorization gate (Strict):** Must confirm target is self-owned or holds explicit written permission (`deep_private: true`).
  - Both `rea` and `craft-anything-cli` installed; CA run explicitly with `--deep`.
- **Step list:**
  1. Run `carea init <project-dir> --mode private-deep-rebuild` (sets `deep_private: true` in config & refuses clean-room markers).
  2. Emit the loud **NOT CLEAN-ROOM** banner in specs, checklists, and handoff notes.
  3. Investigate target deeply with REA (`open_binary`, `analyze_function`, `analyze_javascript_application`, `export_evidence_bundle`).
  4. Run Craft Anything with `--deep` (`craft-anything-cli mcp --deep` or `craft-anything-cli rebuild <target> "<request>" --deep`) allowing `core_target_open`, `native_*`, `js_*`, etc. directly during study/porting.
  5. Verify with both CA checks (`rebuild_check`, `web_pixels_compare`, `web_walkthrough_check`) and REA checks (`verify_reconstruction`, `compare_*`), generating merged `verification/parity-checklist.md`.
- **Lane / workspace layout:** `analyst-evidence/`, `airlock/` *(contains non-clean-room engineering spec `deep_private: true` — airlock lint checks secrets/paths but clean-room claim is forbidden)*, `builder-workspace/`, `verification/`.
- **Exact verified tools:** All verified REA tools + CA `--deep` tools (`core_target_open`, `core_archive_show`, `core_archive_extract`, `web_site_capture`, `rebuild_start`, `rebuild_check`, `build_files_list`, `build_file_write`, `build_file_edit`, `build_command_run`, `web_pixels_compare`, `runtime_captures_compare`).
- **Outputs:** Engineering spec with loud banner, `carea-handoff.json` with `deep_private: true`, ported codebase in `builder-workspace/`, `parity-checklist.md`.
- **Parity method:** Dual-axis parity (`carea parity-report`), noting outputs derive from deep direct visibility (`deep_private: true`).
- **Known limits:** Outputs carry zero clean-room standing and may closely reflect original structure; never strip upstream copyright notices from forked/owned MIT/Apache inputs.

---

## Mode 5: Game Rebuild Path (`game-rebuild`)

- **When to use:** Recreating game mechanics, rendering loops, HUD layouts, or playable levels in Unity, Unreal Engine, Godot, or Rust via Craft Anything (`craft-anything-cli rebuild ... --build-with <unity|unreal|godot|rust>`), optionally informed by REA format analysis.
- **Prerequisites:**
  - **Authorization gate (Strict):** Target game must be owned, open-source, or explicitly authorized. **Zero anti-cheat bypass, zero DRM/license circumvention, zero live multiplayer tampering.**
  - **No-Asset-Copy Rule:** Original sprites, textures, meshes, shaders, music, SFX, and level art remain copyrighted by the target owner. Even when studying authorized game packs, **NEVER copy or ship extracted target assets** into the rebuilt game. Generate original replacement visuals (`assets_image_generate`, `assets_model_generate`, `project_assets_allow`) or author clean original art.
  - **Important `--deep` vs `--clean-room` caveat:** All Craft Anything `game_*` inspection/extraction tools (`game_archives_list`, `game_pak_list`, `game_iostore_list`, `game_unity_list`, `game_unity_bundle_list`, `game_unity_asset_export`, `game_unreal_texture_export`, `game_pak_extract`, `game_unity_code_names_show`) live in the `formats` toolset and are **BLOCKED in `--clean-room` mode (Deep-only)**.
- **Step list:**
  1. Choose clean-room vs authorized deep:
     - **Clean-room game rebuild:** Observe gameplay screenshots/window captures only via `/ca` (`--clean-room`).
     - **Authorized mechanics + format study:** Use REA (`inspect_artifact` for Godot PCK/UnityFS/IL2CPP `inspect_il2cpp_metadata`) in Lane A, write behavior-only rules (frame timing, physics constants, collision rules, input mappings — NO ripped asset blobs) across Airlock into `clean-room-spec.md`, OR explicitly declare `deep_private: true` (Mode 4 banner) if running `craft-anything-cli --deep` with `game_*`.
  2. Configure target engine in CA: `craft-anything-cli rebuild <target> "<goal>" --build-with <godot|unity|unreal|rust> --clean-room` (add `--generate-assets` when original assets are funded/authorized via `project_assets_budget` / `project_assets_allow`).
  3. Verify mechanics & rendered frames via `native_window_capture`, `runtime_walkthrough_record`, `runtime_captures_compare`, plus headless unit tests on physics/state-machine ticks.
- **Lane / workspace layout:** Standard 4-directory layout if pairing REA analysis with CA build (`analyst-evidence/`, `airlock/`, `builder-workspace/`, `verification/`), or single CA workspace when purely observable (`--clean-room`).
- **Exact verified tools:**
  - CA Clean-Room / Rebuild: `rebuild_start`, `rebuild_check`, `native_window_capture`, `runtime_ui_read`, `runtime_walkthrough_record`, `runtime_captures_compare`, `assets_image_generate`, `assets_model_generate`, `project_assets_allow`, `project_assets_budget`, `build_files_list`, `build_file_write`, `build_file_edit`, `build_command_run`.
  - CA Deep-only *(blocked in `--clean-room`)*: `game_archives_list`, `game_pak_list`, `game_iostore_list`, `game_unity_list`, `game_unity_bundle_list`, `game_unity_asset_export`, `game_unreal_texture_export`, `game_pak_extract`, `game_unity_code_names_show`.
  - REA *(Analyst lane)*: `inspect_artifact`, `extract_artifact`, `inspect_il2cpp_metadata`, `inspect_managed_artifact`, `inspect_binary_layout`, `open_binary`.
- **Outputs:** Engine-specific project (`builder-workspace/`), original replacement asset set, state-machine/gameplay spec, `verification/parity-checklist.md`.
- **Parity method:** Frame/window capture comparison (`native_window_capture`, `runtime_captures_compare`) + deterministic gameplay loop tests mapped to `obligations[]`.
- **Known limits:** Real-time frame timing, shaders, RNG, and physics determinism can differ across engines (`partial` parity honest unless deterministic harness passes); `assets_image_generate` / `assets_model_generate` require configured provider keys (`assets_key_status`) and budget (`project_assets_budget`).

---

## Mode 6: Android / Mobile App Path (`android-mobile`)

- **When to use:** Analyzing and cleanly reconstructing Android APKs, Kotlin/Java apps, JNI native bridges, or Flutter mobile apps by pairing **REA** mobile inspection with **Craft Anything** `adb` observable UI capture.
- **Prerequisites:**
  - **Authorization gate:** Own app, open-source APK, or explicit written permission on test device/emulator. Zero malware analysis on unsafe hosts, zero credential/token extraction, zero DRM/SafetyNet/Play Integrity bypass.
  - External mobile tools installed as needed: `adb` (Android platform tools), Java + `jadx` / `apktool`, and optional Frida (`engines_adb_check`, `craft-anything-cli doctor`, REA `inspect_adb_client` / `inspect_apktool_client`).
- **Step list:**
  1. Initialize 4-directory workspace: `carea init <project-dir> --mode android-mobile` + `carea isolation-check <project-dir>`.
  2. **Lane A (REA mobile families):** Configure `REA_MCP_TOOL_FAMILIES=android,apktool,jeb,flutter,frida,adb,application,session` (with `compact`/`off`). Inspect APK/DEX/JNI/Flutter logic (`inspect_android_package`, `decode_android_resources`, `search_android_classes`, `inspect_android_class`, `inspect_android_method`, `inspect_android_jni_bindings`, `identify_flutter_build`, `inspect_dart_aot`, `project_android_application_graph`), export evidence bundle (`export_evidence_bundle`).
  3. **Airlock Gate:** Run `carea spec-draft` -> author screen flows, navigation routes, API contracts, state machines, and unknowns -> run `carea airlock-lint` -> `carea validate-handoff` -> `carea airlock-sign`. (Or mark `deep_private: true` with Mode 4 banner if first-party internal migration.)
  4. **Lane B (CA observable `adb` & rebuild):** Check `engines_adb_check`, capture observable UI screens/logs of test app (`adb_devices_find`, `adb_app_launch`, `adb_display_show`, `adb_window_show`, `adb_screenshot_take`, `adb_log_read`, `adb_app_force_stop`), and build original target mobile/web implementation in `builder-workspace/`.
  5. **Stage 4 Verification:** Compare observable UI captures (`runtime_captures_compare` / screenshots) and API/logic contracts via REA (`verify_reconstruction`, `compare_artifacts`, `compare_web_captures`), merge with `carea parity-report`.
- **Lane / workspace layout:** `analyst-evidence/` (APKs, DEX/Flutter dumps, REA bundles), `airlock/` (navigation/state/API spec), `builder-workspace/` (new mobile/web codebase), `verification/`.
- **Exact verified tools:**
  - REA (`android`, `apktool`, `jeb`, `flutter`, `frida`, `adb`, `application`, `session`): `inspect_android_package`, `inspect_apk_signature`, `decode_android_resources`, `search_android_classes`, `inspect_android_class`, `inspect_android_method`, `inspect_android_jni_bindings`, `trace_android_references`, `identify_flutter_build`, `inspect_dart_aot`, `project_android_application_graph`, `inspect_adb_client`, `list_adb_devices`, `record_unknown`, `export_evidence_bundle`.
  - CA (`adb`, `runtime`, `build`): `engines_adb_check`, `adb_devices_find`, `adb_device_show`, `adb_apps_list`, `adb_display_show`, `adb_window_show`, `adb_screenshot_take`, `adb_log_read`, `adb_app_launch`, `adb_activity_open`, `adb_app_force_stop`, `runtime_captures_compare`, `build_files_list`, `build_file_write`, `build_file_edit`, `build_command_run`.
- **Outputs:** Sanitized mobile functional spec, `carea-handoff.json`, original rebuilt app, device UI screenshots/logs (redacted of tokens), `verification/parity-checklist.md`.
- **Parity method:** Dual axis: CA `adb_screenshot_take` + `runtime_captures_compare` for screen/navigation parity; REA `verify_reconstruction` + backend contract checks for logic parity.
- **Known limits:** Requires physical device or emulator with `adb` debugging enabled (`adb_devices_find` fails if Android platform tools are absent — confirmed in `0.6.0` `capabilities --json`); Flutter AOT / obfuscated ProGuard/R8 symbols may leave unrecovered internals in `unknown_ids`.
