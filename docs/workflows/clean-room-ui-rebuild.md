# Workflow Guide: Clean-Room UI & Web Rebuild

Use **Mode 1 (Pure Clean-Room UI / Web Rebuild)** when your goal is to rebuild a website or observable desktop UI based strictly on how it looks and behaves from the outside, with zero inspection of HTML, CSS, JavaScript bundles, or internal files.

> [!NOTE]
> Craft Anything's `--clean-room` mode is a **tool-level rule, not an OS sandbox**. Always ensure you own or have permission to study the target, and replace all original logos, photographs, illustrations, and prose with original content ([`../../DISCLAIMER.md`](../../DISCLAIMER.md)).

---

## 1. Engine & Context Setup

Run Craft Anything as an MCP server in Clean-Room mode **without** `--all-tools` so only `core` (Essentials) plus enabled toolsets are exposed:

```bash
craft-anything-cli mcp --clean-room
```

*(You do not need REA running for Mode 1 unless you later want Stage 4 capture comparison.)*

Check readiness before starting:

```bash
craft-anything-cli doctor
craft-anything-cli capabilities
```

---

## 2. Step-by-Step Execution

### Stage 1: Observe Observable Surfaces
1. Call `core_session_show` to confirm `clean_room` is active (`core_target_open` and deep inspection tools will report unavailable).
2. Open and capture the target site inside the persistent MCP session (note: one-shot CLI invocations do not keep a browser open across separate CLI commands):
   - `web_site_open` -> open the target URL.
   - `web_site_capture` -> capture observable layout, computed visual traits, and screenshots at mobile (`375px`) and desktop (`1440px`) viewports.
   - `web_page_states_capture` -> capture interactive menus, dialogs, tabs, and state transitions.
   - `web_site_close` -> close the reference browser when observation is complete.
   - *(For desktop windows instead of websites: use `native_window_capture`, `runtime_ui_read`, `runtime_walkthrough_record`, or `runtime_ui_walkthrough_record`.)*

### Stage 2: Write Project Brief & Plan
1. Summarize the observed screens, responsive breakpoints, color/type direction, and interactive states using `core_brief_write` and `core_plan_update`.
2. Record any non-observable behavior (such as backend-only validation rules) via `core_unknown_add` so the rebuild makes explicit design choices rather than guessing.

### Stage 3: Clean Rebuild Loop
1. Start or continue the project build inside a clean workspace:
   - `rebuild_start` (or CLI `craft-anything-cli rebuild <url> "<goal>" --clean-room`).
   - Or manage files directly via `build_files_list`, `build_file_write`, `build_file_edit`, `build_command_run`, and `build_checklist`.
2. Generate original replacement visuals if needed using `assets_image_generate` or `assets_model_generate` (requires user-configured `fal.ai` key checked with `assets_key_status`), or author clean vector SVGs and CSS tokens.

### Stage 4: Visual & Walkthrough Parity Check
1. Run `rebuild_check` to compare the running build against the captured reference across breakpoints and check build health.
2. Run focused checks with `web_pixels_compare` (screenshot pixel diff) and `web_walkthrough_check` (scripted UI flow checks), or `runtime_captures_compare` for desktop windows.
3. Refine layout, spacing, responsiveness, and interactive states until checks pass without copying target brand marks or assets.
