# `carea` Handoff Schema Reference (`1.0.0` & `1.1.0`)

Canonical schema URL (`$id`):  
`https://raw.githubusercontent.com/ImAhmedZarir/carea/main/schemas/carea-handoff.schema.json`

Validate any handoff file with zero external dependencies using:

```bash
carea validate-handoff airlock/carea-handoff.json
```

---

## Versioning & Compatibility

`carea validate-handoff` validates both **`1.0.0`** and **`1.1.0`** documents cleanly:

- Existing `1.0.0` handoffs continue to pass without modification.
- `1.1.0` adds optional and mode-specific fields while keeping the `1.0.0` core shape intact.

## Migration Guide: `1.0.0` -> `1.1.0`

| Area | `1.0.0` | `1.1.0` Addition / Change | Notes |
| --- | --- | --- | --- |
| **`schema_version`** | `"1.0.0"` | `"1.1.0"` | Both values remain accepted by the validator. |
| **`mode`** | `clean-room-ui`, `two-team-process`, `deep-verification` | Adds `private-deep-rebuild`, `game-rebuild`, `android-mobile` | `1.0.0` rejects the new modes; upgrade `schema_version` to `"1.1.0"` to use them. |
| **`topology`** | *(none)* | `"a"` or `"b"` | Records whether Lane B uses CA's `rebuild` subprocess (`a`) or a separate MCP session (`b`). |
| **`deep_private`** | *(none)* | `boolean` (default `false`) | Must be `true` for Mode 4 (`private-deep-rebuild`). **Cannot coexist** with `clean-room-ui`, `two-team-process`, `airlock.status: "passed"`, or `builder_lane.clean_room_verified: true`. |
| **`tool_versions`** | *(none)* | `{ "rea", "ca", "carea" }` | Captures the external engine versions recorded for reproducibility. |
| **`airlock.spec_sha256` & `airlock.audit`** | Manual boolean flags (`audited_by`, `audited_at`) | Adds `spec_sha256` and `audit.{lint_status, lint_hash, human_reviewer, signed_at, linter_version}` | Populated automatically by `carea airlock-sign` after `carea airlock-lint` returns `PASS` and human review is confirmed. |
| **`obligations[]` coverage** | `status`, `notes` | Adds `coverage.{scope, notes}` and `limitations[]` | Forces `carea parity-report` to keep partial or single-axis checks honest (`partial` instead of `passed`). |
| **Target & Method enums** | Original 9 target kinds & initial methods | Adds `firmware`, `bundle` kinds; `gameplay-mechanic`, `mobile-bridge` categories; `native_window_capture`, `adb_screenshot_take`, `compare_functions`, `match_native_functions`, `build_call_path`, `compare_artifacts`, `trace_application_feature`, `trace_javascript_semantics`, `compare_web_screenshots` | Matches verified upstream tool names in `docs/upstream-facts.md`. |
