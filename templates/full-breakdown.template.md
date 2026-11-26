# Complete Reverse Engineering Breakdown (`full-breakdown.md`)

> **Reverse-Engineer-Only Guarantee:** Produced strictly from **Stage 1 (`/rea` internal evidence)** and **Stage 2 (`/ca` observable UI/runtime study)** without executing `rebuild_start` or generating replacement app code.
> **Evidence Discipline:** Label every claim cleanly as `[OBSERVED ev_...]`, `[CA CAPTURE]`, `[INFERRED]`, or `[UNKNOWN unk_...]`.

- **Target:** `<url | .apk | .exe | folder>`
- **Target Kind:** `<web-app | electron-app | android-apk | native-binary | managed-assembly | game | firmware>`
- **Stage 1 Engine (`/rea`):** `<REA version / evidence IDs>`
- **Stage 2 Engine (`/ca` Study Only):** `<CA clean-room/deep session ID — capture/study only, no rebuild>`

---

## 1. Executive Summary & System Purpose

- **What it does:** `<Concise technical summary of the target application>`
- **Primary Stack & Runtime:** `<Frameworks, runtimes, bundles, native libraries>`
- **Companion Reports:**
  - Architecture details: [`architecture.md`](architecture-report.template.md)
  - UI/UX & Design tokens: [`design-system.md`](design-system.template.md)

---

## 2. Stage 1 Findings (`/rea` Internal Analysis)

- **Entrypoints & Packaging:** `<Main binary/activity/HTML entry, exported symbols, bundle structure>`
- **Core Logic & State Machines:** `<Key controllers, validation/domain rules, state transitions>`
- **Network / API / IPC / Storage:** `<Observed endpoints, payloads, SQLite/IndexedDB/localStorage/JNI bridges>`
- **Evidence IDs Recorded:** `<ev_...>`

---

## 3. Stage 2 Findings (`/ca` Observable Study — No Code Built)

- **Screen & Route Map:** `<Pages, navigation patterns, dialogs/drawers>`
- **Responsive & State Coverage:** `<375px mobile vs 1440px desktop differences; loading/empty/error states>`
- **Interaction Walkthrough:** `<Verified user flows observed in browser/window/adb capture>`

---

## 4. Open Unknowns (`unk_...`) & Next Step (Opt-In Rebuild)

- **Unresolved Gaps:**
  - `unk_01`: `<What stayed dynamic, encrypted, authenticated, or out of reach>`
- **To Build Later (Explicit Opt-In Only):** Ask the user if they want an opt-in Mode 1 (`/ca` UI rebuild), Mode 2 (`two-team-process` Airlock), or Mode 4 (`private-deep-rebuild`).
