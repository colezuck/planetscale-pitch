---
name: planetscale-pitch-design
description: Design or refine slides, SVG artwork, and sales copy for this PlanetScale Postgres on Metal pitch deck, including customer stories and the Neki preview. Use the existing HTML deck and visual system.
---

# PlanetScale pitch design

Make the buyer understand a problem, see credible evidence, and agree on a useful next step. The audience is a technical leader; the presentation is a sales conversation, not a component tour.

Locate the repository through the nearest `AGENTS.md`. Read `docs/architecture.md` for implementation boundaries and `docs/pitch-blueprint.md` for the current story. Read only the research document relevant to the claim being changed.

## Visual language

Use the existing tokens in `theme.css`: `#111111` background, `#fafafa` text, `#f35815` Metal/product emphasis, `#fbca00` for Neki, and `#ff4d4d` for bottlenecks. Match existing muted borders and labels.

Use Inter for headlines and system monospace for technical labels. Keep diagrams rectangular: square corners, thin frames, occasional double outlines, sparse stipple, and directional connectors. Use the bundled logos and source artwork. Avoid decorative gradients, generic rounded cards, stock illustrations, and emoji labels.

The slide canvas is 1440 × 810. Content uses 64 px side margins and a vertically centered composition. Budget the heading, art, metrics, and whitespace together. Keep captions and arrowheads clear of container boundaries. Repeated cards share edges and baselines. A bigger icon should explain scale, not displace the connector.

Prefer one-line headlines when they remain readable. If text does not fit, shorten the copy before shrinking the type. Keep original charts at their native resolution; change their framing without inventing data.

## Sales copy

Use concrete outcomes: fewer slow requests, more workload headroom, less recovery work, lower reported cost. Connect the mechanism to the outcome rather than listing features.

Customer slides tell a short story: pressure → previous response → observed result. An outcome headline can remain fixed while the visual reveals the story. Use a clear replacement or fade between states, without overlapping labels or a flash frame.

Keep one job per slide. Use notes for the spoken explanation and discovery questions, and research docs for sources and limitations. Do not turn every caveat into audience-facing copy, but do not remove the information needed to interpret a claim.

Distinguish Postgres customer results, Vitess/MySQL stories, vendor benchmarks, and Neki preview experiments. A reported result is not a customer guarantee. Storage-path latency is not query latency; an SLA is not observed uptime. Do not introduce unverified exclusivity, universal speed claims, or zero-downtime promises.

## Implement and review

Edit the canonical sources described in `AGENTS.md`; rebuild only when slide content or behavior changes. Keep notes outside `.slide-content`. Preserve the slide IDs and requested optional-slide behavior.

Review the initial state and every meaningful reveal. Check text fit, vertical balance, arrow visibility, chart labels, and provider/card alignment. For a PDF, export the rendered HTML states rather than reconstructing layouts in a second drawing system. Strip notes and controls from the export, use 16:9 pages, and inspect every page.
