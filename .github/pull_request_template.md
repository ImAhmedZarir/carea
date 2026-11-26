## Summary
Briefly explain what changed and why.

## Checklist
- [ ] No upstream source code, binaries, fonts, logos, or brand marks were copied (`CONTRIBUTING.md`).
- [ ] Any new upstream tool names, flags, env vars, or versions are verified in `docs/upstream-facts.md` (and excluded from `skills/**` if `UNVERIFIED`).
- [ ] Compatibility matrix edits were made only in `compat/matrix.json` and `python scripts/render-compatibility.py --check` passes.
- [ ] Ran `python -m unittest discover -s tests -v` and `python scripts/check_repo.py` cleanly after final edits.
- [ ] Preserved MIT attribution (`LICENSE`), brand restrictions (`BRAND.md`), and `DISCLAIMER.md` boundaries.
