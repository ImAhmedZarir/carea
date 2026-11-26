# Getting Started with `carea`

`carea` is a lightweight orchestration layer. Before using it, install **REA** and **Craft Anything** directly from their official upstream releases. `carea` does not bundle or mirror either upstream binary.

---

## 1. Compatibility & Version Pinning

| Engine | Tested With | Minimum Compatible | Runtime / Toolchain Notes |
|---|---|---|---|
| **REA** (`rea-agents`) | `6.10.1` | `6.8.0+` | Node.js `^22.23.4 \|\| ^24.22.1 \|\| >=26.12.1` and `npm`. Optional native backends (Ghidra `12.2` with JDK `25+`, Hopper, IDA Pro, Kuna `1.1000`, JADX, Frida, etc.) are bring-your-own. |
| **Craft Anything** (`craft-anything-cli`) | `0.6.1` *(upstream release)* / `0.6.0` *(local binary)* | `0.6.0+` | **Early alpha.** Prebuilt installers/portable archives from GitHub Releases, or Rust `1.97+` to build from source. Optional external engines include Ghidra, JADX, Apktool, adb, Frida, and a Chromium browser. |

> [!NOTE]
> **Version Pinning Advice:** Pin exact versions when reproducibility matters across team workflows. In `REA >= 6.10.0`, `evidence_format: 2` is required (`6.8.x` bundles cannot be re-imported directly without regenerating observations) and `REA_MCP_INPUT_SCHEMA_PROFILE=full` / `REA_MCP_OUTPUT_SCHEMA_PROFILE=full` are rejected at startup.

---

## 2. Official Upstream Installation

### Step A — Install REA (`morluto/rea`)

Official sources: <https://github.com/morluto/rea> · <https://rea.tools/> · <https://www.npmjs.com/package/rea-agents>

```bash
# Option 1: Interactive agent setup (recommended by upstream)
npx rea-agents@6.10.1 setup

# Option 2: Global CLI installation (pinned to verified release)
npm install --global rea-agents@6.10.1

# Verify installation and provider readiness
rea --version
rea doctor
```

### Step B — Install Craft Anything (`storytold/craft-anything`)

Official source: <https://github.com/storytold/craft-anything> *(early alpha)*

Install via official binaries from the [Craft Anything GitHub Releases](https://github.com/storytold/craft-anything/releases), or build from source with Rust `1.97+`:

```bash
git clone https://github.com/storytold/craft-anything
cd craft-anything
cargo install --path apps/craft-anything-cli

# Verify installation, coding agents, and tool availability
craft-anything-cli --version
craft-anything-cli doctor
craft-anything-cli capabilities
```

*(Note: Craft Anything's `ca` command shortcut may also be created depending on your install method; run `craft-anything-cli doctor` to confirm.)*

---

## 3. Lean MCP Profile Presets (Preventing Tool Bloat)

Loading every tool from both servers exposes **500+ tools** at once (`309` engine tools plus AI/setup tools in Craft Anything, plus `200+` tools in REA), which degrades model tool selection and consumes excessive context tokens.

`carea` does **not** ship a hardcoded `mcp_config.json` with machine-specific paths. Instead, merge the preset snippets below into your MCP client configuration using your own local executables.

### Craft Anything (`craft-anything-cli mcp`)

- **Always omit `--all-tools` by default.** Running `craft-anything-cli mcp` without `--all-tools` exposes only `core` (Essentials) plus enabled toolsets instead of all 320+ commands.
- **For the Builder Lane (Clean-Room):** Always include `--clean-room` so deep internal inspection tools remain unavailable (`available: false`).

```json
{
  "mcpServers": {
    "craft-anything-clean-room": {
      "command": "craft-anything-cli",
      "args": ["mcp", "--clean-room"]
    }
  }
}
```

*(When intentionally working in Deep mode outside Clean-Room builds, swap `--clean-room` for `--deep`.)*

### REA (`rea`) — Recommended Context-Saving Presets

#### Preset 1: `hot-cold` On-Demand Discovery (`rea >= 6.10.x`)

Starts with only five discovery/session tools (`binary_session`, `open_binary`, `close_binary`, `get_evidence_bundle`, `discover_tools`) and loads domain tools only when requested:

```json
{
  "mcpServers": {
    "rea": {
      "command": "rea",
      "args": ["mcp"],
      "env": {
        "REA_MCP_TOOL_CATALOG_PROFILE": "hot-cold",
        "REA_MCP_INPUT_SCHEMA_PROFILE": "compact",
        "REA_MCP_OUTPUT_SCHEMA_PROFILE": "off"
      }
    }
  }
}
```

*(Verify your client supports `notifications/tools/list_changed`; if loaded cold tools do not appear automatically, switch to Preset 2 below.)*

#### Preset 2: Scoped Tool Families (`REA_MCP_TOOL_FAMILIES`)

Compatible with both `6.8.x` and `6.10.x`. Valid family IDs in `6.10.1` are:
`direct`, `enhanced`, `native`, `artifact`, `managed`, `firmware`, `uefi`, `android`, `pcap`, `flutter`, `frida`, `apktool`, `jeb`, `adb`, `browser`, `electron`, `javascript-runtime`, `application`, `session`.

*(Note: `uefi` was added in `6.10.0`; omit `uefi` if running `6.8.x`. Always include `session` whenever opening targets or managing Evidence bundles, and `application` when paging via `inspect_analysis_view`.)*

| Workflow Focus | `REA_MCP_TOOL_FAMILIES` Preset |
|---|---|
| **Web / Electron / JS Analyst** | `browser,electron,application,javascript-runtime,session` |
| **Native Binary Analyst** | `native,enhanced,application,session` *(add `direct` if needed)* |
| **Android APK Analyst** | `android,adb,apktool,session` *(add `flutter`, `frida`, or `jeb` as needed)* |
| **Managed .NET Analyst** | `managed,session` |
| **Firmware / UEFI Analyst** | `firmware,uefi,session,direct` |
| **Evidence & Verification Only** | `session,application` |

Example MCP entry (or configure via `rea setup --client <id> --tool-families <ids>`):

```json
{
  "mcpServers": {
    "rea": {
      "command": "rea",
      "args": ["mcp"],
      "env": {
        "REA_MCP_TOOL_FAMILIES": "browser,electron,application,javascript-runtime,session",
        "REA_MCP_INPUT_SCHEMA_PROFILE": "compact",
        "REA_MCP_OUTPUT_SCHEMA_PROFILE": "off"
      }
    }
  }
}
```

> [!WARNING]
> Do **not** set `REA_MCP_INPUT_SCHEMA_PROFILE=full` or `REA_MCP_OUTPUT_SCHEMA_PROFILE=full` when running `rea >= 6.10.0` — upstream removed `full` profiles and refuses startup if either is set.

---

## 4. Quick Readiness Verification

Before running a `carea` workflow, verify both independent engines respond cleanly:

```bash
rea doctor
craft-anything-cli doctor
```

Remember to review [`../DISCLAIMER.md`](../DISCLAIMER.md) before inspecting any target.
