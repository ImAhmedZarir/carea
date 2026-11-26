# Audit Report: `carea` v1.0 Upgrade (`docs/AUDIT.md`)

**Author:** Ahmed Ishtiaque Zarir  
**Audit Date:** 2026-11-26  
**Target State:** v1.0 Level-1 orchestration pack + zero-dependency Python 3.10+ stdlib CLI

---

## 1. Summary of Changes by Phase

1. **Plan (`docs/PLAN.md`):** Documented phased architecture and justified Python 3.10+ stdlib for `carea` CLI (zero external dependencies, OS portability, separation from Node/Rust external engines).
2. **Phase 1 — Upstream Verification & Compatibility (`39ccfb3`):**
   - Audited all upstream claims in `docs/upstream-facts.md` (`VERIFIED`, `UNVERIFIED`, `WRONG`).
   - Fixed v0.1 inaccuracies: replaced nonexistent `trace_spec` claim with `trace_application_feature` / `trace_javascript_semantics` and exact `specification` contract notes; corrected Craft Anything tool count (`309` -> `303` engine tools / `320` total in `0.6.1`, `322` CLI commands in `0.6.0`); removed ambiguous wildcard tool notations (`build_*`, `project_pin_*`, `inspect_uefi_*`); clarified `craft-anything-cli` vs optional `ca` shortcut.
   - Replaced static "Tested With" claims with `compat/matrix.json`, generated `docs/compatibility.md` (`scripts/render-compatibility.py`), and cross-platform scripts (`scripts/verify-upstream.sh`, `scripts/verify-upstream.ps1`).
3. **Phase 2 — Three Non-Conflicting Entry Points & Multi-Client Manifests (`6e39f32`):**
   - Extracted shared protocols into `skills/_shared/` (`clean-room-protocol.md`, `evidence-handoff.md`, `parity-verification.md`, `responsible-use.md`).
   - Split entry points into `skills/rea/`, `skills/ca/`, and `skills/carea/` with non-overlapping triggers.
   - Updated `.claude-plugin/plugin.json` and added `.codex-plugin/plugin.json` and `.cursor-plugin/plugin.json` verified against `rea-agents-6.10.1` manifest formats.
   - Added `docs/coexistence.md` documenting trigger precedence and duplicate MCP schema avoidance.
4. **Phase 3 — Modes 1–6 & Isolation Topologies (`1a27b26`):**
   - Added `skills/carea/references/modes.md` covering Modes 1–6 (`clean-room-ui`, `two-team-process`, `deep-verification`, `private-deep-rebuild` with mandatory non-clean-room banner, `game-rebuild` with `game_*` Deep-only caveat and no-asset-copy rule, and `android-mobile`).
   - Clarified Lane B Topology `(a)` (CA `rebuild`-spawned agent) vs Topology `(b)` (separate fresh MCP session driving CA `--clean-room`), identifying `(b)` as strictly stronger separation.
5. **Phase 4 — Python 3.10+ Stdlib `carea` CLI (`70c425a`, `.gitignore` `f4b1bd8`):**
   - Implemented `src/carea/` + `pyproject.toml` + wrappers (`scripts/carea`, `scripts/carea.ps1`) providing `init`, `doctor`, `validate-handoff`, `airlock-lint`, `airlock-sign`, `isolation-check`, `spec-draft`, `parity-report`, `return-feedback`, and `mcp-profile`.
   - Enforced `airlock-lint` heuristic disclaimer, `PASS` + `--confirm-human-review` requirement before `airlock-sign`, `passed` requiring both parity axes complete, diff+confirmation guard on `mcp-profile --apply`, and no raw payload copying in `spec-draft`.
6. **Phase 5 — Schema `1.1.0`, Templates & Fixtures (`9db0e4c`):**
   - Upgraded `schemas/carea-handoff.schema.json` to `1.1.0` with stable canonical `$id` while keeping `1.0.0` documents valid; added `topology`, `deep_private` mutual-exclusion rules, `tool_versions`, `airlock.audit`, per-obligation `coverage`/`limitations`, and new modes.
   - Added `schemas/README.md`, 7 positive fixtures (all 6 modes + legacy `1.0.0`), and 7 negative fixtures; updated `templates/` and `examples/`.
7. **Phase 6 — Quality, CI, Governance & Threat Model (`c5042a5`):**
   - Added 7 heuristic leak/clean airlock fixtures (`tests/fixtures/airlock/`), comprehensive unit/hygiene tests (`tests/`), `scripts/check_repo.py` (including known upstream brand SHA-256 & extension ban), `.github/workflows/ci.yml` (3 OSes), `.github/workflows/verify-upstream-weekly.yml`, governance files (`CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, issue/PR templates), `docs/faq.md`, `docs/troubleshooting.md`, and `docs/threat-model.md`.
8. **Phase 7 — Honesty Rewrite & Self-Owned Sample Walkthroughs:**
   - Rewrote `README.md` with clear boundaries, 5-minute quickstarts for `/rea`, `/ca`, `/carea`, mode chooser, and measurable claims.
   - Created self-owned sample target `examples/sample-target/` (`pulse-timer`) and grounded all workflow guides (`docs/workflows/*.md`) strictly in self-owned targets.

---

## 2. Verified on Build Host & GitHub Actions CI

- **Cross-OS GitHub Actions CI (`f9fa6eb`, Run [`45852406649`](https://github.com/ImAhmedZarir/carea/actions/runs/45852406649)):** Completed with **`WORKFLOW_RUN_CONCLUSION_SUCCESS`** in `5m 47s` across all 6 runners (`ubuntu-latest`, `macos-latest`, `windows-latest` × Python `3.10` & `3.12`), including `PyYAML` workflow/frontmatter validation, wheel packaging (`setuptools` + `wheel`), `unittest`, `render-compatibility.py --check`, `check_repo.py`, `verify-upstream.sh`, and `verify-upstream.ps1`.
- **`craft-anything-cli.exe` (`0.6.0`):** `--version`, `doctor`, `commands`, `capabilities --json` (`322` commands, 17 toolsets, `analysis_mode: clean-room`), and subcommand `--help` executed directly.
- **Live MCP & Mode 2 E2E trial on self-owned `examples/sample-target` (`pulse-timer`):**
  - `rea_rea:binary_session` (`6.8.0`-era live MCP) and `rea_rea:analyze_javascript_application` (`ev_835b...`, `parent_evidence_id: ev_7615...`) + `export_evidence_bundle` (`149,804` bytes).
  - `carea spec-draft` on the exported 149 KB REA bundle -> `carea airlock-lint --strict` (`PASS`) -> `carea airlock-sign --confirm-human-review` -> `carea validate-handoff` (`1.1.0`).
  - `craft-anything:core_session_show` (`clean_room: true`, `0.6.0`) and `craft-anything-cli.exe --clean-room --allow-run web-site-open` against local `examples/sample-target/server.py` (Chrome `158.0.8127.38`, `ev_785a...`), followed by `carea parity-report` outputting `partial` (preserving REA's `index.html` inline script coverage note).
- **`airlock-lint` adversarial hardening:** Verified detection of inline code snippets (`if(x>>3&1){y=z^0x5A3C}`), 4+ hex constants/offsets (`0x5A3C`, `0x1F40`), obfuscated emails (`j.smith [at] corp [dot] com`), spaced/prefixed keys (`sk_live_ ...`), and high-entropy alphanumeric tokens via `tests/fixtures/airlock/tp_adversarial_leaks.md` while keeping clean specs `PASS`.
- **Standalone packaging:** Verified `carea-cli` wheel build and clean Python `3.12` venv install + `carea` CLI execution outside the repo checkout.
- **Pinned upstream sources inspected:** `morluto/rea` (`rea-agents-6.10.1`) and `storytold/craft-anything` (`v0.6.1`).

---

## 3. Still Unverified Items & Environmental Gaps

1. **Local `rea` CLI execution (`rea --version`, `rea --help`, `rea doctor`):** **UNVERIFIED** on build host. Host lacks Node.js (`^22.23.4 || ^24.22.1 || >=26.12.1`) and bundled plugin lacked compiled `dist/` runtime. Verified via `rea-agents-6.10.1` upstream source/docs and live `rea_rea` MCP instead.
2. **Local `craft-anything-cli` `0.6.1` binary:** **UNVERIFIED** via local execution (host binary is `0.6.0`; `0.6.1` release docs/tools verified remotely).
3. **Live Mode 5 (Game engine build) & Mode 6 (Android physical/emulator `adb` capture):** Documented with verified command/tool names (`0.6.0` / `6.10.1`), **not executed** end-to-end against live Godot/Unity or an attached `adb` device (`adb` absent on host).
4. **Weekly scheduled cron workflow (`.github/workflows/verify-upstream-weekly.yml`):** YAML validated in CI; scheduled weekly run awaits Monday cron or manual `workflow_dispatch`.

---

## 4. Known Architecture & Process Limitations

- **`carea airlock-lint` is heuristic only:** It catches structural/syntax patterns (code fences, asm, hex dumps, minified JS, base64, assets, secrets, `analyst-evidence/` paths, long prose) and cannot detect semantic paraphrasing of algorithms. Human review (`carea airlock-sign`) remains mandatory.
- **Tool-level clean room is not an OS sandbox or legal defense:** `craft-anything-cli --clean-room` does not constrain host agent shell/read tools (`docs/threat-model.md`).
- **Alpha volatility:** `craft-anything-cli` is early alpha; tool counts and CLI flags may change across upstream releases (`compat/matrix.json` is tracked weekly by CI).
- **Attribution integrity:** MIT (`LICENSE`) applies only to original `carea` materials (`Copyright (c) 2026 Ahmed Ishtiaque Zarir`); trademarks remain reserved in `BRAND.md` and `docs/brand/LICENSE-brand.txt`; upstream notices remain in `NOTICE` and `THIRD_PARTY_NOTICES.md`.
