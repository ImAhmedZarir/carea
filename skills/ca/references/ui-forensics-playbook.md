# Pro-Dev 1:1 UI & Design System Forensics Playbook (`/ca`)

Systematic inspection protocol so Stage 2 (`/carea` study-only) and standalone `/ca` rebuilds capture **every token, layout constraint, state transition, responsive pivot, and handler binding** at 1:1 engineering precision.

## 1. Multi-Breakpoint Capture Matrix

Always inspect and capture the running target across these exact widths using `web_site_open` -> `web_site_capture` / `web_page_screenshot_take` (never evaluate desktop only):

| Viewport | Device Class | What to Measure & Record |
| --- | --- | --- |
| **320px** | Compact phone floor | Zero horizontal overflow (`scrollWidth <= clientWidth`), non-clipping text wraps, button wrapping |
| **375px** | Primary phone baseline | Mobile nav pattern (bottom bar vs drawer sheet), card stacking, `>=44px` touch targets, `>=16px` input font size |
| **768px** | Tablet pivot | Navigation transition (hamburger -> rail/topbar), grid column expansion (1 -> 2/6 cols), Dialog vs Drawer switch |
| **1024px / 1440px** | Desktop canvas | Max-width container symmetry, collapsible sidebar (`Cmd/Ctrl+B`), asymmetric bento column ratios, hover states |

## 2. Five-State + Theme Coverage (`web_page_states_capture` / `web_page_watch`)

Never sample only the initial static screenshot. Trigger and capture every view state:

1. **Interactive Micro-States:** `:hover` lift/border tint, `:focus-visible` ring offset, `:active` scale compression, `[disabled]` opacity/cursor.
2. **Async & Data States:** `loading` (exact skeleton block geometry/aspect ratio), `empty` (icon/illustration + headline + primary CTA), `error` (inline validation + retry), `offline / stale` banner, `success` toast position/duration.
3. **Overlay & Overlay-Swap Geometry:** Command palette (`Cmd/Ctrl+K`), dropdowns, popovers, modal backdrop opacity/blur, Escape key focus restoration.
4. **Dark & Light Themes:** Record background/card/popover/primary/muted/border hex & `oklch` values in **both** modes, checking edge highlights (`hairline-top`) and contrast (`>=4.5:1` body text).

## 3. Sub-Pixel Surface, Typography & Motion Spec

Document concrete measured values into `design-system.md` rather than vague adjectives:

- **Elevation Tiers:** `L0` page canvas, `L1` elevated surface + `1px` border + dark-mode inner top highlight, `L2` popover/dropdown shadow, `L3` modal backdrop + blur.
- **Typography Scale:** UI font family, Monospace font family (`tabular-nums` alignment on all counters/timers/prices), H1->H4 clamp/step scale, letter-spacing (`tracking-tight` vs `tracking-widest`), line-height, measure cap (`max-width: ~65ch`).
- **Spacing & Radius Grammar:** Base spacing unit (4px/8px), container horizontal gutter (`px-4 sm:px-6 lg:px-8`), section vertical padding, card internal padding, shared `--radius` hierarchy.
- **Motion Physics:** Transition duration (150ms feedback vs 350–500ms entrance), easing curve (`cubic-bezier(...)`), GPU-composited properties (`transform`/`opacity`).

## 4. Handler, Module & API Binding (When `--deep` or REA Paired)

Tie every visual component directly to behavior and backend calls:
- Event hooks on controls: `web_listeners_list`
- Bundled component chunks: `web_modules_trace` / `js_app_map` / `js_runtime_code_match`
- Live DOM <-> bundle source lookup: `js_source_locate` / `web_page_js_analyze`
- Captured API traffic -> working local stand-in server: `web_recording_show` -> `web_standin_build` -> `web_standin_start`
- Pixel verification after rebuild: `web_pixels_compare`, `web_snapshots_compare`, `web_walkthrough_check`, `runtime_captures_compare`
