# How the deck works

The deck is static HTML with a small Python content build. There is no backend, framework build, or remote asset dependency during presentation.

## Content to presentation

```text
assets/ + qa/data ─────── build_content.py ── slides.js (audience only)
                               └─ qa/content.json + qa/links.json
private/speaker-outline.json ── build_content.py --presenter
                               └─ private/slides.js + private/speaker-notes.md

index.html + slides.js + app.js + theme.css + vendor/ + assets/
                      └─ package_deck.py --html-only
                           └─ Meridian-PlanetScale.html
private/slides.js ───── package_deck.py --html-only --presenter
                           └─ private/Presenter.html
Meridian-PlanetScale.html + current audience PDF
                      └─ build_site.py ── dist/planetscale/ (Pages upload)
                                          dist/index.html (landing page)
```

`build_content.py` defines slide copy, generates several vector diagrams, and reads the standalone diagrams and benchmark data. The default `window.PITCH_SLIDES` output contains each slide's ID, label, theme, and HTML. The `--presenter` build reads the private script, verifies its slide IDs, and adds notes to the private output.

`app.js` selects visible slides, creates the slide sections and note lists, and initializes Reveal.js. `theme.css` positions content within a fixed 1440 × 810 canvas. Reveal scales that canvas to the viewport; the presentation stays in slide mode rather than switching to a scrolling page.

`index.html` loads separate source files for development. `Meridian-PlanetScale.html` bundles CSS, JavaScript, fonts, and artwork into one audience file. Neither includes notes. `private/Presenter.html` bundles the same slides with the local notes.

## State and controls

Slide IDs form the URL hash, such as `#/intercom`. Reveal handles navigation and fragment indices. The app listens for slide and fragment changes to update the Nexus and Intercom artwork.

| Option | Behavior |
| --- | --- |
| `?present` | Hide the on-slide toolbar; retain keyboard controls |
| `?vitalize` | Include the hidden Vitalize case study |
| `?autumn` | Include the hidden Autumn case study |
| `?cloud` | Accepted by old links; cloud is now included by default |
| Direct hash for a hidden slide | Include that slide for review |

The optional-slide filter lives in `app.js`; the full order lives in `build_content.py`. The default deck has 11 slides, with two additional case studies available. Local presenter notes are keyed by stable slide ID, not by visible slide number.

## Notes and presenting

`private/speaker-outline.json` is the ignored editable script. Build with `--presenter` to produce a readable private Markdown copy and notes on each slide in the private HTML. The app then enables the Notes dialog and Reveal's separate presenter window. The public build has no notes and does not load the presenter plugin.

A local HTTP server is recommended for presenter view. `Present-PlanetScale.command` serves this folder on an available localhost port between 8765 and 8774 and opens `private/Presenter.html`. It reuses a server only when that server serves the same HTML file.

In the local presenter build, the Notes dialog is inside the slide window and the presenter window is separate. For screen sharing, share only the slide window.

`build_site.py` places the audience HTML and current PDF under `dist/planetscale/`, writes a minimal landing page at `dist/index.html`, and redirects the former root deck and PDF URLs. `npm run deploy` uploads that folder to the classic Cloudflare Pages project. The private script and presenter build are ignored by Git and never enter `dist/`.

## Exports

The current audience PDF is `output/pdf/PlanetScale-Postgres-on-Metal.pdf`. It contains 14 pages: the 11 default slides, with two Nexus states and three Intercom states. Pages use lossless 4320 × 2430 captures of the rendered HTML on a 16:9 PDF canvas. Notes and controls are excluded from the export.

The export does not modify the live deck. To update it, capture the current rendered states with fonts and assets loaded, then package them at the same aspect ratio. Review the PDF after rendering it back to images. Rebuilding layouts separately can change spacing, SVG rendering, and font metrics.

`package_deck.py` also contains an older PDF path that reads numbered PNGs from `qa/`. Those captures are historical and do not reproduce the current deck. Use `--html-only` for normal builds. `output/archive/Meridian-PlanetScale.pdf` is the legacy output, not the current handoff.

## Evidence and assets

`assets/` contains source artwork and customer charts. `assets/site-prism-color.svg` is the color-only personal homepage background; `build_site.py` copies it and the existing PlanetScale symbol into the Pages upload. `assets/previews/` holds historical slide snapshots; the build does not use them. `qa/` contains benchmark data, provenance, and earlier layout checks. Historical checks are useful context, not evidence that the current version has passed review.

`docs/` separates product and customer evidence from the spoken script. The dates in those documents identify the research snapshot. Verify changing product details against their original sources before adding new claims.

`vendor/` contains local Reveal.js files and its license. The Inter license lives with the font in `assets/`. Keep bundled dependency changes separate from slide edits.
