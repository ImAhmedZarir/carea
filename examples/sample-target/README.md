# `pulse-timer` — Self-Owned Sample Target (`carea`)

`pulse-timer` is an original, minimal countdown utility built inside `carea` (`MIT License`, `Copyright (c) 2026 Ahmed Ishtiaque Zarir`) so all workflow examples (`docs/workflows/*.md`) operate on a self-owned target rather than third-party software.

## Files

- `timer.mjs`: Pure deterministic countdown state machine (`initTimer`, `advanceTimer`, `statusSnapshot`).
- `server.py`: Tiny Python stdlib HTTP server serving `/` (`index.html`) and `GET /api/timer/status`.
- `index.html`: Minimal responsive mobile (`375px`) and desktop (`1440px`) UI (`44px` controls, `tabular-nums` digits, zero external assets).
- `test_timer.py`: Stdlib unit tests verifying deterministic state transitions.

## Running Locally

```bash
python examples/sample-target/server.py --port 4173
```

Then verify behavior or point Craft Anything (`--clean-room`) at `http://127.0.0.1:4173/`.
