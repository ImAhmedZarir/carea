# Threat & Leakage Model for Two-Team Workflows (`docs/threat-model.md`)

> [!IMPORTANT]
> **Baseline Reality:** `carea` is an **engineering process aid**, not an OS sandbox or legal clean-room defense. Whenever raw target knowledge and clean-room reconstruction exist on the same developer workstation or under the same human/AI operator, real leakage channels remain.

---

## 1. Threat Actors & Leakage Goals Protected Against

1. **Accidental Context Contamination:** A coding model building in `builder-workspace/` inadvertently reads decompiler strings, obfuscated JS, copied UI stylesheets, or proprietary API payloads from `analyst-evidence/`.
2. **Tool-Assisted Bypass:** A Builder session retains active `rea` MCP tools or `--deep` flags in Craft Anything and directly queries internal files instead of building from `airlock/clean-room-spec.md`.
3. **Artifact & Credential Spill:** Captured cookies, bearer tokens, screenshots with user PII, raw binaries, fonts, or `analyst-evidence/` paths are committed into `airlock/` or `builder-workspace/`.
4. **False Clean-Room Attribution:** Outputs built under Mode 4 (`private-deep-rebuild`, `deep_private: true`) or extracted via `--deep` `game_*` tools are mistakenly labeled clean-room.

---

## 2. Concrete Leakage Paths, Mitigations & Residual Risk

| Leakage Path | How Leakage Happens | Mitigation in `carea` | Honest Residual Risk |
| --- | --- | --- | --- |
| **1. Host-agent tools (`Read`, `Grep`, `Glob`, `Bash`, editors)** | Coding agents typically hold native host file tools outside MCP; `--clean-room` in `craft-anything-cli` only disables CA's internal tools, NOT host file tools. | Run `carea isolation-check` before Lane B to detect symlinks/parent-child overlap and emit explicit deny snippets (`.claude/settings.local.json`) blocking `./analyst-evidence/**`. | **High if single OS account:** An unrestricted shell tool or subshell command (`cat ../analyst-evidence/...`) can still read disk unless run inside separate OS users, containers, or VMs. |
| **2. Shared LLM conversation memory** | In a single continuous agent thread, Lane B sees earlier Analyst tool outputs, decompiled snippets, and reasoning directly in context. | Use **Topology `(b)`** (`modes.md`): finish Lane A, close session completely, and start Lane B in a brand-new fresh session without REA MCP configured. | **Residual in Topology `(a)`:** `craft-anything-cli rebuild` spawns a child agent from a parent orchestrator prompt; phrasing and request hints originate in the parent session. |
| **3. System clipboard** | Copying snippets manually from Ghidra/REA terminal into prompts or `clean-room-spec.md`. | Generate spec skeletons strictly via `carea spec-draft` (copies opaque IDs only) and inspect diffs before committing `airlock/`. | **Unmitigated technically:** Host OS clipboard contents cannot be audited by `carea`. Human discipline is required. |
| **4. Agent logs, transcripts & shell history** | `~/.bash_history`, PowerShell `PSReadLine` logs, and AI session transcripts capture prior REA commands, string searches, or target source paths. | Pass evidence paths cleanly via JSON files inside `analyst-evidence/`; avoid pasting large proprietary payloads onto command lines. Keep Lane B inside a clean OS user or ephemeral runner when strict separation matters. | **High on shared workstation:** Any host-level agent with shell access on the same user profile could query shell history or IDE transcript directories unless OS-isolated. |
| **5. Craft Anything's spawned agent (`rebuild`)** | `craft-anything-cli rebuild` starts a coding agent (`--backend`) working in `--project-folder`. | Pass `--clean-room`, omit `--all-tools`, avoid pointing `--project-folder` near `analyst-evidence/`, and prefer **Topology `(b)`** (`craft-anything-cli mcp --clean-room`) over unattended `--rebuild`. | Child agent shares the same workstation user identity and environment variables unless isolated by containerization. |
| **6. REA evidence bundles on disk** | `export_evidence_bundle` writes complete `normalized_result` & provenance JSON inside `analyst-evidence/`. | `carea airlock-lint` fails immediately on `analyst-evidence` path references, binary/media assets, hex dumps, code fences, base64 blobs, minified JS, and secrets; `carea spec-draft` drops `raw_result` / `source` / `bytes`. | **Heuristic limit:** Semantic paraphrases of proprietary algorithms (`airlock-lint` cannot read intent) require human review (`carea airlock-sign`) to detect close translation. |
| **7. Mixed clean-room vs `deep_private` metadata** | Labeling a deep-assisted rebuild as clean-room in downstream docs. | Schema `1.1.0` & `carea validate-handoff` reject `deep_private: true` paired with clean-room modes, `airlock.status: "passed"`, or `clean_room_verified: true`. Mode 4 prepends loud `NOT CLEAN-ROOM` banners automatically. | Downstream consumers could ignore warnings if manually stripped outside git/schema validation. |

---

## 3. Recommended Hardened Workstation Checklist

For teams needing stronger practical separation than basic directory conventions:

1. Run **Lane A** (`rea`) and **Lane B** (`craft-anything-cli mcp --clean-room`) under **separate OS accounts or separate containers** mounting `airlock/` read-only into Lane B (never mounting `analyst-evidence/` at all in Lane B's container).
2. Always verify **Topology `(b)`** with `carea isolation-check`, `carea airlock-lint --strict`, `carea validate-handoff`, and human review (`carea airlock-sign`).
3. Treat every `--clean-room` output as engineering hygiene only — obtain formal legal counsel if third-party IP separation is a legal requirement.
