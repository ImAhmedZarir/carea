#!/usr/bin/env python3
"""Repository-wide integrity, link, manifest, schema, fixture, and upstream-asset-ban checks."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from carea.airlock import lint_airlock
from carea.commands import cmd_validate_handoff

# Verified exact hashes of upstream brand artwork & fonts observed in external installs (must never exist in carea).
BANNED_UPSTREAM_SHA256 = {
    "116b66711e78b23d1926bf40e4866a1cfa0f76e10f39bca9a67b8f70a5a2a014": "rea-plugin.png (morluto/rea)",
    "144e207c9ca57f61a311210a0d679c55d36f6614cbf4d15b7b280a268389aa1d": "rea-hopper-analysis.png (morluto/rea)",
    "fee0f409a9f73640ac42f28b3b0402898e968140a769183101ba759c709ff828": "craft-anything-1024.png (storytold/craft-anything)",
    "8c44c58fa2bb9f46afdfea04fe15e09820db325748a8f87c8c3f98de667e746b": "craft-anything.svg (storytold/craft-anything)",
    "479222ef3735852cc8b1533809c8c74f9b6ecef2807fb4027bad95c64c89d660": "craft-anything.ico (storytold/craft-anything)",
    "ac665ea22adb7226113b74fff88ba6f6dd2358665a9a42634f37ebf45297e9f2": "craft-anything.icns (storytold/craft-anything)",
    "1adb096acaa3d14f5ed678e99b808b0c8800f62cb342fa5c276298ad8030b458": "DMSans-Regular.ttf (upstream font)",
    "5a0de4b3d54ab272f76a1d8c84b7fb24c67bbec6591d5300e61c7bc10094b6c8": "GeistMono-Regular.ttf (upstream font)",
    "e6fd0d7e91550b3ed2b735d4312474362c4716edc4fc0577a0f61ed782d5aed1": "JetBrainsMono-Regular.ttf (upstream font)",
}

BANNED_FILENAMES = {
    "rea-plugin.png",
    "craft-anything-cli",
    "craft-anything-cli.exe",
    "rea.mjs",
    "plugin-mcp-launcher.mjs",
    "license-mit",
    "license-apache",
    "craft-anything.svg",
    "craft-anything.ico",
    "craft-anything.icns",
}

BANNED_EXTENSIONS = {
    ".exe", ".dll", ".so", ".dylib", ".jar", ".apk", ".aab", ".wasm",
    ".ttf", ".otf", ".woff", ".woff2", ".rs", ".ts", ".tsx", ".mjs",
}


def check_json_files(errors: list[str]) -> int:
    count = 0
    for jf in sorted(REPO_ROOT.rglob("*.json")):
        if ".git" in jf.parts:
            continue
        count += 1
        try:
            json.loads(jf.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            errors.append(f"Invalid JSON in {jf.relative_to(REPO_ROOT).as_posix()}: {exc}")
    return count


def check_yaml_workflows_and_frontmatter(errors: list[str]) -> int:
    checked = 0
    # Use PyYAML if available; otherwise perform strict structural/tab/tabulation checks + key validation.
    yaml_mod = None
    try:
        import yaml  # type: ignore

        yaml_mod = yaml
    except ImportError:
        pass

    yml_files = list(sorted(REPO_ROOT.rglob("*.yml"))) + list(sorted(REPO_ROOT.rglob("*.yaml")))
    for yf in yml_files:
        if ".git" in yf.parts:
            continue
        checked += 1
        txt = yf.read_text(encoding="utf-8")
        if "\t" in txt:
            errors.append(f"Tab indentation in YAML {yf.relative_to(REPO_ROOT).as_posix()}")
        if yaml_mod is not None:
            try:
                yaml_mod.safe_load(txt)
            except Exception as exc:
                errors.append(f"YAML parse error in {yf.relative_to(REPO_ROOT).as_posix()}: {exc}")
        elif not txt.strip():
            errors.append(f"Empty YAML file {yf.relative_to(REPO_ROOT).as_posix()}")

    for md in sorted((REPO_ROOT / ".github" / "ISSUE_TEMPLATE").glob("*.md")) + sorted((REPO_ROOT / "skills").rglob("SKILL.md")):
        checked += 1
        txt = md.read_text(encoding="utf-8")
        m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", txt, re.S)
        if not m:
            errors.append(f"Missing YAML frontmatter in {md.relative_to(REPO_ROOT).as_posix()}")
            continue
        fm = m.group(1)
        if "\t" in fm:
            errors.append(f"Tab character in YAML frontmatter of {md.relative_to(REPO_ROOT).as_posix()}")
        if yaml_mod is not None:
            try:
                parsed = yaml_mod.safe_load(fm)
                if not isinstance(parsed, dict) or not parsed.get("name"):
                    errors.append(f"Frontmatter missing 'name' mapping in {md.relative_to(REPO_ROOT).as_posix()}")
            except Exception as exc:
                errors.append(f"Frontmatter YAML error in {md.relative_to(REPO_ROOT).as_posix()}: {exc}")
        elif "name:" not in fm:
            errors.append(f"Frontmatter missing 'name:' in {md.relative_to(REPO_ROOT).as_posix()}")
    return checked


def check_markdown_links(errors: list[str]) -> int:
    link_re = re.compile(r"\[[^\]]+\]\(([^)#\s]+)")
    checked = 0
    for md in sorted(REPO_ROOT.rglob("*.md")):
        if ".git" in md.parts:
            continue
        checked += 1
        txt = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8", errors="ignore"), flags=re.S)
        for target in link_re.findall(txt):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"Broken markdown link in {md.relative_to(REPO_ROOT).as_posix()}: {target}")
    return checked


def check_upstream_asset_ban(errors: list[str]) -> int:
    scanned = 0
    for p in sorted(REPO_ROOT.rglob("*")):
        if ".git" in p.parts or "__pycache__" in p.parts or not p.is_file():
            continue
        scanned += 1
        rel = p.relative_to(REPO_ROOT).as_posix()
        low_name = p.name.lower()
        if low_name in BANNED_FILENAMES:
            errors.append(f"Banned upstream filename present: {rel}")
        # Allow JS/TS only if explicitly self-owned under examples/sample-target/ in Phase 7
        in_sample = rel.startswith("examples/sample-target/")
        if p.suffix.lower() in BANNED_EXTENSIONS and not (in_sample and p.suffix.lower() in (".js", ".mjs")):
            errors.append(f"Forbidden binary/font/upstream source extension in {rel}")
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        if digest in BANNED_UPSTREAM_SHA256:
            errors.append(f"Matched banned upstream asset SHA-256 ({BANNED_UPSTREAM_SHA256[digest]}) at {rel}")
    return scanned


def check_examples_and_fixtures(errors: list[str]) -> None:
    # Airlock example artifacts must pass validate-handoff and airlock-lint --strict
    ex_handoff = REPO_ROOT / "examples" / "handoff.example.json"
    ex_spec = REPO_ROOT / "examples" / "clean-room-spec.example.md"
    val = cmd_validate_handoff(ex_handoff)
    if not val["valid"]:
        errors.append(f"examples/handoff.example.json invalid: {val['errors']}")
    for ex_file in (ex_spec, ex_handoff):
        lint = lint_airlock(ex_file)
        if lint["status"] != "PASS":
            errors.append(f"{ex_file.name} failed airlock-lint --strict ({lint['status']}): {lint['findings']}")

    # Positive handoff fixtures must pass
    for pf in sorted((REPO_ROOT / "tests" / "fixtures" / "handoffs" / "positive").glob("*.json")):
        res = cmd_validate_handoff(pf)
        if not res["valid"]:
            errors.append(f"Positive fixture {pf.name} failed validation: {res['errors']}")

    # Negative handoff fixtures must fail
    for nf in sorted((REPO_ROOT / "tests" / "fixtures" / "handoffs" / "negative").glob("*.json")):
        res = cmd_validate_handoff(nf)
        if res["valid"]:
            errors.append(f"Negative fixture {nf.name} unexpectedly validated!")


def check_bundled_data_sync(errors: list[str]) -> None:
    pairs = [
        (REPO_ROOT / "compat" / "matrix.json", SRC_DIR / "carea" / "data" / "matrix.json"),
        (REPO_ROOT / "schemas" / "carea-handoff.schema.json", SRC_DIR / "carea" / "data" / "carea-handoff.schema.json"),
    ]
    for src_f, dst_f in pairs:
        if src_f.read_text(encoding="utf-8") != dst_f.read_text(encoding="utf-8"):
            errors.append(f"Bundled data out of sync: {src_f.name} vs {dst_f.relative_to(REPO_ROOT).as_posix()}")


def main() -> int:
    errors: list[str] = []
    n_json = check_json_files(errors)
    n_yaml = check_yaml_workflows_and_frontmatter(errors)
    n_md = check_markdown_links(errors)
    n_files = check_upstream_asset_ban(errors)
    check_examples_and_fixtures(errors)
    check_bundled_data_sync(errors)

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print(
        f"ALL REPO CHECKS PASSED: {n_json} JSON, {n_yaml} YAML/frontmatter, "
        f"{n_md} markdown link checks, {n_files} files asset-ban clean."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
