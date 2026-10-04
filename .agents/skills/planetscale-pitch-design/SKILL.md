---
name: planetscale-pitch-design
description: Create and iterate technical sales slides in this repository's PlanetScale style, including SVG diagrams, sourced images and charts, Reveal.js animations, speaker outlines, and portable HTML. Use the Postgres on Metal deck as the visual and sales reference; applies to new decks and focused slide edits.
---

# PlanetScale sales slides

Build slides a technical buyer can understand while Cole speaks. Reuse the proven visual system and make each reveal explain a change. The reference is the current rendered [Postgres on Metal deck](../../../decks/postgres-metal/README.md), not old screenshots or every sentence in its private script.

Locate the repository through `AGENTS.md`. Repository paths below are relative to that root. Preserve the user's requested medium, slide count, content scope, and existing approvals. Default to this repo's static HTML/Reveal.js workflow for an animated deck; use the available presentation skill if the user specifically requests editable PPTX. Do not silently substitute HTML for PowerPoint.

## Select the work

- **New deck:** read [sales framework](references/sales-framework.md) and [visual recipes](references/visual-recipes.md). Create a clean shell with `scripts/new_deck.py`; do not duplicate the Metal pitch's claims, optional slides, old scripts, or deployment configuration.
- **Copy or story edit:** read [sales framework](references/sales-framework.md). Inspect the relevant product/account evidence before writing claims.
- **Art, diagram, chart, image, or layout:** read [visual recipes](references/visual-recipes.md), including its source-image rules.
- **Reveal or animation:** read [motion and delivery](references/motion-and-delivery.md). For Nexus-style diagrams, use the [shared scene framework](../../../shared/presentation/README.md) and its authoring guide rather than duplicating complete SVG layers or writing new state handlers.
- **Build, export, or final review:** read [motion and delivery](references/motion-and-delivery.md) and run the relevant commands.

Read [past corrections](references/past-corrections.md) before choosing a new chart treatment or substantial layout. For a focused text edit, consult only the relevant correction. Do not load every reference for every small change.

## Working contract

Before making slides, resolve audience, buyer problem, desired next step, available time, and source evidence from the request and repository. Ask only for missing information that materially changes the result; otherwise state the assumption and proceed. For interview work, `interview/brief/README.md` outranks the earlier pitch blueprint as assignment context.

Use a short slide plan in the target exercise or deck folder: ID; buyer question; slide purpose; visual recipe; evidence and limitations; reveal states; spoken point; check-in or next-step question. Keep one job per slide. For edits, update the existing plan instead of creating parallel documents.

The baseline is a 1440 × 810 canvas, Inter headings, monospace technical labels, #111111 background, #fafafa text, #f35815 product emphasis, #ff4d4d bottlenecks, thin square frames, sparse stipple, and explicit connectors. Yellow identifies the Neki story in the reference; do not make it a generic accent. Keep slides conversational and technical rather than filling them with UI panels.

Claims need a source and an applicable comparison. Product research lives in `context/`; shared account evidence in `accounts/`; exercise scripts in `interview/`. Label scenario premises and hypotheses. Source the speaker outline from evidence too: the existing private script demonstrates delivery structure, but its superlatives and availability claims are not approved reusable facts.

Edit canonical sources and rebuild. Preserve stable slide IDs and audience/presenter separation. Never fix generated HTML instead of its source. A local preview working does not prove that a portable export embeds a newly inserted image.

## Fast iteration

Implement the smallest slide or state that answers the buyer question. Preview it before extending the deck. Change one cause at a time: copy length, geometry, image framing, or reveal timing. Match the current theme before inventing a new treatment. Shorten copy or recompose before shrinking labels.

Check the initial state, each settled reveal, and backward navigation. Inspect at 16:9 after fonts/images load. Capture exports only after transitions settle. Verify source HTML and portable HTML both show inserted images. Record reusable corrections in the relevant reference with a concrete trigger and fix; do not turn a one-off preference into an unrelated universal rule.

The existing deck's builds are documented in `decks/postgres-metal/README.md`. The starter creates its own `build.py` and `package.py`; see [motion and delivery](references/motion-and-delivery.md). Publishing and PDF regeneration are separate tasks, not incidental steps in editing.
