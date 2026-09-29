# Working on this deck

This is a static HTML sales presentation, not a web application. Keep changes small and tied to the requested slide or workflow.

## Start here

- Read `README.md` for local use and the current slide map.
- Read `docs/architecture.md` before changing rendering, build, notes, or export behavior.
- For slide design or copy, read `.agents/skills/planetscale-pitch-design/SKILL.md`.
- Consult the relevant research document in `docs/` when changing a product claim. Research notes are dated evidence, not an automatically current product specification.

## Source of truth

Edit slide content and order in `build_content.py`, standalone diagrams in `assets/`, styles in `theme.css`, and presentation behavior in `app.js`. The user's speaker script is local in ignored `private/speaker-outline.json`; do not commit or deploy it.

`slides.js`, `qa/content.json`, `qa/links.json`, and `Meridian-PlanetScale.html` are generated audience files with no notes. Change their sources, then rebuild:

```sh
python3 build_content.py
python3 package_deck.py --html-only
```

`python3 build_content.py --presenter` and `python3 package_deck.py --html-only --presenter` create ignored local presenter files from the private script. `build_site.py` packages only the audience HTML and PDF into ignored `dist/` for Cloudflare Pages.

Keep the portable filename and slide IDs stable. Existing links use them. Vitalize and Autumn are hidden by default, not deleted. Cloud is included by default.

## Boundaries

- A docs-only request stays docs-only. Do not regenerate the deck or change slide behavior as incidental cleanup.
- Preserve unrelated working-tree changes. Check `git status` before editing.
- Do not replace customer charts with invented curves. Keep units, percentiles, and workload context traceable to the source.
- The speaker script is separate from slide copy. User-requested script imports are not permission to rewrite the script or the evidence.
- Public audience exports and portable HTML exclude speaker notes and presenter controls. Only ignored `private/Presenter.html` has notes.
- Do not use the legacy PDF path in `package_deck.py` with old QA captures to produce a new final export. Capture the current presentation and verify every page.

## Check the change

For code changes, run the two public HTML build commands, `python3 build_site.py`, `node --check app.js`, `node --check slides.js`, and `git diff --check`. Check that `dist/` has no speaker script. Review the affected slide at 16:9 and each reveal state. For documentation, check links, commands, and consistency with the current code; there is no need to rebuild.

Summarize what changed and what was checked. Commit or push when requested.
