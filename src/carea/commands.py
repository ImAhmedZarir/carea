"""Core command implementations for the carea CLI."""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import __version__
from .airlock import lint_airlock
from .data_loader import load_compat_matrix, load_handoff_schema, load_json_text
from .validator import validate_handoff_data


DEEP_PRIVATE_BANNER = """==============================================================================
WARNING: PRIVATE DEEP REBUILD MODE — THIS WORKFLOW IS NOT CLEAN-ROOM
Both REA Deep analysis and Craft Anything --deep were permitted to inspect
source files, binaries, assets, and internals directly. deep_private: true.
NEVER claim clean-room independence for artifacts produced in this mode.
==============================================================================
"""

VALID_MODES = (
    "clean-room-ui",
    "two-team-process",
    "deep-verification",
    "private-deep-rebuild",
    "game-rebuild",
    "android-mobile",
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _slugify(value: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return s[:48] or "project"


def cmd_init(
    project_dir: Path,
    *,
    mode: str = "two-team-process",
    topology: str = "b",
    target_name: str | None = None,
    force: bool = False,
) -> dict[str, Any]:
    if mode not in VALID_MODES:
        raise ValueError(f"Invalid mode {mode!r}; expected one of {VALID_MODES}")
    if topology not in ("a", "b"):
        raise ValueError(f"Invalid topology {topology!r}; expected 'a' or 'b'")

    deep_private = mode == "private-deep-rebuild"
    tname = target_name or project_dir.name or "sample-target"
    slug = _slugify(tname)

    for d in (
        project_dir / ".carea",
        project_dir / "analyst-evidence",
        project_dir / "airlock",
        project_dir / "builder-workspace",
        project_dir / "verification",
    ):
        d.mkdir(parents=True, exist_ok=True)

    config_path = project_dir / ".carea" / "config.json"
    spec_path = project_dir / "airlock" / "clean-room-spec.md"
    handoff_path = project_dir / "airlock" / "carea-handoff.json"
    parity_path = project_dir / "verification" / "parity-checklist.md"

    banner_block = f"\n```text\n{DEEP_PRIVATE_BANNER}```\n" if deep_private else ""
    spec_title = "Private Deep Rebuild Engineering Spec (NOT CLEAN-ROOM)" if deep_private else "Clean-Room Functional Specification"
    spec_notice = (
        "> **Airlock Notice:** `private-deep-rebuild` mode (`deep_private: true`) — **NOT CLEAN-ROOM**. Never claim clean-room independence."
        if deep_private
        else "> **Airlock Notice:** Process aid only — **not legal advice and not a legal clean-room guarantee**."
    )

    spec_content = f"""# {spec_title}: {tname}

{spec_notice}
{banner_block}
- **Status:** `DRAFT` *(requires authoring + `carea airlock-lint` + human review)*
- **Mode:** `{mode}` (`topology: {topology}`)
- **Handoff Record:** `airlock/carea-handoff.json`

## 1. Observable Surfaces & State Transitions

*(Describe rendered views, API routes, inputs, outputs, and errors without copying source code, secrets, or assets.)*

## 2. Explicit Unknowns

- `unk_01`: *(Document unobserved behavior or gaps here.)*

## 3. Acceptance Test Vectors

| Test ID | Obligation | Input / Condition | Expected Observable Result |
| --- | --- | --- | --- |
| `test_01` | `obl_{slug}_core` | `<TODO: input>` | `<TODO: expected response/UI state>` |
"""

    parity_content = f"""# Dual-Axis Parity Checklist: {tname}
{banner_block}
- **Mode:** `{mode}`
- **Handoff Record:** `airlock/carea-handoff.json`

| Obligation ID | Summary | Axis 1 (CA UI Check) | Axis 2 (REA Verification) | Final Verdict | Notes / Limitations |
| --- | --- | --- | --- | --- | --- |
| `obl_{slug}_core` | Core observable behavior | `unknown` | `unknown` | `unknown` | Generated starter checklist |
"""

    written: list[str] = []
    skipped: list[str] = []

    def _write_if_allowed(p: Path, content: str) -> None:
        if p.exists() and not force:
            skipped.append(str(p))
            return
        p.write_text(content, encoding="utf-8", newline="\n")
        written.append(str(p))

    _write_if_allowed(spec_path, spec_content)
    _write_if_allowed(parity_path, parity_content)

    spec_sha = _sha256_file(spec_path)
    config_obj = {
        "carea_version": __version__,
        "mode": mode,
        "topology": topology,
        "deep_private": deep_private,
        "target_name": tname,
        "created_at": _now_iso(),
        "directories": {
            "analyst_evidence": "analyst-evidence",
            "airlock": "airlock",
            "builder_workspace": "builder-workspace",
            "verification": "verification",
        },
    }
    _write_if_allowed(config_path, json.dumps(config_obj, indent=2) + "\n")

    target_kind = "android-apk" if mode == "android-mobile" else ("game" if mode == "game-rebuild" else "web-app")
    handoff_obj: dict[str, Any] = {
        "schema_version": "1.1.0",
        "project": {
            "name": tname,
            "description": f"Generated by carea init ({mode})",
            "created_at": _now_iso(),
            "authorized": True,
        },
        "mode": mode,
        "topology": topology,
        "deep_private": deep_private,
        "tool_versions": {
            "rea": None,
            "ca": None,
            "carea": __version__,
        },
        "airlock": {
            "status": "not_applicable" if deep_private or mode in ("clean-room-ui", "deep-verification") else "pending",
            "no_source_code": False if deep_private else True,
            "no_proprietary_assets": False if deep_private else True,
            "separate_builder_context": topology == "b" and not deep_private,
            "spec_path": "airlock/clean-room-spec.md",
            "spec_sha256": spec_sha,
            "disclaimer_acknowledged": True,
        },
        "target_summary": {
            "kind": target_kind,
            "label": tname,
        },
        "analyst_lane": {
            "engine": "none" if mode == "clean-room-ui" else "rea",
            "rea_version": "none" if mode == "clean-room-ui" else "6.10.1",
            "evidence_format": 2,
            "analyst_bundle_path": "analyst-evidence/bundle.json",
            "evidence_ids": [],
            "unknown_ids": ["unk_01"],
        },
        "obligations": [
            {
                "obligation_id": f"obl_{slug}_core",
                "title": f"Core behavior for {tname}",
                "category": "user-flow",
                "spec_section": "1. Observable Surfaces & State Transitions",
                "source_evidence_ids": [],
                "acceptance_criteria": ["Implement behavior specified in airlock/clean-room-spec.md"],
                "test_vectors": [
                    {
                        "test_id": "test_01",
                        "input_description": "Default startup flow",
                        "expected_outcome": "Renders cleanly and satisfies core contract",
                    }
                ],
                "ca_check_targets": ["none"] if mode == "deep-verification" else ["rebuild_check"],
                "rea_verification_method": "none" if mode == "clean-room-ui" else "verify_reconstruction",
                "status": "pending",
                "coverage": {"scope": "unknown", "notes": "Not yet executed"},
                "limitations": [],
            }
        ],
        "builder_lane": {
            "engine": "manual" if mode == "deep-verification" else "craft-anything",
            "clean_room_verified": False,
            "workspace_path": "builder-workspace",
            "ca_checks": [],
        },
        "parity_summary": {
            "visual_status": "not_applicable" if mode == "deep-verification" else "unknown",
            "behavioral_status": "not_applicable" if mode == "clean-room-ui" else "unknown",
            "structural_status": "not_applicable" if mode == "clean-room-ui" else "unknown",
            "overall_status": "unknown",
            "limitations": [],
            "unresolved_unknowns": ["unk_01"],
        },
    }
    _write_if_allowed(handoff_path, json.dumps(handoff_obj, indent=2) + "\n")

    return {
        "project_dir": str(project_dir.resolve()),
        "mode": mode,
        "topology": topology,
        "deep_private": deep_private,
        "written": written,
        "skipped": skipped,
    }


def cmd_validate_handoff(handoff_path: Path, schema_path: Path | None = None) -> dict[str, Any]:
    data = load_json_text(handoff_path.read_text(encoding="utf-8-sig"))
    errors = validate_handoff_data(data)

    used_jsonschema = False
    if schema_path is not None:
        try:
            import jsonschema  # type: ignore

            schema = load_handoff_schema(schema_path)
            jsonschema.validate(instance=data, schema=schema)
            used_jsonschema = True
        except ImportError:
            pass
        except Exception as exc:
            errors.append(f"jsonschema: {exc.message if hasattr(exc, 'message') else exc}")

    return {
        "valid": len(errors) == 0,
        "file": str(handoff_path),
        "schema_version": data.get("schema_version"),
        "jsonschema_checked": used_jsonschema,
        "errors": errors,
    }


def cmd_airlock_sign(
    handoff_path: Path,
    *,
    reviewer: str,
    confirm_human_review: bool,
    airlock_dir: Path | None = None,
) -> dict[str, Any]:
    if not reviewer.strip():
        raise ValueError("--reviewer must be a non-empty reviewer name")
    if not confirm_human_review:
        raise PermissionError("Refusing to sign airlock: explicit --confirm-human-review flag is required.")

    handoff_path = handoff_path.resolve()
    data = load_json_text(handoff_path.read_text(encoding="utf-8-sig"))
    if data.get("deep_private") is True or data.get("mode") == "private-deep-rebuild":
        raise ValueError("Cannot sign clean-room airlock when deep_private=true or mode=private-deep-rebuild (NOT clean-room).")

    scan_dir = (airlock_dir or handoff_path.parent).resolve()
    lint_report = lint_airlock(scan_dir)
    if lint_report["status"] != "PASS":
        raise ValueError(
            f"Refusing airlock-sign: airlock-lint status is {lint_report['status']} "
            f"(only strictly PASS may be signed). Fix {len(lint_report['findings'])} finding(s) first."
        )

    spec_rel = data["airlock"]["spec_path"]
    spec_candidates = [
        handoff_path.parent.parent / spec_rel,
        handoff_path.parent / spec_rel,
        Path(spec_rel),
    ]
    spec_file = next((p for p in spec_candidates if p.is_file()), None)

    now = _now_iso()
    data["airlock"]["status"] = "passed"
    data["airlock"]["audited_by"] = reviewer.strip()
    data["airlock"]["audited_at"] = now
    data["airlock"]["no_source_code"] = True
    data["airlock"]["no_proprietary_assets"] = True
    data["airlock"]["separate_builder_context"] = True
    data["airlock"]["disclaimer_acknowledged"] = True

    if data.get("schema_version") != "1.0.0":
        if spec_file is not None:
            data["airlock"]["spec_sha256"] = _sha256_file(spec_file)
        data["airlock"]["audit"] = {
            "lint_status": lint_report["status"],
            "lint_hash": lint_report["report_sha256"],
            "human_reviewer": reviewer.strip(),
            "signed_at": now,
            "linter_version": __version__,
        }

    errors = validate_handoff_data(data)
    if errors:
        raise ValueError(f"Signed handoff failed validation: {'; '.join(errors)}")

    handoff_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    return {
        "signed": True,
        "handoff": str(handoff_path),
        "lint_status": lint_report["status"],
        "lint_hash": lint_report["report_sha256"],
        "reviewer": reviewer.strip(),
        "signed_at": now,
    }


def _collect_ids(obj: Any, *, evs: set[str], unks: set[str], obls: list[str], seen_obl: set[str]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("raw_result", "source", "sources", "decompiled", "disassembly", "assembly", "bytes", "payload", "body", "html", "code", "strings"):
                continue
            if k in ("evidence_id", "parent_evidence_id") and isinstance(v, str) and v.startswith("ev_"):
                evs.add(v)
            elif k in ("evidence_ids", "evidence_refs", "source_evidence_ids") and isinstance(v, list):
                for item in v:
                    if isinstance(item, str) and item.startswith("ev_"):
                        evs.add(item)
            elif k == "unknown_id" and isinstance(v, str) and v.startswith("unk_"):
                unks.add(v)
            elif k in ("unknown_ids", "unknown_refs", "unresolved_unknowns") and isinstance(v, list):
                for item in v:
                    if isinstance(item, str) and item.startswith("unk_"):
                        unks.add(item)
            elif k == "obligation_id" and isinstance(v, str) and v.startswith("obl_") and v not in seen_obl:
                seen_obl.add(v)
                obls.append(v)
            else:
                _collect_ids(v, evs=evs, unks=unks, obls=obls, seen_obl=seen_obl)
    elif isinstance(obj, list):
        for item in obj:
            _collect_ids(item, evs=evs, unks=unks, obls=obls, seen_obl=seen_obl)


def cmd_spec_draft(bundle_path: Path, *, out_path: Path | None = None) -> dict[str, Any]:
    bundle = load_json_text(bundle_path.read_text(encoding="utf-8-sig"))
    evs: set[str] = set()
    unks: set[str] = set()
    obls: list[str] = []
    _collect_ids(bundle, evs=evs, unks=unks, obls=obls, seen_obl=set())

    ev_list = sorted(evs)
    unk_list = sorted(unks)
    if not obls:
        obls = ["obl_draft_01"]

    lines = [
        "# DRAFT Clean-Room Spec Skeleton",
        "",
        "> **STATUS: DRAFT — GENERATED FROM IDs AND STRUCTURE ONLY.**",
        "> This file was generated by `carea spec-draft` without copying source code, disassembly, strings, or raw payloads.",
        "> **Human editing + `carea airlock-lint` + `carea airlock-sign` are REQUIRED before Lane B starts.**",
        "",
        "## 1. Structural Inventory (IDs Only)",
        "",
        f"- **Opaque Evidence IDs referenced (`{len(ev_list)}`):** " + (", ".join(f"`{e}`" for e in ev_list) if ev_list else "_none extracted_"),
        f"- **Unknown IDs preserved (`{len(unk_list)}`):** " + (", ".join(f"`{u}`" for u in unk_list) if unk_list else "_none extracted_"),
        "",
        "## 2. Obligations & Acceptance Criteria Placeholders",
        "",
    ]

    for oid in obls:
        lines.extend(
            [
                f"### `{oid}`",
                "",
                "- **Behavior Summary:** `<TODO: describe externally observable behavior in plain English — no code>`",
                "- **Acceptance Criteria:** `<TODO: measurable behavioral assertion>`",
                "- **Related Evidence IDs:** `<TODO: map ev_... IDs>`",
                "",
            ]
        )

    lines.extend(
        [
            "## 3. Acceptance Test Vector Placeholders",
            "",
            "| Test ID | Obligation | Input / Precondition | Expected Observable Result |",
            "| --- | --- | --- | --- |",
        ]
    )
    for idx, oid in enumerate(obls, 1):
        lines.append(f"| `test_{idx:02d}` | `{oid}` | `<TODO: input>` | `<TODO: observable output>` |")

    lines.append("")
    markdown = "\n".join(lines)

    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(markdown, encoding="utf-8", newline="\n")

    return {
        "draft": True,
        "evidence_ids": ev_list,
        "unknown_ids": unk_list,
        "obligation_ids": obls,
        "out_path": str(out_path) if out_path else None,
        "markdown": markdown,
    }


def _extract_axis_status(report: Any, obligation_id: str, expected_tools: list[str] | None = None) -> tuple[str, list[str]]:
    if report is None:
        return "unknown", ["Report not supplied"]
    notes: list[str] = []

    if isinstance(report, dict):
        obls = report.get("obligations")
        if isinstance(obls, dict) and obligation_id in obls:
            entry = obls[obligation_id]
            if isinstance(entry, str):
                return entry, notes
            if isinstance(entry, dict):
                st = str(entry.get("status", "unknown"))
                if entry.get("notes"):
                    notes.append(str(entry["notes"]))
                return st, notes
        if isinstance(obls, list):
            for entry in obls:
                if isinstance(entry, dict) and entry.get("obligation_id") == obligation_id:
                    st = str(entry.get("status", "unknown"))
                    if entry.get("notes"):
                        notes.append(str(entry["notes"]))
                    return st, notes
        checks = report.get("checks")
        if isinstance(checks, dict) and expected_tools:
            statuses = []
            for t in expected_tools:
                if t in checks:
                    val = checks[t]
                    statuses.append(val.get("status", "unknown") if isinstance(val, dict) else str(val))
            if statuses:
                if "failed" in statuses:
                    return "failed", notes
                if all(s == "passed" for s in statuses) and len(statuses) == len(expected_tools):
                    return "passed", notes
                if any(s in ("passed", "partial") for s in statuses):
                    return "partial", notes
        if "status" in report and not isinstance(obls, (list, dict)):
            return str(report["status"]), notes

    return "unknown", ["No obligation-specific entry in report"]


def cmd_parity_report(
    handoff_path: Path,
    *,
    ca_report_path: Path | None = None,
    rea_report_path: Path | None = None,
    out_path: Path | None = None,
) -> dict[str, Any]:
    handoff = load_json_text(handoff_path.read_text(encoding="utf-8-sig"))
    ca_rep = load_json_text(ca_report_path.read_text(encoding="utf-8-sig")) if ca_report_path else None
    rea_rep = load_json_text(rea_report_path.read_text(encoding="utf-8-sig")) if rea_report_path else None

    deep_private = bool(handoff.get("deep_private"))
    project_name = handoff.get("project", {}).get("name", "target")
    rows: list[dict[str, Any]] = []

    for obl in handoff.get("obligations", []):
        oid = obl["obligation_id"]
        title = obl.get("title", "")
        ca_targets = [t for t in (obl.get("ca_check_targets") or []) if t != "none"]
        rea_method = obl.get("rea_verification_method") or "none"

        ca_st, ca_notes = ("none", ["No CA UI checks declared"]) if not ca_targets else _extract_axis_status(ca_rep, oid, ca_targets)
        rea_st, rea_notes = ("none", ["No REA verification declared"]) if rea_method == "none" else _extract_axis_status(rea_rep, oid, [rea_method])

        # `passed` strictly requires BOTH axes complete and passed!
        if ca_st == "failed" or rea_st == "failed":
            final_status = "failed"
        elif ca_st == "passed" and rea_st == "passed":
            cov = obl.get("coverage", {})
            cov_scope = cov.get("scope", "complete") if isinstance(cov, dict) else "complete"
            lims = obl.get("limitations") or []
            if cov_scope in ("partial", "observable-only", "static-only") or lims:
                final_status = "partial"
            else:
                final_status = "passed"
        elif ca_st == "passed" or rea_st == "passed" or ca_st == "partial" or rea_st == "partial":
            final_status = "partial"
        else:
            final_status = "unknown"

        combined_notes = [n for n in (*ca_notes, *rea_notes, *(obl.get("limitations") or [])) if n]
        rows.append(
            {
                "obligation_id": oid,
                "title": title,
                "ca_status": ca_st,
                "rea_status": rea_st,
                "final_status": final_status,
                "notes": "; ".join(combined_notes) if combined_notes else "—",
            }
        )

    statuses = {r["final_status"] for r in rows}
    if "failed" in statuses:
        overall = "failed"
    elif rows and statuses == {"passed"}:
        overall = "passed"
    elif "partial" in statuses or ("passed" in statuses and len(statuses) > 1):
        overall = "partial"
    else:
        overall = "unknown"

    lines = [f"# Dual-Axis Parity Checklist: {project_name}", ""]
    if deep_private:
        lines.extend(["```text", DEEP_PRIVATE_BANNER.rstrip("\n"), "```", ""])
    lines.extend(
        [
            f"- **Project:** `{project_name}`",
            f"- **Mode:** `{handoff.get('mode')}` | **Overall Status:** `{overall}`",
            "- **Verdict Rule:** `passed` requires both CA (observable) and REA (behavioral) checks complete with zero coverage gaps.",
            "",
            "| Obligation ID | Summary | Axis 1 (CA UI) | Axis 2 (REA Behavioral) | Verdict | Notes / Limitations |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for r in rows:
        lines.append(f"| `{r['obligation_id']}` | {r['title']} | `{r['ca_status']}` | `{r['rea_status']}` | `{r['final_status']}` | {r['notes']} |")
    lines.append("")
    md = "\n".join(lines)

    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(md, encoding="utf-8", newline="\n")

    return {
        "overall_status": overall,
        "deep_private": deep_private,
        "rows": rows,
        "out_path": str(out_path) if out_path else None,
        "markdown": md,
    }


def cmd_return_feedback(
    handoff_path: Path,
    *,
    ca_report_path: Path | None = None,
    rea_report_path: Path | None = None,
    out_path: Path | None = None,
) -> dict[str, Any]:
    """Produce Lane-B-safe failure feedback containing only failing vectors & pixel diffs."""
    parity = cmd_parity_report(handoff_path, ca_report_path=ca_report_path, rea_report_path=rea_report_path, out_path=None)
    handoff = load_json_text(handoff_path.read_text(encoding="utf-8-sig"))
    ca_rep = load_json_text(ca_report_path.read_text(encoding="utf-8-sig")) if ca_report_path else {}
    rea_rep = load_json_text(rea_report_path.read_text(encoding="utf-8-sig")) if rea_report_path else {}

    obl_map = {o["obligation_id"]: o for o in handoff.get("obligations", [])}
    failing = [r for r in parity["rows"] if r["final_status"] in ("failed", "partial")]

    lines = [
        "# Lane-B Sanitized Return Feedback",
        "",
        "> **Airlock Feedback Rule:** Lists failing test vectors and observable UI/pixel differences only.",
        "> Original source code, disassembly, payloads, and `analyst-evidence/` paths are strictly excluded.",
        "",
    ]

    if not failing:
        lines.append("No failed or partial obligations reported.")
    else:
        for r in failing:
            oid = r["obligation_id"]
            obl = obl_map.get(oid, {})
            lines.extend(
                [
                    f"## `{oid}` — {r['title']} (`{r['final_status']}`)",
                    "",
                    f"- **CA UI Status:** `{r['ca_status']}` | **REA Verification Status:** `{r['rea_status']}`",
                ]
            )
            if isinstance(ca_rep, dict):
                ca_obls = ca_rep.get("obligations", {})
                if isinstance(ca_obls, dict) and isinstance(ca_obls.get(oid), dict):
                    diff_summary = ca_obls[oid].get("pixel_diff") or ca_obls[oid].get("ui_diff")
                    if isinstance(diff_summary, str):
                        lines.append(f"- **Observable UI / Pixel Diff:** {diff_summary}")
            if isinstance(rea_rep, dict):
                rea_obls = rea_rep.get("obligations", {})
                if isinstance(rea_obls, dict) and isinstance(rea_obls.get(oid), dict):
                    fv = rea_obls[oid].get("failing_vectors") or []
                    if isinstance(fv, list):
                        for item in fv:
                            if isinstance(item, dict):
                                lines.append(
                                    f"- **Failing Vector `{item.get('test_id', 'vec')}`:** "
                                    f"expected `{item.get('expected', '?')}`, observed `{item.get('observed', '?')}`"
                                )
            for tv in obl.get("test_vectors", [])[:3]:
                if isinstance(tv, dict):
                    lines.append(
                        f"- **Contract Vector `{tv.get('test_id', 'test')}`:** "
                        f"`{tv.get('input_description', '')}` -> `{tv.get('expected_outcome', '')}`"
                    )
            lines.append("")

    md = "\n".join(lines)

    with tempfile.TemporaryDirectory() as td:
        tf = Path(td) / "return-feedback.md"
        tf.write_text(md, encoding="utf-8")
        lint_res = lint_airlock(tf)
        if lint_res["status"] == "FAIL":
            raise ValueError(f"Generated feedback tripped heuristic airlock-lint FAIL: {lint_res['findings']}")

    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(md, encoding="utf-8", newline="\n")

    return {
        "failing_count": len(failing),
        "out_path": str(out_path) if out_path else None,
        "markdown": md,
    }


def build_mcp_profile(preset: str, *, server_name: str | None = None) -> dict[str, Any]:
    matrix = load_compat_matrix()
    profs = matrix["mcp_profiles"]
    rea_profiles = profs["rea"]
    ca_profiles = profs["craft_anything"]
    rea_rec = matrix["engines"]["rea"]["recommended"]

    mapping: dict[str, dict[str, Any]] = {
        "rea-hot-cold": {"rea": {"command": "npx", "args": ["-y", f"rea-agents@{rea_rec}", "mcp"], "env": rea_profiles["hot_cold"]["env"]}},
        "rea-native": {"rea": {"command": "npx", "args": ["-y", f"rea-agents@{rea_rec}", "mcp"], "env": rea_profiles["native"]["env"]}},
        "rea-web": {"rea": {"command": "npx", "args": ["-y", f"rea-agents@{rea_rec}", "mcp"], "env": rea_profiles["web_js_electron"]["env"]}},
        "rea-android": {"rea": {"command": "npx", "args": ["-y", f"rea-agents@{rea_rec}", "mcp"], "env": rea_profiles["android_mobile"]["env"]}},
        "rea-firmware": {"rea": {"command": "npx", "args": ["-y", f"rea-agents@{rea_rec}", "mcp"], "env": rea_profiles["firmware_uefi"]["env"]}},
        "rea-managed": {"rea": {"command": "npx", "args": ["-y", f"rea-agents@{rea_rec}", "mcp"], "env": rea_profiles["managed_dotnet"]["env"]}},
        "ca-clean-room": {"craft-anything": ca_profiles["clean_room_default"]},
        "ca-restricted-web": {"craft-anything": ca_profiles["clean_room_restricted_web"]},
        "ca-deep-private": {"craft-anything": ca_profiles["private_deep_rebuild"]},
        "two-team-lane-a": {"rea": {"command": "npx", "args": ["-y", f"rea-agents@{rea_rec}", "mcp"], "env": rea_profiles["hot_cold"]["env"]}},
        "two-team-lane-b": {"craft-anything": ca_profiles["clean_room_default"]},
    }

    if preset not in mapping:
        raise ValueError(f"Unknown preset {preset!r}. Available: {', '.join(sorted(mapping))}")

    selected = mapping[preset]
    if server_name and len(selected) == 1:
        only_val = next(iter(selected.values()))
        selected = {server_name: only_val}
    return {"mcpServers": selected}


def apply_mcp_profile(
    preset: str,
    config_file: Path,
    *,
    server_name: str | None = None,
    assume_yes: bool = False,
) -> dict[str, Any]:
    snippet = build_mcp_profile(preset, server_name=server_name)
    config_file = config_file.resolve()

    if config_file.exists():
        old_text = config_file.read_text(encoding="utf-8-sig")
        existing = json.loads(old_text)
        if not isinstance(existing, dict):
            raise ValueError(f"{config_file} does not contain a JSON object")
    else:
        old_text = "{}\n"
        existing = {}

    merged = json.loads(json.dumps(existing))
    servers = merged.setdefault("mcpServers", {})
    if not isinstance(servers, dict):
        raise ValueError(f"{config_file}: mcpServers must be a JSON object")
    for k, v in snippet["mcpServers"].items():
        servers[k] = v

    new_text = json.dumps(merged, indent=2) + "\n"
    diff = "".join(
        difflib.unified_diff(
            old_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=f"{config_file} (before)",
            tofile=f"{config_file} (after)",
        )
    )

    if not diff:
        return {"applied": False, "reason": "no-changes", "diff": ""}

    if not assume_yes:
        if not sys.stdin.isatty():
            raise PermissionError("Refusing to modify config without interactive confirmation or --yes.")
        print(diff)
        ans = input(f"Apply changes to {config_file}? [y/N]: ").strip().lower()
        if ans not in ("y", "yes"):
            return {"applied": False, "reason": "cancelled", "diff": diff}

    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(new_text, encoding="utf-8", newline="\n")
    return {"applied": True, "file": str(config_file), "diff": diff}
