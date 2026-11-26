# Frequently Asked Questions (`docs/faq.md`)

### Is `carea` a legal clean-room solution?
No. `carea` is an engineering process aid (`DISCLAIMER.md`). `craft-anything-cli --clean-room` is a tool-level setting rather than an OS sandbox, `carea airlock-lint` is a heuristic check, and one operator acting as both Analyst and Builder never makes a legal clean room.

### Does `carea` include REA or Craft Anything?
No. `carea` is an independent Level-1 orchestration pack (`MIT`, `Ahmed Ishtiaque Zarir`). You install `rea` (`rea-agents`, MIT) and `craft-anything-cli` (`storytold/craft-anything`, MIT OR Apache-2.0) separately from their official upstream releases. `carea` checks `compat/matrix.json` at runtime.

### Why did `carea init` create 4 directories (`analyst-evidence/`, `airlock/`, `builder-workspace/`, `verification/`)?
Separating raw analysis outputs (`analyst-evidence/`), sanitized behavioral specifications (`airlock/`), clean rebuild source code (`builder-workspace/`), and dual-axis verification (`verification/`) prevents accidental file reads and allows `carea isolation-check` and `carea airlock-lint` to verify boundaries mechanically.

### Why does REA reject `REA_MCP_INPUT_SCHEMA_PROFILE=full` in `>= 6.10.0`?
Starting in `rea-agents` `6.10.0`, REA intentionally removed `full` input and output schema profiles (`compact` or `off` are accepted instead) to stop clients from blowing past context and SSE payload budgets. Run `carea doctor --client-config <path>` to catch stale `full` settings automatically.

### Why is `rea` reported as `missing` on my machine even though an IDE plugin exists?
Some editor extensions bundle plugin files without globally installing `rea` on `PATH` or without Node.js `^22.23.4 || ^24.22.1 || >=26.12.1` + compiled `dist/` runtime. Install the official CLI cleanly with `npm install -g rea-agents@6.10.1` or set `CAREA_REA_BIN`.

### Can I rely on a `ca` shortcut command on Windows/macOS/Linux?
Do not assume `ca` is always installed. `craft-anything-cli` is the canonical upstream executable (`craft-anything-cli --version`, `craft-anything-cli mcp --clean-room`). In agent chat prompts, `/ca` invokes `carea`'s Craft Anything-first skill.

### Why did `carea parity-report` mark an obligation `partial` when `rebuild_check` passed?
By rule, `carea parity-report` marks an obligation `passed` **only** when both Axis 1 (Craft Anything observable check) and Axis 2 (REA behavioral/structural verification) complete cleanly with no partial coverage (`coverage.scope != "partial"`) or unresolved limitations. Single-axis checks honestly report `partial` or `unknown`.
