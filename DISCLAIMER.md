# Disclaimer & Responsible Use

`carea` is an independent orchestration layer (agent skill pack, routing specification, and handoff schema) that coordinates two external engines: **REA** (`morluto/rea`) and **Craft Anything** (`storytold/craft-anything`). By using `carea`, you agree to the responsibilities below and to the terms of whichever external engines and tools you run.

## 1. Authorized Use Only

Use `carea` and its orchestrated tools strictly for lawful analysis, interoperability research, security auditing, software preservation, education, and reconstruction of software, websites, systems, captures, or devices that **you own or have explicit authorization to examine**.

`carea` must **not** be used to:

- circumvent DRM, copy protection, license verification, or technical protection measures;
- bypass authentication flows, logins, CAPTCHAs, rate limits, or anti-bot defenses;
- defeat anti-cheat systems, build game cheats, or tamper with live online services;
- copy copyrighted logos, photographs, illustrations, editorial prose, proprietary source code, or protected assets without permission from the rights holder; or
- evade usage policies or safety boundaries of AI providers or third-party platforms.

## 2. Important Notice on "Clean-Room" Claims

`carea`'s Two-Team Clean Room protocol is an **engineering and workflow process aid — NOT legal advice and NOT a guarantee of legal clean-room compliance**:

- **No legal guarantee:** Using `carea` does not by itself establish legal independence or shield any resulting implementation from copyright, trade-secret, patent, or license claims. Obtain qualified legal counsel if legal clean-room standing matters to your project.
- **Tool-level rule, not an OS sandbox:** Craft Anything's `--clean-room` mode is a tool-level policy governing which inspection tools Craft Anything exposes or refuses. It does **not** isolate your filesystem, network, or operating system, and general agent shell/file tools operate under your user permissions unless separately restricted.
- **Single-operator limitation:** A true legal clean room requires genuine organizational and information isolation between separate people/teams. A **single person or single continuous agent session acting as both Analyst and Builder does not create a true legal clean room**, even when following `carea`'s handoff templates.

## 3. External Tools, Runtimes, and Commercial Licenses

`carea` bundles no reverse-engineering binaries, decompilers, fonts, or commercial licenses.

- **Commercial decompilers & tools:** Optional engines supported by upstream tools — including **IDA Pro / Hex-Rays**, **Hopper Disassembler**, and **JEB** — are proprietary products. You must independently obtain valid licenses and follow every vendor EULA, automation restriction, and output-sharing rule. Cracked tools, shared keys, or license-bypass methods are strictly out of bounds.
- **Runtime & device execution:** Dynamic workflows (browser automation, Frida instrumentation, debuggers, ADB device actions, PTY process captures, or package installs) execute under your OS permissions and can modify files, application state, devices, or network traffic. You are solely responsible for reviewing commands, sandboxing untrusted targets, and protecting secrets or captured data.
- **AI providers & generated assets:** Model API keys, coding-agent subscriptions, and optional asset-generation keys (such as `fal.ai`) remain governed by their respective provider agreements.

## 4. No Endorsement & Warranty Disclaimer

`carea` is an independent, unofficial project and is not affiliated with, sponsored by, or endorsed by `morluto` (REA), `ArtCraft Team` / `storytold` (Craft Anything), the NSA (Ghidra), or any commercial tool vendor.

`carea` is provided **"AS IS"**, without warranty of any kind, express or implied, including warranties of merchantability, fitness for a particular purpose, accuracy, or non-infringement, as set forth in [`LICENSE`](LICENSE). You assume full responsibility for determining whether your use is lawful, authorized, and suitable for your task.
