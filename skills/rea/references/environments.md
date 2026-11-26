# AgentEnv Web & Desktop Environment Bundles (`/rea`)

How to record, witness, and export self-contained **AgentEnv (`agent-env`)** interactive environments from live web applications, HAR captures, or Linux desktop builds.

## 1. Web Application -> AgentEnv Export

1. **Map UI & API First:** Use `inspect_web_page` + `capture_web_screenshot` to discover selectors, forms, and API routes. Inspect any endpoints inside SPA bundles (`analyze_web_bundle` / `analyze_javascript_application`) so all origins are known.
2. **Declare Credentials Safely:** Pass secret handles via `secrets: [{secret_id, environment_variable}]` (pointing to env vars on the REA MCP process host) so captured values stay redacted.
3. **Record Interactive Flows (`capture_browser_scenario`):**
   - Connect mode (`mode: "connect"`, loopback CDP `target_id`) or launch mode (`mode: "launch"`, isolated profile).
   - Enable network capture (`capture: {network: {request_body: true, response_body: true, header_values: true}}`).
   - Chain `fill`, `click`, `press`, `wait_for`, and `request` actions; save generated entity IDs using `save_response` (`json_pointer`) so later create/read/update/delete requests bind cleanly!
   - Inspect step DOM/accessibility slices with `inspect_analysis_view` (`kind: "browser-scenario"`, `collection: "text"`).
4. **Export (`export_environment_bundle`):** Builds deployable `agent-env` bundle that serves both reads and confirmed stateful writes from the recorded session. HAR files can also be converted directly via `inspect_web_network_capture` -> `export_environment_bundle` or `rea environment-build <capture.har> <out_dir>`.

## 2. Desktop Application Environments (Linux Build Computer)

1. Verify Docker/agentenv runtime: `rea doctor --provider desktop_build --json`.
2. Start build computer: `start_build_computer` (Ubuntu noble archive, apt PPA, `.deb`, AppImage, or tarball install; include runtime helper packages in `extra_packages` if needed).
3. Drive GUI cleanly through `act_on_build_computer`; record consent/checkpoints (`mark_build_checkpoint`, `record_build_consent`); withhold sign-in/license artifacts cleanly from seeds.
4. Export and verify via `export_build_environment` and `check_build_task`, always calling `close_build_computer` on exit.
