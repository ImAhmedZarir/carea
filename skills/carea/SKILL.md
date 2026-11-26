---
name: carea
description: Orchestrate the combined four-stage pipeline (REA deep inspection -> airlock spec/handoff -> Craft Anything rebuild -> dual behavioral + pixel parity) and route multi-engine tasks across Modes 1-6 via carea CLI gates (init, isolation-check, spec-draft, airlock-lint, airlock-sign, validate-handoff, parity-report, return-feedback). Triggered by /carea or requests needing BOTH internal analysis (REA) and clean/rebuilt output (CA), two-team airlock isolation, private deep rebuilds, game/mobile rebuilds, or automatic mode selection.
---

# carea — Craft And Reverse Engineer Everything

> *"Break It Down. Build It Better."*

`carea` is an **independent, unofficial Level-1 orchestration layer** coordinating external **REA (`rea`)** and **Craft Anything (`craft-anything-cli`)** processes across the Study -> Spec -> Clean Rebuild -> Dual Parity pipeline. Neither engine is vendored or bundled.

> Read [`../_shared/responsible-use.md`](../_shared/responsible-use.md) before starting. `carea`'s Two-Team Clean Room protocol is an **engineering process aid — NOT legal advice and NOT a legal guarantee**.

## 1. Mode Router & Single-Engine Delegation

Pick the right mode for the task using [`references/intent-router.md`](references/intent-router.md):

1. **Mode 1 — Clean-Room UI / Web Rebuild -> delegate to `/ca`:** Only observable UI/web/window behavior is needed (`craft-anything-cli` `--clean-room` only).
2. **Mode 2 — Two-Team Clean Room Process (Full `/carea` Pipeline):** Internal protocols, API shapes, state machines, or binary/JS logic must inform a fresh clean rebuild. Enforce separate directories (`analyst-evidence/`, `airlock/`, `builder-workspace/`, `verification/`), Topology B recommended (separate fresh agent session driving `craft-anything-cli mcp --clean-room`).
3. **Mode 3 — Deep Investigation / Verification / AgentEnv -> delegate to `/rea`:** Forensics, binary/JS comparison, `verify_reconstruction`, or `AgentEnv` export without rebuilding UI.
4. **Mode 4 — Private Deep Rebuild (`deep_private: true`):** User owns or holds explicit written permission to combine REA deep inspection with Craft Anything `--deep`. **NOT CLEAN-ROOM**: display the mandatory non-clean-room banner in every spec/output and never set clean-room assertions in `carea-handoff.json`.
5. **Mode 5 — Game Rebuild Path:** Building/recreating game mechanics in Unity/Unreal/Godot via CA (`--build-with`), enforcing the authorization gate, no-asset-copy rule, and noting that CA `game_*` inspection/extraction tools are **Deep-only**.
6. **Mode 6 — Android / Mobile App Path:** Hybrid REA mobile logic analysis (`android`, `apktool`, `jeb`, `flutter`, `frida`, `application`, `session`) paired with CA observable UI checks (`adb`, `adb_screenshot_take`, `adb_window_show`, `runtime_captures_compare`) across the Airlock (when clean-room) or Private Deep (when authorized Mode 4).

## 2. CLI Gates & Four-Stage Execution

Replace honor-system isolation with executable `carea` CLI checks at each boundary:

1. **Initialize & Isolate:**
   - Run `carea doctor` to check upstream binaries against `compat/matrix.json`.
   - Run `carea init <project-dir> --mode <mode>` to create `.carea/config.json`, `analyst-evidence/`, `airlock/`, `builder-workspace/`, `verification/`.
   - Run `carea isolation-check <project-dir>` before starting Lane B.
2. **Lane A (Analyst via REA -> `analyst-evidence/`):**
   - Load lean REA schemas (`REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` or target-scoped `REA_MCP_TOOL_FAMILIES` + `compact` input + `off` output).
   - Export REA bundle (`export_evidence_bundle`) into `analyst-evidence/`. Never pass raw source or payloads directly to Lane B.
3. **Airlock Gate (`airlock/`):**
   - Generate draft skeleton: `carea spec-draft analyst-evidence/bundle.json --out airlock/clean-room-spec.md`.
   - Refine `airlock/clean-room-spec.md` and `airlock/carea-handoff.json` (`1.1.0` schema).
   - Run heuristic scan + schema validation + explicit human review sign-off:
     - `carea airlock-lint airlock/` *(heuristic gate only; human review still required)*
     - `carea validate-handoff airlock/carea-handoff.json`
     - `carea airlock-sign airlock/carea-handoff.json --reviewer "<name>"`
4. **Lane B (Builder via CA -> `builder-workspace/`) & Dual Parity (`verification/`):**
   - Run Craft Anything `--clean-room` (without `--all-tools`, verifying `clean_room: true` via `core_session_show`) — or `--deep` only for authorized Mode 4 (`deep_private: true`) / explicitly authorized Deep game asset workflows.
   - Merge CA checks and REA verification with `carea parity-report` into `verification/parity-checklist.md`.
   - Pass remediation via `carea return-feedback` (failing vectors & pixel diff descriptions only).

## References

- Tool routing & context-budget table: [`references/intent-router.md`](references/intent-router.md)
- Shared Two-Team Clean Room protocol: [`../_shared/clean-room-protocol.md`](../_shared/clean-room-protocol.md)
- Shared Evidence & Handoff schema guide: [`../_shared/evidence-handoff.md`](../_shared/evidence-handoff.md)
- Shared Dual Parity guide: [`../_shared/parity-verification.md`](../_shared/parity-verification.md)
- Responsible use & non-circumvention rules: [`../_shared/responsible-use.md`](../_shared/responsible-use.md)
