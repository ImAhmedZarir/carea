# JavaScript, V8 Cache, Web Bundle & Electron Playbook (`/rea`)

Deep workflow for analyzing Electron desktop apps, bundled SPAs, obfuscated JS, ASAR packages, V8 `.jsc` bytecode caches, and live web/Electron runtimes.

## 1. Static ASAR & JS Tree Analysis (`analyze_javascript_application`)

- Call `analyze_javascript_application` directly on an `.asar` file or extracted JS directory (no `open_binary` needed).
- **Large trees / unknown size:** Always start with `"detail": "summary"` so complete Evidence stays retained under `parent_evidence_id`.
- **Huge ASAR headers (>16 MiB default):** If rejected for `asar.max_header_bytes`, raise up to 256 MiB (`268435456`) via `update_analysis_settings` (`REA_ASAR_MAX_HEADER_BYTES` for CLI/env).
- **Scoped inspection:** When only specific files matter (`["package.json", "main.js", "preload.js"]`), pass exact paths via `source_paths` (`source_paths: []` is invalid — omit it for full scan).
- **Route Inventory View:** Request `detail: "summary"` + `view: {kind: "javascript-routes", collection: "routes", fields: ["path", "confidence"], limit: 32}` to extract all candidate frontend/backend routes without dumping the whole module graph.

## 2. Module Paging, Wakaru Deobfuscation & V8 Code Cache

1. **Page Module Graph:** Call `inspect_analysis_view` with `source: {kind: "retained-evidence", evidence_id: "<parent_evidence_id>"}` and `view: {kind: "page", collection: "modules", offset: 0, limit: 20}` -> pick target `node_id` -> query `kind: "item"` for `static_analysis` and `semantic_module_analysis`.
2. **Recover Minified / Bundled Code (`recover_javascript_sources`):** Pass absolute bundle path + related lazy/shared chunks in `additional_paths`, omitting `output_directory` so REA stages a unified `analysis_input` directory -> then run `analyze_javascript_application` over the unbundled output.
3. **V8 / Bytenode Bytecode (`inspect_v8_code_cache`):** Extract header, version hash, script length, and metadata from `.jsc` V8 code-cache files without running them.
4. **Bundle Endpoints (`analyze_web_bundle`):** Extract inferred HTTP/API endpoints, locations, and bases via `view: {kind: "web-bundle", collection: "endpoints", limit: 32}`.
5. **Semantic & Feature Tracing:** `trace_application_feature`, `trace_javascript_semantics`, `trace_web_module_imports`, `trace_web_source_location`, `compare_javascript_export_shapes`, `compare_source_to_bundle`, `compare_application_versions`, `inspect_api_contract`.

## 3. Electron Specifics & SPA Multi-Origin API Rule

- **Before Electron `--inspect`:** Always check packaged security fuses first with `inspect_electron_fuses` — if `EnableNodeCliInspectArguments` is disabled, Inspector arguments are ignored by the binary. Use `list_electron_targets` / `inspect_electron_page` / `capture_electron_scenario` for live DevTools observation.
- **SPA Multi-Origin Traffic Capture:** Passive web captures default to the page's own origin ONLY. First extract API host URLs from loaded JS bundles (`analyze_web_bundle` / `analyze_javascript_application`), then capture with `allowed_origins: [page_origin, api_origin_1, ...]` so cross-origin REST/GraphQL traffic is NOT dropped.
- **Static <-> Runtime Reconciliation:** Capture live page/API execution (`observe_web_session`, `capture_browser_scenario`, `observe_javascript_runtime`), then reconcile bundle digests against executed runtime code using `reconcile_javascript_runtime` and `compare_static_and_observed_endpoints`.
