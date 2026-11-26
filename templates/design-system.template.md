# Extracted UI/UX & Design System Specification (`design-system.md`)

> **No Asset/Prose Copying:** Describe structural hierarchy, original token roles, responsive rules, and interaction states. **NEVER copy target logos, images, fonts, or proprietary copy verbatim.** Use `assets_image_generate` / original typography for any rebuild.

- **Target:** `<url | apk | exe>`
- **Viewports Studied:** `375px` (mobile), `768px` (tablet), `1440px` (desktop)
- **Theme Behavior:** `<dark / light / adaptive>`

---

## 1. Visual Hierarchy & Navigation Shell

- **App Shell Pattern:** `<Top sticky nav / Bottom tab bar / Collapsible rail / Window toolbar>`
- **Primary Route Map:**
  - `/` — `<Home / Workspace purpose>`
  - `/...` — `<Secondary screens / dialogs / sheets>`
- **Overlay Swap Behavior:** `<Dialog on desktop -> bottom sheet / drawer on <768px>`

---

## 2. Layout Grid & Spacing Rhythm

- **Base Spacing Grid:** `<4px / 8px rhythm>`
- **Content Max Width & Margins:** `<Container width, desktop column split, mobile stacking rules>`
- **Touch Target Minimums:** `<>=44px mobile controls, gap rules>`

---

## 3. Original Token Palette & Typography Roles

| Token Role | Surface / Ink Role | Notes (Original Values) |
| --- | --- | --- |
| Canvas (`background`) | Primary app canvas | `<Measured dark/light contrast intent>` |
| Elevated (`card`) | Panels & inspectors | `<1px hairline border + subtle depth>` |
| Accent (`primary`) | Single high-contrast CTA/focus | `<Restrained 10% accent usage>` |
| Display / UI / Mono | Font hierarchy | `<Distinct heading, body, and tabular-nums metrics>` |

---

## 4. Screen Inventory & Interactive States

Each screen/data widget must account for all five states:
- **Loading:** `<Skeleton structure>`
- **Empty:** `<Actionable zero-state>`
- **Error:** `<Recovery prompt + retry>`
- **Partial / Offline:** `<Stale indicator>`
- **Success:** `<Interactive layout & feedback toasts>`

---

## 5. Rebuild Checklist for Craft Anything

1. Capture multi-viewport reference screenshots (`web_site_capture` / `adb_screenshot_take` / `native_window_capture`).
2. Generate original replacement visuals (`assets_image_generate` / clean SVG) if media assets exist.
3. Verify visual + interaction parity (`rebuild_check`, `web_pixels_compare`, `web_walkthrough_check`, `runtime_captures_compare`).
