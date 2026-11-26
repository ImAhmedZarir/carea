# Stage 4 Dual-Axis Parity Verification Checklist

- **Project:** `<project-name>`
- **Mode & Topology:** `<mode>` (`topology: <a | b>`, `deep_private: <true | false>`)
- **Handoff Record:** `airlock/carea-handoff.json`
- **Builder Workspace:** `builder-workspace/` (Clean-Room verified: `<yes | no — NOT CLEAN-ROOM if deep_private=true>`)
- **Verifier Session:** `<separate from Builder Lane>`

> *(If `deep_private: true`, prepend the loud Mode 4 `NOT CLEAN-ROOM` banner here — never mark a Mode 4 artifact as clean-room.)*

---

## 1. Pre-Verification Airlock Confirmation

- [ ] `carea isolation-check` verified no symlink/overlap between `analyst-evidence/` and `builder-workspace/`.
- [ ] `carea airlock-lint` returned `PASS` and human reviewer signed `airlock/carea-handoff.json` (`carea airlock-sign`). *(N/A only in Mode 4 `deep_private: true`)*
- [ ] Craft Anything ran in `--clean-room` mode for clean-room lanes (`--deep` allowed only for explicit Mode 4 `deep_private: true`).
- [ ] Replacement visuals/copy are original or permissively licensed (zero copied target logos/media/prose).

---

## 2. Obligation Verification Matrix

*(Verdict Rule: `passed` requires BOTH CA observable check AND REA behavioral/structural check complete cleanly with zero coverage gaps.)*

| Obligation ID | Description | CA Visual / UX Check | REA Behavioral / Structural Check | Status (`passed` / `partial` / `failed` / `unknown`) | Coverage & Limitations |
| --- | --- | --- | --- | --- | --- |
| `obl_...` | `<summary>` | `<rebuild_check / web_pixels_compare / adb_screenshot_take / none>` | `<verify_reconstruction / compare_functions / compare_web_captures / none>` | `<status>` | `<complete / partial; cite ev_... or limitations>` |

---

## 3. Aggregate Parity Summary

- **Visual Parity (`CA`):** `<passed | partial | failed | unknown | not_applicable>`
- **Behavioral Parity (`REA`):** `<passed | partial | failed | unknown | not_applicable>`
- **Structural Parity (`REA`):** `<passed | partial | failed | unknown | not_applicable>`
- **Overall Parity (`carea parity-report`):** `<passed | partial | failed | unknown>`
- **Coverage Limitations:** `<e.g., partial static call discovery, viewport set limited to 375/768/1440>`
- **Remaining Unknowns:** `<list unresolved unk_... IDs>`
