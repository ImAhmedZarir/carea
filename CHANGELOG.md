# Changelog

All notable changes to `carea` ("Craft And Reverse Engineer Everything") are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Planned: run `scripts/verify-upstream.sh` / `.ps1` against global Node `>=22` + `rea-agents@6.10.1` CLI and live Mode 5/6 engine/device trials before final `v1.0.0` tag.

## [1.0.0-rc1] - 2026-11-26

### Added
- Hardened `carea airlock-lint` against inline code snippets (`inline-code-snippet`), 4+ digit hex constants (`0x5A3C`, `0x1F40`), obfuscated emails (`user [at] corp [dot] com`), spaced/prefixed tokens (`sk_live_ ...`), and high-entropy alphanumeric tokens (`tests/fixtures/airlock/tp_adversarial_leaks.md`).
- Verified cross-OS CI matrix (`ubuntu-latest`, `macos-latest`, `windows-latest` × Python `3.10` & `3.12`) green with `setuptools` + `wheel` packaging smoke check.
- Executed live Mode 2 end-to-end verification over `examples/sample-target` (`pulse-timer`) coordinating `rea_rea` MCP + `craft-anything-cli --clean-room` + `carea` CLI.
- **Upstream Fact Ledger & Compatibility Matrix:**
  - `docs/upstream-facts.md` verifying referenced tool names, tool families, environment variables, CLI flags, and versions (`VERIFIED` / `UNVERIFIED` / `WRONG` audit log).
  - Single-source `compat/matrix.json` plus generated `docs/compatibility.md` via `scripts/render-compatibility.py`.
  - Cross-platform verification scripts `scripts/verify-upstream.sh` and `scripts/verify-upstream.ps1`.
- **Three Non-Conflicting Entry Points & Multi-Client Manifests:**
  - Split skills into `skills/rea/`, `skills/ca/`, `skills/carea/`, and shared protocols under `skills/_shared/`.
  - Updated `.claude-plugin/plugin.json` and added `.codex-plugin/plugin.json` and `.cursor-plugin/plugin.json`.
  - Added `docs/coexistence.md` documenting trigger precedence and upstream MCP skill suppression.
- **Modes 1–6 & Isolation Topologies:**
  - Added `skills/carea/references/modes.md` covering Clean-Room UI (`clean-room-ui`), Two-Team Clean Room (`two-team-process`), Deep Investigation / AgentEnv (`deep-verification`), Private Deep Rebuild (`private-deep-rebuild`, `deep_private: true` with mandatory non-clean-room banner), Game Rebuild Path (`game-rebuild` with `game_*` Deep-only caveat), and Android/Mobile (`android-mobile`).
  - Documented Lane B Topologies `(a)` CA `rebuild`-spawned agent vs `(b)` separate fresh MCP session.
- **Zero-Dependency Python 3.10+ Stdlib `carea` CLI:**
  - Added `init`, `doctor`, `validate-handoff`, `airlock-lint`, `airlock-sign`, `isolation-check`, `spec-draft`, `parity-report`, `return-feedback`, and `mcp-profile` (`src/carea/`).
- **Schema `1.1.0` & Verification Suite:**
  - Upgraded `schemas/carea-handoff.schema.json` to `1.1.0` while maintaining `1.0.0` compatibility (`schemas/README.md`).
  - Added positive/negative handoff fixtures and heuristic leak fixtures under `tests/fixtures/`.
  - Added cross-OS CI workflows (`.github/workflows/ci.yml`, `.github/workflows/verify-upstream-weekly.yml`), upstream-asset-ban checks, link/schema/manifest validators, governance docs, and `docs/threat-model.md`.

### Fixed
- Replaced inaccurate v0.1 tool references (`trace_spec` -> `trace_application_feature` / `trace_javascript_semantics` with `specification` contract notes; `309` engine tools -> exact verified `303`/`320` in CA `0.6.1` and `322` commands in CA `0.6.0`; wildcard `build_*` -> explicit verified tool names).
- Updated `.gitignore` so Python bytecode (`__pycache__/`, `*.pyc`) is ignored cleanly.

## [0.1.0] - 2026-11-26

### Added
- Initial repository structure, MIT license (`LICENSE`), trademark terms (`BRAND.md`, `docs/brand/LICENSE-brand.txt`, `docs/brand/carea.png`), upstream attributions (`NOTICE`, `THIRD_PARTY_NOTICES.md`), responsible-use disclaimer (`DISCLAIMER.md`), architecture diagram, initial `/carea` skill, v1.0.0 schema, templates, and starter workflow guides.
