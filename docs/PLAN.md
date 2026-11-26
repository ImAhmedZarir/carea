# `carea` v1.0 Upgrade Plan

Author: Ahmed Ishtiaque Zarir  
Scope: Upgrade `carea` ("Craft And Reverse Engineer Everything") from the v0.1 docs pack to a v1.0 production-grade, independent, unofficial Level-1 orchestration layer over `rea` (`rea-agents`, MIT) and `craft-anything-cli` (`storytold/craft-anything`, MIT OR Apache-2.0).

## Architectural Decisions

1. **Strict Level-1 Boundary (No Vendoring):**
   - `carea` never copies, forks, or redistributes upstream source, binaries, logos, icons, or fonts.
   - Upstream engines run externally via CLI/MCP; CI includes an explicit upstream-asset-ban check.

2. **CLI Implementation Language (`carea` CLI): Python 3.10+ Stdlib Only**
   - **Why Python 3.10+ stdlib over Node:**
     1. Zero npm/third-party runtime dependencies: installs and runs out of the box with standard `python3` across Linux, macOS, and Windows CI runners and airgapped analyst environments.
     2. Runtime isolation: keeping `carea`'s own CLI separate from Node (`rea-agents`, which requires Node 22/24/26) allows `carea doctor`, `airlock-lint`, `validate-handoff`, and `isolation-check` to execute even on hosts without Node `>=22` installed.
     3. Rich built-in primitives (`pathlib`, `os.path.realpath`, `hashlib`, `re`, `argparse`, `json`, `difflib`, `unittest`) cleanly support heuristic scanning, schema checks, symlink/junction detection, and zero-dependency tests.
   - Packaged via `pyproject.toml` (`[project.scripts] carea = "carea.cli:main"`), runnable directly via `python -m carea` or `scripts/carea` / `scripts/carea.ps1` without mandatory pip install.

3. **Fact & Evidence Discipline:**
   - Every referenced upstream tool name, tool family, env var, flag, and version is tracked in `docs/upstream-facts.md` (`VERIFIED` / `UNVERIFIED` / `WRONG`).
   - `UNVERIFIED` claims are removed or kept strictly out of skill prompt text (`skills/**`).
   - Clean-room lanes explicitly remain a **process aid**, never a legal guarantee; `deep_private: true` (Mode 4) outputs loud non-clean-room banners and cannot coexist with clean-room claims.

## Phased Execution Roadmap

### Phase 1: Upstream Fact Verification & Compatibility Matrix
- Audit `craft-anything-cli` locally (`--version`, `commands`, `capabilities --json`, `doctor`, subcommand help) and verify upstream `v0.6.1` docs.
- Record `rea` runtime facts from `rea-agents-6.10.1` upstream docs/source + live `rea_rea` MCP inspection, honestly marking local `rea` CLI runs `UNVERIFIED` where Node `22/24/26` is absent on the current host.
- Produce `docs/upstream-facts.md`, fix `WRONG` claims across existing docs/skills, build `compat/matrix.json`, generate `docs/compatibility.md`, and implement `scripts/verify-upstream.sh` + `scripts/verify-upstream.ps1`.

### Phase 2: Three Entry Points & Multi-Client Plugin Manifests
- Extract shared protocols into `skills/_shared/`.
- Split skills into three non-overlapping entry points: `skills/rea/`, `skills/ca/`, and `skills/carea/` (router + combined pipeline).
- Update `.claude-plugin/plugin.json` and add `.codex-plugin/` and `.cursor-plugin/` manifests verified against upstream `rea` structure (without copying upstream prose/branding).
- Add `docs/coexistence.md` covering trigger precedence, avoiding duplicate MCP tool schemas, and side-by-side upstream setup.

### Phase 3: Six Modes & Isolation Topologies
- Document Modes 1–6 in `skills/carea/references/modes.md`:
  1. Clean-Room UI/Web Rebuild (CA clean-room only)
  2. Two-Team Clean Room (REA Analyst -> Airlock -> CA Builder -> Independent Verifier)
  3. Deep Investigation / Verification / AgentEnv (REA-first, no rebuild claim)
  4. Private Deep Rebuild (REA deep + CA `--deep`, authorized targets only, loud non-clean-room banner)
  5. Game Rebuild Path (Unity/Unreal/Godot, Deep-only `game_*` caveat, authorization gate + no-asset-copy rule)
  6. Android / Mobile App Path (REA `android`/`jadx`/`apktool`/`flutter` logic + CA `adb`/screenshot UI)
- Explicitly document Lane B Topologies **(a)** CA `rebuild`-spawned agent vs **(b)** separate fresh agent session driving CA via `craft-anything-cli mcp --clean-room`, identifying `(b)` as providing stronger isolation.

### Phase 4: Production `carea` CLI (Python 3.10+ Stdlib)
- Implement `src/carea/` (`init`, `doctor`, `validate-handoff`, `airlock-lint`, `airlock-sign`, `isolation-check`, `spec-draft`, `parity-report`, `return-feedback`, `mcp-profile`).
- Ensure `airlock-lint` reports itself strictly as a heuristic gate (PASS/WARN/FAIL with `file:line`), never claiming proof of zero leakage; require `PASS` + human sign-off flag in `carea airlock-sign` before `airlock.status = "passed"`.
- Ensure `mcp-profile` prints snippets by default and shows a unified diff + prompts confirmation before writing when applying to a client config file.

### Phase 5: Handoff Schema v1.1.0, Templates & Fixtures
- Bump `schemas/carea-handoff.schema.json` to `1.1.0` with a stable `$id` while keeping `1.0.0` documents readable in `carea validate-handoff`.
- Add `modes`, `topology`, `airlock.audit`, `tool_versions`, per-obligation `coverage` and `limitations`, and `deep_private` constraint (mutually exclusive with clean-room assertions).
- Add `schemas/README.md` (with `1.0 -> 1.1` migration notes), negative/positive `tests/fixtures/`, and update `templates/` and `examples/` to validate cleanly.

### Phase 6: Tests, CI Workflows, Governance & Threat Model
- Add `unittest` coverage for every CLI subcommand, leak scanner true positives/negatives, schema validation, markdown link checking, JSON/YAML checks, and upstream brand/asset-ban verification.
- Add `.github/workflows/ci.yml` (Linux, macOS, Windows) and `.github/workflows/verify-upstream-weekly.yml`.
- Add `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, issue/PR templates, `docs/faq.md`, `docs/troubleshooting.md`, and `docs/threat-model.md`.

### Phase 7: Documentation Honesty Pass, Worked Walkthroughs & Final Audit
- Rewrite `README.md` with clear scope, 5-minute quickstarts (`/rea`, `/ca`, `/carea`), mode chooser table, and measurable, non-hype claims.
- Build a self-owned public sample target inside `examples/sample-target/` and ground all mode walkthroughs in it (zero third-party proprietary targets).
- Write `docs/AUDIT.md` recording all changes, executed verification checks, unverified items, and open gaps.
