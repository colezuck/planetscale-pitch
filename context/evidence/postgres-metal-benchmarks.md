# Postgres on Metal benchmark reference

Reviewed 2026-09-27. Applies to the Postgres offer, not the separate Vitess/MySQL results or the Neki scale benchmark.

## Pitch decision

Use one benchmark slide after the customer story and operated-platform explanation. Its role is to substantiate the speed proposition and earn a workload evaluation. Show mixed-workload mean throughput beside interval p99 at the same concurrency. Keep the customer outcomes and Neki experiment on separate slides.

## What the tests measure

[Benchmark methodology](https://planetscale.com/blog/benchmarking-postgres): the TPCC-like test includes mixed reads and writes on approximately 500 GB; the separate read-only test uses approximately 300 GB. A third test runs `SELECT 1` repeatedly to isolate query-path overhead. They answer different questions and must not share a synthetic comparison axis. They are PlanetScale-run tests, not guarantees for another workload.

## Dataset used in this deck

[Benchmark index](https://planetscale.com/benchmarks) and [public chart data](https://planetscale.com/metal/benchmarks/postgres/iframe).

The v2 charts use **32 simultaneous connections, 300 seconds, TPCC-like, 500 GB**. Mean QPS is calculated from 300 published one-second samples. The latency trace preserves the published one-second p99 values. It is not a run-wide p99, and averaging the trace would not produce one.

| Provider | Mean QPS in the selected run | On-slide display |
| --- | ---: | ---: |
| PlanetScale Metal | 16,338.6276 | 16.3k |
| Amazon Aurora | 10,908.9315 | 10.9k |
| Google AlloyDB | 10,355.0109 | 10.4k |
| Supabase | 5,270.2068 | 5.3k |

The index's rounded headline figures and “up to” ratios describe a broader summary. Do not replace only the PlanetScale bar with its approximately 18k headline while retaining other providers' exact 32-connection values.

Raw QPS samples and provenance are in `decks/postgres-metal/qa/benchmark-qps.json`. The existing `decks/postgres-metal/qa/benchmark-p99.json` arrays were checked against the current public chart bundle on the review date and matched exactly. The selected latency ranges are 170.48–223.34 ms for PlanetScale and 325.98–733 ms for Aurora. A range of interval percentiles is not a latency distribution for every individual query.

## Configurations and interpretation

[PlanetScale versus Aurora](https://planetscale.com/benchmarks/aurora): M-320 and db.r8g.xlarge each use 4 vCPUs and 32 GB RAM. PlanetScale has 937 GB local NVMe; Aurora uses its storage service. The benchmark sends work to the primary. Pricing comparisons separately normalize replica capacity. Do not confuse a three-node price with aggregate three-node benchmark throughput.

The separate read-only comparison reports similar average QPS for PlanetScale and Aurora, with a consistency difference. That matters: the mixed-workload advantage is not a universal ratio across all database operations. Query-path tests also distinguish direct connections from pooled/routed ones.

[PlanetScale versus AlloyDB](https://planetscale.com/benchmarks/alloydb): both use 4 vCPUs and 32 GB RAM. PlanetScale runs in AWS us-east-1 and AlloyDB in GCP us-central1, with clients local to their respective regions. This is not a same-hardware experiment isolating one storage variable.

[PlanetScale versus Supabase](https://planetscale.com/benchmarks/supabase): the compared Supabase instance has 8 vCPUs, 32 GB RAM, 750 GB provisioned storage, and 12k IOPS. It has twice PlanetScale's CPU count to match RAM. Do not call the configurations identical. The page also discusses separate OrioleDB/io2 results; do not generalize these bars to every Supabase storage engine and configuration.

[Metal product explanation](https://planetscale.com/metal): compute and local NVMe share a server, avoiding the network-storage hop. “Unlimited IOPS” is product language for access to the drive's I/O without a separately provisioned IOPS tier; physical hardware remains finite. Storage capacity is selected explicitly. Never translate this into unlimited database size or infinite throughput.

## Speaker framing

“In this published mixed-workload run, Postgres on Metal sustains higher throughput and lower p99 than these configurations. We can assess those same measures with your queries, concurrency, data size, and latency targets.”

Keep provider names, units, dataset, concurrency, and duration visible. Keep source links and fuller hardware details in the research docs. Do not add an ROI estimate, current price quote, extrapolated annual saving, or a promise that the customer's latency will match the benchmark.


## Four-provider latency comparison

The p99 plot now includes AlloyDB and Supabase at 32 connections. Each has 300 published one-second samples; PlanetScale's samples match across the provider comparison datasets. Ranges: AlloyDB 277.21–1,235.62 ms; Supabase 196.89–1,561.52 ms. The shared linear axis is 0–1,600 ms; all samples are retained without smoothing or clipping. The x-axis aligns elapsed time in separate runs, not simultaneous wall-clock timestamps. Provenance is in `decks/postgres-metal/qa/benchmark-p99-provenance.json`. The visible workload footer was removed at the user's request; workload context remains in the speaker notes for spoken delivery.

The slide display now uses a 0–1,200 ms y-axis and clips higher values at the plot boundary. Raw samples remain unchanged; full ranges remain in speaker notes.
