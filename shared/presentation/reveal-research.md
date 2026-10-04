# Reveal.js animation choices

Reviewed October 4, 2026 against official documentation and the repository's bundled **Reveal.js 5.2.0**. Keep that local runtime pinned while this framework is tested; no dependency upgrade is needed for the implemented features.

## Within a slide

Reveal [fragments](https://revealjs.com/fragments/) provide incremental steps, explicit ordering with `data-fragment-index`, and grouped elements sharing an index. `.visible` persists after a step, while `.current-fragment` identifies the active step. Custom fragments opt out of the default fade. `fragmentshown` and `fragmenthidden` expose navigation changes.

Our design choice: zero-size custom fragment markers select declarative scene states. The plugin reads visible markers and interpolates SVG geometry. Stable node identity keeps labels and connector endpoints tied to the same objects. This geometric interpolation is our implementation, not a built-in Reveal SVG morphing feature.

The original Nexus uses visible SVG overlay groups and CSS state classes. That remains a valid approach for staged replacement. The new runtime supports movement and resizing without duplicating a complete diagram at every stage.

## Between slides

Reveal [Auto-Animate](https://revealjs.com/auto-animate/) matches elements across adjacent slides marked `data-auto-animate`. Explicit `data-id` improves matching; settings control duration, easing, unmatched elements, and animation grouping.

Use it for separate slide layouts where continuity between matched elements helps the story. This framework keeps a multi-step diagram on one slide so its slide count, heading context, and speaker notes remain coherent. Do not assume Auto-Animate interpolates arbitrary SVG `d` paths; its documented matching/CSS behavior does not promise a general path-morph engine.

## Lifecycle and controls

Reveal [events](https://revealjs.com/events/) provide readiness, slide changes, and slide-transition completion. Ready/revisit events settle the selected diagram state; fragment events animate a change within the active slide. This handles direct fragment hashes without starting an unwanted base-to-final tween during initial load.

The [API](https://revealjs.com/api/) exposes fragment navigation, available fragment directions, and synchronization methods. The starter's Previous/Next buttons use fragment availability as well as slide position, so first/last-slide fragment steps stay reachable. Layout/sync calls are useful when structure changes; they are unnecessary on every animation frame when only SVG geometry changes.

The runtime is registered through the documented [plugin mechanism](https://revealjs.com/plugins/). It is local and packaged with the deck; no remote animation dependency is required.

These sources establish Reveal's capabilities. Durations, easing, SVG primitives, port routing, and the authoring schema are repository conventions chosen for the PlanetScale visual style.
