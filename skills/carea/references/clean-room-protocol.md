# Two-Team Clean Room Process Protocol

> [!IMPORTANT]
> **Process Aid — Not a Legal Guarantee:** This protocol is an engineering workflow aid, **not legal advice and not a legal guarantee of clean-room compliance**. Craft Anything's `--clean-room` mode is a **tool-level rule rather than an operating-system sandbox**, and **a single person or continuous agent session acting as both Analyst and Builder does not create a true legal clean room**. Consult qualified legal counsel when legal clean-room standing is required.

---

## 1. Roles & Workspace Isolation

Use separate directories and separate agent sessions for the two lanes:

```text
<project-root>/
├── analyst-evidence/        # Lane A ONLY: exported REA evidence JSON bundles, logs, captures
├── airlock/                 # Crossing boundary ONLY:
│   ├── clean-room-spec.md   #   Sanitized behavioral spec (human/agent audited)
│   └── carea-handoff.json   #   Validated handoff contract (opaque ev_... IDs only)
├── builder-workspace/       # Lane B ONLY: clean implementation + CA project (.cany / app/)
└── verification/            # Stage 4 ONLY: parity-checklist.md + comparison outputs
```

- **Lane A (Analyst — REA Deep Mode)** may inspect `analyst-evidence/` and the authorized original target. It must **never** write files inside `builder-workspace/`.
- **Lane B (Builder — Craft Anything `--clean-room`)** may read **only** `airlock/clean-room-spec.md`, `airlock/carea-handoff.json`, files inside `builder-workspace/`, and CA Clean-Room observable UI captures. It must **never** read the original target path, source archives, or `analyst-evidence/`.

---

## 2. Step-by-Step Execution

### Step 1: Authorize & Open Analyst Lane (Lane A)
1. Confirm legal ownership or explicit authorization for the target ([DISCLAIMER.md](../../../DISCLAIMER.md)).
2. Run REA in an isolated session (`REA_MCP_TOOL_FAMILIES` scoped to target type, or `hot-cold`).
3. Extract behavioral facts: public/observed API endpoints and value-free payload schemas, state transitions, CLI flags, UI component states, arithmetic/domain rules expressed mathematically, and edge-case behaviors.
4. Build an obligation inventory where applicable (`build_reconstruction_obligation_ledger` for JS/managed targets) and record unresolved gaps (`record_unknown`).
5. Export the full session evidence bundle (`export_evidence_bundle`) into `analyst-evidence/` and close active native sessions (`close_binary`).

### Step 2: Author Sanitized Spec & Handoff
Write `airlock/clean-room-spec.md` using [clean-room-spec.template.md](../../../templates/clean-room-spec.template.md) and `airlock/carea-handoff.json` conforming to [carea-handoff.schema.json](../../../schemas/carea-handoff.schema.json).

**Strict Analyst Prohibitions (Never Cross the Airlock):**
- No raw target source files, minified/unbundled JS snippets, `.NET` IL, or recovered scripts.
- No decompiled C/pseudocode, assembly listings, or literal register/address maps.
- No copied HTML/CSS source trees, proprietary fonts, trademarks, logos, photographs, illustrations, or copyrighted UI copy.
- No private environment secrets, tokens, cookies, or personal data from captures.
- No direct filesystem paths pointing to `analyst-evidence/` inside `clean-room-spec.md` (keep bundle paths confined to the `analyst_lane` metadata section of `carea-handoff.json` if needed only by the Stage 4 Verifier).

### Step 3: Airlock Audit Gate (Mandatory Checkpoint)
Before launching Lane B, run a 5-point inspection on `airlock/clean-room-spec.md` and `airlock/carea-handoff.json`:
1. **Zero code leakage:** Confirm no code blocks reproduce target implementation code or pseudocode (only abstract state machines, formulas, schemas, and test input/output vectors).
2. **Zero asset leakage:** Confirm no logos, media files, or verbatim copyrighted copy appear.
3. **Traceable obligations:** Every requirement has a stable `obl_...` ID, acceptance criteria, and deterministic test vectors.
4. **Honest unknowns:** Unobserved behaviors remain marked `unknown` so Lane B either asks the user or makes an explicit clean design choice.
5. **Schema valid:** `airlock/carea-handoff.json` validates against `schemas/carea-handoff.schema.json` with `airlock.status` set to `"passed"` after review.

### Step 4: Launch Clean Builder Lane (Lane B)
1. Start a **new, separate agent conversation/subagent** so Lane A's memory and raw decompilation context are completely absent.
2. Start Craft Anything strictly in Clean-Room mode: `craft-anything-cli mcp --clean-room` (without `--all-tools`). Verify via `core_session_show` that Clean Room is active.
3. Restrict the Builder agent's filesystem scope to `airlock/` (read-only) and `builder-workspace/` (read-write). Remember that CA's `--clean-room` only governs Craft Anything tools; if your host coding agent has unrestricted shell/file tools (`Read`, `Bash`), configure host permissions or work in an isolated directory/account so those tools cannot access the original target or `analyst-evidence/`.
4. Build the new project inside `builder-workspace/` using CA's rebuild loop (`rebuild_start`, `build_*`, `rebuild_check`) or clean coding tools, generating original replacement visuals (`assets_image_generate` or original artwork).

### Step 5: Independent Verification Gate
1. **Visual / UI checks (CA Clean Room):** Run `web_pixels_compare`, `web_walkthrough_check`, `runtime_captures_compare`, and `rebuild_check`.
2. **Functional / structural parity checks (Verifier / REA):** An independent verification pass (separate from Lane B so Lane B never sees `analyst-evidence/`) evaluates `builder-workspace/` output against the `test_vectors` and `analyst-evidence/` bundle using REA comparison/verification tools ([parity-verification.md](parity-verification.md)) and records results in `verification/parity-checklist.md`.
3. If Lane B needs fixes, return **only** failing test vectors, pixel diffs, or behavioral discrepancy notes — never original code.
