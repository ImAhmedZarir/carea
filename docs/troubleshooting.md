# Troubleshooting Guide (`docs/troubleshooting.md`)

## 1. `carea doctor` reports `[REA] status=missing` or `unsupported`

- Verify Node.js meets `compat/matrix.json` (`^22.23.4 || ^24.22.1 || >=26.12.1`): `node --version`. Note Deno `node_compat` shims or older Node `18/20` installs are not supported by REA `6.10.x`.
- Install upstream CLI globally (`npm install -g rea-agents@6.10.1`) and test `rea doctor --json`.
- If `rea` is installed at a custom path, export `CAREA_REA_BIN=/path/to/rea` or pass `--rea-bin`.

## 2. REA MCP fails on startup after upgrading to `>= 6.10.0`

- Remove `"REA_MCP_INPUT_SCHEMA_PROFILE": "full"` and `"REA_MCP_OUTPUT_SCHEMA_PROFILE": "full"` from your client MCP env.
- Use `"REA_MCP_TOOL_CATALOG_PROFILE": "hot-cold"`, `"REA_MCP_INPUT_SCHEMA_PROFILE": "compact"`, `"REA_MCP_OUTPUT_SCHEMA_PROFILE": "off"` (generate cleanly with `carea mcp-profile rea-hot-cold`).
- For Codex CLI using `hot-cold`, check `mcp_tool_list_changed = true` in `~/.codex/config.toml` per REA's client configuration docs.

## 3. `carea doctor` reports `[Craft Anything] status=missing`

- Download the official `craft-anything-cli` release binary for your OS from `https://github.com/storytold/craft-anything/releases` (or build from source) and add it to `PATH`, or pass `--ca-bin` / set `CAREA_CA_BIN`.
- Always check `craft-anything-cli doctor` afterward to inspect optional sub-engines (`adb`, `ghidra`, `jadx`, `apktool`, `chromium`).

## 4. `carea airlock-lint` reports `WARN` or `FAIL` and blocks `carea airlock-sign`

`carea airlock-sign` intentionally refuses unless `carea airlock-lint` returns strictly `PASS` AND `--confirm-human-review` is provided:

- **`fenced-target-code` / `unlabelled-code-fence`:** Replace code blocks in target languages (`js`, `c`, `rust`, `py`, `smali`, etc.) with mathematical tables, state transition tables, or clean `json` / `http` / `text` API shape blocks.
- **`analyst-evidence-path` / `host-home-path`:** Strip filesystem paths pointing to `analyst-evidence/` or `/Users/...`, `/home/...`, `C:\Users\...`; leave bundle paths solely inside `carea-handoff.json`'s `analyst_lane.analyst_bundle_path`.
- **`memory-address-hex` / `assembly-mnemonic` / `hex-dump`:** Remove raw disassembly offsets (`0x00401200`) and byte dumps; express rules functionally.
- **`non-example-email` / `secret-*`:** Replace real emails/tokens/cookies with `@example.com` placeholders and `<redacted>` tokens.
- **`long-verbatim-prose` / `quoted-verbatim-prose`:** Break long copy/quoted blocks into concise, original bullet requirements.

## 5. Duplicate MCP Tools in Agent Context

If your agent sees duplicate `rea` or `craft-anything` tools, see [`docs/coexistence.md`](coexistence.md): remove either the marketplace plugin MCP config or the duplicate user config installed via `setup`, and omit `--all-tools` on `craft-anything-cli mcp`.

## 6. Android `adb_devices_find` Unavailable

`craft-anything-cli capabilities --json` blocks `adb_*` tools unless Android Platform Tools (`adb`) are installed and on `PATH`. Run `craft-anything-cli doctor` to confirm `adb` detection before running Mode 6 UI captures.
