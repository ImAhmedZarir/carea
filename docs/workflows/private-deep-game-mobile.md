# Workflow Guide: Private Deep Rebuild, Game Rebuild & Mobile Paths (Modes 4, 5 & 6)

This guide covers worked end-to-end flows for **Mode 4 (`private-deep-rebuild`)**, **Mode 5 (`game-rebuild`)**, and **Mode 6 (`android-mobile`)** using strictly self-owned targets.

---

## Mode 4: Private Deep Rebuild (`private-deep-rebuild`)

```text
==============================================================================
WARNING: PRIVATE DEEP REBUILD MODE — THIS WORKFLOW IS NOT CLEAN-ROOM
Both REA Deep analysis and Craft Anything --deep were permitted to inspect
source files, binaries, assets, and internals directly. deep_private: true.
NEVER claim clean-room independence for artifacts produced in this mode.
==============================================================================
```

Use Mode 4 only for **first-party / owned codebases or explicitly authorized migrations** (for example, migrating [`examples/sample-target/`](../../examples/sample-target/README.md) from Python+vanilla JS to another stack).

### Step-by-Step

1. **Initialize with `deep_private: true`:**
   ```bash
   carea init ./pulse-migrate --mode private-deep-rebuild --topology a --target-name pulse-timer
   ```
   Verify `airlock/clean-room-spec.md` and `verification/parity-checklist.md` contain the loud `NOT CLEAN-ROOM` banner, and `airlock/carea-handoff.json` sets `"deep_private": true`, `"clean_room_verified": false`, and `"airlock": {"status": "not_applicable", ...}`. *(Running `carea airlock-sign` in this mode intentionally fails so Mode 4 can never pose as clean-room.)*
2. **Analyze deeply with REA:** Run `analyze_javascript_application`, `open_binary`, and `export_evidence_bundle` inside `analyst-evidence/`.
3. **Rebuild directly with Craft Anything `--deep`:**
   ```bash
   carea mcp-profile ca-deep-private
   craft-anything-cli rebuild http://127.0.0.1:4173/ "Port pulse-timer cleanly preserving exact status endpoints" --deep --project-folder ./pulse-migrate/builder-workspace
   ```
4. **Verify dual parity:** Run `rebuild_check`, `web_pixels_compare`, and REA `verify_reconstruction` / `compare_web_captures`, then merge with `carea parity-report` (banner preserved in `verification/parity-checklist.md`).

---

## Mode 5: Game Rebuild Path (`game-rebuild`)

Use Mode 5 to build original game implementations in Godot, Unity, Unreal, or Rust (for example, recreating a self-owned MIT grid-drop arcade prototype).

### Mandatory Gates & Caveats
- **Authorization gate:** Own the game or hold written permission. Zero anti-cheat bypass, zero DRM/license circumvention, zero live service tampering.
- **No-Asset-Copy Rule:** Never copy or distribute extracted target sprites, textures, meshes, sounds, or shaders. Always replace visuals with original artwork (`assets_image_generate`, `assets_model_generate`) after enabling budget (`project_assets_budget`, `project_assets_allow`).
- **Deep-only `game_*` warning:** Craft Anything's `game_*` archive/asset tools (`game_archives_list`, `game_pak_list`, `game_iostore_list`, `game_unity_list`, `game_unity_bundle_list`, `game_unity_asset_export`, `game_unreal_texture_export`, `game_pak_extract`, `game_unity_code_names_show`) are **blocked in `--clean-room`** and require `--deep`. If you inspect internals directly via `--deep`, mark the project `deep_private: true` (NOT clean-room).

### Step-by-Step (Clean-Room Mechanics + Original Assets)
1. Initialize workspace: `carea init ./arcade-rebuild --mode game-rebuild --topology b --target-name grid-drop`.
2. Verify isolation: `carea isolation-check ./arcade-rebuild`.
3. **(If analyzing own binary/pack internals first):** Use REA `inspect_artifact`, `inspect_il2cpp_metadata`, and `inspect_binary_layout` in Lane A -> document purely mathematical frame/tick gravity, input, and scoring rules across Airlock -> pass `carea airlock-lint --strict` -> `carea validate-handoff` -> `carea airlock-sign`.
4. **In Lane B (`--clean-room`):** Build inside the target engine (`craft-anything-cli rebuild ... --build-with godot --clean-room --generate-assets`) and generate original art only.
5. Verify rendered frames (`native_window_capture`, `runtime_walkthrough_record`, `runtime_captures_compare`) plus deterministic simulation unit tests (`carea parity-report`).

---

## Mode 6: Android / Mobile App Path (`android-mobile`)

Use Mode 6 to analyze a self-owned Android app's APK/Flutter logic via REA and capture/verify observable UI via Craft Anything `adb` tools.

### Prerequisites
- Self-owned or authorized APK/device; Android Platform Tools (`adb`), `jadx`, `apktool`, and Java configured (`craft-anything-cli doctor` verifies `adb` readiness).

### Step-by-Step
1. Initialize and verify isolation:
   ```bash
   carea init ./notes-mobile-rebuild --mode android-mobile --topology b --target-name sample-notes
   carea isolation-check ./notes-mobile-rebuild
   ```
2. **Lane A (REA mobile families):** Apply `carea mcp-profile rea-android` (`android`, `apktool`, `jeb`, `flutter`, `frida`, `adb`, `application`, `session`). Inspect the owned APK using `inspect_android_package`, `decode_android_resources`, `search_android_classes`, `inspect_android_jni_bindings`, `identify_flutter_build`, and `inspect_dart_aot`, logging obfuscated/hardware gaps (`record_unknown`) and exporting `analyst-evidence/bundle.json`.
3. **Airlock Gate:** `carea spec-draft` -> document screen states, routes, and local storage contracts -> `carea airlock-lint --strict` -> `carea validate-handoff` -> `carea airlock-sign`.
4. **Lane B (CA observable `adb` & rebuild):** Check `engines_adb_check`, capture reference emulator UI via `adb_devices_find`, `adb_app_launch`, `adb_display_show`, `adb_window_show`, `adb_screenshot_take`, `adb_app_force_stop` (strictly `--clean-room` unless declared `deep_private: true`), and build the replacement app in `builder-workspace/`.
5. **Stage 4 Verification:** Compare observable captures (`runtime_captures_compare`, `adb_screenshot_take`) and backend/contract parity (`compare_artifacts`, `compare_web_captures`, `verify_reconstruction`) with `carea parity-report`.
