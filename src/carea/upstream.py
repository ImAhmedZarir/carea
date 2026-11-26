"""Upstream binary discovery, version matching, and MCP config inspection."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .data_loader import load_compat_matrix


SEMVER_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)")


def parse_semver(text: str | None) -> tuple[int, int, int] | None:
    if not text:
        return None
    m = SEMVER_RE.search(text)
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))


def classify_engine_version(ver_text: str | None, engine_spec: dict[str, Any]) -> str:
    ver = parse_semver(ver_text)
    if ver is None:
        return "untested"
    for r in engine_spec.get("ranges", []):
        lo = parse_semver(r.get("min"))
        hi = parse_semver(r.get("max_exclusive"))
        if lo is not None and hi is not None and lo <= ver < hi:
            return str(r.get("status", "untested"))
    min_c = parse_semver(engine_spec.get("minimum_compatible"))
    if min_c is not None and ver < min_c:
        return "unsupported"
    return "untested"


def _probe(cmd: str, args: list[str], timeout_s: int = 12) -> tuple[int, str, str]:
    try:
        res = subprocess.run([cmd, *args], capture_output=True, text=True, timeout=timeout_s, check=False)
        return res.returncode, res.stdout, res.stderr
    except Exception as exc:
        return -1, "", str(exc)


def resolve_executable(override: str | None, candidates: list[str], extra_paths: list[Path] | None = None) -> str | None:
    if override:
        p = Path(override)
        if p.is_file():
            return str(p)
        found = shutil.which(override)
        if found:
            return found
        return None
    for name in candidates:
        found = shutil.which(name)
        if found:
            return found
    for ep in extra_paths or []:
        if ep.is_file():
            return str(ep)
    return None


def discover_windows_plugin_ca() -> list[Path]:
    plugin_root = Path.home() / ".gemini" / "config" / "plugins" / "craft-anything" / "bin"
    if not plugin_root.is_dir():
        return []
    return sorted(plugin_root.rglob("craft-anything-cli*.exe"))[:1]


def check_mcp_config_file(path: Path, rea_version: str | None) -> list[dict[str, str]]:
    """Inspect a client MCP config file for common REA/CA footguns."""
    findings: list[dict[str, str]] = []
    if not path.is_file():
        return [{"severity": "WARN", "file": str(path), "message": "Config file not found"}]

    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    rea_ver = parse_semver(rea_version)
    rea_610_plus = rea_ver is None or rea_ver >= (6, 10, 0)

    if path.suffix.lower() == ".json":
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError as exc:
            return [{"severity": "FAIL", "file": str(path), "message": f"Invalid JSON: {exc}"}]
        servers = doc.get("mcpServers") or doc.get("servers") or {}
        if isinstance(servers, dict):
            for sname, sdef in servers.items():
                if not isinstance(sdef, dict):
                    continue
                env = sdef.get("env") if isinstance(sdef.get("env"), dict) else {}
                args = sdef.get("args") if isinstance(sdef.get("args"), list) else []
                cmd = str(sdef.get("command") or "")
                low = f"{sname} {cmd} {' '.join(map(str, args))}".lower()
                if "rea" in low:
                    for key in ("REA_MCP_INPUT_SCHEMA_PROFILE", "REA_MCP_OUTPUT_SCHEMA_PROFILE"):
                        val = str(env.get(key, "")).lower()
                        if val == "full" and rea_610_plus:
                            findings.append(
                                {
                                    "severity": "FAIL",
                                    "file": str(path),
                                    "message": f"Server {sname!r} sets {key}=full, which REA >= 6.10.0 rejects; use compact or off.",
                                }
                            )
                    if not env.get("REA_MCP_TOOL_CATALOG_PROFILE") and not env.get("REA_MCP_TOOL_FAMILIES"):
                        findings.append(
                            {
                                "severity": "WARN",
                                "file": str(path),
                                "message": f"Server {sname!r} omits REA_MCP_TOOL_CATALOG_PROFILE=hot-cold or REA_MCP_TOOL_FAMILIES (exposes full 264-tool catalog).",
                            }
                        )
                if "craft-anything" in low:
                    if "--all-tools" in args:
                        findings.append(
                            {
                                "severity": "WARN",
                                "file": str(path),
                                "message": f"Server {sname!r} passes --all-tools to craft-anything-cli mcp (bloats context with 300+ tools).",
                            }
                        )
                    if "--clean-room" not in args and "--deep" not in args:
                        findings.append(
                            {
                                "severity": "WARN",
                                "file": str(path),
                                "message": f"Server {sname!r} does not pass --clean-room or --deep explicitly.",
                            }
                        )
    else:
        # Basic text scan for TOML/other configs (e.g., Codex config.toml)
        if ("REA_MCP_INPUT_SCHEMA_PROFILE" in raw or "REA_MCP_OUTPUT_SCHEMA_PROFILE" in raw) and re.search(
            r'REA_MCP_(?:INPUT|OUTPUT)_SCHEMA_PROFILE\s*=\s*["\']full["\']', raw
        ):
            findings.append(
                {
                    "severity": "FAIL",
                    "file": str(path),
                    "message": "Config sets REA schema profile to 'full', which REA >= 6.10.0 rejects; use 'compact' or 'off'.",
                }
            )
        if "--all-tools" in raw and "craft-anything" in raw:
            findings.append(
                {
                    "severity": "WARN",
                    "file": str(path),
                    "message": "Config passes --all-tools to craft-anything-cli mcp; omit it to keep schema count low.",
                }
            )
    return findings


def run_doctor(
    *,
    rea_bin_override: str | None = None,
    ca_bin_override: str | None = None,
    client_configs: list[Path] | None = None,
) -> dict[str, Any]:
    matrix = load_compat_matrix()
    rea_spec = matrix["engines"]["rea"]
    ca_spec = matrix["engines"]["craft_anything"]

    node_bin = resolve_executable(os.environ.get("CAREA_NODE_BIN"), ["node"])
    node_ver = None
    node_ok = False
    if node_bin:
        rc, out, _ = _probe(node_bin, ["--version"])
        nv = parse_semver(out) if rc == 0 else None
        if nv:
            node_ver = ".".join(map(str, nv))
            node_ok = (nv[0] == 22 and nv >= (22, 23, 4)) or (nv[0] == 24 and nv >= (24, 22, 1)) or nv >= (26, 12, 1)

    rea_bin = resolve_executable(rea_bin_override or os.environ.get("CAREA_REA_BIN"), ["rea", "rea-agents"])
    rea_info: dict[str, Any] = {
        "path": rea_bin,
        "version": None,
        "status": "missing",
        "node_version": node_ver,
        "node_satisfied": node_ok,
        "notes": [],
    }
    if rea_bin:
        rc_v, out_v, err_v = _probe(rea_bin, ["--version"])
        sv = parse_semver(out_v + "\n" + err_v)
        if rc_v == 0 and sv:
            rea_info["version"] = ".".join(map(str, sv))
            rea_info["status"] = classify_engine_version(rea_info["version"], rea_spec)
        else:
            rea_info["status"] = "unsupported"
            rea_info["notes"].append(f"rea --version failed cleanly: {(err_v or out_v).strip()[:200]}")
    else:
        rea_info["notes"].append(f"rea not found on PATH (recommended: npm install -g rea-agents@{rea_spec['recommended']})")

    ca_bin = resolve_executable(
        ca_bin_override or os.environ.get("CAREA_CA_BIN"),
        ["craft-anything-cli"],
        extra_paths=discover_windows_plugin_ca(),
    )
    ca_info: dict[str, Any] = {
        "path": ca_bin,
        "version": None,
        "status": "missing",
        "notes": [],
    }
    if ca_bin:
        rc_v, out_v, err_v = _probe(ca_bin, ["--version"])
        sv = parse_semver(out_v + "\n" + err_v)
        if rc_v == 0 and sv:
            ca_info["version"] = ".".join(map(str, sv))
            ca_info["status"] = classify_engine_version(ca_info["version"], ca_spec)
        else:
            ca_info["status"] = "unsupported"
            ca_info["notes"].append(f"craft-anything-cli --version failed cleanly: {(err_v or out_v).strip()[:200]}")
    else:
        ca_info["notes"].append(f"craft-anything-cli not found on PATH (recommended: {ca_spec['recommended']})")

    config_findings: list[dict[str, str]] = []
    for cfg in client_configs or []:
        config_findings.extend(check_mcp_config_file(cfg, rea_info["version"]))

    return {
        "carea_version": matrix["carea_version"],
        "matrix_updated_at": matrix["updated_at"],
        "rea": rea_info,
        "craft_anything": ca_info,
        "mcp_profile_findings": config_findings,
    }
