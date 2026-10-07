# Teach-back presentation

Five-slide Reveal.js TeachBack for an Aurora PostgreSQL engineer, framed through customer experience, growth capacity and managed availability. Intro → Impact of Metal (three benefits with static line illustrations) → Intercom business outcome → combined Metal/Aurora comparison → original Postgres benchmark. Convex, Depot and tradeoffs are retained with `hidden: true`; capacity planning stays in the spoken notes.

Read the [slide plan](../../interview/teach-back/slide-plan.md), [speaking script](../../interview/teach-back/script-outline.md), [Q&A](../../interview/teach-back/questions.md), and [evidence](../../context/product/aurora-metal-teach-back.md). Intercom’s 60%+ reduction compares database cost to previous EBS io2, and its case uses Vitess/MySQL. It is not a Postgres performance claim or total cloud-bill reduction.

Run from the repository root:

```sh
npm run build:teach-back
npm run build:teach-back:presenter
npm run serve
```

Development: `/decks/teach-back/index.html`. Portable audience: [Audience.html](Audience.html). Presenter: `/decks/teach-back/private/Presenter.html`; click **Notes** for the current slide’s short script and understanding question, or use **S** for Reveal speaker view in a browser that permits the popup. The presenter build derives notes from the tracked outline and embeds them in ignored private HTML. Audience output excludes all speaker notes. Share only the slide window.

Edit `content.json` for copy/order, `assets/metal-path.svg` for the combined comparison (`diagrams/aurora.json` retains the hidden Aurora diagram), `theme.css` for layout and `app.js` for behavior. Generated `slides.js`, `Audience.html` and runtime copies are not editable sources. Portable builds embed images, fonts and runtime. This deck is local and excluded from the published site.

The Metal comparison adapts the original pitch hardware geometry to Aurora’s DB instance and shared distributed SSD storage versus Metal’s persistent local NVMe. Static storage-access examples are retained: ~1 ms from a PlanetScale network-storage workload and ~50 µs from a local-NVMe educational example. Labels identify them as examples; they are not Aurora measurements or a matched test. The standalone Aurora slide is retained but hidden. HA explanation is in the notes; local NVMe alone does not supply HA.

Intercom logo and original cost chart are copied unchanged from the Postgres pitch assets. [Provenance and claim scope](../../context/evidence/intercom-teach-back.md). Hidden Convex and Depot assets remain available. No PDF regenerated; aloud five-minute timing remains to be rehearsed.
