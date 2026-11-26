# Upstream Skill & MCP Coexistence Guide

If you also ran `npx rea-agents setup` or `craft-anything-cli setup` (or installed their official plugins), both upstream skills and `carea`'s skills can exist on the same machine. Follow this guide to prevent duplicate tool schemas and conflicting triggers.

## 1. Trigger Precedence & Skill Names

`carea` exposes three distinct skill folders under `./skills`:

- **`/carea` (`skills/carea`)**: Combined REA -> Airlock -> CA pipelines, mode selection (Modes 1–6), and `carea` CLI gates (`init`, `isolation-check`, `airlock-lint`, `validate-handoff`, `parity-report`).
- **`/rea` (`skills/rea`)**: REA-first forensics, evidence tracking, reconstruction checks, and AgentEnv export without UI rebuild loops.
- **`/ca` (`skills/ca`)**: Craft Anything-first observable capture, clean-room rebuild (`--clean-room`), and pixel/walkthrough checks without binary decompilation.

### Client Precedence Notes

- **Claude Code / Codex / Cursor plugin install of `carea`:** Plugin skills load under the `carea` namespace (for example `/carea:carea`, `/carea:rea`, `/carea:ca`), whereas personal skills installed into `~/.claude/skills/`, `~/.codex/skills/`, or `~/.agents/skills/` by upstream `setup` use top-level names (`rea`, `ca`, `reverse-engineer-anything`). Project-local `.claude/skills/` or explicit `/carea:...` invocation resolves ambiguity immediately.
- If you keep upstream `rea` or `ca` skills installed globally alongside `carea`, invoke **`/carea` explicitly** whenever you want Airlock enforcement, Two-Team isolation, `carea-handoff.json`, or Dual Parity checklists — upstream skills do not know about `carea`'s Airlock gates.

## 2. Keeping Upstream MCP Servers Without Duplicate Skills

Both upstream CLIs let you register MCP tool access **without** installing duplicate skill prompts:

```bash
# Install REA MCP registration only (omit REA's bundled skill)
npx rea-agents@6.10.1 setup --client codex --skill=false --dry-run
# Review plan, then re-run without --dry-run

# Install Craft Anything MCP registration only (omit CA's bundled skill)
craft-anything-cli setup --client codex --clean-room --no-skill --dry-run
# Review plan, then re-run with -y after verification
```

*(Supported upstream `--client` IDs include `claude_code`, `codex`, `cursor`, and others reported by each tool's `setup --help`.)*

## 3. Avoiding Duplicate Tool Schemas in Agent Context

`carea` intentionally ships **no MCP server** in `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, or `.cursor-plugin/plugin.json`. It relies on your existing `rea` and `craft-anything` MCP server registrations.

Watch out for these three traps:

1. **Marketplace Plugin MCP + CLI `setup` MCP Both Active:** Installing upstream REA or Craft Anything Marketplace plugins *and* also running `rea setup` / `craft-anything-cli setup` for the same client registers two copies of the same 264 / 300+ tool schemas under different server names. Disable one registration in your client config or run the upstream `uninstall` command on the redundant copy.
2. **Both Full Catalogs Loaded Together:** Never expose REA's `full` catalog plus Craft Anything `--all-tools` at once. Configure REA with `REA_MCP_TOOL_CATALOG_PROFILE=hot-cold` (or scoped `REA_MCP_TOOL_FAMILIES`) plus `REA_MCP_INPUT_SCHEMA_PROFILE=compact` and `REA_MCP_OUTPUT_SCHEMA_PROFILE=off`, and start CA with `craft-anything-cli mcp --clean-room` (without `--all-tools`).
3. **Two-Team Isolation Leakage (Topology B):** In Mode 2 Lane B (Builder session), configure the Builder client profile with **Craft Anything `--clean-room` ONLY** — remove or disable the `rea` MCP server from the Builder's config profile so Lane B cannot query analyst/decompiler tools by accident. Use `carea mcp-profile <preset>` to inspect minimal config snippets per lane.
