# Workflow Guide: Clean-Room UI Rebuild (Mode 1)

Use **Mode 1 (`clean-room-ui` -> `/ca`)** when observable layouts, responsive breakpoints, visual hierarchy, and public interactions provide enough specification to build an original UI cleanly.

> **Scope & Authorization Notice:** This walkthrough uses `carea`'s own self-owned MIT sample application ([`examples/sample-target/`](../../examples/sample-target/README.md)). Craft Anything's `--clean-room` mode is a **tool-level rule, not an OS sandbox or legal clean room** (`DISCLAIMER.md`).

---

## 1. Start the Self-Owned Sample Target

```bash
python examples/sample-target/server.py --port 4173
```

## 2. Configure & Verify Lean Craft Anything MCP (`--clean-room`)

Run Craft Anything **without** `--all-tools` so context exposes only focused clean-room toolsets:

```bash
carea doctor
craft-anything-cli doctor
craft-anything-cli mcp --clean-room
```

Or generate/merge the profile snippet cleanly with:

```bash
carea mcp-profile ca-clean-room
```

## 3. Capture Observable UI (Stage 1)

1. Confirm `clean_room: true` by calling `core_session_show`.
2. Open the local sample URL with `web_site_open` (`http://127.0.0.1:4173/`).
3. Capture layouts and screenshots at mobile (`375px`) and desktop (`1440px`) viewports via `web_site_capture`.
4. Capture Start/Pause/Reset and preset (`5m`, `10m`) DOM transitions via `web_page_states_capture`.
5. Close the browser session cleanly with `web_site_close`.

## 4. Clean Spec & Build Loop (Stage 3)

1. Summarize layout, controls (`>= 44px`), tabular digits, and interaction states via `core_brief_write` and log missing behavior via `core_unknown_add`.
2. Initialize a fresh build workspace inside `builder-workspace/` and run `rebuild_start` (or `craft-anything-cli rebuild http://127.0.0.1:4173/ "Build an accessible responsive countdown timer matching the clean brief" --clean-room`) or author files cleanly with `build_files_list`, `build_file_read`, `build_file_write`, `build_file_edit`, `build_checklist`, and `build_command_run`.
3. Create original replacement icons/styles (`assets_image_generate` or inline SVG) rather than reusing target files.

## 5. Visual Parity Check & Honest Scope

Run `rebuild_check`, `web_pixels_compare`, and `web_walkthrough_check`, then record outcomes with `carea parity-report`. Because Mode 1 runs Craft Anything only without REA behavioral proof, `carea parity-report` records UI likeness while internal parity remains `not_applicable` / `unknown` (never claiming full equivalence).
