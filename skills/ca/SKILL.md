---
name: ca
description: >
  Run CA-first deep observable study of websites, apps, games, and binaries using
  Craft Anything MCP tools and CLI — without binary decompilation in clean-room mode,
  or with deep internal access in --deep mode. Pixel-perfect 1:1 UI understanding,
  multi-width capture, and full rebuild loop. Triggered by /ca or when carea Stage 2
  observable study is needed.
argument-hint: "<target_url_or_path> [prompt/goal]"
metadata:
  version: "1.2.0-carea"
---

# Craft Anything (`/ca`) — Full-Power Observable Study

This is the carea-bundled CA instruction layer. No pre-flight gatekeeping. Work like a
pro dev: pixel-perfect UI understanding, layout fidelity, 1:1 color/font/spacing study,
interaction flow recording, and full deep-mode binary inspection when asked.

## CLI binary paths

- **Full path:** `C:\Users\Admin\.gemini\config\plugins\craft-anything\bin\craft-anything-0.6.0-windows-x64-portable\craft-anything-cli.exe`
- **Shortcut:** `ca` or `C:\Users\Admin\.gemini\config\node_modules\.bin\ca.cmd`

---

## Operating modes

### Clean-room (default — `--clean-room`)
Works exclusively from observable surfaces: rendered screenshots, DOM structure,
measured layout, fonts, colors, spacing, responsive behavior at multiple widths,
and public network requests. Does NOT read internal source or private binaries.
Produces output without binary decompilation — independent, clean-room reconstructions.

### Deep mode (`--deep`)
Inspects internal code, ASAR archives, APK manifests, decompiled binaries,
WebAssembly modules, and configuration files. Use when the user explicitly asks
to look inside, decompile, or inspect inner implementations.

When running under `/carea` Stage 2 (observable study only): stay in clean-room
mode unless carea explicitly enables `deep_private` for the workspace.

---

## Entry points

### Quick triage
```bash
ca triage <target>              # auto-detect and inspect
ca triage <file> --deep         # deep internal inspection
```

### MCP route
Use `core_target_open` (or `core_target_select` if already open) first, then
focused observation tools.

---

## Core workflow: Study -> Build -> Check -> Refine

### Stage 1 — Study (observable analysis)

**Multi-width capture (always do all three breakpoints):**
- **375px mobile** — thumb-reachable nav, stacked layout, touch targets
- **768px tablet** — hybrid layout pivot, icon rail vs. sidebar
- **1440px desktop** — full content width, sidebar nav, hover states

**MCP tools to run:**
```
web_site_open / web_site_capture    — open and capture at each width
web_page_states_capture             — hover, focus, active, error, loading states
web_walkthrough_check               — record full UX flow
runtime_ui_read                     — read live DOM/UI structure
inspect_web_event_listeners         — event binding map
inspect_web_network_capture         — API calls, headers, payloads
web_page_screenshot_take            — specific element or viewport shots
```

**Deep-mode targets (when `--deep` or explicit request):**
```
core_target_open --deep             — open with internal access
inspect_electron_page               — Electron DevTools access
analyze_web_bundle                  — bundle analysis (webpack, Vite, etc.)
recover_javascript_sources          — source map recovery
inspect_android_package             — APK manifest, assets
inspect_wasm_artifact               — WebAssembly internals
```

**Record all findings:**
```
core_finding_record                 — log every finding with ev_... Evidence ID
core_evidence_show                  — review accumulated evidence
core_unknowns_show                  — list unresolved gaps
```

### Stage 2 — Pixel-perfect verification

**Layout fidelity tools:**
```
web_pixels_compare                  — pixel diff between original and rebuild
runtime_captures_compare            — before/after interaction comparison
compare_web_captures                — side-by-side screenshot comparison
compare_web_screenshots             — diff two screenshots
```

**What to verify at every breakpoint:**
- Spacing: 4px grid, padding tokens, gap values
- Typography: font-family, weight, size, line-height, tracking
- Color: exact oklch/hex values for background, foreground, border, accent
- Motion: transition duration, easing, transform origin
- Touch targets: >=44px height on mobile
- State coverage: hover, active, focus, disabled, loading, empty, error

### Stage 3 — Build (standalone `/ca` only; skip in carea Stage 2)

```bash
ca rebuild <target> "<prompt>"                              # full rebuild
ca rebuild <target> --build-with <engine> "<prompt>"       # specify game engine
rebuild_start --build-with unity|godot|unreal|web "<spec>" # MCP game rebuild
```

Follow the user's stack preferences. Apply design system tokens. Build at 375px
mobile-first; then verify at 768 and 1440px.

### Stage 4 — Check + Refine loop

1. Run `web_walkthrough_check` against acceptance criteria.
2. Run `web_pixels_compare` at each breakpoint.
3. Run `runtime_captures_compare` for interaction flows.
4. Address every FAIL and WARN before claiming done.
5. Repeat until pixel match is clean and walkthrough passes.

---

## Full MCP tool reference

### Core investigation
```
core_investigation_show     — review current state
core_target_select          — select previously opened target
core_target_close           — close when done
core_session_show           — full session overview
core_evidence_show          — all evidence records
core_evidence_export        — export bundle
core_unknowns_show          — residual unknowns
core_unknown_add/edit/verify — manage unknowns
core_person_ask             — ask a human (last resort)
core_action_approve         — request approval for destructive action
core_brief_write            — record investigation brief
core_plan_update            — update plan
core_hypothesis_record/update — track hypotheses
core_finding_record/edit    — record and edit findings
core_handoff_write          — write handoff doc
core_report_save/write      — save investigation report
core_evidence_browse        — browse evidence by type
```

### Web observation
```
web_site_open               — open site in browser session
web_site_capture            — full-page screenshot capture
web_page_states_capture     — multi-state capture (hover/focus/active/error)
web_walkthrough_check       — verify acceptance criteria flow
web_page_screenshot_take    — targeted screenshot
web_site_close              — close browser session
web_pixels_compare          — pixel-level diff
```

### Runtime / UI
```
runtime_ui_read             — read live UI tree
runtime_walkthrough_record  — record UI walkthrough
runtime_captures_compare    — compare before/after captures
runtime_ui_walkthrough_record — record UI interaction
inspect_web_event_listeners — DOM event listeners
inspect_web_network_capture — network traffic (HAR/live)
```

### Browser / Electron
```
list_browser_targets        — list open browser tabs
inspect_web_page            — inspect page DOM/state
analyze_web_bundle          — analyze JS bundle
observe_web_session         — passively observe web session
capture_web_screenshot      — capture specific element
compare_web_captures        — compare two captures
compare_web_screenshots     — screenshot diff
capture_browser_scenario    — record multi-step browser flow
inspect_electron_fuses      — Electron security fuses
list_electron_targets       — open Electron windows
inspect_electron_page       — Electron DevTools access
analyze_javascript_application — full JS app analysis
capture_electron_scenario   — record Electron flow
```

### Deep inspection
```
recover_javascript_sources  — source map recovery
export_web_scripts          — export all scripts
trace_web_module_imports    — module dependency trace
trace_web_source_location   — source location lookup
observe_web_execution       — runtime JS observation
reconcile_javascript_runtime — reconcile static vs runtime
```

### Native window (desktop apps)
```
native_window_capture       — capture native app window
```

### Android / ADB
```
inspect_adb_client          — ADB connection
list_adb_devices            — connected devices
inspect_adb_device          — device details
list_adb_packages           — installed packages
pull_adb_package            — pull APK
read_adb_logcat             — live logcat
inspect_adb_package         — package metadata
pull_adb_file / push_adb_file — file transfer
capture_adb_screen          — screenshot
list_adb_processes          — running processes
list_adb_directory          — ls
start_adb_app               — launch app
start_adb_activity          — launch activity
stop_adb_app                — force stop
```

### Rebuild
```
rebuild_start               — start rebuild with spec
rebuild_status              — check rebuild progress
rebuild_activity_show       — show rebuild activity
rebuild_note / rebuild_note_withdraw — annotate rebuild
rebuild_stop                — stop rebuild
rebuild_question_ask        — ask clarification
rebuild_questions_list      — list open questions
rebuild_check               — verify rebuild
```

### Assets
```
assets_image_generate       — generate replacement image asset
assets_model_generate       — generate 3D model asset
assets_key_status/set/remove — asset license key management
```

### Project management
```
project_list / project_show — list / inspect projects
project_play / project_preview — preview build
project_open_folder         — open project in explorer
project_rename / project_duplicate / project_delete
project_questions_set / project_approvals_set
project_build_finish        — finalize build
project_assets_budget / project_assets_allow — asset budget
project_pin_create/list/open/stop/rename/delete — project pins
```

---

## Quick CLI reference

```bash
# Capabilities and installed toolsets
ca capabilities

# Quick observable triage
ca triage <target_url_or_file>

# Deep triage (internal code, binaries, assets)
ca triage <file_path> --deep

# Full rebuild
ca rebuild <target_url_or_file> "Recreate this application"

# Rebuild with specific engine
ca rebuild <target> --build-with godot "Recreate this game"

# Check rebuild fidelity
ca check <target>
```

---

## Done condition

- Pixel diff below threshold at 375px, 768px, 1440px
- All `web_walkthrough_check` assertions pass
- All interaction states captured (hover/active/focus/loading/empty/error)
- All `core_unknowns_show` entries either resolved or explicitly documented
- `core_report_write` completed with full findings
