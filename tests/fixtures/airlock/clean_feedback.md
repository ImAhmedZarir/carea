# Lane-B Sanitized Return Feedback

> **Airlock Feedback Rule:** Observable diffs only.

## `obl_ui_header` — Header spacing (`failed`)

- **CA UI Status:** `failed` | **REA Verification Status:** `passed`
- **Observable UI / Pixel Diff:** At 375px width, header wraps onto two lines with 6px right overflow.
- **Contract Vector `t1`:** `viewport=375x812` -> `scrollWidth <= clientWidth`
