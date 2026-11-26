/* carea Docs & Portfolio interactive helpers (theme toggle, mobile drawer, copy, mode explorer, search) */
(function () {
  "use strict";

  const MODE_DATA = {
    "two-team-process": {
      badge: "Recommended · Mode 2",
      skill: "/carea",
      cleanRoom: "Process aid (Topology b)",
      summary: "REA inspects internals in analyst-evidence/; carea enforces spec-draft + airlock-lint + human sign; fresh CA --clean-room session rebuilds.",
      cmd: "carea init ./my-app --mode two-team-process --topology b\ncarea isolation-check ./my-app\ncarea airlock-lint ./my-app/airlock --strict\ncarea airlock-sign ./my-app/airlock/carea-handoff.json --reviewer \"Ahmed\" --confirm-human-review",
    },
    "clean-room-ui": {
      badge: "Observable · Mode 1",
      skill: "/ca",
      cleanRoom: "CA --clean-room only",
      summary: "Delegates straight to Craft Anything in --clean-room mode to capture responsive screens and build original UIs without reading source.",
      cmd: "carea mcp-profile ca-clean-room\ncraft-anything-cli rebuild http://127.0.0.1:4173/ \"Build responsive timer UI\" --clean-room",
    },
    "deep-verification": {
      badge: "Forensics · Mode 3",
      skill: "/rea",
      cleanRoom: "Analysis only (no rebuild)",
      summary: "Delegates to REA with lean hot-cold / family-scoped profiles for static/runtime evidence ledgers, verify_reconstruction, and AgentEnv.",
      cmd: "carea mcp-profile rea-hot-cold\n# Invoke /rea -> open_binary / analyze_javascript_application / verify_reconstruction",
    },
    "private-deep-rebuild": {
      badge: "NOT CLEAN-ROOM · Mode 4",
      skill: "/carea",
      cleanRoom: "NO (deep_private: true)",
      summary: "For owned codebases only: permits REA deep + CA --deep inspection and prepends loud NOT CLEAN-ROOM banners in specs and parity reports.",
      cmd: "carea init ./own-migration --mode private-deep-rebuild --topology a\ncraft-anything-cli rebuild http://127.0.0.1:4173/ \"Port internal app\" --deep",
    },
    "game-rebuild": {
      badge: "Unity / Godot / Rust · Mode 5",
      skill: "/carea or /ca",
      cleanRoom: "Only without game_* / --deep",
      summary: "Rebuilds game mechanics with original generated artwork. Note CA game_* asset extraction tools are Deep-only and asset copying is banned.",
      cmd: "carea init ./arcade --mode game-rebuild --topology b\ncraft-anything-cli rebuild ./game-capture \"Rebuild mechanics\" --build-with godot --clean-room --generate-assets",
    },
    "android-mobile": {
      badge: "Hybrid Mobile · Mode 6",
      skill: "/carea",
      cleanRoom: "Only across Airlock",
      summary: "Pairs REA android/apktool/flutter logic inspection with Craft Anything adb screenshot and window captures across authorized APKs/emulators.",
      cmd: "carea init ./mobile-rebuild --mode android-mobile --topology b\ncarea mcp-profile rea-android",
    },
  };

  const MCP_PRESETS = {
    "rea-hot-cold": {
      mcpServers: {
        rea: {
          command: "npx",
          args: ["-y", "rea-agents@6.10.1", "mcp"],
          env: {
            REA_MCP_TOOL_CATALOG_PROFILE: "hot-cold",
            REA_MCP_INPUT_SCHEMA_PROFILE: "compact",
            REA_MCP_OUTPUT_SCHEMA_PROFILE: "off",
          },
        },
      },
    },
    "rea-web": {
      mcpServers: {
        rea: {
          command: "npx",
          args: ["-y", "rea-agents@6.10.1", "mcp"],
          env: {
            REA_MCP_TOOL_FAMILIES: "browser,electron,application,javascript-runtime,session",
            REA_MCP_INPUT_SCHEMA_PROFILE: "compact",
            REA_MCP_OUTPUT_SCHEMA_PROFILE: "off",
          },
        },
      },
    },
    "rea-android": {
      mcpServers: {
        rea: {
          command: "npx",
          args: ["-y", "rea-agents@6.10.1", "mcp"],
          env: {
            REA_MCP_TOOL_FAMILIES: "android,apktool,jeb,flutter,frida,adb,application,session",
            REA_MCP_INPUT_SCHEMA_PROFILE: "compact",
            REA_MCP_OUTPUT_SCHEMA_PROFILE: "off",
          },
        },
      },
    },
    "ca-clean-room": {
      mcpServers: {
        "craft-anything": {
          command: "craft-anything-cli",
          args: ["mcp", "--clean-room"],
        },
      },
    },
    "ca-restricted-web": {
      mcpServers: {
        "craft-anything": {
          command: "craft-anything-cli",
          args: ["mcp", "--clean-room", "--restricted", "--allow-web", "--allow-capture"],
        },
      },
    },
    "ca-deep-private": {
      mcpServers: {
        "craft-anything": {
          command: "craft-anything-cli",
          args: ["mcp", "--deep"],
        },
      },
    },
  };

  function setupThemeToggle() {
    const btn = document.getElementById("theme-toggle");
    if (!btn) return;
    const label = btn.querySelector("[data-theme-label]");
    const syncLabel = () => {
      const dark = document.documentElement.classList.contains("dark");
      btn.setAttribute("aria-pressed", String(dark));
      if (label) label.textContent = dark ? "Dark" : "Light";
    };
    syncLabel();
    btn.addEventListener("click", () => {
      const dark = document.documentElement.classList.toggle("dark");
      try {
        localStorage.setItem("carea-theme", dark ? "dark" : "light");
      } catch (_) {}
      syncLabel();
    });
  }

  function setupMobileDrawer() {
    const btn = document.getElementById("mobile-menu-toggle");
    const drawer = document.getElementById("mobile-drawer");
    if (!btn || !drawer) return;
    btn.addEventListener("click", () => {
      const open = drawer.hasAttribute("hidden");
      if (open) {
        drawer.removeAttribute("hidden");
        btn.setAttribute("aria-expanded", "true");
      } else {
        drawer.setAttribute("hidden", "");
        btn.setAttribute("aria-expanded", "false");
      }
    });
  }

  function setupCopyButtons() {
    document.querySelectorAll("[data-copy-target], .copy-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const box = btn.closest(".code-box");
        const codeEl = box ? box.querySelector("pre") : null;
        if (!codeEl) return;
        const text = codeEl.textContent || "";
        try {
          await navigator.clipboard.writeText(text);
          const prev = btn.textContent;
          btn.textContent = "Copied";
          setTimeout(() => {
            btn.textContent = prev || "Copy";
          }, 1500);
        } catch (_) {
          btn.textContent = "Select";
        }
      });
    });
  }

  function setupHomeModePreview() {
    const buttons = document.querySelectorAll("[data-preview-mode]");
    const out = document.getElementById("mode-preview-panel");
    if (!buttons.length || !out) return;
    const render = (key) => {
      const m = MODE_DATA[key];
      if (!m) return;
      buttons.forEach((b) => {
        const active = b.getAttribute("data-preview-mode") === key;
        b.setAttribute("aria-selected", String(active));
        b.classList.toggle("active", active);
      });
      out.querySelector("[data-preview-badge]").textContent = m.badge;
      out.querySelector("[data-preview-skill]").textContent = m.skill;
      out.querySelector("[data-preview-clean]").textContent = m.cleanRoom;
      out.querySelector("[data-preview-summary]").textContent = m.summary;
      out.querySelector("[data-preview-cmd]").textContent = m.cmd;
    };
    buttons.forEach((b) =>
      b.addEventListener("click", () => render(b.getAttribute("data-preview-mode")))
    );
  }

  function setupQuickstartTabs() {
    const tabs = document.querySelectorAll("[data-qs-tab]");
    if (!tabs.length) return;
    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        const target = tab.getAttribute("data-qs-tab");
        tabs.forEach((t) => {
          const active = t === tab;
          t.setAttribute("aria-selected", String(active));
          t.classList.toggle("active", active);
        });
        document.querySelectorAll("[data-qs-panel]").forEach((p) => {
          p.hidden = p.getAttribute("data-qs-panel") !== target;
        });
      });
    });
  }

  function setupMcpProfileViewer() {
    const btns = document.querySelectorAll("[data-mcp-preset]");
    const pre = document.getElementById("mcp-profile-output");
    if (!btns.length || !pre) return;
    const select = (key) => {
      const obj = MCP_PRESETS[key];
      if (!obj) return;
      btns.forEach((b) => {
        const active = b.getAttribute("data-mcp-preset") === key;
        b.setAttribute("aria-selected", String(active));
        b.classList.toggle("active", active);
      });
      pre.textContent = JSON.stringify(obj, null, 2);
    };
    btns.forEach((b) => b.addEventListener("click", () => select(b.getAttribute("data-mcp-preset"))));
    select("rea-hot-cold");
  }

  function setupSearchFilter() {
    const input = document.getElementById("filter-search");
    if (!input) return;
    const items = document.querySelectorAll("[data-filter-item]");
    input.addEventListener("input", () => {
      const q = input.value.trim().toLowerCase();
      items.forEach((el) => {
        const hay = (el.textContent || "").toLowerCase();
        el.hidden = q !== "" && !hay.includes(q);
      });
    });
  }

  function setupModeCategoryFilter() {
    const btns = document.querySelectorAll("[data-mode-filter]");
    const cards = document.querySelectorAll("[data-mode-tags]");
    if (!btns.length || !cards.length) return;
    btns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const tag = btn.getAttribute("data-mode-filter");
        btns.forEach((b) => {
          const active = b === btn;
          b.setAttribute("aria-selected", String(active));
          b.classList.toggle("active", active);
        });
        cards.forEach((c) => {
          const tags = (c.getAttribute("data-mode-tags") || "").split(",");
          c.hidden = tag !== "all" && !tags.includes(tag);
        });
      });
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    setupThemeToggle();
    setupMobileDrawer();
    setupCopyButtons();
    setupHomeModePreview();
    setupQuickstartTabs();
    setupMcpProfileViewer();
    setupSearchFilter();
    setupModeCategoryFilter();
  });
})();
