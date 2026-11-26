# Sanitized Behavioral Specification

> **Airlock Notice:** This template is a process aid for the `carea` Two-Team Clean Room workflow — **not legal advice or a legal clean-room guarantee**.
> **Analyst Rule:** Describe ONLY observable behavior, abstract data contracts, math/domain rules, state transitions, and deterministic test vectors. **NEVER include original source code, decompiled pseudocode, disassembly, CSS/DOM dumps, secrets, `analyst-evidence/` paths, logos, media assets, or copyrighted copy.**
> **Private Deep Mode Notice:** If using Mode 4 (`private-deep-rebuild`, `deep_private: true`), replace the Airlock Notice above with the loud `NOT CLEAN-ROOM` banner from `skills/carea/references/modes.md`.

- **Project Name:** `<project-name>`
- **Mode & Topology:** `<two-team-process | game-rebuild | android-mobile>` (`topology: <a | b>`)
- **Target Kind:** `<web-app | electron-app | cli-tool | native-binary | managed-assembly | android-apk | game | firmware | bundle | other>`
- **Target Stack for Rebuild:** `<user-chosen stack>`
- **Handoff Record:** `airlock/carea-handoff.json` (`schema_version: 1.1.0`)
- **Authorized Scope:** `<owned / explicitly authorized target>`

---

## 1. Scope & Non-Goals

- **In Scope:**
  - `<Feature / capability 1>`
  - `<Feature / capability 2>`
- **Explicitly Out of Scope / Excluded:**
  - `<Any auth/DRM/proprietary brand assets/unobserved areas>`

---

## 2. Observable User Flows & UI States

*(Describe screen architecture, navigation structure, responsive breakpoints such as `375px` mobile and `1440px` desktop, loading/empty/error states, and accessibility behavior in plain English — without copying target prose, SVG paths, or brand tokens.)*

1. **Flow 1 (`obl_...`):** `<Step-by-step user interaction and expected visual/state change>`
2. **Visual Asset Plan:** `<Describe original replacement icons/imagery to generate via assets_image_generate / assets_model_generate or author cleanly>`

---

## 3. Data Contracts & API Shapes (Value-Free)

*(Use abstract schemas only — never copy captured credentials, tokens, cookies, or proprietary payloads.)*

### Contract `<name>` (`obl_...`)
- **Trigger / Transport:** `<HTTP method + route pattern / IPC channel name / CLI subcommand>`
- **Input Shape:** `<Field names, types, validation bounds, defaults>`
- **Output Shape:** `<Success response structure and error status conditions>`

---

## 4. State Machines & Domain / Algorithmic Rules

*(Express rules mathematically or as state tables rather than pseudocode or disassembly.)*

| Current State | Event / Input | Guard Condition | Next State | Observable Side Effect |
| --- | --- | --- | --- | --- |
| `<state_a>` | `<event>` | `<condition>` | `<state_b>` | `<effect>` |

### Domain Formulas & Edge Cases (`obl_...`)
- `<Formula or deterministic rounding/clamping/validation rule>`
- `<Boundary behavior: empty input, overflow, timeout, malformed file>`

---

## 5. Open Unknowns (Do Not Guess)

*(List any behavior REA could not observe statically or dynamically. Builder must either ask the user or document an original design decision.)*

- `unk_01`: `<What remains unknown and why>`

---

## 6. Deterministic Acceptance Test Vectors

| Test ID | Obligation | Input | Expected Outcome |
| --- | --- | --- | --- |
| `test_01` | `obl_...` | `<sanitized input>` | `<exact expected output / state / exit code>` |

---

## 7. Airlock Gate Before Lane B

1. Run heuristic scan: `carea airlock-lint airlock/ --strict` *(heuristic only; does not prove zero leakage)*.
2. Validate contract: `carea validate-handoff airlock/carea-handoff.json`.
3. Human review & sign-off: `carea airlock-sign airlock/carea-handoff.json --reviewer "<name>" --confirm-human-review`.
