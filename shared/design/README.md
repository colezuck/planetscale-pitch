# PlanetScale visual system

The reusable slide workflow, sales framework, layout recipes, animation guidance, and lessons from past corrections live in the [PlanetScale pitch design skill](../../.agents/skills/planetscale-pitch-design/SKILL.md). Use it for brand styling, technical diagrams, copy, and staged reveals.

The current implementation lives in [theme.css](../../decks/postgres-metal/theme.css), [app.js](../../decks/postgres-metal/app.js), and [assets](../../decks/postgres-metal/assets/). Source logos and font licenses remain alongside that deck. Reuse those sources rather than copying a second asset library.

This folder is the shared entry point for visual decisions. Reusable diagram implementation lives in `shared/presentation/`; source artwork and the original theme remain with the Metal deck.

Create a clean deck shell with `python3 .agents/skills/planetscale-pitch-design/scripts/new_deck.py --name <deck-name> --title "<title>"` from the repository root. It copies the proven canvas, runtime, brand assets, and controls, without copying the Metal sales content. See the skill for image embedding, presenter builds, and review.

For smooth Nexus-style system diagrams, use the [shared diagram framework](../presentation/README.md). Its nodes, ports, and named stages keep the same SVG objects connected while resizing; the slide skill covers how to choose the story and composition.
