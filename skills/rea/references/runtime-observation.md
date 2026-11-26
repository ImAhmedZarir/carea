# Runtime Instrumentation, Debuggers, Traffic & Signals (`/rea`)

Live hooking, debugging, process observation, browser/Electron CDP, packet captures, and hardware signal decoding workflows.

## 1. Live Binary Instrumentation & Debugging

| Mechanism | Workflow Tools | Key Operational Details |
| --- | --- | --- |
| **Frida (`frida`)** | `list_frida_devices` -> `list_frida_processes` -> `start_frida_session` -> `load_frida_script` -> `resume_frida_session` -> `instrument_with_frida` | `attach` hooks running PID; `spawn` starts paused until `resume_frida_session`. Unload with `unload_frida_script` and detach cleanly with `close_frida_session`. |
| **GDB Console** | `start_gdb_session` -> `gdb_console` -> `gdb_session_status` -> `close_gdb_session` | Interactive full-control debugger (Linux). Close active Ghidra sessions before modifying target memory/files, then reopen static DB after. |
| **Rizin Debug** | `start_rizin_debug_session` -> `rizin_debug_command` -> `rizin_debug_session_status` -> `close_rizin_debug_session` | Requires durable `inferior_tty`. Teardown via `close_rizin_debug_session`. |
| **Process PTY Capture** | `prepare_bounded_process_capture` -> `capture_process_scenario` -> `compare_process_captures` | Captures terminal I/O, exit state, and selected file deltas; pair with `correlate_static_and_runtime` against static diffs. |
| **macOS LLDB / Native UI** | `observe_native_calls`, `observe_native_ui`, `capture_native_ui_scenario`, `trace_native_ui_action` | Records selected function/ObjC entry integer registers and native window trees/actions. |

## 2. Browser, CDP & Live JS Execution

- **Live User Browser:** `list_browser_targets` -> `inspect_web_page` / `observe_web_session` -> `capture_web_screenshot` -> `observe_web_execution` (coverage/counters) -> `inspect_web_event_listeners` -> `discover_webmcp_tools`.
- **Driven Actions:** `capture_browser_scenario` (connect mode to loopback CDP `target_id` or launch isolated browser profile). Use `detail: "summary"` for multi-step trees, then page `inspect_analysis_view` kind `browser-scenario`.
- **Electron Live:** Verify fuses with `inspect_electron_fuses` -> `list_electron_targets` -> `inspect_electron_page` / `capture_electron_scenario`.
- **Node / Standalone JS Runtime:** `list_javascript_runtime_targets` -> `observe_javascript_runtime` -> `reconcile_javascript_runtime`.

## 3. Historical Network, Packet & Signal Captures

- **Web Network Archives (`inspect_web_network_capture`):** Supports HAR, **Fiddler Everywhere (`.saz` with `format: "saz"`)**, mitmproxy streams, and **aioquic qlog 0.3**. Raise heap if needed via `REA_CAPTURE_DECODER_OLD_GENERATION_MIB` (default 192 MiB -> up to 16384).
- **Packet Captures (`inspect_pcap_capture`, `inspect_packet_fields`, `inspect_packet_capture`):** Requires Wireshark 4.x `tshark` / `capinfos` (`REA_TSHARK_COMMAND` override). Start with `inspect_pcap_capture` (`detail: "summary"`) for DNS/SNI/protocol trees and page `inspect_analysis_view` kind `pcap`; run `inspect_packet_fields` -> `inspect_packet_capture` for display filters, dissectors, and `match_offset`/`match_limit` frame extraction.
- **RF / Logic Analyzer Recordings (`inspect_signal_decoders` -> `decode_signal_recording`):** Powered by `sigrok-cli` (`REA_SIGROK_COMMAND`). Search protocol decoders & options first, then decode captures by paging `line_offset` / `line_limit`.
