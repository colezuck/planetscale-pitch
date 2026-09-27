# PlanetScale — Postgres on Metal

Version 2. A seven-slide, 10–15 minute technical sales presentation for a general Postgres prospect. The close is technical discovery plus a migration assessment.

## Present

Open `Meridian-PlanetScale.html` in a browser. It is a portable file containing the deck, font, logos, charts and speaker notes; the filename is preserved so existing preview links continue to work.

- Arrow keys: move through the seven slides.
- O: slide overview.
- Notes: private reading dialog for the current slide.
- S: separate Reveal presenter view in browsers that allow pop-ups; serve locally for this feature.
- F: fullscreen.
- B: black screen.

The PDF is a static 16:9 presentation backup. Speaker notes are also available in `speaker-notes.md`.

## Narrative

1. Hosted Postgres on Metal: local NVMe, unlimited IOPS, and a path to scale.
2. Vitalize's Postgres migration and measured results.
3. Full-height three-zone node architecture and control plane.
4. Postgres Metal throughput and p99 benchmark evidence.
5. Neki's sharded Postgres architecture.
6. Neki's measured scale for a defined workload.
7. Migration partnership and the technical discovery close.

Technical qualifications and benchmark configurations are in the speaker notes. The Neki benchmark is identified as read-only point selects on primary-only shards. Neki's preview status belongs in the spoken introduction and remains in the notes. No source labels or research appendix are shown in the deck.

## Edit

`build_content.py` contains slide copy, speaker notes and editable SVG diagrams. Run it to regenerate `slides.js`, `speaker-notes.md` and the slide manifest. `theme.css` controls the design. `app.js` controls rendering and presentation controls.

Run `python3 package_deck.py --html-only` to rebuild the portable HTML. Serve this folder on localhost and review it in a browser. For the PDF, capture each final slide in a 16:9 browser view as `qa/slide-01.png` through `qa/slide-07.png`, then run `package_deck.py` with a Python environment containing ReportLab and pypdf. The HTML remains the editable master; the PDF is a raster snapshot with bookmarks.

Official PlanetScale, PostgreSQL, Cash App and Neki artwork is stored in `assets/`. Reveal.js and Inter licenses are included. This is an interview sample, not an actual customer proposal.

## Visual system

Diagrams and charts follow the supplied PlanetScale ASCII reference: system monospace labels, square frames, double-line primaries, stippled fills and dashed connectors. Inter remains the headline font. Neki uses yellow as its accent. The Vitalize latency curve is the original customer-published chart, clipped to the plot area with larger native axis labels; it is not a generated time series.

## Repository workflow

This folder is an independent Git repository. Edit `build_content.py`, `theme.css` and `app.js`; do not edit generated slide content directly.

```sh
python3 build_content.py
python3 package_deck.py --html-only
python3 -m http.server 8765 --bind 127.0.0.1
```

Review all seven slides, then commit the source and updated portable HTML together. Refresh `qa/slide-01.png` through `qa/slide-07.png` before rebuilding the PDF. The seven captures are versioned so the PDF can be reproduced; temporary QA images and source ZIPs are ignored. PDF packaging requires `reportlab` and `pypdf`. Keep reference presentations in the ignored `references/` folder.

## Durable pitch context

- [Customer case studies](docs/customer-case-studies.md): customer-reported results, comparisons, limitations, and selection guidance.
- [Pitch blueprint](docs/pitch-blueprint.md): Gong-based sequencing and delivery plan.
- [Postgres Metal benchmarks](docs/postgres-metal-benchmarks.md): workload definitions, selected data, configuration differences, and pitch framing.

## Slide layout conventions

The PlanetScale header logo appears only on the opening slide; slide 3 also uses the logo inside the control-plane bar to identify platform ownership. Its single-line “Postgres on Metal” heading sits above a product overview: managed Postgres and Metal, Neki for horizontal scale, and the shared PlanetScale platform and infrastructure team. Node topology belongs on slide 3. Content slides start directly with a single-line heading. Keep secondary results with their charts (for example, “Half the vCPUs” above the Vitalize compute chart), and give diagrams their full available width. Neki branding stays in its title row. Avoid restoring a repeated logo spacer or decorative banner.
