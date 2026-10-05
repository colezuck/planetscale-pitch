# Scene authoring

Use [capacity-model.json](examples/capacity-model.json) as the complete working example. [The slide skill](../../.agents/skills/planetscale-pitch-design/SKILL.md) owns sales messaging, evidence, and visual decisions; this guide owns the executable diagram contract.

## Scene

Required fields: `id`, `title`, `description`, nonempty `nodes`, and nonempty `stages`. Optional: `links`, `width` (1250), `height` (470), `duration` in milliseconds (380). Scene/node/link/stage names use lowercase hyphenated identifiers beginning with a letter. Scene IDs namespace SVG title/description/pattern/marker IDs and must be unique within a deck.

Descriptions identify what the picture explains and what it omits. Use source/context documents for detailed citations. Each stage has its own description so the accessible explanation follows the drawn state. Capacity counts and decorative pin counts are illustrative; do not present them as telemetry.

## Nodes

Each node has `id`, `kind`, `x`, `y`, `w`, `h`, and `label`. Coordinates use the SVG viewBox, independently of the 1440 × 810 Reveal canvas. A newline creates another label line. Frame dimensions and font sizes must remain readable after scaling into the slide.

| Kind | Treatment |
| --- | --- |
| `container` | Square system frame, inner outline, left-aligned header |
| `chip` | Hardware frame, pins, centered label |
| `memory` | Frame, lower pins, centered label |
| `storage` | Stippled boundary, inner frame, small disk icon and centered multiline label |
| `callout` | Red stipple/frame for a constraint or buyer question |
| `label` | Text region without a frame |

Optional `iconScale` (0.25–4, default 1) scales the storage glyph independently of its label and frame. Override it in a stage to animate glyph growth; reserve space for the largest glyph.

Optional fields: `stroke`, `fill`, `color` as `#RRGGBB`; `fontSize`; `opacity` from 0 to 1. Defaults are muted border, dark fill, white text, 28px label, and full opacity. Font size range is 12–64 source SVG pixels; this validates numeric plausibility, not audience readability. Nodes including hardware pin extents must stay inside the viewBox. Reserve enough room for all stages, including initially hidden callouts.

Nodes are independent objects with explicitly authored geometry. To resize a container and its inner CPU/memory, override each affected node. This lets labels stay the same font size while frames expand. It also makes component relationships visible in the source rather than implied by automatic layout.

## Connections

Links have `id`, `from`, and `to`. Each endpoint selects a `node`, a `side` (`left`, `right`, `top`, `bottom`), and an optional fractional `at` position (0.5 default). For example:

```json
{
  "id": "reads",
  "from": {"node": "compute", "side": "right", "at": 0.44},
  "to": {"node": "storage", "side": "left", "at": 0.45},
  "label": "Network I/O",
  "labelOffset": -34
}
```

Optional: `stroke`, `opacity`, `label`, `labelOffset` (vertical offset), and boolean `dashed`. Arrowheads are namespaced per link. The router recomputes an orthogonal path from the current node boundaries every frame. Keep a clear connection corridor and review elbows, label placement, and arrowheads during movement.

Smooth resizing supports stable source/target node identities and port sides. For a topology change that reattaches a link to a different node or side, use separate predeclared links with an opacity handoff. The runtime's discrete reattachment switches at the animation midpoint and does not imply a continuous topology morph.

## Stages

Stages define `name`, `heading`, `description`, optional `emphasis` (a heading substring styled in Metal orange), and optional `nodes`/`links` override maps. Overrides accumulate from the previous stage, then compile into independent complete snapshots. Every stage can therefore be reached or reversed without replaying all preceding animations. Stage names are unique.

Predeclare all nodes and links, using `opacity: 0` for later appearances. Geometry, labels, colors, font sizes, opacity, and ports may change; node identity and kind stay stable. Unknown override fields/IDs fail the build, catching misspellings rather than silently ignoring them.

The first stage is the initial state. Subsequent stages become fragment indices 0, 1, and so on. The example has base → more capacity → unresolved questions. Direct URL `#/capacity-model/1` selects its third state because Reveal fragment indices are zero-based.

## Images and other art

Use normal slide HTML for logos, photos, screenshots, and original customer charts, following the skill's image/packaging rules. This first scene schema contains semantic vector primitives. It does not convert customer screenshots into fabricated curves or inferred topology. Frame an SVG diagram and an image together in slide HTML when that composition serves the buyer question.

## Builds and review

For a new deck created by the starter, set `diagramFile` in `content.json`, run `build.py`, then `package.py`. For the lab, edit the canonical example and run `npm run build:diagrams`; its scene/runtime copies are generated.

The compiler also supports:

```sh
python3 shared/presentation/diagram_scene.py shared/presentation/examples/capacity-model.json --output /tmp/capacity-diagram.html
```

That output is inline SVG/fragment markup intended for a Reveal slide. Its initial SVG geometry is present before the plugin runs; later states require the included runtime. Capture a final state only after `data-ps-animating="false"`, fonts and images have loaded, and the target fragment is selected.
