# Corrections worth reusing

These are concrete lessons from the repository's retained evidence, QA, and final implementation. They are local decisions, not universal design prohibitions. The current source and rendered deck outrank chronological research notes describing abandoned layouts.

| Trigger or earlier approach | Preferred decision | Where the lesson comes from |
| --- | --- | --- |
| Reconstructing Convex p99 curves from pixels for native SVG | Use the original chart panels. Preserve all percentile lines, axes, legend, and missing/clipped evidence. Digitized data remains historical. | `context/evidence/customer-case-studies.md`, “Original Convex chart panels replace the reconstruction” |
| Stacking enlarged Convex charts and removing result spacing | The user restored side-by-side panels. The current render is the baseline; do not reintroduce the superseded stacked treatment as cleanup. | Same document, “Layout rollback”; current `theme.css` and `convex` slide |
| Research notes and previews have different titles, order, or slide count | Use canonical content and current rendered slide; those notes preserve history. | `build_content.py`, `architecture.md`, chronological customer notes |
| Adding throughput/IOPS claims to a customer latency story | No Convex-specific throughput/IOPS evidence was found in retained research. Do not substitute vendor benchmarks into its customer result. | Customer evidence, “Convex layout and metric scope” |
| Combining Autumn migration with later query tuning | Separate migration latency (~100 ms to <10 ms, no percentile) from later tuning (~200 ms to <50 ms p99 and CPU change). | Customer evidence, “Autumn follow-on story recommendation” |
| Treating Vitalize's 50-second average and 1.2-second maximum as paired p99 | Preserve their actual statistics; no comparable before p95 is supplied. | Customer evidence and private outline |
| Scaling an icon to fill space | Keep room for connector routes, labels, and the full composition; use size to express a meaningful distinction. | Existing design guidance and centering QA |
| Checking only the final diagram | Review initial, intermediate, reverse, and revisit states; reconcile classes from fragment visibility. | Nexus/Intercom handlers in current `app.js` |
| Capturing immediately after reveal | Wait for the settled state; a cross-fade can briefly show outgoing art behind the chart. | Current 250 ms CSS transitions; browser inspection |
| Image works in local source but is missing in portable HTML | Update the existing packager's asset list or use the new shell's static asset embedding. Inspect the portable file. | `package_deck.py` |
| Rebuilding PDF from old `qa/slide-*.png` | Capture the current slide and meaningful reveal states; preserve 16:9 and inspect every exported page. | Deck architecture and root agent guidance |
| Rebuilt portable HTML still shows old code or typography | Reload the rebuilt source and verify its scene/state in the DOM. For a cached portable preview, use one explicit build-version query on the local URL. | Diagram-lab browser validation |
| Treating speaker prose as verified product documentation | Reuse its question/impact structure, not unsupported superlatives or historical availability language. | Private outline compared with dated product research |

When a new correction recurs or is likely to matter again, add its trigger, concrete fix, and source here. Keep one-off requested layouts scoped to the relevant slide. Do not accumulate speculative restrictions.
