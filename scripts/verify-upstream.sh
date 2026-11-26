#!/usr/bin/env bash
# Verify installed `rea` and `craft-anything-cli` versions against compat/matrix.json.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
MATRIX_PATH="${MATRIX_PATH:-${REPO_ROOT}/compat/matrix.json}"
JSON_OUT=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json)
      JSON_OUT=1
      shift
      ;;
    --matrix)
      MATRIX_PATH="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [--json] [--matrix PATH]"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 2
      ;;
  esac
done

if [[ ! -f "${MATRIX_PATH}" ]]; then
  echo "Compatibility matrix not found: ${MATRIX_PATH}" >&2
  exit 1
fi

PYTHON_BIN="${PYTHON_BIN:-}"
if [[ -z "${PYTHON_BIN}" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
  elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
  fi
fi

if [[ -z "${PYTHON_BIN}" ]]; then
  echo "Python 3 is required to evaluate ${MATRIX_PATH}" >&2
  exit 1
fi

exec "${PYTHON_BIN}" - "${MATRIX_PATH}" "${JSON_OUT}" <<'PYEOF'
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

matrix_path = Path(sys.argv[1])
json_out = sys.argv[2] == "1"
matrix = json.loads(matrix_path.read_text(encoding="utf-8-sig"))


def parse_semver(text: str):
    m = re.search(r"(\d+)\.(\d+)\.(\d+)", text or "")
    if not m:
        return None
    return tuple(int(x) for x in m.groups())


def classify(ver_tuple, spec):
    if ver_tuple is None:
        return "untested"
    for r in spec["ranges"]:
        lo = parse_semver(r["min"])
        hi = parse_semver(r["max_exclusive"])
        if lo <= ver_tuple < hi:
            return r["status"]
    min_c = parse_semver(spec["minimum_compatible"])
    if min_c and ver_tuple < min_c:
        return "unsupported"
    return "untested"


def probe(cmd, args):
    try:
        res = subprocess.run(
            [cmd, *args],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        return res.returncode, res.stdout, res.stderr
    except Exception as exc:
        return -1, "", str(exc)


def resolve_bin(override, names):
    if override:
        p = Path(override)
        if p.exists():
            return str(p)
        found = shutil.which(override)
        return found
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return None


node_bin = resolve_bin(os.environ.get("CAREA_NODE_BIN"), ["node"])
node_ver = None
node_ok = False
if node_bin:
    rc, out, _ = probe(node_bin, ["--version"])
    if rc == 0:
        nv = parse_semver(out)
        if nv:
            node_ver = ".".join(map(str, nv))
            node_ok = (
                (nv[0] == 22 and nv >= (22, 23, 4))
                or (nv[0] == 24 and nv >= (24, 22, 1))
                or (nv[0] == 26 and nv >= (26, 12, 1))
                or nv[0] > 26
            )

rea_bin = resolve_bin(os.environ.get("CAREA_REA_BIN"), ["rea", "rea-agents"])
rea_res = {
    "engine": "rea",
    "path": rea_bin,
    "version": None,
    "status": "missing",
    "node_version": node_ver,
    "node_satisfied": node_ok,
    "checks": {},
    "notes": [],
}
if rea_bin:
    rc_v, out_v, err_v = probe(rea_bin, ["--version"])
    rc_h, _, _ = probe(rea_bin, ["--help"])
    rc_d, _, _ = probe(rea_bin, ["doctor", "--json"])
    rea_res["checks"] = {"version": rc_v == 0, "help": rc_h == 0, "doctor": rc_d == 0}
    sv = parse_semver(out_v + "\n" + err_v)
    if rc_v == 0 and sv:
        rea_res["version"] = ".".join(map(str, sv))
        rea_res["status"] = classify(sv, matrix["engines"]["rea"])
    else:
        rea_res["status"] = "unsupported"
        rea_res["notes"].append(f"rea failed --version: {(err_v or out_v).strip()}")
else:
    rea_res["notes"].append(
        f"rea not found on PATH (install npm install -g rea-agents@{matrix['engines']['rea']['recommended']})"
    )

ca_bin = resolve_bin(os.environ.get("CAREA_CA_BIN"), ["craft-anything-cli"])
ca_res = {
    "engine": "craft_anything",
    "path": ca_bin,
    "version": None,
    "status": "missing",
    "checks": {},
    "notes": [],
}
if ca_bin:
    rc_v, out_v, err_v = probe(ca_bin, ["--version"])
    rc_d, _, _ = probe(ca_bin, ["doctor", "--json"])
    rc_cmd, _, _ = probe(ca_bin, ["commands", "--json"])
    rc_cap, _, _ = probe(ca_bin, ["capabilities", "--json"])
    ca_res["checks"] = {
        "version": rc_v == 0,
        "doctor": rc_d == 0,
        "commands": rc_cmd == 0,
        "capabilities": rc_cap == 0,
    }
    sv = parse_semver(out_v + "\n" + err_v)
    if rc_v == 0 and sv:
        ca_res["version"] = ".".join(map(str, sv))
        ca_res["status"] = classify(sv, matrix["engines"]["craft_anything"])
    else:
        ca_res["status"] = "unsupported"
        ca_res["notes"].append(f"craft-anything-cli failed --version: {(err_v or out_v).strip()}")
else:
    ca_res["notes"].append(
        f"craft-anything-cli not found on PATH (install {matrix['engines']['craft_anything']['recommended']})"
    )

report = {
    "carea_version": matrix["carea_version"],
    "matrix_updated_at": matrix["updated_at"],
    "rea": rea_res,
    "craft_anything": ca_res,
}

if json_out:
    print(json.dumps(report, indent=2))
else:
    print(f"carea upstream verification report (matrix {matrix['carea_version']}, updated {matrix['updated_at']})")
    print()
    print(f"[REA]            status={rea_res['status']} version={rea_res['version'] or 'none'} path={rea_res['path'] or 'missing'}")
    print(f"                 node={rea_res['node_version'] or 'none'} satisfied={rea_res['node_satisfied']}")
    for n in rea_res["notes"]:
        print(f"                 note: {n}")
    print(f"[Craft Anything] status={ca_res['status']} version={ca_res['version'] or 'none'} path={ca_res['path'] or 'missing'}")
    for n in ca_res["notes"]:
        print(f"                 note: {n}")
PYEOF
