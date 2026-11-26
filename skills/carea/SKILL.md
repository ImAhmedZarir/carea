---
name: carea
description: Autonomous target-to-architecture and combined rebuild pipeline (/carea <target>) over external REA and Craft Anything engines. Auto-detects .apk/.aab, web URLs/.asar, .exe/.dll/binaries, or Unity/Godot/Unreal games to reverse engineer system architecture (architecture.md), UI/UX design tokens (design-system.md), and reconstructed apps via REA + CA, plus enforces the optional two-team clean-room airlock CLI gates (init, isolation-check, spec-draft, airlock-lint, airlock-sign, validate-handoff, parity-report, return-feedback) across Modes 1-6.
---

# carea — Craft And Reverse Engineer Everything

> *"Break It Down. Build It Better."*

`carea` is an **independent, unofficial Level-1 orchestration layer** coordinating external **REA (`rea`)** and **Craft Anything (`craft-anything-cli`)** processes so a single `/carea <target>` invocation can analyze an authorized target, extract its complete **architecture + UI/UX design**, and rebuild it cleanly. Neither upstream engine is vendored or bundled.

> Read [`../_shared/responsible-use.md`](../_shared/responsible-use.md) before starting: **authorized targets only**, never bypass DRM/auth/paywalls/anti-cheat/CAPTCHA, and never copy proprietary brand logos, photos, or copy. When clean-room independence is requested, remember `carea`'s airlock is an **engineering process aid — NOT legal advice**.

---

## 0. Single-Command Auto-Intake (`/carea <target>`)

When invoked as `/carea <target>` (e.g., `/carea app.apk`, `/carea https://app.example.com`, `/carea tool.exe`, `/carea ./game-dir`), **automatically classify the target and start the pipeline immediately** without stalling on unnecessary configuration questions:

| Input Pattern | Auto-Detected Target | Engines & Profiles Loaded | Mode Track |
| --- | --- | --- | --- |
| `*.apk`, `*.aab`, Android `package:` | Android / Flutter App | REA (`android,apktool,jeb,flutter,frida,application,session`) + CA `adb` UI capture | Mode 6 *(or Mode 4 Direct)* |
| `https://...`, `http://...`, SPA bundle, `*.asar` | Web / Electron App | REA (`browser,electron,application,javascript-runtime,session`) + CA web capture/rebuild | Mode 1 *(UI-only `/ca`)* or Mode 2 / 4 |
| `*.exe`, `*.dll`, `*.so`, `*.dylib`, ELF, Mach-O, `.nupkg` | Native / Managed Binary | REA (`hot-cold` / `native` / `managed`) + CA runtime/UI if GUI exists | Mode 3 (`/rea` analysis) or Mode 4 / 2 |
| `*.pak`, `*.pck`, Unity/Unreal/Godot folder | Game Project | CA `--build-with` + original generated assets (`assets_image_generate`); `game_*` only if Deep authorized | Mode 5 |
| Firmware `.bin` / `.rom` / `.fd` / UEFI | Embedded / Firmware | REA (`firmware,uefi,artifact,session,direct`) | Mode 3 (`/rea` analysis) |

See [`references/intent-router.md`](references/intent-router.md) for full tool-routing and context-budget rules.

---

## 1. Choose Execution Track (Auto-Direct vs Clean-Room Airlock)

1. **Track A — Default Autonomous Extraction & Rebuild (Owned / Authorized Direct — Modes 4 / 5 / 6):**
   Use by default when the user supplies `/carea <target>` asking to reverse engineer the full design, architecture, and rebuild/blueprint for an **owned or authorized target** without asking for a clean-room firewall:
   - Run **REA deep inspection** + **Craft Anything UI/runtime capture & rebuild** in one coordinated pass.
   - Produce three structured deliverables:
     1. **`architecture.md`** ([`../../templates/architecture-report.template.md`](../../templates/architecture-report.template.md)): entrypoints, subsystems, call/module graphs, state machines, API/IPC schemas, storage layout, `ev_...` observations, `[INFERRED]` notes, and `unk_...` gaps.
     2. **`design-system.md`** ([`../../templates/design-system.template.md`](../../templates/design-system.template.md)): screen/route inventory, layout grid, original design tokens, typography hierarchy, and 5 UI states (no copied media/logos/prose).
     3. **Rebuilt Implementation + Parity Summary**: working target implementation (`rebuild/` or `builder-workspace/`) plus CA visual checks (`rebuild_check`, `web_pixels_compare`) and REA behavioral checks (`verify_reconstruction`, `carea parity-report`).
   - Emit the **Mode 4 non-clean-room notice** (`deep_private: true`) whenever internal binaries/sources were inspected directly (`NOT CLEAN-ROOM`).

2. **Track B — Strict Two-Team Clean Room Process (Only When `clean-room` / `two-team` / `airlock` Requested — Mode 2):**
   Enforce strict separation (`analyst-evidence/`, `airlock/`, `builder-workspace/`, `verification/`) with **Topology B** recommended (separate fresh agent session driving `craft-anything-cli mcp --clean-room`) and mandatory CLI gates:
   - **Stage 1 (Setup & Isolation):** `carea doctor` -> `carea init <project-dir> --mode two-team-process` -> `carea isolation-check <project-dir>`.
   - **Stage 2 (Lane A Analyst -> REA):** Inspect with lean `REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` (or family-scoped `compact`/`off`); export `analyst-evidence/bundle.json` (`export_evidence_bundle`).
   - **Stage 3 (Airlock Gate -> `airlock/`):** `carea spec-draft` -> refine `airlock/clean-room-spec.md` & `airlock/carea-handoff.json` (`1.1.0`) -> `carea airlock-lint airlock/ --strict` -> `carea validate-handoff` -> human review -> `carea airlock-sign --reviewer "<name>" --confirm-human-review`.
   - **Stage 4 (Lane B Builder -> CA `--clean-room` & Dual Parity):** Confirm `core_session_show` (`clean_room: true`), build cleanly from `airlock/` specs only, merge checks via `carea parity-report`, and route failures back cleanly via `carea return-feedback`.

3. **Single-Engine Delegation:**
   - **UI-only observable clone** (no binary/API forensics needed) -> delegate to `/ca` (Mode 1).
   - **Forensics / `AgentEnv` / verification without rebuilding** -> delegate to `/rea` (Mode 3).

---

## References

- Auto-intake routing & context-budget table: [`references/intent-router.md`](references/intent-router.md)
- Modes 1–6 & Lane B Topologies A/B: [`references/modes.md`](references/modes.md)
- Architecture blueprint template: [`../../templates/architecture-report.template.md`](../../templates/architecture-report.template.md)
- Design system blueprint template: [`../../templates/design-system.template.md`](../../templates/design-system.template.md)
- Shared protocols: [`../_shared/clean-room-protocol.md`](../_shared/clean-room-protocol.md) · [`../_shared/evidence-handoff.md`](../_shared/evidence-handoff.md) · [`../_shared/parity-verification.md`](../_shared/parity-verification.md) · [`../_shared/responsible-use.md`](../_shared/responsible-use.md)
