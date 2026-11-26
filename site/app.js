/* carea Design System Interactive Shell & Component Controllers (Zero Dependencies) */
(() => {
  "use strict";

  const ROOT = document.documentElement;
  const BASE = document.body.dataset.rootPrefix || "./";

  function showToast(message) {
    let region = document.getElementById("carea-toast-region");
    if (!region) {
      region = document.createElement("div");
      region.id = "carea-toast-region";
      region.className = "toast-region";
      region.setAttribute("aria-live", "polite");
      document.body.appendChild(region);
    }
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.innerHTML = `<span class="status-dot status-dot--success"></span><span></span>`;
    toast.querySelector("span:last-child").textContent = message;
    region.appendChild(toast);
    setTimeout(() => {
      toast.remove();
    }, 2400);
  }

  /* 1. Theme Toggle + Sync */
  function currentTheme() {
    return ROOT.classList.contains("dark") ? "dark" : "light";
  }

  function applyTheme(theme) {
    ROOT.classList.toggle("dark", theme === "dark");
    try {
      localStorage.setItem("theme", theme);
    } catch (_) {}
    document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
      const next = theme === "dark" ? "light" : "dark";
      btn.setAttribute("aria-label", `Switch to ${next} theme`);
      btn.dataset.themeState = theme;
      const sun = btn.querySelector("[data-icon-sun]");
      const moon = btn.querySelector("[data-icon-moon]");
      if (sun && moon) {
        sun.style.display = theme === "dark" ? "block" : "none";
        moon.style.display = theme === "dark" ? "none" : "block";
      }
    });
  }

  document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const next = currentTheme() === "dark" ? "light" : "dark";
      applyTheme(next);
      showToast(`${next === "dark" ? "Dark" : "Light"} theme enabled`);
    });
  });
  applyTheme(currentTheme());

  /* 2. Copy Buttons */
  document.addEventListener("click", async (ev) => {
    const btn = ev.target.closest("[data-copy]");
    if (!btn) return;
    const text = btn.getAttribute("data-copy") || "";
    try {
      await navigator.clipboard.writeText(text);
    } catch (_) {
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy"); } catch (_) {}
      ta.remove();
    }
    btn.setAttribute("data-copied", "true");
    const label = btn.querySelector("[data-copy-label]");
    const prev = label ? label.textContent : "";
    if (label) label.textContent = "Copied";
    showToast("Copied command to clipboard");
    setTimeout(() => {
      btn.removeAttribute("data-copied");
      if (label) label.textContent = prev || "Copy";
    }, 1500);
  });

  /* 3. Mobile Navigation Sheet */
  const mobileBackdrop = document.getElementById("mobile-sheet-backdrop");
  const mobileCloseBtn = document.getElementById("mobile-sheet-close");
  let lastTrigger = null;

  function setMobileSheet(open, trigger) {
    if (!mobileBackdrop) return;
    mobileBackdrop.dataset.open = open ? "true" : "false";
    mobileBackdrop.setAttribute("aria-hidden", open ? "false" : "true");
    if (open) {
      lastTrigger = trigger || document.activeElement;
      if (mobileCloseBtn) mobileCloseBtn.focus();
    } else if (lastTrigger && typeof lastTrigger.focus === "function") {
      lastTrigger.focus();
      lastTrigger = null;
    }
  }

  document.querySelectorAll("[data-mobile-menu-open]").forEach((btn) => {
    btn.addEventListener("click", () => setMobileSheet(true, btn));
  });
  if (mobileCloseBtn) {
    mobileCloseBtn.addEventListener("click", () => setMobileSheet(false));
  }
  if (mobileBackdrop) {
    mobileBackdrop.addEventListener("click", (ev) => {
      if (ev.target === mobileBackdrop) setMobileSheet(false);
    });
  }

  /* 4. Command Menu (Cmd+K / Ctrl+K / /) */
  const COMMAND_INDEX = [
    { group: "Routes", title: "Overview & Interactive Workbench", hint: "/", url: `${BASE}` },
    { group: "Routes", title: "Operational Modes 1–6 & Topologies", hint: "/modes/", url: `${BASE}modes/` },
    { group: "Routes", title: "CLI Reference, Schema 1.1.0 & Parity States", hint: "/cli/", url: `${BASE}cli/` },
    { group: "Routes", title: "Upstream Compatibility & Coexistence", hint: "/docs/", url: `${BASE}docs/` },
    { group: "Routes", title: "Portfolio & pulse-timer Live Case Study", hint: "/portfolio/", url: `${BASE}portfolio/` },
    { group: "Modes", title: "Mode 1 · clean-room-ui (/ca observable UI)", hint: "Clean-room", url: `${BASE}modes/#mode-list` },
    { group: "Modes", title: "Mode 2 · two-team-process (REA + Airlock + CA)", hint: "Strongest flow", url: `${BASE}modes/#mode-list` },
    { group: "Modes", title: "Mode 3 · deep-verification (/rea + AgentEnv)", hint: "Analysis only", url: `${BASE}modes/#mode-list` },
    { group: "Modes", title: "Mode 4 · private-deep-rebuild (deep_private: true)", hint: "NOT clean-room", url: `${BASE}modes/#mode-list` },
    { group: "Modes", title: "Mode 5 · game-rebuild (Unity / Unreal / Godot)", hint: "game_* Deep-only", url: `${BASE}modes/#mode-list` },
    { group: "Modes", title: "Mode 6 · android-mobile (JADX / Flutter + ADB)", hint: "Mobile hybrid", url: `${BASE}modes/#mode-list` },
    { group: "CLI", title: "carea init <dir> --mode --topology", hint: "4-dir layout", url: `${BASE}cli/#cli-workbench` },
    { group: "CLI", title: "carea doctor", hint: "Engine & MCP check", url: `${BASE}cli/#cli-workbench` },
    { group: "CLI", title: "carea airlock-lint <dir> --strict", hint: "Heuristic scanner", url: `${BASE}cli/#cli-workbench` },
    { group: "CLI", title: "carea airlock-sign --reviewer --confirm-human-review", hint: "Audit stamp", url: `${BASE}cli/#cli-workbench` },
    { group: "CLI", title: "carea isolation-check <dir>", hint: "Symlink & host fence", url: `${BASE}cli/#cli-workbench` },
    { group: "CLI", title: "carea spec-draft <bundle.json>", hint: "Opaque IDs only", url: `${BASE}cli/#cli-workbench` },
    { group: "CLI", title: "carea parity-report", hint: "Dual-axis merge", url: `${BASE}cli/#cli-workbench` },
    { group: "CLI", title: "carea mcp-profile <preset>", hint: "rea-hot-cold / lane-b", url: `${BASE}cli/#cli-workbench` },
    { group: "Actions", title: "Toggle Light / Dark Theme", hint: "Action", action: () => applyTheme(currentTheme() === "dark" ? "light" : "dark") },
    { group: "Actions", title: "Copy Install Command (pip install --no-deps .)", hint: "Clipboard", action: () => navigator.clipboard?.writeText("pip install --no-deps .").then(() => showToast("Copied pip install --no-deps .")) },
  ];

  const cmdBackdrop = document.getElementById("cmd-dialog-backdrop");
  const cmdInput = document.getElementById("cmd-search-input");
  const cmdList = document.getElementById("cmd-results-list");
  let cmdActiveIndex = 0;
  let filteredCommands = COMMAND_INDEX;

  function renderCommands(query) {
    if (!cmdList) return;
    const q = (query || "").trim().toLowerCase();
    filteredCommands = q
      ? COMMAND_INDEX.filter((c) => `${c.group} ${c.title} ${c.hint}`.toLowerCase().includes(q))
      : COMMAND_INDEX;
    cmdActiveIndex = 0;
    cmdList.innerHTML = "";
    if (!filteredCommands.length) {
      cmdList.innerHTML = `<div class="muted" style="padding: 1.5rem 1rem; text-align: center; font-size: 0.85rem;">No matching routes, modes, or CLI commands.</div>`;
      return;
    }
    filteredCommands.forEach((item, idx) => {
      const el = document.createElement("button");
      el.type = "button";
      el.className = "cmd-item";
      el.setAttribute("role", "option");
      el.setAttribute("aria-selected", idx === cmdActiveIndex ? "true" : "false");
      el.innerHTML = `<span class="min-w-0 truncate"><strong style="font-weight:500;"></strong></span><span class="tag">${item.hint}</span>`;
      el.querySelector("strong").textContent = item.title;
      el.addEventListener("click", () => runCommandItem(item));
      el.addEventListener("mouseenter", () => {
        cmdActiveIndex = idx;
        syncCommandHighlight();
      });
      cmdList.appendChild(el);
    });
  }

  function syncCommandHighlight() {
    if (!cmdList) return;
    cmdList.querySelectorAll(".cmd-item").forEach((el, idx) => {
      el.setAttribute("aria-selected", idx === cmdActiveIndex ? "true" : "false");
      if (idx === cmdActiveIndex) el.scrollIntoView({ block: "nearest" });
    });
  }

  function runCommandItem(item) {
    setCommandDialog(false);
    if (typeof item.action === "function") {
      item.action();
    } else if (item.url) {
      window.location.href = item.url;
    }
  }

  function setCommandDialog(open) {
    if (!cmdBackdrop) return;
    cmdBackdrop.dataset.open = open ? "true" : "false";
    cmdBackdrop.setAttribute("aria-hidden", open ? "false" : "true");
    if (open) {
      setMobileSheet(false);
      renderCommands("");
      if (cmdInput) {
        cmdInput.value = "";
        setTimeout(() => cmdInput.focus(), 10);
      }
    }
  }

  document.querySelectorAll("[data-cmd-open]").forEach((btn) => {
    btn.addEventListener("click", () => setCommandDialog(true));
  });
  if (cmdBackdrop) {
    cmdBackdrop.addEventListener("click", (ev) => {
      if (ev.target === cmdBackdrop) setCommandDialog(false);
    });
  }
  if (cmdInput) {
    cmdInput.addEventListener("input", () => renderCommands(cmdInput.value));
    cmdInput.addEventListener("keydown", (ev) => {
      if (!filteredCommands.length) return;
      if (ev.key === "ArrowDown") {
        ev.preventDefault();
        cmdActiveIndex = (cmdActiveIndex + 1) % filteredCommands.length;
        syncCommandHighlight();
      } else if (ev.key === "ArrowUp") {
        ev.preventDefault();
        cmdActiveIndex = (cmdActiveIndex - 1 + filteredCommands.length) % filteredCommands.length;
        syncCommandHighlight();
      } else if (ev.key === "Enter") {
        ev.preventDefault();
        runCommandItem(filteredCommands[cmdActiveIndex]);
      }
    });
  }

  document.addEventListener("keydown", (ev) => {
    if ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === "k") {
      ev.preventDefault();
      const isOpen = cmdBackdrop?.dataset.open === "true";
      setCommandDialog(!isOpen);
    } else if (ev.key === "/" && !["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement?.tagName || "")) {
      if (cmdBackdrop) {
        ev.preventDefault();
        setCommandDialog(true);
      }
    } else if (ev.key === "Escape") {
      setCommandDialog(false);
      setMobileSheet(false);
    }
  });

  /* 5. Overview Hero 4-Stage Pipeline Workbench */
  const heroWorkbench = document.getElementById("hero-pipeline-workbench");
  if (heroWorkbench) {
    const STAGE_DATA = {
      a: {
        stage1: {
          title: "Lane A · REA Analyst",
          dir: "analyst-evidence/",
          tools: "REA_MCP_TOOL_CATALOG_PROFILE=hot-cold · open_binary · record_unknown",
          output: `{
  "evidence_id": "ev_835b...",
  "evidence_format": 2,
  "bytes": 149804,
  "unknowns": ["unk_inline_script_01"]
}`,
          note: "Session 1 inspects authorized binaries or web apps, logs incomplete coverage via record_unknown, and exports opaque evidence IDs."
        },
        stage2: {
          title: "Airlock Gate · carea CLI",
          dir: "airlock/",
          tools: "spec-draft -> airlock-lint --strict -> airlock-sign",
          output: `PASS: clean-room-spec.md (0 leaks)
VALID: carea-handoff.json (schema 1.1.0)
SIGNED: airlock.status="passed" (human review logged)`,
          note: "Heuristic leak scanner checks code fences, bitwise snippets, hex offsets, obfuscated emails, spaced secrets, assets, and absolute paths before human sign-off."
        },
        stage3: {
          title: "Lane B · CA Builder",
          dir: "builder-workspace/",
          tools: "craft-anything-cli mcp --clean-room (30 tools)",
          output: `core_session_show -> {"clean_room": true, "version": "0.6.0"}
web_site_open     -> Chrome 158 (ev_785a...)`,
          note: "Reads ONLY signed airlock/ artifacts and public UI renders. Never mounts analyst-evidence/."
        },
        stage4: {
          title: "Stage 4 · Dual Parity",
          dir: "verification/",
          tools: "carea parity-report + return-feedback",
          output: `overall: "partial"
CA observable: PASS | REA verification: partial
note: index.html inline script coverage gap preserved`,
          note: "Passed requires BOTH CA UI parity and REA behavioral checks satisfied on declared obligations."
        }
      },
      topo: {
        b: { badge: "Topology (b) · Stronger Separation", detail: "Separate fresh agent context + zero REA MCP tools in Lane B MCP config + empty history." },
        a: { badge: "Topology (a) · CA Subprocess", detail: "Orchestrator triggers craft-anything-cli rebuild --clean-room; shared parent terminal unless sandboxed." }
      }
    };

    let activeStage = "stage1";
    let activeTopo = "b";

    const outEl = document.getElementById("wb-terminal-output");
    const noteEl = document.getElementById("wb-stage-note");
    const toolsEl = document.getElementById("wb-tools-line");
    const dirEl = document.getElementById("wb-dir-line");
    const topoNoteEl = document.getElementById("wb-topo-detail");

    function renderWorkbench() {
      const s = STAGE_DATA.a[activeStage];
      heroWorkbench.querySelectorAll("[data-stage-btn]").forEach((b) => {
        b.setAttribute("aria-selected", b.dataset.stageBtn === activeStage ? "true" : "false");
      });
      heroWorkbench.querySelectorAll("[data-topo-btn]").forEach((b) => {
        b.setAttribute("aria-selected", b.dataset.topoBtn === activeTopo ? "true" : "false");
      });
      if (dirEl) dirEl.textContent = s.dir;
      if (toolsEl) toolsEl.textContent = s.tools;
      if (outEl) outEl.textContent = s.output;
      if (noteEl) noteEl.textContent = s.note;
      if (topoNoteEl) topoNoteEl.textContent = STAGE_DATA.topo[activeTopo].detail;
    }

    heroWorkbench.querySelectorAll("[data-stage-btn]").forEach((b) => {
      b.addEventListener("click", () => { activeStage = b.dataset.stageBtn; renderWorkbench(); });
    });
    heroWorkbench.querySelectorAll("[data-topo-btn]").forEach((b) => {
      b.addEventListener("click", () => { activeTopo = b.dataset.topoBtn; renderWorkbench(); });
    });
    renderWorkbench();
  }

  /* 6. Airlock Lint Sandbox on Overview */
  const lintSandbox = document.getElementById("airlock-lint-sandbox");
  if (lintSandbox) {
    const SAMPLES = {
      clean: {
        label: "Clean Spec",
        status: "PASS",
        tagClass: "tag--success",
        spec: `# Spec: pulse-timer State Machine\n- Behavior: Countdown decrements once per 1000ms tick when active.\n- Controls: Play, Pause, Reset buttons mapped to accessible labels.\n- Coverage: ev_835b (opaque reference only; no payload copied).`,
        log: `PASS: airlock/clean-room-spec.md (1 file scanned)\n[NOTE] Heuristic scan passed. Human review via 'carea airlock-sign --confirm-human-review' still required.`
      },
      inline: {
        label: "Inline Code Leak",
        status: "FAIL",
        tagClass: "tag--destructive",
        spec: `# Spec: CRC Bit Mixer\n- Compute the accumulator update using inline bitwise shift:\n  if(x>>3&1){y=z^0x5A3C} on each frame boundary.`,
        log: `FAIL: airlock/leak-spec.md (1 file scanned)\n  [FAIL] leak-spec.md:3 (INLINE_CODE_SNIPPET) - Bitwise/control-flow snippet leaked outside fenced block.\n  [FAIL] leak-spec.md:3 (HEX_CONSTANT_DENSITY) - Low-level hex constant/offset (0x5A3C) matched.`
      },
      obfuscated: {
        label: "Obfuscated Email & Key",
        status: "FAIL",
        tagClass: "tag--destructive",
        spec: `# Spec: Telemetry Headers\n- Forward diagnostic reports to j.smith [at] corp [dot] com\n- Header fallback prefix observed as sk_live_ 4eC39HqLyjWDarjt`,
        log: `FAIL: airlock/telemetry.md (1 file scanned)\n  [FAIL] telemetry.md:2 (OBFUSCATED_EMAIL) - Masked address ([at]/[dot]) detected.\n  [FAIL] telemetry.md:3 (SPACED_SECRET_KEY) - Whitespace-split secret token prefix (sk_live_) detected.`
      },
      pathwarn: {
        label: "Long Prose Warning",
        status: "WARN",
        tagClass: "tag--warning",
        spec: `# Spec: Long Verbatim Narrative\nThis specification paragraph exceeds normal concise behavioral contract limits across dozens of words closely mirroring continuous extracted manual text without concise bullet contracts...`,
        log: `WARN: airlock/narrative.md (1 file scanned)\n  [WARN] narrative.md:2 (PROSE_LENGTH) - Long continuous prose paragraph detected; convert into atomic state/IO rules.\nExit 1 under '--strict'.`
      }
    };
    let activeSample = "clean";
    const sampleSpecEl = document.getElementById("lint-sample-spec");
    const sampleLogEl = document.getElementById("lint-sample-log");
    const sampleBadgeEl = document.getElementById("lint-sample-badge");

    function renderLintSample() {
      const s = SAMPLES[activeSample];
      lintSandbox.querySelectorAll("[data-lint-preset]").forEach((b) => {
        b.setAttribute("aria-selected", b.dataset.lintPreset === activeSample ? "true" : "false");
      });
      if (sampleSpecEl) sampleSpecEl.textContent = s.spec;
      if (sampleLogEl) sampleLogEl.textContent = s.log;
      if (sampleBadgeEl) {
        sampleBadgeEl.className = `tag ${s.tagClass}`;
        sampleBadgeEl.textContent = s.status;
      }
    }
    lintSandbox.querySelectorAll("[data-lint-preset]").forEach((b) => {
      b.addEventListener("click", () => { activeSample = b.dataset.lintPreset; renderLintSample(); });
    });
    renderLintSample();
  }

  /* 7. Generic Data-Tab Switchers (Quickstarts, Coexistence, Portfolio Timeline, Schema) */
  document.querySelectorAll("[data-tab-group]").forEach((group) => {
    const triggers = group.querySelectorAll("[data-tab-target]");
    const panels = group.querySelectorAll("[data-tab-panel]");
    triggers.forEach((t) => {
      t.addEventListener("click", () => {
        const key = t.dataset.tabTarget;
        triggers.forEach((x) => x.setAttribute("aria-selected", x === t ? "true" : "false"));
        panels.forEach((p) => { p.hidden = p.dataset.tabPanel !== key; });
      });
    });
  });

  /* 8. Modes Filter + Inspector (/modes/) */
  const modesExplorer = document.getElementById("modes-explorer");
  if (modesExplorer) {
    const MODES_DB = [
      {
        id: "clean-room-ui",
        num: "Mode 1",
        name: "Clean-Room UI / Web Rebuild",
        skill: "/ca",
        clean: "Tool-level (--clean-room)",
        category: "clean",
        engines: "Craft Anything >= 0.6.0",
        steps: "1. core_session_show (verify clean_room:true) -> 2. web_site_open / web_site_capture / web_page_states_capture -> 3. rebuild_start + assets_image_generate -> 4. rebuild_check & web_pixels_compare.",
        limits: "Cannot inspect hidden algorithms or proprietary offline storage internals."
      },
      {
        id: "two-team-process",
        num: "Mode 2",
        name: "Two-Team Clean Room Process",
        skill: "/carea",
        clean: "Process aid (airlock/ + Topology b)",
        category: "clean",
        engines: "REA + airlock + CA --clean-room",
        steps: "1. carea init + isolation-check -> 2. Lane A (REA) exports bundle -> 3. spec-draft -> airlock-lint --strict -> human review -> airlock-sign -> 4. Lane B (Topology b CA) rebuilds -> 5. parity-report + return-feedback.",
        limits: "Process aid only — not a legal clean-room defense or OS kernel sandbox."
      },
      {
        id: "deep-verification",
        num: "Mode 3",
        name: "Deep Investigation / AgentEnv",
        skill: "/rea",
        clean: "N/A (analysis only)",
        category: "rea",
        engines: "REA (264 MCP schemas)",
        steps: "1. Set REA_MCP_TOOL_CATALOG_PROFILE=hot-cold -> 2. open_binary / inspect_artifact / analyze_javascript_application -> 3. record_unknown -> 4. verify_reconstruction or export_environment_bundle -> 5. close_binary.",
        limits: "Verification checks finite declared claims; build host lacked Node >=22 for local rea CLI."
      },
      {
        id: "private-deep-rebuild",
        num: "Mode 4",
        name: "Private Deep Rebuild (NOT Clean-Room)",
        skill: "/carea",
        clean: "NO (deep_private: true)",
        category: "deep",
        engines: "REA Deep + CA --deep",
        steps: "1. carea init --mode private-deep-rebuild (sets deep_private: true) -> 2. Emit mandatory non-clean-room warning banner -> 3. REA deep + CA --deep (core_target_open allowed) -> 4. Dual parity verification.",
        limits: "Carries zero clean-room standing; forbidden from setting airlock.status=\"passed\"."
      },
      {
        id: "game-rebuild",
        num: "Mode 5",
        name: "Game Rebuild Path",
        skill: "/carea · /ca",
        clean: "Clean-room unless game_* / --deep used",
        category: "deep",
        engines: "CA --build-with unity|unreal|godot|rust",
        steps: "1. Confirm ownership & no-asset-copy rule -> 2. Choose observable --clean-room OR authorized deep (game_* tools disabled in clean-room) -> 3. Generate replacement art via assets_image_generate -> 4. runtime_captures_compare.",
        limits: "Live Mode 5 engine run unverified on host; game_pak_extract / game_unity_* blocked under --clean-room."
      },
      {
        id: "android-mobile",
        num: "Mode 6",
        name: "Android / Mobile App Path",
        skill: "/carea",
        clean: "Clean-room across Airlock only",
        category: "deep",
        engines: "REA android/flutter + CA adb",
        steps: "1. carea init --mode android-mobile -> 2. Lane A REA inspect_android_package / identify_flutter_build / decode_android_resources -> 3. Airlock lint + sign -> 4. Lane B engines_adb_check + adb_screenshot_take -> 5. Dual parity.",
        limits: "Live adb hardware capture unverified on host (adb missing); Flutter AOT may preserve unknown_ids."
      }
    ];

    let filterCat = "all";
    let query = "";
    let selectedId = "two-team-process";

    const searchInput = document.getElementById("modes-search");
    const detailPanel = document.getElementById("mode-detail-inspector");

    function updateModesView() {
      const visible = MODES_DB.filter((m) => {
        const catOk = filterCat === "all" || m.category === filterCat;
        const qOk = !query || `${m.id} ${m.name} ${m.engines} ${m.skill}`.toLowerCase().includes(query);
        return catOk && qOk;
      });
      if (!visible.some((m) => m.id === selectedId) && visible[0]) {
        selectedId = visible[0].id;
      }

      modesExplorer.querySelectorAll("[data-mode-filter]").forEach((btn) => {
        btn.setAttribute("aria-selected", btn.dataset.modeFilter === filterCat ? "true" : "false");
      });

      modesExplorer.querySelectorAll("[data-mode-row]").forEach((row) => {
        const id = row.dataset.modeRow;
        const show = visible.some((m) => m.id === id);
        row.style.display = show ? "" : "none";
        row.dataset.selected = id === selectedId ? "true" : "false";
      });

      const active = MODES_DB.find((m) => m.id === selectedId) || MODES_DB[0];
      if (detailPanel && active) {
        detailPanel.innerHTML = `
          <div class="flex flex-wrap items-start justify-between gap-2">
            <div class="min-w-0">
              <div class="eyebrow">${active.num} · ${active.id}</div>
              <h3 class="h3 mt-2">${active.name}</h3>
            </div>
            <span class="tag ${active.clean.startsWith("NO") ? "tag--warning" : "tag--primary"}">${active.clean}</span>
          </div>
          <div class="surface-sub mt-4" style="padding: 0.875rem;">
            <div class="tabular muted" style="font-size: 0.72rem; text-transform: uppercase;">Sequence</div>
            <p class="mt-2" style="margin-bottom:0; font-size:0.875rem;">${active.steps}</p>
          </div>
          <div class="mt-4 flex flex-wrap items-center justify-between gap-3" style="font-size:0.8125rem;">
            <span class="muted"><strong>Engines:</strong> <code>${active.engines}</code></span>
            <span class="muted"><strong>Trigger:</strong> <code>${active.skill}</code></span>
          </div>
          <div class="callout ${active.clean.startsWith("NO") ? "callout--warning" : "callout--primary"} mt-4" style="font-size:0.8125rem;">
            <strong>Verified Boundary:</strong> ${active.limits}
          </div>`;
      }
    }

    modesExplorer.querySelectorAll("[data-mode-filter]").forEach((b) => {
      b.addEventListener("click", () => { filterCat = b.dataset.modeFilter; updateModesView(); });
    });
    modesExplorer.querySelectorAll("[data-mode-row]").forEach((row) => {
      row.addEventListener("click", () => { selectedId = row.dataset.modeRow; updateModesView(); });
    });
    if (searchInput) {
      searchInput.addEventListener("input", () => { query = searchInput.value.trim().toLowerCase(); updateModesView(); });
    }
    updateModesView();
  }

  /* 9. CLI 10-Command Inspector (/cli/) */
  const cliWorkbench = document.getElementById("cli-workbench");
  if (cliWorkbench) {
    const CLI_DATA = {
      init: {
        cmd: "carea init <dir> --mode two-team-process --topology b --target-name pulse-timer",
        summary: "Creates the 4-directory boundary layout (analyst-evidence/, airlock/, builder-workspace/, verification/) plus starter templates and .carea/config.json.",
        sample: `Initialized ./my-rebuild (mode=two-team-process, topology=b, deep_private=false)\n  wrote: airlock/clean-room-spec.md\n  wrote: airlock/carea-handoff.json\n  wrote: .carea/config.json`
      },
      doctor: {
        cmd: "carea doctor [--client-config ~/.claude/settings.json]",
        summary: "Inspects REA + Craft Anything CLI versions, Node.js runtime bounds, and checks MCP profiles against compat/matrix.json (warns on full schema profile for >=6.10 or CA --all-tools).",
        sample: `carea doctor (matrix 1.0.0, updated 2026-11-26)\n  [REA]            status=missing version=none (host lacks Node >=22)\n  [Craft Anything] status=supported version=0.6.0`
      },
      "validate-handoff": {
        cmd: "carea validate-handoff airlock/carea-handoff.json",
        summary: "Validates handoff records against bundled schema 1.1.0 & 1.0.0 (checks deep_private mutual exclusion and airlock audit fields).",
        sample: `VALID: airlock/carea-handoff.json (schema_version=1.1.0)`
      },
      "airlock-lint": {
        cmd: "carea airlock-lint airlock/ --strict",
        summary: "Heuristic leak scanner detecting code fences, bitwise inline snippets, 4+ hex constants, asm, minified JS, base64 blobs, secrets, obfuscated emails, media assets, analyst-evidence/ paths, and long prose.",
        sample: `PASS: airlock (2 files scanned)\n[NOTE] Heuristic scanner only — does NOT guarantee absence of semantic leaks.`
      },
      "airlock-sign": {
        cmd: 'carea airlock-sign airlock/carea-handoff.json --reviewer "zarir" --confirm-human-review',
        summary: "Stamps airlock.status=\"passed\" ONLY when airlock-lint passes cleanly and --reviewer + --confirm-human-review are supplied.",
        sample: `SIGNED: airlock/carea-handoff.json by zarir (lint_hash=sha256:9d4a...)`
      },
      "isolation-check": {
        cmd: "carea isolation-check ./my-rebuild",
        summary: "Verifies builder-workspace/ is neither a symlink nor parent/child of analyst-evidence/ and prints recommended host-agent permission rules.",
        sample: `PASS: isolation check on ./my-rebuild\n[PASS] symlink_and_nesting: Clean separation verified.`
      },
      "spec-draft": {
        cmd: "carea spec-draft analyst-evidence/bundle.json --out airlock/clean-room-spec.md",
        summary: "Generates a sanitized draft specification skeleton from an REA evidence_format: 2 bundle using opaque IDs only (zero raw strings/code).",
        sample: `Drafted airlock/clean-room-spec.md from 149,804-byte REA bundle (opaque IDs only).`
      },
      "parity-report": {
        cmd: "carea parity-report --handoff airlock/carea-handoff.json --ca-report ca.json --rea-report rea.json",
        summary: "Merges CA UI/walkthrough evidence and REA behavioral verification into verification/parity-checklist.md without collapsing missing gaps into passed.",
        sample: `Wrote verification/parity-checklist.md (overall=partial, total=2, passed=1, partial=1)`
      },
      "return-feedback": {
        cmd: "carea return-feedback --handoff airlock/carea-handoff.json --ca-report ca.json --rea-report rea.json",
        summary: "Emits Lane-B-safe failure test vectors and observable UI diffs back across the airlock with zero target source disclosures.",
        sample: `Wrote verification/lane-b-feedback.md (sanitized input/output test vectors only).`
      },
      "mcp-profile": {
        cmd: "carea mcp-profile carea-master [--apply ~/.claude.json]",
        summary: "Outputs lean or full-power MCP configs (carea-master, rea-master, rea-all-families, ca-deep-full, rea-hot-cold, ca-clean-room, two-team-lane-b) and prints an explicit diff before modifying config files.",
        sample: `{"mcpServers":{"rea":{"env":{"REA_MCP_TOOL_CATALOG_PROFILE":"hot-cold"}},"craft-anything":{"args":["mcp","--deep","--all-tools"]}}}`
      }
    };

    let activeCli = "init";
    const outBox = document.getElementById("cli-inspector-output");

    function renderCliInspector() {
      cliWorkbench.querySelectorAll("[data-cli-cmd]").forEach((btn) => {
        btn.setAttribute("aria-selected", btn.dataset.cliCmd === activeCli ? "true" : "false");
      });
      const item = CLI_DATA[activeCli];
      if (outBox && item) {
        outBox.innerHTML = `
          <div class="code-box">
            <div class="code-head">
              <span>carea ${activeCli}</span>
              <button class="copy-pill" type="button" data-copy="${item.cmd.replace(/"/g, "&quot;")}"><span data-copy-label>Copy</span></button>
            </div>
            <pre class="code-pre"><code>$ ${item.cmd}

${item.sample}</code></pre>
          </div>
          <p class="mt-4" style="margin-bottom:0; font-size:0.875rem;">${item.summary}</p>`;
      }
    }

    cliWorkbench.querySelectorAll("[data-cli-cmd]").forEach((btn) => {
      btn.addEventListener("click", () => { activeCli = btn.dataset.cliCmd; renderCliInspector(); });
    });
    renderCliInspector();
  }

  /* 10. Parity 5-State Inspector (/cli/) */
  const stateInspector = document.getElementById("parity-state-inspector");
  if (stateInspector) {
    const VIEW_STATES = {
      partial: {
        badge: "partial",
        badgeClass: "tag--warning",
        body: `
          <div class="flex items-center justify-between gap-2">
            <strong style="font-size:0.9rem;">pulse-timer · Mode 2 E2E Run</strong>
            <span class="tag tag--warning">overall: partial</span>
          </div>
          <p class="muted mt-2" style="font-size:0.8125rem; margin-bottom:0;">
            CA Chrome 158 UI check (ev_785a) passed; REA reported inline script coverage gap inside index.html — honestly preserved as <code>partial</code>.
          </p>`
      },
      success: {
        badge: "passed",
        badgeClass: "tag--success",
        body: `
          <div class="flex items-center justify-between gap-2">
            <strong style="font-size:0.9rem;">timer-state-core · Verified</strong>
            <span class="tag tag--success">overall: passed</span>
          </div>
          <p class="muted mt-2" style="font-size:0.8125rem; margin-bottom:0;">
            Both Axis 1 (web_pixels_compare + walkthrough pass) and Axis 2 (verify_reconstruction finite spec pass) completed after signed airlock.
          </p>`
      },
      loading: {
        badge: "loading",
        badgeClass: "tag--primary",
        body: `
          <div class="stack">
            <div class="skeleton" style="height:1rem; width:45%;"></div>
            <div class="skeleton" style="height:2.5rem; width:100%;"></div>
            <div class="skeleton" style="height:0.875rem; width:68%;"></div>
          </div>`
      },
      empty: {
        badge: "empty",
        badgeClass: "tag",
        body: `
          <div style="text-align:center; padding:1rem 0;">
            <div class="tabular muted" style="font-size:0.8rem;">0 obligations declared</div>
            <p class="muted mt-2" style="font-size:0.8125rem; margin-bottom:0;">Run <code>carea spec-draft &lt;bundle.json&gt;</code> to scaffold tracked obligations.</p>
          </div>`
      },
      error: {
        badge: "error",
        badgeClass: "tag--destructive",
        body: `
          <div class="callout" style="border-left-color:var(--destructive); background:transparent; border-color:color-mix(in oklab,var(--destructive) 35%,transparent);">
            <strong>Airlock Sign-Off Blocked</strong>
            <p class="muted mt-2" style="font-size:0.8125rem; margin-bottom:0;"><code>carea airlock-sign</code> refused because <code>--confirm-human-review</code> was omitted or <code>airlock-lint</code> returned FAIL.</p>
          </div>`
      }
    };

    const panel = document.getElementById("parity-state-render");
    const badge = document.getElementById("parity-state-badge");

    function renderState(key) {
      const s = VIEW_STATES[key];
      stateInspector.querySelectorAll("[data-ui-state]").forEach((b) => {
        b.setAttribute("aria-selected", b.dataset.uiState === key ? "true" : "false");
      });
      if (panel && s) panel.innerHTML = s.body;
      if (badge && s) {
        badge.className = `tag ${s.badgeClass}`;
        badge.textContent = s.badge;
      }
    }

    stateInspector.querySelectorAll("[data-ui-state]").forEach((b) => {
      b.addEventListener("click", () => renderState(b.dataset.uiState));
    });
    renderState("partial");
  }
})();
