# Diagram framework

Author a system once, then describe the states of the explanation. The compiler creates editable inline SVG; Reveal fragments select a state; a local plugin animates the same objects between states. This extends the Nexus visual language with geometric interpolation while retaining its capacity → larger resources → unanswered questions story.

## Start with the working example

```sh
npm run build:diagrams
npm run test:diagrams
npm run serve
```

Open `/decks/diagram-lab/index.html#/capacity-model` on the local server. Press Right twice, then Left to reverse. The portable [diagram lab](../../decks/diagram-lab/Audience.html) includes the runtime, fonts, and SVG without network dependencies. It is a development example and is not included in site deployment.

Canonical files:

| File | Responsibility |
| --- | --- |
| [examples/capacity-model.json](examples/capacity-model.json) | Editable nodes, ports, stage overrides, and story text |
| [diagram_scene.py](diagram_scene.py) | Validation, independent stage snapshots, inline SVG, fragment triggers |
| [diagram-motion.js](diagram-motion.js) | Reveal plugin, interpolation, connection geometry, navigation state |
| [diagram-motion.css](diagram-motion.css) | Canvas integration and fragment trigger styling |
| [Reveal.js research](reveal-research.md) | Official APIs, chosen approach, compatibility boundaries |
| [Scene authoring guide](scene-authoring.md) | Schema, geometry, image choices, motion rules |

The existing Metal deck retains its original SVG and animation handlers. The starter includes this framework for new decks. Its build refreshes `runtime/` from these canonical files; those copies are ignored by Git. Avoid editing copied runtime files.

## Use in a new deck

Create the deck with the [slide skill](../../.agents/skills/planetscale-pitch-design/SKILL.md). Store your scene JSON in that deck's `diagrams/` folder and use a slide record like:

```json
{
  "id": "capacity-model",
  "label": "Capacity model",
  "theme": "diagram-slide",
  "diagramFile": "diagrams/capacity-model.json"
}
```

Provide either `html` or `diagramFile`. Run the deck's `build.py`, then `package.py`; the generated slide contains the SVG and Reveal steps. Namespaced scene IDs must be unique across the deck. Source geometry stays in scene JSON; dynamic SVG attributes are derived output.

For an existing shell, include `diagram-motion.css` and `diagram-motion.js`, and register `PlanetScaleDiagrams.createPlugin()` in Reveal's `plugins` array. Each deck gets its own plugin instance. Keep the input diagram inline in the slide: an SVG loaded through an `img` is isolated from fragment and DOM control.

## Motion contract

A stage is a complete target derived from sparse overrides. Navigation reads Reveal's visible fragment state, including reverse navigation. An interrupted animation retargets from the currently drawn geometry. Boxes resize without stretching text; connector ports are recomputed on every frame. Labels change through a fade rather than an overlapping pair of readable labels.

Default duration is 380 ms with cubic ease-out; the example uses 420 ms. Stage changes on entry/revisit settle immediately. `prefers-reduced-motion` and `duration: 0` settle without tweening. The runtime cancels active frames during retargeting and plugin destruction. The plugin's `settle()` method provides a deterministic final render for a capture tool after navigation; this does not change the selected fragment.

Review initial, intermediate, settled, reverse, direct-hash, and revisit behavior. The test suite checks snapshot isolation, valid geometry/ports, safe SVG text, moving connector endpoints, and interrupted reverse motion. Browser review is still needed for typography, overlaps, and visual quality.

Geometry is explicitly authored. The current router makes simple orthogonal connections; route clearance around unrelated nodes needs visual review. General SVG path morphing, automatic diagram layout, and particle traffic animation are outside this first implementation.
