# Sanitized Behavioral Specification — `deck-timer` Example

> **Airlock Notice:** Process aid only — **not legal advice and not a legal clean-room guarantee**.
> **Analyst Rule:** This example specification was audited to exclude source code, pseudocode, disassembly, CSS/DOM markup, secrets, and third-party brand assets.

- **Project Name:** `deck-timer` (example Electron countdown utility)
- **Target Kind:** `electron-app`
- **Target Stack for Rebuild:** React + TypeScript + Vite web/desktop timer (original UI)
- **Handoff Record:** [`handoff.example.json`](handoff.example.json)
- **Authorized Scope:** User-owned reference binary/app

---

## 1. Scope & Non-Goals

- **In Scope:**
  - Countdown timer state machine (`idle`, `running`, `paused`, `completed`)
  - Local HTTP status endpoint (`/api/timer/status`) and keyboard shortcuts (`Space` toggle, `R` reset)
  - Responsive layout for compact speaker card (`375px`) and presenter control view (`1440px`)
- **Explicitly Out of Scope / Excluded:**
  - Auto-updater mechanism and telemetry endpoints
  - Original icon artwork, font files, and marketing copy (Builder generates original visual assets)

---

## 2. Observable User Flows & UI States

1. **Compact & Presenter Views (`obl_ui_responsive`):**
   - At `375px` width, display a single-column centered timer readout (`tabular` monospace digits `MM:SS`), primary Play/Pause button (`>= 44px` height), and Reset button.
   - At `1440px` width, display the timer readout alongside preset duration buttons (`5m`, `10m`, `15m`, `25m`) and a live status indicator pill.
   - Warning threshold state: when `remaining_ms <= 60_000` and `remaining_ms > 0`, switch status indicator to warning state; when `remaining_ms == 0`, switch to completed state.
2. **Visual Asset Plan:**
   - Use standard geometric vector controls and original color tokens rather than any graphics from the reference target.

---

## 3. Data Contracts & API Shapes (Value-Free)

### Local Read Endpoint (`obl_api_status_read`)
- **Trigger / Transport:** `GET /api/timer/status` on localhost port configured by `--port` (default `4173`)
- **Input Shape:** No request body; optional query flag `format=json`
- **Output Shape:**
  - `state`: enum `"idle" | "running" | "paused" | "completed"`
  - `duration_ms`: integer `>= 1000` and `<= 86_400_000`
  - `remaining_ms`: integer `>= 0` and `<= duration_ms`
  - `warning_active`: boolean (`true` when `state == "running"` and `remaining_ms <= 60_000` and `remaining_ms > 0`)

---

## 4. State Machines & Domain / Algorithmic Rules

| Current State | Event / Input | Guard Condition | Next State | Observable Side Effect |
|---|---|---|---|---|
| `idle` | `start` / `Space` | `duration_ms > 0` | `running` | Monotonic tick starts; status emits `running` |
| `running` | `pause` / `Space` | `remaining_ms > 0` | `paused` | Freezes `remaining_ms` |
| `paused` | `resume` / `Space` | `remaining_ms > 0` | `running` | Resumes monotonic subtraction from frozen `remaining_ms` |
| `running` | `tick` | `elapsed_since_start >= remaining_at_resume` | `completed` | Clamps `remaining_ms = 0`; triggers completion banner |
| `any` | `reset` / `R` | always | `idle` | Restores `remaining_ms = duration_ms` |

### Domain Formulas & Edge Cases (`obl_timer_math`)
- Elapsed time uses monotonic clock delta clamped to `[0, duration_ms]`:
  `remaining_ms = max(0, remaining_at_resume - (now_monotonic_ms - resume_monotonic_ms))`
- Durations outside `[1000, 86_400_000]` ms are rejected with validation error `invalid_duration` and state remains unchanged.

---

## 5. Open Unknowns (Do Not Guess)

- `unk_01`: Audio chime behavior when system audio device is muted or unavailable could not be observed statically; Builder should treat chime as optional with visual completion alert always enabled.

---

## 6. Deterministic Acceptance Test Vectors

| Test ID | Obligation | Input | Expected Outcome |
|---|---|---|---|
| `test_01` | `obl_timer_math` | `duration_ms = 90000`, start, advance `35000ms` | `state = "running"`, `remaining_ms = 55000`, `warning_active = true` |
| `test_02` | `obl_timer_math` | `duration_ms = 10000`, start, advance `15000ms` | `state = "completed"`, `remaining_ms = 0`, `warning_active = false` |
| `test_03` | `obl_api_status_read` | `GET /api/timer/status` while `paused` at `42000ms` | HTTP `200`, JSON with `state = "paused"`, `remaining_ms = 42000`, `warning_active = false` |
