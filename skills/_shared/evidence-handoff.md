# Shared Evidence & Handoff Protocol

**REA** and **Craft Anything** both maintain immutable Evidence IDs and Unknown ledgers. `carea` connects them cleanly through [`schemas/carea-handoff.schema.json`](../../schemas/carea-handoff.schema.json) (`1.1.0`, backward-compatible with `1.0.0` documents) without copying raw target internals across the Airlock.

## 1. Upstream Evidence Format Notes

- **REA (`>= 6.10.0`):** Requires `evidence_format: 2`. Large results return compact summaries with `normalized_result.parent_evidence_id`; retrieve complete pages via `inspect_analysis_view` or `get_evidence_bundle` / `export_evidence_bundle`. Older `6.8.x` bundles remain `limited` and should be regenerated with `6.10.x` when building `evidence_format: 2` workflows.
- **Craft Anything (`0.6.x`):** Tracks evidence (`core_evidence_show`, `core_evidence_export`), unknowns (`core_unknowns_show`, `core_unknown_add`, `core_unknown_verify`), findings (`core_finding_record`), and walkthrough/pixel diffs inside `.cany` projects.

## 2. Field Mapping in `carea-handoff.json`

| Concept | REA Source | `carea-handoff.json` (`1.1.0`) | Craft Anything Side |
| --- | --- | --- | --- |
| **Target & Mode** | Target digest & container facts | `target_summary`, `mode`, `topology`, `tool_versions`, `deep_private` | `core_target_select` / `core_brief_write` |
| **Raw Evidence Anchors** | `ev_...` / `parent_evidence_id` / bundle SHA-256 | `analyst_lane.evidence_ids[]`, `bundle_path`, `bundle_sha256` *(IDs only cross; files stay in `analyst-evidence/`)* | Never read by `--clean-room` Lane B |
| **Unknowns / Gaps** | `record_unknown` -> `unk_...` | `analyst_lane.unknown_ids[]` | `core_unknown_add` / `core_unknown_verify` |
| **Behavioral Obligations** | `build_reconstruction_obligation_ledger` | `obligations[]` (`obligation_id`, `title`, `acceptance_criteria`, `test_vectors`, `coverage`, `limitations`) | `project_show` / `build_checklist` |
| **Visual Check Targets** | — | `obligations[].ca_check_targets[]` | `rebuild_check`, `web_pixels_compare`, `web_walkthrough_check`, `runtime_captures_compare` |
| **Verification Methods** | `verify_reconstruction`, `evaluate_reconstruction_coverage`, `compare_*` | `obligations[].rea_verification_method` | Tested against built artifacts in `builder-workspace/` |
| **Airlock Audit** | — | `airlock.status`, `airlock.audit.{lint_status, lint_hash, human_reviewer, signed_at}` | Prerequisite before Lane B launches |

## 3. Strict Invariants

1. **IDs cross, payloads stay behind:** Copy only opaque IDs (`ev_...`, `unk_...`, `obl_...`), spec summaries, and test vectors into `airlock/`. Use `carea spec-draft` to generate initial sanitized skeletons.
2. **Audit before sign-off:** Run `carea airlock-lint` + `carea validate-handoff` and obtain human review (`carea airlock-sign`) before setting `airlock.status = "passed"`.
3. **No mixed clean-room / deep-private claim:** If `deep_private: true` (or `mode: "private-deep-rebuild"`), `airlock.status` and clean-room flags must NEVER claim clean-room status. Schema validation rejects combining `deep_private: true` with a clean-room assertion.
4. **Honest coverage & unknowns:** Record per-obligation `coverage` and `limitations` explicitly so downstream parity checks do not mistake partial evidence for full equivalence.
