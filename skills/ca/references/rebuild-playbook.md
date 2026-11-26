# Craft Anything Toolsets & Clean-Room Rebuild Playbook (`0.6.x`)

*Verified against `craft-anything-cli 0.6.0` (`322` commands, 17 toolsets) and upstream `v0.6.1` (`303` engine tools, `320` total). Remember Craft Anything is **early alpha**.*

## 1. Safe Startup Profiles

- **Clean-room MCP (default):** `craft-anything-cli mcp --clean-room` *(lists Essentials + enabled clean-room tools without `--all-tools`)*
- **Restricted shared-host MCP:** `craft-anything-cli mcp --clean-room --restricted --allow-web --allow-capture`
- **Single-shot CLI rebuild:** `craft-anything-cli rebuild <target> "<goal>" --clean-room` *(note `--backend`, `--build-with`, `--rounds`, `--project-folder`, `--existing` flags)*

## 2. Clean-Room Available vs Deep-Only Toolsets

| Toolset | Clean-Room (`--clean-room`) | Verified Representative Tools |
| --- | --- | --- |
| **`core`** | Partially available (`28/36` in `0.6.0`) | `core_session_show`, `core_targets_list`, `core_target_select`, `core_brief_write`, `core_evidence_show`, `core_unknown_add`, `core_finding_record`, `core_report_write` *(Deep-only blocked: `core_target_open`, `core_archive_show`, `core_archive_extract`)* |
| **`browser`** | Observable tools only (`7/22`) | Available: `web_site_open`, `web_site_capture`, `web_page_states_capture`, `web_site_close`, `web_page_screenshot_take`, `web_pixels_compare`, `web_walkthrough_check` |
| **`projects`** | Available (`28/29`) | `project_list`, `project_show`, `project_preview`, `project_pin_create`, `project_pin_open`, `project_pin_stop`, `project_pin_delete`, `project_assets_allow`, `project_assets_budget`, `project_build_finish`, `rebuild_start`, `rebuild_check`, `rebuild_status`, `rebuild_stop` |
| **`build`** | Fully available (`6/6`) | `build_files_list`, `build_file_read`, `build_file_write`, `build_file_edit`, `build_checklist`, `build_command_run` |
| **`runtime`** | Observable capture only (`5/14`) | `native_window_capture`, `runtime_walkthrough_record`, `runtime_captures_compare`, `runtime_ui_read`, `runtime_ui_walkthrough_record` |
| **`adb`** | Observable phone UI when `adb` installed | `engines_adb_check`, `adb_devices_find`, `adb_device_show`, `adb_display_show`, `adb_window_show`, `adb_screenshot_take`, `adb_log_read`, `adb_app_launch`, `adb_app_force_stop` |
| **`setup`** | Available (`20/20`) | `engines_list`, `assets_image_generate`, `assets_model_generate`, `assets_key_status`, `settings_show` |
| **`formats` (`game_*`), `native`, `android`, `apple`, `managed`, `java`, `javascript`, `frida`, `application`, `database`** | **Blocked in Clean-Room** (**Deep-only**) | Inspecting game paks/bundles (`game_archives_list`, `game_pak_list`, `game_unity_asset_export`, etc.) and binary/source inspection require `--deep` under explicit authorization and NEVER belong in clean-room rebuilds. |

## 3. Notes on `project-assets` & Copyright

- Replacement assets generated via `assets_image_generate` or `assets_model_generate` must use original prompts derived from your clean-room design spec — never trace or export copyrighted target sprites, logos, or textures into the new build.
- Keep `rebuild_check` honest: matching pixels or walkthrough steps confirms observable likeness only, not internal parity.
