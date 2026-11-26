# Evidence Paging, Retained References & Parity Verification (`/rea`)

How to traverse multi-megabyte analyses without blowing context limits, compare builds rigorously, and formally verify behavioral obligations.

## 1. Retained References & `inspect_analysis_view`

Whenever a producer supports `detail: "summary"`, prefer summary mode first and read specific slices via `inspect_analysis_view`:

```json
{
  "source": { "kind": "retained-evidence", "evidence_id": "ev_PARENT_ID" },
  "view": { "kind": "page", "collection": "modules", "offset": 0, "limit": 24 }
}
```

- **Supported `view.kind` selectors:**
  - `page` / `item` (`modules`) — JS/application graph nodes & semantic facts
  - `javascript-routes` (`routes`, `occurrences`, `sources`, `unknowns`) — route inventory
  - `web-bundle` (`endpoints`, `inferences`, `summary`) — extracted API endpoints
  - `inventory` (`occurrences`, `nodes`, `edges`, `integrity_contradictions`) — archive/container inventory
  - `native-inventory` (`procedures`, `names`, `strings`) — native symbol/string tables
  - `batch-decompile` (`items`, `pseudocode`) — filter by `indices`, `addresses`, ` statuses`, `include_pseudocode`
  - `go` (`string_literals`), `il2cpp` (`sections`, `images`, `types`, `methods`, `fields`, `properties`, `events`, `parameters`, `string_literals`), `model-artifact`, `desktop-application`, `browser-scenario`, `pcap`, `apk-signature`, `android-jni`, `beam`, `rust`, `function-matches`.
- **Lost Parent ID Recovery:** Call `get_evidence_bundle` with `detail: "summary"` and exact filters (operation, target SHA-256, procedure address).
- **Portable Persistence:** Export with `export_evidence_bundle` (`evidence_format: 2`) before closing session; restore later via `import_evidence_bundle` or pass `--evidence-bundle` to supported CLI commands.

## 2. Diffing & Cross-Version Forensics

Pass `{kind: "retained-evidence", evidence_id}` references rather than re-sending megabytes of JSON:

- **Native Diffing:** Retain `list_procedures` + `list_names` + `read_bytes` -> `match_native_functions` -> inspect unmatched/changed functions -> `compare_functions` (requires full `parent_evidence_id` dossiers, NOT summaries) -> aggregate via `find_changed_behavior`. Raise `native.matching_representation_bytes` via `update_analysis_settings` if refused on huge binaries.
- **JS / Web / Capture Diffing:** `compare_artifacts`, `compare_bundles`, `compare_application_versions`, `compare_javascript_export_shapes`, `compare_source_to_bundle`, `compare_wasm_interfaces`, `compare_web_captures`, `compare_web_screenshots`, `compare_process_captures`, `compare_static_and_observed_endpoints`.
- **Static <-> Runtime Correlation:** Supply explicit finding mappings across static diffs + `compare_process_captures` to `correlate_static_and_runtime`.

## 3. Obligation Ledgers, Verification & Unknowns

1. Track unverified paths honestly via `record_unknown` (`unk_...`), update via `update_unknown`, audit via `audit_residual_unknowns`, close with observed evidence via `verify_unknown_resolution`.
2. Build obligation ledgers via `build_reconstruction_obligation_ledger` -> check coverage via `evaluate_reconstruction_coverage` -> evaluate typed specs via `verify_reconstruction`.
3. Checkpoint before exit via `reset_investigation` with optional `save_path`.
