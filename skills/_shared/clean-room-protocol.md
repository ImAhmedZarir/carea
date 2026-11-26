# Two-Team Clean Room Process Protocol

> [!IMPORTANT]
> **Process Aid — Not a Legal Guarantee:** This protocol is an engineering isolation workflow. It is **not legal advice** and does not establish legal independence. Craft Anything's `--clean-room` mode is a tool-level rule rather than an operating-system sandbox, and one operator or shared session playing both Analyst and Builder does not create a true legal clean room.

## 1. Directory Airlock Layout

Initialize every Mode 2 project with `carea init <project-dir>` so four distinct directories exist:

```text
<project-dir>/
├── .carea/config.json       # Mode, paths, topology metadata
├── analyst-evidence/        # Lane A & Stage 4 Verifier only (raw REA bundles, captures, notes)
├── airlock/                 # Audited boundary only: clean-room-spec.md + carea-handoff.json
├── builder-workspace/       # Lane B only: fresh implementation under CA --clean-room
└── verification/            # Stage 4 Parity outputs (parity-checklist.md, diffs)
```

Before Lane B touches `builder-workspace/`, run `carea isolation-check <project-dir>` to confirm `builder-workspace/` is neither a symlink to nor a parent/child of `analyst-evidence/`, and review recommended host-agent permission restrictions.

## 2. Two Supported Topologies for Lane B

Because `craft-anything-cli rebuild` spawns its own coding agent subprocess inside Craft Anything, two isolation topologies exist:

- **Topology A (`rebuild`-spawned agent):** One orchestrator controls Lane A and calls `craft-anything-cli rebuild --clean-room`; Craft Anything's child agent acts as Lane B. *Weaker isolation*: the orchestrator holds both Analyst and Builder visibility unless restarted cleanly, and `rebuild`'s prompt/session history originates from the same operator/workspace.
- **Topology B (Separate fresh agent session driving CA via MCP — Recommended):** Lane A runs in Session 1 and stops after passing the Airlock. Lane B starts in a **fresh Session 2** configured solely with `craft-anything-cli mcp --clean-room` (without REA MCP, without `--all-tools`), restricted read-only to `airlock/` and read-write to `builder-workspace/`. *Stronger isolation*: context window, conversation memory, and inspection tool permissions are structurally separated from `analyst-evidence/`.

See [carea modes guide](../carea/references/modes.md#lane-b-topologies-a-vs-b) for full setup details.

## 3. Stage-by-Stage Workflow

### Stage 1 — Lane A (Analyst using REA)

1. Verify authorization per [responsible-use.md](responsible-use.md).
2. Run REA in an isolated session (`REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` or target-scoped `REA_MCP_TOOL_FAMILIES`, with `REA_MCP_INPUT_SCHEMA_PROFILE=compact` and `REA_MCP_OUTPUT_SCHEMA_PROFILE=off`).
3. Gather evidence (`ev_...`), track gaps (`record_unknown` -> `unk_...`), and build an obligation ledger (`build_reconstruction_obligation_ledger` where applicable).
4. Save raw bundles (`export_evidence_bundle`) inside `analyst-evidence/` only, then close native/debugger sessions (`close_binary`, `close_frida_session`, `close_gdb_session`, `close_rizin_session` if active).

### Stage 2 — Airlock Drafting, Heuristic Lint & Human Sign-Off

1. Generate a sanitized `DRAFT` skeleton from the exported bundle:
   `carea spec-draft analyst-evidence/bundle.json --out airlock/clean-room-spec.md`
   *(Copies IDs and structure only — never raw code, payloads, or strings.)*
2. Author observable behavior, state machines, API shapes, error cases, unknowns, and test vectors in `airlock/clean-room-spec.md`, keeping all raw source, pseudocode, disassembly, hex dumps, secrets, copied prose, and `analyst-evidence/` filesystem paths out.
3. Populate `airlock/carea-handoff.json` matching [`schemas/carea-handoff.schema.json`](../../schemas/carea-handoff.schema.json).
4. Run heuristic leakage scan + schema check:
   `carea airlock-lint airlock/`
   `carea validate-handoff airlock/carea-handoff.json`
   *(Note: `airlock-lint` is a heuristic gate, not proof of zero leakage. Human review is required.)*
5. Only after `airlock-lint` returns `PASS` and a human reviewer inspects `airlock/`, run:
   `carea airlock-sign airlock/carea-handoff.json --reviewer "<name>"`
   which computes the lint/spec digest, updates `airlock.audit`, and sets `airlock.status = "passed"`.

### Stage 3 — Lane B (Builder using Craft Anything `--clean-room`)

1. Run `carea isolation-check <project-dir>`.
2. Start Craft Anything with `--clean-room` (without `--all-tools`) and confirm `clean_room: true` via `core_session_show`.
3. Provide Lane B **only** `airlock/clean-room-spec.md`, `obligations[]` from `airlock/carea-handoff.json`, and approved observable UI inputs when applicable.
4. Build inside `builder-workspace/` using `rebuild_start` or `build_files_list`, `build_file_read`, `build_file_write`, `build_file_edit`, `build_checklist`, `build_command_run`, generating replacement visual assets with `assets_image_generate` or original SVGs/styles.

### Stage 4 — Dual Parity & Lane-B-Safe Return Feedback

1. Run Craft Anything visual/UI checks (`rebuild_check`, `web_pixels_compare`, `web_walkthrough_check`, `runtime_captures_compare`) and REA behavioral/structural verification (`verify_reconstruction`, `evaluate_reconstruction_coverage`, `compare_web_captures`, `compare_functions`, `compare_artifacts`) following [parity-verification.md](parity-verification.md).
2. Merge both check axes with `carea parity-report` into `verification/parity-checklist.md`.
3. If rebuilt behavior fails verification, generate sanitized Lane-B feedback using `carea return-feedback` — passing only failing test vectors, expected vs observed API/pixel diffs, never source code or decompiler output from `analyst-evidence/`.
