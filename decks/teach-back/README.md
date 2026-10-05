# Teach-back presentation

Six-slide animated Reveal.js draft for an Aurora PostgreSQL staff engineer: clean cover, actual Aurora architecture and vertical scale-up, local NVMe comparison, the original Postgres benchmark slide, Convex customer outcome, and a five-row tradeoffs comparison. Built locally, not included in the published site.

Read the [slide plan](../../interview/teach-back/slide-plan.md), [speaking outline](../../interview/teach-back/script-outline.md), [Q&A](../../interview/teach-back/questions.md), and [evidence review](../../context/product/aurora-metal-teach-back.md). The comparison reuses the original Metal pitch’s EBS/local-NVMe hardware geometry and labels. The static storage figures are illustrative references: io2 ~400 µs, gp3 ~1 ms and local NVMe ~50 µs. Source qualifications live in the notes; these are not Aurora measurements or a measured Metal mean. Convex’s exact original slide is the active customer proof, with its two original chart panels and query/batch-commit results. Depot is hidden.

Run from the repository root:

```sh
npm run build:teach-back
npm run build:teach-back:presenter
npm run serve
```

Preview `/decks/teach-back/index.html`; open [Audience.html](Audience.html) for portable audience delivery. The presenter command derives its local notes from the tracked speaking outline, then embeds them in ignored `private/Presenter.html`. The audience build excludes those notes. The portable HTML embeds Reveal.js, fonts, logos, diagrams and motion code; no external connection is needed for delivery.

Edit `content.json` for slide copy and surrounding markup, `diagrams/` for scene geometry/reveals, `theme.css` for composition, and `app.js` for behavior. `slides.js`, `Audience.html`, and `runtime/` are generated. The local builder supports `beforeHtml`/`afterHtml` around `diagramFile` for accompanying content without duplicating diagram markup. Use the [slide skill](../../.agents/skills/planetscale-pitch-design/SKILL.md) and [shared framework](../../shared/presentation/README.md) when iterating.

Asset provenance: PlanetScale logo, Inter font/license and Reveal runtime/license come from the existing Metal deck. `assets/metal-path.svg` adapts its hardware geometry with deck-specific IDs and synchronized metric reveals. `assets/depot-iowait-original.webp` is downloaded from Depot’s published case study and embedded in both development and portable builds; CSS adjusts contrast/colors while preserving the source pixels, axes and legend. [Source and checksum](../../context/evidence/depot-metal-art.md). The older `depot-latency.svg` bars are unused. The inline history art is explicitly schematic, not reconstructed telemetry.

Validation October 4, 2026: repository build/check and five-slide presenter generation passed. Portable audience visuals reviewed at 1440×810, including forward/reverse reveals, direct fragment hashes, Aurora revisit reset and same-line cover. Aloud five-minute timing remains to be rehearsed.

Art revision: original Depot CPU chart and retention-boundary schematic replace the initial bars. Aurora resources grow vertically; the network connector stays level. The comparison shows EBS io2 and illustrative NVMe storage figures. Build/check/presenter generation passed after this revision.

Tradeoffs revision: `fit` is now an art-free comparison table. All rows are visible; it no longer uses the retained `diagrams/capacity.json`. Comparison headings are PlanetScale Metal and Aurora.

Convex revision: exact slide markup and CSS copied from `decks/postgres-metal/`; original image and logo copied unchanged. Depot has `hidden: true` in `content.json`, so audience and presenter outputs exclude it entirely. Its source, assets and [script](../../interview/teach-back/depot-hidden-script.md) remain for later.
