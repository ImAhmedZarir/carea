# Security & Responsible Use Policy

## Scope of Authorized Use

`carea` coordinates **REA** and **Craft Anything** strictly for authorized software understanding, interoperability research, security review, migration of owned software, and educational clean-room practice.

`carea` does not execute exploitation payloads, bundle reverse-engineering binaries, or automate DRM/license/anti-cheat/CAPTCHA bypasses. Please do not submit issues, workflows, or examples targeting unauthorized commercial products or live services.

## Reporting Vulnerabilities in `carea` Itself

If you discover a security bug in `carea` (for example: path traversal, command injection, unsafe file overwrite in `carea init` / `mcp-profile --apply`, or bypasses in `carea airlock-lint` / `carea isolation-check`):

1. **Do not** open a public issue containing exploit payloads or private credentials.
2. Open a private security advisory on GitHub (<https://github.com/ImAhmedZarir/carea/security/advisories/new>) or contact the repository maintainer (**Ahmed Ishtiaque Zarir**) directly via GitHub with:
   - Affected file/command (`carea` CLI or workflow script)
   - Minimal reproduction steps using self-owned/dummy files
   - Suggested remediation if known

## Reporting Upstream Engine Bugs

Issues inside the underlying **REA** or **Craft Anything** engines (such as binary parsers, Ghidra/Frida bridges, Playwright/Chromium sandboxes, or `craft-anything-cli` subprocess agents) should be reported directly to those projects:

- **REA (`morluto/rea`):** <https://github.com/morluto/rea/security>
- **Craft Anything (`storytold/craft-anything`):** <https://github.com/storytold/craft-anything>

## Known Airlock Security Boundaries

As documented in [`docs/threat-model.md`](docs/threat-model.md), `carea airlock-lint` is a heuristic scanner and `craft-anything-cli --clean-room` is a tool-level policy, not a security boundary against a compromised or misconfigured host environment.
