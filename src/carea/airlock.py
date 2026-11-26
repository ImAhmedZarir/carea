"""Heuristic airlock leak scanner (`carea airlock-lint`) and isolation checks.

IMPORTANT: `airlock-lint` is a heuristic gate only. It NEVER proves absence of
leakage; human review and `carea airlock-sign` remain mandatory before Lane B starts.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import stat
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


HEURISTIC_DISCLAIMER = (
    "HEURISTIC GATE ONLY: airlock-lint NEVER proves absence of leakage. "
    "Manual human review and `carea airlock-sign` are still required."
)

MEDIA_BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".ico", ".svg",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".mp3", ".wav", ".ogg", ".flac", ".mp4", ".webm", ".mov",
    ".glb", ".gltf", ".fbx", ".obj",
    ".pak", ".utoc", ".ucas", ".bundle",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".dex", ".apk", ".aab", ".wasm", ".pyc",
}

CODE_FENCE_LANGS = {
    "c", "cpp", "cc", "cxx", "h", "hpp", "rust", "rs", "java", "kotlin", "kt",
    "swift", "csharp", "cs", "ts", "tsx", "js", "jsx", "javascript", "typescript",
    "py", "python", "go", "golang", "asm", "nasm", "s", "smali", "glsl", "hlsl",
    "php", "ruby", "rb", "il",
}

NON_CODE_FENCE_LANGS = {"json", "http", "text", "txt", "mermaid", "csv", "tsv", "markdown", "md", "yaml", "yml", "toml"}

CODE_SYNTAX_RE = re.compile(
    r"(^|\s)(#include\b|function\s+\w+\s*\(|class\s+\w+\s*[{:]|impl\s+\w+|struct\s+\w+\s*\{|"
    r"public\s+(static\s+)?(class|void|int|String)\b|FUN_[0-9a-fA-F]{4,}|sub_[0-9a-fA-F]{4,}|"
    r"undefined[1248]?\s+\w+|reinterpret_cast<|->\s*\w+\s*\()"
)

ASM_RE = re.compile(
    r"\b(?:mov|movq|movl|lea|call|jmp|jne|je|jz|jnz|cmp|test|push|pop|ret|xor|add|sub|ldr|str|bl|blr|svc)\b"
    r"[^\n]{0,40}\b(?:rax|rbx|rcx|rdx|rsi|rdi|rsp|rbp|eax|ebx|ecx|edx|eip|rip|x[0-9]{1,2}|w[0-9]{1,2}|sp|lr)\b",
    re.IGNORECASE,
)
INLINE_CODE_RE = re.compile(
    r"(?:\b(?:if|while|for|switch)\s*\([^()\n]{2,60}\)\s*\{|"
    r"\b(?:return|const|let|var|def|fn|pub\s+fn)\s+[A-Za-z_][A-Za-z0-9_]*\s*(?:=|\([^)\n]*\)\s*\{)|"
    r"\{[A-Za-z_]\w*\s*=\s*[A-Za-z0-9_]+\s*(?:>>|<<|\^|\||&)\s*[^}\n]+\}|"
    r"\b[A-Za-z_]\w*\s*(?:>>|<<|\^=|\|=|&=)\s*(?:0x[0-9a-fA-F]+|\d+))"
)
MEM_ADDR_RE = re.compile(r"\b0x[0-9a-fA-F]{4,16}\b")
HEX_DUMP_RE = re.compile(r"(?:^[0-9a-fA-F]{6,8}:\s*(?:[0-9a-fA-F]{2}\s+){4,}|(?:[0-9a-fA-F]{2}\s+){8,}[0-9a-fA-F]{2})")
MINIFIED_JS_RE = re.compile(
    r"(?:webpackJsonp|__webpack_require__|__webpack_modules__|Object\.defineProperty\([^,]+,\s*[\"']__esModule[\"']|"
    r"!function\([a-z],[a-z]\)\{)"
)
BASE64_DATA_URI_RE = re.compile(r"data:(?:image|font|audio|video|application)/[a-z0-9.+-]+;base64,[A-Za-z0-9+/=]{24,}", re.I)
BASE64_LONG_BLOB_RE = re.compile(r"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{120,}={0,2}(?![A-Za-z0-9+/=])")

ANALYST_PATH_RE = re.compile(r"(?:[A-Za-z]:[\\/][^\s\"'`]+|[\\/][^\s\"'`]*)analyst-evidence(?:[\\/][^\s\"'`]*)?", re.I)
HOST_HOME_PATH_RE = re.compile(r"(?:C:\\Users\\[^\s\"'`]+|/Users/[^\s\"'`]+|/home/[^\s\"'`]+)")

SECRET_PATTERNS = [
    ("secret-openai-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("secret-prefixed-token", re.compile(r"\b(?:sk_live|sk_test|pk_live|pk_test|rk_live|rk_test|whsec|gh[pousr]|xox[baprs]|glpat)_[ \t]{0,3}[A-Za-z0-9_-]{8,}\b")),
    ("secret-spaced-bearer", re.compile(r"\b(?:Bearer|sk-live|sk-proj)[ \t]+[A-Za-z0-9._-]{16,}\b")),
    ("secret-github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("secret-aws-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("secret-google-key", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b")),
    ("secret-jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{8,}\b")),
    ("secret-bearer", re.compile(r"\bBearer\s+[A-Za-z0-9._-]{20,}\b")),
    ("cookie-header", re.compile(r"(?i)\b(?:set-cookie|cookie):\s*[^\r\n=;]{1,40}=[^\r\n;]{8,}")),
]

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b")
OBFUSCATED_EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+-]+\s*(?:\[\s*at\s*\]|\(\s*at\s*\)|\{\s*at\s*\})\s*"
    r"([A-Za-z0-9.-]+(?:\s*(?:\[\s*dot\s*\]|\(\s*dot\s*\)|\{\s*dot\s*\}|\.)\s*[A-Za-z]{2,})+)\b",
    re.IGNORECASE,
)
SAFE_EMAIL_DOMAINS = {"example.com", "example.org", "example.net", "localhost.localdomain", "test.invalid"}
TOKEN_CANDIDATE_RE = re.compile(r"(?<![A-Za-z0-9_/\\.-])([A-Za-z0-9_-]{24,})(?![A-Za-z0-9_/\\.-])")


def _shannon_entropy(s: str) -> float:
    counts = Counter(s)
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def _looks_high_entropy_secret(tok: str) -> bool:
    if tok.startswith(("ev_", "unk_", "obl_", "handoff_")):
        return False
    if re.fullmatch(r"[a-f0-9]{24,64}", tok.lower()):
        return False
    if re.fullmatch(r"[a-z]+(?:[_-][a-z0-9]+)+", tok):
        return False
    has_upper = any(c.isupper() for c in tok)
    has_lower = any(c.islower() for c in tok)
    has_digit = any(c.isdigit() for c in tok)
    if (has_upper + has_lower + has_digit) < 3:
        return False
    return _shannon_entropy(tok) >= 3.8


@dataclass
class LintFinding:
    severity: str  # FAIL | WARN
    rule: str
    file: str
    line: int
    message: str


def _is_spec_skeleton_line(line: str) -> bool:
    s = line.strip()
    return s.startswith("<!--") or s.startswith("> **Airlock Notice")


def lint_airlock(target: Path) -> dict[str, Any]:
    """Scan an airlock directory (or single file) for potential code, asset, path, or secret leaks."""
    target = target.resolve()
    files: list[Path]
    base_dir: Path
    if target.is_file():
        files = [target]
        base_dir = target.parent
    elif target.is_dir():
        files = sorted(p for p in target.rglob("*") if p.is_file())
        base_dir = target
    else:
        return {
            "status": "FAIL",
            "disclaimer": HEURISTIC_DISCLAIMER,
            "target": str(target),
            "files_scanned": 0,
            "findings": [asdict(LintFinding("FAIL", "missing-target", str(target), 0, "Target path does not exist"))],
            "report_sha256": hashlib.sha256(str(target).encode("utf-8")).hexdigest(),
        }

    findings: list[LintFinding] = []
    scanned = 0

    for fp in files:
        rel = fp.relative_to(base_dir).as_posix()
        ext = fp.suffix.lower()

        if ext in MEDIA_BINARY_EXTENSIONS:
            findings.append(
                LintFinding("FAIL", "binary-or-media-asset", rel, 0, f"Forbidden binary/media/font asset {ext!r} inside airlock")
            )
            continue

        try:
            text = fp.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(
                LintFinding("FAIL", "non-utf8-binary", rel, 0, "Non-UTF-8 binary payload detected inside airlock")
            )
            continue

        scanned += 1
        lines = text.splitlines()
        in_fence = False
        fence_lang = ""
        fence_start = 0
        fence_lines: list[str] = []
        prose_block_words = 0
        prose_block_start = 1

        for idx, line in enumerate(lines, 1):
            stripped = line.strip()

            if stripped.startswith("```"):
                if not in_fence:
                    in_fence = True
                    fence_lang = stripped[3:].strip().lower().split()[0] if stripped[3:].strip() else ""
                    fence_start = idx
                    fence_lines = []
                    if fence_lang in CODE_FENCE_LANGS:
                        findings.append(
                            LintFinding("FAIL", "fenced-target-code", rel, idx, f"Disallowed source/assembly code fence ```{fence_lang}")
                        )
                else:
                    block_body = "\n".join(fence_lines)
                    if fence_lang not in CODE_FENCE_LANGS and fence_lang not in NON_CODE_FENCE_LANGS:
                        if CODE_SYNTAX_RE.search(block_body):
                            findings.append(
                                LintFinding("FAIL", "unlabelled-code-fence", rel, fence_start, "Unlabelled fenced block resembles target source/pseudocode")
                            )
                    in_fence = False
                    fence_lang = ""
                prose_block_words = 0
                continue

            if in_fence:
                fence_lines.append(line)

            if ANALYST_PATH_RE.search(line):
                findings.append(
                    LintFinding("FAIL", "analyst-evidence-path", rel, idx, "Absolute or explicit reference pointing into analyst-evidence/")
                )
            elif HOST_HOME_PATH_RE.search(line) and not _is_spec_skeleton_line(line):
                findings.append(
                    LintFinding("WARN", "host-home-path", rel, idx, "Machine-specific user home path present in airlock document")
                )

            if ext in (".md", ".txt") and not in_fence and INLINE_CODE_RE.search(line):
                findings.append(
                    LintFinding("FAIL", "inline-code-snippet", rel, idx, "Inline code / bitwise logic snippet detected outside spec contract")
                )

            if ASM_RE.search(line):
                findings.append(
                    LintFinding("FAIL", "assembly-mnemonic", rel, idx, "Disassembly instruction/register pattern detected")
                )
            elif MEM_ADDR_RE.search(line) and not re.search(r'"[a-f0-9]{64}"', line):
                findings.append(
                    LintFinding("WARN", "memory-address-hex", rel, idx, "4+ digit 0x... hex constant/offset literal detected (verify not raw binary offset)")
                )

            if HEX_DUMP_RE.search(line):
                findings.append(
                    LintFinding("FAIL", "hex-dump", rel, idx, "Raw byte hex dump sequence detected")
                )

            if MINIFIED_JS_RE.search(line) or (len(line) > 350 and ext in (".md", ".txt") and line.count(";") >= 6 and "{" in line):
                findings.append(
                    LintFinding("FAIL", "minified-js", rel, idx, "Minified JavaScript / bundler artifact detected")
                )

            if BASE64_DATA_URI_RE.search(line) or BASE64_LONG_BLOB_RE.search(line):
                findings.append(
                    LintFinding("FAIL", "base64-blob", rel, idx, "Embedded Base64 data URI or encoded payload detected")
                )

            for rule_name, pat in SECRET_PATTERNS:
                if pat.search(line):
                    findings.append(
                        LintFinding("FAIL", rule_name, rel, idx, f"Potential secret, credential, or cookie matched rule {rule_name}")
                    )

            for tok_m in TOKEN_CANDIDATE_RE.finditer(line):
                if _looks_high_entropy_secret(tok_m.group(1)):
                    findings.append(
                        LintFinding("WARN", "high-entropy-token", rel, idx, "High-entropy alphanumeric string detected; verify not an API key or secret")
                    )

            for em in EMAIL_RE.finditer(line):
                domain = em.group(1).lower()
                if domain not in SAFE_EMAIL_DOMAINS:
                    findings.append(
                        LintFinding("WARN", "non-example-email", rel, idx, f"Email address with non-placeholder domain @{domain} detected")
                    )

            for oem in OBFUSCATED_EMAIL_RE.finditer(line):
                norm_dom = re.sub(r"\s*(?:\[\s*dot\s*\]|\(\s*dot\s*\)|\{\s*dot\s*\})\s*", ".", oem.group(1), flags=re.I).lower()
                if norm_dom not in SAFE_EMAIL_DOMAINS:
                    findings.append(
                        LintFinding("WARN", "obfuscated-email", rel, idx, f"Obfuscated email address (@{norm_dom}) detected")
                    )

            # Long verbatim prose heuristic (paragraphs / blockquotes >= 85 words on non-list markdown)
            if ext in (".md", ".txt") and not in_fence:
                is_blockquote = stripped.startswith(">") and not stripped.startswith(("> **Airlock", "> **Process", "> [!"))
                if stripped == "" or stripped.startswith(("#", "|", "-", "*", "```")):
                    if prose_block_words >= 70:
                        findings.append(
                            LintFinding("WARN", "long-verbatim-prose", rel, prose_block_start, f"Long continuous prose paragraph ({prose_block_words} words); verify not verbatim target copy")
                        )
                    prose_block_words = 0
                else:
                    if prose_block_words == 0:
                        prose_block_start = idx
                    prose_block_words += len(stripped.split())
                    if is_blockquote and len(stripped.split()) >= 25:
                        findings.append(
                            LintFinding("WARN", "quoted-verbatim-prose", rel, idx, "Long verbatim blockquote in airlock spec; paraphrase behavior instead")
                        )

        if prose_block_words >= 70:
            findings.append(
                LintFinding("WARN", "long-verbatim-prose", rel, prose_block_start, f"Long continuous prose paragraph ({prose_block_words} words); verify not verbatim target copy")
            )

    has_fail = any(f.severity == "FAIL" for f in findings)
    has_warn = any(f.severity == "WARN" for f in findings)
    status = "FAIL" if has_fail else ("WARN" if has_warn else "PASS")

    canonical_payload = json.dumps(
        {
            "status": status,
            "files_scanned": scanned,
            "findings": [asdict(f) for f in findings],
        },
        sort_keys=True,
    )
    report_hash = hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()

    return {
        "status": status,
        "disclaimer": HEURISTIC_DISCLAIMER,
        "target": str(target),
        "files_scanned": scanned,
        "findings": [asdict(f) for f in findings],
        "report_sha256": report_hash,
    }


def _is_reparse_or_symlink(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        st = os.lstat(path)
        attrs = getattr(st, "st_file_attributes", 0)
        reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x0400)
        return bool(attrs & reparse_flag)
    except OSError:
        return False


def check_isolation(project_dir: Path) -> dict[str, Any]:
    """Check directory separation and host-agent permission snippet presence."""
    project_dir = project_dir.resolve()
    analyst = project_dir / "analyst-evidence"
    airlock = project_dir / "airlock"
    builder = project_dir / "builder-workspace"
    issues: list[dict[str, str]] = []

    for label, d in (("analyst-evidence", analyst), ("airlock", airlock), ("builder-workspace", builder)):
        if not d.exists():
            issues.append({"severity": "WARN", "check": "missing-dir", "message": f"Expected directory missing: {d}"})
        elif _is_reparse_or_symlink(d):
            issues.append({"severity": "FAIL", "check": "symlink-or-junction", "message": f"{label} is a symlink or reparse junction: {d}"})

    if analyst.exists() and builder.exists():
        real_a = Path(os.path.realpath(analyst))
        real_b = Path(os.path.realpath(builder))
        if real_a == real_b:
            issues.append({"severity": "FAIL", "check": "same-directory", "message": "builder-workspace and analyst-evidence resolve to the same path"})
        elif real_b.is_relative_to(real_a):
            issues.append({"severity": "FAIL", "check": "nested-inside-analyst", "message": "builder-workspace resides inside analyst-evidence"})
        elif real_a.is_relative_to(real_b):
            issues.append({"severity": "FAIL", "check": "builder-is-parent", "message": "builder-workspace is a parent of analyst-evidence"})

    if airlock.exists() and analyst.exists():
        real_a = Path(os.path.realpath(analyst))
        real_air = Path(os.path.realpath(airlock))
        if real_a == real_air or real_air.is_relative_to(real_a) or real_a.is_relative_to(real_air):
            issues.append({"severity": "FAIL", "check": "airlock-overlaps-analyst", "message": "airlock and analyst-evidence overlap"})

    # Check common host-agent permission files for explicit analyst-evidence deny rules
    perm_candidates = [
        project_dir / ".claude" / "settings.json",
        project_dir / ".claude" / "settings.local.json",
        project_dir / ".carea" / "permissions.json",
    ]
    perm_found = None
    for p in perm_candidates:
        if p.is_file():
            txt = p.read_text(encoding="utf-8", errors="ignore")
            if "analyst-evidence" in txt:
                perm_found = str(p)
                break

    if perm_found is None:
        issues.append(
            {
                "severity": "WARN",
                "check": "host-agent-permissions-missing",
                "message": "No host-agent permission config denying Lane B access to analyst-evidence/ was found.",
            }
        )

    recommended_claude_snippet = {
        "permissions": {
            "deny": [
                "Read(./analyst-evidence/**)",
                "Edit(./analyst-evidence/**)",
                "Write(./analyst-evidence/**)",
                "Grep(./analyst-evidence/**)",
                "Glob(./analyst-evidence/**)",
            ]
        }
    }

    has_fail = any(i["severity"] == "FAIL" for i in issues)
    has_warn = any(i["severity"] == "WARN" for i in issues)
    status = "FAIL" if has_fail else ("WARN" if has_warn else "PASS")

    return {
        "status": status,
        "project_dir": str(project_dir),
        "permission_config_found": perm_found,
        "issues": issues,
        "recommended_snippets": {
            "claude_settings_json": recommended_claude_snippet,
            "builder_mcp_command": "craft-anything-cli mcp --clean-room",
            "note": "Use Topology (b): run Lane B in a separate fresh session with REA MCP disabled and OS/workspace permissions restricting analyst-evidence/.",
        },
    }
