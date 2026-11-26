---
name: ca
description: Run Craft Anything-first observable study and clean-room UI/app/game rebuilding via external craft-anything-cli (--clean-room default). Triggered by /ca or tasks asking to capture observable web/window/Android UI screens, generate original replacement assets, and run rebuild_start / rebuild_check / web_pixels_compare / web_walkthrough_check WITHOUT binary decompilation, disassembly, Frida, or internal source analysis. Hand off to /carea when hidden protocols, binary logic, or two-team airlock specs are required.
---

# `/ca` — Craft Anything-First Observable Study & Clean Rebuild

Use this entry point when observable UI, layout, responsive breakpoints, interactions, and public API behavior provide everything needed to build a clean implementation via **Craft Anything (`craft-anything-cli`)**.

> Read [`../_shared/responsible-use.md`](../_shared/responsible-use.md) first: obtain target authorization, never copy upstream brand assets or prose, and treat `--clean-room` as a **tool-level rule — NOT a legal clean-room guarantee or OS sandbox**.

## When to Stay Here vs Delegate

- **Stay in `/ca`:** Rebuilding websites, UI screens, interactive web flows, desktop window layouts, or original games from observable screenshots, DOM/runtime UI states, and clean-room briefs, including `rebuild_check`, `web_pixels_compare`, `web_walkthrough_check`, `runtime_captures_compare`, and original `assets_image_generate` / `assets_model_generate` creation.
- **Delegate to `/rea`:** Deep binary, bytecode, APK, obfuscated JS, or AgentEnv investigation without building a new app.
- **Delegate to `/carea`:** Reconstructing internal logic, state machines, protocols, or binary behavior via an REA -> Airlock -> CA pipeline, Private Deep Rebuild (Mode 4), Game Rebuild with Deep checks (Mode 5), or Mobile hybrid logic+UI rebuild (Mode 6).

## Clean-Room & Context Discipline

1. **Always check mode at session start:** Run `core_session_show` and confirm `clean_room: true` unless the user explicitly requested authorized Deep mode.
2. **Avoid `--all-tools`:** Run `craft-anything-cli mcp --clean-room` without `--all-tools` (`0.6.0` advertises 30 focused tools cleanly instead of flooding context).
3. **Never touch internals in clean-room runs:** Clean-room mode intentionally blocks `core_target_open`, `native_*`, `android_*`, `apple_*`, `js_*`, `frida_*`, `game_*`, etc. If blocked tools are required, escalate to `/carea` (Mode 2 Two-Team Clean Room or Mode 4 Private Deep Rebuild).

## Standard Execution Loop

1. **Capture Observable UI:**
   - Websites: `web_site_open` -> `web_site_capture` (mobile & desktop widths) -> `web_page_states_capture` -> `web_site_close`.
   - Desktop runtime: `native_window_capture`, `runtime_ui_read`, `runtime_walkthrough_record`.
   - Android observable screen: `adb_devices_find`, `adb_screenshot_take`, `adb_window_show`, `adb_display_show`.
2. **Record Clean Spec & Project:** Summarize observed layout, interactions, and unknowns using `core_brief_write`, `core_finding_record`, and `core_unknown_add`.
3. **Build Original Code & Assets:** Run `rebuild_start` (or CLI `craft-anything-cli rebuild <url> "<goal>" --clean-room`) or build directly with `build_files_list`, `build_file_read`, `build_file_write`, `build_file_edit`, `build_checklist`, `build_command_run`, generating original visual assets (`assets_image_generate`, `assets_model_generate` when authorized & budgeted).
4. **Verify Visual & Walkthrough Parity:** Run `rebuild_check`, `web_pixels_compare`, `web_walkthrough_check`, `runtime_captures_compare`, and fix mismatches cleanly before finishing (`project_build_finish`).

## References

- Verified toolsets and clean-room vs deep availability: [`references/rebuild-playbook.md`](references/rebuild-playbook.md)
- Parity axes & verdicts: [`../_shared/parity-verification.md`](../_shared/parity-verification.md)
- Authorization & non-circumvention rules: [`../_shared/responsible-use.md`](../_shared/responsible-use.md)
