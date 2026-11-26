---
name: carea
description: >
  Orchestrate REA and Craft Anything through a phase-based workflow: Observe /
  Reverse-engineer -> Spec + Obligation Ledger -> Clean rebuild -> Visual +
  Behavioral + Binary parity check. Triggered by /carea or when asked to study,
  reverse-engineer, cleanly rebuild, or parity-verify apps, websites, binaries,
  or agent environments without flooding agent context.
argument-hint: "<target_url_or_path> [goal]"
metadata:
  version: "0.1.0"
---

# carea — Craft And Reverse Engineer Everything

> *"Break It Down. Build It Better."*

`carea` coordinates two independent external engines through their CLI and MCP interfaces:

- **REA (`rea`)** for deep static/runtime reverse engineering, evidence/unknown tracking, parity verification, and AgentEnv export.
- **Craft Anything (`craft-anything-cli` / `ca`)** for observable web/app capture, clean-room rebuild loops, visual pixel comparison, and original asset generation.

Do **not** load full tool catalogs from both servers at once. Keep active schemas minimal using the phase-based presets in [intent-router.md](references/intent-router.md).

---

## 1. Responsible Use & Clean-Room Notice

Before inspecting any target, confirm the user owns or has explicit authorization to examine it (see [DISCLAIMER.md](../../DISCLAIMER.md)).

- **Refuse outright:** DRM, license, authentication, anti-cheat, or CAPTCHA/bot-check circumvention; game cheats; tampering with live services; or copying logos, photos, illustrations, or copyrighted prose without permission.
- **Clean-room disclaimer:** `carea`'s Two-Team Clean Room protocol is an **engineering process aid — NOT legal advice and NOT a legal clean-room guarantee**. Craft Anything's `--clean-room` flag is a **tool-level rule, not an OS sandbox**, and **a single person or agent acting as both Analyst and Builder does not create a true legal clean room**.

---

## 2. Select Operating Mode

Choose one mode before running any tool:

1. **Pure Clean-Room UI / Web Rebuild (`ca`-first):**
   Target is a website or visible UI where layout, style, and public behavior suffice. Run `craft-anything-cli` in `--clean-room` mode only; do not invoke REA deep inspection tools.
2. **Two-Team Clean Room Process (REA Analyst -> Airlock -> CA Builder):**
   Target requires understanding internal protocols, logic, state machines, or binary/JS structures before rebuilding cleanly. Enforce the workspace and context split in [clean-room-protocol.md](references/clean-room-protocol.md).
3. **Deep Investigation / Reconstruction Verification / AgentEnv (`rea`-first):**
   User wants binary forensics, runtime tracing, security/compatibility auditing, exact functional parity verification, or an AgentEnv RL bundle (no clean-room rebuild claim).

---

## 3. Four-Stage Workflow

### Stage 1: Observe / Reverse-Engineer
- Route by target type using [intent-router.md](references/intent-router.md).
- Start narrow: use summary-first calls (`detail: "summary"` + `inspect_analysis_view` in REA; `core_session_show` / clean-room captures in CA) rather than dumping full payloads.
- Close opened native REA sessions (`close_binary`) once observations are exported (`export_evidence_bundle`).

### Stage 2: Spec + Obligation Ledger
- For rebuild workflows, draft the sanitized functional spec from [clean-room-spec.template.md](../../templates/clean-room-spec.template.md) and record the handoff mapping against [carea-handoff.schema.json](../../schemas/carea-handoff.schema.json).
- Follow [evidence-handoff.md](references/evidence-handoff.md) so REA `ev_...` IDs and `unknown` IDs map to verifiable obligations (`obl_...`) without exposing raw source code, pseudocode, or original media assets across the Airlock.

### Stage 3: Clean Rebuild
- In Two-Team mode, open a **fresh agent conversation** and clean `builder-workspace/` strictly bounded to the sanitized spec, handoff JSON, and observable CA captures.
- Run `craft-anything-cli` with `--clean-room` (and without `--all-tools`). Verify via `core_session_show` that Clean Room is active.
- Build original code and replacement assets (`assets_image_generate` or original SVGs/styles) via CA's Study -> Build -> Check -> Refine loop (`rebuild_start`, `build_*`, `rebuild_check`).

### Stage 4: Visual + Behavioral + Binary Parity Check
- Verify rebuild parity using [parity-verification.md](references/parity-verification.md) and record results in [parity-checklist.template.md](../../templates/parity-checklist.template.md).
- **Evidence discipline:** Clearly separate direct observations, inferences, and unresolved `unknown`s. Never present static inspection as runtime execution, and never present partial coverage as complete equivalence.

---

## 4. Reference Map

- **Routing & context-budget rules:** [references/intent-router.md](references/intent-router.md)
- **Two-Team Airlock rules:** [references/clean-room-protocol.md](references/clean-room-protocol.md)
- **Evidence ID & schema mapping:** [references/evidence-handoff.md](references/evidence-handoff.md)
- **Dual-axis parity verification:** [references/parity-verification.md](references/parity-verification.md)
