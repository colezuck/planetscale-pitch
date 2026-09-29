# Postgres on Metal

A PlanetScale sales pitch for a technical buyer already running Postgres. Built for an SDR interview: find the pressure, show the evidence, earn the next conversation.

Dark slides. Square diagrams. Actual customer charts. [See the deck](https://colezuck.com/).

## Open the deck

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open [the public presentation](http://127.0.0.1:8765/Meridian-PlanetScale.html?present#/opening). It has no speaker notes. Your local, ignored `private/Presenter.html` is the presenter version; build it with the commands below. On macOS, double-click `Present-PlanetScale.command` to serve and open that version.

| Key | What it does |
| --- | --- |
| ← / → | Previous / next slide or reveal |
| S | Separate presenter window on the local presenter version only |
| O | Slide overview |
| F | Fullscreen |
| B | Black screen |

For Zoom, share the slide window and keep the presenter window private. Allow localhost popups for speaker view. Remove `?present` to bring back the on-slide controls.

## Send it

[Download the audience PDF](https://colezuck.com/PlanetScale-Postgres-on-Metal.pdf): 14 widescreen pages, including staged Nexus and Intercom reveals. No speaker notes. The export uses 4320 × 2430 captures of the actual slides. The [local copy](output/pdf/PlanetScale-Postgres-on-Metal.pdf) is the file deployed with the site.

`Meridian-PlanetScale.html` is the portable audience presentation, with fonts and artwork embedded. It contains no speaker notes. The `Meridian` filename stays so existing links keep working. The public Pages upload contains only the deck and PDF.

The older nine-page PDF is archived at `output/archive/Meridian-PlanetScale.pdf`. Use the linked audience PDF above.

## The story

The default deck has 11 slides:

1. **Postgres on Metal** — introduce the conversation and ask what hurts.
2. **Nexus** — show the common capacity model, then its unresolved bottlenecks.
3. **Convex** — production Postgres latency evidence.
4. **Intercom** — peak-load pain, a costly workaround, then Metal results. This is a Vitess/MySQL story.
5. **What is Metal?** — explain the local storage path.
6. **Performance** — throughput and p99 from a defined benchmark.
7. **Architecture** — primary, replicas, availability zones, and managed operations.
8. **Neki** — preview the path beyond one machine.
9. **Neki at scale** — a specific read benchmark, not a promise for every workload.
10. **Cloud** — hosted or BYOC, operated by PlanetScale.
11. **Migration** — two delivery paths and one concrete next meeting.

Vitalize and Autumn remain available with `?vitalize` and `?autumn`. Combine options with `&`, for example `?present&vitalize`. Cloud is included by default; the older `?cloud` links still work.

## Change a slide

| File | Edit here for… |
| --- | --- |
| `build_content.py` | Slide copy, ordering, and generated SVG diagrams |
| `assets/` | Source artwork, customer charts, and standalone SVG diagrams |
| `private/speaker-outline.json` | Local speaker script, keyed by slide ID; ignored by Git |
| `theme.css` | Typography, layout, color, and motion |
| `app.js` | Rendering, controls, optional slides, and reveal state |

Rebuild after editing:

```sh
python3 build_content.py
python3 package_deck.py --html-only
```

This updates the audience-only `slides.js`, QA manifests, and portable HTML. To rebuild your local presenter version with the ignored script:

```sh
python3 build_content.py --presenter
python3 package_deck.py --html-only --presenter
```

That writes `private/Presenter.html`, `private/slides.js`, and `private/speaker-notes.md`. Reload the deck; reopen speaker view if it was already open. Python 3 is enough for the HTML builds.

To assemble and deploy the public site, run `npm install`, then `npm run build` and `npm run deploy`. The build copies only the audience deck and PDF into ignored `dist/`; Wrangler uploads that folder to Cloudflare Pages. Keep the local `private/` directory out of commits and uploads.

For code edits, run `node --check app.js`, `node --check slides.js`, and `git diff --check`. Review affected slides and their reveals in the browser. A successful build does not prove a layout looks right.

## Under the hood

- [Architecture](docs/architecture.md) — source files, rendering, notes, and export boundaries.
- [Pitch structure](docs/pitch-blueprint.md) — the sales logic behind the order.
- [Research index](docs/README.md) — evidence and claim boundaries.
- [AGENTS.md](AGENTS.md) — guidance for working in this repo.
- [PlanetScale pitch design skill](.agents/skills/planetscale-pitch-design/SKILL.md) — the visual and copy rules used here.

Reveal.js runs the presentation. Inter handles headlines; monospace labels handle the machinery. Both are bundled locally with their licenses in `vendor/LICENSE` and `assets/Inter-LICENSE.txt`.

This is an independent interview project, not an official PlanetScale deck. Customer artwork and published charts belong to their respective owners.
