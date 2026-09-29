# PlanetScale customer evidence

Reviewed: 2026-09-27. Durable research context for the Postgres on Metal pitch. These are customer-reported experiences, not controlled benchmarks or promises for another workload. Keep this reference in the repository; use selected evidence in the deck and retain source links in research docs.

## Autumn

Source: [Migrating Autumn to PlanetScale](https://useautumn.com/blog/migrating-to-planetscale), John, 2026-04-20.

- **Workload:** Billing infrastructure for AI companies; real-time access and credit checks sit in customers' request paths.
- **Move:** Unnamed previous Postgres provider to PlanetScale Metal. Prior issues included connection pooling, upgrades, and variable latency.
- **Migration:** Two days; seconds of cutover downtime. PlanetScale's team helped and recommended its pgcopydb fork.
- **Results:** General query latency around 100 ms became consistently under 10 ms. The article does not assign a percentile to these values.
- **Separate optimization:** After support helped with indexing/query changes, CPU use fell from 40% to under 10%; the heavily used query's p99 fell from around 200 ms to under 50 ms. Do not attribute this entire improvement to the hosting move.
- **Best pitch use:** Strong combined story for Metal performance, migration assistance, and the infrastructure team. Particularly relevant to an application with database calls in the critical path.
- **Visual option:** Two clearly separated comparisons: migration latency and subsequent query p99 optimization. Never merge their baselines.
- **Boundary:** Do not infer the previous provider, promise a two-day migration, or turn reported support responsiveness into an SLA.

## OpenSecret / Maple AI

Source: [Why We Migrated from Neon to PlanetScale](https://blog.opensecret.cloud/why-we-migrated-from-neon-to-planetscale/), Anthony Ronning, 2025-08-12.

- **Workload:** Always-on private AI chat; confidential computing with encrypted data in the database.
- **Move:** Neon to PlanetScale Postgres. The author emphasizes availability, observability, and operating effort.
- **Migration:** Reports zero downtime using PlanetScale migration scripts and support. Their encrypted-blob workload had limited transformation complexity.
- **Results:** Slowest billing API endpoint: 550 ms to 300 ms. Database p99 after migration: 1.0 ms, with no comparable prior p99 supplied. Keep API response time and database latency distinct.
- **Historical cost:** $250/month for four databases without replicas versus $156/month for four databases and eight replicas. These describe the author's 2025 deployment, not current pricing or identical configurations.
- **Best pitch use:** Reliability, replica coverage, query visibility, and a small team's migration experience.
- **Visual option:** Paired API endpoint bars; show post-migration database p99 separately.
- **Boundary:** The article identifies Metal as a tier to explore later. Do not present these as Metal results. Reported prior outages and provider limitations are the author's experience at that time; do not generalize them into current competitor claims. The report of no subsequent downtime has no precise observation duration.

## Convex / Chef

Source: [Powered by PlanetScale for Postgres](https://news.convex.dev/powered-by-planetscale-for-postgres/), Jamie Turner, 2025-07-01.

- **Workload:** Convex's backend platform; the measured example is Chef's message histories and project snapshots.
- **Move:** AWS Aurora to PlanetScale for Postgres. The article announces a launch partnership and rollout.
- **Results:** Chef query p99 changed from a variable 10–15 ms to a steadier 5–7 ms. Batch-commit p99 previously spiked between 75–200 ms and subsequently stayed around 20 ms.
- **Best pitch use:** Strongest supplied customer evidence for a matched before/after percentile and reduced tail-latency variability. Also supports credibility with an infrastructure buyer.
- **Visual option:** Two separate range comparisons: query p99 and batch-commit p99. Preserve ranges instead of inventing averages or a continuous time series. The article contains an original results chart that can be inspected if selected.
- **Boundary:** Results belong to Chef, not every Convex project or every query. The old Aurora engine and full hardware configuration are not specified in this article. No quantified migration downtime is supplied. Do not treat the launch-era rollout statement as a freshly verified current fleet inventory.

## Supermemory

Source: [Supermemory just got faster on PlanetScale](https://supermemory.ai/blog/supermemory-just-got-faster-on-planetscale/), Dhravya Shah, 2025-07-18.

- **Workload:** AI memory, document ingestion/retrieval, and vector-related data.
- **Move:** TigerData, formerly Timescale, to PlanetScale. The article emphasizes performance, observability, and migration partnership.
- **Migration:** Hands-on help and a proxy script; reports no user interruption.
- **Results:** Reported QPS rose from 20 to 1,000. Monthly cost fell from $900 to $90. Database p99 after migration was below 6 ms; no prior p99 is given.
- **Best pitch use:** Ingestion/retrieval applications, customer-reported throughput gains, and migration support.
- **Visual option:** QPS comparison with a distinct after-migration p99 figure. Use the cost comparison only when its historical context is relevant.
- **Boundary:** No matched hardware, concurrency, measurement duration, or controlled workload definition is provided. Do not describe 50x as a universal engine speedup or a vector-search benchmark. The article does not explicitly identify the hardware tier as Metal. Reported costs are historical, not a quote.

## Selection guide

| Buyer concern | Best starting evidence | Reason |
| --- | --- | --- |
| Migration support plus Metal performance | Autumn | Explicit Metal deployment and concrete support/migration account |
| Comparable p99 before and after | Convex / Chef | Same percentile is supplied on both sides |
| Reliability and operating effort | OpenSecret | Always-on application, replica coverage, and observability |
| Retrieval workload and throughput | Supermemory | Customer-reported QPS and migration experience |
| Moderate Postgres dataset and compute reduction | Vitalize | Existing deck's 400 GB / 150 million row example |
| Team experience at very large scale | Cash App | Existing Vitess/MySQL case; keep product identity explicit |

## Existing deck evidence

- [Vitalize](https://vitalize.care/blog/from-supabase-to-planetscale): 400 GB, 150 million rows; 4 to 2 vCPUs at 16 GB RAM; reported after-migration p95 around 2 ms. No comparable before p95. The JSONB read comparison uses different statistics (50 s average versus 1.2 s maximum).
- [Cash App](https://planetscale.com/case-studies/cash-app): Vitess/MySQL operating-scale evidence, not a Postgres or Neki customer result. Preserve its separate role in the pitch.

## Current working-deck selection

The user requested two additional slides while preserving Vitalize and the existing migration close. Convex and Autumn are appended as slides 8 and 9 for comparison; the working deck has nine slides. Final sequencing remains undecided. The recommended eventual pairing is Convex for early technical proof and Autumn for migration partnership. Vitalize remains available as the compute-efficiency story.

## Customer logo provenance

- Convex: unmodified white logo from the [official brand kit](https://www.convex.dev/brand), downloaded from `https://www.convex.dev/resources/logos.zip`, entry `Logos/SVG/logo-white.svg`.
- Autumn: official website navbar logo, `https://useautumn.com/images/navbar/autumnlogo.svg`. The slide uses the same white-on-dark CSS treatment shown by Autumn's site footer.


## Customer-slide visual refinement — 2026-09-27

Convex now uses two p99 curves reconstructed from its original published chart. The red p99 traces are digitized at source-pixel resolution by `qa/digitize_convex.py`, persisted in `qa/convex-p99-digitized.json`, and rendered as native SVG. This is approximate image-derived data, not raw telemetry. Missing pixels remain gaps, including query peaks clipped above 20 ms in the source. The white/orange boundary follows the visible step around 23:55; it is not an independently established cutover timestamp. Callouts use the article’s explicit 10–15 → 5–7 ms and 75–200 ms spikes → ~20 ms claims, rather than statistics recomputed from pixels. Other percentile lines are intentionally omitted.

Original Convex chart: https://storage.ghost.io/c/e6/e9/e6e9d6ca-a1ad-4d1c-bd58-d32798cd446c/content/images/2025/07/Screenshot-2025-07-01-at-7.59.02---AM-2.png

Autumn uses an approximate 100 ms baseline and a dashed 10 ms upper-bound bar, labelled <10 ms. This is general query latency, with no published percentile. The previous provider remains unnamed. Its Insights screenshot (`assets/autumn-original-insights.png`) is retained as research evidence only: it is not a paired migration comparison. The later ~200 → <50 ms p99 and 40% → <10% CPU improvements followed query/index tuning, so they remain separate from the migration result.

Original Autumn chart: https://useautumn.com/images/blog/planetscale-insights.png

Brand assets: Convex’s unmodified color symbol and white wordmark come from https://www.convex.dev/resources/logos.zip . Autumn’s current official logo at https://useautumn.com/images/navbar/autumnlogo.svg and official icon at https://useautumn.com/icon-192.png are monochrome. Keep the official logo rather than inventing a colored version.

Both stories remain candidate slides 8–9, with Vitalize and the original seven slide records preserved.


### Original Convex chart panels replace the reconstruction

The current slide now displays `assets/convex-original-results.png` directly in two CSS clipping viewports, one per original chart. The source PNG remains unchanged. `filter: invert(.93) hue-rotate(180deg) brightness(1.7) contrast(1.12)` changes only browser presentation colors to fit the dark deck. All five percentile lines, legends, ticks, and chart titles remain as published. Chart axes remain in seconds; the separate p99 summaries are in milliseconds. The digitized JSON/script above are historical research and no longer supply the slide.


### Convex layout and metric scope

The two original plots are now stacked at larger scale with their p99 callouts alongside. The subtitle and result dividers are removed. The full-color wordmark leads the headline, “Convex migrated and lowered p99.” Chart crops retain the plot areas and axis labels; the original percentile legend is shared alongside. The axes are still in seconds and summaries in milliseconds. Rechecked the original Convex post and searched Convex/PlanetScale sources on 2026-09-27: no Convex migration throughput or IOPS comparison was found. Do not substitute PlanetScale synthetic benchmark results for customer-specific metrics.


### Layout rollback

At user request, restored the side-by-side original chart panels, subtitle, dividers, and result spacing from commit 97e06c0. Retained the left-aligned Convex branding and “migrated and lowered p99” headline. The stacked layout above is superseded.


### Autumn follow-on story recommendation

For a separate infrastructure-team proof slide, prioritize the later engineer-assisted query/index tuning: one heavily used query’s p99 fell from ~200 ms to <50 ms, while CPU use fell from 40% to <10%. This occurred after migration and must not be combined with the migration’s ~100 ms to <10 ms general query latency baseline. Secondary talking points: pooling stopped being a bottleneck; Insights helped locate an incident-causing query within minutes. The current slide retains migration proof, with the title in the deck font and the official Autumn symbol. Source: https://useautumn.com/blog/migrating-to-planetscale
