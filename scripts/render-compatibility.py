#!/usr/bin/env python3
"""Render or verify docs/compatibility.md from compat/matrix.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def render_markdown(matrix: dict) -> str:
    rea = matrix["engines"]["rea"]
    ca = matrix["engines"]["craft_anything"]
    supported_handoffs = ", ".join(f"`{v}`" for v in matrix["handoff_schema_supported"])

    lines: list[str] = [
        "# Upstream Compatibility Matrix",
        "",
        "<!-- GENERATED FROM compat/matrix.json via `python scripts/render-compatibility.py`. DO NOT HAND-EDIT. -->",
        "",
        f"`carea` target release **`{matrix['carea_version']}`** supports handoff schema versions {supported_handoffs} (current: `{matrix['handoff_schema_version']}`).",
        "All version bounds in `carea` (`carea doctor`, `scripts/verify-upstream.sh`, and `scripts/verify-upstream.ps1`) read [`compat/matrix.json`](../compat/matrix.json) as the single source of truth.",
        "",
        "## Engine Version Matrix",
        "",
        "| Engine | Package / Binary | Recommended | Minimum Compatible | Runtime Requirement | Maturity & Policy |",
        "| --- | --- | --- | --- | --- | --- |",
        (
            f"| **[{rea['display_name']}]({rea['repository']})** | `{rea['package']}` (`{rea['binary']}`) | "
            f"`{rea['recommended']}` | `{rea['minimum_compatible']}` | `{rea['runtime_requirement']['node']}` | {rea['license']} |"
        ),
        (
            f"| **[{ca['display_name']}]({ca['repository']})** | `{ca['package']}` (`{ca['binary']}`) | "
            f"`{ca['recommended']}` | `{ca['minimum_compatible']}` | Prebuilt binary or Rust toolchain | {ca['license']} — **{ca['maturity']}** |"
        ),
        "",
        "## Supported Version Ranges",
        "",
        "### REA (`rea-agents`)",
        "",
        "| Range | Status | Behavior Notes |",
        "| --- | --- | --- |",
    ]

    for row in rea["ranges"]:
        lines.append(f"| `>={row['min']}, <{row['max_exclusive']}` | `{row['status']}` | {row['summary']} |")

    lines.extend(
        [
            "",
            "### Craft Anything (`craft-anything-cli`)",
            "",
            "| Range | Status | Behavior Notes |",
            "| --- | --- | --- |",
        ]
    )
    for row in ca["ranges"]:
        lines.append(f"| `>={row['min']}, <{row['max_exclusive']}` | `{row['status']}` | {row['summary']} |")

    lines.extend(
        [
            "",
            "## Observed Verification Evidence",
            "",
            "Instead of generic \"Tested with\" claims, the table below records exactly what was verified vs left unverified on the build environment:",
            "",
        ]
    )

    for key in ("rea", "craft_anything"):
        eng = matrix["engines"][key]
        lines.append(f"### {eng['display_name']}")
        lines.append("")
        for obs in eng["observed"]:
            lines.append(f"- **`{obs['version']}`** (`{obs['channel']}`):")
            for item in obs["verified"]:
                lines.append(f"  - Verified: {item}")
            for item in obs.get("unverified_on_host", []):
                lines.append(f"  - Unverified on build host: {item}")
        lines.append("")

    lines.extend(
        [
            "## Running Local Compatibility Checks",
            "",
            "Run the upstream verification script for your OS to compare locally installed `rea` and `craft-anything-cli` binaries against `compat/matrix.json`:",
            "",
            "```bash",
            "# Linux / macOS / Git Bash",
            "bash scripts/verify-upstream.sh",
            "```",
            "",
            "```powershell",
            "# Windows PowerShell",
            "pwsh -File scripts/verify-upstream.ps1",
            "```",
            "",
            "Or run `carea doctor` (which checks binaries, versions, and MCP config profiles directly against `compat/matrix.json`).",
            "",
            f"*Matrix updated: `{matrix['updated_at']}`. Claim-by-claim evidence lives in [`docs/upstream-facts.md`](upstream-facts.md).*",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render docs/compatibility.md from compat/matrix.json")
    parser.add_argument("--check", action="store_true", help="Exit non-zero if docs/compatibility.md differs")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    matrix_path = repo_root / "compat" / "matrix.json"
    out_path = repo_root / "docs" / "compatibility.md"

    matrix = json.loads(matrix_path.read_text(encoding="utf-8-sig"))
    expected = render_markdown(matrix)

    if args.check:
        if not out_path.exists():
            print(f"MISSING: {out_path}", file=sys.stderr)
            return 1
        actual = out_path.read_text(encoding="utf-8")
        if actual != expected:
            print(f"STALE: {out_path} does not match {matrix_path}. Run scripts/render-compatibility.py.", file=sys.stderr)
            return 1
        print(f"OK: {out_path} matches {matrix_path}")
        return 0

    out_path.write_text(expected, encoding="utf-8", newline="\n")
    print(f"WROTE: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
