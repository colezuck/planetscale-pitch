# Depot Metal: original art provenance

Retrieved October 4, 2026 for the TeachBack, at Cole’s request.

- Original article: [8x faster queries with PlanetScale Metal](https://depot.dev/blog/faster-database-with-planetscale-metal), Jacob Gillespie, CTO, March 11, 2025.
- Original chart file: [published CPU/iowait WebP](https://depot.dev/images/faster-database-with-planetscale-metal-iowait.webp).
- Local original: [depot-iowait-original.webp](../../decks/teach-back/assets/depot-iowait-original.webp), 720×202 pixels, 9,508 bytes.
- SHA-256: `6faa681e2e24de851880c8150630fe6694183b581876e8f51abd5002dd771cbf`.

The article’s substantive chart shows stacked CPU usage across January 22–28. Its legend includes iowait, irq, nice, softirq, steal, system and user. Depot reports that I/O wait disappeared after the move. Preserve original pixels and the complete axes/legend; do not trace new curves or add a precise migration timestamp. The source file is unchanged. CSS `invert(.93) hue-rotate(180deg)` adapts chart colors and text to the dark deck while transforming the legend consistently. This is CPU evidence, not a percentile-latency plot.

The source uses Vitess/MySQL, PS-400 with eight CPUs → M-320 with four CPUs. Different CPU counts mean the full drop in chart height cannot be attributed solely to faster disk. Depot’s query table separately gives p95 40→5 ms and p99 50→30 ms. The current slide uses large typography for these exact values. Its retention art is a schematic of removed 7/30/90-day plan limits, not capacity telemetry.

Depot’s article also has a generic blog banner; it adds little evidence and is omitted. PlanetScale’s case-study listing points to the same original Depot article. The source is attributed in preparation documents and accessible image descriptions; no asset ownership or broad reuse license is asserted.
