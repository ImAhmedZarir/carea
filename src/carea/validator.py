"""Zero-dependency validator for carea-handoff.json (v1.0.0 and v1.1.0)."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any


MODES_V1_0 = {"clean-room-ui", "two-team-process", "deep-verification"}
MODES_V1_1 = MODES_V1_0 | {"private-deep-rebuild", "game-rebuild", "android-mobile"}
SUPPORTED_SCHEMA_VERSIONS = {"1.0.0", "1.1.0"}

SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
OBLIGATION_ID_RE = re.compile(r"^obl_[a-z0-9_-]+$")
EVIDENCE_ID_RE = re.compile(r"^ev_[A-Za-z0-9_-]+$")

TARGET_KINDS_V1_0 = {
    "website",
    "web-app",
    "electron-app",
    "native-binary",
    "cli-tool",
    "managed-assembly",
    "android-apk",
    "game",
    "other",
}
TARGET_KINDS_V1_1 = TARGET_KINDS_V1_0 | {"firmware", "bundle"}

CATEGORIES_V1_0 = {
    "ui-layout",
    "user-flow",
    "api-contract",
    "state-machine",
    "algorithm-logic",
    "cli-behavior",
    "storage-schema",
    "security-boundary",
}
CATEGORIES_V1_1 = CATEGORIES_V1_0 | {"gameplay-mechanic", "mobile-bridge"}

CA_CHECK_TARGETS_V1_0 = {
    "rebuild_check",
    "web_pixels_compare",
    "web_walkthrough_check",
    "runtime_captures_compare",
    "none",
}
CA_CHECK_TARGETS_V1_1 = CA_CHECK_TARGETS_V1_0 | {
    "native_window_capture",
    "adb_screenshot_take",
}

REA_METHODS_V1_0 = {
    "verify_reconstruction",
    "evaluate_reconstruction_coverage",
    "compare_source_to_bundle",
    "compare_javascript_export_shapes",
    "compare_managed_members",
    "compare_process_captures",
    "compare_web_captures",
    "compare_wasm_interfaces",
    "correlate_static_and_runtime",
    "manual-test-vector",
    "none",
}
REA_METHODS_V1_1 = REA_METHODS_V1_0 | {
    "compare_web_screenshots",
    "compare_functions",
    "match_native_functions",
    "build_call_path",
    "compare_artifacts",
    "trace_application_feature",
    "trace_javascript_semantics",
}


def _is_valid_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    candidate = value.replace("Z", "+00:00")
    try:
        datetime.fromisoformat(candidate)
        return "T" in value or "t" in value
    except ValueError:
        return False


def _check_str(
    obj: dict[str, Any],
    key: str,
    path: str,
    errors: list[str],
    *,
    min_len: int = 0,
    pattern: re.Pattern[str] | None = None,
    enum: set[str] | None = None,
    required: bool = False,
) -> None:
    if key not in obj:
        if required:
            errors.append(f"{path}.{key}: missing required field")
        return
    val = obj[key]
    if not isinstance(val, str):
        errors.append(f"{path}.{key}: expected string, got {type(val).__name__}")
        return
    if len(val) < min_len:
        errors.append(f"{path}.{key}: string shorter than minLength {min_len}")
    if pattern is not None and not pattern.match(val):
        errors.append(f"{path}.{key}: value {val!r} does not match pattern {pattern.pattern}")
    if enum is not None and val not in enum:
        errors.append(f"{path}.{key}: value {val!r} not in {sorted(enum)}")


def validate_handoff_data(data: Any) -> list[str]:
    """Validate a handoff object against schema_version 1.0.0 or 1.1.0. Returns list of errors."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root: handoff document must be a JSON object"]

    schema_ver = data.get("schema_version")
    is_v1_0 = schema_ver == "1.0.0"

    allowed_root = {
        "$schema",
        "schema_version",
        "project",
        "mode",
        "airlock",
        "target_summary",
        "analyst_lane",
        "obligations",
        "builder_lane",
        "parity_summary",
    }
    if not is_v1_0:
        allowed_root |= {"topology", "deep_private", "tool_versions"}

    for k in data:
        if k not in allowed_root:
            errors.append(f"root: unexpected property {k!r}")

    for req in (
        "schema_version",
        "project",
        "mode",
        "airlock",
        "target_summary",
        "analyst_lane",
        "obligations",
        "builder_lane",
        "parity_summary",
    ):
        if req not in data:
            errors.append(f"root.{req}: missing required field")

    if schema_ver is not None and schema_ver not in SUPPORTED_SCHEMA_VERSIONS:
        errors.append(
            f"root.schema_version: unsupported {schema_ver!r} (supported: {sorted(SUPPORTED_SCHEMA_VERSIONS)})"
        )

    # project
    proj = data.get("project")
    if proj is not None:
        if not isinstance(proj, dict):
            errors.append("root.project: expected object")
        else:
            for k in proj:
                if k not in {"name", "description", "created_at", "authorized"}:
                    errors.append(f"root.project: unexpected property {k!r}")
            _check_str(proj, "name", "root.project", errors, min_len=1, required=True)
            _check_str(proj, "description", "root.project", errors)
            if "created_at" not in proj or not _is_valid_datetime(proj["created_at"]):
                errors.append("root.project.created_at: required ISO-8601 date-time string")
            if proj.get("authorized") is not True:
                errors.append("root.project.authorized: must be boolean true")

    valid_modes = MODES_V1_0 if is_v1_0 else MODES_V1_1
    mode = data.get("mode")
    _check_str(data, "mode", "root", errors, enum=valid_modes)

    if "topology" in data and data["topology"] not in ("a", "b"):
        errors.append(f"root.topology: must be 'a' or 'b', got {data['topology']!r}")

    deep_private = data.get("deep_private", False)
    if "deep_private" in data and not isinstance(deep_private, bool):
        errors.append("root.deep_private: expected boolean")

    if "tool_versions" in data:
        tv = data["tool_versions"]
        if not isinstance(tv, dict):
            errors.append("root.tool_versions: expected object")
        else:
            for k in tv:
                if k not in {"rea", "ca", "carea"}:
                    errors.append(f"root.tool_versions: unexpected property {k!r}")
                elif tv[k] is not None and not isinstance(tv[k], str):
                    errors.append(f"root.tool_versions.{k}: expected string or null")

    # airlock
    airlock = data.get("airlock")
    airlock_status = None
    if airlock is not None:
        if not isinstance(airlock, dict):
            errors.append("root.airlock: expected object")
        else:
            allowed_air = {
                "status",
                "audited_by",
                "audited_at",
                "no_source_code",
                "no_proprietary_assets",
                "separate_builder_context",
                "spec_path",
                "disclaimer_acknowledged",
            }
            if not is_v1_0:
                allowed_air |= {"spec_sha256", "audit"}
            for k in airlock:
                if k not in allowed_air:
                    errors.append(f"root.airlock: unexpected property {k!r}")
            for req in ("status", "no_source_code", "no_proprietary_assets", "separate_builder_context", "spec_path"):
                if req not in airlock:
                    errors.append(f"root.airlock.{req}: missing required field")
            _check_str(airlock, "status", "root.airlock", errors, enum={"pending", "passed", "rejected", "not_applicable"})
            airlock_status = airlock.get("status")
            _check_str(airlock, "audited_by", "root.airlock", errors)
            if "audited_at" in airlock and not _is_valid_datetime(airlock["audited_at"]):
                errors.append("root.airlock.audited_at: expected ISO-8601 date-time string")
            for bkey in ("no_source_code", "no_proprietary_assets", "separate_builder_context"):
                if bkey in airlock and not isinstance(airlock[bkey], bool):
                    errors.append(f"root.airlock.{bkey}: expected boolean")
            if "disclaimer_acknowledged" in airlock and not isinstance(airlock["disclaimer_acknowledged"], bool):
                errors.append("root.airlock.disclaimer_acknowledged: expected boolean")
            _check_str(airlock, "spec_path", "root.airlock", errors, min_len=1)
            _check_str(airlock, "spec_sha256", "root.airlock", errors, pattern=SHA256_RE)

            if airlock_status == "passed":
                if not (
                    airlock.get("no_source_code") is True
                    and airlock.get("no_proprietary_assets") is True
                    and airlock.get("separate_builder_context") is True
                ):
                    errors.append(
                        "root.airlock: status 'passed' requires no_source_code, no_proprietary_assets, and separate_builder_context all true"
                    )

            if "audit" in airlock:
                audit = airlock["audit"]
                if not isinstance(audit, dict):
                    errors.append("root.airlock.audit: expected object")
                else:
                    for k in audit:
                        if k not in {"lint_status", "lint_hash", "human_reviewer", "signed_at", "linter_version"}:
                            errors.append(f"root.airlock.audit: unexpected property {k!r}")
                    _check_str(audit, "lint_status", "root.airlock.audit", errors, enum={"PASS", "WARN", "FAIL"}, required=True)
                    _check_str(audit, "lint_hash", "root.airlock.audit", errors, pattern=SHA256_RE, required=True)
                    _check_str(audit, "human_reviewer", "root.airlock.audit", errors, min_len=1, required=True)
                    if "signed_at" not in audit or not _is_valid_datetime(audit["signed_at"]):
                        errors.append("root.airlock.audit.signed_at: expected ISO-8601 date-time string")
                    if airlock_status == "passed" and audit.get("lint_status") != "PASS":
                        errors.append("root.airlock.audit.lint_status: airlock.status='passed' requires lint_status='PASS'")

    # target_summary
    ts = data.get("target_summary")
    if ts is not None:
        if not isinstance(ts, dict):
            errors.append("root.target_summary: expected object")
        else:
            for k in ts:
                if k not in {"kind", "label", "observable_url", "subject_sha256"}:
                    errors.append(f"root.target_summary: unexpected property {k!r}")
            kinds = TARGET_KINDS_V1_0 if is_v1_0 else TARGET_KINDS_V1_1
            _check_str(ts, "kind", "root.target_summary", errors, enum=kinds, required=True)
            _check_str(ts, "label", "root.target_summary", errors, min_len=1, required=True)
            _check_str(ts, "observable_url", "root.target_summary", errors)
            _check_str(ts, "subject_sha256", "root.target_summary", errors, pattern=SHA256_RE)

    # analyst_lane
    al = data.get("analyst_lane")
    if al is not None:
        if not isinstance(al, dict):
            errors.append("root.analyst_lane: expected object")
        else:
            allowed_al = {"engine", "rea_version", "evidence_format", "analyst_bundle_path", "tool_families_used", "evidence_ids", "unknown_ids"}
            for k in al:
                if k not in allowed_al:
                    errors.append(f"root.analyst_lane: unexpected property {k!r}")
            _check_str(al, "engine", "root.analyst_lane", errors, enum={"rea", "none"}, required=True)
            _check_str(al, "rea_version", "root.analyst_lane", errors, required=True)
            if "evidence_format" not in al or not isinstance(al["evidence_format"], int) or isinstance(al["evidence_format"], bool) or al["evidence_format"] not in (1, 2):
                errors.append("root.analyst_lane.evidence_format: required integer in {1, 2}")
            _check_str(al, "analyst_bundle_path", "root.analyst_lane", errors)
            if "tool_families_used" in al:
                if not isinstance(al["tool_families_used"], list) or any(not isinstance(x, str) for x in al["tool_families_used"]):
                    errors.append("root.analyst_lane.tool_families_used: expected array of strings")
            if "evidence_ids" not in al or not isinstance(al["evidence_ids"], list):
                errors.append("root.analyst_lane.evidence_ids: required array")
            else:
                for idx, ev in enumerate(al["evidence_ids"]):
                    if not isinstance(ev, str) or not EVIDENCE_ID_RE.match(ev):
                        errors.append(f"root.analyst_lane.evidence_ids[{idx}]: invalid evidence ID {ev!r}")
            if "unknown_ids" not in al or not isinstance(al["unknown_ids"], list):
                errors.append("root.analyst_lane.unknown_ids: required array")
            elif any(not isinstance(x, str) for x in al["unknown_ids"]):
                errors.append("root.analyst_lane.unknown_ids: expected array of strings")

    # obligations
    obls = data.get("obligations")
    if obls is not None:
        if not isinstance(obls, list) or len(obls) < 1:
            errors.append("root.obligations: required non-empty array")
        else:
            cats = CATEGORIES_V1_0 if is_v1_0 else CATEGORIES_V1_1
            ca_tgts = CA_CHECK_TARGETS_V1_0 if is_v1_0 else CA_CHECK_TARGETS_V1_1
            rea_methods = REA_METHODS_V1_0 if is_v1_0 else REA_METHODS_V1_1
            allowed_obl = {
                "obligation_id",
                "title",
                "category",
                "spec_section",
                "source_evidence_ids",
                "acceptance_criteria",
                "test_vectors",
                "ca_check_targets",
                "rea_verification_method",
                "status",
                "notes",
            }
            if not is_v1_0:
                allowed_obl |= {"coverage", "limitations"}
            for idx, obl in enumerate(obls):
                op = f"root.obligations[{idx}]"
                if not isinstance(obl, dict):
                    errors.append(f"{op}: expected object")
                    continue
                for k in obl:
                    if k not in allowed_obl:
                        errors.append(f"{op}: unexpected property {k!r}")
                _check_str(obl, "obligation_id", op, errors, pattern=OBLIGATION_ID_RE, required=True)
                _check_str(obl, "title", op, errors, min_len=1, required=True)
                _check_str(obl, "category", op, errors, enum=cats, required=True)
                _check_str(obl, "spec_section", op, errors, min_len=1, required=True)
                if "source_evidence_ids" not in obl or not isinstance(obl["source_evidence_ids"], list):
                    errors.append(f"{op}.source_evidence_ids: required array")
                else:
                    for eidx, ev in enumerate(obl["source_evidence_ids"]):
                        if not isinstance(ev, str) or not EVIDENCE_ID_RE.match(ev):
                            errors.append(f"{op}.source_evidence_ids[{eidx}]: invalid evidence ID {ev!r}")
                if "acceptance_criteria" not in obl or not isinstance(obl["acceptance_criteria"], list) or len(obl["acceptance_criteria"]) < 1:
                    errors.append(f"{op}.acceptance_criteria: required non-empty array")
                if "test_vectors" in obl:
                    if not isinstance(obl["test_vectors"], list):
                        errors.append(f"{op}.test_vectors: expected array")
                    else:
                        for tidx, tv in enumerate(obl["test_vectors"]):
                            tp = f"{op}.test_vectors[{tidx}]"
                            if not isinstance(tv, dict):
                                errors.append(f"{tp}: expected object")
                                continue
                            for k in tv:
                                if k not in {"test_id", "input_description", "expected_outcome"}:
                                    errors.append(f"{tp}: unexpected property {k!r}")
                            _check_str(tv, "test_id", tp, errors, min_len=1, required=True)
                            _check_str(tv, "input_description", tp, errors, min_len=1, required=True)
                            _check_str(tv, "expected_outcome", tp, errors, min_len=1, required=True)
                if "ca_check_targets" in obl:
                    if not isinstance(obl["ca_check_targets"], list):
                        errors.append(f"{op}.ca_check_targets: expected array")
                    else:
                        for cidx, tgt in enumerate(obl["ca_check_targets"]):
                            if tgt not in ca_tgts:
                                errors.append(f"{op}.ca_check_targets[{cidx}]: invalid target {tgt!r}")
                _check_str(obl, "rea_verification_method", op, errors, enum=rea_methods)
                _check_str(obl, "status", op, errors, enum={"pending", "passed", "partial", "failed", "unknown"}, required=True)
                _check_str(obl, "notes", op, errors)
                if "coverage" in obl:
                    cov = obl["coverage"]
                    if not isinstance(cov, dict):
                        errors.append(f"{op}.coverage: expected object")
                    else:
                        for ck in cov:
                            if ck not in {"scope", "notes"}:
                                errors.append(f"{op}.coverage: unexpected property {ck!r}")
                        _check_str(cov, "scope", f"{op}.coverage", errors, enum={"complete", "partial", "observable-only", "static-only", "unknown"}, required=True)
                        _check_str(cov, "notes", f"{op}.coverage", errors)
                if "limitations" in obl:
                    if not isinstance(obl["limitations"], list) or any(not isinstance(x, str) for x in obl["limitations"]):
                        errors.append(f"{op}.limitations: expected array of strings")

    # builder_lane
    bl = data.get("builder_lane")
    clean_room_verified = False
    if bl is not None:
        if not isinstance(bl, dict):
            errors.append("root.builder_lane: expected object")
        else:
            for k in bl:
                if k not in {"engine", "ca_version", "clean_room_verified", "workspace_path", "ca_project_id", "ca_checks"}:
                    errors.append(f"root.builder_lane: unexpected property {k!r}")
            _check_str(bl, "engine", "root.builder_lane", errors, enum={"craft-anything", "manual"}, required=True)
            _check_str(bl, "ca_version", "root.builder_lane", errors)
            if "clean_room_verified" not in bl or not isinstance(bl["clean_room_verified"], bool):
                errors.append("root.builder_lane.clean_room_verified: required boolean field")
            else:
                clean_room_verified = bl["clean_room_verified"]
            _check_str(bl, "workspace_path", "root.builder_lane", errors, min_len=1, required=True)
            _check_str(bl, "ca_project_id", "root.builder_lane", errors)
            if "ca_checks" in bl:
                if not isinstance(bl["ca_checks"], list):
                    errors.append("root.builder_lane.ca_checks: expected array")
                else:
                    for cidx, chk in enumerate(bl["ca_checks"]):
                        cp = f"root.builder_lane.ca_checks[{cidx}]"
                        if not isinstance(chk, dict):
                            errors.append(f"{cp}: expected object")
                            continue
                        for k in chk:
                            if k not in {"tool", "status", "summary"}:
                                errors.append(f"{cp}: unexpected property {k!r}")
                        _check_str(chk, "tool", cp, errors, required=True)
                        _check_str(chk, "status", cp, errors, enum={"passed", "partial", "failed", "skipped"}, required=True)
                        _check_str(chk, "summary", cp, errors, required=True)

    # parity_summary
    ps = data.get("parity_summary")
    if ps is not None:
        if not isinstance(ps, dict):
            errors.append("root.parity_summary: expected object")
        else:
            for k in ps:
                if k not in {"visual_status", "behavioral_status", "structural_status", "overall_status", "limitations", "unresolved_unknowns"}:
                    errors.append(f"root.parity_summary: unexpected property {k!r}")
            for sfield in ("visual_status", "behavioral_status", "structural_status"):
                _check_str(ps, sfield, "root.parity_summary", errors, enum={"passed", "partial", "failed", "unknown", "not_applicable"}, required=True)
            _check_str(ps, "overall_status", "root.parity_summary", errors, enum={"passed", "partial", "failed", "unknown"}, required=True)
            if "limitations" in ps:
                if not isinstance(ps["limitations"], list) or any(not isinstance(x, str) for x in ps["limitations"]):
                    errors.append("root.parity_summary.limitations: expected array of strings")
            if "unresolved_unknowns" not in ps or not isinstance(ps["unresolved_unknowns"], list):
                errors.append("root.parity_summary.unresolved_unknowns: required array")
            elif any(not isinstance(x, str) for x in ps["unresolved_unknowns"]):
                errors.append("root.parity_summary.unresolved_unknowns: expected array of strings")

    # Mutual exclusion: deep_private: true can NEVER coexist with any clean-room claim
    if deep_private is True:
        if mode in ("clean-room-ui", "two-team-process"):
            errors.append(f"root.deep_private: true cannot coexist with clean-room mode {mode!r}")
        if airlock_status == "passed":
            errors.append("root.deep_private: true cannot coexist with clean-room airlock.status='passed'")
        if clean_room_verified is True:
            errors.append("root.builder_lane.clean_room_verified: cannot be true when deep_private is true")

    return errors
