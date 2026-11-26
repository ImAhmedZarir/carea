# Shared Evidence & Handoff Protocol

Both **REA** and **Craft Anything** track claims using immutable Evidence IDs and structured Unknown records. `carea` bridges them across the Airlock without leaking raw target code into the Builder Lane.

---

## 1. Upstream Evidence Format Notes

- **REA (`6.10.x` vs `6.8.x`):**
  - `REA >= 6.10.0` requires `evidence_format: 2`, replacing legacy `subject.digest`/`format`/`architecture` with explicit `subject.identity` (such as `{kind: "file", sha256}` or `{kind: "url", url, origin}`). Older `6.8.x` bundles cannot be re-imported into `6.10.x` without regenerating observations.
  - Large results return a compact summary plus `normalized_result.parent_evidence_id`; query pages with `inspect_analysis_view` or export the full session via `export_evidence_bundle`.
- **Craft Anything (`0.6.x`):**
  - Clean-Room sessions maintain evidence (`core_evidence_show`, `core_evidence_browse`, `core_evidence_export`) and open questions (`core_unknown_add`, `core_unknown_edit`, `core_unknown_verify`) inside the active project (`.cany` / `craft.json`), alongside `core_brief_write`, `core_finding_record`, and `core_handoff_write`.

---

## 2. How Records Map Across `carea-handoff.json`

`carea-handoff.json` (validated against [`../../../schemas/carea-handoff.schema.json`](../../../schemas/carea-handoff.schema.json)) serves as the single contract connecting **Lane A (Analyst)**, **Lane B (Builder)**, and **Stage 4 (Verification)**:

| Concept | REA Field / Tool | `carea-handoff.json` Field | Craft Anything Field / Tool |
|---|---|---|---|
| **Target Identity** | `subject.identity` (SHA-256 / URL / process) | `target_summary` *(non-identifying behavioral summary + opaque hash/origin)* | `core_brief_write` *(Clean-Room target URL or sanitized brief only)* |
| **Observation Provenance** | `evidence_id` (`ev_...`) + `parent_evidence_id` | `analyst_lane.evidence_ids[]` & `obligations[].source_evidence_ids[]` *(IDs only, no raw code payloads)* | Referenced indirectly; CA Clean-Room records its own observable captures (`core_evidence_show`) |
| **Unresolved Gaps** | `record_unknown` / `list_unknowns` (`unk_...`) | `analyst_lane.unknown_ids[]` & `parity_summary.unresolved_unknowns[]` | `core_unknown_add` / `core_unknown_verify` |
| **Behavioral Obligations** | `build_reconstruction_obligation_ledger` | `obligations[]` (`obligation_id`, `acceptance_criteria`, `test_vectors[]`) | `build_checklist` / `core_plan_update` |
| **Clean-Room Check Targets** | — | `obligations[].ca_check_targets[]` | `rebuild_check`, `web_pixels_compare`, `web_walkthrough_check`, `runtime_captures_compare` |
| **Parity Proof** | `verify_reconstruction` / `evaluate_reconstruction_coverage` / `compare_*` | `obligations[].rea_verification_method` & `parity_summary` | `core_finding_record` / `core_report_save` |

---

## 3. Handoff Rules (Zero Contamination)

1. **IDs Cross, Payloads Stay Behind:** `carea-handoff.json` carries opaque REA `ev_...` IDs so the Stage 4 Verifier can cross-reference the exported REA bundle in `analyst-evidence/`. Never embed decompiled code, raw script extracts, or target secrets in `carea-handoff.json`.
2. **Builder Writes Only to `builder_lane`:** In Two-Team mode, Lane B reads `clean-room-spec.md` and `obligations[]` (`title`, `acceptance_criteria`, `test_vectors[]`, `ca_check_targets[]`), then records its CA project metadata (`ca_project_id`, `clean_room_verified: true`, `ca_checks[]`) under `builder_lane`.
3. **Preserve Coverage & Limitations:** If an obligation relies on a partial REA trace or an unresolved unknown, mark it honestly rather than assuming completeness.
