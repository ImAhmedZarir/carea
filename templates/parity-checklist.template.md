# Stage 4 Parity Verification Checklist

- **Project:** `<project-name>`
- **Handoff Record:** `airlock/carea-handoff.json`
- **Builder Workspace:** `builder-workspace/` (Clean-Room verified: `<yes/no>`)
- **Verifier Session:** `<separate from Builder Lane>`

---

## 1. Pre-Verification Airlock Confirmation

- [ ] Lane A (`analyst-evidence/`) remained isolated from Lane B (`builder-workspace/`).
- [ ] `craft-anything-cli` ran in `--clean-room` mode for all Lane B build/check steps.
- [ ] Replacement visuals/copy are original or permissively licensed (zero copied target logos/media/prose).

---

## 2. Obligation Verification Matrix

| Obligation ID | Description | CA Visual / UX Check | REA Behavioral / Structural Check | Status (`passed` / `partial` / `failed` / `unknown`) | Evidence / Notes |
|---|---|---|---|---|---|
| `obl_...` | `<summary>` | `<rebuild_check / web_pixels_compare / none>` | `<verify_reconstruction / compare_process_captures / etc.>` | `<status>` | `<cite ev_... or diff notes>` |

---

## 3. Aggregate Parity Summary

- **Visual Parity (`CA`):** `<passed | partial | failed | unknown | not_applicable>`
- **Behavioral Parity (`REA`):** `<passed | partial | failed | unknown | not_applicable>`
- **Structural Parity (`REA`):** `<passed | partial | failed | unknown | not_applicable>`
- **Coverage Limitations:** `<e.g., partial static call discovery, viewport set limited to 375/768/1440>`
- **Remaining Unknowns:** `<list unresolved unk_... IDs>`
