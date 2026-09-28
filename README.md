# PlanetScale — Postgres on Metal

Working deck: ten core slides, with optional Vitalize and cloud deployment slides (twelve in the full deck). The opening is a minimal PlanetScale / Postgres on Metal hero, followed by a buyer-focused Nexus. Migration closes the deck. The pitch supports discovery, with technical detail selected around the buyer’s priorities.

## Present

Open `Meridian-PlanetScale.html` in a browser. It is a portable file containing the deck, font, logos, charts and speaker notes; the filename is preserved so existing preview links continue to work.

- Arrow keys: move through the slides.
- O: slide overview.
- Notes: private reading dialog for the current slide.
- S: separate Reveal presenter view in browsers that allow pop-ups; serve locally for this feature.
- F: fullscreen.
- B: black screen.

The PDF is a static 16:9 presentation backup. Speaker notes are also available in `speaker-notes.md`.

## Narrative

1. PlanetScale / Postgres on Metal hero.
2. Nexus: establish the common cloud Postgres capacity model, grow vCPU/RAM/storage, then reveal latency, high availability, and storage I/O; pause for discovery.
3. Convex: production migration and reported p99 results.
4. Vitalize: migration outcomes (optional).
5. Autumn: migration support and reported latency outcomes.
6. Postgres cluster architecture and high availability.
7. Why Metal: local NVMe versus network-attached storage.
8. Postgres on Metal throughput and p99 benchmark evidence.
9. Neki’s sharded Postgres architecture.
10. Neki’s measured scale for a defined workload.
11. Cloud deployment and networking responsibilities (optional).
12. Self-service and PlanetScale-led migration options, closing with technical discovery and assessment.

Technical qualifications and benchmark configurations are in the speaker notes. The Neki benchmark is identified as read-only point selects on primary-only shards. Neki's preview status belongs in the spoken introduction and remains in the notes. No source labels or research appendix are shown in the deck.

## Edit

`build_content.py` contains slide copy, speaker notes and editable SVG diagrams. Run it to regenerate `slides.js`, `speaker-notes.md` and the slide manifest. `theme.css` controls the design. `app.js` controls rendering and presentation controls.

Run `python3 package_deck.py --html-only` to rebuild the portable HTML. Serve this folder on localhost and review it in a browser. For the PDF, capture each final slide in a 16:9 browser view as `qa/slide-01.png` through `qa/slide-09.png`, then run `package_deck.py` with a Python environment containing ReportLab and pypdf. The HTML remains the editable master; the PDF is a raster snapshot with bookmarks.

Official PlanetScale, PostgreSQL, Cash App, Neki, Convex and Autumn artwork is stored in `assets/`. Reveal.js and Inter licenses are included. This is an interview sample, not an actual customer proposal.

## Visual system

Diagrams and charts follow the supplied PlanetScale ASCII reference: system monospace labels, square frames, double-line primaries, stippled fills and dashed connectors. Inter remains the headline font. Neki uses yellow as its accent. The Vitalize latency curve is the original customer-published chart, clipped to the plot area with larger native axis labels; it is not a generated time series.

## Repository workflow

This folder is an independent Git repository. Edit `build_content.py`, `theme.css` and `app.js`; do not edit generated slide content directly.

```sh
python3 build_content.py
python3 package_deck.py --html-only
python3 -m http.server 8765 --bind 127.0.0.1
```

Review all slides, then commit the source and updated portable HTML together. Refresh `qa/slide-01.png` through `qa/slide-09.png` before rebuilding the PDF. The nine captures are versioned so the PDF can be reproduced; temporary QA images and source ZIPs are ignored. PDF packaging requires `reportlab` and `pypdf`. Keep reference presentations in the ignored `references/` folder.

## Durable pitch context

- [Customer case studies](docs/customer-case-studies.md): customer-reported results, comparisons, limitations, and selection guidance.
- [Migration options](docs/migration-options.md): self-service tooling, migration services, and closing-slide positioning.
- [Pitch blueprint](docs/pitch-blueprint.md): Gong-based sequencing and delivery plan.
- [Postgres Metal benchmarks](docs/postgres-metal-benchmarks.md): workload definitions, selected data, configuration differences, and pitch framing.

## Slide layout conventions

The opening contains only a centered PlanetScale logo and “Postgres on Metal,” with Metal in orange. Nexus first shows a Postgres server with vCPU/RAM and a separate network-attached volume. Advance once to grow compute and storage; advance again to change the headline and reveal latency, high availability, and storage I/O as discovery topics. Provider names, replicas, and operational details belong in the notes; this is a capacity model, not a complete HA topology. The PDF shows the final reveal on one page. Research and boundaries are in `docs/nexus-research.md`. Content slides otherwise use single-line headings. Keep secondary results with their evidence and give diagrams their full available width. Neki branding stays in its title row.

### Optional cloud deployment slide

The core pitch keeps ten slides. Add the cloud/account discussion immediately before migration with `?cloud`, or open `Meridian-PlanetScale.html?cloud#/cloud` directly. Combine `?cloud&vitalize` to include both optional slides. Cloud deployment sources, region guidance, and BYOC discovery questions are in this slide's notes.
