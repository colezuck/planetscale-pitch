# Visual system and slide recipes

Current implementation: [theme.css](../../../../decks/postgres-metal/theme.css), [source assets](../../../../decks/postgres-metal/assets/), and [build_content.py](../../../../decks/postgres-metal/build_content.py). Inspect the current rendered slide before adapting its layout; `assets/previews/` and historical QA images are not the final design.

## Geometry and typography

The Reveal canvas is 1440 × 810. Sections use 60 px vertical and 64 px horizontal padding. Main content sits at `top:50%` with `translateY(-50%)`; the available width is 1312 px. Budget heading, spacing, art, and lower labels as one composition. Balanced margins follow from composition height, not arbitrary absolute offsets added repeatedly.

The current base uses 88 px h1, 56 px h2, 25 px monospace h3, and 25 px body. The cover uses a 112 px title. These are CSS pixels on the source canvas, not PowerPoint points. Match the selected reference slide; the actual chart labels vary by density. Do not shrink readable evidence to fit an additional sentence. Shorten, split, or choose a different composition.

| Token | Use |
| --- | --- |
| #111111 | Background and label backing |
| #fafafa | Main text |
| #a5a5a5 | Secondary labels |
| #414141 | Muted CSS borders; SVG frames may use brighter thin strokes |
| #f35815 | Metal, changed mechanism, outcome emphasis |
| #ff4d4d | Bottleneck or pressure |
| #fbca00 | Neki-specific story in the reference deck |

Use Inter for titles and prose; system monospace for node names, units, and measurements. Preserve official logo proportions and actual brand colors. Keep technical art sharp: square frames, occasional double outline on an emphasized node, sparse stipple on hardware, restrained directional arrows. Distinguish application, query path, replica, storage, and control plane by boundaries and labels rather than decorative icons.

## Recipes

| Job | Composition | Reference |
| --- | --- | --- |
| Introduce subject | One brand lockup and one product title, centered | `opening` |
| Explain why capacity may not solve a constraint | Stable schematic, grow resource shapes, reveal unresolved questions | `nexus` |
| Show customer proof | Original chart panels with readable axes/legend and separate result callouts | `convex` |
| Explain pressure and workaround | Stable outcome headline; diagram changes, then replaces with original cost chart | `intercom` |
| Explain mechanism | Parallel columns with consistent boundaries; highlight the changed path | `metal-path` |
| Explain operating model | Large topology; explicit primary/replica paths; control plane outside query path | `availability` |
| Compare measurements | Aligned plots, units, legend, workload context; no synthetic shared axis | `metal` |
| Close on evaluation | Migration or workflow diagram; readable choice labels and one concrete next step | `migration` |

Choose one dominant visual and a reading order. Avoid unrelated card grids, pill labels, decorative gradients, and crowded dashboards. A frame can represent a real system boundary; a collection of framed facts is not automatically an architecture diagram. Existing small metric boxes or controls do not justify turning every slide into UI.

## Diagrams and art

Use editable SVG for explanatory technical diagrams in this HTML workflow. Reuse current standalone assets where the mechanism is unchanged; otherwise build a schematic from explicit topology and evidence. Decorative illustration or photographic art can use image generation when requested or useful; follow the available image-generation skill/tool. Do not turn an AI-generated diagram into evidence about a real architecture.

Give SVG a viewBox, title/description or accessible label, and stable fragment groups. Use deck/slide-specific marker and pattern IDs when SVGs are inserted inline into one document; duplicate IDs can make arrows or fills use another slide's definitions. Leave room for arrowheads and captions. Use dashed lines only where the meaning is explicit. Show replica/control-plane responsibilities accurately; local NVMe by itself is not HA.

Scale art to fit the composition instead of making a symbol so large it displaces connectors or labels. Do not change topology merely to make a balanced picture. Label omitted components or illustrative counts in the accessible description or source context when relevant.

## Images, logos, and original charts

1. Store the original file in the target deck's `assets/`. Record source URL or supplied filename, retrieval date, rights/brand provenance where known, and what the image establishes in context or a concise asset note.
2. Use semantic `img` markup with meaningful alt text. Give it a reserved frame/aspect ratio to avoid loading shifts. Use `object-fit:contain` for logos, technical screenshots, and charts. Crop editorial photography only when the crop preserves the intended subject; use `cover` deliberately.
3. For chart panels, a clipping viewport is acceptable when axes, legend, labels, and the evidence being discussed remain visible. Preserve the original pixels; callouts can convert units with the conversion stated. Do not trace replacement curves or invent data to fit the palette.
4. The current Convex panel uses CSS color inversion/hue rotation for dark-slide readability. That changes presentation colors, not values; do not apply it blindly to a logo or a chart whose color legend becomes ambiguous.
5. Embed assets into the portable output and inspect that output. The existing Metal packager has an explicit asset list: adding a source `img` requires updating packaging too. New shells use the generic starter packager for static `assets/...` references.

Keep source logos unmodified. Do not invent a colored Autumn logo or recolor an official symbol just to match Metal orange. Prefer appropriate official variants. A bitmap picture and an editable diagram serve different jobs; choose the asset type deliberately.
