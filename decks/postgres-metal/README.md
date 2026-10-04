# Postgres on Metal pitch

Existing static HTML sales presentation. The default flow has 11 slides, with Vitalize and Autumn available as optional case studies. It is separate from the final-round teach-back.

- [Architecture and export behavior](architecture.md)
- [Pitch story and slide flow](pitch-blueprint.md)
- [Shared product research](../../context/README.md)
- [Design skill](../../.agents/skills/planetscale-pitch-design/SKILL.md)
- [Current PDF](output/pdf/PlanetScale-Postgres-on-Metal.pdf)
- [Portable audience HTML](Meridian-PlanetScale.html)

Run `npm run build:pitch` from the repository root. For development, run `npm run serve` and open `/decks/postgres-metal/index.html`. Run `npm run build:presenter` for the existing ignored local speaker script, then use the root `Present-PlanetScale.command` launcher.

Canonical editable sources: `build_content.py`, `app.js`, `theme.css`, `index.html`, and `assets/`. `slides.js`, portable HTML, and QA content/link JSON are generated. `qa/` also retains benchmark provenance and historical captures. `vendor/` holds the local Reveal.js runtime and license.

The PDF is the existing export; a source rebuild does not regenerate it. Root `build_site.py` packages this deck and PDF under the existing `/planetscale/` URL. Local `private/` and `references/` remain ignored.
