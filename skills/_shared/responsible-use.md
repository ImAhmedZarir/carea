# Responsible Use, Authorization & Evidence Discipline

All workflows under `carea` (`/rea`, `/ca`, `/carea`) coordinate external tools (`rea` and `craft-anything-cli`) and must follow these rules without exception.

## 1. Authorized Targets Only

Analyze, instrument, capture, or reconstruct only:

- Software, websites, packages, or devices you own.
- Targets for which you hold explicit written authorization from the rights holder or system owner.
- Intentionally open-source, self-owned test fixtures, or public educational/CTF targets within published rules.

**Explicitly prohibited:**

- Bypassing or defeating DRM, license checks, paywalls, authentication gates, rate limits, CAPTCHAs, anti-bot protections, or game anti-cheat systems.
- Creating cheats, credential harvesters, unauthorized scraping bots, or payloads that tamper with live third-party services.
- Copying or bundling upstream/target logos, illustrations, photos, fonts, sound/3D assets, or verbatim prose/marketing copy into rebuilt outputs.

## 2. Clean-Room Claims & Process Boundaries

- **Process aid, not legal advice:** `carea`'s Two-Team Clean Room protocol helps organize workflows and reduce accidental code transfer. It is **not legal advice** and does **not** constitute a legal guarantee or copyright defense.
- **Tool-level rule, not an OS sandbox:** Craft Anything's `--clean-room` flag disables internal inspection tools inside that MCP/CLI process. It does not restrict general shell, editor, grep, or file tools available to the host agent unless separately isolated by workspace permissions or containers.
- **Single-operator limit:** One person or one shared context window acting as both Analyst and Builder cannot achieve genuine clean-room independence. Use separate human operators or isolated agent sessions (Topology B) and review `airlock/` outputs manually.
- **Private Deep Rebuild (`deep_private: true`) is NOT clean-room:** Mode 4 combines REA deep analysis with CA `--deep`. Any output produced under Mode 4 MUST display the non-clean-room banner and MUST NEVER carry `clean-room` labels in handoff files, specs, or READMEs.

## 3. Evidence Discipline (Observation / Inference / Unknown)

In every spec, report, handoff record, and parity table:

1. **Observed (`ev_...`):** Cite exact artifact digests, capture records, screenshots, API responses, or decompiler addresses produced in-session.
2. **Inferred:** Label hypotheses or behavioral abstractions clearly as inferences; never cite an inference as an observed fact.
3. **Unknown (`unk_...`):** Preserve unverified, encrypted, obfuscated, dynamic, or skipped behavior explicitly via `record_unknown` / `unknown_ids`. Do not silently fill gaps.
4. **Bounded claims only:** Never present static analysis as runtime proof, UI screenshot similarity as internal logic parity, or partial coverage (`partial`) as full equivalence (`passed`).
