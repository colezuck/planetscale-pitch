# Motion, builds, and review

## Animate a reasoning step

The current deck uses Reveal.js with a fixed 1440 × 810 slide view, hash navigation, and `transition:'none'` between slides. The SVG/HTML changes happen through fragments and CSS state classes. Use short opacity transitions (the reference uses about 250 ms) rather than decorative fly-ins. Honor `prefers-reduced-motion`.

Plan each settled state before implementation. A reveal should add a constraint, show a changed system, or introduce evidence. Keep the buyer's anchor text stable except where a heading change is the explicit reasoning step.

### Proven patterns

- **Nexus:** base compute/network storage → more capacity → unresolved latency/I/O/availability questions. `updateNexusState()` derives `.nexus-scaled` and `.nexus-revealed` from fragment visibility, swaps the two headings, and hides obsolete connectors.
- **Intercom:** peak-load bottleneck → more replicas/io2 headroom at higher cost → original cost chart. `updateIntercomState()` changes the schematic; a fade-out/fade-in pair swaps the main visual on the same fragment index while retaining the result headline.

Put fragment groups in the diagram, with explicit `data-fragment-index` values. Use the same index for elements that change together. Do not stack two readable charts/diagrams at once during a cross-fade. Keep stable geometry so labels and connectors do not jump or flash. Hidden content needs appropriate visibility and accessibility treatment, not just a transparent overlapping label.

State is derived from the visible fragments, not a click counter. Subscribe to `fragmentshown`, `fragmenthidden`, and `slidechanged`; reconcile after initialization. Scope queries to the slide and guard optional/missing elements. This keeps backward navigation, direct hashes, and revisits correct. Test entry by direct hash, forward/back reveal, and return from the next slide. The starter omits Metal-specific handlers and registers the shared `ps-diagrams` plugin for declarative scenes. Use [the shared framework](../../../../shared/presentation/README.md) for smooth node/connection geometry changes. Keep bespoke handlers only for effects outside that contract.

## New deck shell

From the repository root:

```sh
python3 .agents/skills/planetscale-pitch-design/scripts/new_deck.py --name teach-back --title 'PlanetScale Metal'
python3 decks/teach-back/build.py
python3 decks/teach-back/package.py
npm run serve
```

The helper refuses an existing implementation; an existing planning README alone is allowed. It copies the proven local runtime, brand/font assets, base canvas styling, and controls, without copying the old sales story or product claims. It writes a minimal opening slide for replacement. It does not add the deck to deployment.

`content.json` contains `{id, label, theme, html}` records, or a `diagramFile` path instead of `html` for a declarative SVG scene. Builds copy the canonical shared runtime into ignored deck `runtime/` output. Edit copy/markup there and CSS in `theme.css`; edit `app.js` for behavior. Complex future content can use a Python source builder rather than forcing large diagrams into JSON. Keep one canonical content source. Scene states live in their diagram JSON; shared code lives in `shared/presentation/`. `build.py` creates audience `slides.js` and optionally presenter data from local `private/speaker-outline.json`. The private script maps slide IDs to arrays of spoken bullet points.

```sh
python3 decks/teach-back/build.py --presenter
python3 decks/teach-back/package.py --presenter
```

The starter produces `Audience.html` or ignored `private/Presenter.html`. Its packager embeds the local runtime, font, and static `assets/...` paths, including new PNG/JPEG/WebP/GIF/SVG images. It rejects missing assets and unresolved asset expressions. Dynamic image paths must be made explicit before packaging. Copy any reused image into the new deck's assets; outside paths or remote URLs do not produce a self-contained deliverable. Review animations separately if using an animated image format.

## Existing Metal deck

```sh
npm run build:pitch
npm run build:presenter    # When notes or presenter behavior changes
npm run build            # When deployment packaging needs verification
npm run check
```

Do not edit generated `slides.js` or `Meridian-PlanetScale.html`. Update the original build content, CSS, SVG, runtime, or packager. The Metal packager's legacy PDF path reads historical captures; use `--html-only` for normal builds. A PDF export is separately captured from the rendered current slide states and reviewed page by page. Keep the existing filename and published URLs stable.

## Review the actual artifact

Use the available browser control interface for visual inspection. Use read-only DOM inspection if available to diagnose geometry and image-loading failures; visual review remains necessary. Inspect all affected states at 16:9 after fonts and images are ready and transitions settle. A screenshot immediately after a keypress may show a cross-fade rather than the settled result.

Check:

- Titles, important labels, arrows, units, and chart legends fit and remain readable.
- The whole composition is vertically balanced; repeated structures share baselines.
- New images are loaded in both development and portable HTML.
- Forward, backward, and direct-hash entry produce the planned state.
- Notes never appear in audience content; presenter output still has the intended script.
- Exports reflect the actual current render rather than old QA images.

Run `npm run check` for repository navigation and baseline JavaScript syntax. For a new deck, also run `node --check decks/<name>/app.js` and `node --check decks/<name>/slides.js`. Historical QA JSON is useful evidence of prior checks, not proof that the current slide passes. Report meaningful limitations; do not claim a current visual check from an old capture.
