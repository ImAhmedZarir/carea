"""Command-line interface for carea (Python 3.10+ stdlib only)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from . import __version__
from .airlock import check_isolation, lint_airlock
from .commands import (
    VALID_MODES,
    apply_mcp_profile,
    build_mcp_profile,
    cmd_airlock_sign,
    cmd_init,
    cmd_parity_report,
    cmd_return_feedback,
    cmd_spec_draft,
    cmd_validate_handoff,
)
from .upstream import run_doctor


def _dump_json(payload: object) -> None:
    print(json.dumps(payload, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="carea",
        description="Independent Level-1 orchestration CLI and airlock gates for carea.",
    )
    parser.add_argument("-V", "--version", action="version", version=f"carea {__version__}")

    sub = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = sub.add_parser("init", help="Create 4-dir airlock workspace layout and .carea/config.json")
    p_init.add_argument("dir", type=Path, help="Project workspace directory to initialize")
    p_init.add_argument("--mode", choices=VALID_MODES, default="two-team-process")
    p_init.add_argument("--topology", choices=("a", "b"), default="b")
    p_init.add_argument("--target-name", default=None)
    p_init.add_argument("--force", action="store_true")
    p_init.add_argument("--json", action="store_true")

    # doctor
    p_doc = sub.add_parser("doctor", help="Check rea + craft-anything-cli versions and MCP config profiles")
    p_doc.add_argument("--rea-bin", default=None)
    p_doc.add_argument("--ca-bin", default=None)
    p_doc.add_argument("--client-config", type=Path, action="append", default=[])
    p_doc.add_argument("--json", action="store_true")

    # validate-handoff
    p_val = sub.add_parser("validate-handoff", help="Validate carea-handoff.json against bundled schema (1.0.0 & 1.1.0)")
    p_val.add_argument("file", type=Path)
    p_val.add_argument("--schema", type=Path, default=None)
    p_val.add_argument("--json", action="store_true")

    # airlock-lint
    p_lint = sub.add_parser("airlock-lint", help="Heuristic leak scanner for airlock/ files (requires human review)")
    p_lint.add_argument("path", type=Path)
    p_lint.add_argument("--strict", action="store_true", help="Exit non-zero on WARN as well as FAIL")
    p_lint.add_argument("--json", action="store_true")

    # airlock-sign
    p_sign = sub.add_parser("airlock-sign", help="Record explicit human review sign-off after airlock-lint PASS")
    p_sign.add_argument("handoff", type=Path)
    p_sign.add_argument("--reviewer", required=True, help="Human reviewer name or handle")
    p_sign.add_argument("--confirm-human-review", action="store_true", help="Explicitly attest human review completed")
    p_sign.add_argument("--airlock-dir", type=Path, default=None)
    p_sign.add_argument("--json", action="store_true")

    # isolation-check
    p_iso = sub.add_parser("isolation-check", help="Check builder-workspace vs analyst-evidence directory & permission isolation")
    p_iso.add_argument("dir", type=Path, nargs="?", default=Path("."))
    p_iso.add_argument("--strict", action="store_true")
    p_iso.add_argument("--json", action="store_true")

    # spec-draft
    p_draft = sub.add_parser("spec-draft", help="Generate DRAFT sanitized spec skeleton from an REA evidence bundle (IDs/structure only)")
    p_draft.add_argument("bundle", type=Path)
    p_draft.add_argument("--out", type=Path, default=None)
    p_draft.add_argument("--json", action="store_true")

    # parity-report
    p_par = sub.add_parser("parity-report", help="Merge CA and REA verification reports into verification/parity-checklist.md")
    p_par.add_argument("--handoff", type=Path, required=True)
    p_par.add_argument("--ca-report", type=Path, default=None)
    p_par.add_argument("--rea-report", type=Path, default=None)
    p_par.add_argument("--out", type=Path, default=None)
    p_par.add_argument("--json", action="store_true")

    # return-feedback
    p_fb = sub.add_parser("return-feedback", help="Generate Lane-B-safe failure feedback (vectors/diffs only, no source)")
    p_fb.add_argument("--handoff", type=Path, required=True)
    p_fb.add_argument("--ca-report", type=Path, default=None)
    p_fb.add_argument("--rea-report", type=Path, default=None)
    p_fb.add_argument("--out", type=Path, default=None)
    p_fb.add_argument("--json", action="store_true")

    # mcp-profile
    p_mcp = sub.add_parser("mcp-profile", help="Print (or safely merge with diff confirmation) MCP profile snippets")
    p_mcp.add_argument("preset", help="Preset name (e.g. carea-master, rea-master, rea-all-families, rea-hot-cold, ca-deep-full, ca-clean-room)")
    p_mcp.add_argument("--apply", type=Path, default=None, help="Target JSON config file to patch after showing diff")
    p_mcp.add_argument("--server-name", default=None)
    p_mcp.add_argument("--yes", action="store_true", help="Apply printed diff non-interactively")
    p_mcp.add_argument("--json", action="store_true")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "init":
            res = cmd_init(args.dir, mode=args.mode, topology=args.topology, target_name=args.target_name, force=args.force)
            if args.json:
                _dump_json(res)
            else:
                print(f"Initialized {res['project_dir']} (mode={res['mode']}, topology={res['topology']}, deep_private={res['deep_private']})")
                for f in res["written"]:
                    print(f"  wrote:   {f}")
                for f in res["skipped"]:
                    print(f"  skipped: {f}")
            return 0

        if args.command == "doctor":
            res = run_doctor(rea_bin_override=args.rea_bin, ca_bin_override=args.ca_bin, client_configs=args.client_config)
            if args.json:
                _dump_json(res)
            else:
                r = res["rea"]
                c = res["craft_anything"]
                print(f"carea doctor (matrix {res['carea_version']}, updated {res['matrix_updated_at']})")
                print(f"  [REA]            status={r['status']} version={r['version'] or 'none'} node={r['node_version'] or 'none'} (satisfied={r['node_satisfied']})")
                for n in r["notes"]:
                    print(f"                   note: {n}")
                print(f"  [Craft Anything] status={c['status']} version={c['version'] or 'none'} path={c['path'] or 'missing'}")
                for n in c["notes"]:
                    print(f"                   note: {n}")
                for f in res["mcp_profile_findings"]:
                    print(f"  [{f['severity']}] {f['file']}: {f['message']}")
            has_cfg_fail = any(f["severity"] == "FAIL" for f in res["mcp_profile_findings"])
            return 1 if has_cfg_fail else 0

        if args.command == "validate-handoff":
            res = cmd_validate_handoff(args.file, schema_path=args.schema)
            if args.json:
                _dump_json(res)
            else:
                if res["valid"]:
                    print(f"VALID: {res['file']} (schema_version={res['schema_version']})")
                else:
                    print(f"INVALID: {res['file']} ({len(res['errors'])} error(s))")
                    for err in res["errors"]:
                        print(f"  - {err}")
            return 0 if res["valid"] else 1

        if args.command == "airlock-lint":
            res = lint_airlock(args.path)
            if args.json:
                _dump_json(res)
            else:
                print(f"{res['status']}: {res['target']} ({res['files_scanned']} file(s) scanned)")
                print(res["disclaimer"])
                for f in res["findings"]:
                    print(f"  [{f['severity']}] {f['file']}:{f['line']} ({f['rule']}) - {f['message']}")
            if res["status"] == "FAIL" or (args.strict and res["status"] == "WARN"):
                return 1
            return 0

        if args.command == "airlock-sign":
            res = cmd_airlock_sign(
                args.handoff,
                reviewer=args.reviewer,
                confirm_human_review=args.confirm_human_review,
                airlock_dir=args.airlock_dir,
            )
            if args.json:
                _dump_json(res)
            else:
                print(f"SIGNED: {res['handoff']} by {res['reviewer']} at {res['signed_at']} (lint_hash={res['lint_hash']})")
            return 0

        if args.command == "isolation-check":
            res = check_isolation(args.dir)
            if args.json:
                _dump_json(res)
            else:
                print(f"{res['status']}: isolation check on {res['project_dir']}")
                for iss in res["issues"]:
                    print(f"  [{iss['severity']}] {iss['check']}: {iss['message']}")
                print("Recommended host-agent permission snippet (.claude/settings.local.json):")
                print(json.dumps(res["recommended_snippets"]["claude_settings_json"], indent=2))
            if res["status"] == "FAIL" or (args.strict and res["status"] == "WARN"):
                return 1
            return 0

        if args.command == "spec-draft":
            res = cmd_spec_draft(args.bundle, out_path=args.out)
            if args.json:
                _dump_json(res)
            elif args.out:
                print(f"DRAFT written to {args.out} ({len(res['obligation_ids'])} obligations, {len(res['evidence_ids'])} ev IDs, {len(res['unknown_ids'])} unk IDs)")
            else:
                print(res["markdown"])
            return 0

        if args.command == "parity-report":
            res = cmd_parity_report(
                args.handoff,
                ca_report_path=args.ca_report,
                rea_report_path=args.rea_report,
                out_path=args.out,
            )
            if args.json:
                _dump_json(res)
            elif args.out:
                print(f"WROTE parity checklist {args.out} (overall_status={res['overall_status']})")
            else:
                print(res["markdown"])
            return 1 if res["overall_status"] == "failed" else 0

        if args.command == "return-feedback":
            res = cmd_return_feedback(
                args.handoff,
                ca_report_path=args.ca_report,
                rea_report_path=args.rea_report,
                out_path=args.out,
            )
            if args.json:
                _dump_json(res)
            elif args.out:
                print(f"WROTE sanitized return feedback {args.out} ({res['failing_count']} failing/partial obligation(s))")
            else:
                print(res["markdown"])
            return 0

        if args.command == "mcp-profile":
            if args.apply is None:
                res = build_mcp_profile(args.preset, server_name=args.server_name)
                _dump_json(res)
                return 0
            res = apply_mcp_profile(args.preset, args.apply, server_name=args.server_name, assume_yes=args.yes)
            if args.json:
                _dump_json(res)
            elif res.get("applied"):
                print(res["diff"])
                print(f"Applied MCP profile {args.preset!r} to {res['file']}")
            else:
                print(f"Not applied ({res.get('reason')})")
            return 0

    except Exception as exc:
        print(f"carea error: {exc}", file=sys.stderr)
        return 1

    return 2
