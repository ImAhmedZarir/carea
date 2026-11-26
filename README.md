<p align="center">
  <img src="docs/brand/carea.png" alt="carea logo" width="128" height="128">
</p>

<h1 align="center">carea</h1>

<p align="center">
  <strong>Craft And Reverse Engineer Everything</strong><br>
  <em>"Break It Down. Build It Better."</em>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square"></a>
  <a href="BRAND.md"><img alt="Brand: Trademark Notice" src="https://img.shields.io/badge/brand-trademark%20notice-informational?style=flat-square"></a>
  <a href="DISCLAIMER.md"><img alt="Responsible Use" src="https://img.shields.io/badge/use-authorized%20only-warning?style=flat-square"></a>
</p>

---

**carea** is an open-source, **Level-1 agent skill and orchestration pack** that coordinates two external tools through their own CLI and MCP interfaces:

1. **[REA (`morluto/rea`)](https://github.com/morluto/rea)** — Deep reverse-engineering, binary/runtime instrumentation, evidence ledgers, reconstruction verification, and AgentEnv export (TypeScript / Node.js).
2. **[Craft Anything (`storytold/craft-anything`)](https://github.com/storytold/craft-anything)** — Observable study, clean-room build loop, multi-viewport visual pixel diffing, and project workspace orchestration (Rust, *early alpha*).

`carea` does **not** merge, vendor, fork, or redistribute either upstream codebase or binary. Both engines remain separate external dependencies managed by their official installers.

---

## Core Workflow

`carea` connects deep understanding with clean reconstruction and measurable parity verification:

```text
Observe / Reverse-Engineer (REA or CA)
        │
        ▼
Spec + Obligation Ledger (Sanitized Behavioral Spec + Handoff JSON)
        │
        ▼  [Airlock Boundary]
Clean Rebuild (Craft Anything --clean-room)
        │
        ▼
Visual + Behavioral + Binary Parity Check (CA Pixel Diff + REA Verification)
```

See [`docs/architecture/architecture.md`](docs/architecture/architecture.md) and [`docs/architecture/carea-architecture.mmd`](docs/architecture/carea-architecture.mmd) for the full orchestration model.

---

## Clean-Room & Legal Notice

> [!IMPORTANT]
> `carea`'s Two-Team Clean Room protocol is an **engineering and process aid — NOT legal advice and NOT a legal clean-room guarantee**.
> Craft Anything's `--clean-room` mode is a **tool-level rule rather than an operating-system sandbox**, and **a single person or agent acting as both Analyst and Builder does not constitute a true legal clean room**.
> Read [`DISCLAIMER.md`](DISCLAIMER.md) in full before analyzing any target.

---

## Compatibility & Verification

`carea` tracks supported upstream engine ranges, runtime prerequisites, and verified vs unverified host facts in [`compat/matrix.json`](compat/matrix.json) and renders them into [`docs/compatibility.md`](docs/compatibility.md). Run `scripts/verify-upstream.sh` (or `scripts/verify-upstream.ps1` on Windows) to inspect your locally installed binaries against the matrix.

- **Verified claim ledger:** [`docs/upstream-facts.md`](docs/upstream-facts.md)
- **Generated compatibility matrix:** [`docs/compatibility.md`](docs/compatibility.md) *(single source: [`compat/matrix.json`](compat/matrix.json))*

---

## Getting Started

Install both upstream engines from their official distributions and configure lean MCP profiles (to avoid flooding your agent's context window with 500+ tools) by following [`docs/getting-started.md`](docs/getting-started.md).

### Project Status (Phased Build)

- **Phase 1 (Complete):** Repository skeleton, licensing & trademark governance, responsible-use disclaimer, architecture diagram, and getting-started/MCP profile docs.
- **Phase 2 (v0.2 / v1.0 upgrade in progress):** Multi-client manifests ([`.claude-plugin/plugin.json`](.claude-plugin/plugin.json), [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json), [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json)), non-overlapping skills ([`/carea`](skills/carea/SKILL.md), [`/rea`](skills/rea/SKILL.md), [`/ca`](skills/ca/SKILL.md)), shared protocols ([clean-room](skills/_shared/clean-room-protocol.md), [evidence handoff](skills/_shared/evidence-handoff.md), [parity verification](skills/_shared/parity-verification.md), [responsible use](skills/_shared/responsible-use.md)), [upstream coexistence](docs/coexistence.md), and [intent router](skills/carea/references/intent-router.md).
- **Phase 3 (Complete):** Worked workflow guides ([clean-room UI rebuild](docs/workflows/clean-room-ui-rebuild.md), [two-team clean room](docs/workflows/two-team-clean-room.md), [binary parity & AgentEnv](docs/workflows/binary-parity-rebuild.md)) and validated examples ([sanitized spec](examples/clean-room-spec.example.md), [handoff record](examples/handoff.example.json)).

---

## Licensing & Branding

- **Code, skills, schemas & docs:** Original `carea` materials are licensed under the **[MIT License](LICENSE)** (`Copyright (c) 2026 Ahmed Ishtiaque Zarir`). MIT applies **only** to original `carea` files; upstream engines keep their own licenses and copyrights.
- **Brand & trademarks:** The name **carea**, full title **Craft And Reverse Engineer Everything**, tagline **"Break It Down. Build It Better."**, and logo ([`docs/brand/carea.png`](docs/brand/carea.png)) are trademarks of Ahmed Ishtiaque Zarir and are **not** covered by the MIT License. Forks and modified versions must remove or replace them. See [`BRAND.md`](BRAND.md) and [`docs/brand/LICENSE-brand.txt`](docs/brand/LICENSE-brand.txt).
- **Upstream notices:** Preserved in [`NOTICE`](NOTICE) and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

---

## Credits & Upstream

`carea` is built on top of the capabilities of two independent open-source projects. Please install them from and support their official repositories:

- **REA (Reverse Engineer Anything)** by **morluto** (MIT License)
  - GitHub: <https://github.com/morluto/rea>
  - Website & Guides: <https://rea.tools/>
  - npm Package: <https://www.npmjs.com/package/rea-agents>
- **Craft Anything** by **ArtCraft Team / storytold** and contributors (MIT OR Apache-2.0)
  - GitHub: <https://github.com/storytold/craft-anything>

`carea` is an **independent, UNOFFICIAL project** and is **not** affiliated with, sponsored by, certified by, or endorsed by `morluto` or `ArtCraft Team / storytold`.
