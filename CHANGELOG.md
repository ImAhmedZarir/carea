# Changelog

All notable changes to `carea` ("Craft And Reverse Engineer Everything") are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2026-11-27

### Added
- **Full-Power `/rea` Atomic Playbooks (`skills/rea/`):** Complete 5-Layer atomic reverse-engineering instruction layer covering all 237+ verified REA server tools & primitives (`inspect_byte_entropy`, `inspect_v8_code_cache`, `inspect_devicetree`, `inspect_uefi_*`, `batch_decompile`, `decompile_all`, `get_call_graph`, `inspect_api_contract`, `compare_static_and_observed_endpoints`, `audit_residual_unknowns`, `open_jeb_project`/`decompile_jeb_item`, `cutter_command`, `execute_rizin_command`, `inspect_with_objdump`, etc.) PLUS all 7 companion reference playbooks inside `skills/rea/references/` (`native-and-artifacts.md`, `javascript-applications.md`, `android-applications.md`, `runtime-observation.md`, `evidence-workflows.md`, `environments.md`, `connection-and-recovery.md`).
- **True 322-Tool / 17-Toolset `/ca` + 1:1 UI Forensics (`skills/ca/`):** Rewrote `skills/ca/SKILL.md` and `skills/ca/references/rebuild-playbook.md` against live verified `craft-anything-cli 0.6.0 --deep capabilities --json` (replacing mismatched tool names with all 322 real CA tools including `[native]`, `[apple]`, `[formats]`/`formats_sbpf_*`/`game_*`, `[managed]` `managed_ilspy_decompile`, `[java]` `java_vineflower_decompile`, `[android]`, `[adb]`, `[browser]` `web_standin_*`, `[javascript]`, `[runtime]`, `[frida]`, `[application]`, `[database]`) and added `skills/ca/references/ui-forensics-playbook.md`.
- **Dual-Engine Master MCP Presets (`compat/matrix.json`, `carea mcp-profile`):** Added `carea-master`, `rea-master` (raised ASAR/matching/capture memory caps), `rea-all-families` (all 19 tool families), and `ca-deep-full` (`--deep --all-tools`) presets with new unit tests.

### Removed
- Deleted `skills/_shared/responsible-use.md` and stripped all pre-flight gatekeeping/authorization-nag filters from `skills/` (`_shared/clean-room-protocol.md`, `carea/references/modes.md`, manifests, and site copy).

## [1.2.0] - 2026-11-27

### Added
- `skills/rea/SKILL.md`: Complete rewrite with full 230+ REA tool catalog routing — zero-engine built-in parsers (Go, Rust, PE suite, ELF suite, IL2CPP, WASM, EVM, SQLite, ML models, Apple IPS, kernel module, kernel build config, Python pyc, Erlang BEAM, Windows shortcut, GPU code objects, ELF core dump, signal recordings, PCAP), container/runtime detection (PyInstaller, Bun compile, Deno compile, NativeAOT, ESP32), full provider rules (IDA: never use .idb/.i64; Kuna: raw_result.source for cached .c/.asm; Ghidra: startup_timeout_ms), SPA cross-origin API detection, summary-first + parent_evidence_id paging, transport truncation recovery, AgentEnv/export_environment_bundle workflow, Fiddler Everywhere .saz, 7-step broader investigation planning, npx -y rea-agents@latest CLI fallback, multi-worker parallelism.
- `skills/ca/SKILL.md`: Complete rewrite with full CA tool catalog — deep mode (--deep) routing, ca triage entry point, core_target_open routing, multi-width capture (375px/768px/1440px), rebuild_start --build-with game mechanics, pixel-perfect verification (web_pixels_compare, web_walkthrough_check, runtime_captures_compare), complete MCP tool reference (120+ tools), Study → Build → Check → Refine production workflow.
- `skills/rea/references/tool-families.md`: Expanded with new families: signals, sqlite, wasm, evm, model, il2cpp, kernel, desktop-build, environments; added zero-engine built-in parsers table.
- `skills/carea/SKILL.md`: Stage 1 REA tool list expanded to full 230+ catalog; responsible-use pre-flight block removed from SKILL.md (doc remains in _shared/responsible-use.md for reference).
- CI fix: replaced `pip install --no-deps --no-build-isolation` with `pip install .` to fix BackendUnavailable on macOS/Windows runners.

### Changed
- Version bumped to `1.2.0` across `pyproject.toml`, `src/carea/__init__.py`, `compat/matrix.json`, `src/carea/data/matrix.json`, all plugin manifests.

## [1.1.0] - 2026-11-27

### Added
- **Reverse-Engineer-Only `/carea <target>` Pipeline (`REA -> CA Study -> Full Breakdown`):**
  - Updated `skills/carea/SKILL.md` and `skills/carea/references/intent-router.md` so invoking `/carea <target>` auto-classifies targets (`.apk`/`.aab`, web URLs/`.asar`, `.exe`/native/managed binaries, games, firmware), executes **Stage 1 (`/rea` internal inspection)** followed by **Stage 2 (`/ca` observable UI/runtime study ONLY)**, and synthesizes `full-breakdown.md`, `architecture.md`, and `design-system.md` **without automatically triggering `rebuild_start` or writing rebuilt app code**.
  - Added `templates/full-breakdown.template.md`, `templates/architecture-report.template.md`, and `templates/design-system.template.md`.
  - Kept clean-room airlock Mode 2 and Modes 1/4/5/6 rebuilds as explicit opt-in tracks.
- **Rebuilt Documentation & Portfolio Web App (`site/`):**
  - Deployed multi-page documentation, interactive Mode/CLI/Airlock workbench, `⌘K` command palette, SEO metadata, and `pulse-timer` portfolio case study via GitHub Pages.

### Fixed
- Prevented Craft Anything study stages inside `/carea` from unexpectedly starting application rebuilds when only reverse engineering analysis and architectural breakdown were requested.

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
